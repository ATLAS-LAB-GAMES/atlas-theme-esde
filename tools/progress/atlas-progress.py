#!/usr/bin/env python3
"""ATLAS Collection Progress helper for ES-DE.

Calculates played/total progress from ES-DE gamelist.xml files and writes the
result into ATLAS per-system theme metadata. A game is considered played when
<playcount> is greater than zero. Entries with <nogamecount>true</nogamecount>
are excluded.

Optional custom-collection support reads ES-DE ``custom-*.cfg`` files and
aggregates play state across source systems. A JSON snapshot is saved inside
the theme by default when --apply is used so the calculated state travels with
that theme copy.
"""
from __future__ import annotations

from pathlib import Path, PurePosixPath
import argparse
import json
import re
import unicodedata
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

MAX_FILL = 0.286


def safe_int(text: str | None) -> int:
    try:
        return int((text or "0").strip() or "0")
    except ValueError:
        return 0



def gamelist_games(path: Path):
    """Return <game> nodes from ES-DE gamelists, including files with top-level alternativeEmulator + gameList siblings."""
    text=path.read_text(encoding="utf-8-sig", errors="replace")
    text=re.sub(r"^\s*<\?xml[^>]*\?>", "", text, count=1, flags=re.I)
    try:
        wrapped=ET.fromstring("<atlasRoot>" + text + "</atlasRoot>")
    except ET.ParseError as exc:
        raise RuntimeError(f"could not parse {path}: {exc}") from exc
    return wrapped.findall("./gameList/game") or wrapped.findall("./game")

def calc_gamelist(path: Path) -> tuple[int, int, float]:
    total = played = 0
    for game in gamelist_games(path):
        if (game.findtext("nogamecount") or "").strip().lower() == "true":
            continue
        total += 1
        if safe_int(game.findtext("playcount")) > 0:
            played += 1
    pct = (100.0 * played / total) if total else 0.0
    return played, total, pct


def progress_values(pct: float) -> dict[str, str]:
    return {
        "systemCollectionProgress": f"{round(pct)}%",
        "systemCollectionProgressFill": f"{max(0.001, MAX_FILL * pct / 100):.6f}",
        "systemCollectionProgressOpacity": "1" if pct > 0 else "0",
    }


def update_metadata(path: Path, pct: float) -> None:
    txt = path.read_text(encoding="utf-8")
    for tag, val in progress_values(pct).items():
        pattern = fr"<{tag}>.*?</{tag}>"
        replacement = f"<{tag}>{val}</{tag}>"
        if re.search(pattern, txt, re.S):
            txt = re.sub(pattern, replacement, txt, count=1, flags=re.S)
        else:
            txt = txt.replace("</variables>", f"    <{tag}>{val}</{tag}>\n  </variables>", 1)
    path.write_text(txt, encoding="utf-8")


def norm_name(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).casefold()
    return "".join(ch for ch in text if ch.isalnum())


def canonical_rel(system: str, game_path: str) -> str:
    game_path = game_path.strip().replace("\\", "/")
    while game_path.startswith("./"):
        game_path = game_path[2:]
    return PurePosixPath(system, game_path).as_posix()


def build_game_index(gamelists_root: Path) -> tuple[dict[str, dict], dict[str, str]]:
    games: dict[str, dict] = {}
    casefold: dict[str, str] = {}
    for d in sorted(p for p in gamelists_root.iterdir() if p.is_dir()):
        gl = d / "gamelist.xml"
        if not gl.is_file():
            continue
        for node in gamelist_games(gl):
            if (node.findtext("nogamecount") or "").strip().lower() == "true":
                continue
            raw_path = (node.findtext("path") or "").strip()
            if not raw_path:
                continue
            key = canonical_rel(d.name, raw_path)
            rec = {
                "system": d.name,
                "path": raw_path,
                "name": (node.findtext("name") or Path(raw_path).stem).strip(),
                "played": safe_int(node.findtext("playcount")) > 0,
            }
            games[key] = rec
            casefold[key.casefold()] = key
    return games, casefold


def collection_line_to_key(line: str, known_systems: set[str], roms_root: Path | None = None) -> str | None:
    s = line.strip().replace("\\", "/")
    if not s or s.startswith("#"):
        return None
    if s.startswith("%ROMPATH%/"):
        return PurePosixPath(s[len("%ROMPATH%/"):]).as_posix()
    if roms_root:
        try:
            p = Path(s).resolve()
            rel = p.relative_to(roms_root.resolve())
            return PurePosixPath(*rel.parts).as_posix()
        except (OSError, ValueError):
            pass
    # Portable fallback for absolute paths: find the first path segment matching
    # a known ES-DE system folder and keep everything from there onward.
    parts = [p for p in PurePosixPath(s).parts if p not in ("/", "")]
    for i, part in enumerate(parts):
        if part in known_systems:
            return PurePosixPath(*parts[i:]).as_posix()
    return PurePosixPath(s.lstrip("/")).as_posix() if "/" in s else None


def metadata_collection_map(meta_root: Path) -> dict[str, Path]:
    result = {}
    for p in meta_root.glob("*.xml"):
        if p.stem.startswith("_"):
            continue
        result[norm_name(p.stem)] = p
    return result


def collection_display_name(cfg: Path) -> str:
    stem = cfg.stem
    if stem.casefold().startswith("custom-"):
        stem = stem[7:]
    return stem


def calc_custom_collection(cfg: Path, games: dict[str, dict], casefold: dict[str, str], known_systems: set[str], roms_root: Path | None) -> tuple[int, int, float, list[str]]:
    raw_entries = []
    for line in cfg.read_text(encoding="utf-8-sig", errors="replace").splitlines():
        key = collection_line_to_key(line, known_systems, roms_root)
        if key:
            raw_entries.append(key)
    # ES-DE collection files should not contain duplicates, but de-duplicate safely.
    entries = list(dict.fromkeys(raw_entries))
    played = 0
    unresolved: list[str] = []
    for key in entries:
        actual = key if key in games else casefold.get(key.casefold())
        if not actual:
            unresolved.append(key)
            continue
        if games[actual]["played"]:
            played += 1
    total = len(entries)
    pct = (100.0 * played / total) if total else 0.0
    return played, total, pct, unresolved


def main() -> int:
    ap = argparse.ArgumentParser(description="Calculate ATLAS system and custom-collection progress from ES-DE data.")
    ap.add_argument("--gamelists-root", type=Path, required=True, help="ES-DE gamelists directory (contains SYSTEM/gamelist.xml)")
    ap.add_argument("--theme-root", type=Path, required=True, help="ATLAS theme root")
    ap.add_argument("--collections-root", type=Path, help="optional ES-DE collections directory containing custom-*.cfg")
    ap.add_argument("--roms-root", type=Path, help="optional ROM root, used to resolve legacy absolute collection paths")
    ap.add_argument("--state-file", type=Path, help="JSON snapshot path (default: THEME/tools/progress/state/progress.json)")
    ap.add_argument("--apply", action="store_true", help="write progress values to theme metadata and save JSON state")
    ap.add_argument("--strict", action="store_true", help="fail if any custom-collection entry cannot be matched to a gamelist")
    a = ap.parse_args()

    gamelists_root = a.gamelists_root.resolve()
    theme_root = a.theme_root.resolve()
    meta = theme_root / "_inc/systems/metadata-global"
    if not gamelists_root.is_dir():
        raise SystemExit(f"ERROR: gamelists root not found: {gamelists_root}")
    if not meta.is_dir():
        raise SystemExit(f"ERROR: ATLAS metadata directory not found: {meta}")

    snapshot = {
        "format": 1,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "systems": {},
        "collections": {},
    }
    matched = 0
    print("NORMAL SYSTEMS")
    for d in sorted(p for p in gamelists_root.iterdir() if p.is_dir()):
        gl = d / "gamelist.xml"
        target = meta / f"{d.name}.xml"
        if not gl.is_file() or not target.is_file():
            continue
        played, total, pct = calc_gamelist(gl)
        matched += 1
        print(f"{d.name:28} {played:4}/{total:<4} {pct:6.1f}%")
        snapshot["systems"][d.name] = {"played": played, "total": total, "percent": round(pct, 3)}
        if a.apply:
            update_metadata(target, pct)

    collection_count = 0
    unresolved_total = 0
    if a.collections_root:
        collections_root = a.collections_root.resolve()
        print("\nCUSTOM COLLECTIONS")
        if not collections_root.is_dir():
            raise SystemExit(f"ERROR: collections root not found: {collections_root}")
        games, casefold = build_game_index(gamelists_root)
        known_systems = {rec["system"] for rec in games.values()}
        meta_map = metadata_collection_map(meta)
        for cfg in sorted(collections_root.glob("custom-*.cfg")):
            lookup = norm_name(collection_display_name(cfg))
            target = meta_map.get(lookup)
            if not target:
                # ES-DE commonly turns spaces into hyphens in filenames. Match
                # against metadata stems after normalization, so exact case is irrelevant.
                print(f"SKIP {cfg.name}: no matching themed collection metadata")
                continue
            played, total, pct, unresolved = calc_custom_collection(cfg, games, casefold, known_systems, a.roms_root)
            collection_count += 1
            unresolved_total += len(unresolved)
            print(f"{target.stem:28} {played:4}/{total:<4} {pct:6.1f}%" + (f"  unresolved={len(unresolved)}" if unresolved else ""))
            snapshot["collections"][target.stem] = {
                "source": cfg.name,
                "played": played,
                "total": total,
                "percent": round(pct, 3),
                "unresolved": unresolved,
            }
            if a.apply:
                update_metadata(target, pct)

    if a.apply:
        state_file = (a.state_file.resolve() if a.state_file else theme_root / "tools/progress/state/progress.json")
        state_file.parent.mkdir(parents=True, exist_ok=True)
        tmp = state_file.with_suffix(state_file.suffix + ".tmp")
        tmp.write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        tmp.replace(state_file)
        print(f"\nState saved: {state_file}")

    print(f"\nSystems matched: {matched}; custom collections matched: {collection_count}; mode: {'APPLY' if a.apply else 'DRY RUN'}")
    if unresolved_total:
        print(f"WARNING: {unresolved_total} custom-collection entr{'y' if unresolved_total == 1 else 'ies'} could not be matched to gamelist records.")
        if a.strict:
            return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
