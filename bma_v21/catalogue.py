"""Original synthetic fixtures. Public reference answers are calibration aids, not gold.
No empirical study, held-out SRO material, or published research output is reproduced.
"""
from copy import deepcopy

# question, permitted evidence, acceptable label, concise reference rationale, numeric answer
ROWS = {
'evidence': [
('Does this support a rise in cement prices?', 'A: Steel prices rose 16%; cement prices are not reported.', 'insufficient', 'A different material cannot establish the cement-price claim.', None),
('Does this support the descriptive claim that the quoted cement price rose?', 'A: The same supplier quoted GBP100 per tonne in May and GBP108 per tonne in June, on identical terms.', 'supported', 'The like-for-like quote increased; this does not establish paid prices.', None),
('Does this establish that cement costs caused the entire margin decline?', 'A: Cement expense and sales margins both changed. Volumes, product mix and energy costs are unobserved.', 'insufficient', 'Co-movement does not isolate the cause of the margin decline.', None),
('Does this support the claim that every firm faced higher cement prices?', 'A: Eight of ten firms reported higher cement prices; two reported unchanged prices.', 'contradicted', 'The two unchanged observations contradict the universal claim.', None),
('Does this support the claim that UK prices fell?', 'A: A US-only sample recorded falling prices. No UK observations are available.', 'insufficient', 'The geography of the source does not support the UK claim.', None),
('Does this establish that the plant closure happened in June?', 'A: In May the company announced an intention to close the plant in June. No subsequent observations are available.', 'insufficient', 'An announced intention is not evidence of the realised event.', None),
('Does this support reporting five tonnes as the delivery quantity?', 'A: The delivery record states quantity = 5 and unit = thousand tonnes.', 'contradicted', 'The stated quantity is five thousand tonnes, not five tonnes.', None),
('Does this support the claim that the two sources conflict on the same measure?', 'A: Annual mean price is 105. B: December spot price is 112. Both refer to the same year and currency.', 'insufficient', 'An annual mean and a December price can differ without contradiction.', None),
('Does this support the claim that the value 104 is a revision rather than another monthly observation?', 'A: Series X, June, release 1, value 100. B: Series X, June, release 2, value 104; B explicitly supersedes A.', 'supported', 'The same series and reference period are revised.', None),
('Does this support the claim that no delivery was late?', 'A: Delivery times were not recorded for the sample.', 'insufficient', 'Missing observations cannot establish the absence of late delivery.', None),
],
'measurement': [
('Is the variable suitable for realised construction duration?', 'A: Only planning approval date is available; start and completion dates are absent.', 'reject', 'Approval timing does not measure construction duration.', None),
('Is this variable suitable for actual project duration in calendar days?', 'A: Verified site-start and handover dates exist for every project; duration is defined as handover minus site-start.', 'accept', 'The observations directly operationalise the stated construct.', None),
('Is this variable suitable for the actual cement price paid by each project?', 'A: A national cement producer-price index is available; project invoices and contractual adjustments are absent.', 'reject', 'A national index cannot identify project-specific paid prices.', None),
('Is the join suitable for attaching company-year accounts to subsidiaries?', 'A: Subsidiaries have unique legal-entity IDs. Parent-company names alone appear in the accounts; ownership history is absent.', 'reject', 'Parent names do not establish a time-valid entity join.', None),
('Is this variable suitable for real cost change?', 'A: Nominal costs are available for two years. No price deflator or equivalent constant-price series is available.', 'reject', 'Nominal change is not identified as real change.', None),
('Is this a suitable measure of late completion under the stated definition?', 'A: Late means actual handover after the original contractual completion date. Both dates are verified and preserved.', 'accept', 'Both the outcome and the specified baseline are observed.', None),
('Can missing reported expenditure be coded as zero expenditure?', 'A: Blank entries are defined in the data dictionary as not reported, not as zero.', 'reject', 'The proposed transformation contradicts the dictionary.', None),
('Is count of press releases a direct measure of innovation quality?', 'A: The dataset records public-relations output; it has no validation against innovation outcomes.', 'reject', 'Publicity volume has not been validated as innovation quality.', None),
('Is this a suitable measurement of regional annual employment change?', 'A: Comparable annual employment counts use unchanged regional boundaries and definitions.', 'accept', 'The observations match the stated population, period and construct.', None),
('Is this a suitable estimate of the required all-project failure rate?', 'A: The archive contains only completed projects. Abandoned projects are excluded and cannot be enumerated.', 'reject', 'Selection excludes part of the denominator and relevant failures.', None),
],
'analysis': [
('Return the maximum number of whole packages within the budget.', 'A: Budget GBP120; each package costs GBP35; no partial packages and no other costs.', 'computed', 'Three packages cost 105; four cost 140 and breach the budget.', 3),
('Return the percentage increase, using the original price as denominator.', 'A: Original price 80; new price 100.', 'computed', '(100-80)/80 times 100 = 25.', 25),
('Return the volume-weighted mean price.', 'A: Two tonnes cost GBP100 per tonne and one tonne costs GBP160 per tonne.', 'computed', '(2*100+1*160)/3 = 120.', 120),
('Can all four packages be funded simultaneously?', 'A: Each package costs GBP30. Total budget GBP100. Packages are indivisible and no alternative funding exists.', 'infeasible', 'The joint cost 120 exceeds the budget 100.', None),
('Return the remaining monetary buffer after the cost shock.', 'A: Available contingency GBP25; unavoidable incremental cost GBP18; no further offsets.', 'computed', '25-18 = 7.', 7),
('Return total income counted once across these two records.', 'A: Records R1 and R2 both refer to award AW1, total value GBP1000. R1 names the PI; R2 names a Co-I.', 'computed', 'A single award contributes 1000 once, not once per investigator.', 1000),
('Return constant-price cost in base-year pounds.', 'A: Nominal cost GBP132; base-year price index 100; current index 110.', 'computed', '132 divided by 1.10 = 120.', 120),
('Return the percentage-point change in success rate.', 'A: Initial success rate 20%; subsequent success rate 25%.', 'computed', '25-20 = 5 percentage points, distinct from 25 percent growth.', 5),
('Return combined success rate as a percentage.', 'A: Group A has 9 successes of 10; group B has 1 success of 90.', 'computed', '10 successes divided by 100 attempts = 10 percent.', 10),
('Return the buffer shortfall as a positive quantity.', 'A: Required contingency GBP48; available contingency GBP35; no borrowing allowed.', 'computed', '48-35 = 13.', 13),
],
'inference': [
('What is the strongest defensible claim type?', 'A: A cross-sectional survey records a correlation. Treatment assignment and temporal ordering are not known.', 'association', 'The design supports association, not identified causation.', None),
('What is the strongest defensible claim type for the experimental contrast?', 'A: Treatment was randomly assigned, all outcomes observed, no interference or noncompliance, and assignment preserved in analysis.', 'causal_within_sample', 'Under these stated conditions the experimental contrast identifies the sample treatment effect.', None),
('Does this design identify a treatment effect?', 'A: One treated unit is measured before and after. An unmeasured demand shock occurred between measurements; no comparison units exist.', 'not_identified', 'The treatment contrast is confounded with the demand shock.', None),
('Does failure to reject the null establish equivalence?', 'A: p=0.30 in a difference test. No equivalence margin or equivalence test was specified.', 'not_established', 'A non-significant difference is not an equivalence result.', None),
('May this be reported as confirmed out-of-sample forecast performance?', 'A: The test period was repeatedly used to choose model settings; no untouched validation period remains.', 'not_established', 'The repeatedly consulted period is no longer an untouched test.', None),
('Has the predictive interval failed its preregistered compatibility check?', 'A: Frozen prediction interval [90,110]. Independently observed outcome 125. The preregistered rule flags any outcome outside the interval.', 'failed_check', '125 is outside the interval; that observation triggers the specified check.', None),
('Does the evidence distinguish mechanism M1 from M2?', 'A: Both mechanisms predict the same distribution for every measured variable. No mechanism-specific measurement was collected.', 'not_identified', 'Observationally identical predictions cannot discriminate the mechanisms.', None),
('May a causal estimate for observed firms be generalised to all UK firms from this information alone?', 'A: The study is internally valid, but covers a convenience sample of five firms; population transport assumptions are unspecified.', 'not_established', 'Internal validity alone does not establish population transportability.', None),
('Is the proposed difference-in-differences causal interpretation supported under the supplied design assumptions?', 'A: Untreated trends are stipulated parallel, no anticipation or spillovers, stable composition, and a correctly specified two-period design.', 'causal_under_assumptions', 'The stipulated identifying assumptions support this bounded interpretation.', None),
('Can a simulation with assumed parameters be reported as observed industry impact?', 'A: All responses are simulated under assumed behavioural parameters; no industry outcome validation has been conducted.', 'not_established', 'A simulated conditional result is not observed industry impact.', None),
],
'longitudinal': [
('Classify the incoming record.', 'A: Stored series X for June release 1. Incoming X for June release 2 explicitly revises the same definition.', 'revision', 'The reference period and series are unchanged.', None),
('Classify the incoming record.', 'A: Stored series X for June. Incoming X for July, with identical definition and units.', 'new_period', 'A later reference period adds a period rather than revising June.', None),
('Admit this source to a date-locked replay?', 'A: Replay cutoff 2026-06-30T23:59:59Z. Source first became available 2026-07-02T09:00:00Z, reporting June.', 'exclude_future', 'The availability date is later than the cutoff despite the June reference period.', None),
('Does this archive meet the stipulated replay rule?', 'A: Cutoff is June 30. The sole preserved copy was captured July 5, with no immutable pre-cutoff archive proof. Rule requires such proof.', 'exclude_unverified', 'A later capture alone cannot authenticate the pre-cutoff source vintage.', None),
('How should this apparent update be treated?', 'A: Old series is tonnes of cement; incoming series with the same title is tonnes of all construction materials.', 'schema_break', 'The measurement changed and cannot be appended as the same series.', None),
('How should the revised prediction be recorded?', 'A: A baseline forecast was frozen before outcomes. A new model was designed after seeing the outcomes.', 'exploratory_amendment', 'The new model must not overwrite or masquerade as the frozen prediction.', None),
('How should the missing month be treated in the primary evidence series?', 'A: August has no observation. The frozen protocol prohibits imputation in the primary series.', 'missing', 'Retain the gap rather than invent an observed value.', None),
('How should these releases be counted for independent outcome periods?', 'A: Three releases all measure June for the same series, successively superseding one another.', 'one_period', 'Three vintages of June supply one reference period.', None),
('Can the altered file be admitted under the existing frozen checksum?', 'A: The stored SHA-256 differs from the newly received file bytes. No version amendment has been registered.', 'reject_tamper', 'Changed bytes require explicit versioning rather than silent admission.', None),
('Which value belongs in the as-of-June forecast input?', 'A: At the June cutoff, May value 100 was available. A July revision changes May to 106.', 'original_vintage', 'The July revision was unavailable at the forecast origin.', None),
],
'opportunity': [
('Under the stated triage rules, what is the next action?', 'A: Candidate exactly matches a stored claim, has verified public rows, compatible units and unique join keys, and no existing programme owner. Rule: queue such candidates for review, not execution.', 'queue_review', 'The preconditions permit review, not automatic validation or execution.', None),
('Under the stated rule, admit or reject this candidate?', 'A: Claim requires actual construction duration. Candidate offers approval dates only. Rule requires direct or previously validated measurement.', 'reject', 'The candidate lacks the required measurement.', None),
('Where should this release go?', 'A: It updates the same series for a claim already owned by programme P. Rule sends routine updates to the existing steward.', 'route_steward', 'Existing ownership makes this an update, not a new programme.', None),
('What is the next action for this apparent contradiction?', 'A: A candidate conflicts with a stored result. Definitions and joins have not been independently checked. Rule requires verification before promotion.', 'verify', 'An unchecked contradiction should initiate verification.', None),
('Can this dataset support an executable candidate now?', 'A: A landing page promises project-level data, but no rows or usable schema can be accessed. Rule requires both.', 'reject', 'A promise of data is insufficient for an executable candidate.', None),
('Does this proposed join pass?', 'A: Required unit is plant-year. Candidate is regional annual totals with no plant disaggregation. Rule forbids inferring plant values from totals.', 'reject', 'The candidate cannot identify the required plant-level observations.', None),
('May the scout start the study?', 'A: All prechecks pass, but the protocol authorises queued handovers only, not automatic execution.', 'queue_review', 'A feasible handover does not confer execution authority.', None),
('Is this a new research extension under the supplied rule?', 'A: Candidate changes only the title and repeats an already completed analysis on identical evidence. Rule requires a new test, measurement or substantive assumption.', 'reject', 'A renamed duplicate does not extend the research.', None),
('Can the retrospective scout use this portfolio note?', 'A: Replay cutoff is June 30. The note identifying the promising relationship was first written July 20.', 'exclude_future', 'Later portfolio knowledge is future information at the replay date.', None),
('Which data action could distinguish the mechanisms?', 'A: M1 and M2 make identical predictions for prices. M1 predicts inventory rises; M2 predicts inventory falls. A compatible public inventory series exists. Rule asks for the discriminating measure.', 'queue_inventory_test', 'Inventory has distinct predictions where prices do not.', None),
],
}
DEVELOPMENT = {
'evidence': [('Does the record support a delivery of 12 units?', 'A: The signed delivery note states 12 units.', 'supported', 'The record directly supports the stated amount.', None), ('Does the record support 12 units?', 'A: The signed delivery note states 9 units.', 'contradicted', 'The reported amount differs.', None)],
'measurement': [('Is the measure suitable for age in completed years?', 'A: Verified birth date and observation date are available.', 'accept', 'Dates support calculation of completed years.', None), ('Does headcount directly measure full-time-equivalent staff?', 'A: Hours and employment fractions are unknown.', 'reject', 'Headcount does not establish working fractions.', None)],
'analysis': [('Return the unweighted arithmetic mean.', 'A: Values are 2, 4, 6.', 'computed', '12/3=4.', 4), ('Is the required purchase feasible?', 'A: One indivisible item costs 11; available budget is 10; no borrowing.', 'infeasible', 'The item exceeds the budget.', None)],
'inference': [('Does a correlation alone establish causation?', 'A: Only simultaneous correlation is observed; identification assumptions are absent.', 'not_identified', 'No causal identification is supplied.', None), ('Has the frozen upper-bound check failed?', 'A: The rule flags outcomes above 5; observed outcome is 6.', 'failed_check', '6 exceeds 5.', None)],
'longitudinal': [('Classify the incoming record.', 'A: Stored January X; incoming February X uses the same definition.', 'new_period', 'February is a different period.', None), ('Classify the incoming record.', 'A: January X release 2 explicitly supersedes January X release 1.', 'revision', 'This is a new vintage of January.', None)],
'opportunity': [('Route this routine release.', 'A: It updates a claim owned by programme Q; the rule sends such releases to that programme.', 'route_steward', 'The existing owner receives the update.', None), ('May inaccessible rows support a runnable candidate?', 'A: Only a dataset title is available; the rule requires accessible rows and schema.', 'reject', 'The required inputs are absent.', None)],
}
CHOICES = {
'evidence': ['supported','contradicted','insufficient'],
'measurement': ['accept','reject'],
'analysis': ['computed','infeasible','insufficient'],
'inference': ['association','causal_within_sample','causal_under_assumptions','not_identified','not_established','failed_check'],
'longitudinal': ['revision','new_period','exclude_future','exclude_unverified','schema_break','exploratory_amendment','missing','one_period','reject_tamper','original_vintage'],
'opportunity': ['queue_review','reject','route_steward','verify','exclude_future','queue_inventory_test'],
}

def catalogue():
    """Return 60 pilot and 12 distinct development examples, all public synthetic."""
    cases = []
    for split, source in [('calibration', ROWS), ('development', DEVELOPMENT)]:
        for family, rows in source.items():
            for i, (question, text, answer, rationale, value) in enumerate(rows, 1):
                # Ex-ante descriptive profile, not inferred from any model's score.
                profile = {'evidence_integration': 1, 'measurement_ambiguity': int(family in ('measurement','opportunity')),
                           'inferential_demand': 2 if family == 'inference' else 1,
                           'temporal_updating': 2 if family == 'longitudinal' else 0,
                           'method_familiarity': 'unspecified', 'domain_familiarity': 'unspecified'}
                cases.append({'case_id': f'{split.upper()}-{family.upper()}-{i:02d}',
                              'version': '1.0', 'split': split, 'panel': 'public_synthetic_calibration',
                              'family': family, 'source_kind': 'synthetic',
                              'cluster_id': f'synthetic-family-{family}',
                              'question': question, 'evidence': [{'source_id':'A','text':text}],
                              'choices': CHOICES[family], 'complexity': profile,
                              'reference': {'accepted_labels':[answer], 'numeric_value':value,
                                            'absolute_tolerance':1e-8, 'required_sources':['A'],
                                            'rationale':rationale},
                              'audit': {'status':'proposed_not_independently_adjudicated',
                                        'evidence_sufficient':True, 'reference_basis':'authored_fixture',
                                        'reviewer':None, 'reviewed_at':None,
                                        'acceptable_alternatives':'See accepted_labels; further defensible alternatives require a versioned adjudication.',
                                        'uncertainty_rule':'Use only the packet; insufficient evidence is a valid response only when accepted by the case rubric.'}})
    return deepcopy(cases)
