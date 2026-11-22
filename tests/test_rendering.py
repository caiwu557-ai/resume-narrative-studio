#!/usr/bin/env python3
"""Optional actual browser/PDF smoke test. Requires Playwright, Chromium, PyMuPDF (see README)."""
import argparse,copy,json,re,sys,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from render_resume import make_html,load_themes,load_tokens
import fitz
from playwright.sync_api import sync_playwright

def norm(x):return re.sub(r'\s+','',x)
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',default='render-qa');p.add_argument('--chromium',default=shutil.which('chromium') or shutil.which('google-chrome'));a=p.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
 data=json.loads((ROOT/'examples/sample_resume.json').read_text());themes=load_themes();layouts=list(themes.values());records=[];issues=[]
 # Valid synthetic long CV contains distinct tokens at end of every entry. Deliberate long title/contact.
 long=copy.deepcopy(data);long['name']='欧阳林沐';long['contact']=['example.research.department.longname@example.org','https://example.org/portfolio/research-and-digital-education'];long['sections']=[]
 for i in range(14):
  original=copy.deepcopy(data['sections'][i%len(data['sections'])]);original['title']=f'履历项目{i+1:02d}';original.pop('placement',None);original.pop('featured',None);original['entries']=[{'heading':f'完整经历{i+1:02d} · 跨学科项目与协作实践', 'meta':f'2025—2026 · 个人参与','detail':('通过真实任务组织资料、明确工作范围并完成项目交付。与团队梳理需求和行动记录，重视在复杂问题中提炼主要信息并完成交流。')*3+f'末尾标识{i+1:02d}'}];long['sections'].append(original)
 # PDF: every section title, every unique long marker and end detail present; page coordinate bounds.
 with sync_playwright() as pw:
  b=pw.chromium.launch(headless=True,executable_path=a.chromium,args=['--no-sandbox'] if sys.platform.startswith('linux') else [])
  for idx,t in enumerate(layouts):
   for kind,src,kwargs in [('default',data,{}),('long',long,{}),('mix',data,{'palette':'paper' if t['ats_candidate'] else list(load_tokens()['palettes'])[idx%12],'font':'neutral' if t['ats_candidate'] else list(load_tokens()['fonts'])[idx%7],'rhythm':['balanced','airy','large'][idx%3],'page':'Letter' if idx%2 else 'A4'})]:
    page=b.new_page(viewport={'width':900,'height':1300},device_scale_factor=1)
    page.set_content(make_html(src,t,**kwargs),wait_until='load');page.evaluate('document.fonts.ready');desktop=page.evaluate('({w:document.documentElement.scrollWidth,viewport:innerWidth})'); page.set_viewport_size({'width':390,'height':844});mobile=page.evaluate('({w:document.documentElement.scrollWidth,viewport:innerWidth})');page.set_viewport_size({'width':900,'height':1300});page.emulate_media(media='print')
    f=out/f'{t["id"]}-{kind}.pdf';page.pdf(path=str(f),prefer_css_page_size=True,print_background=True)
    d=fitz.open(f);s=norm(''.join(pg.get_text() for pg in d));text_ok=norm(src['name']) in s and all(norm(sec['title']) in s for sec in src['sections']);markers_ok=(kind!='long' or all(f'末尾标识{i+1:02d}' in s for i in range(14)));coords=True;counts=[];body_sizes=[];last_bottom=[]
    for pg in d:
     found=[]
     for block in pg.get_text('dict')['blocks']:
      if 'lines' not in block:continue
      for ln in block['lines']:
       for span in ln['spans']:
        if span['text'].strip():
         x0,y0,x1,y1=span['bbox'];coords=coords and x0>=-1 and y0>=-1 and x1<=pg.rect.width+1 and y1<=pg.rect.height+1;found.append(span);body_sizes.append(span['size'])
     counts.append(len(found));last_bottom.append(round(max([z['bbox'][3] for z in found] or [0])/pg.rect.height,2))
    ok=text_ok and markers_ok and coords and mobile['w']<=mobile['viewport']+1 and desktop['w']<=desktop['viewport']+1 and all(counts) and min(body_sizes)>=9.75
    rec={'theme':t['id'],'case':kind,'pages':len(d),'titles_and_name':text_ok,'unique_end_markers':markers_ok,'within_page':coords,'mobile_no_overflow':mobile['w']<=mobile['viewport']+1,'desktop_no_overflow':desktop['w']<=desktop['viewport']+1,'min_extracted_font_pt':round(min(body_sizes),2),'page_text_bottom_fraction':last_bottom,'text_spans_per_page':counts,'pass':ok};records.append(rec)
    if not ok:issues.append(rec)
    if kind=='default':d[0].get_pixmap(matrix=fitz.Matrix(1.1,1.1),alpha=False).save(out/(t['id']+'.png'))
    print(t['id'],kind,'pages',len(d),'pass',ok,flush=True);page.close();d.close()
  # Actual gallery controls, export configuration and HTML snapshot.
  page=b.new_page(viewport={'width':1366,'height':900},accept_downloads=True);page.set_content((ROOT/'style-gallery.html').read_text(encoding='utf8'),wait_until='load');page.wait_for_timeout(500);page.select_option('#layout','pop-blocks');page.select_option('#palette','cobalt');page.select_option('#font','serif');page.select_option('#rhythm','large');page.select_option('#paper','Letter');page.wait_for_timeout(400)
  child=page.frame_locator('#frame');ok=child.locator('main').get_attribute('data-layout')=='pop' and '12 pt' in page.locator('#rhythmhelp').inner_text();
  with page.expect_download() as de:page.click('#save-config')
  cfg=json.loads(de.value.path().read_text());ok=ok and cfg['theme']=='pop-blocks' and cfg['palette']=='cobalt' and cfg['font']=='serif' and cfg['rhythm']=='large' and cfg['page']=='Letter'
  with page.expect_download() as de:page.click('#save-html')
  content=de.value.path().read_text();ok=ok and '--body-size:12pt' in content and '@page{size:Letter;' in content and '--band:#1E3689' in content
  page.select_option('#layout','ats-clean');ok=ok and page.locator('#palette').is_disabled() and page.locator('#font').is_disabled() and page.locator('#palette').input_value()=='paper';page.click('#mono');ok=ok and 'mono-mode' in page.locator('#gallery').get_attribute('class');page.screenshot(path=str(out/'gallery-qa.png'),full_page=False);records.append({'gallery_mixer_and_exports':ok});print('MIXER',ok);b.close()
 (out/'results.json').write_text(json.dumps(records,ensure_ascii=False,indent=2));print('failures',len(issues),'mixer',ok)
 if issues or not ok:raise SystemExit(1)
if __name__=='__main__':main()
