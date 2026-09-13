import type {Character,Lesson} from '../types';
import {DEMO_WORDS} from './demo-lessons';
import {getSceneDefinition} from './scene-catalog';

/** The growing collection admits authored scenes only; a story alone is not an illustration. */
export function selectIllustratedLessons(lessons:readonly Lesson[]):Lesson[]{
  const illustrated=lessons.filter(lesson=>getSceneDefinition(lesson.word));
  const opening=DEMO_WORDS.flatMap(word=>illustrated.find(lesson=>lesson.word===word)??[]);
  return [...opening,...illustrated.filter(lesson=>!DEMO_WORDS.some(word=>word===lesson.word))];
}

export function selectIllustratedCharacters(characters:Record<string,Character>,lessons:readonly Lesson[]):Record<string,Character>{
  const ids=new Set(lessons.map(lesson=>lesson.id));
  return Object.fromEntries([...new Set(lessons.flatMap(lesson=>lesson.characters))].map(glyph=>{
    const character=characters[glyph];
    if(!character?.geometryUrl)throw new Error(`The ${glyph} writing is unavailable.`);
    return [glyph,{...character,usages:character.usages.filter(id=>ids.has(id))}];
  }));
}

export function collectionWordUrl(word:string):string{return `?view=collection&word=${encodeURIComponent(word)}`;}
