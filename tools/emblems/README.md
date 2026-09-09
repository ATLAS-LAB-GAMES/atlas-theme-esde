# ATLAS Game Emblem Tool — v0.2.0 Test Build 5

This optional **manual** companion utility adds ATLAS-styled corner emblems to ES-DE scraped artwork while preserving pristine originals. The active theme still requests ordinary media such as `3dbox`, so decorated artwork works in both ATLAS Shelf and ATLAS Grid.

Supported emblems:

- `hack` — red
- `mod` — blue
- `fangame` — blue
- `disc1` through `disc6` — neutral grey

Python 3 and Pillow are required.

## CSV

Edit `atlas-emblems.csv` using this format:

```csv
SYSTEM,GAME,IMAGE_TYPE,EMBLEM_TYPE,ACTION,POSITION
n64,"Super Smash Bros [Hack v1.2]",3dbox,hack,add,top-right
psx,"Final Fantasy VII (Disc 2)",3dbox,disc2,add,top-right
```

`POSITION` can be `top-right`, `top-left`, `bottom-right`, or `bottom-left`. Multiple emblems on one game are supported and stack inward from the selected corner.

## Recommended manual workflow

Always dry-run first:

```bash
python3 atlas-emblems.py \
  --media-root /path/to/ES-DE/downloaded_media \
  --gamelists-root /path/to/ES-DE/gamelists \
  --dry-run
```

Then synchronize:

```bash
python3 atlas-emblems.py \
  --media-root /path/to/ES-DE/downloaded_media \
  --gamelists-root /path/to/ES-DE/gamelists \
  --sync
```

`--sync` treats all `ACTION=add` rows as the desired state. Removing a previously managed game from the CSV restores its pristine original.

`--apply` applies only explicit ADD/REMOVE rows and leaves managed games not mentioned in the CSV alone.

Restore everything managed by ATLAS:

```bash
python3 atlas-emblems.py --media-root /path/to/ES-DE/downloaded_media --restore-all
```

## Backups and safety

The first time an image is decorated, its original bytes are copied under:

```text
MEDIA_ROOT/.atlas-emblems/backups/
```

`manifest.json` stores SHA-256 hashes for both the original and ATLAS-generated files. Test Build 5 also hash-checks **restore operations**, so a re-scraped or externally modified image is not silently overwritten by an old backup.

If an image was intentionally re-scraped and you want it to become the new pristine source before another render, inspect it first and use `--refresh-backup` with an apply/sync operation.

Display-name lookup first tries media filenames directly, then can use the optional ES-DE gamelist directory (`--gamelists-root`) to resolve a scraped display name back to its ROM/media stem. Ambiguous matches are refused rather than guessed.
