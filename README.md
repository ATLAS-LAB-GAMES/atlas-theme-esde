# ATLAS Theme for ES-DE

**Version 0.1.0**

ATLAS is a console-focused theme for [ES-DE](https://es-de.org/) designed around cinematic system artwork, a compact console-style information layout, and a consistent visual identity across classic and modern gaming platforms.

This is the first public release of the ATLAS ES-DE theme from **ATLAS-LAB-GAMES**.

## Features

- Five selectable visual variants:
  - **Balanced** — moderate contrast with restrained emerald lighting
  - **Dark** — deep blacks, cinematic shadows, and stronger green highlights
  - **Light** — bright silver-white styling with softer depth
  - **Vibrant** — higher saturation with stronger teal and emerald energy
  - **Clean** — minimal white and pale-grey presentation
- Dedicated **4:3** layout, with handheld devices such as the Anbernic RG476H as a primary design target
- **16:9** landscape support
- Full-screen, system-specific ATLAS artwork
- Metallic system titles and ATLAS system branding
- Seven-item system carousel
- System information panel with:
  - game count
  - favorite count
  - last-played date
  - collection-progress field
- ATLAS-styled gamelist with 3D box-art carousel
- Video and fan-art/screenshot support
- Native ES-DE metadata indicators for favorites, playtime, completion, manuals, rating, and broken status
- Optional per-game RetroAchievements indicator overrides
- Dedicated artwork and metadata for supported ATLAS custom collections
- ATLAS transition profile with fade transitions between system and gamelist views

## Supported aspect ratios

ATLAS currently supports:

- **4:3** — primary ATLAS layout
- **16:9** — widescreen landscape layout

The layout can be selected through ES-DE's theme settings when automatic aspect-ratio selection does not choose the desired mode.

## Installation

### Release download

1. Download the latest ATLAS ES-DE theme release from this repository.
2. Extract the release archive.
3. Copy the extracted theme folder into your ES-DE themes directory.
4. Start or restart ES-DE.
5. Open **UI Settings → Theme**.
6. Select **ATLAS**.
7. Select the desired theme variant:
   - Balanced
   - Dark
   - Light
   - Vibrant
   - Clean

Keep the complete directory structure intact. The `_inc` directory contains required artwork, fonts, metadata, logos, icons, and supporting XML files.

### Git installation

The repository can also be cloned directly into your ES-DE themes directory:

```bash
git clone https://github.com/ATLAS-LAB-GAMES/atlas-theme-esde.git
```

To update a cloned copy later:

```bash
git pull
```

## Repository structure

```text
atlas-theme-esde/
├── _inc/
│   ├── atlas/
│   ├── fonts/
│   └── systems/
├── Digimon Collection/
├── EA Sports Collection/
├── Final Fantasy Collection/
├── Hogwarts Collection/
├── Jurassic Park Collection/
├── Mario Collection/
├── Middle Earth Collection/
├── Pokemon Collection/
├── Sonic Collection/
├── Yu-Gi-Oh Collection/
├── Zelda Collection/
├── completed/
├── now-playing/
├── aspect-ratio-16-9.xml
├── aspect-ratio-4-3.xml
├── atlas-gamelist.xml
├── atlas-system.xml
├── capabilities.xml
├── theme.xml
├── README.md
├── ATLAS-METADATA-NOTES.md
└── COLLECTIONS-SETUP.md
```

## Custom collections

ATLAS currently includes dedicated theme support for:

- Digimon Collection
- EA Sports Collection
- Final Fantasy Collection
- Hogwarts Collection
- Jurassic Park Collection
- Mario Collection
- Middle Earth Collection
- Pokemon Collection
- Sonic Collection
- Yu-Gi-Oh Collection
- Zelda Collection

See [COLLECTIONS-SETUP.md](COLLECTIONS-SETUP.md) for configuration instructions.

## Metadata

ATLAS uses ES-DE's native metadata where possible and supplements it with ATLAS-specific system metadata and optional per-game overrides.

See [ATLAS-METADATA-NOTES.md](ATLAS-METADATA-NOTES.md) for details.

## Collection progress

ES-DE does not currently expose a live system-level completion percentage to themes.

ATLAS therefore provides the variable:

```text
${systemCollectionProgress}
```

It defaults to an em dash (`—`) unless a value is supplied through the system metadata configuration.

## Compatibility and project status

Version **0.1.0** is the first public ATLAS ES-DE release.

The theme is intended for ES-DE 3.x and uses the current ES-DE theme capability, metadata, badge, carousel, and game-override mechanisms used during ATLAS development.

Because ATLAS contains a large amount of system-specific artwork, the repository and release archive are substantially larger than a typical text-only ES-DE theme.

## Credits

ATLAS was developed using the structure of the **Elementerial ES-DE port**, which is based on the original Elementerial theme by **mluizvitor**.

The included system metadata set incorporates third-party metadata work distributed under Creative Commons Attribution-NonCommercial-ShareAlike terms. Some metadata was derived from sources including Wikipedia, LaunchBox, ScreenScraper, and prior community theme projects.

Included fonts and third-party assets retain their respective licenses.

Platform names, logos, game characters, artwork, and trademarks remain the property of their respective owners.

ATLAS is a non-commercial fan project intended for personal game-library organization and preservation.

## License

The ATLAS theme is distributed under **Creative Commons Attribution-NonCommercial-ShareAlike (CC BY-NC-SA)** terms, subject to the separate rights and licenses that apply to included third-party assets.

## Project

**ATLAS-LAB-GAMES**

Find your game. Play your way.