# ATLAS ES-DE v0.2.0 — Test Build 4

Build source: v0.2.0 Test Build 3A (Test 3 plus RG476H runtime hotfix).

## Focused changes from Test 3A

### System View
- Kept the working carousel architecture and selection artwork.
- Removed the unsupported carousel `imageRelativeScale` property that caused the Test 3 black-screen failure.
- Shifted the system carousel approximately 11 px upward and 1 px right on the RG476H 1448x1086 target to center selected cards inside the existing green selection outline.
- Normalized all 222 `_inc/systems/logos-atlas/*.png` files to identical 480x360 full-canvas card geometry.
- Collection Progress companion from Test 3 remains unchanged and optional.

### Game View
- Reduced the system logo approximately 20% from Test 3A.
- Repositioned the system logo so its top edge aligns with the video plane.
- Kept the larger single-line system-name treatment.
- Removed the Verified/Playable/Broken shield/status icon from the metadata icon row entirely.
- Kept the bottom status emblem.
- VERIFIED, PLAYABLE and BROKEN bottom emblems now use exactly the same normalized position (`0.185 0.487`) and size (`0.143 0.034`).
- Shelf and Grid mechanics otherwise remain unchanged.

### Video window
- Preserved the Test 3 bottom-left organic video blend.
- Rebuilt top/right closure for all five gamelist backgrounds.
- Background is now fully opaque above and to the right of the actual video rectangle, eliminating the exposed black strips.
- Top/right background colors are extended from the existing upper-left/lower-right artwork and feather inward over the video.
- Updated: Balanced, Dark, Light, Vibrant and Clean gamelist backgrounds.

## Validation
- 459 / 459 XML files parse successfully.
- ES-DE-specific safety check confirms no `imageRelativeScale` remains inside a carousel element.
- 222 / 222 system carousel cards pass 480x360 geometry audit.
- Metadata status shield elements are absent.
- VERIFIED / PLAYABLE / BROKEN status plate geometry is identical.
- All five gamelist backgrounds are opaque outside the exact video top/right bounds and transparent in the center of the video opening.
- Python tooling compiles.
- ATLAS Emblem Tool: 5 / 5 automated tests pass.
- Collection Progress helper test: 2 played / 4 total -> 50% and half-filled bar.

Runtime rendering must still be validated on the RG476H.
