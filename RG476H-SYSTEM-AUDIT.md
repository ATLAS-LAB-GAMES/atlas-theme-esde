# RG476H ATLAS System Audit — September 2026

This audit is based on the supplied `RG476H-ATLAS-AUDIT` inventory. The RG476H uses a Unisoc T820, Mali-G57, 8 GB RAM and Android 13. The current ES-DE gamelist set contains **42 systems**.

## Recommended production tiers

### Green — suitable for the ATLAS family gold master

These are comfortably within the RG476H's performance envelope. Normal per-game controller/input certification still applies.

- Amiga 1200 — 6 gamelist entries; performance is easy, but keyboard/mouse-heavy games need curation.
- Atari 2600 — 32
- Atari 5200 — 42
- Atari 7800 — 27
- Atari Jaguar — 21
- Atari Lynx — 19
- Atari ST — 36; performance is easy, but keyboard/mouse-heavy titles need curation.
- Commodore 64 — 17; controller/keyboard mapping is the main concern.
- DOS — 27 gamelist entries; CPU performance is easy, but DOSBox/controller profiles are the main certification work.
- Dreamcast — 43; currently configured for Flycast Standalone.
- Game Gear — 53
- Game Boy — 85
- Game Boy Advance — 90
- Game Boy Color — 48
- Genesis — 216
- MAME — 5; verify the ROM set matches the selected core/version.
- Master System — 176
- Mega CD — 15
- Nintendo 64 — 235
- Nintendo DS — 25
- Neo Geo — 11
- NES — 43
- PC Engine — 2
- Pokemon Mini — 6
- PlayStation 1 — 185; currently configured for SwanStation.
- PSP — 41; currently configured for PPSSPP Standalone.
- Sega 32X — 16
- SNES — 165
- Virtual Boy — 14
- ZX Spectrum — 7; controller/keyboard mapping is the main concern.

### Yellow — keep, but certify game-by-game

- **GameCube — 84.** Dolphin is a good fit, but the T820 is not full-library GameCube hardware. Your list includes demanding titles such as F-Zero GX, Metroid Prime 1/2 and Twilight Princess. Keep the system, but use Verified/Playable/Broken status per title.
- **Wii — 27.** Dolphin support is useful, but motion-control requirements and heavier games (Galaxy 1/2, Metroid Prime Trilogy, Skyward Sword) make controller-only family certification important.
- **PlayStation 2 — 186.** This is the largest high-end certification workload. Many lighter/JRPG titles work, but games such as Burnout Revenge, demanding shooters and other heavy titles can require native resolution, speed hacks or per-game tuning.
- **Nintendo 3DS — 31.** Azahar Standalone is configured. Many games are realistic, but shader/performance and dual-screen layouts should be certified individually.
- **Sega Saturn — 46.** Yaba Sanshiro 2 Standalone is configured. Keep it, but expect occasional game-specific compatibility issues.
- **PlayStation Vita — 10.** Vita3K on Mali has improved but remains game-specific. Treat every Vita title as Playable until personally certified.

### Red / experimental — do not make these a gold-master promise yet

- **PlayStation 3 — 1 (`Turok`).** Android PS3 emulation remains experimental, and the old RPCS3-Android project was discontinued/archived. This should be a lab/experimental system, not a family-console feature target.
- **Xbox — 45.** Original Xbox emulation arrived experimentally on Android in 2026, but current xemu-derived Android ports are resource-heavy. The T820/Mali-G57 is below the class of hardware normally associated with good Xbox performance. Keep the files if desired, but do not expect the 45-game library to be production-ready on RG476H.
- **Wii U — 19.** Android Cemu work exists but remains early/experimental; the official Cemu project still targets desktop platforms. Games such as Breath of the Wild, Mario Kart 8 and Smash Wii U are unrealistic gold-master targets on this T820 device.
- **Switch — 7.** The RG476H is not a good general Switch target. Hollow Knight may have easier alternatives, but Pokémon Legends Arceus, Sword and Super Mario Bros. Wonder should not be assumed reliable. Prefer native Android/source-port/older-platform versions when available.
- **Sega Model 2 — 3 / Model 3 — 2.** These systems lack the straightforward mature Android standalone path that your core retro systems have. Keep them experimental unless you prove a specific emulator/core and direct-launch path on the RG476H.

## Easy system additions

The strongest immediate addition already present on the SD card is **Sega SG-1000**: the ROM audit contains 11 game files under `ROMs/sg1000`, but ES-DE expects the system folder name `sg-1000`. Rename/move that game folder to the ES-DE name and rescan. This should be trivial for the RG476H to emulate.

Other easy systems worth adding when you actually add games include ColecoVision, Intellivision, Amstrad CPC, MSX/MSX2, WonderSwan/WonderSwan Color, Neo Geo CD, PC Engine CD, Game & Watch, ScummVM, EasyRPG, OpenBOR and Pico-8. Their performance requirements are far below the T820; controller suitability and content setup matter more than raw performance.

For the ATLAS fan-game plan, **EasyRPG** is especially useful for RPG Maker 2000/2003 titles. Keep JoiPlay/native Android handling for later RPG Maker generations as a separate certification path.

## Inventory cleanup notes

- `ROMs/sg1000` is a naming mismatch with ES-DE's `sg-1000` convention.
- `ROMs/winint` contains thousands of installed Windows-game files (including an installed Harry Potter game tree); this is not equivalent to thousands of separate games. Treat Windows/Winlator integration as its own curated system, not as a ROM-count system.
- Some gamelists contain duplicate entries (for example multiple Pokémon Brilliant Diamond entries in Switch and duplicates in some GameCube data). Clean these during metadata certification rather than inside the theme.
- Seven supplied gamelists contain ES-DE's top-level `alternativeEmulator` block before `<gameList>`. They are valid for ES-DE's use but are not a conventional single-root XML document. Test Build 5's Emblem and Collection Progress tools now explicitly handle this format.

## ATLAS recommendation

For the October family-console target, treat everything through Dreamcast/N64/PSP/PS1 plus the classic systems as the guaranteed core; keep GameCube/Wii/PS2/3DS/Saturn/Vita as individually certified higher-end libraries; and leave PS3/Xbox/Wii U/Switch/Model 2/Model 3 out of the guaranteed feature set until each game has passed ATLAS certification on the actual RG476H.
