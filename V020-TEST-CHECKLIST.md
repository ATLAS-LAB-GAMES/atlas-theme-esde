# ATLAS ES-DE v0.2.0 — Test Build 5 checklist

Test Build 5 keeps Test Build 4's validated layout and focuses on artwork/tool validation.

## System View

- Confirm the carousel still matches Test Build 4 positioning and selection spacing.
- Check several untouched cards plus the replaced cards (N64, PS1, PS2, GameCube, Dreamcast, Saturn, SNES, PSP and updated collections).
- Confirm replaced cards are no longer stretched/cropped incorrectly by ES-DE.
- Check the four new collections appear as independently themed systems.
- Check new collection backgrounds in Balanced, Dark, Light, Vibrant and Clean.
- Spot-check the newly added ATLAS backgrounds for GB/GBA/GBC, N64, GameCube, SNES, Wii and 3DS.

## Game View

- Test Shelf and Grid.
- Confirm no Verified/Playable/Broken shield reappears in the metadata row.
- Confirm bottom VERIFIED / PLAYABLE / BROKEN plates still share the same geometry.
- Confirm video top/right closure and bottom-left blend remain identical to Test Build 4.

## Game Emblem Tool

1. Work against copied/safe media first.
2. Run `--dry-run`.
3. Test Hack, Mod, Fan Game and Disc 1–6.
4. Test two emblems on one game.
5. Remove a row and run `--sync`; confirm pristine artwork returns.
6. Change a managed image externally and confirm ATLAS refuses to overwrite/restore it.

## Collection Progress

1. Run a dry run against the RG476H ES-DE gamelists.
2. Apply and restart/reload ES-DE.
3. Confirm displayed percentages match played game counts.
4. Point `--collections-root` at ES-DE's collections directory and verify at least one custom collection.
5. Confirm `tools/progress/state/progress.json` is created after `--apply`.

## Regression

- No black screen entering System View.
- `systemcarousel` contains no `imageRelativeScale`.
- All 226 active carousel cards are true 480×360 PNGs.
- All five gamelist background variants retain their Test Build 4 video opening.
