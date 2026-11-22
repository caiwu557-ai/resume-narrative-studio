#!/usr/bin/env python3
"""Optional Pillow: local image only; explicit share approval required. Re-encode, remove metadata."""
import argparse,base64,io,json
from pathlib import Path
from PIL import Image,ImageOps

def import_asset(path,alt,approved=False):
    if not approved:raise ValueError('User must approve this specific asset for the intended audience.')
    p=Path(path)
    if p.stat().st_size>30_000_000:raise ValueError('Input too large')
    with Image.open(p) as im:
        if im.format not in ('PNG','JPEG','WEBP'):raise ValueError('Only raster PNG/JPEG/WebP')
        if im.width*im.height>30_000_000:raise ValueError('Image too large')
        im=ImageOps.exif_transpose(im).convert('RGB');im.thumbnail((1500,1500));b=io.BytesIO();im.save(b,format='JPEG',quality=90,optimize=True)
    return dict(src='data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode(),alt=alt,approved=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('path');p.add_argument('--alt',required=True);p.add_argument('--approved',action='store_true');p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output);out.write_text(json.dumps(import_asset(a.path,a.alt,a.approved),ensure_ascii=False,indent=2))
