import {useEffect,useMemo,useState} from 'react';
import type {Character,GeometryData,Lesson} from '../types';
import {lessonParts,partStrokeIndices} from './geometry';
import {getScenePoster} from './scene-catalog';
import {explorerPose} from './transitions';

interface Props {
  lesson:Lesson;
  characters:Record<string,Character>;
  progress:number;
  recoveryState:'error'|'recovering';
  message:string;
  onReady?:(ready:boolean)=>void;
}

/** A complete lesson presentation using ordinary images and sourced SVG paths. */
export default function ExplorerFallback({lesson,characters,progress,recoveryState,message,onReady}:Props){
  const parts=useMemo(()=>lessonParts(lesson,characters),[lesson,characters]);
  const poster=getScenePoster(lesson.word);
  const [posterState,setPosterState]=useState<'loading'|'ready'|'missing'>(poster?'loading':'missing');
  const [geometry,setGeometry]=useState<GeometryData[]|null>(null);
  const pose=explorerPose(progress,lesson.word==='休',true,true);
  const stage=pose.weights.indexOf(Math.max(...pose.weights));
  const historical=['','seal','bronze','oracle'][stage];
  const showPoster=stage===4&&posterState!=='missing';

  useEffect(()=>{
    const abort=new AbortController();
    Promise.all(lesson.characters.map(async glyph=>{
      const url=characters[glyph]?.geometryUrl;
      if(!url)throw new Error('Missing writing source');
      const response=await fetch(url,{signal:abort.signal});
      if(!response.ok)throw new Error('Writing source could not load');
      return response.json() as Promise<GeometryData>;
    })).then(data=>{if(!abort.signal.aborted)setGeometry(data);}).catch(()=>{
      // Even a writing-source failure must leave the word, cues and story usable.
      if(!abort.signal.aborted)setGeometry(null);
    });
    return()=>abort.abort();
  },[lesson,characters]);

  useEffect(()=>{
    // Failed still downloads also unblock playback: text and cues remain useful.
    if(posterState!=='loading')onReady?.(true);
  },[posterState,recoveryState,onReady]);

  return <div className="explorer-fallback" data-scene-source="poster" data-poster-state={posterState} aria-label={`${lesson.word} illustrated lesson`}>
    <div className="explorer-fallback-picture">
      {poster&&<img className="explorer-fallback-poster" src={poster} alt={`${lesson.word}: still illustration rendered from its Blender scene`}
        hidden={!showPoster} onLoad={()=>setPosterState('ready')} onError={()=>setPosterState('missing')}/>}
      {historical?<img className="explorer-fallback-history" src={`/reference/assets/xiu-${historical}.svg`} alt={`${lesson.word}: ${historical} writing`}/>
        :!showPoster&&(geometry?<svg className="explorer-fallback-writing" viewBox={`0 0 ${1024*geometry.length} 1024`} role="img" aria-label={`${lesson.word}: sourced written strokes`}>
          {geometry.map((source,characterIndex)=>{
            const colors=new Map<number,string>();
            if(pose.explode>.5)parts.filter(part=>part.characterIndex===characterIndex).forEach(part=>{
              for(const stroke of partStrokeIndices(source,part))colors.set(stroke,part.color);
            });
            return <g key={characterIndex} transform={`translate(${characterIndex*1024} 900) scale(1 -1)`}>
              {source.strokes.map((path,index)=><path key={index} d={path} fill={colors.get(index)??'#e5e8d8'}/>)}
            </g>;
          })}
        </svg>:<span className="explorer-fallback-word" lang="zh-Hans">{lesson.word}</span>)}
    </div>
    {!historical&&<div className="explorer-fallback-parts" aria-label="Memory elements">
      {parts.map((part,index)=><span key={index} className="explorer-fallback-part" style={{color:part.color}}>
        <span className="explorer-callout-glyph">{part.glyph}</span><span>{part.image}</span>
      </span>)}
    </div>}
    <details className="explorer-fallback-help">
      <summary>Still view · 3D is temporarily unavailable</summary>
      <p>{message} You can keep learning in this view.</p>
    </details>
  </div>;
}
