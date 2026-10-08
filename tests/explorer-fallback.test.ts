import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createElement} from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import type {Character,Lesson} from '../src/types';
import ExplorerFallback from '../src/explorer/ExplorerFallback';
import {lessonParts} from '../src/explorer/geometry';
import {getScenePoster} from '../src/explorer/scene-catalog';

const lessons=JSON.parse(readFileSync(new URL('../public/data/lessons.json',import.meta.url),'utf8')) as Lesson[];
const characters=JSON.parse(readFileSync(new URL('../public/data/characters.json',import.meta.url),'utf8')) as Record<string,Character>;
const lesson=(word:string)=>lessons.find(item=>item.word===word)!;
const render=(item:Lesson,progress=100/6)=>renderToStaticMarkup(createElement(ExplorerFallback,{
  lesson:item,characters,progress,recoveryState:'error',message:'Use the browser’s Reload button to restore 3D.',
}));

test('all lessons can present their own poster and memory cues without a browser or graphics context',()=>{
  for(const item of lessons){
    const html=render(item),parts=lessonParts(item,characters);
    assert.ok(html.includes(`src="${getScenePoster(item.word)}"`),item.word);
    assert.equal((html.match(/class="explorer-fallback-part"/g)??[]).length,parts.length,item.word);
    for(const part of parts)assert.ok(html.includes(renderToStaticMarkup(createElement('span',null,part.image))),`${item.word}: ${part.image}`);
    assert.ok(html.includes('Still view · 3D is temporarily unavailable'),item.word);
    assert.doesNotMatch(html,/<canvas\b/);
  }
});

test('only the lesson with sourced history shows the matching historical outline',()=>{
  for(const [progress,script] of [[100,'oracle'],[500/6,'bronze'],[400/6,'seal']] as const){
    const html=render(lesson('休'),progress);
    assert.ok(html.includes(`src="/reference/assets/xiu-${script}.svg"`));
    assert.ok(html.includes(`alt="休: ${script} writing"`));
    assert.doesNotMatch(html,/aria-label="Memory elements"/);
    assert.doesNotMatch(render(lesson('大'),progress),/xiu-/);
  }
});

test('a lesson without a poster still has readable writing, cues and recovery help',()=>{
  const html=render({...lesson('大'),id:'missing-scene',word:'No scene'});
  assert.ok(html.includes('data-poster-state="missing"'));
  assert.ok(html.includes('lang="zh-Hans">No scene</span>'));
  assert.ok(html.includes('aria-label="Memory elements"'));
  assert.ok(html.includes('You can keep learning in this view.'));
  assert.doesNotMatch(html,/<img\b|<canvas\b/);
});
