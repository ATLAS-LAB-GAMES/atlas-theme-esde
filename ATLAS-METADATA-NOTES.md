# ATLAS Metadata Notes

This document describes the metadata used by **ATLAS Theme for ES-DE v0.1.0**.

ATLAS uses native ES-DE metadata wherever possible and adds a small number of theme-specific variables and optional override files where ES-DE does not expose the required information directly.

## Gamelist metadata indicators

ATLAS currently displays the following game-level indicators.

### Favorite

Uses the native ES-DE:

```text
favorite
```

metadata/badge state.

A game marked as a favorite in ES-DE receives the active ATLAS favorite indicator.

### Time played

Uses the native ES-DE:

```text
playtime
```

metadata value.

ATLAS displays the recorded playtime in the gamelist information area.

### Completed

Uses the native ES-DE:

```text
completed
```

badge state.

Games marked completed in the ES-DE metadata editor receive the ATLAS completed indicator.

### RetroAchievements available

ES-DE does not expose a general theme metadata field for whether a game has RetroAchievements support.

ATLAS therefore uses an optional per-game `gameOverridePath`:

```text
_inc/atlas/metadata-overrides/achievements/
```

To enable the achievements indicator for a game, create a system-specific directory and place an override image matching the ROM basename.

Example ROM:

```text
ROMs/psx/Crash Bandicoot.chd
```

Create:

```text
_inc/atlas/metadata-overrides/achievements/psx/Crash Bandicoot.svg
```

The filename must match the ROM basename exactly, excluding the ROM extension.

Supported ES-DE game-override image formats include:

- JPG
- PNG
- unanimated GIF
- SVG

A template is available at:

```text
_inc/atlas/metadata-overrides/achievements/_template.svg
```

### Manual available

Uses the native ES-DE:

```text
manual
```

badge state.

When a manual is associated with a game, ATLAS displays the manual indicator.

### Rating

Uses the native ES-DE:

```text
rating
```

element.

ATLAS renders the ES-DE 0–5 rating using ATLAS-styled filled and unfilled rating graphics.

### ATLAS approved / broken

ATLAS uses the native ES-DE:

```text
broken
```

metadata state.

By default, a game is treated as available/approved because ES-DE normally considers `broken` false unless the game is explicitly marked otherwise.

To flag a game:

1. Open the game's metadata editor in ES-DE.
2. Mark the game as **Broken**.
3. ATLAS will display its red broken status treatment instead of the normal approved state.

No separate ATLAS verification override file is required in v0.1.0.

## System metadata

The root `theme.xml` loads system metadata from three locations:

```text
_inc/systems/metadata-global/_default.xml
_inc/systems/metadata-global/${system.theme}.xml
_inc/systems/metadata-custom/${system.theme}.xml
```

### Global metadata

```text
_inc/systems/metadata-global/
```

contains the common system information used by the theme, including variables such as:

- system description
- release year/date
- manufacturer
- hardware type
- system color values
- common cover-art proportions

The `_default.xml` file acts as a fallback when a dedicated metadata file is not available.

### ATLAS custom metadata

```text
_inc/systems/metadata-custom/
```

contains ATLAS-specific additions or overrides for individual systems.

These files can be used to adjust system-specific presentation without modifying the shared global metadata set.

## ATLAS system variables

ATLAS uses additional variables for the system information area.

### `systemSummary`

Provides the shorter console-style description displayed on the ATLAS system view.

Example:

```xml
<systemSummary>A concise description intended for the ATLAS system screen.</systemSummary>
```

### `systemCollectionProgress`

Provides the value displayed beside **COLLECTION PROGRESS**.

ES-DE does not currently expose a live aggregate completion percentage for an entire system, so ATLAS cannot calculate this value automatically.

If no value is supplied, the theme should display:

```text
—
```

A custom metadata file can provide a manual value when desired.

Example:

```xml
<systemCollectionProgress>72%</systemCollectionProgress>
```

## Editing metadata

When adding or changing ATLAS-specific metadata:

1. Prefer an entry under:

   ```text
   _inc/systems/metadata-custom/
   ```

2. Use the ES-DE system theme identifier as the filename.

   Example:

   ```text
   psx.xml
   gc.xml
   ps2.xml
   ```

3. Preserve valid ES-DE theme XML structure.

4. Avoid modifying the shared global metadata set unless the underlying factual metadata itself needs correction.

## Naming

System-specific metadata, artwork, titles, logos, and overrides depend on exact ES-DE system identifiers.

Case, spacing, and filenames should therefore be treated as significant unless ES-DE explicitly documents otherwise.