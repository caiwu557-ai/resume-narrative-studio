#!/usr/bin/env python3
import argparse,json
from pathlib import Path
from personalization import custom_palette,validated_palette,contrast,PAIRS
p=argparse.ArgumentParser();p.add_argument('--seed',required=True);p.add_argument('--secondary');p.add_argument('--paper',default='#FFFFFF');p.add_argument('--output',required=True);a=p.parse_args();r=validated_palette(custom_palette(a.seed,a.secondary,a.paper));Path(a.output).write_text(json.dumps(r,ensure_ascii=False,indent=2));print(json.dumps({'palette':r,'contrasts':{f'{x}/{y}':round(contrast(r[x],r[y]),2) for x,y in PAIRS}},ensure_ascii=False,indent=2))
