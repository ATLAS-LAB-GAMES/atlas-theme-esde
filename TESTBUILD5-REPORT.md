# ATLAS ES-DE v0.2.0 — Test Build 5 Report

**Baseline:** RG476H-validated Test Build 4  
**Purpose:** artwork normalization/completeness, four new collections, and hardening of the manual Emblem and Collection Progress tools.

## Baseline integrity

The Test Build 5 working tree was compared directly against the supplied original Test Build 4 archive.

The following runtime/layout files are **byte-identical to Test Build 4**:

- `theme.xml`
- `capabilities.xml`
- `atlas-system.xml`
- `atlas-gamelist.xml`
- `atlas-gamelist-common.xml`
- `atlas-gamelist-grid.xml`
- `atlas-gamelist-shelf.xml`
- `aspect-ratio-16-9.xml`
- `aspect-ratio-4-3.xml`
- `aspect-ratio-16-9-grid.xml`
- `aspect-ratio-4-3-grid.xml`
- all five `_inc/atlas/backgrounds/*-gamelist.webp` files

This preserves the known-good Test Build 4 Shelf/Grid layout, carousel geometry and video/background behavior. The unsupported `imageRelativeScale` property is still absent from `systemcarousel`; its valid use in the game grid remains unchanged.

## Carousel cards

The 23 user-updated files under `_inc/systems/logos-atlas/` were normalized to the Test Build 4 contract:

- 480×360 pixels
- actual PNG encoding (not WebP data with a `.png` extension)
- transparent/full-canvas card geometry compatible with the working carousel

Affected replacements include the updated collection cards plus Dreamcast, GameCube, N64, Neo Geo, PS1/2/3/4, PSP, Saturn, SNES and ZX Spectrum cards.

Final carousel audit: **226/226 active cards passed**.

## Four new collections

Complete theme asset contracts were added for:

- Crash Bandicoot Collection
- Spyro the Dragon Collection
- Pokemon Hacks Collection
- Emulators Collection

Each includes:

- root `theme.xml`
- five ATLAS color-scheme backgrounds
- modern artwork
- active carousel card
- standard logo
- global metadata
- system logo
- title artwork

The collection backgrounds/cards use a clean ATLAS collection treatment intended to remain visually compatible with the existing collection artwork while avoiding dependency on missing franchise-specific source art.

## Missing active-system artwork

The supplied RG476H audit contains 42 active gamelist systems. Test Build 5 now has a complete checked asset contract for **42/42** of those active systems.

ATLAS Balanced/Dark/Light/Vibrant/Clean variants were added for the 16 active systems that previously had base artwork but no ATLAS variant set:

- C64
- Game Boy
- Game Boy Advance
- Game Boy Color
- GameCube
- Mega CD
- Nintendo 3DS
- Nintendo 64
- Nintendo DS
- NES
- Pokemon Mini
- SNES
- Switch
- Virtual Boy
- Wii
- Wii U

These variants derive from the theme's existing system artwork and add the same dark/readability treatment used by the ATLAS presentation.

## Alternate carousel cards

`_inc/systems/logos-atlas-alt/` was added as a **non-runtime experimental folder**. It currently contains 12 optional alternate cards plus a README. The active theme does not reference this directory, so it cannot change Test Build 5 behavior unless cards are manually copied into `logos-atlas` later.

## Game Emblem Tool

`tools/emblems/atlas-emblems.py` was hardened for manual use.

Changes:

- supports ES-DE gamelists containing a top-level `alternativeEmulator` block before `<gameList>`
- adds `--gamelists-root` naming/alias for clearer manual usage
- preserves SHA-256 tracked pristine backups
- restore and sync-prune paths now refuse to overwrite media that was externally re-scraped/changed after ATLAS generated it
- ambiguous display-name matches remain refused rather than guessed
- README/manual workflow updated

Automated tests: **8/8 passed**.

Recommended workflow remains: edit CSV → `--dry-run` → `--sync`.

## Collection Progress

`tools/progress/atlas-progress.py` was reworked so it can be used manually against the current RG476H ES-DE data.

Changes:

- supports normal gamelists and the ES-DE `alternativeEmulator` + `<gameList>` multi-root form
- counts a game as played when `<playcount> > 0`
- excludes `<nogamecount>true</nogamecount>`
- supports optional ES-DE `custom-*.cfg` collection files and aggregates their games across source systems
- supports `%ROMPATH%/...` custom-collection entries
- can report unresolved collection entries and fail them with `--strict`
- on `--apply`, saves an informational local snapshot to `tools/progress/state/progress.json` by default
- updates the existing theme metadata variables consumed by the collection-progress display

Automated tests: **4/4 passed**.

A real dry run against the supplied RG476H audit successfully parsed and calculated all **42/42 gamelist systems**, including the seven gamelists with an `alternativeEmulator` sibling. No real custom collection `.cfg` files were included in the supplied audit, so custom-collection aggregation was validated with synthetic cross-system tests rather than the user's actual collection files. A synthetic APPLY test also confirmed metadata updates plus creation of the local `progress.json` state snapshot.

## Cleanup

Removed stale/non-runtime artifacts from the packaged theme:

- `BUILD-REPORT-v0.2.0-test3.md`
- `TESTBUILD4-REPORT.md`
- `_inc/systems/logos-atlas-v010-original/`
- `tools/logos/logo-audit-build1.json`

Historical copies remain available in the previous Test Build/Git archives; they are not required at runtime.

File permissions were normalized so XML/Markdown/data files are not incorrectly marked executable, while Python tools remain executable.

## Validation results

Final host-side checks:

- Theme XML: **467/467 parsed successfully**
- Test Build 5 validator: **PASS — 0 errors, 0 warnings**
- Active carousel audit: **226 checked, 0 failures**
- Emblem tool tests: **8/8 PASS**
- Collection Progress tests: **4/4 PASS**
- Python tool compilation: **PASS**
- RG476H real gamelist progress dry-run: **42/42 systems matched**
- Active-system artwork contract: **42/42 complete**

## Device test priorities

On the RG476H, specifically verify:

1. System carousel appearance for all recently replaced cards and all four new collection cards.
2. Each new collection in all five color schemes and both Shelf/Grid variants.
3. Manual emblem `--dry-run`, one real `--sync`, then restore/sync-prune behavior on test media.
4. Normal-system Collection Progress with `--apply`, ES-DE reload, and visible percentage/bar update.
5. Custom collection progress using the RG476H's actual ES-DE `collections/custom-*.cfg` files.
6. No regression in Test Build 4 video/background, Verified/Playable/Broken, Shelf/Grid or system-carousel behavior.
