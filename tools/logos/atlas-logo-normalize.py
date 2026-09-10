#!/usr/bin/env python3
"""Normalize ATLAS system carousel cards for v0.2.0 Test Build 4.

Contract:
  * 480x360 (4:3) PNG canvas
  * meaningful visible card cropped using alpha >= 48
  * visible card stretched to the complete canvas

The theme leaves the small visual gap around a selected item through carousel
geometry/selection artwork, not through inconsistent transparent PNG margins.
"""
from pathlib import Path
from PIL import Image
import argparse
CANVAS=(480,360); THRESHOLD=48

def normalize(path: Path):
    im=Image.open(path).convert('RGBA'); a=im.getchannel('A')
    mask=a.point(lambda v:255 if v>=THRESHOLD else 0)
    bbox=mask.getbbox() or a.getbbox()
    if not bbox: return
    im.crop(bbox).resize(CANVAS,Image.Resampling.LANCZOS).save(path)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('directory',nargs='?',default='../../_inc/systems/logos-atlas'); a=ap.parse_args()
    base=(Path(__file__).resolve().parent/a.directory).resolve() if not Path(a.directory).is_absolute() else Path(a.directory)
    files=sorted(base.glob('*.png'))
    for p in files: normalize(p)
    print(f'Normalized {len(files)} cards to 480x360 full-canvas geometry.')
if __name__=='__main__': main()
