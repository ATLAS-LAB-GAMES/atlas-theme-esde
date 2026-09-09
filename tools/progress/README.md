# ATLAS Collection Progress helper — v0.2.0 Test Build 5

ES-DE exposes a system's total game count to themes, but not an aggregate count of games that have been played. This manual helper calculates **played / available** from ES-DE `gamelist.xml` data and writes the percentage/bar variables into the ATLAS theme metadata.

A game counts as played when `<playcount>` is greater than zero. Entries marked `<nogamecount>true</nogamecount>` are excluded.

## Normal systems

Dry run first:

```bash
python3 atlas-progress.py \
  --gamelists-root /path/to/ES-DE/gamelists \
  --theme-root /path/to/atlas-theme-esde
```

Apply:

```bash
python3 atlas-progress.py \
  --gamelists-root /path/to/ES-DE/gamelists \
  --theme-root /path/to/atlas-theme-esde \
  --apply
```

Restart/reload ES-DE after applying.

## Custom collections

Test Build 5 can also aggregate custom collections across source systems. Point it at the ES-DE application-data `collections` directory:

```bash
python3 atlas-progress.py \
  --gamelists-root /path/to/ES-DE/gamelists \
  --collections-root /path/to/ES-DE/collections \
  --theme-root /path/to/atlas-theme-esde \
  --apply
```

ES-DE `custom-*.cfg` collection files use `%ROMPATH%/...` paths. Legacy absolute paths are also supported when `--roms-root` is supplied.

## Local state

On `--apply`, the helper writes a snapshot to:

```text
tools/progress/state/progress.json
```

inside that copy of the theme. This is informational/recoverable state; ES-DE reads the values written into `_inc/systems/metadata-global/*.xml`.

Use `--strict` if you want the command to fail when a custom-collection entry cannot be matched to a gamelist record.
