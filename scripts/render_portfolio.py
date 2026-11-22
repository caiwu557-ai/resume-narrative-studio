#!/usr/bin/env python3
"""Standalone, human-facing evidence appendix. Explicitly selected assets only; no network."""
import argparse,json
from pathlib import Path
from personalization import verified_image
from render_resume import esc,links_html,resolve,load_themes,token_css

def render_portfolio(data,theme=None):
    r=resolve(theme or load_themes()['formal-split']);pieces=[]
    for item in data.get('items',[]):
        source=verified_image(item)
        if not source:continue
        if not all(item.get(k) for k in ('alt','caption','heading','contribution')):raise ValueError('Portfolio image needs heading, caption, alt and actual contribution')
        pieces.append(f'<article><h2>{esc(item["heading"])}</h2><p>{esc(item["contribution"])}</p><figure><img src="{esc(source)}" alt="{esc(item["alt"])}"><figcaption>{esc(item["caption"])}</figcaption></figure>{links_html(item.get("links",[]),"links")}</article>')
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(data.get('name',''))} · 作品证明</title><style>{token_css(r)}
*{{box-sizing:border-box}}body{{font:var(--body-size)/var(--leading) var(--font-body);color:var(--ink);background:var(--paper);margin:0}}main{{max-width:210mm;margin:auto;padding:17mm}}header{{border-bottom:1pt solid var(--accent);padding-bottom:14pt;margin-bottom:18pt}}h1{{font:700 25pt var(--font-head);margin:0}}h2{{font-size:13pt;margin:0 0 5pt}}p{{margin:0}}article{{margin:0 0 18pt;break-inside:avoid-page}}figure{{margin:8pt 0 0}}img{{width:100%;max-height:110mm;object-fit:contain;object-position:left center;border:1px solid var(--line)}}figcaption,.links{{font-size:10pt;color:var(--muted)}}a{{color:var(--accent)}}@page{{size:A4;margin:17mm}}@media print{{main{{padding:0;max-width:none}}}}@media(max-width:600px){{main{{padding:20px}}}}</style></head><body><main><header><h1>{esc(data.get('name',''))}</h1><p>精选作品与经历证明</p></header>{''.join(pieces)}</main></body></html>'''
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',required=True);p.add_argument('--theme',default='formal-split');a=p.parse_args();Path(a.output).write_text(render_portfolio(json.loads(Path(a.input).read_text()),load_themes()[a.theme]),encoding='utf-8')
