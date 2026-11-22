#!/usr/bin/env python3
"""Measured regression cases for sparse-page reflow. Optional browser dependencies required."""
import argparse,sys,json,re,shutil
from pathlib import Path
import fitz
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from render_resume import load_themes,load_tokens
from export_pdf import export
p=argparse.ArgumentParser();p.add_argument('--out',default='pagination-qa');p.add_argument('--chromium',default=shutil.which('chromium') or shutil.which('google-chrome'));a=p.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
styles=list(load_themes().values());tokens=load_tokens();data=json.loads((ROOT/'examples/sample_resume.json').read_text());results=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=a.chromium,args=['--no-sandbox'] if sys.platform.startswith('linux') else [])
 for idx in [2,5,7,8,9]:
  t=styles[idx];settings={'palette':list(tokens['palettes'])[idx%12],'font':list(tokens['fonts'])[idx%7],'rhythm':['balanced','airy','large'][idx%3],'page':'Letter' if idx%2 else 'A4'}
  f=out/(t['id']+'.pdf');r=export(data,t,settings,f,b);d=fitz.open(f);text=re.sub(r'\s+','',''.join(x.get_text() for x in d));titles=all(re.sub(r'\s+','',s['title']) in text for s in data['sections']);links=any((x.get('uri') or '').rstrip('/')=='https://example.org' for p in d for x in p.get_links());ok=titles and links and not r['final_sparse_pages'];d.close();r.update(all_section_titles=titles,example_link_preserved=links,passed=ok);results.append(r);print(t['id'],'flagged',r['natural_sparse_pages'],'final',r['final_sparse_pages'],'pass',ok,flush=True)
 b.close()
(out/'pagination-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2));assert all(x['passed'] for x in results)
