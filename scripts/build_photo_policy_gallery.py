#!/usr/bin/env python3
"""Create a self-contained, synthetic photo placement comparison; no real user photo."""
import argparse,base64,html,json,sys
from pathlib import Path
from io import BytesIO
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tests'))
from test_personalization import example
from render_resume import make_html,load_themes

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
 data=example();policy=json.loads((ROOT/'templates/photo_policy.json').read_text(encoding='utf-8'))
 cards=[]
 with sync_playwright() as pw:
  b=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  for name,t in load_themes().items():
   if t['ats_candidate']:
    continue
   shots=[]
   for label,profile,mode in [('正式 · 右上','cn-formal','auto'),('原版 · 创意','creative','auto')]+([('现代 · 三栏','cn-formal','three-column')] if t['layout'] in ('formal','studio','product','tracks') else []):
    page=b.new_page(viewport={'width':1060,'height':970},device_scale_factor=1)
    page.set_content(make_html(data,t,audience_profile=profile,photo_mode=mode),wait_until='load');page.evaluate('document.fonts.ready')
    rect=page.locator('.page').bounding_box();top=rect['y'];height=min(405,rect['height'])
    raw=page.screenshot(clip={'x':round(rect['x']),'y':round(top),'width':round(rect['width']),'height':int(height)})
    img=Image.open(BytesIO(raw)).convert('RGB');img.thumbnail((420,230))
    buff=BytesIO();img.save(buff,format='JPEG',quality=84,optimize=True)
    uri='data:image/jpeg;base64,'+base64.b64encode(buff.getvalue()).decode('ascii')
    shots.append((label,uri));page.close()
   item=policy['templates'][name];status=item['cn_formal_recommendation']
   leg='优选' if status=='preferred' else '合理' if status=='good' else '有条件合理' if status=='conditional' else '正式默认不推荐'
   cards.append(f'<section class="card"><div class="h"><b>{html.escape(name)}</b><span>{leg}</span></div><div class="shots">'+''.join(f'<figure><figcaption>{html.escape(label)}</figcaption><img alt="{html.escape(name+" "+label)}实际渲染" src="{uri}"></figure>' for label,uri in shots)+f'</div><p>{html.escape(item.get("reason",""))}</p></section>')
  b.close()
 output=Path(a.output);output.parent.mkdir(parents=True,exist_ok=True)
 web='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>头像位置 A/B 审计 · Resume Narrative Studio v1.3</title><style>body{margin:0;background:#f5f6f3;color:#202b30;font-family:Arial,'Microsoft YaHei',sans-serif}main{max-width:1450px;margin:auto;padding:44px 25px}h1{font-size:30px;margin:0 0 10px;font-weight:650}p.lead{line-height:1.9;color:#5b6668;max-width:860px;font-size:14px;margin:0 0 32px}.gallery{display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr));gap:20px}.card{border-radius:11px;background:white;box-shadow:0 6px 21px #15252e11;border:1px solid #e0e3df;padding:18px;overflow:hidden}.h{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:15px}.h b{font-size:15px}.h span{font-size:12px;color:#58736d}.shots{display:flex;gap:10px}.shots figure{margin:0;min-width:0;flex:1}.shots img{display:block;width:100%;border:1px solid #dbe2de;border-radius:3px;object-fit:contain;background:#fff}.shots figcaption{font-size:11px;color:#576566;margin-bottom:9px}.card p{font-size:12px;color:#647070;line-height:1.7;margin:14px 0 0}aside{margin:28px 0 0;color:#62706b;line-height:1.9;font-size:12px}@media(max-width:700px){main{padding:24px 13px}.gallery{display:block}.card{margin-bottom:15px}.shots{display:block}.shots figure{margin-bottom:16px}}</style></head><body><main><h1>11 款含照片布局：正式版与原创意版对照</h1><p class="lead">均为自动生成的虚构示意头像与虚构履历。正式版默认采用页眉右上独立式；原版创意位置保持不变，4款适合的布局另外展示现代三栏式。第12款 ATS 简历无头像，因此不列入下方有照对照。</p><div class="gallery">'''+''.join(cards)+'''</div><aside>政策依据：湖南第一师范学院就业指南的中文简历实践建议、NN/g视觉层级与接近原则；ATS例外遵循UCSD/Princeton的美国求职指导。结论是有条件的设计建议，不代表任何国家的统一强制规则。照片与真实个人经历均不在本演示中。</aside></main></body></html>'''
 output.write_text(web,encoding='utf-8');print('created',output,'cards',len(cards),'size',round(output.stat().st_size/1048576,2),'MiB')

if __name__=='__main__':main()
