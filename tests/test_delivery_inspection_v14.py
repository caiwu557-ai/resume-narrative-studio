#!/usr/bin/env python3
"""Synthetic DOCX XML and PDF fixtures; no private resume data."""
import sys,tempfile,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from inspect_delivery import docx_metrics,pdf_metrics

class Delivery(unittest.TestCase):
    def test_docx(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'fixture.docx'
            with zipfile.ZipFile(p,'w') as z:
                z.writestr('word/document.xml','''<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p><w:r><w:t>Title </w:t></w:r><w:hyperlink><w:r><w:t>Project</w:t></w:r></w:hyperlink><w:ins><w:r><w:t> draft</w:t></w:r></w:ins></w:p></w:body></w:document>''')
                z.writestr('word/_rels/document.xml.rels','''<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" Target="https://example.org" TargetMode="External"/></Relationships>''')
            r=docx_metrics(p);self.assertEqual(r['parts'][0]['paragraphs'],['Title Project draft']);self.assertEqual(r['hyperlinks'][0]['target'],'https://example.org');self.assertIn('word/document.xml:ins',r['review_trace_indicators'])
    def test_pdf(self):
        try:import fitz
        except ImportError:self.skipTest('optional PyMuPDF missing')
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'fixture.pdf';doc=fitz.open();page=doc.new_page();page.insert_text((30,40),'Research role',fontsize=10.5,fontname='hebo');page.insert_text((30,60),'Details',fontsize=8.5);page.insert_link({'kind':fitz.LINK_URI,'from':fitz.Rect(30,30,130,44),'uri':'https://example.org'});doc.save(p);doc.close();r=pdf_metrics(p)[0];self.assertEqual(r['font_pt_character_counts'][8.5],7);self.assertIn('Research role',r['bold_spans_font_flag']);self.assertEqual(r['links'],['https://example.org']);self.assertGreater(r['bottom_distance_pt'],0);self.assertFalse(r['out_of_bounds_spans'])
if __name__=='__main__':unittest.main()
