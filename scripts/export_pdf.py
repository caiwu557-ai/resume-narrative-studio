#!/usr/bin/env python3
"""Optional measured PDF export. Reflow is structural, never density compression."""
from __future__ import annotations
import argparse,copy,json,shutil,sys
from pathlib import Path
import fitz
from playwright.sync_api import sync_playwright
from render_resume import make_html,load_themes,load_tokens

def page_metrics(doc):
    stats=[]
    for pg in doc:
        spans=[s for b in pg.get_text('dict')['blocks'] if 'lines'in b for l in b['lines'] for s in l['spans'] if s['text'].strip()]
        bottom=max([s['bbox'][3] for s in spans] or [0])/pg.rect.height
        top=min([s['bbox'][1] for s in spans] or [pg.rect.height])/pg.rect.height
        stats.append({'text_spans':len(spans),'top_fraction':round(top,3),'bottom_fraction':round(bottom,3),'extent_fraction':round(max(0,bottom-top),3),'min_font_pt':round(min([s['size'] for s in spans] or [0]),2)})
    return stats

def flag_pages(stats):
    # Local diagnostic heuristics, not universal whitespace ratios.
    if len(stats)<=1:return []
    return [i+1 for i,p in enumerate(stats) if p['text_spans']<7 or p['extent_fraction']<(.26 if i==len(stats)-1 else .30)]

def export(data,theme,settings,output,browser,auto_reflow=True):
    page=browser.new_page(viewport={'width':900,'height':1400});page.emulate_media(media='print')
    def render(d):
        page.set_content(make_html(d,theme,**settings),wait_until='load');page.evaluate('document.fonts.ready');return page.pdf(print_background=True,prefer_css_page_size=True)
    natural=render(data); doc=fitz.open(stream=natural,filetype='pdf');before=page_metrics(doc); flagged=flag_pages(before);doc.close()
    report={'theme':theme['id'],'settings':settings,'natural_pages':before,'natural_sparse_pages':flagged,'reflowed':False,'page_groups':[],'final_pages':before,'final_sparse_pages':flagged,'status':'review-required' if flagged else 'preflight-ok'}
    result=natural
    if auto_reflow and flagged and len(data['sections'])>1:
        original=copy.deepcopy(data); sections=original['sections'];n=len(sections)
        for i,s in enumerate(sections):s['_source_index']=i
        cache={}
        def part(i,j):
            k=(i,j)
            if k not in cache:
                d=copy.deepcopy(original);d['sections']=sections[i:j]
                if i>0:
                    d['_continuation']=True;d.pop('contact',None);d.pop('profile',None);d.pop('target',None);d.pop('links',None);d.pop('photo',None)
                pdf=render(d); x=fitz.open(stream=pdf,filetype='pdf');m=page_metrics(x);x.close();cache[k]=(pdf,m)
            return cache[k]
        def score(a,b):return min(a[0]['extent_fraction'],b[0]['extent_fraction'])-.22*abs(a[0]['extent_fraction']-b[0]['extent_fraction'])
        groups=[]
        if n<=12 and len(before)==2:
            candidates=[]
            for k in range(1,n):
                _,am=part(0,k); _,bm=part(k,n)
                if len(am)==len(bm)==1:candidates.append((score(am,bm),k))
            if candidates:
                k=max(candidates)[1];groups=[(0,k),(k,n)]
        if not groups:
            i=0
            while i<n:
                lo=i+1;hi=n;best=None
                while lo<=hi:
                    mid=(lo+hi)//2;_,m=part(i,mid)
                    if len(m)==1:best=mid;lo=mid+1
                    else:hi=mid-1
                if best is None:groups=[];break
                groups.append((i,best));i=best
            if len(groups)>1:
                a,b=groups[-2][0],groups[-1][1];candidates=[]
                for k in range(a+1,b):
                    _,am=part(a,k);_,bm=part(k,b)
                    if len(am)==len(bm)==1:candidates.append((score(am,bm),k))
                if candidates:
                    k=max(candidates)[1];groups[-2:]=[(a,k),(k,b)]
        if groups:
            merged=fitz.open()
            for i,j in groups:
                raw,_=part(i,j);q=fitz.open(stream=raw,filetype='pdf');merged.insert_pdf(q,links=True,annots=True);q.close()
            after=page_metrics(merged); flags=flag_pages(after)
            if not flags:
                result=merged.tobytes(garbage=4,deflate=True);report.update(reflowed=True,page_groups=[list(x) for x in groups],final_pages=after,final_sparse_pages=[],status='preflight-ok-after-reflow')
            else:report['reflow_attempt_sparse_pages']=flags
            merged.close()
    page.close();output.parent.mkdir(parents=True,exist_ok=True);output.write_bytes(result);output.with_suffix('.preflight.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');return report

def main():
    p=argparse.ArgumentParser(description=__doc__);t=load_tokens();p.add_argument('--input',required=True);p.add_argument('--theme',required=True,choices=list(load_themes()));p.add_argument('--palette',choices=list(t['palettes']));p.add_argument('--font',choices=list(t['fonts']));p.add_argument('--rhythm',choices=list(t['rhythms']));p.add_argument('--page',choices=t['allowed_page_sizes'],default='A4');p.add_argument('--custom-palette');p.add_argument('--output',required=True);p.add_argument('--chromium',default=shutil.which('chromium') or shutil.which('google-chrome'));p.add_argument('--no-reflow',action='store_true');a=p.parse_args()
    d=json.loads(Path(a.input).read_text(encoding='utf-8'));settings={k:getattr(a,k) for k in ('palette','font','rhythm','page')};
    if a.custom_palette:settings['custom_colors']=json.loads(Path(a.custom_palette).read_text())
    with sync_playwright() as pw:
        b=pw.chromium.launch(headless=True,executable_path=a.chromium,args=['--no-sandbox'] if sys.platform.startswith('linux') else []);r=export(d,load_themes()[a.theme],settings,Path(a.output),b,not a.no_reflow);b.close()
    print(json.dumps(r,ensure_ascii=False,indent=2));print('PDF must still receive visual and content review.')
    if r['status']=='review-required':raise SystemExit(2)
if __name__=='__main__':main()
