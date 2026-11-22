"""Automated photo placement semantics + Chromium smoke checks. No real photographs."""
import copy, json, sys, os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
sys.path.insert(0,str(ROOT/'tests'))
from personalization import select_photo_mode,photo_recommendation, PHOTO_SLOTS, THREE_COL_ALLOWED
from render_resume import make_html,load_themes
from test_personalization import example

def core():
    themes=load_themes(); cfg=json.loads((ROOT/'templates/photo_policy.json').read_text(encoding='utf-8'))
    assert set(cfg['templates'])==set(themes)
    d=example(); results=[]
    for name,theme in themes.items():
        l=theme['layout'];formal=make_html(d,theme,audience_profile='cn-formal')
        if theme['ats_candidate']:
            assert 'class="portrait"' not in formal
        else:
            assert 'photo-header-right' in formal and formal.count('class="portrait"')==1
            assert '<img class="portrait"' in formal
            # Creative profile explicitly preserves v1.2 editorial placement.
            art=make_html(d,theme,audience_profile='creative')
            assert 'photo-'+PHOTO_SLOTS[l] in art
            assert 'photo-header-right' not in art.split('<main',1)[1].split('>',1)[0]
            assert 'class="portrait"' not in make_html(dict(d,_continuation=True),theme,audience_profile='cn-formal')
            if l in THREE_COL_ALLOWED:
                tri=make_html(d,theme,audience_profile='cn-formal',photo_mode='three-column')
                assert 'photo-three-column' in tri and tri.count('class="portrait"')==1
            else:
                try:
                    make_html(d,theme,audience_profile='cn-formal',photo_mode='three-column')
                    raise AssertionError('unapproved 3-col '+name)
                except ValueError:pass
            assert 'class="portrait"' not in make_html(d,theme,audience_profile='cn-formal',photo_mode='none')
            assert 'class="portrait"' not in make_html(d,theme,audience_profile='ats')
            absent=copy.deepcopy(d);absent.pop('photo')
            assert 'class="portrait"' not in make_html(absent,theme,audience_profile='cn-formal')
        results.append({'template':name,'cn_formal':cfg['templates'][name]['cn_formal_recommendation']})
    assert photo_recommendation({'channel':'ats'})['mode']=='none'
    assert photo_recommendation({'channel':'direct','audience_profile':'cn-formal'})['mode']=='header-right'
    assert photo_recommendation({'channel':'direct','audience_profile':'creative'})['mode']=='editorial'
    return results


def browser(out):
    import fitz
    from playwright.sync_api import sync_playwright
    out.mkdir(exist_ok=True,parents=True)
    data=example(); data['audience_profile']='cn-formal'
    rows=[]
    with sync_playwright() as pw:
        b=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
        for name,t in load_themes().items():
            if t['ats_candidate']:continue
            for mode in (['header-right','three-column'] if t['layout'] in THREE_COL_ALLOWED else ['header-right']):
                page=b.new_page(viewport={'width':1050,'height':1350},device_scale_factor=1)
                h=make_html(data,t,audience_profile='cn-formal',photo_mode=mode)
                page.set_content(h,wait_until='load');page.evaluate('document.fonts.ready')
                loc=page.locator('.portrait'); header=page.locator('.header');identity=page.locator('.identity'); info=page.locator('.info'); name_loc=page.locator('h1')
                pos=page.evaluate('''() => {const rect=s=>{const n=document.querySelector(s);if(!n)return null;const r=n.getBoundingClientRect();return {x:r.x,y:r.y,right:r.right,bottom:r.bottom,width:r.width,height:r.height}};return {photo:rect('.portrait'),header:rect('.header'),identity:rect('.identity'),info:rect('.info'),name:rect('h1'),overflow:document.documentElement.scrollWidth>innerWidth+1,loaded:document.querySelector('.portrait').naturalWidth>0}}''')
                p,hdr=pos['photo'],pos['header'];assert pos['loaded'],(name,mode,'image fail')
                assert not pos['overflow'],(name,mode,'desktop overflow')
                assert pos['name']['right'] < p['x']-3,(name,mode,'name-photo overlap',pos)
                if mode=='header-right':
                    assert abs(p['right']-hdr['right'])<25,(name,'photo not rightmost',pos)
                else: assert pos['info']['right']<p['x']+3,(name,'3 col info/photo overlap',pos)
                page.screenshot(path=str(out/(name+'-'+mode+'.png')),full_page=False)
                page.set_viewport_size({'width':390,'height':844})
                mobile=page.evaluate('document.documentElement.scrollWidth>innerWidth+1')
                assert not mobile,(name,mode,'mobile overflow')
                page.set_viewport_size({'width':1050,'height':1350});page.emulate_media(media='print')
                raw=page.pdf(format='A4',print_background=True,prefer_css_page_size=True)
                pdf=fitz.open(stream=raw,filetype='pdf')
                txt=''.join(x.get_text() for x in pdf)
                assert '林沐' in txt and '未来方向' in txt,(name,'lost text',len(pdf))
                assert len(pdf)<=2,(name,'strange pages',len(pdf))
                rows.append({'layout':name,'mode':mode,'pages':len(pdf),'photo_right_error_px':round(p['right']-hdr['right'],2),'desktop_no_overflow':not pos['overflow'],'mobile_no_overflow':not mobile})
                page.close()
        b.close()
    (out/'results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    return rows

if __name__=='__main__':
    print('core',len(core()))
    if '--browser' in sys.argv: print('browser',len(browser(ROOT/'tests'/'output'/'photo-policy-v13')))
