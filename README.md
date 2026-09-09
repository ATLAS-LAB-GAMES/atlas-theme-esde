# ATLAS Theme for ES-DE

**Version 0.2.0 — Test Build 2**

ATLAS is a console-focused theme for [ES-DE](https://es-de.org/) built around cinematic system artwork, a compact information layout, 3D-box library browsing, and a consistent ATLAS visual identity.

This archive is the **first test build for v0.2.0**. It is intended for hands-on validation before the final v0.2.0 release and will be iterated based on device testing.

## What is new in v0.2.0 Test 1

### Theme layout and visual modes

Visual styling and game-library layout are now independent:

- **Theme Variant**
  - **ATLAS Shelf** — the existing 3D-box carousel concept, refined for v0.2.0
  - **ATLAS Grid** — a new matrix-style 3D-box browser
- **Theme Color Scheme**
  - **Balanced**
  - **Dark**
  - **Light**
  - **Vibrant**
  - **Clean**

Supported aspect ratios remain:

- **4:3** — primary ATLAS handheld layout
- **16:9** — widescreen landscape layout

### System View

- Preserves the centered seven-item system carousel geometry from v0.1.0
- Makes the carousel furniture more transparent and removes the strong separator-line treatment
- Moves the system statistics/progress block upward for more breathing room above the carousel
- Makes the system description a vertical scrolling text container when its content exceeds the available area
- Establishes an ATLAS carousel-logo artwork contract:
  - 480 × 320 px canvas
  - 360 × 240 px card footprint at x=60, y=40
  - centered logo safe area
  - no stretching
- First-pass normalization is included for the previously transparent/inconsistent carousel logos; untouched v0.1.0 originals for changed files are retained in `_inc/systems/logos-atlas-v010-original/`

### Game View

Both Shelf and Grid use the same upper information/media layout:

- Information and video panels share the same top/bottom alignment
- Panel treatment is intentionally soft/translucent rather than hard-framed
- Video is inset and uses rounded corners instead of running into the top-right display edge
- Current system logo appears on the left with the system name immediately to its right
- Game title receives a fixed title area
- Existing metadata icon styling is retained and shifted slightly downward
- Description is a vertically scrolling text container if it is too long for its allotted area
- Genre remains unlabeled
- **RELEASE** year is shown from ES-DE `releasedate` metadata
- **PLAY TIME**, the actual playtime, and the Verified/Playable/Broken status occupy a common aligned row
- Verified / Playable / Broken status plates are rebuilt as opaque, mutually covering plates to prevent state labels showing through one another

### ATLAS Shelf

- Selected 3D box is larger
- Unselected games are more transparent, less saturated, and dimmed
- Games remain visually floating over the gamelist background; no black shelf slab is introduced

### ATLAS Grid

- New vertically scrolling 3D-box grid
- 4:3 and 16:9 receive separate sizing presets
- Selected game receives stronger scale/selector emphasis
- Unselected games are subdued using the same ATLAS focus treatment as Shelf
- Games float directly over the gamelist background

Grid edge-wrap behavior is controlled by ES-DE itself rather than the theme and should be observed during runtime testing.

## ATLAS Game Emblem Tool

`tools/emblems/` contains an optional external companion utility for decorating scraped 3D box artwork with ATLAS corner emblems while preserving pristine originals.

Initial emblem types:

- **Hack** — red
- **Mod** — blue
- **Fan Game** — blue
- **Disc 1–6** — neutral grey

The tool supports:

- CSV-driven mappings
- `--dry-run`
- `--sync`
- `--apply`
- `--restore-all`
- SHA-256 tracked pristine backups
- detection of externally re-scraped/changed artwork
- optional `gamelist.xml` display-name resolution
- multiple emblems on one game

See [`tools/emblems/README.md`](tools/emblems/README.md) before using it. The emblem tool modifies scraped media files, so a dry run should always be performed first.

## Installation for Test Build 2

1. Back up your current ATLAS theme folder or keep your existing v0.1.0 release archive.
2. Extract this archive.
3. Copy the extracted `atlas-theme-esde` directory into the ES-DE themes directory, replacing the test copy you intend to use.
4. Fully restart ES-DE because `capabilities.xml` changes are not picked up by a normal theme reload.
5. Open **UI Settings → Theme** and select **ATLAS**.
6. Configure:
   - **Theme Variant:** `ATLAS Shelf` or `ATLAS Grid`
   - **Theme Color Scheme:** `Balanced`, `Dark`, `Light`, `Vibrant`, or `Clean`
   - **Theme Aspect Ratio:** normally `4:3` for a 4:3 handheld, or `16:9` for widescreen
7. Work through [`V020-TEST-CHECKLIST.md`](V020-TEST-CHECKLIST.md).

## Repository structure

```text
atlas-theme-esde/
├── _inc/
│   ├── atlas/
│   ├── fonts/
│   └── systems/
│       ├── logos-atlas/
│       └── logos-atlas-v010-original/
├── tools/
│   ├── emblems/
│   └── logos/
├── atlas-system.xml
├── atlas-gamelist-common.xml
├── atlas-gamelist-shelf.xml
├── atlas-gamelist-grid.xml
├── atlas-gamelist.xml
├── aspect-ratio-4-3.xml
├── aspect-ratio-16-9.xml
├── aspect-ratio-4-3-grid.xml
├── aspect-ratio-16-9-grid.xml
├── capabilities.xml
├── theme.xml
├── V020-TEST-CHECKLIST.md
├── BUILD-REPORT-v0.2.0-test2.md
├── CHANGELOG.md
└── README.md
```

The custom collection directories and the full `_inc` artwork/metadata hierarchy from v0.1.0 remain included.

## Custom collections and metadata

See:

- [`COLLECTIONS-SETUP.md`](COLLECTIONS-SETUP.md)
- [`ATLAS-METADATA-NOTES.md`](ATLAS-METADATA-NOTES.md)

For v0.2.0 Test 1, the existing ES-DE **Kid Game** flag continues to act as the ATLAS **Playable** state. ES-DE themes cannot add a new editable metadata field to the application itself.

## Test-build status

This is **not the final v0.2.0 release**. Static validation and companion-tool unit tests are performed before packaging, but actual ES-DE rendering/navigation behavior must still be validated in ES-DE on the target hardware.

Background music is intentionally **not** part of v0.2.0 Test 1. It is planned as a separate ATLAS Android companion component rather than being forced into the theme.

## Credits and license

ATLAS was developed using the structure of the **Elementerial ES-DE port**, which is based on the original Elementerial theme by **mluizvitor**.

The included system metadata set incorporates third-party metadata work distributed under Creative Commons Attribution-NonCommercial-ShareAlike terms. Included fonts and third-party assets retain their respective licenses. Platform names, logos, characters, artwork, and trademarks remain the property of their respective owners.

ATLAS is a non-commercial fan project intended for personal game-library organization and preservation.

The ATLAS theme is distributed under **Creative Commons Attribution-NonCommercial-ShareAlike (CC BY-NC-SA)** terms, subject to the separate rights and licenses that apply to included third-party assets.

## Project

**ATLAS-LAB-GAMES**

**Find your game. Play your way.**
