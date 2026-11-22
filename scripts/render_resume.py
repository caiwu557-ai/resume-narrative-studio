#!/usr/bin/env python3
"""Render a self-contained resume. A design system, not a fact checker or ATS certificate."""
from __future__ import annotations
import argparse, html, json, re
from pathlib import Path
from urllib.parse import urlparse
from personalization import PHOTO_SLOTS,verified_image,validated_palette,normalize_data,select_photo_mode
ROOT=Path(__file__).resolve().parent.parent

def esc(v): return html.escape(str(v if v is not None else ''),quote=True)
def load_tokens(): return json.loads((ROOT/'templates/design_tokens.json').read_text(encoding='utf-8'))
def load_themes(): return {v['id']:v for v in load_tokens()['layouts']}
def valid_external_url(uri):
    if not isinstance(uri,str): return False
    p=urlparse(uri)
    return p.scheme in ('http','https') and bool(p.netloc) and not p.username and not p.password

def resolve(theme, palette=None, font=None, rhythm=None, page='A4', custom_colors=None):
    t=load_tokens(); r=dict(theme)
    r.update(palette_id=palette or r['palette_id'],font_id=font or r['font_id'],rhythm_id=rhythm or r['rhythm_id'],page=page)
    if page not in t['allowed_page_sizes']: raise ValueError('Unknown page size')
    for key,group in [('palette_id','palettes'),('font_id','fonts'),('rhythm_id','rhythms')]:
        if r[key] not in t[group]: raise ValueError(f'Unknown {key}: {r[key]}')
    if r.get('ats_candidate') and (r['palette_id']!='paper' or r['font_id']!='neutral'):
        raise ValueError('ATS baseline locks paper palette and neutral font. Choose another layout for visual customisation.')
    if custom_colors is not None and r.get('ats_candidate'):raise ValueError('ATS must use paper colors')
    r['colors']=validated_palette(custom_colors) if custom_colors is not None else t['palettes'][r['palette_id']];r['fonts']=t['fonts'][r['font_id']];r['rhythm']=t['rhythms'][r['rhythm_id']]
    return r

def token_css(r):
    p,f,s=r['colors'],r['fonts'],r['rhythm']; v={k.replace('_','-'):v for k,v in p.items() if k!='title'}
    v.update({'font-body':f['body'],'font-head':f['heading'],'head-weight':f['weight'],'body-size':str(s['body_pt'])+'pt','leading':s['line_height'],'head-size':str(s['heading_pt'])+'pt','section-gap':str(s['section_gap_pt'])+'pt','entry-gap':str(s['entry_gap_pt'])+'pt','title-gap':str(s['title_gap_pt'])+'pt','bullet-gap':str(s['bullet_gap_pt'])+'pt','gutter':str(s['gutter_mm'])+'mm','margin':str(s['margin_mm'])+'mm','page-width':'210mm' if r['page']=='A4' else '215.9mm','page-height':'297mm' if r['page']=='A4' else '279.4mm'})
    return ':root{'+''.join(f'--{k}:{v};' for k,v in v.items())+'}'

CSS=r'''
*{box-sizing:border-box}html{background:#e9ebee}body{margin:0;color:var(--ink);font-family:var(--font-body);font-size:var(--body-size);line-height:var(--leading);font-weight:400;overflow-wrap:anywhere}a{color:var(--accent);text-underline-offset:2px;text-decoration-thickness:.6px}p,h1,h2,h3{margin:0}h1,h2,h3{font-family:var(--font-head);font-weight:var(--head-weight)}h1{font-size:29pt;line-height:1.2;letter-spacing:-.025em}h2{font-size:var(--head-size);line-height:1.35;break-after:avoid-page}h3{font-size:var(--body-size);line-height:1.45;break-after:avoid-page}p{margin:0}ul{margin:3pt 0 0;padding-left:1.2em}li{padding-left:1pt;margin:var(--bullet-gap) 0 0}li:first-child{margin-top:0}.page{width:100%;max-width:var(--page-width);min-height:var(--page-height);padding:var(--margin);margin:20px auto;background:var(--paper);box-shadow:0 6px 24px #1a26301a}.header{margin-bottom:var(--section-gap);padding-bottom:12pt;border-bottom:1.2pt solid var(--accent)}.identity,.info,.bio,.content,.section,.section-body,.entry,.entry-content{min-width:0}.subtitle{margin-top:5pt;font-weight:600}.target{margin-top:3pt;color:var(--muted);font-size:10pt}.contact{display:flex;flex-wrap:wrap;gap:2pt 9pt;color:var(--muted);font-size:10pt;margin-top:6pt;line-height:1.5}.profile{margin-top:9pt;max-width:44em}.section{margin-bottom:var(--section-gap)}.section:last-child{margin-bottom:0}.section-title{margin-bottom:var(--title-gap);color:var(--accent);padding-bottom:3pt;border-bottom:.65pt solid var(--line)}.entry{margin-bottom:var(--entry-gap);break-inside:auto}.entry:last-child{margin-bottom:0}.entry-head{display:flex;align-items:baseline;justify-content:space-between;gap:3pt 10pt;flex-wrap:wrap;margin-bottom:2.5pt;break-after:avoid-page}.entry-meta{font-size:10pt;line-height:1.45;color:var(--muted)}.entry-text,.entry li{font-size:var(--body-size);line-height:var(--leading)}.entry-link{font-size:10pt;margin-top:4pt}.entry-link a{overflow-wrap:anywhere}.section-title,.entry-head{page-break-after:avoid}.entry-text,li,.profile{orphans:2;widows:2}h1{orphans:2;widows:2}.grid-flow{display:block}.marker{display:none}.section{break-inside:auto}.section-title{break-inside:avoid}.section-body{break-inside:auto}.entry-head:empty{display:none}.secondary .section-title{font-size:var(--head-size)}
/* Structural compositions: no font-size or spacing reduction by layout. */
.l-plain .header{border-color:var(--ink);border-width:.7pt;padding-bottom:10pt}.l-plain .section-title{color:var(--ink);border-color:var(--ink);border-width:.5pt}.l-plain .entry-head{display:block}.l-plain .entry-meta{display:inline-block;margin-bottom:2pt}.l-plain .contact{color:var(--ink)}
.l-formal .header{display:grid;grid-template-columns:1.25fr 1fr;column-gap:var(--gutter);align-items:end;border-top:4pt solid var(--accent);padding-top:10pt}.l-formal .info{border-left:.7pt solid var(--line);padding-left:13pt;align-self:stretch;display:flex;flex-direction:column;justify-content:center}.l-formal .bio{grid-column:1/-1}.l-formal .contact{display:block}.l-formal .contact span{display:block}.l-formal .section-title{border:0;border-left:3pt solid var(--accent);padding:0 0 0 8pt}.l-formal h1{font-size:30pt}
.l-ledger .header{border-bottom:2pt solid var(--ink);padding-bottom:11pt}.l-ledger .section{display:grid;grid-template-columns:24% 1fr;gap:var(--gutter);padding-top:8pt;border-top:.6pt solid var(--line)}.l-ledger .section-title{border:0;padding:0;margin:0;word-break:normal}.l-ledger .entry-head{display:block}.l-ledger .entry-meta{margin-top:2pt}.l-ledger .section:first-child{border-top:0;padding-top:0}.l-ledger .marker{display:block;font-family:var(--font-body);font-size:10pt;letter-spacing:.05em;color:var(--muted);font-weight:500;margin-bottom:3pt}
.l-ivory .header{text-align:center;border:0;padding-top:4pt;padding-bottom:5pt}.l-ivory h1{font-size:33pt;letter-spacing:.09em}.l-ivory .contact{justify-content:center}.l-ivory .bio{text-align:left;border-block:.6pt solid var(--line);padding:8pt 0;margin-top:9pt}.l-ivory .profile{margin:0;max-width:none}.l-ivory .section-title{display:flex;align-items:center;justify-content:center;gap:12pt;padding:0;border:0;margin-bottom:8pt;text-align:center}.l-ivory .section-title:before,.l-ivory .section-title:after{content:'';height:.6pt;background:var(--line);flex:1}.l-ivory .entry-head{gap:4pt 12pt}
.l-book .header{display:grid;grid-template-columns:1fr .92fr;align-items:end;gap:0 var(--gutter);border-bottom:2pt solid var(--ink);padding:0 0 13pt}.l-book .identity{grid-column:1}.l-book h1{font-size:37pt;line-height:1.15}.l-book .info{grid-column:1;grid-row:2}.l-book .bio{grid-column:2;grid-row:1/span 2;border-left:.8pt solid var(--line);padding-left:14pt;align-self:end}.l-book .profile{margin:0}.l-book .section-title{border-bottom:0;border-top:.8pt solid var(--accent);padding-top:7pt;padding-bottom:0}.l-book .section-title .marker{display:inline-block;margin-right:10pt;font-family:var(--font-body);font-weight:400;color:var(--muted);font-size:10pt}.l-book .entry-title{font-family:var(--font-head)}
.l-studio .header{padding-bottom:12pt;border:0;border-bottom:2pt solid var(--ink);display:grid;grid-template-columns:1fr 1fr;column-gap:var(--gutter)}.l-studio .identity{grid-column:1}.l-studio .info{align-self:end}.l-studio .bio{grid-column:1/-1}.l-studio .grid-flow{display:grid;grid-template-columns:1fr 1fr;gap:var(--section-gap) var(--gutter);align-items:start}.l-studio .section{padding:10pt;border:1pt solid var(--line);margin:0;break-inside:avoid-page}.l-studio .section.wide{grid-column:1/-1}.l-studio .section-title{border:0;margin-bottom:8pt;padding:0;font-size:var(--head-size)}.l-studio .entry-head{display:block}.l-studio .marker{display:inline-block;margin-right:8pt;font-size:10pt;font-weight:500;color:var(--muted)}
.l-product .header{border:0;border-bottom:2pt solid var(--accent);display:grid;grid-template-columns:1fr auto;column-gap:var(--gutter);align-items:start}.l-product .bio{grid-column:1/-1}.l-product .info{align-self:start}.l-product .contact{display:block}.l-product .contact span{display:block}.l-product .section-title{border:0}.l-product .feature{padding:13pt;background:var(--panel);border:1pt solid var(--line);border-left:4pt solid var(--accent);break-inside:auto}.l-product .feature .section-title{font-size:calc(var(--head-size) + 2pt);border:0;margin-bottom:8pt}.l-product .feature .entry-head{display:grid;grid-template-columns:1fr auto;align-items:start}.l-product .feature .entry-title{font-weight:700}.l-product .feature .entry-meta{max-width:16em}.l-product .feature .entry-content{padding-top:2pt}.l-product .feature .marker{display:block;font-family:var(--font-body);font-weight:600;font-size:10pt;color:var(--accent);letter-spacing:.03em;margin-bottom:3pt}
.l-rail .resume-inner{display:grid;grid-template-columns:30% 1fr;gap:var(--gutter);align-items:start}.l-rail .header{background:var(--band);color:var(--band-ink);padding:14pt;border:0;margin:0;min-height:100%;break-inside:auto}.l-rail .header h1{font-size:25pt;overflow-wrap:anywhere}.l-rail .header .subtitle{margin-top:12pt}.l-rail .header .target,.l-rail .header .contact{color:var(--band-ink)}.l-rail .contact{display:block;border-top:.6pt solid var(--band-ink);padding-top:10pt;margin-top:13pt}.l-rail .contact span{display:block;margin-bottom:4pt}.l-rail .profile{margin-top:14pt}.l-rail .section-title{padding-bottom:5pt;border-bottom:1pt solid var(--line)}.l-rail .entry-head{display:block}.l-rail .entry-meta{display:block;margin-top:2pt}.l-rail .section:first-child .section-title{margin-top:0}
.l-index .header{border:0;border-bottom:1.2pt solid var(--accent);padding-bottom:12pt}.l-index .section-title{border:0;border-bottom:.7pt solid var(--line)}.l-index .entry.has-meta{display:grid;grid-template-columns:25% 1fr;column-gap:var(--gutter);align-items:start}.l-index .entry.has-meta .entry-head{display:contents}.l-index .entry.has-meta .entry-meta{grid-column:1;grid-row:1/span 2;color:var(--accent);border-right:1pt solid var(--line);padding-right:8pt;min-height:100%}.l-index .entry.has-meta .entry-title{grid-column:2;grid-row:1;margin-bottom:2pt}.l-index .entry.has-meta .entry-content{grid-column:2;grid-row:2}.l-index .entry:not(.has-meta) .entry-head{display:block}
.l-poster .header{background:var(--band);color:var(--band-ink);padding:15pt 17pt;border:0;border-bottom:7pt solid var(--highlight);margin-bottom:var(--section-gap)}.l-poster .header h1{font-size:37pt;line-height:1.16;font-weight:900;letter-spacing:-.045em}.l-poster .header .target,.l-poster .header .contact{color:var(--band-ink)}.l-poster .bio{border-top:.6pt solid var(--band-ink);padding-top:7pt;margin-top:9pt}.l-poster .profile{margin-top:0}.l-poster .section-title{border:0;padding:3pt 0 3pt 9pt;border-left:6pt solid var(--highlight);color:var(--ink);border-bottom:.5pt solid var(--line)}.l-poster .marker{display:inline-block;color:var(--accent);font-family:var(--font-body);font-size:10pt;font-weight:700;margin-right:9pt}
.l-pop .header{display:grid;grid-template-columns:1fr .72fr;gap:0 0;border:0;padding:0}.l-pop .identity{background:var(--highlight);color:var(--highlight-ink);padding:14pt 12pt}.l-pop .identity h1{font-size:28pt;line-height:1.22}.l-pop .info{background:var(--band);color:var(--band-ink);padding:12pt;display:flex;flex-direction:column;justify-content:center}.l-pop .contact,.l-pop .target{color:var(--band-ink);display:block}.l-pop .contact span{display:block}.l-pop .bio{grid-column:1/-1;background:var(--panel);padding:10pt 12pt}.l-pop .profile{margin:0}.l-pop .grid-flow{display:grid;grid-template-columns:1.18fr .82fr;gap:var(--section-gap) var(--gutter);align-items:start}.l-pop .section{margin:0;break-inside:avoid-page}.l-pop .section.wide{grid-column:1/-1}.l-pop .section-title{display:inline-flex;align-items:center;gap:6pt;padding:4pt 8pt;background:var(--panel);color:var(--ink);border:0;border-radius:4pt;margin-bottom:7pt}.l-pop .marker{display:inline;font-size:10pt;color:var(--accent);font-family:var(--font-body)}.l-pop .entry-head{display:block}.l-pop .section.wide .entry-head{display:flex}
.l-tracks .header{border-bottom:1.5pt solid var(--ink);display:grid;grid-template-columns:1fr .8fr;gap:0 var(--gutter);align-items:end}.l-tracks .bio{grid-column:1/-1}.l-tracks .contact{display:block}.l-tracks .contact span{display:block}.l-tracks .tracks{display:grid;grid-template-columns:1fr 33%;gap:var(--gutter);align-items:start}.l-tracks .secondary{background:var(--panel);padding:11pt}.l-tracks .secondary .section-title{border-bottom:.6pt solid var(--line);color:var(--ink)}.l-tracks .secondary .entry-head{display:block}.l-tracks .primary .section-title{border:0;border-bottom:1pt solid var(--line)}
/* Long-form safety applies to preview and print, never shrinks typography. */
.long-form .grid-flow{display:block}.long-form .grid-flow .section{margin-bottom:var(--section-gap);break-inside:auto}.long-form .grid-flow .short-section{break-inside:avoid-page}.long-form.l-rail .resume-inner,.long-form.l-tracks .tracks{display:block}.long-form.l-rail .header{min-height:0;margin-bottom:var(--section-gap)}.long-form.l-tracks .secondary{margin-top:var(--section-gap)}
/* Deliberate continuation header: maintain identity and tokens, not a second cover. */
.continuation .resume-inner{display:block}.continuation .header{display:block!important;background:none!important;color:var(--ink)!important;min-height:0!important;padding:0 0 8pt!important;border:0!important;border-bottom:1pt solid var(--line)!important;margin-bottom:var(--section-gap)!important;text-align:left!important}.continuation .identity{background:none!important;color:var(--ink)!important;padding:0!important}.continuation .header h1{font-size:17pt!important;line-height:1.3!important;letter-spacing:0!important}.continuation .header .subtitle{font-size:10pt!important;margin-top:2pt!important}.continuation .header .info,.continuation .header .bio{display:none!important}
/* On short screens use natural order and a single reading lane; print stays on intended layout. */
@media screen and (max-width:650px){.page{margin:0;min-height:0;padding:20px;box-shadow:none}.header,.l-formal .header,.l-book .header,.l-studio .header,.l-product .header,.l-pop .header,.l-tracks .header,.l-rail .resume-inner,.l-ledger .section,.l-index .entry.has-meta,.l-tracks .tracks,.l-studio .grid-flow,.l-pop .grid-flow{display:block}.l-rail .header{margin-bottom:var(--section-gap)}.l-ledger .section-title{margin-bottom:8pt}.l-index .entry.has-meta .entry-head{display:block}.l-index .entry.has-meta .entry-meta{border:0;padding:0;margin-top:2pt}.l-book .bio{border:0;padding:0;margin-top:8pt}.l-formal .info{border:0;padding:0;margin-top:8pt}.l-studio .section,.l-pop .section{margin-bottom:var(--section-gap)}.l-product .feature .entry-head{display:block}.l-tracks .secondary{margin-top:var(--section-gap)}.l-rail .contact span{margin-bottom:3pt}.entry-head{display:block}.l-poster .header h1,.l-book h1{font-size:30pt}}
@media print{html,body{background:var(--paper);margin:0}.page{margin:0;padding:0;max-width:none;width:100%;min-height:0;box-shadow:none;print-color-adjust:exact;-webkit-print-color-adjust:exact}.header{break-inside:avoid-page}.section-title,.entry-head{page-break-after:avoid}.short-section{break-inside:avoid-page}.entry-text,li{orphans:2;widows:2}.l-studio .section.wide,.l-pop .section.wide{break-inside:auto}.long-form .grid-flow{display:block}.long-form .grid-flow .section{margin-bottom:var(--section-gap);break-inside:auto}.long-form .grid-flow .short-section{break-inside:avoid-page}.long-form.l-rail .resume-inner,.long-form.l-tracks .tracks{display:block}.long-form.l-rail .header{min-height:0;margin-bottom:var(--section-gap)}.long-form.l-tracks .secondary{margin-top:var(--section-gap)}}
'''

CSS += r"""
/* v1.2: optional approved visual assets, never occupy space when absent. */
.portrait{display:block;width:26mm;height:32mm;object-fit:cover;object-position:center;flex:none;border:1pt solid var(--line);border-radius:3pt}.with-photo .identity{display:flex;align-items:center;gap:12pt}.with-photo .identity-copy{flex:1;min-width:0}.with-photo.photo-center-top .identity,.with-photo.photo-identity-top .identity,.with-photo.photo-rail-top .identity{flex-direction:column;align-items:start}.with-photo.photo-center-top .identity{align-items:center}.photo-center-top .portrait,.photo-identity-top .portrait,.photo-rail-top .portrait{order:-1}.photo-rail-top .portrait{width:25mm;height:31mm}.l-poster.with-photo .portrait{width:30mm;height:36mm}.l-formal.with-photo .header,.l-studio.with-photo .header,.l-product.with-photo .header,.l-tracks.with-photo .header{grid-template-columns:minmax(0,1.4fr) minmax(0,.8fr)}.with-photo.l-book .header{grid-template-columns:minmax(0,1fr) minmax(0,.85fr)}.with-photo .header .info a{color:inherit}.contact a{color:inherit}.contact-links{display:flex;gap:4pt 9pt;flex-wrap:wrap;margin-top:5pt;font-size:10pt}.l-rail .contact-links,.l-pop .contact-links,.l-poster .contact-links{color:var(--band-ink)}.entry-media{display:grid;grid-template-columns:1fr;gap:7pt;margin-top:8pt;break-inside:avoid-page}.entry-media.pair{grid-template-columns:1fr 1fr}.entry-media figure{margin:0;min-width:0;break-inside:avoid-page}.entry-media img{display:block;width:auto;max-width:100%;height:auto;max-height:43mm;object-fit:contain;object-position:left center;background:var(--panel);border:.5pt solid var(--line)}.entry-media figcaption{font-size:10pt;line-height:1.5;margin-top:4pt;color:var(--muted)}.section-icon{display:inline-flex;vertical-align:middle;width:1.1em;height:1.1em;margin-right:7pt;color:var(--accent);align-items:center}.section-icon svg{width:100%;height:100%;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}.continuation .portrait{display:none!important}.no-info .info{display:none!important}.no-info.l-formal .header,.no-info.l-studio .header,.no-info.l-product .header,.no-info.l-tracks .header,.no-info.l-pop .header{grid-template-columns:1fr}.no-info.l-book .header{grid-template-columns:1fr}.no-info.l-book .bio,.no-bio.l-book .identity,.no-bio.l-book .info{grid-column:1/-1;grid-row:auto}.no-info.l-book .bio{padding-left:0;border-left:0;margin-top:9pt}.no-bio.l-book .header{grid-template-columns:1fr}.no-info.l-pop .identity{grid-column:1/-1}.continuation .identity-copy{flex:auto}
@media screen and (max-width:650px){.with-photo .identity{gap:9pt}.with-photo .portrait{width:22mm;height:27mm}.entry-media.pair{grid-template-columns:1fr}.with-photo.l-book .header,.with-photo.l-formal .header,.with-photo.l-studio .header,.with-photo.l-product .header,.with-photo.l-tracks .header{display:block}}
"""
# v1.3 contextual identity layout. Header-right is the default for *requested* photos
# in mainland China formal human-readable applications, not a global mandate.
PHOTO_CSS=r'''
.photo-header-right .header{position:relative;display:block!important;min-height:calc(32mm + 12pt);padding-right:calc(26mm + 15pt)!important;overflow:visible}
.photo-header-right .header .identity{display:block!important;grid-column:auto;grid-row:auto;padding:0;background:transparent;color:inherit;border:0}
.photo-header-right .header .identity-copy{display:block;min-width:0}
.photo-header-right .header .info{display:block!important;grid-column:auto;grid-row:auto;position:static;min-width:0;background:transparent;border:0;padding:0;color:inherit;margin-top:6pt}
.photo-header-right .header .info .contact,.photo-header-right .header .info .contact-links,.photo-header-right .header .info .target{color:inherit;display:flex;flex-wrap:wrap;gap:2pt 10pt}
.photo-header-right .header .bio{display:block;grid-column:auto;grid-row:auto;position:static;padding:0;border-left:0;margin-top:9pt;max-width:100%;text-align:left;background:transparent;color:inherit}
.photo-header-right .header .bio .profile{max-width:none}
.photo-header-right .portrait{position:absolute;top:4pt;right:0;order:initial;width:26mm;height:32mm;z-index:1}
.photo-header-right.l-poster .portrait{right:15pt;top:15pt;max-height:32mm}
.photo-header-right.l-poster .header{min-height:calc(32mm + 30pt);padding-right:calc(26mm + 33pt)!important}
.photo-header-right.l-pop .header .identity h1,.photo-header-right.l-pop .header .info{color:var(--ink)}
.photo-header-right.l-rail .resume-inner{display:block!important}
.photo-header-right.l-rail .header{color:var(--ink);background:var(--paper);padding:0 0 12pt;border-bottom:1.2pt solid var(--accent);min-height:calc(32mm + 12pt);margin-bottom:var(--section-gap)}
.photo-header-right.l-ivory .header{text-align:left}
.photo-header-right.l-ivory .header .contact{justify-content:start}
.photo-header-right.l-ivory .header .bio{text-align:left;border-top:.6pt solid var(--line);padding-top:7pt}
.photo-three-column .header{display:grid!important;grid-template-columns:minmax(0,1.13fr) minmax(0,.87fr) 26mm!important;column-gap:var(--gutter);row-gap:7pt;align-items:center}
.photo-three-column .header .identity{grid-column:1;grid-row:1;display:block!important;min-width:0}
.photo-three-column .header .info{grid-column:2;grid-row:1;min-width:0;border-left:.7pt solid var(--line);padding-left:9pt;margin:0;display:block;background:transparent;color:inherit}
.photo-three-column .header .info .contact{display:block}
.photo-three-column .header .info .contact span{display:block;overflow-wrap:anywhere}
.photo-three-column .header .bio{grid-column:1/-1;grid-row:2;min-width:0}
.photo-three-column .header .portrait{grid-column:3;grid-row:1;position:static;width:26mm;height:32mm;order:initial;justify-self:end}
.photo-three-column .header .info .target,.photo-three-column .header .info .contact,.photo-three-column .header .info .contact-links{color:inherit}
@media screen and (max-width:650px){
  .photo-three-column .header{display:block!important}
  .photo-three-column .header .info{border-left:0;padding-left:0;margin-top:7pt}
  .photo-three-column .header .portrait{width:22mm;height:27mm;margin-top:9pt}
  .photo-header-right .header{padding-right:calc(22mm + 9pt)!important;min-height:calc(27mm + 10pt)}
  .photo-header-right .portrait{width:22mm;height:27mm;right:0;top:0}
  .photo-header-right.l-poster .portrait{right:8pt;top:8pt}
}
'''
# Small original geometric pictograms; no external assets or library license claim. Official repository catalog in reference 14.
ICONS={'education':'<path d="M2 9l10-5 10 5-10 5zM6 11v6q6 5 12 0v-6"/>','research':'<path d="M9 3h6M10 3v7l-5 9h14l-5-9V3M8 15h8"/>','work':'<rect x="3" y="7" width="18" height="14" rx="2"/><path d="M8 7V3h8v4M3 13h18"/>','award':'<circle cx="12" cy="9" r="6"/><path d="M8 14l-2 8 6-3 6 3-2-8"/>','portfolio':'<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M7 13h4M7 16h10"/>','service':'<path d="M12 20S3 14 3 8a5 5 0 019-2 5 5 0 019 2c0 6-9 12-9 12z"/>','skills':'<path d="M4 17l5-5 4 4 7-9M4 5h5M4 8h3"/>','target':'<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>'}

def links_html(items,css):
    good=[];seen=set()
    for link in items:
        if isinstance(link,dict) and valid_external_url(link.get('url')) and link['url'] not in seen:
            seen.add(link['url']);good.append(f'<a href="{esc(link["url"])}" rel="noopener noreferrer">{esc(link.get("label") or link["url"])}</a>')
    return f'<div class="{css}">'+ ' · '.join(good)+'</div>' if good else ''

def count_text(obj):
    if isinstance(obj,str):return len(obj)
    if isinstance(obj,list):return sum(count_text(x) for x in obj)
    if isinstance(obj,dict):return sum(count_text(v) for k,v in obj.items() if k not in ('url','src','alt','approved','featured','placement','span','photo','icon','media'))
    return 0

def make_html(data,theme,palette=None,font=None,rhythm=None,page='A4',custom_colors=None,audience_profile=None,photo_mode=None):
    data=normalize_data(data)
    r=resolve(theme,palette,font,rhythm,page,custom_colors); layout=r['layout']; is_ats=r['ats_candidate']; m=r['rhythm']['margin_mm']; secs=data.get('sections',[])
    if not isinstance(secs,list):raise ValueError('sections must be a list')
    # Conservative long-form trigger: preserve algorithmic reading order and avoid fragile multi-page CSS grids.
    text_len=count_text(data); longform=text_len>1600 or len(secs)>10 or any(count_text(s)>700 for s in secs)
    continuation=data.get("_continuation") is True
    portrait=None if is_ats or continuation else verified_image(data.get('photo'))
    photo_slot=select_photo_mode(layout, profile=audience_profile or data.get('audience_profile','general'), requested=photo_mode or data.get('photo_mode','auto'), is_ats=is_ats) if portrait else 'none'
    if photo_slot=='none':portrait=None
    direct_photo=bool(portrait) and photo_slot in ('header-right','three-column')
    sparse_header=not (data.get('contact') or data.get('target') or data.get('links'))
    absent_bio=not data.get('profile')
    total=0
    if not is_ats:
        for sec in secs:
            for e in sec.get('entries',[]):
                n=sum(1 for obj in e.get('media',[]) if verified_image(obj))
                if n>2:raise ValueError('Maximum two visual assets per entry. Move excess into portfolio appendix.')
                total+=n
        if total>3:raise ValueError('Maximum three inline visual assets. Move excess into a separate portfolio appendix.')
    P=[]
    P.append(f'<!doctype html><html lang="{esc(data.get("lang","zh-CN"))}"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(data.get("name","简历"))}</title><style>/*TOKENS_START*/{token_css(r)}/*TOKENS_END*//*PAGE_START*/@page{{size:{page};margin:{m}mm}}/*PAGE_END*/{CSS}{PHOTO_CSS}</style></head><body>')
    P.append(f'<main class="page l-{esc(layout)}{" long-form" if longform else ""}{" continuation" if continuation else ""}{" with-photo photo-"+photo_slot if portrait else ""}{" no-info" if sparse_header else ""}{" no-bio" if absent_bio else ""}" data-layout="{esc(layout)}" data-theme="{esc(r["id"])}" data-ats="{str(is_ats).lower()}"><div class="resume-inner">')
    P.append('<header class="header"><div class="identity">')
    if portrait and not direct_photo:P.append('<div class="identity-copy">')
    P.append(f'<h1>{esc(data.get("name","姓名"))}</h1>')
    if data.get('subtitle'):P.append(f'<p class="subtitle">{esc(data["subtitle"])}</p>')
    if portrait and not direct_photo:
        P.append(f'</div><img class="portrait" src="{esc(portrait)}" alt="{esc(data["photo"].get("alt","个人照片"))}">')
    P.append('</div><div class="info">')
    if data.get('target'):P.append(f'<p class="target">{esc(data["target"])}</p>')
    if data.get('contact'):P.append('<div class="contact">'+''.join(f'<span>{esc(x)}</span>' for x in data['contact'])+'</div>')
    P.append(links_html(data.get('links',[]),'contact-links'))
    P.append('</div>')
    if direct_photo:P.append(f'<img class="portrait" src="{esc(portrait)}" alt="{esc(data["photo"].get("alt","个人照片"))}">')
    if data.get('profile'):P.append(f'<div class="bio"><p class="profile">{esc(data["profile"])}</p></div>')
    P.append('</header><div class="content">')
    # A short orphan before a full-width module, or at the end, becomes full-width instead of wasting a half-row.
    wide_map={i:(not is_ats and any(any(verified_image(o) for o in e.get('media',[])) for e in s.get('entries',[])) or s.get('span')=='full' or count_text(s)>165 or len(s.get('entries',[]))>1) for i,s in enumerate(secs)}
    if layout in ('studio','pop'):
        run=[]
        for i in range(len(secs)+1):
            if i==len(secs) or wide_map[i]:
                if len(run)%2:wide_map[run[-1]]=True
                run=[]
            else:run.append(i)
    def sec_html(s,i):
        wide=wide_map[i]
        i=int(s.get("_source_index",i))
        # User-confirmed feature flag and side placement; no implied importance invented.
        feature=layout=='product' and s.get('featured') is True
        c='section'+(' wide' if wide else '')+(' feature' if feature else '')+(' short-section' if count_text(s)<380 else '')
        S=[f'<section class="{c}" data-source-index="{i}"><h2 class="section-title">']
        if layout in ('ledger','book','studio','poster','pop'):
            S.append(f'<span class="marker" aria-hidden="true">{i+1:02d}</span>')
        if feature:S.append('<span class="marker">精选项目</span>')
        if not is_ats and s.get('icon') in ICONS:S.append('<span class="section-icon" aria-hidden="true"><svg viewBox="0 0 24 24">'+ICONS[s['icon']]+'</svg></span>')
        S.append(esc(s.get('title',f'经历 {i+1}'))+'</h2><div class="section-body">')
        for e in s.get('entries',[]):
            heading,meta=e.get('heading'),e.get('meta'); S.append('<article class="entry'+(' has-meta' if meta and heading else '')+'">')
            if heading or meta:
                S.append('<div class="entry-head">')
                if heading:S.append(f'<h3 class="entry-title">{esc(heading)}</h3>')
                if meta:S.append(f'<p class="entry-meta">{esc(meta)}</p>')
                S.append('</div>')
            S.append('<div class="entry-content">')
            if e.get('detail'):S.append(f'<p class="entry-text">{esc(e["detail"])}</p>')
            if e.get('bullets'):S.append('<ul>'+''.join(f'<li>{esc(b)}</li>' for b in e['bullets'])+'</ul>')
            items=([e['link']] if e.get('link') else [])+e.get('links',[])
            S.append(links_html(items,'entry-link'))
            if not is_ats:
                media=[(o,verified_image(o)) for o in e.get('media',[]) if o.get('approved') is True]
                if media:
                    S.append('<div class="entry-media'+(' pair' if len(media)>1 else '')+'">')
                    for o,src in media:
                        if not o.get('alt') or not o.get('caption'):raise ValueError('Informative media requires alt and caption')
                        S.append(f'<figure><img src="{esc(src)}" alt="{esc(o["alt"])}"><figcaption>{esc(o["caption"])}</figcaption></figure>')
                    S.append('</div>')
            S.append('</div></article>')
        return ''.join(S)+'</div></section>'
    if layout=='tracks' and any(s.get('placement')=='support' for s in secs):
        # Grouped reading order is explicit and is a visual-only variant. All content retained once.
        P.append('<div class="tracks"><div class="primary">')
        P.extend(sec_html(s,i) for i,s in enumerate(secs) if s.get('placement')!='support')
        P.append('</div><aside class="secondary">');P.extend(sec_html(s,i) for i,s in enumerate(secs) if s.get('placement')=='support');P.append('</aside></div>')
    else:
        P.append('<div class="grid-flow">');P.extend(sec_html(s,i) for i,s in enumerate(secs));P.append('</div>')
    P.append('</div></div></main></body></html>')
    return '\n'.join(P)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',required=True);p.add_argument('--theme',required=True,choices=list(load_themes()));p.add_argument('--palette',choices=list(load_tokens()['palettes']));p.add_argument('--font',choices=list(load_tokens()['fonts']));p.add_argument('--rhythm',choices=list(load_tokens()['rhythms']));p.add_argument('--page',choices=['A4','Letter'],default='A4');p.add_argument('--custom-palette',help='JSON role palette generated by make_palette.py');p.add_argument('--audience-profile',choices=['general','cn-formal','creative','ats'],help='Photograph policy context, not inferred from document language');p.add_argument('--photo-mode',choices=['auto','header-right','three-column','editorial','none'],help='User-approved photo placement override');p.add_argument('--output',required=True);a=p.parse_args()
    data=json.loads(Path(a.input).read_text(encoding='utf-8'));out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
    try: result=make_html(data,load_themes()[a.theme],a.palette,a.font,a.rhythm,a.page,json.loads(Path(a.custom_palette).read_text()) if a.custom_palette else None,a.audience_profile,a.photo_mode)
    except ValueError as e:p.error(str(e))
    out.write_text(result,encoding='utf-8');print(out)
if __name__=='__main__':main()
