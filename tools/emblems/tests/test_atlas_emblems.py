import csv
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

SCRIPT = Path(__file__).resolve().parents[1] / "atlas-emblems.py"
spec = importlib.util.spec_from_file_location("atlas_emblems", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def h(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class Args:
    pass


class AtlasEmblemTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.media = self.root / "downloaded_media"
        self.media_dir = self.media / "n64" / "3dboxes"
        self.media_dir.mkdir(parents=True)
        self.target = self.media_dir / "Super Smash Bros [Hack v1.2].png"
        Image.new("RGBA", (600, 900), (60, 80, 120, 255)).save(self.target)
        self.original_hash = h(self.target)
        self.assets = Path(__file__).resolve().parents[1] / "assets"
        self.csv = self.root / "atlas-emblems.csv"
        self.state = self.root / "state"

    def tearDown(self):
        self.tmp.cleanup()

    def write_rows(self, rows):
        with self.csv.open("w", newline="") as f:
            w=csv.writer(f)
            w.writerow(["SYSTEM","GAME","IMAGE_TYPE","EMBLEM_TYPE","ACTION","POSITION"])
            w.writerows(rows)

    def args(self, mode):
        a=Args()
        a.media_root=self.media
        a.csv=self.csv
        a.emblem_root=self.assets
        a.state_root=self.state
        a.gamelist_root=None
        a.dry_run=mode=="dry"
        a.sync=mode=="sync"
        a.apply=mode=="apply"
        a.restore_all=mode=="restore"
        a.refresh_backup=False
        return a

    def test_add_and_restore_all(self):
        self.write_rows([["n64","Super Smash Bros [Hack v1.2]","3dbox","hack","add","top-right"]])
        self.assertEqual(mod.execute(self.args("sync")), 0)
        self.assertNotEqual(h(self.target), self.original_hash)
        manifest=json.loads((self.state/"manifest.json").read_text())
        self.assertEqual(len(manifest["records"]),1)
        self.assertEqual(mod.execute(self.args("restore")),0)
        self.assertEqual(h(self.target),self.original_hash)
        manifest=json.loads((self.state/"manifest.json").read_text())
        self.assertEqual(manifest["records"],{})

    def test_sync_prunes_removed_entry(self):
        self.write_rows([["n64","Super Smash Bros [Hack v1.2]","3dbox","hack","add","top-right"]])
        mod.execute(self.args("sync"))
        self.assertNotEqual(h(self.target),self.original_hash)
        self.write_rows([])
        mod.execute(self.args("sync"))
        self.assertEqual(h(self.target),self.original_hash)

    def test_dry_run_changes_nothing(self):
        self.write_rows([["n64","Super Smash Bros [Hack v1.2]","3dbox","hack","add","top-right"]])
        self.assertEqual(mod.execute(self.args("dry")),0)
        self.assertEqual(h(self.target),self.original_hash)
        self.assertFalse((self.state/"manifest.json").exists())

    def test_display_name_lookup_handles_alternative_emulator_sibling(self):
        glroot=self.root / "gamelists" / "n64"
        glroot.mkdir(parents=True)
        (glroot / "gamelist.xml").write_text(
            '<?xml version="1.0"?>\n<alternativeEmulator><label>Standalone</label></alternativeEmulator>\n'
            '<gameList><game><path>./Super Smash Bros [Hack v1.2].zip</path><name>Smash Hack Display</name></game></gameList>'
        )
        self.target.rename(self.media_dir / "Super Smash Bros [Hack v1.2].png")
        resolved=mod.resolve_media(self.media,"n64","Smash Hack Display","3dbox",self.root / "gamelists")
        self.assertEqual(resolved.name,"Super Smash Bros [Hack v1.2].png")

    def test_multiple_emblems_are_recorded(self):
        self.write_rows([
            ["n64","Super Smash Bros [Hack v1.2]","3dbox","hack","add","top-right"],
            ["n64","Super Smash Bros [Hack v1.2]","3dbox","disc2","add","top-right"],
        ])
        mod.execute(self.args("sync"))
        manifest=json.loads((self.state/"manifest.json").read_text())
        rec=next(iter(manifest["records"].values()))
        self.assertEqual([x["emblem"] for x in rec["emblems"]],["hack","disc2"])


    def test_restore_refuses_external_change(self):
        self.write_rows([["n64","Super Smash Bros [Hack v1.2]","3dbox","hack","add","top-right"]])
        mod.execute(self.args("sync"))
        Image.new("RGBA",(600,900),(1,2,3,255)).save(self.target)
        with self.assertRaises(RuntimeError):
            mod.execute(self.args("restore"))

    def test_sync_prune_refuses_external_change(self):
        self.write_rows([["n64","Super Smash Bros [Hack v1.2]","3dbox","hack","add","top-right"]])
        mod.execute(self.args("sync"))
        Image.new("RGBA",(600,900),(9,8,7,255)).save(self.target)
        self.write_rows([])
        with self.assertRaises(RuntimeError):
            mod.execute(self.args("sync"))
    def test_external_change_is_refused(self):
        self.write_rows([["n64","Super Smash Bros [Hack v1.2]","3dbox","hack","add","top-right"]])
        mod.execute(self.args("sync"))
        Image.new("RGBA",(600,900),(255,0,0,255)).save(self.target)
        self.write_rows([["n64","Super Smash Bros [Hack v1.2]","3dbox","mod","add","top-right"]])
        with self.assertRaises(RuntimeError):
            mod.execute(self.args("sync"))


if __name__ == "__main__":
    unittest.main()
