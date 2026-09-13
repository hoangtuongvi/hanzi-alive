import {useEffect,useRef,useState} from 'react';
import * as THREE from 'three';
import {SVGLoader} from 'three/addons/loaders/SVGLoader.js';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {RotateCcw,Box,Layers,Move,Expand} from 'lucide-react';
import type {Character,GeometryData} from './types';
import {COLORS,componentColor} from './types';
const cache=new Map<string,GeometryData>();
export function FlatGlyph({data,split=0,label,className='',colors=COLORS}:{data:GeometryData;split?:number;label:string;className?:string;colors?:string[]}){
 return <svg className={className} viewBox="-210 -210 1444 1444" role="img" aria-label={label}><g transform="translate(0 900) scale(1 -1)">{data.strokes.map((d,i)=>{const group=data.groups[i];return <path key={i} d={d} fill={colors[group]||'#8d9083'} transform={`translate(${group===0?-150*split:group>0?150*split:0},0)`}/>;})}</g></svg>;
}
function Scene({data,split,reset,onFail,onReady,colors}:{data:GeometryData;split:number;reset:number;onFail:()=>void;onReady:()=>void;colors:string[]}){
 const host=useRef<HTMLDivElement>(null), sceneControl=useRef<{groups:THREE.Group[];offsets:THREE.Vector3[];controls:OrbitControls;camera:THREE.PerspectiveCamera;root:THREE.Group;render:()=>void}|null>(null);const splitRef=useRef(split);splitRef.current=split;
 useEffect(()=>{
  if(!host.current)return;let renderer:THREE.WebGLRenderer|undefined,controls:OrbitControls|undefined,frame=0,observer:ResizeObserver|undefined;let scene:THREE.Scene|undefined;
  const container=host.current;let disposed=false;
  try{
   renderer=new THREE.WebGLRenderer({antialias:true,alpha:true});renderer.setPixelRatio(Math.min(window.devicePixelRatio,2));renderer.setClearColor(0x000000,0);renderer.outputColorSpace=THREE.SRGBColorSpace;container.append(renderer.domElement);renderer.domElement.setAttribute('aria-label','Rotatable 3D Chinese character');renderer.domElement.setAttribute('role','img');
   scene=new THREE.Scene();const camera=new THREE.PerspectiveCamera(36,1,.1,100);camera.position.set(.2,.35,8.8);
   scene.add(new THREE.HemisphereLight(0xfff9e9,0x78927e,2.6));const sun=new THREE.DirectionalLight(0xffffff,3);sun.position.set(-3,6,7);scene.add(sun);const fill=new THREE.DirectionalLight(0xc1dab8,1.3);fill.position.set(3,-2,-4);scene.add(fill);
   const root=new THREE.Group();root.rotation.set(-.08,-.19,.01);scene.add(root);
   const groupIds=[...new Set(data.groups)];const groups=groupIds.map(()=>new THREE.Group());const loader=new SVGLoader();
   for(let i=0;i<data.strokes.length;i++){
    const parsed=loader.parse(`<svg xmlns="http://www.w3.org/2000/svg"><path d="${data.strokes[i]}"/></svg>`);
    for(const path of parsed.paths){for(const shape of SVGLoader.createShapes(path)){
     const geom=new THREE.ExtrudeGeometry(shape,{depth:27,bevelEnabled:true,bevelSegments:2,steps:1,bevelSize:4,bevelThickness:4,curveSegments:5});geom.translate(-512,-388,-13.5);geom.scale(.0048,.0048,.0048);
     const mesh=new THREE.Mesh(geom,new THREE.MeshStandardMaterial({color:colors[data.groups[i]]||'#8d9083',roughness:.45,metalness:.06}));groups[groupIds.indexOf(data.groups[i])].add(mesh);
    }}
   }
   groups.forEach(g=>root.add(g));
   const offsets=groups.map((g,j)=>{if(groupIds[j]===-1||groups.length===1)return new THREE.Vector3();const box=new THREE.Box3().setFromObject(g);const center=box.getCenter(new THREE.Vector3());center.z=0;return center.length()>.05?center.normalize().multiplyScalar(.78):new THREE.Vector3(j%2?1:-1,0,0);});
   controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=true;controls.dampingFactor=.1;controls.enablePan=false;controls.minDistance=6;controls.maxDistance=13;controls.rotateSpeed=.65;controls.enableZoom=false;
   const reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
   const render=()=>{if(renderer&&scene)renderer.render(scene,camera);};
   sceneControl.current={groups,offsets,controls,camera,root,render};
   const resize=()=>{const {width,height}=container.getBoundingClientRect();if(!width||!height||!renderer)return;renderer.setSize(width,height);camera.aspect=width/height;camera.updateProjectionMatrix();render();};
   observer=new ResizeObserver(resize);observer.observe(container);resize();
   const tick=()=>{if(disposed)return;groups.forEach((g,j)=>{const target=offsets[j].clone().multiplyScalar(splitRef.current);if(reduced)g.position.copy(target);else g.position.lerp(target,.18);});controls?.update();render();frame=requestAnimationFrame(tick);};tick();onReady();
   renderer.domElement.addEventListener('webglcontextlost',onFail);
  }catch(error){console.error('3D character unavailable',error);onFail();}
  return()=>{disposed=true;cancelAnimationFrame(frame);observer?.disconnect();controls?.dispose();scene?.traverse(o=>{if(o instanceof THREE.Mesh){o.geometry.dispose();const mats=Array.isArray(o.material)?o.material:[o.material];mats.forEach(m=>m.dispose());}});renderer?.domElement.removeEventListener('webglcontextlost',onFail);renderer?.dispose();renderer?.domElement.remove();sceneControl.current=null;};
 },[data,onFail,onReady]);
 useEffect(()=>{const s=sceneControl.current;if(s){s.controls.reset();s.camera.position.set(.2,.35,8.8);s.root.rotation.set(-.08,-.19,.01);s.controls.update();s.render();}},[reset]);
 return <div className="three-host" ref={host}/>;
}
// Stable callbacks keep the geometry alive while sliders and parent state change.
export default function GlyphViewer({character,onData}:{character:Character;onData?:(g:GeometryData)=>void}){
 const [data,setData]=useState<GeometryData|null>(null),[error,setError]=useState(''),[mode,setMode]=useState<'3d'|'2d'>('3d'),[split,setSplit]=useState(0),[reset,setReset]=useState(0),[ready,setReady]=useState(false);
 const callbacks=useRef({onFail:()=>{setError('3D is unavailable on this device. The stroke view remains fully usable.');setMode('2d');},onReady:()=>setReady(true)});
 useEffect(()=>{let active=true;setData(null);setError('');setReady(false);setSplit(0);const cached=cache.get(character.character);if(cached){setData(cached);onData?.(cached);return;}
 fetch(character.geometryUrl).then(r=>{if(!r.ok)throw Error('Could not load the stroke data.');return r.json();}).then((g:GeometryData)=>{cache.set(character.character,g);if(active){setData(g);onData?.(g);}}).catch(e=>{if(active)setError(e.message);});return()=>{active=false;};},[character.character,character.geometryUrl]);
 const groups=data?[...new Set(data.groups.filter(g=>g>=0))]:[];const canSplit=groups.length>1;const partial=data?.groups.some(g=>g<0)&&character.components.length>0;
 return <div className="glyph-viewer">
  <div className="viewer-top"><span className="micro">CHARACTER STUDIO</span><div className="segmented"><button aria-pressed={mode==='3d'} onClick={()=>{if(mode!=='3d'){setMode('3d');setReady(false);}}}><Box size={14}/>3D</button><button aria-pressed={mode==='2d'} onClick={()=>setMode('2d')}><Layers size={14}/>2D</button></div></div>
  <div className="glyph-stage">
   <div className="stage-ring ring-a"/><div className="stage-ring ring-b"/>
   {data&&<div className={`flat-layer ${mode==='3d'&&ready?'hidden':''}`}><FlatGlyph data={data} split={split} label={character.character} colors={character.components.map(componentColor)}/></div>}
   {!data&&<span className="fallback-char" lang="zh-Hans">{character.character}</span>}
   {data&&mode==='3d'&&<Scene data={data} split={split} reset={reset} onFail={callbacks.current.onFail} onReady={callbacks.current.onReady} colors={character.components.map(componentColor)}/>}
   <span className="stage-caption"><Move size={13}/>{mode==='3d'?'Drag to turn the character':'Real stroke outlines'}</span>
   <button className="reset icon-button" title="Reset view" aria-label="Reset view" onClick={()=>{setReset(r=>r+1);setSplit(0);}}><RotateCcw size={16}/></button>
  </div>
  <div className="split-control"><label htmlFor="split">{canSplit?'Separate the components':'Whole character'}<span>{canSplit?`${Math.round(split*100)}%`:'No complete split available'}</span></label><input id="split" aria-label="Separate components" type="range" min="0" max="1" step="0.01" value={split} disabled={!canSplit} onChange={e=>setSplit(Number(e.target.value))}/><div className="range-labels"><span>Together</span><Expand size={12}/><span>Apart</span></div></div>
  {partial&&<p className="viewer-note">Gray strokes have no complete component mapping in the source.</p>}{error&&<p className="viewer-note" role="status">{error}</p>}
 </div>;
}
