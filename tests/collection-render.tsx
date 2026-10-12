/// <reference types="vite/client" />
import {useEffect,useState} from 'react';
import {createRoot} from 'react-dom/client';
import type {WebGLRenderer} from 'three';
import type {Character,Lesson} from '../src/types';
import ExplorerStage from '../src/explorer/ExplorerStage';
import {getSceneDefinition} from '../src/explorer/scene-catalog';
import '../src/styles.css';
import '../src/explorer/focused.css';

if(!import.meta.env.DEV)throw new Error('The collection graphics audit is development-only.');

// Use the application's supported reduced-motion path to inspect settled
// writing and illustration frames without spending time on 1,251 transitions.
const originalMatchMedia=window.matchMedia;
window.matchMedia=query=>query==='(prefers-reduced-motion: reduce)'
  ?{matches:true,media:query,addEventListener(){},removeEventListener(){}} as unknown as MediaQueryList
  :originalMatchMedia.call(window,query);

type Sample={word:string;phase:string;geometries:number;textures:number;programs:number;triangles:number;calls:number;};
let current={word:'',phase:'scene'},lastFrame:Sample|undefined;
let renders=0,contexts=0,contextLosses=0,runtimeError='';
let seenContexts=new WeakSet<WebGLRenderingContext|WebGL2RenderingContext>();
function captureFrame(renderer:WebGLRenderer){
  const gl=renderer.getContext();
  if(!seenContexts.has(gl)){seenContexts.add(gl);contexts++;}
  const error=gl.getError();
  if(error!==gl.NO_ERROR)throw new Error(`WebGL error ${error} while rendering ${current.word} ${current.phase}`);
  const {memory,programs,render:frame}=renderer.info;
  lastFrame={...current,geometries:memory.geometries,textures:memory.textures,programs:programs?.length??0,triangles:frame.triangles,calls:frame.calls};
  renders++;
}
document.addEventListener('webglcontextlost',()=>{contextLosses++;},true);
window.addEventListener('error',event=>{runtimeError=event.message;});
window.addEventListener('unhandledrejection',event=>{runtimeError=String(event.reason);});

function Audit({lessons,characters}:{lessons:Lesson[];characters:Record<string,Character>}){
  const [running,setRunning]=useState(false),[index,setIndex]=useState(0),[phase,setPhase]=useState('scene'),[ready,setReady]=useState(false);
  const [report,setReport]=useState('Ready to render every illustration and every written form.');
  const [samples,setSamples]=useState<Sample[]>([]);
  const lesson=lessons[index%lessons.length];
  current={word:lesson.word,phase};
  useEffect(()=>{
    if(!running)return;
    const timeout=window.setTimeout(()=>{setRunning(false);setReport(`FAIL: ${lesson.word} ${phase} did not render within 20 seconds.`);},20000);
    return()=>clearTimeout(timeout);
  },[running,index,phase,lesson.word]);
  useEffect(()=>{
    if(!running||!ready)return;
    const frameBefore=renders;
    const timer=window.setInterval(()=>{
      const fallback=document.querySelector('.explorer-fallback');
      const canvas=document.querySelector<HTMLCanvasElement>('canvas');
      if(runtimeError||contextLosses||fallback||contexts!==1){
        setRunning(false);setReport(`FAIL: ${runtimeError||`${lesson.word}: losses=${contextLosses}, contexts=${contexts}, fallback=${!!fallback}`}`);return;
      }
      // A phase change must actually reach the GPU before the audit advances.
      if(!lastFrame||lastFrame.word!==lesson.word||lastFrame.phase!==phase||(phase==='writing'&&renders===frameBefore))return;
      if(canvas?.dataset.sceneSource!=='blender'||canvas.dataset.sceneAsset!==getSceneDefinition(lesson.word)?.asset){
        setRunning(false);setReport(`FAIL: ${lesson.word} did not use its own Blender scene.`);return;
      }
      if(lastFrame.triangles<=0){setRunning(false);setReport(`FAIL: ${lesson.word} ${phase} rendered no triangles.`);return;}
      const completed=[...samples,lastFrame];
      setSamples(completed);
      if(index===lessons.length&&phase==='writing'){
        const first=completed[1],last=completed.at(-1)!;
        const stable=['geometries','textures','programs'].every(key=>first[key as keyof Sample]===last[key as keyof Sample]);
        setReport(JSON.stringify({status:stable?'PASS':'FAIL: GPU resources grew after a complete cycle',lessons:lessons.length,renderedPhases:completed.length,contexts,contextLosses,runtimeError,first,last,maxTriangles:Math.max(...completed.map(s=>s.triangles)),maxGeometries:Math.max(...completed.map(s=>s.geometries))},null,2));
        setRunning(false);
      }else if(phase==='scene'){
        setPhase('writing');
      }else{
        setReady(false);setPhase('scene');setIndex(value=>value+1);
      }
    },120);
    return()=>clearInterval(timer);
  },[running,ready,index,phase,lesson.word,lessons.length,samples]);
  return <main style={{maxWidth:1100,margin:'auto',padding:20,color:'#e5e8d8'}}>
    <h1>Full collection graphics audit</h1>
    <p>Actual Blender and written-stroke rendering on one persistent canvas, followed by a return to the first word to check GPU resource cleanup.</p>
    <button onClick={()=>{
      seenContexts=new WeakSet();contexts=0;contextLosses=0;runtimeError='';renders=0;lastFrame=undefined;
      setIndex(0);setPhase('scene');setSamples([]);setReady(false);setRunning(true);setReport('Running');
    }} disabled={running}>Audit all 1,251 lessons</button>
    <button onClick={()=>{setRunning(false);setReport('Stopped');}} disabled={!running}>Stop audit</button>
    <p role="status">{running?`${Math.min(index+1,lessons.length)} / ${lessons.length} · ${lesson.word} · ${phase} · ${samples.length} verified phases`:report}</p>
    <div style={{position:'relative',height:480}}>
      {running&&<ExplorerStage lesson={lesson} characters={characters} progress={phase==='scene'?100/6:50} show3D={true} resetKey={0} onReady={setReady} onFrame={captureFrame}/>}
    </div>
    <pre aria-label="Audit report" style={{whiteSpace:'pre-wrap'}}>{report}</pre>
  </main>;
}

const [lessons,characters]=await Promise.all([
  fetch('/data/lessons.json').then(r=>r.json() as Promise<Lesson[]>),
  fetch('/data/characters.json').then(r=>r.json() as Promise<Record<string,Character>>),
]);
createRoot(document.getElementById('root')!).render(<Audit lessons={lessons} characters={characters}/>);
