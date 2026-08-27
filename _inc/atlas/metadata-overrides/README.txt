ATLAS per-game metadata icon overrides
======================================

ES-DE does not currently expose arbitrary custom metadata fields to themes for
"RetroAchievements available" or "ATLAS verified". Revision 5 therefore uses
the supported gameOverridePath mechanism as a manual, per-game switch.

To activate an icon for a game:

1. Choose either the achievements or verified directory.
2. Create a subdirectory matching the ROM system short name, for example:
     achievements/psx/
     verified/snes/
3. Copy _template.svg into that directory.
4. Rename the copy to the exact ROM basename, without the ROM extension.

Example for ROM:
  ROMs/psx/Crash Bandicoot.chd

Create:
  achievements/psx/Crash Bandicoot.svg
  verified/psx/Crash Bandicoot.svg

The gray placeholder remains when no override file exists. The green icon is
shown when the matching override exists. Supported override formats are JPG, PNG, unanimated GIF and SVG.
