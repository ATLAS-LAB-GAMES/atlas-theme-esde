# ATLAS system logo standard — v0.2.0

The system carousel itself keeps the v0.1.0 geometry. Artwork should target a consistent **480×320** transparent canvas with a **360×240** card/visual footprint placed at **x=60, y=40**. Keep the actual system mark comfortably inside the card (roughly 300×145 is a good starting safe area), preserve aspect ratio, and never stretch a logo.

For this first v0.2.0 build, transparent/inconsistently sized `logos-atlas` entries were given a first-pass graphite + system-accent card so they remain legible in both light and dark color schemes. Existing card artwork was intentionally left intact for manual refinement. Originals changed by this build are retained in `_inc/systems/logos-atlas-v010-original/`.

Audit the directory with:

```bash
cd tools/logos
python3 atlas-logo-audit.py
```
