"""Fail-closed admission checks for preserved (non-recipe) Blender scenes."""
import hashlib
import json
import sys
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts/blender'))
import sync_catalog


class PreservedSceneChecks(unittest.TestCase):
    def setUp(self):
        self.stack=ExitStack()
        self.addCleanup(self.stack.close)
        self.root=Path(self.stack.enter_context(tempfile.TemporaryDirectory(prefix='hanzi-catalog-test-')))
        self.stack.enter_context(patch.object(sync_catalog,'ROOT',self.root))
        self.stack.enter_context(patch.object(sync_catalog,'RECIPES',{}))
        self.stack.enter_context(patch.object(sync_catalog,'EXTRA_SCENES',{}))
        self.glb=self.root/'public/models/blender/rest.glb'
        self.native=self.root/'assets/blender/rest.blend'
        for file,data in ((self.glb,b'test GLB fixture'),(self.native,b'test native fixture')):
            file.parent.mkdir(parents=True,exist_ok=True)
            file.write_bytes(data)
        self.scene={'word':'休','scene':'rest','format':'blender','asset':'/models/blender/rest.glb',
                    'anchors':['anchor_person','anchor_tree'],'history':True}
        self.asset={'word':'休','url':self.scene['asset'],'blendFile':'assets/blender/rest.blend',
                    'sha256':hashlib.sha256(self.glb.read_bytes()).hexdigest(),
                    'blendSha256':hashlib.sha256(self.native.read_bytes()).hexdigest(),
                    'anchors':self.scene['anchors']}
        self.lessons=[{'word':'休','memoryElements':[{'glyph':'亻'},{'glyph':'木'}]}]
        self.json('src/explorer/scene-catalog.json',[self.scene])
        self.json('public/data/lessons.json',self.lessons)
        self.json('data/curation/illustration-exclusions.json',{})
        self.manifest()

    def json(self,path,value):
        file=self.root/path
        file.parent.mkdir(parents=True,exist_ok=True)
        file.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

    def manifest(self,extra=None):
        self.json('public/models/blender/manifest.json',{'assets':{'rest':self.asset,**(extra or {})}})

    def verify(self):
        sync_catalog.synchronize(check=True,require_complete=True)

    def test_verified_preserved_scene_passes(self):
        self.verify()

    def test_missing_preserved_glb_is_rejected(self):
        self.glb.unlink()
        with self.assertRaisesRegex(ValueError,'catalog GLB'):self.verify()

    def test_changed_preserved_glb_is_rejected(self):
        self.glb.write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError,'catalog GLB'):self.verify()

    def test_missing_preserved_native_is_rejected(self):
        self.native.unlink()
        with self.assertRaisesRegex(ValueError,'catalog native'):self.verify()

    def test_changed_preserved_native_is_rejected(self):
        self.native.write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError,'catalog native'):self.verify()

    def test_missing_native_checksum_is_rejected(self):
        self.asset.pop('blendSha256');self.manifest()
        with self.assertRaisesRegex(ValueError,'catalog native'):self.verify()

    def test_wrong_manifest_word_is_rejected(self):
        self.asset['word']='木';self.manifest()
        with self.assertRaisesRegex(ValueError,'binding mismatch'):self.verify()

    def test_wrong_callout_inventory_is_rejected(self):
        self.asset['anchors']=['anchor_other'];self.manifest()
        with self.assertRaisesRegex(ValueError,'callout inventory'):self.verify()

    def test_duplicate_manifest_word_is_rejected(self):
        self.manifest({'extra':self.asset})
        with self.assertRaisesRegex(ValueError,'manifest contains'):self.verify()

    def test_missing_database_word_is_rejected(self):
        self.lessons.append({'word':'高手','memoryElements':[{'glyph':'高'},{'glyph':'手'}]})
        self.json('public/data/lessons.json',self.lessons)
        with self.assertRaisesRegex(ValueError,'Incomplete corpus'):self.verify()


if __name__=='__main__':
    unittest.main()
