import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "atlas-progress.py"
spec = importlib.util.spec_from_file_location("atlas_progress", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

GAMELIST = """<gameList>
<game><path>./A.zip</path><name>A</name><playcount>1</playcount></game>
<game><path>./B.zip</path><name>B</name><playcount>0</playcount></game>
<game><path>./C.zip</path><name>C</name><playcount>2</playcount></game>
<game><path>./D.zip</path><name>D</name><playcount>0</playcount></game>
<game><path>./Ignored.zip</path><name>Ignored</name><playcount>1</playcount><nogamecount>true</nogamecount></game>
</gameList>"""

class ProgressTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.root = Path(self.tmp.name)
        self.g = self.root / "gamelists" / "nes"; self.g.mkdir(parents=True)
        (self.g / "gamelist.xml").write_text(GAMELIST)
    def tearDown(self): self.tmp.cleanup()
    def test_normal_system(self):
        played,total,pct = mod.calc_gamelist(self.g / "gamelist.xml")
        self.assertEqual((played,total,round(pct)), (2,4,50))
    def test_esde_alternative_emulator_sibling(self):
        text = """<?xml version="1.0"?>
<alternativeEmulator><label>Standalone</label></alternativeEmulator>
<gameList><game><path>./X.zip</path><name>X</name><playcount>1</playcount></game></gameList>"""
        (self.g / "gamelist.xml").write_text(text)
        self.assertEqual(mod.calc_gamelist(self.g / "gamelist.xml")[:2], (1,1))

    def test_custom_collection_cross_reference(self):
        games,cf = mod.build_game_index(self.root / "gamelists")
        c = self.root / "custom-test-collection.cfg"
        c.write_text("%ROMPATH%/nes/A.zip\n%ROMPATH%/nes/B.zip\n")
        played,total,pct,unresolved = mod.calc_custom_collection(c,games,cf,{"nes"},None)
        self.assertEqual((played,total,round(pct),unresolved),(1,2,50,[]))
    def test_unresolved_is_counted_but_reported(self):
        games,cf = mod.build_game_index(self.root / "gamelists")
        c = self.root / "custom-test.cfg"; c.write_text("%ROMPATH%/nes/A.zip\n%ROMPATH%/nes/Missing.zip\n")
        played,total,pct,unresolved = mod.calc_custom_collection(c,games,cf,{"nes"},None)
        self.assertEqual((played,total,round(pct)),(1,2,50))
        self.assertEqual(unresolved,["nes/Missing.zip"])

if __name__ == '__main__': unittest.main()
