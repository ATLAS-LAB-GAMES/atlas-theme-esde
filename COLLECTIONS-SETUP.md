# ATLAS Custom Collections Setup

ATLAS v0.2.0 Test Build 5 includes dedicated presentation for these custom collections:

- Crash Bandicoot Collection
- Digimon Collection
- EA Sports Collection
- Emulators Collection
- Final Fantasy Collection
- Hogwarts Collection
- Jurassic Park Collection
- Mario Collection
- Middle Earth Collection
- Pokemon Collection
- Pokemon Hacks Collection
- Sonic Collection
- Spyro the Dragon Collection
- Yu-Gi-Oh Collection
- Zelda Collection

Use the names exactly as shown.

## ES-DE setting

Set:

**Main Menu → Game Collection Settings → Group custom collections → Never**

Then use **Create new custom collection from theme** so ES-DE uses the matching ATLAS discovery folder and artwork.

Each collection has a root `theme.xml` that includes the main ATLAS theme. A fully supported collection also has matching files in:

```text
_inc/systems/artwork (atlas)/balanced/
_inc/systems/artwork (atlas)/dark/
_inc/systems/artwork (atlas)/light/
_inc/systems/artwork (atlas)/vibrant/
_inc/systems/artwork (atlas)/clean/
_inc/systems/artwork (modern)/
_inc/systems/logos-atlas/
_inc/systems/logos/
_inc/systems/metadata-global/
_inc/systems/system-logos/
_inc/systems/titles/
```

## Progress for custom collections

Test Build 5 can calculate progress for custom collections by reading ES-DE's `custom-*.cfg` files. See `tools/progress/README.md` and supply both `--gamelists-root` and `--collections-root`.

## Troubleshooting

If a collection appears generic or is grouped with other collections, confirm the exact collection name, create it from the theme, set **Group custom collections** to **Never**, and fully reload ES-DE after replacing theme assets.
