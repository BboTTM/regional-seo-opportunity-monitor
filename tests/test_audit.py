import copy, json, sys, unittest
from pathlib import Path
from datetime import datetime
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_report import audit, week_window, state_path, baseline_growth

ROOT=Path(__file__).resolve().parents[1]
def config(region='tr'):
    return json.loads((ROOT/f'assets/{region}.example.json').read_text())
def report():
    shared={'topic_id':'synthetic-topic','facts':{'count':2},'evidence_status':'candidate','local_term':'test','target_keywords':['test'],'headline':'Test'}
    return {'region_id':'tr','history_topic_ids':[],'topics':[dict(shared,kind='new',source_urls=['https://example.org/post'],zh=copy.deepcopy(shared),en=copy.deepcopy(shared))]}

class AuditTests(unittest.TestCase):
    def test_valid_and_empty(self):
        self.assertEqual(audit(config(),report()),[])
        self.assertEqual(audit(config(),{'region_id':'tr','topics':[]}),[])
    def test_country_isolation(self):
        self.assertTrue(audit(config('az'),report()))
        self.assertNotEqual(state_path(config(),'config.json'),state_path(config('az'),'config.json'))
    def test_local_week_boundaries(self):
        now=datetime.fromisoformat('2026-09-27T20:30:00+00:00')
        self.assertTrue(week_window(config(),now)[1].startswith('2026-09-21T00:00:00+03:00'))
        self.assertTrue(week_window(config('az'),now)[1].startswith('2026-09-28T00:00:00+04:00'))
    def test_old_topic_cannot_be_new(self):
        r=report();r['history_topic_ids']=['synthetic-topic'];self.assertTrue(audit(config(),r))
    def test_stage_change_requires_evidence(self):
        r=report();r['history_topic_ids']=['synthetic-topic'];t=r['topics'][0];t.update(kind='continuation',previous_stage='preview',stage='open',new_evidence_urls=t['source_urls'])
        self.assertEqual(audit(config(),r),[])
        t['stage']='preview';self.assertTrue(audit(config(),r))
    def test_duplicate_and_translation_drift(self):
        r=report();r['topics'].append(copy.deepcopy(r['topics'][0]));self.assertTrue(audit(config(),r))
        r=report();r['topics'][0]['en']['facts']['count']=20;self.assertTrue(audit(config(),r))
        r=report();r['topics'][0]['en']['evidence_status']='confirmed';self.assertTrue(audit(config(),r))
    def test_growth_requires_comparable_nonzero_data(self):
        self.assertEqual(baseline_growth([10]*28+[20]*7),100)
        for values in ([0]*35,[None]*35,[1]*34,[float('nan')]*35):self.assertIsNone(baseline_growth(values))
    def test_credential_url_rejected(self):
        r=report();r['topics'][0]['source_urls']=['https://user:password@example.org/'];self.assertTrue(audit(config(),r))

if __name__=='__main__':unittest.main(verbosity=2)
