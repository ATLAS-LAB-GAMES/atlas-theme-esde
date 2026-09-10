#!/usr/bin/env python3
"""ATLAS ES-DE 3D-box emblem manager.

This is an external companion utility. ES-DE continues to display normal 3dbox
media; this tool safely composes ATLAS emblems into those files while retaining
pristine backups and a hash-checked manifest.

Typical use:
  python3 atlas-emblems.py --media-root /path/to/ES-DE/downloaded_media --dry-run
  python3 atlas-emblems.py --media-root /path/to/ES-DE/downloaded_media --sync
  python3 atlas-emblems.py --media-root /path/to/ES-DE/downloaded_media --restore-all
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import unicodedata
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover - user-facing dependency path
    raise SystemExit(
        "Pillow is required. Install it with your OS package manager or 'python3 -m pip install Pillow'."
    ) from exc

VERSION = "0.2.0-build4"
SUPPORTED_EMBLEMS = {
    "hack", "mod", "fangame",
    "disc1", "disc2", "disc3", "disc4", "disc5", "disc6",
}
SUPPORTED_POSITIONS = {"top-right", "top-left", "bottom-right", "bottom-left"}
MEDIA_FOLDER_ALIASES = {
    "3dbox": ("3dboxes", "3dbox"),
    "3dboxes": ("3dboxes", "3dbox"),
    "cover": ("covers", "cover"),
    "covers": ("covers", "cover"),
    "fanart": ("fanart",),
    "screenshot": ("screenshots", "screenshot"),
    "screenshots": ("screenshots", "screenshot"),
}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).casefold()
    return "".join(ch for ch in text if ch.isalnum())


def media_folder_candidates(image_type: str) -> Tuple[str, ...]:
    key = image_type.strip().casefold()
    return MEDIA_FOLDER_ALIASES.get(key, (key,))


def get_media_dir(media_root: Path, system: str, image_type: str) -> Path:
    sysdir = media_root / system
    if not sysdir.is_dir():
        raise FileNotFoundError(f"system media directory not found: {sysdir}")
    for folder in media_folder_candidates(image_type):
        candidate = sysdir / folder
        if candidate.is_dir():
            return candidate
    expected = ", ".join(str(sysdir / f) for f in media_folder_candidates(image_type))
    raise FileNotFoundError(f"media folder not found; tried: {expected}")


def image_files(directory: Path) -> List[Path]:
    return sorted(p for p in directory.iterdir() if p.is_file() and p.suffix.casefold() in IMAGE_EXTS)



def gamelist_games(path: Path):
    """Return game nodes from standard or ES-DE multi-root gamelist fragments."""
    text=path.read_text(encoding="utf-8-sig", errors="replace")
    text=re.sub(r"^\s*<\?xml[^>]*\?>", "", text, count=1, flags=re.I)
    try:
        wrapped=ET.fromstring("<atlasRoot>" + text + "</atlasRoot>")
    except ET.ParseError as e:
        raise RuntimeError(f"could not parse {path}: {e}") from e
    return wrapped.findall("./gameList/game") or wrapped.findall("./game")

def gamelist_rom_stem(gamelist_root: Path | None, system: str, game: str) -> str | None:
    if not gamelist_root:
        return None
    candidates = [gamelist_root / system / "gamelist.xml", gamelist_root / system / "gamelist.xml.xml"]
    gl = next((p for p in candidates if p.is_file()), None)
    if gl is None:
        return None
    exact=[]; normalized=[]
    for node in gamelist_games(gl):
        name=(node.findtext("name") or "").strip()
        path=(node.findtext("path") or "").strip()
        if not name or not path:
            continue
        stem=Path(path).stem
        if name.casefold()==game.casefold(): exact.append(stem)
        if norm(name)==norm(game): normalized.append(stem)
    matches=exact or normalized
    matches=list(dict.fromkeys(matches))
    if len(matches)==1:
        return matches[0]
    if len(matches)>1:
        raise RuntimeError(f"gamelist name is ambiguous for {system!r}/{game!r}: {matches}")
    return None


def resolve_media(media_root: Path, system: str, game: str, image_type: str,
                  gamelist_root: Path | None = None) -> Path:
    directory=get_media_dir(media_root, system, image_type)
    files=image_files(directory)
    exact=[p for p in files if p.stem.casefold()==game.casefold()]
    if len(exact)==1:
        return exact[0]
    if len(exact)>1:
        raise RuntimeError(f"multiple exact media matches for {system!r}/{game!r}: {[p.name for p in exact]}")

    n=norm(game)
    normalized=[p for p in files if norm(p.stem)==n]
    if len(normalized)==1:
        return normalized[0]
    if len(normalized)>1:
        raise RuntimeError(f"multiple normalized media matches for {system!r}/{game!r}: {[p.name for p in normalized]}")

    romstem=gamelist_rom_stem(gamelist_root, system, game)
    if romstem:
        exact_rom=[p for p in files if p.stem.casefold()==romstem.casefold()]
        if len(exact_rom)==1:
            return exact_rom[0]
        norm_rom=[p for p in files if norm(p.stem)==norm(romstem)]
        if len(norm_rom)==1:
            return norm_rom[0]

    raise FileNotFoundError(f"no {image_type} media found for {system!r}/{game!r} in {directory}")


def read_csv(path: Path) -> List[dict]:
    if not path.is_file():
        raise FileNotFoundError(f"CSV not found: {path}")
    rows=[]
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader=csv.DictReader(f)
        required={"SYSTEM","GAME","IMAGE_TYPE","EMBLEM_TYPE","ACTION"}
        fields={x.strip().upper() for x in (reader.fieldnames or [])}
        missing=required-fields
        if missing:
            raise ValueError(f"CSV missing required column(s): {', '.join(sorted(missing))}")
        for lineno,row in enumerate(reader,start=2):
            r={str(k).strip().upper(): (v or "").strip() for k,v in row.items()}
            if not any(r.values()):
                continue
            emblem=r["EMBLEM_TYPE"].casefold().replace(" ","")
            action=r["ACTION"].casefold()
            position=(r.get("POSITION") or "top-right").casefold()
            if emblem not in SUPPORTED_EMBLEMS:
                raise ValueError(f"line {lineno}: unsupported EMBLEM_TYPE {r['EMBLEM_TYPE']!r}")
            if action not in {"add","remove"}:
                raise ValueError(f"line {lineno}: ACTION must be add or remove")
            if position not in SUPPORTED_POSITIONS:
                raise ValueError(f"line {lineno}: unsupported POSITION {position!r}")
            if not r["SYSTEM"] or not r["GAME"] or not r["IMAGE_TYPE"]:
                raise ValueError(f"line {lineno}: SYSTEM, GAME and IMAGE_TYPE are required")
            rows.append({
                "system":r["SYSTEM"], "game":r["GAME"], "image_type":r["IMAGE_TYPE"],
                "emblem":emblem, "action":action, "position":position, "line":lineno,
            })
    return rows


def load_manifest(state_root: Path) -> dict:
    path=state_root/"manifest.json"
    if not path.exists():
        return {"format":1,"tool_version":VERSION,"records":{}}
    data=json.loads(path.read_text(encoding="utf-8"))
    if data.get("format")!=1 or not isinstance(data.get("records"),dict):
        raise RuntimeError(f"unsupported/corrupt manifest: {path}")
    return data


def save_manifest(state_root: Path, manifest: dict) -> None:
    state_root.mkdir(parents=True,exist_ok=True)
    manifest["tool_version"]=VERSION
    tmp=state_root/"manifest.json.tmp"
    tmp.write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    os.replace(tmp,state_root/"manifest.json")


def backup_path(state_root: Path, relative: str) -> Path:
    return state_root/"backups"/relative


def save_image_atomic(image: Image.Image, destination: Path) -> None:
    destination.parent.mkdir(parents=True,exist_ok=True)
    suffix=destination.suffix.casefold()
    fmt={".png":"PNG",".jpg":"JPEG",".jpeg":"JPEG",".webp":"WEBP"}.get(suffix)
    if not fmt:
        raise RuntimeError(f"unsupported output format: {destination}")
    fd,tmpname=tempfile.mkstemp(prefix=destination.name+".",suffix=destination.suffix,dir=destination.parent)
    os.close(fd)
    tmp=Path(tmpname)
    try:
        out=image
        kwargs={}
        if fmt=="JPEG":
            out=image.convert("RGB"); kwargs={"quality":95,"subsampling":0}
        elif fmt=="WEBP":
            kwargs={"lossless":True,"quality":100}
        elif fmt=="PNG":
            kwargs={"optimize":True}
        out.save(tmp,format=fmt,**kwargs)
        os.replace(tmp,destination)
    finally:
        if tmp.exists(): tmp.unlink()

def render_from_backup(target: Path, backup: Path, emblems: List[dict], emblem_root: Path) -> None:
    base = Image.open(backup).convert("RGBA")
    W, H = base.size

    margin = max(4, round(W * 0.024))
    gap = max(3, round(W * 0.012))

    # Keep labels readable but small enough not to dominate box art.
    target_w = max(80, round(W * 0.31))

    # ES-DE 3D box images commonly contain transparent/unused headroom
    # around the rendered case. 3D-box artwork therefore starts the
    # emblem stack lower than flat cover artwork.
    is_3dbox = target.parent.name.casefold() in {"3dbox", "3dboxes"}

    grouped = defaultdict(list)

    for e in emblems:
        grouped[e["position"]].append(e)

    for position, items in grouped.items():
        offset = 0
        stack_inset = None

        for e in items:
            ep = emblem_root / f"{e['emblem']}.png"

            if not ep.is_file():
                raise FileNotFoundError(f"emblem asset not found: {ep}")

            badge = Image.open(ep).convert("RGBA")

            scale = target_w / badge.width
            badge = badge.resize(
                (
                    target_w,
                    max(1, round(badge.height * scale)),
                ),
                Image.Resampling.LANCZOS,
            )

            # Calculate the initial stack inset once.
            #
            # Flat artwork:
            #   Starts at the normal margin.
            #
            # Standard/wider 3D-box artwork:
            #   Starts 1.5 emblem heights lower.
            #
            # Narrow/tall 3D-box artwork:
            #   Starts 2.0 emblem heights lower because these renders tend to
            #   contain substantially more transparent headroom above the case.
            if stack_inset is None:
                if is_3dbox:
                    aspect_ratio = W / H

                    if aspect_ratio <= 0.60:
                        stack_inset = round(badge.height * 2.0) + gap
                    else:
                        stack_inset = round(badge.height * 1.5) + gap
                else:
                    stack_inset = 0

            slot_offset = stack_inset + offset

            if position.startswith("top"):
                y = margin + slot_offset
            else:
                y = H - margin - badge.height - slot_offset

            if position.endswith("right"):
                x = W - margin - badge.width
            else:
                x = margin

            base.alpha_composite(badge, (x, y))

            # Normal spacing for every subsequent emblem.
            offset += badge.height + gap

    save_image_atomic(base, target)

def relative_key(media_root: Path, target: Path) -> str:
    try:
        return target.resolve().relative_to(media_root.resolve()).as_posix()
    except ValueError:
        raise RuntimeError(f"resolved media is outside media root: {target}")


def ensure_backup(media_root: Path, state_root: Path, target: Path, manifest: dict,
                  refresh_backup: bool=False) -> tuple[str,dict]:
    key=relative_key(media_root,target)
    records=manifest["records"]
    rec=records.get(key)
    if rec:
        bp=state_root/rec["backup_rel"]
        if not bp.is_file():
            raise RuntimeError(f"backup missing for managed image {key}: {bp}")
        current=sha256(target)
        allowed={rec.get("generated_sha256"),rec.get("original_sha256")}
        if current not in allowed:
            if not refresh_backup:
                raise RuntimeError(
                    f"media changed outside ATLAS since last run: {target}\n"
                    "Refusing to overwrite it. Re-scrape/inspect as needed, then rerun with --refresh-backup to accept it as the new pristine source."
                )
            shutil.copy2(target,bp)
            rec["original_sha256"]=sha256(bp)
            rec["generated_sha256"]=None
        return key,rec

    rel=Path(key)
    bp=state_root/"backups"/rel
    bp.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(target,bp)
    rec={
        "backup_rel":bp.relative_to(state_root).as_posix(),
        "original_sha256":sha256(bp),
        "generated_sha256":None,
        "emblems":[],
    }
    records[key]=rec
    return key,rec


def verify_managed_target(media_root: Path, key: str, rec: dict) -> str:
    """Return current hash after confirming a managed target was not changed externally."""
    target=media_root/key
    if not target.is_file():
        raise RuntimeError(f"managed media is missing: {target}")
    current=sha256(target)
    allowed={rec.get("generated_sha256"),rec.get("original_sha256")}
    allowed.discard(None)
    if current not in allowed:
        raise RuntimeError(
            f"media changed outside ATLAS since last run: {target}\n"
            "Refusing to restore/overwrite it. Inspect or re-scrape as needed before continuing."
        )
    return current


def restore_record(media_root: Path, state_root: Path, key: str, rec: dict, dry_run: bool=False) -> None:
    target=media_root/key
    bp=state_root/rec["backup_rel"]
    if not bp.is_file():
        raise RuntimeError(f"cannot restore {key}: backup missing at {bp}")
    verify_managed_target(media_root,key,rec)
    if not dry_run:
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(bp,target)


def canonical_emblems(items: Iterable[dict]) -> List[dict]:
    seen=set(); out=[]
    for e in items:
        tup=(e["emblem"],e["position"])
        if tup in seen: continue
        seen.add(tup); out.append({"emblem":e["emblem"],"position":e["position"]})
    return out


def execute(args) -> int:
    media_root=args.media_root.resolve()
    csv_path=args.csv.resolve()
    emblem_root=args.emblem_root.resolve()
    state_root=(args.state_root.resolve() if args.state_root else (media_root/".atlas-emblems"))
    gamelist_root=args.gamelist_root.resolve() if args.gamelist_root else None
    manifest=load_manifest(state_root)

    if args.restore_all:
        print(f"Restoring {len(manifest['records'])} managed image(s)...")
        for key,rec in list(manifest["records"].items()):
            print(f"RESTORE {key}")
            restore_record(media_root,state_root,key,rec,dry_run=False)
        manifest["records"]={}
        save_manifest(state_root,manifest)
        print("Done. All ATLAS-managed images were restored.")
        return 0

    rows=read_csv(csv_path)
    resolved=[]
    errors=[]
    for row in rows:
        try:
            target=resolve_media(media_root,row["system"],row["game"],row["image_type"],gamelist_root)
            key=relative_key(media_root,target)
            resolved.append((row,target,key))
        except Exception as e:
            errors.append(f"line {row['line']}: {e}")
    if errors:
        print("CSV resolution failed:",file=sys.stderr)
        for e in errors: print(f"  - {e}",file=sys.stderr)
        return 2

    # Build desired state.
    desired: Dict[str,List[dict]]={}
    if args.apply:
        # Start from current managed state and make only explicit changes.
        for key,rec in manifest["records"].items():
            desired[key]=list(rec.get("emblems",[]))
    # sync/dry-run start empty: ADD rows are the source of truth.
    target_by_key={key:target for _,target,key in resolved}
    for row,target,key in resolved:
        cur=desired.setdefault(key,[])
        marker={"emblem":row["emblem"],"position":row["position"]}
        if row["action"]=="add":
            cur.append(marker)
            desired[key]=canonical_emblems(cur)
        else:
            desired[key]=[e for e in cur if e.get("emblem")!=row["emblem"]]

    all_keys=set(manifest["records"]) | set(desired)
    operations=[]
    for key in sorted(all_keys):
        wanted=canonical_emblems(desired.get(key,[]))
        current=canonical_emblems(manifest["records"].get(key,{}).get("emblems",[]))
        if wanted==current:
            continue
        if not wanted:
            operations.append(("restore",key,wanted))
        else:
            operations.append(("render",key,wanted))

    mode="DRY-RUN" if args.dry_run else ("APPLY" if args.apply else "SYNC")
    print(f"ATLAS Emblems {VERSION} — {mode}")
    print(f"Media root: {media_root}")
    print(f"CSV:        {csv_path}")
    print(f"State:      {state_root}")
    if not operations:
        print("No changes required.")
        return 0

    for op,key,wanted in operations:
        labels=", ".join(f"{e['emblem']}@{e['position']}" for e in wanted) or "original"
        print(f"{op.upper():7s} {key} -> {labels}")
    if args.dry_run:
        print(f"\nDry run complete: {len(operations)} operation(s), no files changed.")
        return 0

    # Perform operations. If any error occurs, manifest is saved only after all requested writes succeed.
    for op,key,wanted in operations:
        if op=="restore":
            rec=manifest["records"].get(key)
            if rec:
                restore_record(media_root,state_root,key,rec)
                manifest["records"].pop(key,None)
            continue

        target=target_by_key.get(key) or (media_root/key)
        if not target.is_file():
            raise RuntimeError(f"target disappeared before render: {target}")
        key2,rec=ensure_backup(media_root,state_root,target,manifest,args.refresh_backup)
        bp=state_root/rec["backup_rel"]
        render_from_backup(target,bp,wanted,emblem_root)
        rec["emblems"]=wanted
        rec["generated_sha256"]=sha256(target)
        manifest["records"][key2]=rec

    save_manifest(state_root,manifest)
    print(f"\nComplete: {len(operations)} operation(s).")
    return 0


def parser() -> argparse.ArgumentParser:
    here=Path(__file__).resolve().parent
    ap=argparse.ArgumentParser(description="Safely add/remove ATLAS emblems on ES-DE scraped artwork.")
    ap.add_argument("--media-root", type=Path, required=True,
                    help="ES-DE downloaded_media directory")
    ap.add_argument("--csv", type=Path, default=here/"atlas-emblems.csv",
                    help="mapping CSV (default: atlas-emblems.csv beside this script)")
    ap.add_argument("--emblem-root", type=Path, default=here/"assets",
                    help="directory containing emblem PNG files")
    ap.add_argument("--state-root", type=Path,
                    help="backup/manifest directory (default: MEDIA_ROOT/.atlas-emblems)")
    ap.add_argument("--gamelist-root", "--gamelists-root", dest="gamelist_root", type=Path,
                    help="optional ES-DE gamelists directory containing SYSTEM/gamelist.xml for display-name resolution")
    group=ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true", help="show a sync plan without changing files")
    group.add_argument("--sync", action="store_true", help="make ADD rows the authoritative desired state")
    group.add_argument("--apply", action="store_true", help="apply only explicit ADD/REMOVE rows")
    group.add_argument("--restore-all", action="store_true", help="restore every ATLAS-managed image")
    ap.add_argument("--refresh-backup", action="store_true",
                    help="accept externally changed media as the new pristine original before rendering")
    return ap


def main() -> int:
    ap=parser(); args=ap.parse_args()
    try:
        return execute(args)
    except (OSError,ValueError,RuntimeError) as e:
        print(f"ERROR: {e}",file=sys.stderr)
        return 2

if __name__=="__main__":
    raise SystemExit(main())
