import type {ElementCue} from './types';
import {componentColor} from './types';
export default function MemoryImages({elements,missing=-1,hideLabels=false}:{elements:ElementCue[];missing?:number;hideLabels?:boolean}){
 return <div className="memory-images" aria-label="Memory elements">{elements.map((e,i)=><div className={`memory-image ${i===missing?'missing':''}`} key={`${e.glyph}-${i}`}><span lang="zh-Hans" style={{color:componentColor(e.glyph,i)}}>{i===missing?'?':e.glyph}</span>{!hideLabels&&<small>{i===missing?'Missing image':e.image}</small>}</div>)}</div>;
}
