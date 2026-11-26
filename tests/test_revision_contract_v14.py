#!/usr/bin/env python3
"""Deterministic regression fixtures; synthetic only, not an agent-compliance study."""
import copy,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from revision_contract import check_revision

def item(i,rule,scope='job'):
    return {'id':i,'scope':scope,'rule':rule,'status':'locked','source':'user:synthetic','check_method':'manual','target_artifact':'pdf'}
def state(*items):return {'job_id':'synthetic-job','candidate_version':'1','constraints':list(items)}
class Contract(unittest.TestCase):
    def setUp(self):
        self.old=state(item('C1','retain community practice'),item('C2','emphasize all roles'))
        self.new=copy.deepcopy(self.old);self.new.update(source_version="1",candidate_version="2")
        self.receipts=[{'id':i,'status':'PASS','evidence':'synthetic: actual check','artifact_version':'2','reviewer':'self-review-only'} for i in ('C1','C2')]
    def test_unchanged_passes(self):self.assertEqual(check_revision(self.old,self.new,[],self.receipts),[])
    def test_missing_constraint_fails(self):self.new['constraints'].pop();self.assertTrue(check_revision(self.old,self.new,[],self.receipts))
    def test_silent_edit_fails(self):self.new['constraints'][1]['rule']='only heading bold';self.assertTrue(check_revision(self.old,self.new,[],self.receipts))
    def test_scope_shift_fails(self):self.new['constraints'][1]['scope']='another-job';self.assertTrue(check_revision(self.old,self.new,[],self.receipts))
    def test_no_evidence_fails(self):self.receipts[1]['evidence']='';self.assertTrue(check_revision(self.old,self.new,[],self.receipts))
    def test_fail_or_na_not_pass(self):
        for s in ('FAIL','NA','NOT_RUN'):
            self.receipts[1]['status']=s;self.assertTrue(check_revision(self.old,self.new,[],self.receipts))
    def test_new_constraint_needs_receipt(self):self.new['constraints'].append(item('C3','keep title'));self.assertTrue(check_revision(self.old,self.new,[],self.receipts))
    def test_explicit_revision_passes(self):
        self.new['constraints'][1]['rule']='emphasize role titles only';self.new['constraints'][1]['source']='user:change';a={'id':'C2','before':self.old['constraints'][1],'after':self.new['constraints'][1],'authorization':'user:change'};self.assertEqual(check_revision(self.old,self.new,[a],self.receipts),[])
    def test_forged_old_snapshot_fails(self):
        self.new['constraints'][1]['rule']='new';a={'id':'C2','before':self.new['constraints'][1],'after':self.new['constraints'][1],'authorization':'user:change'};self.assertTrue(check_revision(self.old,self.new,[a],self.receipts))
    def test_stale_receipt_fails(self):self.receipts[1]['artifact_version']='1';self.assertTrue(check_revision(self.old,self.new,[],self.receipts))
    def test_wrong_job_fails(self):self.new['job_id']='other';self.assertTrue(check_revision(self.old,self.new,[],self.receipts))
    def test_wrong_source_version_fails(self):self.new['source_version']='0';self.assertTrue(check_revision(self.old,self.new,[],self.receipts))
    def test_duplicate_ids_fail(self):self.new['constraints'].append(self.new['constraints'][0]);self.assertTrue(check_revision(self.old,self.new,[],self.receipts))
    def test_duplicate_receipt_fails(self):self.receipts.append(self.receipts[0]);self.assertTrue(check_revision(self.old,self.new,[],self.receipts))
if __name__=='__main__':unittest.main()
