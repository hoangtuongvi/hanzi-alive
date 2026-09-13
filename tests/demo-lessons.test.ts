import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {DEMO_WORDS, demoWordUrl, getDemoWord, isDemoWord, selectDemoCharacters, selectDemoLessons} from '../src/explorer/demo-lessons';
import type {Character, GeometryData, Lesson} from '../src/types';

const readData = <T,>(name:string):T => JSON.parse(readFileSync(new URL(`../public/data/${name}`, import.meta.url), 'utf8')) as T;
const sourceLessons = readData<Lesson[]>('lessons.json');
const sourceCharacters = readData<Record<string, Character>>('characters.json');
const demoLessons = readData<Lesson[]>('demo-lessons.json');
const demoCharacters = readData<Record<string, Character>>('demo-characters.json');

test('the served demo contains exactly 休, 清, 晴 in order with original lesson provenance', () => {
  assert.deepEqual(DEMO_WORDS, ['休', '清', '晴']);
  assert.deepEqual(demoLessons.map(lesson => lesson.word), ['休', '清', '晴']);
  assert.deepEqual(demoLessons, selectDemoLessons(sourceLessons));
  assert.equal(sourceLessons.length, 1000);
  const sourceSnapshot = JSON.stringify(sourceLessons);
  assert.deepEqual(selectDemoLessons([...sourceLessons].reverse()), demoLessons);
  assert.equal(JSON.stringify(sourceLessons), sourceSnapshot);
});

test('demo characters retain source metadata and geometry while excluding unrelated usage links', () => {
  assert.deepEqual(Object.keys(demoCharacters), ['休', '清', '晴']);
  assert.deepEqual(demoCharacters, selectDemoCharacters(sourceCharacters, sourceLessons));
  const allowedIds = new Set(demoLessons.map(lesson => lesson.id));
  for (const [glyph, character] of Object.entries(demoCharacters)) {
    assert.ok(character.usages.every(id => allowedIds.has(id)), glyph);
    assert.deepEqual({...character, usages:sourceCharacters[glyph].usages}, sourceCharacters[glyph], glyph);
    const geometry = JSON.parse(readFileSync(new URL(`../public${character.geometryUrl}`, import.meta.url), 'utf8')) as GeometryData;
    assert.equal(geometry.character, glyph);
    assert.ok(geometry.strokes.length > 0, glyph);
  }
  assert.equal(Object.keys(sourceCharacters).length, 919);
});

test('valid demo deep links retain their selected word and canonicalize consistently', () => {
  for (const word of DEMO_WORDS) {
    assert.equal(isDemoWord(word), true);
    assert.equal(getDemoWord(`?view=theatre&word=${encodeURIComponent(word)}`), word);
    assert.equal(getDemoWord(`?word=${word}`), word);
    const canonical = demoWordUrl(word);
    assert.equal(canonical, `?view=theatre&word=${encodeURIComponent(word)}`);
    assert.equal(demoWordUrl(getDemoWord(canonical)), canonical);
  }
});

test('retired routes and unsupported words cannot restore the full library', () => {
  for (const query of [
    '', '?view=library', '?view=library&word=清', '?view=practice&word=晴',
    '?view=results&word=休', '?view=other&word=清', '?view=theatre&word=情',
    '?view=theatre&word=林', '?word=w0006', '?word=', '?word=%FF',
  ]) {
    assert.equal(getDemoWord(query), '休', query);
    assert.equal(demoWordUrl(getDemoWord(query)), '?view=theatre&word=%E4%BC%91', query);
  }
  for (const unsupported of sourceLessons.filter(lesson => !isDemoWord(lesson.word))) {
    assert.equal(getDemoWord(`?view=theatre&word=${encodeURIComponent(unsupported.word)}`), '休');
    assert.equal(demoWordUrl(unsupported.word), '?view=theatre&word=%E4%BC%91');
  }
});

test('incomplete demo data fails clearly instead of exposing fallback corpus entries', () => {
  assert.throws(() => selectDemoLessons(sourceLessons.filter(lesson => lesson.word !== '清')), /清 lesson/);
  const {晴:omitted, ...remainingCharacters} = sourceCharacters;
  assert.ok(omitted);
  assert.throws(() => selectDemoCharacters(remainingCharacters, demoLessons), /晴 writing/);
});
