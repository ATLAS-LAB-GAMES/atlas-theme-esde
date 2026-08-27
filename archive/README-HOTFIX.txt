ATLAS ES-DE Phase 1 Revision 5 — Compatibility Hotfix

This package fixes the theme-loading fallback seen in the original Revision 5 archive.

Changes:
- Removed the unsupported carousel itemSpacing property that is present only in the ES-DE development theme engine.
- Removed the active playtime metadata text from the default build so this package remains compatible with ES-DE 3.2 and 3.3 as well as 3.4.
- Kept the grey playtime icon placeholder and all other Revision 5 visual/layout work.
- Preserved the five variants, system logos, metallic titles, tagline, carousel corrections, gamelist vignette, metadata icon row and collection shims.

Installation:
1. Delete the existing atlas-es-de theme folder completely.
2. Extract the atlas-es-de folder from this archive into the ES-DE themes directory.
3. Restart ES-DE; do not merely overlay the archive over the broken folder.

After confirming the installed ES-DE version, the live playtime value can be restored for ES-DE 3.4 or newer.
