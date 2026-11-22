#!/usr/bin/env python3
"""Fast deterministic tests: structure/token policy, contrasts, content preservation, escaping. Not aesthetic or ATS certification."""
import json,re,sys,html
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from render_resume import load_themes,load_tokens,make_html,resolve,token_css,count_text
T=load_tokens(); themes=load_themes();data=json.loads((ROOT/'examples/sample_resume.json').read_text());errors=[]
def check(x,msg):
 if not x:errors.append(msg)
def luminance(h):
 c=[int(h[i:i+2],16)/255 for i in (1,3,5)];return sum(w*(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4) for v,w in zip(c,(.2126,.7152,.0722)))
def contrast(a,b):
 a,b=sorted([luminance(a),luminance(b)]);return (b+.05)/(a+.05)
pairs=[('ink','paper'),('muted','paper'),('accent','paper'),('ink','panel'),('muted','panel'),('accent','panel'),('band_ink','band'),('highlight_ink','highlight')]
for pid,p in T['palettes'].items():
 for a,b in pairs:check(contrast(p[a],p[b])>=4.5,f'Contrast insufficient: {pid}/{a}/{b}')
for k,r in T['rhythms'].items():
 check(10.5<=r['body_pt']<=12,f'Body size violation {k}');check(r['line_height']>=1.5,f'Leading too tight {k}');check(r['section_gap_pt']>=16,f'Section gap too tight {k}');check(r['entry_gap_pt']>=8 and r['section_gap_pt']>r['entry_gap_pt']>r['title_gap_pt'],f'Spacing hierarchy {k}');check(r['margin_mm']>=15 and r['gutter_mm']>=6,f'Margins/gutter {k}')
check(len(themes)==12 and len({v['layout'] for v in themes.values()})==12,'Layouts not distinct by configuration');check(not any('compact' in k or 'dense' in k for k in themes),'High-density preset remains');check(sum(v['ats_candidate'] for v in themes.values())==1,'Expected one ATS baseline');check(len(T['palettes'])==12 and len(T['fonts'])==7 and len(T['rhythms'])==3,'Token counts changed')
for name in ['SKILL.md','references/06-design-and-style-selection.md','references/09-design-density-contract.md','references/10-design-theory-and-benchmarks.md','references/11-structural-layout-patterns.md','templates/design_tokens.json','templates/themes.json','style-gallery.html','tests/test_rendering.py','tests/test_skill_package.py','templates/photo_policy.json','references/19-chinese-formal-photo-design.md','photo-policy-gallery.html','tests/test_photo_policy_v13.py']:
 check((ROOT/name).exists(),'Missing '+name)
for s in re.findall(r'`((?:references|templates|scripts|examples)/[^`]+\.(?:md|json|py))`',(ROOT/'SKILL.md').read_text()):check((ROOT/s).exists(),'Missing skill reference '+s)
class Collector(HTMLParser):
 def __init__(self):super().__init__();self.sections=[];self.articles=0;self.links=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='section':self.sections.append(a.get('data-source-index'))
  if tag=='article':self.articles+=1
  if tag=='a':self.links.append(a.get('href'))
for sid,t in themes.items():
 h=make_html(data,t);c=Collector();c.feed(h);check(sorted(c.sections)==[str(i) for i in range(len(data['sections']))],f'Missing/duplicate sections {sid}');check(c.articles==sum(len(s['entries']) for s in data['sections']),f'Missing entries {sid}');check('https://example.org' in c.links,f'Link lost {sid}');check('<h1>林沐</h1>' in h,f'Name missing {sid}')
 check((ROOT/'previews'/f'{sid}.html').exists(),f'Missing preview {sid}')
 hbad=make_html({**data,'name':'<script>bad()</script>'},t);check('<script>bad()</script>' not in hbad,f'Unescaped input {sid}')
 bad={**data,'sections':[{'title':'test','entries':[{'link':{'url':'javascript:alert(1)'}}]}]};check('href="javascript:' not in make_html(bad,t),f'Unsafe link {sid}')
 if sid=='ats-clean':
  try:resolve(t,palette='cobalt');check(False,'ATS palette override allowed')
  except ValueError:pass
  try:resolve(t,font='kai-head');check(False,'ATS font override allowed')
  except ValueError:pass
 else:
  # All token values composable at source (not a graphical acceptance of all combinations).
  r=resolve(t,palette='coral',font='serif',rhythm='large',page='Letter');h=make_html(data,t,'coral','serif','large','Letter');check('--body-size:12pt' in h and '@page{size:Letter;' in h and '--paper:#FFF9F6' in h,'Override not propagated '+sid)
 check('/*TOKENS_START*/' in h and '/*PAGE_START*/' in h,'Gallery contract lost')
# Avoid introducing an orphan half module in a two-column grid: final odd short block is made wide.
h=make_html(data,themes['studio-grid']);check('section wide short-section" data-source-index="5"' in h,'Trailing half-cell orphan')
for f in ROOT.rglob('*'):
 if f.is_file() and f.suffix in {'.md','.py','.json','.html'}:
  # No personal contact information from the original author's real resume; only synthetic examples.
  if f.name=='test_skill_package.py':continue
  text=f.read_text(encoding='utf8');check(re.search(r'(?<![0-9])1[3-9][0-9]{9}(?![0-9])',text) is None,'Potential private phone '+str(f.relative_to(ROOT)));check(re.search(r'[\w.-]+@stu[.]edu[.]cn\b',text) is None,'Potential school email '+str(f.relative_to(ROOT)))
check(load_tokens()['version']=='1.3.0','Design token version not updated')
if errors:
 print('\n'.join('FAIL '+e for e in errors));raise SystemExit(1)
print(f'PASS: {len(themes)} structural presets, {len(T["palettes"])} palettes × {len(pairs)} contrast pairs, typography/spacing bounds, composition, ATS lock, escaping and content preservation.')
