import {getSceneDefinition} from '../src/explorer/scene-catalog';
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {getExplorerContent, getExplorerParts, historyAvailable} from '../src/explorer/content';
import {THEATRE_LESSONS} from '../src/theatre/lessons';
import type {Lesson} from '../src/types';

const lessons = JSON.parse(readFileSync(new URL('../public/data/lessons.json', import.meta.url), 'utf8')) as Lesson[];

test('the explorer preserves every lesson’s ordered memory images, pronunciation and selected meaning', () => {
  for (const lesson of lessons) {
    assert.deepEqual(getExplorerParts(lesson).map(({glyph, image}) => ({glyph, image})), lesson.memoryElements.map(part=>({...part,image:getSceneDefinition(lesson.word)?.mnemonicImages?.[part.glyph]??part.image})), lesson.word);
    const meaning = getExplorerContent(lesson, 3);
    assert.ok(meaning.description.includes(lesson.word), lesson.word);
    assert.ok(meaning.description.includes(lesson.pinyin), lesson.word);
    assert.ok(meaning.description.includes(lesson.meaning), lesson.word);
  }
});

test('only the supplied 休 historical forms carry script provenance', () => {
  const rest = lessons.find(lesson => lesson.word === '休')!;
  assert.equal(historyAvailable(rest), true);
  for (const [index, script] of ['seal', 'bronze', 'oracle'].entries()) {
    const content = getExplorerContent(rest, index + 4);
    assert.equal(content.source, `https://commons.wikimedia.org/wiki/File:%E4%BC%91-${script}.svg`);
    assert.doesNotMatch(content.description, /No sourced/);
  }
  assert.match(getExplorerContent(rest, 4).note, /not a dated Qin inscription/);
});

test('missing historical sources stay explicit for every other lesson', () => {
  for (const lesson of lessons.filter(item => item.word !== '休')) {
    assert.equal(historyAvailable(lesson), false, lesson.word);
    for (let stage = 4; stage <= 6; stage++) {
      const content = getExplorerContent(lesson, stage);
      assert.equal(content.source, undefined, lesson.word);
      assert.match(content.description, /^No sourced (seal|bronze|oracle) form in this collection yet\.$/, lesson.word);
      assert.doesNotMatch(content.period, /Han|Qin|Zhou|Shang|BCE|BC|century/, lesson.word);
    }
  }
});

test('lessons without illustrated scenes describe the writing available in their 3D view', () => {
  const illustratedWords = new Set(THEATRE_LESSONS.map(lesson => lesson.word));
  for (const lesson of lessons.filter(item => !illustratedWords.has(item.word))) {
    const content = getExplorerContent(lesson, 1);
    assert.match(content.description, /written shapes/);
    assert.doesNotMatch(content.description, /Turn the scene|Move around the person/);
    assert.match(getExplorerContent(lesson, 0).title, /Picture the story/);
  }
});

test('part colors remain readable against the explorer background', () => {
  const luminance = (hex:string):number => {
    const linear = [1, 3, 5].map(index => {
      const channel = parseInt(hex.slice(index, index + 2), 16) / 255;
      return channel <= .04045 ? channel / 12.92 : ((channel + .055) / 1.055) ** 2.4;
    });
    return linear[0] * .2126 + linear[1] * .7152 + linear[2] * .0722;
  };
  const background = luminance('#101412');
  const colors = new Set(lessons.flatMap(lesson => getExplorerParts(lesson).map(part => part.color)));
  for (const color of colors) {
    assert.ok((luminance(color) + .05) / (background + .05) >= 4.5, color);
  }
});
