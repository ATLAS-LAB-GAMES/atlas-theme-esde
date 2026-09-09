#!/usr/bin/env python3
"""Static validation for ATLAS ES-DE v0.2.0 test builds.

This is not a replacement for ES-DE's strict runtime theme parser. It catches
well-formedness, static include/asset mistakes, capability mismatches, required
v0.2.0 files and logo geometry before packaging.
"""
from __future__ import annotations
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


# 1. Parse every XML file.
xml_files = sorted(ROOT.rglob("*.xml"))
parsed: dict[Path, ET.Element] = {}
for path in xml_files:
    try:
        root = ET.parse(path).getroot()
        parsed[path] = root
        if path.name != "capabilities.xml" and root.tag != "theme":
            err(f"{path.relative_to(ROOT)}: expected <theme> root, got <{root.tag}>")
        if path.name == "capabilities.xml" and root.tag != "themeCapabilities":
            err(f"{path.relative_to(ROOT)}: expected <themeCapabilities> root")
    except ET.ParseError as exc:
        err(f"XML parse error {path.relative_to(ROOT)}: {exc}")

# 2. Static include targets must exist. Dynamic includes are skipped.
for path, root in parsed.items():
    if path.name == "capabilities.xml":
        continue
    for inc in root.iter("include"):
        text = (inc.text or "").strip()
        if not text or "${" in text:
            continue
        target = (path.parent / text).resolve()
        try:
            target.relative_to(ROOT.resolve())
        except ValueError:
            err(f"{path.relative_to(ROOT)}: include escapes theme root: {text}")
            continue
        if not target.is_file():
            err(f"{path.relative_to(ROOT)}: missing include {text}")

# 3. Check static asset paths in the v0.2.0 core files. Dynamic paths are skipped.
core_files = [
    ROOT/"atlas-system.xml",
    ROOT/"atlas-gamelist-common.xml",
    ROOT/"atlas-gamelist-shelf.xml",
    ROOT/"atlas-gamelist-grid.xml",
    ROOT/"theme.xml",
]
for path in core_files:
    root = parsed.get(path)
    if root is None:
        continue
    for tag in ("path", "default", "defaultImage", "staticImage", "fontPath", "filledPath", "unfilledPath"):
        for el in root.iter(tag):
            text = (el.text or "").strip()
            if not text or "${" in text or not text.startswith("."):
                continue
            target = (path.parent / text).resolve()
            if not target.is_file():
                err(f"{path.relative_to(ROOT)}: missing static {tag} target {text}")
    for el in root.iter("customBadgeIcon"):
        text = (el.text or "").strip()
        if text and "${" not in text and text.startswith("."):
            target = (path.parent / text).resolve()
            if not target.is_file():
                err(f"{path.relative_to(ROOT)}: missing customBadgeIcon {text}")

# 4. Capability declarations and root usage.
cap = parsed.get(ROOT/"capabilities.xml")
theme = parsed.get(ROOT/"theme.xml")
if cap is not None and theme is not None:
    cap_schemes = {x.attrib.get("name", "") for x in cap.findall("colorScheme")}
    cap_variants = {x.attrib.get("name", "") for x in cap.findall("variant")}
    theme_schemes = {x.attrib.get("name", "") for x in theme.findall("colorScheme")}
    theme_variants = {x.attrib.get("name", "") for x in theme.findall("variant")}
    expected_schemes = {"atlas-balanced", "atlas-dark", "atlas-light", "atlas-vibrant", "atlas-clean"}
    expected_variants = {"atlas-shelf", "atlas-grid"}
    if cap_schemes != expected_schemes:
        err(f"capabilities color schemes={sorted(cap_schemes)}, expected={sorted(expected_schemes)}")
    if theme_schemes != expected_schemes:
        err(f"theme color schemes={sorted(theme_schemes)}, expected={sorted(expected_schemes)}")
    if cap_variants != expected_variants:
        err(f"capabilities variants={sorted(cap_variants)}, expected={sorted(expected_variants)}")
    if theme_variants != expected_variants:
        err(f"theme variants={sorted(theme_variants)}, expected={sorted(expected_variants)}")

# 5. Shelf/Grid structure.
def elements(path: Path, tag: str) -> list[ET.Element]:
    root = parsed.get(path)
    return list(root.iter(tag)) if root is not None else []

shelf = ROOT/"atlas-gamelist-shelf.xml"
grid = ROOT/"atlas-gamelist-grid.xml"
common = ROOT/"atlas-gamelist-common.xml"
if len(elements(shelf, "carousel")) != 1:
    err("atlas-gamelist-shelf.xml must define exactly one carousel")
if elements(shelf, "grid"):
    err("atlas-gamelist-shelf.xml unexpectedly defines a grid")
if len(elements(grid, "grid")) != 1:
    err("atlas-gamelist-grid.xml must define exactly one grid")
if elements(grid, "carousel"):
    err("atlas-gamelist-grid.xml unexpectedly defines a carousel")
if elements(common, "grid") or elements(common, "carousel"):
    err("atlas-gamelist-common.xml must not define the primary carousel/grid")

# 6. Geometry/metadata invariants for the agreed first pass.
common_root = parsed.get(common)
if common_root is not None:
    by_name = {}
    for el in common_root.iter():
        name = el.attrib.get("name")
        if name:
            by_name[name] = el
    def child_text(name: str, child: str) -> str | None:
        el = by_name.get(name)
        if el is None:
            return None
        c = el.find(child)
        return (c.text or "").strip() if c is not None else None
    if child_text("game-panel", "pos") != "0.026 0.026" or child_text("game-panel", "size") != "0.325 0.500":
        warn("game info panel geometry differs from Test Build 3 design target")
    if child_text("game-video", "pos") != "0.365 0.026" or child_text("game-video", "size") != "0.609 0.500":
        err("game video geometry differs from Test Build 3 inset media window")
    if child_text("game-video", "zIndex") != "4":
        err("game video must render behind the gamelist background in Test Build 3")
    if child_text("game-media-panel", "color") != "00000000":
        err("legacy hard-edged game media panel must remain transparent")
    if child_text("game-description", "container") != "true" or child_text("game-description", "containerType") != "vertical":
        err("game description must be a vertical scrolling container")
    if child_text("game-release-year", "metadata") != "releasedate" or child_text("game-release-year", "format") != "%Y":
        err("release year must use releasedate formatted as %Y")
    if child_text("game-system-name", "text") != "${systemName}":
        err("game system name must use the short ATLAS ${systemName} variable")

system_root = parsed.get(ROOT/"atlas-system.xml")
if system_root is not None:
    desc = None
    for el in system_root.iter("text"):
        if el.attrib.get("name") == "system-description":
            desc = el
            break
    if desc is None or (desc.findtext("container") or "").strip() != "true":
        err("system description must be a scrolling container")
    cars = [el for el in system_root.iter("carousel") if el.attrib.get("name") == "systemcarousel"]
    if len(cars) != 1:
        err("system view must contain exactly one systemcarousel")
    else:
        if (cars[0].findtext("pos") or "").strip() != "0.5 0.746":
            warn("system carousel position changed from the locked v0.1.0 geometry")
        if (cars[0].findtext("itemSize") or "").strip() != "0.125 0.125":
            err("system carousel itemSize must use the Test Build 3 slot-filling geometry")
        if (cars[0].findtext("imageFit") or "").strip() != "fill":
            err("system carousel imageFit must be fill")

# 7. Required files.
required = [
    "atlas-gamelist-common.xml", "atlas-gamelist-shelf.xml", "atlas-gamelist-grid.xml",
    "aspect-ratio-4-3-grid.xml", "aspect-ratio-16-9-grid.xml",
    "_inc/atlas/ui/metadata-icons/verified-status-v020.png",
    "_inc/atlas/ui/metadata-icons/playable-status-v020.png",
    "_inc/atlas/ui/metadata-icons/broken-status-v020.png",
    "_inc/atlas/ui/metadata-icons/verified-icon-v020.png",
    "_inc/atlas/ui/metadata-icons/playable-icon-v020.png",
    "_inc/atlas/ui/metadata-icons/broken-icon-v020.png",
    "tools/emblems/atlas-emblems.py", "tools/emblems/atlas-emblems.csv.example",
    "tools/logos/atlas-logo-audit.py", "tools/logos/atlas-logo-normalize.py", "tools/progress/atlas-progress.py", "V020-TEST-CHECKLIST.md",
]
for rel in required:
    if not (ROOT/rel).is_file():
        err(f"missing required v0.2.0 file: {rel}")

# 8. Carousel logo canvas geometry and Test Build 3 occupancy.
logo_dir = ROOT/"_inc/systems/logos-atlas"
logo_files = sorted(logo_dir.glob("*.png"))
for path in logo_files:
    try:
        with Image.open(path) as src:
            im=src.convert("RGBA")
            if im.size != (480, 360):
                err(f"carousel logo {path.name}: {im.size[0]}x{im.size[1]}, expected 480x360")
                continue
            mask=im.getchannel("A").point(lambda v:255 if v>=48 else 0)
            bbox=mask.getbbox()
            if not bbox:
                err(f"carousel logo {path.name}: no meaningful visible content")
                continue
            expect=(2,2,478,358)
            if any(abs(a-b)>2 for a,b in zip(bbox,expect)):
                err(f"carousel logo {path.name}: meaningful bbox={bbox}, expected about {expect}")
    except Exception as exc:
        err(f"logo image unreadable: {path.name}: {exc}")
if len(logo_files) < 200:
    warn(f"only {len(logo_files)} carousel logo PNG files found")

# 8b. Five gamelist backgrounds must be full-size RGBA-capable images.
for variant in ("balanced","dark","light","vibrant","clean"):
    bg=ROOT/"_inc/atlas/backgrounds"/f"{variant}-gamelist.webp"
    if not bg.is_file():
        err(f"missing gamelist background {bg.relative_to(ROOT)}")
        continue
    try:
        with Image.open(bg) as im:
            rgba=im.convert("RGBA")
            if rgba.size != (1536,1024):
                err(f"{bg.name}: size {rgba.size}, expected 1536x1024")
            # Center of video window should be transparent so video is visible; four near-edge
            # samples should retain overlay alpha for the organic frame.
            W,H=rgba.size; x0=round(.365*W); y0=round(.026*H); x1=round(.974*W); y1=round(.526*H)
            a=rgba.getchannel("A")
            cx=(x0+x1)//2; cy=(y0+y1)//2
            if a.getpixel((cx,cy)) > 20:
                err(f"{bg.name}: video-window center is not transparent")
            samples=[(x0+5,cy),(x1-6,cy),(cx,y0+5),(cx,y1-6)]
            if any(a.getpixel(pt)<100 for pt in samples):
                err(f"{bg.name}: one or more video-window edges lack the organic overlay")
    except Exception as exc:
        err(f"gamelist background unreadable {bg.name}: {exc}")

# 9. Emblem assets.
for name in ["hack", "mod", "fangame"] + [f"disc{i}" for i in range(1,7)]:
    p = ROOT/"tools/emblems/assets"/f"{name}.png"
    if not p.is_file():
        err(f"missing emblem asset {p.relative_to(ROOT)}")
    else:
        try:
            with Image.open(p) as im:
                if im.mode not in ("RGBA", "LA", "P"):
                    warn(f"emblem {name} is not stored with an obvious alpha-capable mode ({im.mode})")
        except Exception as exc:
            err(f"emblem {name} unreadable: {exc}")

print(f"XML files parsed: {len(parsed)}/{len(xml_files)}")
print(f"Carousel PNGs checked: {len(logo_files)}")
if warnings:
    print("\nWARNINGS:")
    for item in warnings:
        print(f"  - {item}")
if errors:
    print("\nERRORS:")
    for item in errors:
        print(f"  - {item}")
    print(f"\nFAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
    raise SystemExit(1)
print(f"\nPASS: 0 errors, {len(warnings)} warning(s)")
