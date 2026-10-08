import test from 'node:test';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFileSync} from 'node:fs';
import {SCENE_CATALOG,getScenePoster} from '../src/explorer/scene-catalog';

test('every Blender lesson has a complete, current still illustration for graphics failures',()=>{
  const models=JSON.parse(readFileSync(new URL('../public/models/blender/manifest.json',import.meta.url),'utf8')).assets;
  const posters=JSON.parse(readFileSync(new URL('../public/models/posters/manifest.json',import.meta.url),'utf8')).assets;
  const scenes=SCENE_CATALOG.filter(scene=>scene.format==='blender');
  assert.equal(scenes.length,1251);
  assert.deepEqual(Object.keys(posters).sort(),scenes.map(scene=>scene.scene).sort());
  for(const scene of scenes){
    const poster=posters[scene.scene],model=models[scene.scene];
    assert.equal(poster.word,scene.word,scene.word);
    assert.equal(getScenePoster(scene.word),poster.url,scene.word);
    assert.equal(poster.glbSha256,model.sha256,`${scene.word}: stale GLB render`);
    assert.equal(poster.blendSha256,model.blendSha256,`${scene.word}: stale native render`);
    const bytes=readFileSync(new URL(`../public${poster.url}`,import.meta.url));
    assert.equal(bytes.toString('ascii',0,4),'RIFF',scene.word);
    assert.equal(bytes.toString('ascii',8,12),'WEBP',scene.word);
    assert.equal(bytes.readUInt32LE(4)+8,bytes.length,`${scene.word}: incomplete image`);
    assert.equal(bytes.length,poster.bytes,scene.word);
    assert.equal(createHash('sha256').update(bytes).digest('hex'),poster.sha256,scene.word);
    assert.equal(poster.settings.width,512,scene.word);
    assert.equal(poster.settings.height,460,scene.word);
  }
  assert.equal(getScenePoster('not-a-word'),undefined);
});
