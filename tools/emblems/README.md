# ATLAS Game Emblem Tool — v0.2.0 build 1

This optional companion utility adds ATLAS-styled corner emblems to ES-DE scraped artwork while preserving the original image. It runs **outside ES-DE**; the theme itself continues to request ordinary `3dbox` media, so decorated art works in both **ATLAS Shelf** and **ATLAS Grid** without a second-media lookup.

Initial emblem set:

- `hack` — red
- `mod` — blue
- `fangame` — blue
- `disc1` through `disc6` — neutral grey

## Dependency

Python 3 and Pillow are required. Examples:

```bash
# AlmaLinux / RHEL if python3-pillow is available in your enabled repositories
sudo dnf install python3-pillow

# Or in a Python virtual environment
python3 -m pip install Pillow
```

## CSV

Copy `atlas-emblems.csv.example` to `atlas-emblems.csv` and edit it:

```csv
SYSTEM,GAME,IMAGE_TYPE,EMBLEM_TYPE,ACTION,POSITION
n64,"Super Smash Bros [Hack v1.2]",3dbox,hack,add,top-right
psx,"Final Fantasy VII (Disc 2)",3dbox,disc2,add,top-right
```

`POSITION` may be `top-right`, `top-left`, `bottom-right`, or `bottom-left`. Multiple `add` rows for the same game are supported and are stacked inward from the selected corner.

## Safe workflow

Always start with a dry run:

```bash
python3 atlas-emblems.py \
  --media-root /path/to/ES-DE/downloaded_media \
  --dry-run
```

Then synchronize the artwork:

```bash
python3 atlas-emblems.py \
  --media-root /path/to/ES-DE/downloaded_media \
  --sync
```

`--sync` treats all `ACTION=add` rows as the desired state. If a previously managed game is removed from the CSV, its pristine original is restored automatically.

`--apply` instead performs only the explicit ADD/REMOVE rows and does not prune managed games that are absent from the CSV.

Restore everything managed by ATLAS:

```bash
python3 atlas-emblems.py \
  --media-root /path/to/ES-DE/downloaded_media \
  --restore-all
```

## Backups and re-scrapes

The first time a media file is decorated, its pristine bytes are copied under:

```text
MEDIA_ROOT/.atlas-emblems/backups/
```

A SHA-256 manifest tracks both the pristine and generated files. If a scraper or another program changes a managed image, ATLAS refuses to overwrite it. Inspect the new image first, then use `--refresh-backup` on the next apply/sync if you want that new file to become the pristine source.

## Display-name lookup

Direct media-filename matching is attempted first. If your CSV uses the scraped display name rather than the ROM/media filename, optionally point the tool at your ROM root containing `SYSTEM/gamelist.xml` files:

```bash
python3 atlas-emblems.py \
  --media-root /path/to/downloaded_media \
  --gamelist-root /path/to/ROMs \
  --dry-run
```

The tool refuses ambiguous matches rather than guessing.
