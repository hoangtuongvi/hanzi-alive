import {lazy, Suspense, useMemo, useState} from 'react';
import {ArrowLeft, ArrowRight, ArrowUpRight} from 'lucide-react';
import type {Character, Lesson} from '../types';
import {getFocusedSteps, getFocusedStory, nextFocusedWord} from './focused-flow';
import {usePlaybackTimer} from './usePlaybackTimer';
import './focused.css';

const ExplorerStage=lazy(()=>import('./ExplorerStage'));
interface Props {
  lessons:Lesson[];
  characters:Record<string,Character>;
  word:string;
  onWordChange:(word:string)=>void;
}

function FocusedLesson({lesson,characters,run}:{lesson:Lesson;characters:Record<string,Character>;run:number}){
  const steps=useMemo(()=>getFocusedSteps(lesson),[lesson]);
  const lessonRun=`${lesson.id}:${run}`;
  const [playback,setPlayback]=useState({lessonRun,stepIndex:0});
  const [ready,setReady]=useState(false);
  // Restart the lesson without unmounting its canvas and graphics context.
  if(playback.lessonRun!==lessonRun){
    setPlayback({lessonRun,stepIndex:0});
    setReady(false);
  }
  const step=steps[playback.lessonRun===lessonRun?playback.stepIndex:0];
  const isWord=step.key==='word';
  const isStory=step.key==='story'||step.key==='recap';
  const isScene=step.key==='visual'||isStory;
  const isHistory=!!step.period;
  const story=getFocusedStory(lesson);

  // Preload 3D during the opening word. Later phases count only visible,
  // ready time, so loading or switching tabs cannot skip them.
  usePlaybackTimer(`${lessonRun}:${step.key}`,step.durationMs,isWord||ready,()=>{
    setPlayback(current=>current.lessonRun===lessonRun?{...current,stepIndex:Math.min(current.stepIndex+1,steps.length-1)}:current);
  });

  return <section className="focused-content" aria-label={`${lesson.word} lesson`} data-step={isScene?'visual':step.key} data-phase={step.key} data-history={isHistory} data-story-visible={isStory}>
      <div className={`focused-visual ${isWord?'focused-visual-concealed':''}`} aria-hidden={isWord} inert={isWord}>
        <div className="focused-model" aria-label={isHistory?`${lesson.word} ${step.label} form`:`${lesson.word} visualization`}>
          <div className="focused-pulse" key={step.progress} aria-hidden="true"/>
          <Suspense fallback={<div className="focused-loading" role="status">Preparing the scene…</div>}>
            <ExplorerStage lesson={lesson} characters={characters} progress={step.progress} show3D={true} resetKey={0} onReady={setReady}/>
          </Suspense>
        </div>

        <div className="focused-caption" aria-live="polite" aria-atomic="true">
          <p className={`focused-story ${isStory?'focused-enter':'focused-story-reserve'}`} aria-hidden={!isStory}>{lesson.word==='清'?<>Only in <em>clear water</em> can you see the <em className="focused-green">green grass.</em></>:story}</p>
          {isHistory&&<div className="focused-history-note focused-enter" key={step.key}><p className="focused-history-era">{step.key==='modern'?'Today':`${step.label} script`}</p><p>{step.period}{step.source&&<><span aria-hidden="true"> · </span><a href={step.source} target="_blank" rel="noreferrer">Source <ArrowUpRight size={12}/></a></>}</p></div>}
        </div>
      </div>

      <div className={`focused-word ${isWord?'':'focused-word-concealed'}`} aria-hidden={!isWord}>
        <h1 className="focused-hanzi" lang="zh-Hans" data-length={lesson.characters.length}>{lesson.word}</h1>
        <p className="focused-pinyin">{lesson.pinyin}</p>
      </div>
    </section>;
}

export default function Explorer({lessons,characters,word,onWordChange}:Props){
  const lesson=lessons.find(item=>item.word===word)||lessons[0];
  const [run,setRun]=useState(0);
  const move=(direction:1|-1)=>{
    const following=nextFocusedWord(lessons,lesson.id,direction);
    if(following)onWordChange(following.word);
    setRun(value=>value+1);
  };
  return <main className="focused-study">
    <FocusedLesson lesson={lesson} characters={characters} run={run}/>
    <nav className="focused-controls" aria-label="Words">
      <button className="focused-back" onClick={()=>move(-1)}><ArrowLeft size={18}/>Back</button>
      <button className="focused-next" onClick={()=>move(1)}>Next<ArrowRight size={18}/></button>
    </nav>
  </main>;
}
