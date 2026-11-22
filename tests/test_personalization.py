"""Synthetic fixtures and deterministic policy tests, optional Chromium/PDF tests."""
import sys,json,copy,io,base64,shutil,argparse,re
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from personalization import custom_palette,validated_palette,PAIRS,contrast,recommend,PHOTO_SLOTS
from render_resume import make_html,load_themes
from render_portfolio import render_portfolio

def fixture(kind):
 if kind=='portrait':
  im=Image.new('RGB',(300,380),'#e4e3da');d=ImageDraw.Draw(im);d.ellipse((99,50,201,152),fill='#627c80');d.rounded_rectangle((46,175,254,350),radius=65,fill='#627c80');alt='虚构头像示意'
 else:
  im=Image.new('RGB',(800,440),'#e6efed');d=ImageDraw.Draw(im);d.rounded_rectangle((45,38,755,400),radius=18,fill='#ffffff');d.rectangle((45,38,755,88),fill='#264b4c');d.rectangle((65,110,245,370),fill='#d8ebe7');d.rounded_rectangle((270,110,730,218),radius=10,fill='#f1e5d5');d.rounded_rectangle((270,235,490,370),radius=10,fill='#b8d8d2');d.rounded_rectangle((505,235,730,370),radius=10,fill='#e3e9ed');alt='虚构项目界面示意'
 f=io.BytesIO();im.save(f,format='PNG',optimize=True);return {'src':'data:image/png;base64,'+base64.b64encode(f.getvalue()).decode(),'alt':alt,'approved':True}
def example():
 data=json.loads((ROOT/'examples/sample_resume.json').read_text());data['photo']=fixture('portrait');data['links']=[{'label':'示例作品主页','url':'https://example.org/portfolio'}]
 for idx,icon in [(0,'education'),(1,'research'),(2,'portfolio'),(4,'award')]:data['sections'][idx]['icon']=icon
 e=data['sections'][2]['entries'][0];e['media']=[dict(fixture('project'),caption='界面原型示意（虚构演示）')];e['links']=[{'label':'示例源码','url':'https://example.org/source'},{'label':'重复链接','url':'https://example.org'}];return data

def core():
 data=example();themes=load_themes();checks=[]
 for t in themes.values():
  h=make_html(data,t);ats=t['ats_candidate'];assert ('class="portrait"' in h)==(not ats);assert ('<figure>' in h)==(not ats);assert ('aria-hidden="true"><svg' in h)==(not ats);assert 'https://example.org/source' in h;assert h.count('href="https://example.org"')==1
  bare=copy.deepcopy(data)
  for k in ('photo','profile','links','contact','target'):bare.pop(k,None)
  bare['sections'][2]['entries'][0].pop('media');bare['sections'].append({'title':'无资料栏目','entries':[]});text=make_html(bare,t);assert 'class="portrait"' not in text and '<figure>' not in text and '无资料栏目' not in text and 'class="bio"' not in text
  assert 'class="portrait"' not in make_html(dict(data,_continuation=True),t)
  if not ats:assert 'photo-'+PHOTO_SLOTS[t['layout']] in h
  checks.append({'theme':t['id'],'optional_fields_media_links_continuation':True})
 for seed in ['#FFFFFF','#000000','#FFFF00','#FF00FF','#C0D5DD','#73DFA3','#E5AA40','#344E8D','#FF5B47','#9B99ED','#12A4E3','#FFD4C0']:
  p=validated_palette(custom_palette(seed,'#2F7269'));assert all(contrast(p[x],p[y])>=4.5 for x,y in PAIRS)
 try:make_html(data,themes['ats-clean'],custom_colors=custom_palette('#FFFF00'));raise AssertionError('ATS custom accepted')
 except ValueError:pass
 bad=copy.deepcopy(data);bad['photo']['src']='https://example.org/a.jpg'
 try:make_html(bad,themes['formal-split']);raise AssertionError('remote asset accepted')
 except ValueError:pass
 assert 'https://example.org/a.jpg' not in make_html(bad,themes['ats-clean']);bad['photo']['approved']=False;assert 'class="portrait"' not in make_html(bad,themes['formal-split'])
 many=copy.deepcopy(data);many['sections'][2]['entries'][0]['media']*=4
 try:make_html(many,themes['formal-split']);raise AssertionError('Unbounded media')
 except ValueError:pass
 assert recommend({'channel':'ats','tone':'bold'})['recommended']==['ats-clean'];assert recommend({'channel':'direct','layout_lock':'book-editorial'})['recommended']==['book-editorial'];assert recommend({'channel':'direct','focus':'clinical'})['recommended'][0]=='research-ledger';assert recommend({'channel':'direct','tone':'young'})['recommended'][0]=='pop-blocks'
 portfolio={'name':'林沐（虚构）','items':[dict(fixture('project'),heading='项目证据示意',contribution='虚构示例，演示项目图与文字相邻。',caption='原型示意',links=[{'label':'示例','url':'https://example.org'}])]};assert '<figure>' in render_portfolio(portfolio)
 (ROOT/'examples/sample_resume_media.json').write_text(json.dumps(data,ensure_ascii=False,indent=2));(ROOT/'examples/sample_portfolio.json').write_text(json.dumps(portfolio,ensure_ascii=False,indent=2));return checks

def browser_checks(out):
 import fitz
 from playwright.sync_api import sync_playwright
 data=example();records=[];out.mkdir(exist_ok=True,parents=True)
 with sync_playwright() as pw:
  b=pw.chromium.launch(headless=True,executable_path=shutil.which('chromium') or None,args=['--no-sandbox'])
  for idx,t in enumerate(load_themes().values()):
   for kind in ('media','sparse'):
    src=copy.deepcopy(data)
    if kind=='sparse':
     for k in ('photo','profile','links','contact','target'):src.pop(k,None)
     src['sections']=src['sections'][:1]
    palette=custom_palette('#E5AA40','#2F7269') if kind=='media' and idx==4 else None
    h=make_html(src,t,custom_colors=palette);p=b.new_page(viewport={'width':900,'height':1300});p.set_content(h,wait_until='load');p.evaluate('document.fonts.ready');loaded=p.evaluate('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)');desktop=p.evaluate('document.documentElement.scrollWidth<=innerWidth+1');p.set_viewport_size({'width':390,'height':844});mobile=p.evaluate('document.documentElement.scrollWidth<=innerWidth+1');p.set_viewport_size({'width':900,'height':1300});p.emulate_media(media='print')
    raw=p.pdf(prefer_css_page_size=True,print_background=True);d=fitz.open(stream=raw,filetype='pdf');s=''.join(x.get_text() for x in d);norm=lambda x:re.sub(r'\s+','',x);ok=all(norm(sec['title']) in norm(s) for sec in src['sections']) and norm(src['name']) in norm(s);rects=True;images=0
    for pg in d:
     for block in pg.get_text('dict')['blocks']:
      if block.get('type')==1:images+=1
      x0,y0,x1,y1=block['bbox'];rects=rects and x0>=-1 and y0>=-1 and x1<=pg.rect.width+1 and y1<=pg.rect.height+1
    expected=kind=='media' and not t['ats_candidate'];image_ok=images>=2 if expected else images==0;links=sum(len(pg.get_links()) for pg in d);link_ok=kind=='sparse' or links>=3
    z={'theme':t['id'],'case':kind,'pages':len(d),'images':images,'links':links,'mobile':mobile,'desktop':desktop,'bounds':rects,'retained':ok,'pass':all([loaded,desktop,mobile,ok,rects,image_ok,link_ok])};records.append(z);print(z,flush=True)
    if kind=='media':
     (out/(t['id']+'.html')).write_text(h);(out/(t['id']+'.pdf')).write_bytes(raw);d[0].get_pixmap(matrix=fitz.Matrix(.85,.85),alpha=False).save(out/(t['id']+'.png'))
    d.close();p.close()
  b.close()
 return records
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--render',action='store_true');a.add_argument('--out',default='/mnt/data/v12-media-qa');a=a.parse_args();checks=core();print('PASS core:',len(checks),'layouts, 12 color seeds, asset policy, ATS, sparse content, links, appendix, recommendation',flush=True)
 if a.render:
  rs=browser_checks(Path(a.out));(ROOT/'tests/results/personalization-results.json').write_text(json.dumps({'core':checks,'browser':rs},ensure_ascii=False,indent=2));assert all(r['pass'] for r in rs),'Browser/PDF checks failed'
