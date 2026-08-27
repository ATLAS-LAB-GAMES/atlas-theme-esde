# ATLAS Phase 1 Revision 5 Compatibility Hotfix

- Fixed stable ES-DE theme loading by removing a development-only carousel property.
- Default package targets ES-DE 3.2+; live playtime text is disabled until the installed ES-DE version is confirmed.

## Phase 1 Revision 3
- Enlarged and repositioned hero artwork so characters/art can extend under the top header, behind the information area, and further beneath the system carousel.
- Replaced the top-center ATLAS header with a metallic lockup asset closer to the supplied concept art, including a smaller integrated emblem and updated green accent.
- Replaced the top-left ATLAS OS lockup with a concept-art-based style asset while leaving the version text separate.
- Reduced overlay opacity in the information side fade, bottom fade, and carousel fill so more of the background hero art remains visible.

# ATLAS Phase 1 Changelog

## Revision 2 — concept-art alignment

- Removed the outlined information card from the system view. System information now sits directly over a controlled left-side atmospheric fade, matching the supplied concept art.
- Rebuilt the system-view geometry around the supplied 4:3 reference: larger metallic system title, shorter description, four compact statistics rows, seven-card carousel and a slimmer footer.
- Switched system-view body and metadata typography to the included Roboto Condensed face for a closer match to the reference.
- Added pre-rendered metallic title artwork for supported systems and collections, with a text fallback for newly created collections.
- Rebuilt the five backgrounds without the previous technical grid pattern. They now use softer nebula texture, vignette, horizon bloom and emerald lighting.
- Added variant-specific PlayStation hero artwork extracted from the supplied concept references. Other systems continue to reuse the strongest existing artwork until their dedicated art passes.
- Rebuilt the carousel cards with restrained fills, subtle borders and a brighter selected-system glow.
- Added concise `systemSummary` metadata so the information area uses short console-style descriptions rather than long encyclopedia text.
- Restored the concept-art information row `COLLECTION PROGRESS`. ES-DE does not expose a live system-level completion percentage, so the theme provides a per-system `systemCollectionProgress` variable that defaults to an em dash and can be overridden manually.
- Cleaned the supplied ATLAS emblem and used it for the centered wordmark and compact ATLAS OS lockup.

## Theme architecture

- Five selectable variants only: Balanced, Dark, Light, Vibrant and Clean.
- One non-selectable ATLAS transition profile.
- Supported aspect ratios reduced to 4:3 and 16:9.
- Active view definitions consolidated into `atlas-system.xml` and `atlas-gamelist.xml`.

## Gamelist

- Old list, detailed, Elementflix and multiple grid choices remain removed from the selectable interface.
- One interim 3D-box carousel with video and fan-art/screenshot support remains available.
- The final Elementarial-inspired 3D-box grid is reserved for Phase 2.

## Included collections

- Middle Earth Collection
- Pokemon Collection
- Zelda Collection
- Sonic Collection
- Mario Collection
- Jurassic Park Collection
- Hogwarts Collection
- Final Fantasy Collection
- Yu-Gi-Oh Collection
- Digimon Collection
- EA Sports Collection

Each includes a root theme entry, metadata, logo, metallic title and ATLAS-styled hero artwork.
## Phase 1 Revision 5

- Re-cropped and repositioned the ATLAS wordmark at the very top of the screen.
- Added a separate metallic `atlas-tagline.png` with an integrated shadow.
- Added `_inc/systems/system-logos/` for horizontal header-logo replacements.
- Applied a subtle brushed-metal finish and integrated shadow to system titles.
- Removed the duplicate XML title shadow that caused two system names to show.
- Re-centred and resized carousel logos to stay inside all seven cards.
- Aligned Wi-Fi/battery status and clock on a shared top baseline.
- Reworked system and gamelist footers with ATLAS-green icons and wider spacing.
- Rebuilt the gamelist panel without a border, using the system artwork stack,
  vignetted video/fanart, display-font game titles and the existing 3D-box carousel.
- Added native favorite, playtime, completed, manual and rating indicators.
- Added manual per-game override support for achievements and ATLAS verification.
- Moved collection implementation files under `_inc/collections/` while retaining
  the root-level discovery shims required for explicitly themed collections.
- Added setup and metadata documentation.
- Removed an invalid zero-byte EA Sports collection artwork placeholder so ES-DE safely falls back to the default background.
