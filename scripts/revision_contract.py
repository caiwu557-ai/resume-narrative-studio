#!/usr/bin/env python3
"""Check constraint continuity and evidence receipt completeness, not truth or authorization itself."""
import argparse,json
from pathlib import Path

def check_revision(previous,current,changes,receipts):
    errors=[]
    version=current.get('candidate_version')
    if not isinstance(version,str) or not version.strip():errors.append('current: missing candidate_version')
    if current.get('job_id')!=previous.get('job_id') or not current.get('job_id'):errors.append('job_id mismatch or missing')
    if previous.get('candidate_version') and current.get('source_version')!=previous.get('candidate_version'):errors.append('source_version does not match prior snapshot')
    if previous.get('candidate_version') and version==previous.get('candidate_version'):errors.append('candidate_version must identify a new revision')
    def index(items,label):
        out={}
        for item in items:
            k=item.get('id')
            if not isinstance(k,str) or not k.strip() or k in out:
                errors.append(f'{label}: missing/duplicate id {k!r}');continue
            out[k]=item
        return out
    old=index(previous['constraints'],'previous');new=index(current['constraints'],'current');diff=index(changes,'changes');checks=index(receipts,'receipts')
    for k,c in new.items():
        for field in ('rule','scope','source','check_method','target_artifact'):
            if not isinstance(c.get(field),str) or not c[field].strip():errors.append(f'{k}: missing {field}')
        if c.get('status') not in ('locked','tentative','delegated','retired','rejected'):errors.append(f'{k}: invalid status')
    for k,c in old.items():
        if k not in new:
            errors.append(f'{k}: deleted; preserve row and explicitly retire instead');continue
        if c.get('status')=='locked' and c!=new[k]:
            a=diff.get(k,{})
            if a.get('before')!=c or a.get('after')!=new[k] or not isinstance(a.get('authorization'),str) or not a['authorization'].strip():errors.append(f'{k}: locked constraint altered without matching authorization record')
    for k,c in new.items():
        if c.get('status')=='locked':
            r=checks.get(k,{})
            if r.get('status')!='PASS' or not isinstance(r.get('evidence'),str) or not r['evidence'].strip():errors.append(f'{k}: locked rule lacks passing evidence receipt')
            if r.get('artifact_version')!=version:errors.append(f'{k}: stale or missing artifact_version')
            if not isinstance(r.get('reviewer'),str) or not r['reviewer'].strip():errors.append(f'{k}: missing reviewer')
    for k in diff:
        if k not in old or k not in new or old[k]==new[k]:errors.append(f'{k}: stale/unknown change record')
    for k in checks:
        if k not in new:errors.append(f'{k}: unknown receipt')
    return errors

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for k in ('previous','current','changes','receipts'):p.add_argument('--'+k,required=True,type=Path)
    a=p.parse_args();errors=check_revision(*[json.loads(getattr(a,k).read_text(encoding='utf-8')) for k in ('previous','current','changes','receipts')]);print(json.dumps({'status':'review-required' if errors else 'contract-check-ok','errors':errors,'limit':'Checks recorded data only; inspect actual artifacts and verify authorization.'},ensure_ascii=False,indent=2));return 1 if errors else 0
if __name__=='__main__':raise SystemExit(main())
