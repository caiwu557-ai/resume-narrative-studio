#!/usr/bin/env python3
"""Read-only PDF/DOCX diagnostics. No assertion of semantic parity or visual quality."""
import argparse,json,zipfile,re
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
R='{http://schemas.openxmlformats.org/package/2006/relationships}'

def pdf_metrics(path):
    import fitz
    result=[]
    with fitz.open(path) as d:
        for p in d:
            spans=[s for b in p.get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l['spans'] if s['text'].strip()]
            counts=Counter();bold=[]
            for s in spans:
                counts[round(s['size'],2)]+=len(s['text'])
                if s['flags'] & 16: bold.append(s['text'])
            result.append({'page':p.number+1,'size_pt':[p.rect.width,p.rect.height], 'characters':sum(counts.values()),'font_pt_character_counts':dict(sorted(counts.items())), 'dominant_font_pt':counts.most_common(1)[0][0] if counts else None,'bottom_distance_pt':round(p.rect.height-max(s['bbox'][3] for s in spans),2) if spans else None,'bold_spans_font_flag':bold,'links':[l.get('uri') for l in p.get_links() if l.get('uri')],'text':p.get_text(),'out_of_bounds_spans':[s['text'] for s in spans if s['bbox'][0]<-0.5 or s['bbox'][1]<-0.5 or s['bbox'][2]>p.rect.width+0.5 or s['bbox'][3]>p.rect.height+0.5]})
    return result

def docx_metrics(path):
    with zipfile.ZipFile(path) as z:
        names=z.namelist(); parts=[n for n in names if re.fullmatch(r'word/(document|header\d+|footer\d+)\.xml',n)];content=[];links=[];traces=[]
        for part in parts:
            root=ET.fromstring(z.read(part));paragraphs=[]
            for p in root.iter(W+'p'):
                paragraphs.append(''.join(t.text or '' for t in p.iter(W+'t')))
            content.append({'part':part,'paragraphs':paragraphs})
            for tag in ('ins','del','moveFrom','moveTo','commentRangeStart','commentRangeEnd','commentReference'):
                if any(True for _ in root.iter(W+tag)):traces.append(f'{part}:{tag}')
        for part in names:
            if part.startswith('word/') and part.endswith('.rels'):
                for rel in ET.fromstring(z.read(part)).iter(R+'Relationship'):
                    if rel.get('Type','').endswith('/hyperlink'):links.append({'part':part,'target':rel.get('Target'),'mode':rel.get('TargetMode')})
        traces.extend(n for n in names if n.startswith('word/comments') and n.endswith('.xml'))
        return {'parts':content,'hyperlinks':links,'review_trace_indicators':traces,'metadata_present':[n for n in names if n.startswith('docProps/')]}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--pdf',type=Path);p.add_argument('--docx',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if not (a.pdf or a.docx):p.error('provide --pdf and/or --docx')
    r={'status':'diagnostics-only','private':True,'limits':'Extracted text may differ in reading order; bold flags are heuristic; inspect actual pages, paragraph styles, metadata, URI destinations and semantic parity manually.'}
    if a.pdf:r['pdf']=pdf_metrics(a.pdf)
    if a.docx:r['docx']=docx_metrics(a.docx)
    a.output.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':main()
