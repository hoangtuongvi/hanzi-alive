import {useEffect,useMemo,useRef,useState} from 'react';
import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import type {Character,GeometryData,Lesson} from '../types';
import {disposeObject,lessonParts,makeGlyph,makeModernWord,type GlyphLabel} from './geometry';
import {createMeaningModel,type SceneLabel} from './scenes';
import {blendExplorerPoses,easeTransition,explorerPose,TRANSITION_DURATION} from './transitions';
import {layoutBreakdownCallouts,layoutCallouts,type ScreenBounds,type ScreenPoint} from './callout-layout';

interface ExplorerStageProps {
  lesson:Lesson;
  characters:Record<string,Character>;
  progress:number;
  show3D:boolean;
  resetKey:number;
  onReady?:(ready:boolean)=>void;
}
interface Label {key:string;glyph:string;image:string;color:string;modern?:GlyphLabel;scene?:SceneLabel;}
const neutralColor=new THREE.Color(0xe5e8d8);
const sceneLabelDirections:Record<string,ScreenPoint[]>={
  '休':[{x:-1,y:0},{x:1,y:-.3}],
  '清':[{x:-1,y:0},{x:1,y:-.5}],
  '晴':[{x:1,y:-.35},{x:1,y:.1}],
};

export default function ExplorerStage({lesson,characters,progress,show3D,resetKey,onReady}:ExplorerStageProps){
  const host=useRef<HTMLDivElement>(null);
  const renderHost=useRef<HTMLDivElement>(null);
  const labelsRef=useRef(new Map<string,HTMLDivElement>());
  const linesRef=useRef(new Map<string,SVGPathElement>());
  const dotsRef=useRef(new Map<string,SVGCircleElement>());
  const leaders=useRef<SVGSVGElement>(null);
  const controlsRef=useRef<OrbitControls|null>(null);
  const wakeRef=useRef<(()=>void)|null>(null);
  const stateRef=useRef({progress,show3D,onReady});stateRef.current={progress,show3D,onReady};
  const [status,setStatus]=useState<'loading'|'ready'|'error'>('loading');
  const [error,setError]=useState('');
  const [labels,setLabels]=useState<Label[]>([]);
  const [retry,setRetry]=useState(0);
  const parts=useMemo(()=>lessonParts(lesson,characters),[lesson,characters]);
  const geometryKey=lesson.characters.map(character=>characters[character]?.geometryUrl??'').join('|');

  const concealed=progress<=.001&&!show3D;
  useEffect(()=>{
    const canvas=host.current?.querySelector('canvas');
    if(canvas)canvas.tabIndex=concealed||status!=='ready'?-1:0;
    wakeRef.current?.();
  },[progress,show3D,concealed,status]);
  useEffect(()=>{controlsRef.current?.reset();wakeRef.current?.();},[resetKey]);
  useEffect(()=>{
    const viewport=renderHost.current;if(!viewport)return;
    let disposed=false,frameId=0,lastTime:number|null=null,ready=false;
    let renderer:THREE.WebGLRenderer|undefined,controls:OrbitControls|undefined,observer:ResizeObserver|undefined;
    let scene:THREE.Scene|undefined,camera:THREE.PerspectiveCamera|undefined,root:THREE.Group|undefined;
    let content:THREE.Group[]=[];
    let sceneGroup:THREE.Group|undefined,activeLabels:Label[]=[];
    const geometryCorners=new WeakMap<THREE.BufferGeometry,THREE.Vector3[]>();
    let pose=explorerPose(stateRef.current.progress,lesson.word==='休',true,stateRef.current.show3D);
    let fromPose=pose,targetPose=pose,targetKey='',elapsed=TRANSITION_DURATION;
    const abort=new AbortController();
    const motion=matchMedia('(prefers-reduced-motion: reduce)');
    let reducedMotion=motion.matches;
    const cameraMaterials:THREE.Material[]=[];
    setStatus('loading');setError('');setLabels([]);stateRef.current.onReady?.(false);

    function setOpacity(group:THREE.Group,opacity:number){
      group.visible=opacity>.001;
      group.traverse(object=>{
        if(!(object instanceof THREE.Mesh))return;
        for(const material of Array.isArray(object.material)?object.material:[object.material]){
          const baseOpacity=material.userData.baseOpacity??1;
          material.opacity=opacity*baseOpacity;material.depthWrite=opacity>.98&&baseOpacity>=.98;
        }
      });
    }
    function updateModel(){
      if(!root||!camera||!viewport||!host.current)return false;
      const {weights,explode}=pose;
      content.forEach((group,index)=>{
        const opacity=weights[index];setOpacity(group,opacity);
        group.position.z=-.26*(1-opacity);
        group.rotation.y=(index%2?.12:-.12)*(1-opacity);
        group.scale.setScalar(.94+.06*opacity);
        if(index===0)group.traverse(object=>{
          if(!(object instanceof THREE.Mesh))return;
          const offset=object.userData.offset as THREE.Vector3|undefined;
          if(offset){
            object.position.copy(offset).multiplyScalar(explode);
            object.position.z+=((object.userData.stroke as number)-2.5)*.065*explode;
            object.rotation.y=Math.sin(explode*Math.PI)*(offset.x<0?-.12:.12);
          }
          const material=object.material as THREE.MeshStandardMaterial;
          material.color.copy(neutralColor);
          if(object.userData.color)material.color.lerp(object.userData.color,explode);
        });
      });
      if(sceneGroup){
        const opacity=weights[4];setOpacity(sceneGroup,opacity);
        sceneGroup.rotation.y=.16*(1-opacity);
        sceneGroup.position.z=-.22*(1-opacity);
        sceneGroup.scale.setScalar(.95+.05*opacity);
      }
      root.updateMatrixWorld(true);camera.updateMatrixWorld();
      const width=viewport.clientWidth,height=viewport.clientHeight;
      const project=(point:THREE.Vector3):ScreenPoint=>{const p=point.project(camera!);return {x:(p.x+1)/2*width,y:(1-p.y)/2*height};};
      const obstacles:ScreenBounds[]=[];
      // Each visible mesh is an obstacle, leaving real gaps between elements available.
      // traverseVisible also excludes every descendant of a hidden model or object.
      root.traverseVisible(object=>{
        if(!(object instanceof THREE.Mesh))return;
        const materials=Array.isArray(object.material)?object.material:[object.material];
        if(!materials.some(material=>material.visible&&material.opacity>.001))return;
        let corners=geometryCorners.get(object.geometry);
        if(!corners){
          if(!object.geometry.boundingBox)object.geometry.computeBoundingBox();
          const bounds=object.geometry.boundingBox;if(!bounds||bounds.isEmpty())return;
          corners=[];
          for(const x of [bounds.min.x,bounds.max.x])for(const y of [bounds.min.y,bounds.max.y])for(const z of [bounds.min.z,bounds.max.z])corners.push(new THREE.Vector3(x,y,z));
          geometryCorners.set(object.geometry,corners);
        }
        const projected=corners.map(corner=>project(corner.clone().applyMatrix4(object.matrixWorld)));
        const obstacle={left:Math.min(...projected.map(p=>p.x)),right:Math.max(...projected.map(p=>p.x)),top:Math.min(...projected.map(p=>p.y)),bottom:Math.max(...projected.map(p=>p.y))};
        if(obstacle.right>=0&&obstacle.left<=width&&obstacle.bottom>=0&&obstacle.top<=height)obstacles.push(obstacle);
      });
      const measures=activeLabels.flatMap((label,index)=>{
        const element=labelsRef.current.get(label.key);if(!element)return [];
        let modernPoint:ScreenPoint|undefined,scenePoint:ScreenPoint|undefined;
        if(label.modern&&content[0]){
          const anchor=label.modern.anchor.clone().addScaledVector(label.modern.offset,explode);
          modernPoint=project(content[0].localToWorld(anchor));
        }
        if(label.scene&&sceneGroup)scenePoint=project(sceneGroup.localToWorld(label.scene.anchor.clone()));
        const a=modernPoint??scenePoint??{x:width/2,y:height/2},b=scenePoint??a;
        const sceneWeight=scenePoint?weights[4]/Math.max(.001,weights[0]+weights[4]):0;
        const glyphDirection={x:index===0?-1:1,y:0},sceneDirection=sceneLabelDirections[lesson.word]?.[index]??glyphDirection;
        const preferred={x:glyphDirection.x+(sceneDirection.x-glyphDirection.x)*sceneWeight,y:sceneDirection.y*sceneWeight};
        return [{key:label.key,anchor:{x:a.x+(b.x-a.x)*sceneWeight,y:a.y+(b.y-a.y)*sceneWeight},width:element.offsetWidth||110,height:element.offsetHeight||38,preferred}];
      });
      const sceneMix=weights[4]/Math.max(.001,weights[0]+weights[4]);
      const bottomLabels=layoutBreakdownCallouts(measures,width,height);
      const nearbyLabels=sceneMix>0?new Map(layoutCallouts(measures,width,height,obstacles).map(label=>[label.key,label])):null;
      // Written parts keep a stable baseline. Only the illustration uses
      // element-following callouts, with the same eased blend as the models.
      const placements=bottomLabels.map(bottom=>{
        const nearby=nearbyLabels?.get(bottom.key);if(!nearby)return bottom;
        return {...nearby,x:bottom.x+(nearby.x-bottom.x)*sceneMix,y:bottom.y+(nearby.y-bottom.y)*sceneMix};
      });
      for(const placement of placements){
        const element=labelsRef.current.get(placement.key),line=linesRef.current.get(placement.key);if(!element||!line)continue;
        const point=placement;
        const opacity=placement.visible?pose.labels:0;
        element.style.left=point.x+'px';element.style.top=point.y+'px';element.style.opacity=String(opacity);
        element.setAttribute('aria-hidden',String(opacity<.5||(!stateRef.current.show3D&&stateRef.current.progress<=.001)));
        const dx=placement.anchor.x-point.x,dy=placement.anchor.y-point.y;
        const edgeRatio=Math.max(Math.abs(dx)/(placement.width/2+4),Math.abs(dy)/(placement.height/2+4));
        const end=edgeRatio>0?{x:point.x+dx/edgeRatio,y:point.y+dy/edgeRatio}:{x:point.x,y:point.y-placement.height/2-4};
        line.setAttribute('d',`M ${placement.anchor.x} ${placement.anchor.y} L ${end.x} ${end.y}`);
        const connectorOpacity=opacity*sceneMix;
        line.style.opacity=String(connectorOpacity*.64);
        const dot=dotsRef.current.get(placement.key);
        if(dot){dot.setAttribute('cx',String(placement.anchor.x));dot.setAttribute('cy',String(placement.anchor.y));dot.style.opacity=String(connectorOpacity*.8);}
      }
    }
    function frame(time:number){
      frameId=0;
      if(disposed||!ready||document.hidden||!renderer||!scene||!camera||!controls)return;
      const requestedKey=`${stateRef.current.progress}|${stateRef.current.show3D}`;
      if(requestedKey!==targetKey){
        targetKey=requestedKey;fromPose=pose;
        targetPose=explorerPose(stateRef.current.progress,content.length>1,!!sceneGroup,stateRef.current.show3D);
        elapsed=0;lastTime=time;
      }
      const dt=lastTime===null?0:Math.min(time-lastTime,100);lastTime=time;
      elapsed=reducedMotion?TRANSITION_DURATION:Math.min(TRANSITION_DURATION,elapsed+dt);
      pose=blendExplorerPoses(fromPose,targetPose,easeTransition(elapsed/TRANSITION_DURATION));
      const moving=controls.update();
      updateModel();renderer.render(scene,camera);
      if((moving||elapsed<TRANSITION_DURATION)&&!frameId)frameId=requestAnimationFrame(frame);
    }
    function wake(){if(!disposed&&ready&&!document.hidden&&!frameId)frameId=requestAnimationFrame(frame);}
    wakeRef.current=wake;
    function fail(message:string){
      if(disposed)return;
      ready=false;cancelAnimationFrame(frameId);frameId=0;
      if(renderer)renderer.domElement.style.visibility='hidden';
      setStatus('error');setError(message);setLabels([]);stateRef.current.onReady?.(false);
    }
    function contextLost(event:Event){event.preventDefault();fail('The 3D view paused. Restore the view to continue exploring.');}
    function cameraFocus(){
      if(renderer){renderer.domElement.style.outline='2px solid #ebb08d';renderer.domElement.style.outlineOffset='-3px';}
    }
    function cameraBlur(){if(renderer)renderer.domElement.style.outline='';}
    function cameraKey(event:KeyboardEvent){
      if(!ready||!camera||!controls||document.activeElement!==renderer?.domElement||event.altKey||event.ctrlKey||event.metaKey)return;
      if(!stateRef.current.show3D&&stateRef.current.progress<=.001)return;
      if(!['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','+','=','-','_','0'].includes(event.key))return;
      event.preventDefault();
      if(event.key==='0'){controls.reset();wake();return;}
      const offset=camera.position.clone().sub(controls.target);
      const spherical=new THREE.Spherical().setFromVector3(offset),step=Math.PI/18;
      if(event.key==='ArrowLeft')spherical.theta-=step;
      if(event.key==='ArrowRight')spherical.theta+=step;
      if(event.key==='ArrowUp')spherical.phi-=step;
      if(event.key==='ArrowDown')spherical.phi+=step;
      if(event.key==='+'||event.key==='=')spherical.radius*=.9;
      if(event.key==='-'||event.key==='_')spherical.radius/= .9;
      spherical.theta=THREE.MathUtils.clamp(spherical.theta,controls.minAzimuthAngle,controls.maxAzimuthAngle);
      spherical.phi=THREE.MathUtils.clamp(spherical.phi,controls.minPolarAngle,controls.maxPolarAngle);
      spherical.radius=THREE.MathUtils.clamp(spherical.radius,controls.minDistance,controls.maxDistance);
      camera.position.copy(controls.target).add(new THREE.Vector3().setFromSpherical(spherical));
      camera.lookAt(controls.target);controls.update();wake();
    }
    function visibility(){lastTime=null;if(document.hidden){cancelAnimationFrame(frameId);frameId=0;}else wake();}
    function motionChange(){reducedMotion=motion.matches;if(controls)controls.enableDamping=!reducedMotion;wake();}
    function resize(){
      if(!renderer||!camera||!viewport)return;
      const width=viewport.clientWidth,height=viewport.clientHeight;if(!width||!height)return;
      const oldAspect=camera.aspect,aspect=width/height;
      const oldFit=Math.max(1,1/oldAspect),newFit=Math.max(1,1/aspect);
      if(controls){
        camera.position.sub(controls.target).multiplyScalar(newFit/oldFit).add(controls.target);
        controls.minDistance=7*newFit;controls.maxDistance=16*newFit;
        controls.position0.set(.5,.3,10.4).multiplyScalar(newFit);
        controls.target0.set(0,0,0);controls.zoom0=1;
      }else camera.position.multiplyScalar(newFit/oldFit);
      camera.aspect=aspect;camera.updateProjectionMatrix();
      if(leaders.current&&host.current)leaders.current.setAttribute('viewBox',`0 0 ${width} ${host.current.clientHeight}`);
      renderer.setSize(width,height,false);wake();
    }
    async function loadText(url:string){
      const response=await fetch(url,{signal:abort.signal});if(!response.ok)throw new Error('A writing source could not load.');
      return response.text();
    }
    async function init(){
      try{
        renderer=new THREE.WebGLRenderer({antialias:true,alpha:true,powerPreference:'low-power'});
        renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.outputColorSpace=THREE.SRGBColorSpace;
        renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.65;
        Object.assign(renderer.domElement.style,{display:'block',position:'absolute',inset:'0',width:'100%',height:'100%',touchAction:'none',cursor:'grab'});
        renderer.domElement.setAttribute('aria-label',`${lesson.word}: interactive three dimensional model. Arrow keys rotate; plus and minus zoom; zero resets the view. You can also drag to rotate and scroll to zoom.`);
        renderer.domElement.setAttribute('role','img');
        renderer.domElement.setAttribute('aria-roledescription','interactive 3D view');
        renderer.domElement.tabIndex=-1;
        renderer.domElement.addEventListener('keydown',cameraKey);
        renderer.domElement.addEventListener('focus',cameraFocus);
        renderer.domElement.addEventListener('blur',cameraBlur);
        renderer.domElement.addEventListener('webglcontextlost',contextLost);
        viewport!.prepend(renderer.domElement);
        scene=new THREE.Scene();camera=new THREE.PerspectiveCamera(35,1,.1,100);camera.position.set(.5,.3,10.4);
        controls=new OrbitControls(camera,renderer.domElement);controlsRef.current=controls;
        controls.enableDamping=!reducedMotion;controls.dampingFactor=.075;controls.enablePan=false;
        controls.minDistance=7;controls.maxDistance=16;controls.minPolarAngle=Math.PI*.25;controls.maxPolarAngle=Math.PI*.75;
        controls.maxAzimuthAngle=Math.PI*.8;controls.minAzimuthAngle=-Math.PI*.8;controls.addEventListener('change',wake);
        scene.add(new THREE.HemisphereLight(0xe8eddc,0x25392a,2.3));
        const key=new THREE.DirectionalLight(0xffdfc0,4.8);key.position.set(-4,6,8);scene.add(key);
        const fill=new THREE.DirectionalLight(0xb9daed,3);fill.position.set(5,1,3);scene.add(fill);
        const rim=new THREE.DirectionalLight(0xddd6b0,3.4);rim.position.set(1,3,-4);scene.add(rim);
        root=new THREE.Group();root.rotation.y=-.17;root.rotation.x=.03;scene.add(root);
        const ringPoints=Array.from({length:128},(_,index)=>{const a=index/128*Math.PI*2;return new THREE.Vector3(Math.cos(a)*3.15,Math.sin(a)*3.15,-.9);});
        const ringMaterial=new THREE.LineBasicMaterial({color:0x809176,transparent:true,opacity:.14});cameraMaterials.push(ringMaterial);
        scene.add(new THREE.LineLoop(new THREE.BufferGeometry().setFromPoints(ringPoints),ringMaterial));
        const lines:THREE.Vector3[]=[];
        for(let i=0;i<4;i++){const a=i*Math.PI/2;lines.push(new THREE.Vector3(Math.cos(a)*2.99,Math.sin(a)*2.99,-.9),new THREE.Vector3(Math.cos(a)*3.3,Math.sin(a)*3.3,-.9));}
        const tickMaterial=new THREE.LineBasicMaterial({color:0x9ca992,transparent:true,opacity:.25});cameraMaterials.push(tickMaterial);
        scene.add(new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(lines),tickMaterial));
        resize();
        observer=new ResizeObserver(resize);observer.observe(viewport!);
        document.addEventListener('visibilitychange',visibility);motion.addEventListener('change',motionChange);
        const urls=geometryKey.split('|');if(urls.some(url=>!url))throw new Error('This character has no available writing source.');
        const [data,historical]=await Promise.all([
          Promise.all(urls.map(async url=>JSON.parse(await loadText(url)) as GeometryData)),
          lesson.word==='休'?Promise.all(['seal','bronze','oracle'].map(name=>loadText(`/reference/assets/xiu-${name}.svg`))):Promise.resolve([]),
        ]);
        if(disposed)return;
        const modern=makeModernWord(data,parts);content=[modern.group];root.add(modern.group);
        for(const svg of historical){const group=makeGlyph(svg);content.push(group);root.add(group);}
        const meaning=createMeaningModel(lesson.word,parts);sceneGroup=meaning?.group;
        if(sceneGroup)root.add(sceneGroup);
        activeLabels=parts.map((part,index)=>({...part,key:`part-${index}`,modern:modern.labels[index],scene:meaning?.labels[index]}));
        pose=explorerPose(stateRef.current.progress,content.length>1,!!sceneGroup,stateRef.current.show3D);
        fromPose=pose;targetPose=pose;targetKey=`${stateRef.current.progress}|${stateRef.current.show3D}`;elapsed=TRANSITION_DURATION;
        setLabels(activeLabels);setStatus('ready');ready=true;stateRef.current.onReady?.(true);wake();
      }catch(reason){
        if(!disposed&&!(reason instanceof DOMException&&reason.name==='AbortError'))fail('The 3D view could not load. You can still read the character’s story and explore its stages.');
      }
    }
    void init();
    return ()=>{
      disposed=true;ready=false;abort.abort();cancelAnimationFrame(frameId);observer?.disconnect();
      document.removeEventListener('visibilitychange',visibility);motion.removeEventListener('change',motionChange);
      controls?.removeEventListener('change',wake);controls?.dispose();controlsRef.current=null;wakeRef.current=null;
      if(scene)disposeObject(scene);cameraMaterials.forEach(material=>material.dispose());
      if(renderer){
        renderer.domElement.removeEventListener('webglcontextlost',contextLost);
        renderer.domElement.removeEventListener('keydown',cameraKey);
        renderer.domElement.removeEventListener('focus',cameraFocus);
        renderer.domElement.removeEventListener('blur',cameraBlur);
        renderer.dispose();renderer.domElement.remove();
      }
      labelsRef.current.clear();linesRef.current.clear();dotsRef.current.clear();
    };
  },[lesson.id,lesson.word,geometryKey,parts,retry]);

  useEffect(()=>{wakeRef.current?.();},[labels]);
  return <div ref={host} className="explorer-three-stage" aria-hidden={concealed} inert={concealed} style={{position:'absolute',inset:0,overflow:'hidden',pointerEvents:concealed?'none':undefined}}>
    <div ref={renderHost} className="explorer-render-area" style={{position:'absolute',inset:0,overflow:'hidden'}}/>
    {status!=='ready'&&<div className="explorer-three-loading" role="status" style={{position:'absolute',inset:0,display:'flex',alignItems:'center',justifyContent:'center',flexDirection:'column',gap:14,textAlign:'center',padding:30}}>
      <span style={{fontFamily:'serif',fontSize:100,color:'#e5e8d8',lineHeight:1.2}}>{lesson.word}</span>
      <p style={{maxWidth:320,color:'#9da69b',fontSize:14}}>{status==='error'?error:'Preparing your 3D explorer…'}</p>
      {status==='error'&&<button className="quiet" type="button" onClick={()=>setRetry(value=>value+1)}>Restore 3D view ↻</button>}
    </div>}
    <svg ref={leaders} className="explorer-callout-lines" aria-hidden="true" style={{position:'absolute',inset:0,width:'100%',height:'100%',pointerEvents:'none',overflow:'hidden'}}>
      {labels.map(label=><path key={label.key} ref={element=>{if(element)linesRef.current.set(label.key,element);else linesRef.current.delete(label.key);}} fill="none" stroke={label.color} strokeWidth="1" strokeLinecap="round" style={{opacity:0}}/>)}
      {labels.map(label=><circle key={`${label.key}-anchor`} ref={element=>{if(element)dotsRef.current.set(label.key,element);else dotsRef.current.delete(label.key);}} r="2" fill={label.color} style={{opacity:0}}/>)}
    </svg>
    {labels.map(label=><div key={label.key} ref={element=>{if(element)labelsRef.current.set(label.key,element);else labelsRef.current.delete(label.key);}} className="explorer-callout" aria-hidden="true" style={{position:'absolute',display:'flex',alignItems:'center',justifyContent:'center',gap:8,minWidth:0,maxWidth:'calc((100% - 48px) / 2)',color:label.color,transform:'translate(-50%, -50%)',opacity:0,pointerEvents:'none'}}>
      <span className="explorer-callout-glyph">{label.glyph}</span><span className="explorer-callout-name">{label.image}</span>
    </div>)}
  </div>;
}
