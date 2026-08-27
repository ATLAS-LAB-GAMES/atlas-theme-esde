## Phase 1 Revision 3
- Enlarged and repositioned hero artwork so characters/art can extend under the top header, behind the information area, and further beneath the system carousel.
- Replaced the top-center ATLAS header with a metallic lockup asset closer to the supplied concept art, including a smaller integrated emblem and updated green accent.
- Replaced the top-left ATLAS OS lockup with a concept-art-based style asset while leaving the version text separate.
- Reduced overlay opacity in the information side fade, bottom fade, and carousel fill so more of the background hero art remains visible.

# ATLAS for ES-DE — Phase 1 Revision 2

ATLAS is a focused ES-DE theme designed to provide a console-like interface for browsing and preserving classic game libraries. This revision aligns the system view much more closely with the supplied ATLAS concept artwork and deliberately limits customization to five visual variants.

## System-view variants

- **Balanced** — smoky graphite, moderate contrast and restrained emerald lighting
- **Dark** — deep black, cinematic shadows and the strongest emerald glow
- **Light** — luminous silver-white with soft depth
- **Vibrant** — saturated teal and emerald energy
- **Clean** — minimal white and pale grey

All five use the same layout and navigation behavior.

## Revised system view

- Full-screen hero artwork rather than a separated rectangular art region
- Open left-side information area with no outlined panel
- Supplied ATLAS emblem, centered metallic wordmark and compact ATLAS OS lockup
- Roboto Condensed system information typography
- Metallic pre-rendered system title artwork
- Concise system summaries instead of long metadata paragraphs
- Game count, favorite count, last-played date and collection-progress row
- Seven-card system carousel with a restrained frame and stronger selected glow
- Slim footer controls and simple transitions

The five supplied PlayStation concept images are used to provide variant-specific PlayStation hero artwork. Existing artwork is retained for other systems until their dedicated visual passes are completed.

### Collection progress field

ES-DE does not expose a live system-level collection completion percentage to themes. The layout includes the field because it is part of the supplied concept design, but the underlying `${systemCollectionProgress}` variable defaults to `—`. A value can be set manually in a system metadata XML file when desired.

## Interim gamelist

Phase 1 keeps one interim 3D-box carousel with video and fan-art/screenshot support. The final Elementarial-inspired **3D-box grid** is planned for Phase 2.

## Supported aspect ratios

- **4:3** — primary target matching the supplied concept art and RG476H display
- **16:9** — landscape fallback

## Included collection systems

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

Create or rename each ES-DE custom collection using the exact corresponding name. In **Game collection settings**, set **Group custom collections** to **If unthemed** or **Never** so explicitly themed collections can appear as individual systems.

## Installation

1. Extract the `atlas-es-de` folder into the ES-DE themes directory.
2. Select **ATLAS** in ES-DE UI Settings.
3. Choose Balanced, Dark, Light, Vibrant or Clean under Theme Variant.
4. Select 4:3 or 16:9 if automatic aspect-ratio detection does not choose the intended layout.

Keep a backup of the previous theme folder before replacing it.

## Credits and notice

The theme was derived from the Elementerial ES-DE port, itself based on Elementerial by mluizvitor. Existing Inter and Roboto Condensed font assets are retained from the uploaded theme package.

The package retains the original **Creative Commons CC-BY-NC-SA** licensing notice. Third-party platform names, logos, characters and game artwork remain the property of their respective rights holders. This is a noncommercial fan project intended for game-library preservation and personal use.
