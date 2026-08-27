# ATLAS gamelist metadata indicators

Revision 10 uses ES-DE native metadata wherever possible.

1. Favorite — native `favorite` badge
2. Time played — native `playtime` metadata
3. Completed — native `completed` badge
4. RetroAchievements available — optional per-game image override
5. Manual available — native `manual` badge
6. Rating — native ES-DE 0–5 `rating` element
7. ATLAS approved / broken — native ES-DE `broken` metadata

Games are ATLAS approved by default because ES-DE defaults `broken` to false. Mark a game as Broken in the ES-DE metadata editor to replace the approved shield with a red broken shield and replace the star rating with a red BROKEN status.

RetroAchievements availability still uses the optional image override workflow under:

`_inc/atlas/metadata-overrides/achievements/`
