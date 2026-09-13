import type {Character,Lesson} from '../types';
export type SceneId='rest'|'woods'|'clear'|'sunny'|'emotion'|'invite'|'phone'|'computer'|'parting'|'expert';
export interface VisualPart {glyph:string;image:string;color:string;characterIndex:number;sourceGroup:number|null;}
export interface TheatreLesson {word:string;wordId:string;scene:SceneId;title:string;story:string;action:string;parts:VisualPart[];source:string;stageCaptions:[string,string,string];}
export interface SceneProps {scene:SceneId;progress:number;reducedMotion:boolean;highlight?:string|null;onSelect?:(id:string)=>void;}
export interface GlyphStageProps {lesson:TheatreLesson;characters:Record<string,Character>;progress:number;highlight?:string|null;}
export interface ReconstructionProps {lesson:TheatreLesson;onComplete:()=>void;}
