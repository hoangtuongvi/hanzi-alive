import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import type {Character,Lesson} from '../src/types';
import {SCENE_CATALOG} from '../src/explorer/scene-catalog';
import {collectionWordUrl,selectIllustratedCharacters,selectIllustratedLessons} from '../src/explorer/illustrated-lessons';

const lessons=JSON.parse(readFileSync(new URL('../public/data/lessons.json',import.meta.url),'utf8')) as Lesson[];
const characters=JSON.parse(readFileSync(new URL('../public/data/characters.json',import.meta.url),'utf8')) as Record<string,Character>;

test('the growing collection admits only authored illustrations while preserving the opening demo sequence',()=>{
  const before=JSON.stringify(lessons);
  const selected=selectIllustratedLessons(lessons);
  assert.equal(lessons.length,1000);
  assert.equal(collectionWordUrl('森'),'?view=collection&word=%E6%A3%AE');
  assert.equal(selected.length,SCENE_CATALOG.length);
  assert.deepEqual(selected.slice(0,3).map(lesson=>lesson.word),['休','清','晴']);
  assert.equal(new Set(selected.map(lesson=>lesson.id)).size,selected.length);
  assert.deepEqual(new Set(selected.map(lesson=>lesson.word)),new Set(SCENE_CATALOG.map(scene=>scene.word)));
  assert.equal(JSON.stringify(lessons),before);
  const missing=new Set(SCENE_CATALOG.map(scene=>scene.word));
  assert.deepEqual(selectIllustratedLessons(lessons.filter(lesson=>!missing.has(lesson.word))),[]);
});

test('collection character selection retains source data and only the selected reuse links',()=>{
  const selected=selectIllustratedLessons(lessons);
  const subset=selectIllustratedCharacters(characters,selected);
  const ids=new Set(selected.map(lesson=>lesson.id));
  assert.deepEqual(new Set(Object.keys(subset)),new Set(selected.flatMap(lesson=>lesson.characters)));
  for(const [glyph,character] of Object.entries(subset)){
    assert.ok(character.usages.every(id=>ids.has(id)));
    assert.deepEqual({...character,usages:characters[glyph].usages},characters[glyph]);
  }
  assert.throws(()=>selectIllustratedCharacters({},selected),/writing is unavailable/);
});
