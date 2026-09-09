#!/usr/bin/env python3
from pathlib import Path
from PIL import Image
import argparse
CANVAS=(480,360); THRESHOLD=48

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('directory',nargs='?',default='../../_inc/systems/logos-atlas'); a=ap.parse_args()
    base=(Path(__file__).resolve().parent/a.directory).resolve() if not Path(a.directory).is_absolute() else Path(a.directory)
    bad=0; files=sorted(base.glob('*.png'))
    for p in files:
        im=Image.open(p).convert('RGBA')
        if im.size!=CANVAS:
            print(f'FAIL {p.name}: canvas {im.size}'); bad+=1; continue
        bbox=im.getchannel('A').point(lambda v:255 if v>=THRESHOLD else 0).getbbox()
        if not bbox:
            print(f'FAIL {p.name}: empty'); bad+=1; continue
        # Full-canvas normalization can lose a pixel at antialiased corners.
        if bbox[0]>2 or bbox[1]>2 or bbox[2]<478 or bbox[3]<358:
            print(f'FAIL {p.name}: meaningful bbox {bbox}'); bad+=1
    print(f'Checked {len(files)} cards; failures: {bad}')
    raise SystemExit(1 if bad else 0)
if __name__=='__main__': main()
