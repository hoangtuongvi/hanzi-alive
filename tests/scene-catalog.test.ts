import test from 'node:test';
import assert from 'node:assert/strict';
import {existsSync,readFileSync} from 'node:fs';
import {SCENE_CATALOG,getSceneDefinition,getVisualCoverage} from '../src/explorer/scene-catalog';

const lessons=JSON.parse(readFileSync(new URL('../public/data/lessons.json',import.meta.url),'utf8')) as {word:string}[];

test('the illustration catalog points only to available words and authored Blender files',()=>{
  const words=new Set(lessons.map(lesson=>lesson.word));
  assert.equal(new Set(SCENE_CATALOG.map(scene=>scene.word)).size,SCENE_CATALOG.length);
  for(const scene of SCENE_CATALOG){
    assert.ok(words.has(scene.word),scene.word);
    assert.equal(getSceneDefinition(scene.word),scene);
    if(scene.format==='blender'){
      assert.match(scene.asset??'',/^\/models\/blender\/[a-z-]+\.glb$/);
      assert.ok(existsSync(new URL(`../public${scene.asset}`,import.meta.url)),scene.word);
      assert.ok(scene.anchors?.length,`${scene.word}: authored callout anchors`);
    }
    if(scene.history)assert.equal(scene.word,'休');
  }
});

test('coverage counts writing-only lessons separately and counts a repeated word just once',()=>{
  const coverage=getVisualCoverage(lessons);
  assert.equal(coverage.words,1000);
  assert.equal(coverage.illustratedScenes,SCENE_CATALOG.length);
  assert.equal(coverage.blenderScenes+coverage.proceduralScenes,coverage.illustratedScenes);
  assert.equal(coverage.writingOnly+coverage.illustratedScenes,1000);
  assert.equal(coverage.historicalLessons,1);
  assert.deepEqual(getVisualCoverage([{word:'休'},{word:'休'},{word:'学习'}]),{
    words:2,blenderScenes:1,proceduralScenes:0,illustratedScenes:1,writingOnly:1,historicalLessons:1,
  });
});
