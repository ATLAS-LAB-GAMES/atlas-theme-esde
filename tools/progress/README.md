# ATLAS Collection Progress helper

The ES-DE theme engine exposes total game counts but not an aggregate count of games with `playcount > 0`. This optional helper computes played/available for normal systems from ES-DE `gamelist.xml` files and writes the resulting percentage/bar value into the ATLAS theme metadata.

Dry run:
```bash
python3 atlas-progress.py --gamelists-root /path/to/ES-DE/gamelists --theme-root /path/to/atlas-theme-esde
```
Apply:
```bash
python3 atlas-progress.py --gamelists-root /path/to/ES-DE/gamelists --theme-root /path/to/atlas-theme-esde --apply
```
Restart/reload ES-DE afterward. Custom-collection aggregation is deferred because those collections reference games across source systems.
