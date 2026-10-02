import copy
import json
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from .catalogue import catalogue
from .engine import (CONFIG, GATES, HUMAN_FIELDS, Ledger, canonical, cost_summary,
                     demo, digest, freeze, mechanical_grade, paired_cluster_interval,
                     paper_summary, prepare, release_readiness, score_ledger,
                     select_slot, validate_cases, validate_finish, verify_freeze,
                     worker_request)

class AmendmentTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.root=Path(self.temp.name)
        self.cases=catalogue(); self.case=self.cases[0]
    def tearDown(self): self.temp.cleanup()
    def prediction(self,case=None):
        case=case or self.case; r=case['reference']
        return {'case_id':case['case_id'],'label':r['accepted_labels'][0],
                'numeric_value':r['numeric_value'],'source_ids':r['required_sources'],
                'justification':r['rationale']}
    def resource(self,**updates):
        r={'direct_cost_gbp':0,'cost_basis':'synthetic_zero','wall_seconds':0,
           **{f:None for f in HUMAN_FIELDS}}; r.update(updates); return r
    def record(self,**updates):
        r={'run_id':'P1','initiated':True,'system_id':'mock','panel':'fixed','output_type':'paper',
           'status':'completed','evaluation_authority':'independent','substantive_human_rescue':False,
           'gates':{g:True for g in GATES},'journal_readiness':'independently_qualified'}
        r.update(updates); return r
    def prepared(self):
        frozen=self.root/'frozen'; output=self.root/'prepared'
        freeze(frozen); plan=prepare(frozen,output)
        return frozen,output,plan

    def test_01_counts(self):
        self.assertEqual(Counter(c['split'] for c in self.cases),{'calibration':60,'development':12})
        self.assertTrue(all(v==10 for v in Counter(c['family'] for c in self.cases if c['split']=='calibration').values()))
    def test_02_no_duplicate_cases_or_prompts(self):
        self.assertEqual(len({c['case_id'] for c in self.cases}),72)
        self.assertEqual(len({digest(worker_request(c)) for c in self.cases}),72)
        prompts=[(c['question'],canonical(c['evidence'])) for c in self.cases]
        self.assertEqual(len(set(prompts)),72)
    def test_03_public_cases_explicitly_synthetic(self):
        validate_cases(self.cases)
        self.assertTrue(all(c['source_kind']=='synthetic' for c in self.cases))
    def test_04_private_or_prospective_rows_rejected(self):
        case=copy.deepcopy(self.case); case['source_kind']='observed'
        with self.assertRaises(ValueError): validate_cases([case])
        case=copy.deepcopy(self.case); case['split']='prospective'
        with self.assertRaises(ValueError): validate_cases([case])
    def test_05_projection_excludes_answers_and_audit(self):
        request=worker_request(self.case)
        self.assertEqual(set(request),{'case_id','task_version','instruction','question','evidence','choices','output_contract'})
        self.assertNotIn('reference',request); self.assertNotIn('audit',request)
        self.assertNotIn(self.case['reference']['rationale'],canonical(request).decode())
    def test_06_freeze_verify(self):
        manifest=freeze(self.root/'frozen'); cases,config=verify_freeze(self.root/'frozen')
        self.assertEqual(cases,self.cases); self.assertEqual(config,CONFIG)
        self.assertEqual(manifest['counts']['calibration'],60)
    def test_07_immutable_destination(self):
        freeze(self.root/'frozen')
        with self.assertRaises(FileExistsError): freeze(self.root/'frozen')
    def test_08_changed_evidence_rejected(self):
        freeze(self.root/'frozen'); p=self.root/'frozen/worker_packets/calibration.json'
        p.write_text('[]')
        with self.assertRaises(ValueError): verify_freeze(self.root/'frozen')
    def test_09_no_official_claim(self):
        status=release_readiness(self.cases,CONFIG)
        self.assertFalse(status['official_run_ready']); self.assertGreaterEqual(len(status['blockers']),4)
    def test_10_routing_frozen_ex_ante(self):
        counts=Counter(select_slot(c,'routed',CONFIG) for c in self.cases if c['split']=='calibration')
        self.assertEqual(counts,{'lower':40,'higher':20})
    def test_11_reject_hindsight_routing(self):
        cfg=copy.deepcopy(CONFIG); cfg['routing']['learned_from_evaluation']=True
        with self.assertRaises(ValueError): select_slot(self.case,'routed',cfg)
    def test_12_matched_requests(self):
        f,o,plan=self.prepared(); self.assertEqual(len(plan['jobs']),180)
        jobs=[j for j in plan['jobs'] if j['case_id']==self.case['case_id']]
        self.assertEqual(len({j['request_sha256'] for j in jobs}),1)
        self.assertEqual(len({digest(j['per_case_ceiling']) for j in jobs}),1)
    def test_13_prepare_is_not_initiation(self):
        f,o,plan=self.prepared(); report=score_ledger(f,o,self.root/'absent.jsonl')
        self.assertTrue(all(v['initiated']==0 for v in report['conditions'].values()))
        self.assertTrue(all(v['mechanical_rate'] is None for v in report['conditions'].values()))
    def test_14_all_reference_fixtures_mechanically_valid(self):
        for case in self.cases: self.assertTrue(mechanical_grade(case,self.prediction(case))[0],case['case_id'])
    def test_15_wrong_label(self):
        p=self.prediction(); p['label']='invented'; self.assertFalse(mechanical_grade(self.case,p)[0])
    def test_16_wrong_case_id(self):
        p=self.prediction(); p['case_id']='different'; self.assertFalse(mechanical_grade(self.case,p)[0])
    def test_17_fabricated_citation(self):
        p=self.prediction(); p['source_ids']=['INVENTED']; self.assertFalse(mechanical_grade(self.case,p)[0])
    def test_18_missing_rationale(self):
        p=self.prediction(); p['justification']=''; self.assertFalse(mechanical_grade(self.case,p)[0])
    def test_19_numeric_failures(self):
        case=next(c for c in self.cases if c['reference']['numeric_value'] is not None)
        for value in (True,float('nan'),float('inf'),None,'3',-999):
            p=self.prediction(case); p['numeric_value']=value
            self.assertFalse(mechanical_grade(case,p)[0])
    def test_20_spurious_numeric_claim(self):
        p=self.prediction(); p['numeric_value']=1
        self.assertFalse(mechanical_grade(self.case,p)[0])
    def test_21_malformed_prediction(self):
        for p in (None,'text',[],3): self.assertFalse(mechanical_grade(self.case,p)[0])
    def test_22_no_semantic_validation_claim(self):
        p=self.prediction(); p['justification']='Deliberately irrelevant explanation.'
        passed,reason=mechanical_grade(self.case,p)
        self.assertTrue(passed); self.assertEqual(reason,'mechanical_checks_only')
        # Demonstrates the documented boundary: prose requires independent adjudication.
    def test_23_no_hidden_restart(self):
        ledger=Ledger(self.root/'l.jsonl'); ledger.append('started','R1',{'job_id':'j'})
        with self.assertRaises(ValueError): ledger.append('started','R1',{'job_id':'j'})
    def test_24_no_finish_without_start(self):
        with self.assertRaises(ValueError): Ledger(self.root/'l.jsonl').append('finished','R1',{})
    def test_25_ledger_mutation_detected(self):
        path=self.root/'l.jsonl'; ledger=Ledger(path); ledger.append('started','R1',{'job_id':'j'})
        path.write_text(path.read_text().replace('"job_id":"j"','"job_id":"wrong"'))
        with self.assertRaises(ValueError): ledger.read()
    def test_26_initiated_interruption_stays_in_denominator(self):
        f,o,plan=self.prepared(); path=self.root/'l.jsonl'
        Ledger(path).append('started','R1',{'job_id':plan['jobs'][0]['job_id']})
        result=score_ledger(f,o,path)['conditions']['fixed_lower']
        self.assertEqual(result['initiated'],1); self.assertEqual(result['mechanical_rate'],0)
    def test_27_duplicate_case_restart_not_best_of(self):
        f,o,plan=self.prepared(); path=self.root/'l.jsonl'; ledger=Ledger(path)
        for run in ('R1','R2'): ledger.append('started',run,{'job_id':plan['jobs'][0]['job_id']})
        with self.assertRaises(ValueError): score_ledger(f,o,path)
    def test_28_positive_cost_breaches_zero_authorisation(self):
        f,o,plan=self.prepared(); path=self.root/'l.jsonl'; ledger=Ledger(path)
        ledger.append('started','R1',{'job_id':plan['jobs'][0]['job_id']})
        ledger.append('finished','R1',{'status':'completed','prediction':self.prediction(),
            'resources':self.resource(direct_cost_gbp=1,cost_basis='estimate')})
        report=score_ledger(f,o,path)
        self.assertEqual(report['rows'][0]['reason'],'cost_ceiling_breached')
    def test_29_unknown_cost_not_zero(self):
        row=self.resource(direct_cost_gbp=None,cost_basis='unknown')
        validate_finish({'status':'infrastructure_failure','resources':row})
        report=cost_summary([row],0)
        self.assertFalse(report['direct_cost_complete']); self.assertIsNone(report['production_cost_gbp'])
    def test_30_missing_human_minutes_stay_unknown(self):
        result=cost_summary([self.resource()],1,50)
        self.assertFalse(result['human_production_time_complete'])
        self.assertIsNone(result['cost_per_qualified_output_gbp'])
    def test_31_evaluation_cost_separate(self):
        row=self.resource(direct_cost_gbp=10,cost_basis='provider_billed',production_minutes=30,
                          operational_verification_minutes=10,rework_minutes=20,evaluation_minutes=90)
        report=cost_summary([row],1,60)
        self.assertEqual(report['production_cost_gbp'],70)
        self.assertEqual(report['known_evaluation_minutes'],90)
    def test_32_zero_qualified_unit_cost_undefined(self):
        row=self.resource(**{f:0 for f in HUMAN_FIELDS})
        report=cost_summary([row],0)
        self.assertIsNone(report['cost_per_qualified_output_gbp'])
        self.assertEqual(report['unit_cost_status'],'undefined_no_qualified_output')
    def test_33_unknown_basis_inconsistent_amount(self):
        with self.assertRaises(ValueError): validate_finish({'status':'completed','resources':self.resource(cost_basis='unknown')})
    def test_34_nonfinite_resource_rejected(self):
        for value in (-1,True,float('nan'),float('inf')):
            with self.assertRaises(ValueError): cost_summary([self.resource(production_minutes=value)],0)
    def test_35_all_five_paper_gates_required(self):
        for gate in GATES:
            r=self.record(); r['gates'][gate]=False
            self.assertEqual(paper_summary([r])['groups'][0]['passes'],0)
    def test_36_no_self_awarded_pass(self):
        self.assertEqual(paper_summary([self.record(evaluation_authority='producer')])['groups'][0]['passes'],0)
    def test_37_human_rescue_blocks_paper_pass(self):
        self.assertEqual(paper_summary([self.record(substantive_human_rescue=True)])['groups'][0]['passes'],0)
    def test_38_every_initiated_paper_failure_counts(self):
        rows=[self.record(),self.record(run_id='P2',status='infrastructure_failure'),self.record(run_id='P3',initiated=False)]
        result=paper_summary(rows)['groups'][0]
        self.assertEqual(result['initiated'],2); self.assertEqual(result['raw_autonomous_task_pass_rate'],0.5)
    def test_39_no_decision_to_paper_conversion(self):
        with self.assertRaises(ValueError): paper_summary([self.record(output_type='decision')])
    def test_40_no_pooling_across_panels(self):
        rows=[self.record(),self.record(run_id='P2',panel='prospective')]
        self.assertEqual(len(paper_summary(rows)['groups']),2)
    def test_41_small_cluster_interval_suppressed(self):
        rows=[]
        for condition in ('a','b'):
            rows.extend({'condition':condition,'case_id':str(i),'cluster_id':'ONE-STUDY',
                         'mechanically_correct':True} for i in range(60))
        result=paired_cluster_interval(rows,'a','b')
        self.assertEqual(result['source_clusters'],1); self.assertIsNone(result['interval_95'])
    def test_42_unmatched_cases_rejected(self):
        rows=[{'condition':'a','case_id':'1','cluster_id':'x','mechanically_correct':True}]
        with self.assertRaises(ValueError): paired_cluster_interval(rows,'a','b')
    def test_43_deterministic_paired_bootstrap(self):
        rows=[]
        for condition in ('a','b'):
            rows.extend({'condition':condition,'case_id':str(i),'cluster_id':str(i),
                         'mechanically_correct':condition=='a'} for i in range(12))
        result=paired_cluster_interval(rows,'a','b',draws=100)
        self.assertEqual(result['interval_95'],[1,1])
        self.assertEqual(result,paired_cluster_interval(rows,'a','b',draws=100))
    def test_44_complete_fault_demo(self):
        report=demo(self.root/'demo')
        self.assertTrue(report['all_primary_jobs_initiated'])
        self.assertIsNone(report['raw_autonomous_task_pass_rate'])
        for value in report['conditions'].values():
            self.assertEqual(value['initiated'],60); self.assertEqual(value['mechanically_correct'],56)
            self.assertEqual(sum(value['failures'].values()),4)
    def test_45_public_calibration_not_sro(self):
        self.assertNotIn('SRO-001',canonical(self.cases).decode())
        self.assertNotIn('MISSOURI-001',canonical(self.cases).decode())
    def test_46_invalid_known_resource_count(self):
        with self.assertRaises(ValueError): cost_summary([],1)
        self.assertFalse(cost_summary([],0)['direct_cost_complete'])

    def test_47_dropped_jobs_rejected_even_after_rehash(self):
        f,o,plan=self.prepared(); plan['jobs']=plan['jobs'][:-1]; plan['plan_sha256']=digest(plan['jobs'])
        (o/'plan.json').write_text(json.dumps(plan))
        with self.assertRaises(ValueError): score_ledger(f,o,self.root/'l.jsonl')
    def test_48_changed_job_ceiling_rejected_after_rehash(self):
        f,o,plan=self.prepared(); plan['jobs'][0]['per_case_ceiling']={'wall_seconds':9999,'output_tokens':9999,'cost_gbp':9999}
        plan['plan_sha256']=digest(plan['jobs']); (o/'plan.json').write_text(json.dumps(plan))
        with self.assertRaises(ValueError): score_ledger(f,o,self.root/'l.jsonl')
    def test_49_missing_output_field_rejected(self):
        p=self.prediction(); del p['numeric_value']
        self.assertFalse(mechanical_grade(self.case,p)[0])
    def test_50_unrecognised_output_field_rejected(self):
        p=self.prediction(); p['unsupported_extra_claim']='invented'
        self.assertFalse(mechanical_grade(self.case,p)[0])

if __name__=='__main__': unittest.main()
