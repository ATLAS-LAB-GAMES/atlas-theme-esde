# Changelog

## v0.2.0 — Test Build 5

- Based directly on the RG476H-validated Test Build 4 tree.
- Normalized the 23 post-Test-4 replacement carousel cards to true 480×360 PNGs.
- Added full theme assets/metadata for Crash Bandicoot, Spyro the Dragon, Pokemon Hacks and Emulators collections.
- Added ATLAS variant artwork for 16 active RG476H systems that previously lacked it.
- Hardened the manual emblem tool and expanded automated tests from 5 to 7.
- Reworked Collection Progress for ES-DE multi-root gamelists and optional custom-collection aggregation; added tests and local JSON state.
- Added experimental alternate carousel cards.
- Updated static validation and cleaned obsolete build artifacts/documentation.

## v0.2.0 — Test Build 4

- Removed unsupported `imageRelativeScale` from `systemcarousel`.
- Locked the RG476H carousel position at `0.5007 0.7360`.
- Normalized all original Test Build 4 carousel cards to 480×360.
- Reduced/repositioned game-view system logo and removed the metadata-row status shield.
- Unified bottom status plate geometry.
- Rebuilt the five gamelist backgrounds around the video opening.

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
