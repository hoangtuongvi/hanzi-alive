import type {Character, Lesson} from '../types';

export const DEMO_WORDS = ['休', '清', '晴'] as const;
export type DemoWord = typeof DEMO_WORDS[number];

export function isDemoWord(word:string|null|undefined):word is DemoWord {
  return DEMO_WORDS.some(item => item === word);
}

/** Unsupported words and the retired library routes open the first demo word. */
export function getDemoWord(search:string):DemoWord {
  const params = new URLSearchParams(search);
  const view = params.get('view');
  const word = params.get('word');
  return (view === null || view === 'theatre') && isDemoWord(word) ? word : DEMO_WORDS[0];
}

export function demoWordUrl(word:string):string {
  return `?view=theatre&word=${encodeURIComponent(isDemoWord(word) ? word : DEMO_WORDS[0])}`;
}

/** Explicit selection keeps both the demo order and the source corpus intact. */
export function selectDemoLessons(lessons:readonly Lesson[]):Lesson[] {
  return DEMO_WORDS.map(word => {
    const lesson = lessons.find(item => item.word === word);
    if (!lesson) throw new Error(`The ${word} lesson is unavailable.`);
    return lesson;
  });
}

export function selectDemoCharacters(characters:Record<string, Character>, lessons:readonly Lesson[]):Record<string, Character> {
  const selected = selectDemoLessons(lessons);
  const ids = new Set(selected.map(lesson => lesson.id));
  const glyphs = new Set(selected.flatMap(lesson => lesson.characters));
  return Object.fromEntries([...glyphs].map(glyph => {
    const character = characters[glyph];
    if (!character?.geometryUrl) throw new Error(`The ${glyph} writing is unavailable.`);
    return [glyph, {...character, usages:character.usages.filter(id => ids.has(id))}];
  }));
}
