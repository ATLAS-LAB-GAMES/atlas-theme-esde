# ATLAS ES-DE v0.2.0 Test Build 3

Changes driven by RG476H Test Build 2 screenshots:

- Carousel artwork canvas changed from 480x320 (3:2) to 480x360 (4:3) to match the carousel item aspect ratio. ES-DE preserves image aspect ratio, so the old 3:2 canvases inherently left extra vertical space.
- All 222 `_inc/systems/logos-atlas/` cards normalized to the same 480x360 outer geometry with only a 2 px transparent edge. Internal logo artwork can be refined individually later without changing the slot contract.
- Collection progress no longer uses a fake fixed fill. Optional `tools/progress/atlas-progress.py` calculates played/available from `playcount > 0`, writes the percentage, and sets the bar width to the same percentage.
- Game system logo enlarged again; system name uses per-system font sizing and remains single-line.
- Content below the game title moved upward about 10 px.
- Rating moved to a dedicated lower row opposite the status plate.
- Both status indicators remain: small shield in the metadata icon row AND the large VERIFIED/PLAYABLE/BROKEN plate at the bottom.
- Status shields/plates now share neutral outer geometry; only their state accent and central glyph are colored. This prevents stale lower-state colors from visibly peeking through if ES-DE inset-scales a badge.
- Grid selector remains fully transparent and selected game scale remains 1.25.
- Video remains behind the gamelist background. All five gamelist backgrounds were rebuilt from pristine v0.1.0 artwork using the real video rectangle, ~2% full background coverage and ~5% organic alpha feather on all four sides. No flat rectangle/frame color was added.
