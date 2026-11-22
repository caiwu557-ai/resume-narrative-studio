#!/usr/bin/env python3
import argparse,json
from pathlib import Path
from personalization import recommend
from render_resume import load_themes
p=argparse.ArgumentParser();p.add_argument('--brief',required=True);a=p.parse_args();r=recommend(json.loads(Path(a.brief).read_text()));themes=load_themes()
if any(k not in themes for k in r['recommended']):raise ValueError('Unknown locked layout')
r['candidates']=[{k:themes[i][k] for k in ('id','title','description','recommended_for')} for i in r['recommended']];print(json.dumps(r,ensure_ascii=False,indent=2))
