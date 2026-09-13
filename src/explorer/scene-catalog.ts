import catalog from './scene-catalog.json';
import type {Lesson} from '../types';

export interface SceneDefinition {
  word:string;
  scene:string;
  format:'blender'|'procedural';
  asset?:string;
  anchors?:string[];
  history:boolean;
}

export const SCENE_CATALOG:readonly SceneDefinition[]=catalog as SceneDefinition[];
const byWord=new Map(SCENE_CATALOG.map(scene=>[scene.word,scene]));
export function getSceneDefinition(word:string):SceneDefinition|undefined {return byWord.get(word);}

/** Only authored illustrations count as scenes; extruded writing is a separate tier. */
export function getVisualCoverage(lessons:readonly Pick<Lesson,'word'>[]){
  const words=new Set(lessons.map(lesson=>lesson.word));
  const scenes=[...words].flatMap(word=>byWord.get(word)??[]);
  return {
    words:words.size,
    blenderScenes:scenes.filter(scene=>scene.format==='blender').length,
    proceduralScenes:scenes.filter(scene=>scene.format==='procedural').length,
    illustratedScenes:scenes.length,
    writingOnly:words.size-scenes.length,
    historicalLessons:scenes.filter(scene=>scene.history).length,
  };
}
