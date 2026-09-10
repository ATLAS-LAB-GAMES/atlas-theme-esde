# ATLAS Theme for ES-DE

**Version 0.2.0 — Test Build 5**

ATLAS is a console-focused ES-DE theme built around cinematic system artwork, a compact information layout, 3D-box library browsing, and a consistent ATLAS visual identity.

Test Build 5 uses the **RG476H-validated Test Build 4** as its functional baseline. Core Shelf/Grid layout XML and the proven Test Build 4 carousel/video behavior are retained. This build focuses on artwork normalization/completeness and hardening the two manual companion tools.

## Theme modes

- **Theme Variant:** ATLAS Shelf / ATLAS Grid
- **Theme Color Scheme:** Balanced / Dark / Light / Vibrant / Clean
- **Aspect Ratio:** 4:3 / 16:9

## Test Build 5 changes

- Corrected all 23 newly replaced carousel cards to the Test Build 4 contract: **480×360, actual PNG encoding, full-canvas geometry**.
- Added complete theme support for:
  - Crash Bandicoot Collection
  - Spyro the Dragon Collection
  - Pokemon Hacks Collection
  - Emulators Collection
- Added ATLAS variant backgrounds for active RG476H systems that previously relied only on base modern artwork: C64, GB, GBA, GBC, GameCube, Mega CD, 3DS, N64, NDS, NES, Pokemon Mini, SNES, Switch, Virtual Boy, Wii and Wii U.
- Added an experimental `_inc/systems/logos-atlas-alt/` folder for optional future carousel-card customization.
- Hardened the manual Game Emblem Tool, including hash-safe restore behavior and support for ES-DE gamelists that contain a top-level `alternativeEmulator` block.
- Reworked Collection Progress so it handles those ES-DE gamelists and can aggregate custom collections across source systems when given the ES-DE `collections` directory.
- Collection Progress now stores an informational JSON snapshot in `tools/progress/state/progress.json` when applied.
- Updated static validation for the Test Build 4 carousel geometry, actual PNG encoding, the four new collection asset contracts and companion-tool tests.
- Removed obsolete Test Build 3/4 report artifacts and the no-longer-needed in-package v0.1 carousel backup directory. Historical source remains recoverable from Git/Test Build archives.

## Custom collections

See [`COLLECTIONS-SETUP.md`](COLLECTIONS-SETUP.md). For individually themed collections, use:

**Main Menu → Game Collection Settings → Group custom collections → Never**

and create supported collections using **Create new custom collection from theme**.

## Game Emblem Tool

`tools/emblems/atlas-emblems.py` manually decorates scraped artwork with:

- Hack
- Mod
- Fan Game
- Disc 1–6

It maintains pristine SHA-256 tracked backups and refuses to overwrite externally changed media. Always use `--dry-run` first. See [`tools/emblems/README.md`](tools/emblems/README.md).

## Collection Progress

`tools/progress/atlas-progress.py` manually calculates played/total percentages from ES-DE gamelists. Test Build 5 also supports ES-DE custom collection configuration files. See [`tools/progress/README.md`](tools/progress/README.md).

## Carousel artwork contract

Active files in `_inc/systems/logos-atlas/` must be:

- 480×360
- actual PNG files
- full-canvas card geometry

Do not add `imageRelativeScale` to the `systemcarousel`; that property caused the RG476H black-screen failure during Test Build 3 testing.

## Testing

Run:

```bash
python3 tools/validate-v020.py
python3 tools/logos/atlas-logo-audit.py
python3 tools/emblems/tests/test_atlas_emblems.py
python3 tools/progress/tests/test_atlas_progress.py
```

Then work through [`V020-TEST-CHECKLIST.md`](V020-TEST-CHECKLIST.md) on the RG476H.

## Project

**ATLAS-LAB-GAMES**  
**Find your game. Play your way.**
