## v0.2.0 — Test Build 2

- Normalized all 222 `_inc/systems/logos-atlas/` assets to a 480x320 canvas with near-full visible card occupancy.
- Added reproducible `tools/logos/atlas-logo-normalize.py`.
- Enlarged game-view system logo and changed the adjacent header to the ATLAS short system name.
- Rebuilt lower metadata into Genre/Release, Play Time/value, and Rating/Status rows.
- Added faint five-star baseline with green overlay for non-zero ES-DE ratings.
- Moved video behind the gamelist background and removed the hard media-panel frame.
- Added a 2% top/right background cover and 5% alpha feather to all five `*-gamelist.webp` backgrounds.
- Grid selector is transparent; selected Grid item scale is 1.25.
- Rebuilt Verified/Playable/Broken status assets in the ATLAS emblem visual language with opaque backgrounds to eliminate visual stacking.

# Changelog

## v0.2.0 — Test Build 1

First implementation pass for the ATLAS ES-DE v0.2.0 redesign.

### Added

- Separate **ATLAS Shelf** and **ATLAS Grid** theme variants.
- Separate **Balanced, Dark, Light, Vibrant, Clean** color schemes.
- New shared gamelist upper-layout file.
- New 4:3/16:9 Grid sizing overrides.
- Current-system logo + full-system-name game-view header.
- Release-year display.
- Scrollable long system/game description containers.
- Revised mutually covering Verified/Playable/Broken status plates.
- ATLAS Game Emblem companion tool with Hack, Mod, Fan Game, and Disc 1–6 assets.
- System carousel logo geometry audit tool.
- First-pass standardization for previously transparent/inconsistent system carousel logos.

### Changed

- System statistics/progress block moved upward.
- System carousel furniture made more transparent with no visible border-line treatment.
- Game video inset from the top/right edges and given rounded corners.
- Info and media panels aligned to equal height with softer transparency.
- Game metadata icon row moved slightly lower.
- Playtime promoted to a clearer aligned bottom metadata row.
- Shelf selected-cover scale increased and unfocused covers subdued.

### Deferred

- Background music companion Android application.
- Continuous selected-cover pulse/glow experiment.
- Final hand-tuning of every individual system carousel logo.

## v0.1.0

First public ATLAS ES-DE theme release.
