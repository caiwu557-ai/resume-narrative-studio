"""Deterministic, offline helpers. Agent/user must approve semantic choices; not a hiring predictor."""
from __future__ import annotations
import base64, json, re, io, copy
from pathlib import Path
HEX=re.compile(r'#[0-9a-fA-F]{6}$')
PAIRS=[('ink','paper'),('muted','paper'),('accent','paper'),('ink','panel'),('muted','panel'),('accent','panel'),('band_ink','band'),('highlight_ink','highlight')]
def rgb(h):
    if not isinstance(h,str) or not HEX.fullmatch(h):raise ValueError('Expected #RRGGBB')
    return tuple(int(h[i:i+2],16) for i in (1,3,5))
def hexcolor(c):return '#'+''.join(f'{round(x):02X}' for x in c)
def mix(a,b,t):return hexcolor(tuple(x+(y-x)*t for x,y in zip(rgb(a),rgb(b))))
def lum(h):
    c=[x/255 for x in rgb(h)];return sum(w*(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4) for w,v in zip((.2126,.7152,.0722),c))
def contrast(a,b):
    a,b=sorted((lum(a),lum(b)));return (b+.05)/(a+.05)
def readable(c,bgs):
    # Preserve hue as far as simple interpolation permits; never pretend user seed is legible text.
    for end in ('#000000','#FFFFFF'):
        for i in range(101):
            x=mix(c,end,i/100)
            if all(contrast(x,b)>=4.6 for b in bgs):return x
    raise ValueError('No common legible text color on requested surfaces')
def custom_palette(seed,secondary=None,paper='#FFFFFF'):
    rgb(seed);rgb(paper);secondary=secondary or seed;rgb(secondary)
    if lum(paper)<.75:raise ValueError('Paper must be light for this print-first palette generator; use a preset for dark bands.')
    panel=mix(paper,seed,.08);highlight=mix(paper,secondary,.28);band=mix(seed,'#000000',.58)
    return {'title':f'定制 {seed.upper()}','paper':paper.upper(),'ink':readable('#20262B',[paper,panel]),'muted':readable('#58636B',[paper,panel]),'accent':readable(seed,[paper,panel]),'panel':panel,'band':band,'band_ink':readable('#FFFFFF',[band]),'highlight':highlight,'highlight_ink':readable('#20262B',[highlight]),'line':mix(paper,seed,.24)}
def validated_palette(p):
    if not isinstance(p,dict) or set(p)!=set(['title','paper','ink','muted','accent','panel','band','band_ink','highlight','highlight_ink','line']):raise ValueError('Palette must provide exact role tokens')
    if not isinstance(p['title'],str):raise ValueError('Invalid palette title')
    for k,v in p.items():
        if k!='title':rgb(v)
    for a,b in PAIRS:
        if contrast(p[a],p[b])<4.5:raise ValueError(f'Contrast below 4.5:1: {a}/{b}')
    return dict(p)
# Legacy layout slots are retained for creative/editorial mode and existing v1.2 inputs.
PHOTO_SLOTS={'plain':'none','formal':'identity-right','ledger':'identity-right','ivory':'center-top','book':'identity-top','studio':'identity-right','product':'identity-right','rail':'rail-top','index':'identity-right','poster':'identity-right','pop':'identity-top','tracks':'identity-right'}
THEME_TO_LAYOUT={
    'ats-clean':'plain','formal-split':'formal','research-ledger':'ledger',
    'ivory-classic':'ivory','book-editorial':'book','studio-grid':'studio',
    'product-feature':'product','portfolio-rail':'rail','experience-index':'index',
    'bold-poster':'poster','pop-blocks':'pop','two-track':'tracks'
}
THREE_COL_ALLOWED={'formal','studio','product','tracks'}
PHOTO_MODES={'auto','header-right','three-column','editorial','none'}

def select_photo_mode(layout, profile='general', requested='auto', *, is_ats=False):
    """Context-dependent photo position; CSS semantics, not identity inference.

    Never infer profile from language, gender, photo or name. The Agent must obtain
    the application context from the user/brief, and must not generate a portrait.
    """
    if requested not in PHOTO_MODES:
        raise ValueError('Unsupported photo mode: '+str(requested))
    if profile not in ('general','cn-formal','creative','ats'):
        raise ValueError('Unsupported audience profile: '+str(profile))
    if is_ats or profile=='ats' or layout=='plain' or requested=='none':return 'none'
    if requested=='three-column':
        if layout not in THREE_COL_ALLOWED:
            raise ValueError('Three-column photo layout is not approved for '+layout)
        return 'three-column'
    if requested=='header-right':return 'header-right'
    if requested=='editorial':return PHOTO_SLOTS[layout]
    return 'header-right' if profile=='cn-formal' else PHOTO_SLOTS[layout]

def photo_recommendation(brief):
    """Explain recommendation without treating style preference as an obligation."""
    profile=brief.get('audience_profile')
    if brief.get('channel')=='ats':
        return {'mode':'none','reason':'ATS自动解析，不插入头像或图形。','ask':False}
    if profile=='cn-formal':
        return {'mode':'header-right','reason':'中文正式简历如需照片，默认身份区右上独立式；现代三栏为可选方案。','ask':False}
    if profile=='creative':
        return {'mode':'editorial','reason':'作品集允许与身份区连贯的居中或侧栏人像，正式申请另做右上版。','ask':False}
    return {'mode':'editorial','reason':'先确认具体投递地区及渠道，不依据中文或姓名推断默认照片规范。','ask':bool(brief.get('photo_requested') and not profile)}

# Only locally imported, re-encoded raster assets. No remote image fetching or raw SVG injection.
def verified_image(obj):
    if not isinstance(obj,dict) or obj.get('approved') is not True:return None
    s=obj.get('src','');m=re.fullmatch(r'data:image/(png|jpeg|webp);base64,([A-Za-z0-9+/=]+)',s) if isinstance(s,str) and len(s)<4_000_000 else None
    if not m:raise ValueError('Approved asset requires a bounded local raster data URI; use import_asset.py')
    raw=base64.b64decode(m.group(2),validate=True);kind=m.group(1)
    if not ((kind=='png' and raw.startswith(b'\x89PNG\r\n\x1a\n')) or (kind=='jpeg' and raw.startswith(b'\xff\xd8\xff')) or (kind=='webp' and raw[:4]==b'RIFF' and raw[8:12]==b'WEBP')):raise ValueError('Image signature mismatch')
    return s

def normalize_data(data):
    d=copy.deepcopy(data)
    if not isinstance(d.get('sections'),list):raise ValueError('sections must be a list')
    # Empty sections do not get fake copy. Preserve real data and original source indexes on optional sections.
    secs=[]
    for s in d['sections']:
        e=[x for x in s.get('entries',[]) if any(x.get(k) for k in ('heading','meta','detail','bullets','link','links','media'))]
        if e: s['entries']=e;secs.append(s)
    d['sections']=secs
    return d

def recommend(brief):
    """Structured fields are interpreted by Agent from conversation; no inference from demographics."""
    channel=brief.get('channel','unknown');tone=brief.get('tone','formal');focus=brief.get('focus','general');volume=brief.get('volume','medium');photo=brief.get('photo','undecided');evidence=brief.get('visual_evidence','none');locked=brief.get('layout_lock')
    if channel=='ats':return {'recommended':['ats-clean'],'reason':'自动投递优先自然阅读顺序；图像和装饰留给单独真人版。','photo':'omit','media':'appendix-if-requested','needs_confirmation':bool(locked and locked!='ats-clean')}
    cn_photo=brief.get('audience_profile')=='cn-formal' and brief.get('photo_requested') is True
    photo_policy=photo_recommendation(brief)
    if locked:return {'recommended':[locked],'reason':'继承用户已批准布局，不因新资料或颜色喜好擅自换版。','photo':photo,'photo_placement':photo_policy['mode'],'photo_style_warning':locked in ('ivory-classic','pop-blocks') and cn_photo,'media':'inline-or-appendix','needs_confirmation':False}
    if tone in ('bold','young','playful'):
        ids=['pop-blocks','bold-poster','product-feature'] if volume!='long' else ['bold-poster','book-editorial','formal-split']
    elif focus in ('academic','research','clinical'):
        ids=['research-ledger','formal-split','ivory-classic'] if volume!='long' else ['formal-split','experience-index','book-editorial']
    elif focus in ('design','product','creative') or evidence=='strong':
        ids=['product-feature','studio-grid','portfolio-rail'] if volume!='long' else ['product-feature','formal-split','experience-index']
    elif volume=='long':ids=['experience-index','formal-split','research-ledger']
    elif tone=='editorial':ids=['book-editorial','ivory-classic','studio-grid']
    else:ids=['formal-split','experience-index','ivory-classic']
    if cn_photo and focus in ('academic','research','clinical'):
        ids=['research-ledger','experience-index','formal-split'] if volume!='long' else ['experience-index','research-ledger','formal-split']
    if volume=='sparse':ids=[x for x in ids if x not in ('studio-grid','portfolio-rail','two-track')];ids += [x for x in ['ivory-classic','formal-split','book-editorial'] if x not in ids];ids=ids[:3]
    if cn_photo:ids=[x for x in ids if x not in ('ivory-classic','pop-blocks')];ids += [x for x in ['research-ledger','experience-index','formal-split'] if x not in ids];ids=ids[:3]
    return {'recommended':ids,'reason':f'按渠道、受众语气、主题和内容量筛选；{("长履历优先线性结构" if volume=="long" else "先比较不同结构，视觉偏好单独匹配")}。','photo':photo,'photo_placement':photo_policy['mode'],'media':'select evidence then attach to related entry','needs_confirmation':channel=='unknown'}
