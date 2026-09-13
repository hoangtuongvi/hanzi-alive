import type {Lesson} from '../types';
import {THEATRE_LESSONS} from '../theatre/lessons';
import {getExplorerContent, historyAvailable} from './content';

export interface FocusedStep {
  key:'word'|'parts'|'visual'|'story'|'oracle'|'bronze'|'seal'|'modern'|'recap';
  label:string;
  progress:number;
  durationMs:number|null;
  period?:string;
  source?:string;
}

/** Timed phases share one scene; a null duration holds until Next word. */
export function getFocusedSteps(lesson:Lesson):FocusedStep[] {
  const hasHistory=historyAvailable(lesson);
  const steps:FocusedStep[] = [
    {key:'word', label:'The word', progress:50, durationMs:2000},
    {key:'parts', label:'The parts', progress:200 / 6, durationMs:3000},
    {key:'visual', label:'Visualize', progress:100 / 6, durationMs:3000},
    {key:'story', label:'Visualize', progress:100 / 6, durationMs:hasHistory?8000:null},
  ];
  if (!hasHistory) return steps;

  const scripts = [
    {key:'oracle', label:'Oracle', stage:6, progress:100},
    {key:'bronze', label:'Bronze', stage:5, progress:500 / 6},
    {key:'seal', label:'Seal', stage:4, progress:400 / 6},
  ] as const;
  for (const {key, label, stage, progress} of scripts) {
    const {period, source} = getExplorerContent(lesson, stage);
    steps.push({key, label, progress, period, source, durationMs:3500});
  }
  steps.push({key:'modern', label:'Today', period:'Modern form', progress:50, durationMs:3500});
  steps.push({key:'recap', label:'Visualize', progress:100 / 6, durationMs:null});
  return steps;
}

/** Keep this mnemonic copy local to the focused lesson. */
export function getFocusedStory(lesson:Lesson):string {
  if (lesson.word === '清') return 'Only in clear water can you see the green grass.';
  return THEATRE_LESSONS.find(item => item.word === lesson.word)?.story || lesson.story;
}

/** Move between words in the supplied sequence, wrapping at either end. */
export function nextFocusedWord(lessons:readonly Lesson[], currentId:string, direction:1|-1=1):Lesson|undefined {
  if (lessons.length === 0) return undefined;
  const currentIndex = lessons.findIndex(lesson => lesson.id === currentId);
  if (currentIndex < 0) return lessons[0];
  return lessons[(currentIndex + direction + lessons.length) % lessons.length];
}
