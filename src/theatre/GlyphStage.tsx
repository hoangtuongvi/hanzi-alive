import {useEffect,useMemo,useState} from 'react';
import type {GeometryData} from '../types';
import type {GlyphStageProps,VisualPart} from './types';
import './glyphs.css';

const geometryCache=new Map<string,Promise<GeometryData>>();
function geometryAt(url:string):Promise<GeometryData> {
  if(!geometryCache.has(url)) {
    const request=fetch(url).then(response=>{
      if(!response.ok) throw new Error('Stroke source unavailable');
      return response.json() as Promise<GeometryData>;
    }).catch(error=>{geometryCache.delete(url);throw error;});
    geometryCache.set(url,request);
  }
  return geometryCache.get(url)!;
}
const clamp=(value:number)=>Math.min(1,Math.max(0,value));
const ease=(value:number)=>{const p=clamp(value);return p*p*(3-2*p);};
interface Segment {part:VisualPart;indices:number[];geometry:GeometryData;center:[number,number];neutral:boolean;}

function segmentCenter(geometry:GeometryData,indices:number[]):[number,number] {
  const points=indices.flatMap(index=>geometry.medians[index]??[]);
  if(!points.length) return [512,450];
  const xs=points.map(point=>point[0]),ys=points.map(point=>900-point[1]);
  return [(Math.min(...xs)+Math.max(...xs))/2,(Math.min(...ys)+Math.max(...ys))/2];
}

export default function GlyphStage({lesson,characters,progress,highlight}:GlyphStageProps) {
  const glyphs=Array.from(lesson.word);
  const geometryKey=glyphs.map(glyph=>characters[glyph]?.geometryUrl??'').join('|');
  const [loaded,setLoaded]=useState<{key:string;data:GeometryData[]}|null>(null);
  const [failed,setFailed]=useState<string|null>(null);
  useEffect(()=>{
    let active=true;
    setFailed(null);
    const urls=geometryKey.split('|');
    if(urls.some(url=>!url)) {setFailed(geometryKey);return;}
    Promise.all(urls.map(geometryAt)).then(data=>{if(active)setLoaded({key:geometryKey,data});}).catch(()=>{if(active)setFailed(geometryKey);});
    return ()=>{active=false;};
  },[geometryKey]);
  const segments=useMemo(()=>{
    if(loaded?.key!==geometryKey) return [];
    const result:Segment[]=[];
    loaded.data.forEach((geometry,characterIndex)=>{
      const used=new Set<number>();
      lesson.parts.filter(part=>part.characterIndex===characterIndex).forEach(part=>{
        const indices=geometry.strokes.flatMap((_,index)=>part.sourceGroup===null||geometry.groups[index]===part.sourceGroup?[index]:[]);
        indices.forEach(index=>used.add(index));
        if(indices.length)result.push({part,indices,geometry,center:segmentCenter(geometry,indices),neutral:false});
      });
      const remaining=geometry.strokes.flatMap((_,index)=>used.has(index)?[]:[index]);
      if(remaining.length)result.push({part:{glyph:'',image:'Unassigned strokes',color:'#77786e',characterIndex,sourceGroup:-1},indices:remaining,geometry,center:segmentCenter(geometry,remaining),neutral:true});
    });
    return result;
  },[loaded,geometryKey,lesson]);
  const reveal=ease((progress-.43)/.13);
  const join=ease((progress-.75)/.25);
  const active=progress>=.43;
  const labelOpacity=1-ease((progress-.77)/.12);
  const ordinaryCount=segments.filter(segment=>!segment.neutral).length;
  let ordinaryIndex=0;
  return <svg className="theatre-glyph-stage" viewBox="0 0 900 500" role="img" aria-label={`${lesson.word}: ${lesson.parts.map(part=>`${part.glyph}, ${part.image}`).join('; ')}`} style={{opacity:reveal}} aria-hidden={!active}>
    <title>{lesson.word}: sourced writing, separated into {glyphs.length>1?'characters':'elements'}</title>
    {loaded?.key!==geometryKey&&active&&<text className="theatre-glyph-loading" x="450" y="250" textAnchor="middle">{failed===geometryKey?'The stroke view could not load. Try reloading the lesson.':'Loading the writing…'}</text>}
    {segments.map((segment,index)=>{
      const {part,indices,geometry,center,neutral}=segment;
      const slot=neutral?ordinaryCount:ordinaryIndex++;
      const separatedX=neutral||ordinaryCount<=1?450:280+slot*(340/(ordinaryCount-1));
      const separatedY=neutral?355:225;
      const scale=.32;
      const combinedX=glyphs.length===1?450:450+(part.characterIndex-(glyphs.length-1)/2)*265;
      const combinedY=250;
      const fromX=separatedX-center[0]*scale,fromY=separatedY-center[1]*scale;
      const toX=combinedX-512*scale,toY=combinedY-450*scale;
      const x=fromX+(toX-fromX)*join,y=fromY+(toY-fromY)*join;
      const selected=highlight===part.glyph||highlight===part.image;
      const muted=!!highlight&&!selected&&!neutral;
      return <g key={`${part.characterIndex}-${part.sourceGroup}-${index}`} data-glyph={part.glyph} data-source-group={part.sourceGroup??'whole'}>
        {selected&&<ellipse cx={separatedX+(combinedX-separatedX)*join} cy={225} rx="135" ry="155" fill={part.color} opacity=".09"/>}
        <g transform={`translate(${x} ${y}) scale(${scale})`} opacity={muted?.35:1}>
          <g transform="translate(0 900) scale(1 -1)" fill={part.color}>
            {indices.map(strokeIndex=><path key={strokeIndex} d={geometry.strokes[strokeIndex]} data-stroke={strokeIndex}/>)}
          </g>
        </g>
        <g opacity={labelOpacity}>
          <text x={separatedX} y={407} className="theatre-glyph-name" textAnchor="middle" fill={part.color}>{part.image}</text>
          {neutral&&<text x={separatedX} y={430} className="theatre-glyph-source" textAnchor="middle">shown intact, without an assigned image</text>}
        </g>
      </g>;
    })}
    <g opacity={ease((progress-.91)/.09)}><text x="450" y="433" textAnchor="middle" className="theatre-glyph-caption">{glyphs.length===1?'The images become one character.':'The characters become one word.'}</text></g>
  </svg>;
}
