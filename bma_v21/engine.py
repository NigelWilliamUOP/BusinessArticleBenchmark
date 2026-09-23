"""Offline calibration, frozen requests, auditable attempts and reporting.

This module makes no network calls. Mechanical fixture scores are never paper
passes or independently established scientific judgements. Python 3.10+.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import random
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from .catalogue import catalogue

VERSION = 'BMA-lifecycle-amendment-2.1.0'
GATES = ('completion','executability','result_validity','evidence_integrity','autonomy')
STATUSES = {'completed','agent_failure','infrastructure_failure','budget_exhausted','time_exhausted','human_rescue','abstained'}
HUMAN_FIELDS = ('production_minutes','operational_verification_minutes','rework_minutes','evaluation_minutes')
CONFIG = {
    'amendment_version': VERSION, 'parent_benchmark_version':'BMA-ARB-v0.1',
    'network_enabled':False, 'external_spend_authorised_gbp':0,
    'comparison':'matched_packet_and_equal_ceilings',
    'conditions':['fixed_lower','fixed_higher','routed'],
    'model_slots': {
        'lower':{'provider':None,'model_id':None,'reasoning_setting':None},
        'higher':{'provider':None,'model_id':None,'reasoning_setting':None}},
    'per_case_ceiling':{'wall_seconds':180,'output_tokens':1200,'cost_gbp':0},
    'routing':{'version':'ex_ante_static_1','higher_if_inferential_demand_at_least':2,
               'higher_if_temporal_updating_at_least':2,
               'learned_from_evaluation':False},
    'retry_policy':'No external restart within an attempt; every new attempt needs a new ID. No best-of selection.',
    'endpoint':'mechanical_decision_diagnostic_only',
    'private_holdouts_accessed':False,
}


def canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode('utf-8')


def digest(obj: Any) -> str:
    return hashlib.sha256(canonical(obj)).hexdigest()


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def number(value: Any, nullable: bool = False) -> bool:
    return (nullable and value is None) or (type(value) in (int, float) and math.isfinite(value) and value >= 0)


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as out:
        out.write(json.dumps(obj, indent=2, ensure_ascii=False, allow_nan=False)+'\n')


def read_json(path: Path) -> Any:
    def reject_constant(text):
        raise ValueError(f'Non-finite JSON constant: {text}')
    return json.loads(path.read_text(encoding='utf-8'), parse_constant=reject_constant)


def validate_cases(cases: list[dict]) -> None:
    ids = set()
    for case in cases:
        if case['case_id'] in ids:
            raise ValueError('Duplicate case ID')
        ids.add(case['case_id'])
        if case['source_kind'] != 'synthetic' or case['panel'] != 'public_synthetic_calibration':
            raise ValueError('This public runner accepts synthetic calibration only; use a separately audited prospective adapter.')
        if case['split'] not in ('calibration','development'):
            raise ValueError('Unknown or protected split')
        if not case['question'] or not case['evidence']:
            raise ValueError('Question and evidence are required')
        sources = {s['source_id'] for s in case['evidence']}
        ref = case['reference']
        if not set(ref['accepted_labels']).issubset(case['choices']) or not ref['accepted_labels']:
            raise ValueError('Invalid answer labels')
        if not set(ref['required_sources']).issubset(sources):
            raise ValueError('Reference uses unavailable evidence')
        if not number(ref['absolute_tolerance']):
            raise ValueError('Invalid numeric tolerance')
        if ref['numeric_value'] is not None and (type(ref['numeric_value']) not in (int,float) or not math.isfinite(ref['numeric_value'])):
            raise ValueError('Invalid numeric reference')


def release_readiness(cases: list[dict], config: dict) -> dict:
    """Fail closed. This public starter release is not a private scored panel."""
    blockers = []
    if any(c['source_kind']=='synthetic' for c in cases):
        blockers.append('Public synthetic examples cannot establish a prospective empirical benchmark result.')
    if any(c['audit']['status'] != 'independently_adjudicated' for c in cases):
        blockers.append('Reference answers and acceptable alternatives lack independent adjudication.')
    if any(any(slot.get(k) is None for k in ('provider','model_id','reasoning_setting')) for slot in config['model_slots'].values()):
        blockers.append('Exact model configurations are not assigned.')
    blockers.append('This implementation deliberately has no authorised live provider runner or private-panel importer.')
    return {'official_run_ready':False,'blockers':blockers,'mechanical_calibration_ready':True,
            'private_holdouts_accessed':False}


def select_slot(case: dict, condition: str, config: dict) -> str:
    if condition == 'fixed_lower': return 'lower'
    if condition == 'fixed_higher': return 'higher'
    if condition != 'routed': raise ValueError('Unknown comparison condition')
    policy = config['routing']
    if policy['learned_from_evaluation']:
        raise ValueError('Evaluation-selected routing is prohibited')
    profile = case['complexity']
    high = (profile['inferential_demand'] >= policy['higher_if_inferential_demand_at_least'] or
            profile['temporal_updating'] >= policy['higher_if_temporal_updating_at_least'])
    return 'higher' if high else 'lower'


def worker_request(case: dict) -> dict:
    """Allowlisted projection. No answer keys, audits, rationale or future material."""
    return {'case_id':case['case_id'], 'task_version':case['version'],
            'instruction':'Use only this synthetic evidence packet. Return one JSON object. Give a brief evidence-based justification, not private chain of thought.',
            'question':case['question'], 'evidence':case['evidence'], 'choices':case['choices'],
            'output_contract':{'case_id':'exact supplied ID','label':'one supplied choice',
                               'numeric_value':'number or null','source_ids':'array of cited supplied source IDs',
                               'justification':'brief explanation grounded in the supplied evidence'}}


def freeze(output: Path, config: dict | None = None) -> dict:
    config = CONFIG if config is None else config
    if output.exists(): raise FileExistsError('Freeze destination already exists; create a new version.')
    cases = catalogue()
    validate_cases(cases)
    output.mkdir(parents=True)
    write_json(output/'config.json', config)
    write_json(output/'evaluator'/'public_calibration_references.json', cases)
    for split in ('calibration','development'):
        rows = [worker_request(c) for c in cases if c['split']==split]
        write_json(output/'worker_packets'/f'{split}.json', rows)
    write_json(output/'readiness.json', release_readiness(cases,config))
    hashes = {str(p.relative_to(output)):hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(output.rglob('*.json'))}
    manifest = {'version':VERSION,'source':'original_public_synthetic_fixtures',
                'counts':dict(Counter(c['split'] for c in cases)), 'files':hashes,
                'manifest_sha256':digest(hashes)}
    write_json(output/'manifest.json',manifest)
    return manifest


def verify_freeze(root: Path) -> tuple[list[dict],dict]:
    manifest = read_json(root/'manifest.json')
    if digest(manifest['files']) != manifest['manifest_sha256']:
        raise ValueError('Manifest commitment changed')
    for name, expected in manifest['files'].items():
        path = (root/name).resolve()
        if root.resolve() not in path.parents:
            raise ValueError('Manifest path escapes root')
        if hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
            raise ValueError(f'Frozen file changed: {name}')
    cases = read_json(root/'evaluator'/'public_calibration_references.json')
    validate_cases(cases)
    return cases, read_json(root/'config.json')


def planned_jobs(cases: list[dict], config: dict, split: str) -> list[dict]:
    if split not in ('calibration','development'): raise ValueError('Public calibration/development only')
    jobs=[]
    for condition in config['conditions']:
        for case in [c for c in cases if c['split']==split]:
            request=worker_request(case)
            jobs.append({'job_id':digest([digest(config),condition,case['case_id'],case['version']])[:24],
                         'case_id':case['case_id'],'condition':condition,
                         'slot':select_slot(case,condition,config),
                         'request_sha256':digest(request),'config_sha256':digest(config),
                         'case_sha256':digest(case),'status':'planned',
                         'per_case_ceiling':config['per_case_ceiling']})
    return jobs


def prepare(root: Path, output: Path, split: str='calibration') -> dict:
    cases,config=verify_freeze(root)
    jobs=planned_jobs(cases,config,split)
    if output.exists(): raise FileExistsError('Request destination already exists')
    output.mkdir(parents=True)
    by_case={c['case_id']:c for c in cases}
    for job in jobs:
        write_json(output/'requests'/f"{job['job_id']}.json",worker_request(by_case[job['case_id']]))
    plan={'version':VERSION,'split':split,'config':config,'jobs':jobs,
          'plan_sha256':digest(jobs),'claim_limit':'Requests prepared; no model has been called.'}
    write_json(output/'plan.json',plan)
    return plan


class Ledger:
    """Single-writer append-only JSONL with a verifiable hash chain.

    This detects edits when the head is independently retained; it is not a
    cryptographic signature or an operating-system sandbox. Never share a writer.
    """
    def __init__(self, path: Path):
        self.path=path
        path.parent.mkdir(parents=True,exist_ok=True)

    def read(self) -> list[dict]:
        if not self.path.exists(): return []
        events=[]; previous='0'*64
        for line in self.path.read_text(encoding='utf-8').splitlines():
            event=json.loads(line)
            signature=event.pop('sha256')
            if event['previous_sha256']!=previous or digest(event)!=signature:
                raise ValueError('Ledger chain mismatch')
            event['sha256']=signature
            events.append(event); previous=signature
        return events

    def append(self, kind: str, run_id: str, payload: dict) -> dict:
        if not run_id or kind not in ('started','finished'): raise ValueError('Invalid event identity/type')
        events=self.read(); prior=[e for e in events if e['run_id']==run_id]
        if kind=='started' and prior: raise ValueError('Run ID already initiated; no hidden restart')
        if kind=='finished' and (len(prior)!=1 or prior[0]['kind']!='started'):
            raise ValueError('Finish requires one unmatched initiation')
        if kind=='finished': validate_finish(payload)
        event={'sequence':len(events)+1,'at':now(),'kind':kind,'run_id':run_id,'payload':payload,
               'previous_sha256':events[-1]['sha256'] if events else '0'*64}
        event['sha256']=digest(event)
        with self.path.open('a',encoding='utf-8') as out:
            out.write(canonical(event).decode('utf-8')+'\n'); out.flush()
        return event


def validate_finish(record: dict) -> None:
    if record['status'] not in STATUSES: raise ValueError('Unknown terminal status')
    resources=record['resources']
    for field in ('direct_cost_gbp','wall_seconds',*HUMAN_FIELDS):
        if not number(resources.get(field),nullable=True): raise ValueError(f'Invalid resource: {field}')
    basis=resources.get('cost_basis')
    if basis not in ('provider_billed','estimate','unknown','synthetic_zero'):
        raise ValueError('Cost provenance required')
    if basis=='unknown' and resources.get('direct_cost_gbp') is not None:
        raise ValueError('Unknown cost cannot be a finite asserted total')
    if basis!='unknown' and resources.get('direct_cost_gbp') is None:
        raise ValueError('Known cost basis requires an amount')
    if basis=='synthetic_zero' and resources['direct_cost_gbp']!=0:
        raise ValueError('Synthetic zero must be zero')


def mechanical_grade(case: dict, prediction: Any) -> tuple[bool,str]:
    """Exact decision, numeric and citation checks; no semantic-rationale oracle."""
    if not isinstance(prediction,dict): return False,'malformed_prediction'
    if set(prediction)!={'case_id','label','numeric_value','source_ids','justification'}:
        return False,'prediction_schema_mismatch'
    if prediction.get('case_id')!=case['case_id']: return False,'case_id_mismatch'
    ref=case['reference']
    if prediction.get('label') not in ref['accepted_labels']: return False,'decision_mismatch'
    sources=prediction.get('source_ids')
    if not isinstance(sources,list) or not all(isinstance(x,str) for x in sources):
        return False,'invalid_citations'
    if not set(ref['required_sources']).issubset(sources) or not set(sources).issubset({s['source_id'] for s in case['evidence']}):
        return False,'invalid_citations'
    if not isinstance(prediction.get('justification'),str) or not prediction['justification'].strip():
        return False,'missing_justification'
    target=ref['numeric_value']; value=prediction.get('numeric_value')
    if target is None:
        if value is not None: return False,'unexpected_numeric_claim'
    elif type(value) not in (int,float) or not math.isfinite(value) or abs(value-target)>ref['absolute_tolerance']:
        return False,'numeric_mismatch'
    return True,'mechanical_checks_only'


def score_ledger(root: Path, plan_root: Path, ledger_path: Path) -> dict:
    cases,config=verify_freeze(root)
    by_case={c['case_id']:c for c in cases}
    plan=read_json(plan_root/'plan.json')
    if digest(plan['jobs'])!=plan['plan_sha256'] or digest(plan['config'])!=digest(config):
        raise ValueError('Plan or configuration changed')
    if plan['jobs']!=planned_jobs(cases,config,plan['split']):
        raise ValueError('Plan differs from the full preregistered case/configuration cross-product')
    jobs={j['job_id']:j for j in plan['jobs']}
    if len(jobs)!=len(plan['jobs']): raise ValueError('Duplicate job IDs')
    for job in jobs.values():
        case=by_case[job['case_id']]
        request=read_json(plan_root/'requests'/f"{job['job_id']}.json")
        if digest(case)!=job['case_sha256'] or digest(request)!=job['request_sha256'] or digest(config)!=job['config_sha256']:
            raise ValueError('Case, request or configuration mismatch')
        if request!=worker_request(case) or job['slot']!=select_slot(case,job['condition'],config):
            raise ValueError('Request projection or routing mismatch')
    events=Ledger(ledger_path).read()
    starts={}; finishes={}
    for event in events:
        run_id=event['run_id']
        if event['kind']=='started':
            if run_id in starts: raise ValueError('Duplicate initiation')
            job_id=event['payload']['job_id']
            if job_id not in jobs: raise ValueError('Run absent from frozen plan')
            starts[run_id]=job_id
        else:
            if run_id not in starts or run_id in finishes: raise ValueError('Invalid terminal event')
            validate_finish(event['payload']); finishes[run_id]=event['payload']
    # Each planned case has at most one primary attempt. Additional attempts need
    # a separately declared replicate plan; do not selectively retry test cases.
    if len(set(starts.values()))!=len(starts):
        raise ValueError('Multiple attempts for a primary planned job; declare a complete replicate panel')
    rows=[]
    for run_id,job_id in starts.items():
        job=jobs[job_id]; case=by_case[job['case_id']]; result=finishes.get(run_id)
        passed=False; reason='unfinished'; status='unfinished'; resources=None
        if result:
            status=result['status']; resources=result['resources']
            elapsed=resources.get('wall_seconds'); cost=resources.get('direct_cost_gbp')
            ceiling=job['per_case_ceiling']
            if elapsed is not None and elapsed>ceiling['wall_seconds']:
                reason='time_ceiling_breached'
            elif cost is not None and cost>ceiling['cost_gbp']:
                reason='cost_ceiling_breached'
            elif status=='completed':
                passed,reason=mechanical_grade(case,result.get('prediction'))
            else: reason=status
        rows.append({'run_id':run_id,'job_id':job_id,'case_id':case['case_id'],
                     'family':case['family'],'cluster_id':case['cluster_id'],
                     'condition':job['condition'],'slot':job['slot'],
                     'status':status,'mechanically_correct':passed,'reason':reason,'resources':resources})
    conditions={}
    for condition in config['conditions']:
        subset=[r for r in rows if r['condition']==condition]
        n=len(subset); correct=sum(r['mechanically_correct'] for r in subset)
        planned=sum(j['condition']==condition for j in jobs.values())
        conditions[condition]={'planned':planned,'initiated':n,'not_started':planned-n,
                               'mechanically_correct':correct,'mechanical_rate':correct/n if n else None,
                               'failures':dict(Counter(r['reason'] for r in subset if not r['mechanically_correct'])),
                               'families':{f:{'initiated':sum(r['family']==f for r in subset),
                                              'correct':sum(r['family']==f and r['mechanically_correct'] for r in subset)}
                                           for f in sorted({c['family'] for c in cases})}}
    return {'version':VERSION,'kind':'public_synthetic_mechanical_diagnostic',
            'raw_autonomous_task_pass_rate':None,'independent_scientific_decision_pass_rate':None,
            'claim_limit':'No LLM capability, paper pass, population share or independent scientific validity is established.',
            'all_primary_jobs_initiated':len(starts)==len(jobs),'conditions':conditions,'rows':rows,
            'ledger_head_sha256':events[-1]['sha256'] if events else None}


def paper_summary(records: list[dict]) -> dict:
    """Secondary adapter for already independently adjudicated end-to-end records.

    Exclude uninitiated plans. Every initiated failure stays in the denominator.
    A producer cannot independently award journal readiness. No conversion from
    decision-battery scores is accepted here. Human-time zero must be recorded.
    """
    seen=set(); counts=defaultdict(lambda:{'initiated':0,'passes':0,'qualified':0})
    for record in records:
        if record['run_id'] in seen: raise ValueError('Duplicate run ID')
        seen.add(record['run_id'])
        if record.get('initiated') is not True: continue
        if record.get('output_type') != 'paper':
            raise ValueError('Paper gates cannot score component decisions or other lifecycle outputs')
        key=(record['system_id'],record['panel'],record['output_type'])
        group=counts[key]; group['initiated']+=1
        gate=record.get('gates',{})
        reviewed=record.get('evaluation_authority')=='independent'
        no_rescue=record.get('substantive_human_rescue') is False
        passed=(record.get('status')=='completed' and reviewed and no_rescue and
                all(gate.get(k) is True for k in GATES))
        group['passes']+=int(passed)
        group['qualified']+=int(passed and record.get('journal_readiness')=='independently_qualified')
    return {'groups':[{'system_id':k[0],'panel':k[1],'output_type':k[2],**v,
                       'raw_autonomous_task_pass_rate':v['passes']/v['initiated']}
                      for k,v in counts.items()],
            'note':'No pooling across systems, panels or output types. Decision records are not accepted as paper evidence.'}


def cost_summary(resources: list[dict], qualified_outputs: int, hourly_rate_gbp: float | None=None) -> dict:
    if type(qualified_outputs) is not int or qualified_outputs<0 or qualified_outputs>len(resources):
        raise ValueError('Invalid qualified-output count; supply one resource record per initiated attempt')
    if hourly_rate_gbp is not None and not number(hourly_rate_gbp): raise ValueError('Invalid labour rate')
    direct=[]; operational=[]; evaluation=[]; basis=Counter()
    for row in resources:
        for field in ('direct_cost_gbp',*HUMAN_FIELDS):
            if not number(row.get(field),nullable=True): raise ValueError('Invalid monetary or human effort record')
        direct.append(row.get('direct_cost_gbp')); basis[row.get('cost_basis','unknown')]+=1
        times=[row.get(f) for f in HUMAN_FIELDS[:3]]
        operational.append(sum(times) if all(t is not None for t in times) else None)
        evaluation.append(row.get('evaluation_minutes'))
    direct_complete=bool(resources) and all(v is not None for v in direct)
    human_complete=bool(resources) and all(v is not None for v in operational)
    known_direct=sum(v for v in direct if v is not None)
    total=None
    if direct_complete and human_complete and (hourly_rate_gbp is not None or sum(operational)==0):
        total=known_direct+(sum(operational)*hourly_rate_gbp/60 if hourly_rate_gbp is not None else 0)
    return {'qualified_outputs':qualified_outputs,'known_direct_cost_gbp':known_direct,
            'direct_cost_complete':direct_complete,'human_production_time_complete':human_complete,
            'known_operational_minutes':sum(v for v in operational if v is not None),
            'known_evaluation_minutes':sum(v for v in evaluation if v is not None),
            'evaluation_time_complete':all(v is not None for v in evaluation),
            'cost_basis_counts':dict(basis),'production_cost_gbp':total,
            'cost_per_qualified_output_gbp':total/qualified_outputs if total is not None and qualified_outputs else None,
            'unit_cost_status':'undefined_no_qualified_output' if not qualified_outputs else ('complete' if total is not None else 'incomplete_resources'),
            'evaluation_cost_excluded_from_production':True}


def paired_cluster_interval(rows: list[dict], condition_a: str, condition_b: str, seed: int=20260923, draws: int=2000) -> dict:
    """Equal-item difference; pairs and all items in a source cluster resampled together.

    At least 10 source clusters is a reporting convention, not a validity theorem.
    Public synthetic fixtures deliberately have only six conservative family
    clusters; their interval is suppressed. Repeated cases are never independent.
    """
    if draws<100: raise ValueError('At least 100 bootstrap draws required')
    if condition_a==condition_b: raise ValueError('Two distinct conditions required')
    by_condition={c:{} for c in (condition_a,condition_b)}
    for r in rows:
        if r['condition'] in by_condition:
            bucket=by_condition[r['condition']]
            if r['case_id'] in bucket: raise ValueError('Duplicate case; aggregate declared replicates first')
            bucket[r['case_id']]=r
    a,b=by_condition.values()
    if set(a)!=set(b): raise ValueError('Matched initiated case sets required; no complete-case cherry-picking')
    clusters=defaultdict(list)
    for key in a:
        if a[key]['cluster_id']!=b[key]['cluster_id']: raise ValueError('Cluster mismatch')
        clusters[a[key]['cluster_id']].append(int(a[key]['mechanically_correct'])-int(b[key]['mechanically_correct']))
    values=[v for vs in clusters.values() for v in vs]
    difference=sum(values)/len(values) if values else None
    if len(clusters)<10:
        return {'difference_a_minus_b':difference,'paired_items':len(values),'source_clusters':len(clusters),
                'interval_95':None,'reason':'Fewer than 10 source clusters; descriptive pilot only.'}
    rng=random.Random(seed); blocks=list(clusters.values()); samples=[]
    for _ in range(draws):
        sampled=[v for block in rng.choices(blocks,k=len(blocks)) for v in block]
        samples.append(sum(sampled)/len(sampled))
    samples.sort()
    return {'difference_a_minus_b':difference,'paired_items':len(values),'source_clusters':len(clusters),
            'interval_95':[samples[int(.025*draws)],samples[min(draws-1,int(.975*draws))]],
            'seed':seed,'draws':draws,'method':'paired cluster percentile bootstrap; equal item estimand'}


def demo(output: Path) -> dict:
    if output.exists(): raise FileExistsError('Demo output already exists')
    freeze(output/'frozen'); plan=prepare(output/'frozen',output/'prepared')
    cases={c['case_id']:c for c in catalogue()}; ledger=Ledger(output/'attempts.jsonl')
    for index,job in enumerate(plan['jobs']):
        case=cases[job['case_id']]; ref=case['reference']; run_id=f'FIXTURE-{index:03d}'
        ledger.append('started',run_id,{'job_id':job['job_id'],'execution_mode':'synthetic_test_double'})
        prediction={'case_id':case['case_id'],'label':ref['accepted_labels'][0],
                    'numeric_value':ref['numeric_value'],'source_ids':ref['required_sources'],
                    'justification':ref['rationale']}
        # Identical cases receive identical injected faults in all three conditions.
        fault=index%60
        status='infrastructure_failure' if fault==0 else 'completed'
        if fault==1: prediction='malformed'
        if fault==2: prediction['source_ids']=['MISSING']
        if fault==3: continue  # initiated and interrupted: remains in denominator
        ledger.append('finished',run_id,{'status':status,'prediction':prediction,
             'resources':{'direct_cost_gbp':0,'cost_basis':'synthetic_zero','wall_seconds':0,
                          **{f:None for f in HUMAN_FIELDS}}})
    report=score_ledger(output/'frozen',output/'prepared',output/'attempts.jsonl')
    report['injected_faults_per_condition']=4
    report['paired_diagnostic']=paired_cluster_interval(report['rows'],'fixed_lower','routed')
    write_json(output/'report.json',report)
    return {k:v for k,v in report.items() if k!='rows'}


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    for name in ('freeze','demo'):
        p=sub.add_parser(name); p.add_argument('--output',type=Path,required=True)
    p=sub.add_parser('prepare'); p.add_argument('--frozen',type=Path,required=True); p.add_argument('--output',type=Path,required=True)
    p.add_argument('--split',choices=('development','calibration'),default='calibration')
    p=sub.add_parser('score'); p.add_argument('--frozen',type=Path,required=True); p.add_argument('--prepared',type=Path,required=True)
    p.add_argument('--ledger',type=Path,required=True); p.add_argument('--output',type=Path,required=True)
    p=sub.add_parser('verify'); p.add_argument('--frozen',type=Path,required=True)
    args=parser.parse_args()
    try:
        if args.command=='freeze': result=freeze(args.output)
        elif args.command=='demo': result=demo(args.output)
        elif args.command=='prepare': result=prepare(args.frozen,args.output,args.split)
        elif args.command=='score':
            result=score_ledger(args.frozen,args.prepared,args.ledger); write_json(args.output,result)
        else:
            cases,config=verify_freeze(args.frozen); result=release_readiness(cases,config)
        print(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False))
    except (ValueError,KeyError,TypeError,OSError) as exc:
        parser.exit(2,f'{type(exc).__name__}: {exc}\n')

if __name__=='__main__': main()
