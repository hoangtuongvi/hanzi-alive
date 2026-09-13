import * as THREE from 'three';
import {SVGLoader} from 'three/addons/loaders/SVGLoader.js';
import type {Character, GeometryData, Lesson} from '../types';
import {THEATRE_LESSONS} from '../theatre/lessons';
import type {VisualPart} from '../theatre/types';
import {getExplorerParts} from './content';

export interface GlyphLabel extends VisualPart {
  anchor: THREE.Vector3;
  offset: THREE.Vector3;
}

export interface ExplorerVisualPart extends VisualPart {
  /** A path in this character's supplied IDS tree. Null means no proven split. */
  sourcePath?:number[]|null;
}
interface SourceNode {glyph?:string;operator?:string;children?:SourceNode[];}

/** Resolve ordered mnemonic cuts against the same tree as the source stroke matches. */
export function mnemonicSourcePaths(tree:unknown,glyphs:string[]):number[][]|null {
  const label=(node:SourceNode):string=>node.glyph??`${node.operator??''}${(node.children??[]).map(label).join('')}`;
  type Cut={next:number;paths:number[][]};
  function cuts(node:SourceNode,path:number[],start:number):Cut[] {
    const found:Cut[]=label(node)===glyphs[start]?[{next:start+1,paths:[path]}]:[];
    if(node.children?.length){
      let choices:Cut[]=[{next:start,paths:[]}];
      node.children.forEach((child,index)=>{
        choices=choices.flatMap(choice=>cuts(child,[...path,index],choice.next).map(cut=>({next:cut.next,paths:[...choice.paths,...cut.paths]})));
      });
      found.push(...choices);
    }
    return found;
  }
  if(!tree||typeof tree!=='object')return null;
  // Do not expand another character's IDS: its stroke order is not a mapping
  // for this occurrence. An unproved split must keep the supplied writing intact.
  return cuts(tree as SourceNode,[],0).find(cut=>cut.next===glyphs.length)?.paths??null;
}

export function lessonParts(lesson:Lesson,characters:Record<string,Character>):ExplorerVisualPart[] {
  const cues=getExplorerParts(lesson);
  const curated=THEATRE_LESSONS.find(item=>item.word===lesson.word);
  if(curated) return curated.parts.map((part,index)=>({...part,...cues[index]}));
  if(lesson.characters.length>1) return cues.map((cue,characterIndex)=>({...cue,characterIndex,sourceGroup:null}));
  const character=characters[lesson.characters[0]];
  if(character?.mnemonic.kind==='outline')return cues.map(cue=>({...cue,characterIndex:0,sourceGroup:null}));
  const paths=mnemonicSourcePaths(character?.tree,cues.map(cue=>cue.glyph));
  return cues.map((cue,index)=>({...cue,
    characterIndex:0,sourceGroup:null,sourcePath:paths?.[index]??null}));
}

/** Unknown or shared strokes remain neutral; no stroke is assigned by visual guesswork. */
export function partStrokeIndices(geometry:GeometryData,part:ExplorerVisualPart):number[] {
  return geometry.strokes.flatMap((_,index)=>{
    if(part.sourcePath===null)return [];
    if(part.sourcePath!==undefined){
      const match=geometry.matches[index];
      return match&&part.sourcePath.every((value,depth)=>match[depth]===value)?[index]:[];
    }
    return part.sourceGroup===null||geometry.groups[index]===part.sourceGroup?[index]:[];
  });
}

/** Extrude only the filled outlines in the supplied writing source. */
export function makeGlyph(svg:string,modern=false):THREE.Group {
  const parsed=new SVGLoader().parse(svg);
  const group=new THREE.Group();
  let pathIndex=0;
  for(const path of parsed.paths){
    for(const shape of SVGLoader.createShapes(path)){
      const geometry=new THREE.ExtrudeGeometry(shape,{
        depth:modern?26:6,bevelEnabled:true,bevelSegments:3,steps:1,
        bevelSize:modern?2.5:.6,bevelThickness:modern?2.5:.6,curveSegments:18,
      });
      if(!modern)geometry.scale(1,-1,1);
      const material=new THREE.MeshStandardMaterial({color:0xe5e8d8,roughness:.31,metalness:.22,transparent:true,opacity:1,side:THREE.DoubleSide});
      const mesh=new THREE.Mesh(geometry,material);
      mesh.userData.stroke=pathIndex;
      group.add(mesh);
    }
    pathIndex++;
  }
  if(!group.children.length)throw new Error('This writing source contains no filled outlines.');
  const box=new THREE.Box3().setFromObject(group);
  const center=box.getCenter(new THREE.Vector3()),size=box.getSize(new THREE.Vector3());
  const scale=4.6/Math.max(size.x,size.y);
  group.traverse(object=>{
    if(!(object instanceof THREE.Mesh))return;
    object.geometry.translate(-center.x,-center.y,-center.z);
    object.geometry.scale(scale,scale,scale);
    object.geometry.computeBoundingBox();
  });
  return group;
}

export function makeModernWord(data:GeometryData[],parts:ExplorerVisualPart[]):{group:THREE.Group;labels:GlyphLabel[]} {
  const group=new THREE.Group(),labels:GlyphLabel[]=[];
  const count=data.length,scale=1/count,spacing=5.2*scale;
  data.forEach((geometry,characterIndex)=>{
    if(!Array.isArray(geometry.strokes)||!geometry.strokes.length)throw new Error('The writing source is unavailable.');
    // A DOM serializer escapes path attributes without interpreting supplied text as SVG markup.
    const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');
    geometry.strokes.forEach(d=>{const path=document.createElementNS(svg.namespaceURI,'path');path.setAttribute('d',d);svg.appendChild(path);});
    const glyph=makeGlyph(new XMLSerializer().serializeToString(svg),true);
    const origin=(characterIndex-(count-1)/2)*spacing;
    glyph.position.x=origin;glyph.scale.setScalar(scale);group.add(glyph);
    const localParts=parts.filter(part=>part.characterIndex===characterIndex);
    localParts.forEach((part,partIndex)=>{
      const strokes=new Set(partStrokeIndices(geometry,part));
      const allMeshes=glyph.children.filter((object):object is THREE.Mesh=>object instanceof THREE.Mesh);
      const meshes=allMeshes.filter(object=>strokes.has(object.userData.stroke));
      const bounds=new THREE.Box3();
      // Even an unmapped cue keeps its own label slot and an intact-word anchor.
      // Skipping it would shift later labels onto the wrong written parts.
      (meshes.length?meshes:allMeshes).forEach(mesh=>bounds.union(mesh.geometry.boundingBox!));
      const center=bounds.getCenter(new THREE.Vector3()).multiplyScalar(scale).add(new THREE.Vector3(origin,0,0));
      const sign=localParts.length===1?(characterIndex-(count-1)/2):partIndex-(localParts.length-1)/2;
      const offset=meshes.length?new THREE.Vector3(Math.sign(sign)*.70,(localParts.length>2?(partIndex%2)*.2:0),sign<0?.24:-.12):new THREE.Vector3();
      // Strokes without a reliable component assignment remain intact and neutral.
      meshes.forEach(mesh=>{
        mesh.userData.color=new THREE.Color(part.color);
        mesh.userData.offset=offset.clone().divideScalar(scale);
        mesh.userData.part=parts.indexOf(part);
      });
      const anchor=new THREE.Vector3(center.x,center.y,.3);
      labels.push({...part,anchor,offset});
    });
  });
  return {group,labels};
}

export function disposeObject(root:THREE.Object3D){
  const geometries=new Set<THREE.BufferGeometry>(),materials=new Set<THREE.Material>();
  root.traverse(object=>{
    for(const material of (object.userData.materials??[]) as THREE.Material[])materials.add(material);
    if(object instanceof THREE.Mesh||object instanceof THREE.Line){
      geometries.add(object.geometry);
      for(const material of Array.isArray(object.material)?object.material:[object.material])materials.add(material);
    }
  });
  geometries.forEach(geometry=>geometry.dispose());
  materials.forEach(material=>material.dispose());
}
