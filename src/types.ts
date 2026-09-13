export type Strategy='mnemonic'|'structure'|'phonetic'|'compound'|'context'|'grammar'|'borrowing'|'idiom';
export interface ElementCue {glyph:string;image:string;}
export interface CharacterMnemonic {image:string;elements:ElementCue[];story:string;kind:"parts"|"outline";}
export interface Lesson { memoryElements:ElementCue[];memorySearch:string;mnemonicKind:"parts"|"outline"|"word";contentRevision:string; id:string;word:string;traditional:string;pinyin:string;meaning:string;dictionaryMeanings:string[];story:string;connection:string;strategy:Strategy;stressTest:boolean;level:number|null;characters:string[];syllables:number;readings:string[];status:'draft';source:string;formSource:string;author:string; }
export interface Character { mnemonic:CharacterMnemonic; character:string;definition:string;pinyin:string[];radical:string;decomposition:string;components:string[];etymology:{type:string;hint?:string;semantic?:string;phonetic?:string}|null;usages:string[];geometryUrl:string;tree:unknown; }
export interface GeometryData {character:string;strokes:string[];groups:number[];medians:number[][][];matches:(number[]|null)[];}
export interface Manifest {version:string;words:number;uniqueCharacters:number;characterOccurrences:number;geometryCoverage:number;missingCharacters:string[];partialStrokeMappings:string[];stressCases:number;strategies:Record<string,number>;syllables:Record<string,number>;draftStories:number;independentlyReviewed:number;selection:string;sourceRevisions:{repo:string;sha:string;url:string}[];}
export interface Review { contentRevision?:string; verdict:'helpful'|'misleading'|'unclear';note:string;updatedAt:string; }
export interface Trial {lessonId:string;condition:'story'|'definition';correct:boolean;selected:string;responseMs:number;studyMs:number;}
export interface Session { focus?:"elements"|"meaning";contentRevision?:string;id:string;date:string;trials:Trial[];}
export interface Saved {version:1;reviews:Record<string,Review>;sessions:Session[];}
export const STRATEGIES:Record<Strategy,string>={mnemonic:'Element story',structure:'Shape connection',phonetic:'Sound + meaning',compound:'Word connection',context:'Meaning in context',grammar:'Grammar in context',borrowing:'Borrowed word',idiom:'Expression'};
export const COLORS=['#d37c53','#315e4b','#c29a39'];
export function componentColor(c:string,i:number){return ({'亻':'#d37c53','人':'#d37c53','扌':'#d37c53','手':'#d37c53','青':'#315e4b','绿':'#315e4b','⺼':'#8b86ad','月':'#8b86ad','木':'#315e4b','林':'#315e4b','艹':'#315e4b','氵':'#527f91','水':'#527f91','日':'#c29a39','忄':'#b97568','心':'#b97568'} as Record<string,string>)[c]||COLORS[Array.from(c).reduce((n,g)=>n+g.codePointAt(0)!,0)%COLORS.length];}
