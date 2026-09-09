#!/usr/bin/env python3
"""Calculate ATLAS system collection progress from ES-DE gamelist.xml files.

A game is "played" when <playcount> is greater than zero. Entries with
<nogamecount>true</nogamecount> are excluded. ES-DE's theme API does not expose an
aggregate played-game count, so this utility writes the calculated percentage into
ATLAS per-system theme variables. Restart/reload ES-DE after applying.
"""
from pathlib import Path
import argparse,re,xml.etree.ElementTree as ET
MAX_FILL=0.286

def calc(path):
    root=ET.parse(path).getroot(); total=played=0
    for game in root.findall('game'):
        if (game.findtext('nogamecount') or '').strip().lower()=='true': continue
        total+=1
        try: count=int((game.findtext('playcount') or '0').strip() or '0')
        except ValueError: count=0
        if count>0: played+=1
    pct=(100.0*played/total) if total else 0.0
    return played,total,pct

def update(path,pct):
    txt=path.read_text()
    values={
        'systemCollectionProgress':f'{round(pct)}%',
        'systemCollectionProgressFill':f'{max(0.001,MAX_FILL*pct/100):.6f}',
        'systemCollectionProgressOpacity':'1' if pct>0 else '0',
    }
    for tag,val in values.items():
        if re.search(fr'<{tag}>.*?</{tag}>',txt,re.S):
            txt=re.sub(fr'<{tag}>.*?</{tag}>',f'<{tag}>{val}</{tag}>',txt,count=1,flags=re.S)
        else:
            txt=txt.replace('</variables>',f'        <{tag}>{val}</{tag}>\n    </variables>',1)
    path.write_text(txt)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--gamelists-root',type=Path,required=True)
    ap.add_argument('--theme-root',type=Path,required=True)
    ap.add_argument('--apply',action='store_true')
    a=ap.parse_args(); meta=a.theme_root/'_inc/systems/metadata-global'; matched=0
    for d in sorted(a.gamelists_root.iterdir()):
        gl=d/'gamelist.xml'; target=meta/f'{d.name}.xml'
        if not gl.is_file() or not target.is_file(): continue
        played,total,pct=calc(gl); matched+=1
        print(f'{d.name:24} {played:4}/{total:<4} {pct:6.1f}%')
        if a.apply: update(target,pct)
    print(f'\nSystems matched: {matched}; mode: {"APPLY" if a.apply else "DRY RUN"}')
if __name__=='__main__': main()
