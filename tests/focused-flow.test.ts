import {getSceneDefinition} from '../src/explorer/scene-catalog';
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {getFocusedSteps, getFocusedStory, nextFocusedWord} from '../src/explorer/focused-flow';
import {THEATRE_LESSONS} from '../src/theatre/lessons';
import type {Lesson} from '../src/types';

const lessons = JSON.parse(readFileSync(new URL('../public/data/lessons.json', import.meta.url), 'utf8')) as Lesson[];

test('all 1,000 words have a focused lesson without unavailable-history detours', () => {
  assert.equal(lessons.length, 1000);
  for (const lesson of lessons) {
    const steps = getFocusedSteps(lesson);
    assert.deepEqual(steps.slice(0, 4).map(step => step.key), ['word', 'parts', 'visual', 'story'], lesson.word);
    if (lesson.word !== '休') assert.equal(steps.length, 4, lesson.word);
    assert.ok(getFocusedStory(lesson).trim().length > 0, lesson.word);
  }
});

test('the available evolution moves chronologically from sourced forms to today', () => {
  const rest = lessons.find(lesson => lesson.word === '休')!;
  const evolution = getFocusedSteps(rest).filter(step=>step.period);
  assert.deepEqual(evolution.map(step => step.key), ['oracle', 'bronze', 'seal', 'modern']);
  assert.deepEqual(evolution.map(step => step.progress), [100, 500 / 6, 400 / 6, 50]);
  for (const step of evolution.slice(0, 3)) {
    assert.equal(step.source, `https://commons.wikimedia.org/wiki/File:%E4%BC%91-${step.key}.svg`);
    assert.ok(step.period);
  }
  assert.equal(evolution.at(-1)?.label, 'Today');
});

test('autoplay reveals the story after three seconds on the same visualization', () => {
  for (const lesson of lessons) {
    const steps = getFocusedSteps(lesson);
    assert.equal(steps[0].durationMs, 2000);
    assert.equal(steps[1].durationMs, 3000);
    const scene = steps.find(step=>step.key==='visual')!;
    const story = steps.find(step=>step.key==='story')!;
    assert.equal(scene.durationMs, 3000);
    assert.equal(story.progress, scene.progress, lesson.word);
    assert.equal(story.label, scene.label, lesson.word);
    assert.equal(steps.at(-1)?.durationMs, null, 'Wait for Next word at the end');
    if (lesson.word !== '休') assert.equal(story.durationMs, null);
  }
});

test('sourced history plays once after time to read, then returns to the story scene', () => {
  const steps = getFocusedSteps(lessons.find(lesson=>lesson.word==='休')!);
  assert.equal(steps.find(step=>step.key==='story')?.durationMs, 8000);
  assert.ok(steps.slice(4,-1).every(step=>step.durationMs===3500));
  assert.equal(steps.at(-1)?.key, 'recap');
  assert.equal(steps.at(-1)?.progress, steps[2].progress);
});

test('the clear-water story follows the requested wording without rewriting source lessons', () => {
  const clear = lessons.find(lesson => lesson.word === '清')!;
  const originalCorpusStory = clear.story;
  const curated = THEATRE_LESSONS.find(lesson => lesson.word === '清')!;
  const originalCuratedStory = curated.story;
  assert.equal(getFocusedStory(clear), 'Only in clear water can you see the green grass.');
  assert.equal(clear.story, originalCorpusStory);
  assert.equal(curated.story, originalCuratedStory);

  for (const lesson of lessons.filter(lesson => lesson.word !== '清')) {
    const curatedStory = THEATRE_LESSONS.find(item => item.word === lesson.word)?.story;
    assert.equal(getFocusedStory(lesson), getSceneDefinition(lesson.word)?.story || curatedStory || lesson.story, lesson.word);
  }
});

test('next word reaches every lesson in corpus order and wraps without reordering the corpus', () => {
  const originalIds = lessons.map(lesson => lesson.id);
  let current = lessons[0];
  const visited = new Set([current.id]);
  for (const expected of lessons.slice(1)) {
    const next = nextFocusedWord(lessons, current.id);
    assert.equal(next, expected);
    current = next!;
    visited.add(current.id);
  }
  assert.equal(visited.size, 1000);
  assert.equal(nextFocusedWord(lessons, current.id), lessons[0]);
  assert.deepEqual(lessons.map(lesson => lesson.id), originalIds);
});

test('next word handles missing and minimal corpora', () => {
  assert.equal(nextFocusedWord([], 'missing'), undefined);
  assert.equal(nextFocusedWord(lessons, 'missing'), lessons[0]);
  assert.equal(nextFocusedWord([lessons[0]], lessons[0].id), lessons[0]);
});

test('Back and Next cycle only through the supplied three demo words', () => {
  const demo=['休','清','晴'].map(word=>lessons.find(lesson=>lesson.word===word)!);
  assert.equal(nextFocusedWord(demo,demo[0].id,-1),demo[2]);
  assert.equal(nextFocusedWord(demo,demo[2].id),demo[0]);
  for (const lesson of demo) {
    const next=nextFocusedWord(demo,lesson.id)!;
    assert.equal(nextFocusedWord(demo,next.id,-1),lesson);
  }
  assert.equal(nextFocusedWord([], 'missing', -1),undefined);
  assert.equal(nextFocusedWord(demo,'missing',-1),demo[0]);
});
