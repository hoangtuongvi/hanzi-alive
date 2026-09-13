import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {THEATRE_LESSONS,THEATRE_META,reconstructionChoices} from '../src/theatre/lessons';
import type {Character,GeometryData,Lesson} from '../src/types';

const corpus=JSON.parse(readFileSync(new URL('../public/data/lessons.json',import.meta.url),'utf8')) as Lesson[];
const characters=JSON.parse(readFileSync(new URL('../public/data/characters.json',import.meta.url),'utf8')) as Record<string,Character>;

test('all ten visual lessons preserve the corpus ID, chosen sense and pronunciation',()=>{
  assert.equal(THEATRE_LESSONS.length,10);
  assert.equal(new Set(THEATRE_LESSONS.map(lesson=>lesson.wordId)).size,10);
  for(const lesson of THEATRE_LESSONS){
    const original=corpus.find(candidate=>candidate.id===lesson.wordId);
    assert.ok(original,lesson.word);
    assert.equal(lesson.word,original.word);
    assert.equal(THEATRE_META[lesson.word].meaning,original.meaning);
    assert.equal(THEATRE_META[lesson.word].pinyin,original.pinyin);
    assert.deepEqual(lesson.parts.map(({glyph,image})=>({glyph,image})),original.memoryElements);
  }
});

test('animated pieces cover each sourced stroke exactly once and name real source groups',()=>{
  for(const lesson of THEATRE_LESSONS){
    Array.from(lesson.word).forEach((glyph,characterIndex)=>{
      const character=characters[glyph];
      const geometry=JSON.parse(readFileSync(new URL(`../public${character.geometryUrl}`,import.meta.url),'utf8')) as GeometryData;
      const parts=lesson.parts.filter(part=>part.characterIndex===characterIndex);
      const coverage=geometry.strokes.map(()=>0);
      for(const part of parts){
        if(part.sourceGroup===null)assert.equal(part.glyph,glyph,'whole-character piece must retain source glyph');
        else assert.equal(character.components[part.sourceGroup],part.glyph,`${lesson.word}: sourced component name`);
        const indices=geometry.strokes.flatMap((_,index)=>part.sourceGroup===null||part.sourceGroup===geometry.groups[index]?[index]:[]);
        assert.ok(indices.length>0,`${lesson.word}: empty part`);
        indices.forEach(index=>coverage[index]++);
      }
      assert.ok(coverage.every(count=>count===1),`${lesson.word}: missing or duplicated strokes`);
    });
  }
});

test('the 青 family retains the same green image and color throughout the visual story',()=>{
  const family=THEATRE_LESSONS.filter(lesson=>['清','晴','情','请'].includes(lesson.word));
  assert.equal(family.length,4);
  for(const lesson of family){
    const green=lesson.parts.find(part=>part.glyph==='青');
    assert.equal(green?.image,'green');
    assert.equal(green?.color,'#315e4b');
    assert.match(lesson.story,/green/i);
    assert.ok(lesson.stageCaptions.every(caption=>/green/i.test(caption)),lesson.word);
  }
});

test('each reconstruction prompt has four stable, distinct shapes with one correct answer',()=>{
  const correctPositions=new Set<number>();
  for(const lesson of THEATRE_LESSONS){
    lesson.parts.forEach((part,slot)=>{
      const choices=reconstructionChoices(lesson,slot);
      assert.equal(choices.length,4);
      assert.equal(new Set(choices).size,4);
      assert.equal(choices.filter(glyph=>glyph===part.glyph).length,1);
      assert.deepEqual(choices,reconstructionChoices(lesson,slot));
      correctPositions.add(choices.indexOf(part.glyph));
    });
  }
  assert.equal(correctPositions.size,4,'correct choice positions should vary');
});
