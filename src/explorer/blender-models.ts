import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import type {VisualPart} from '../theatre/types';
import {disposeObject} from './geometry';
import type {MeaningModel} from './scenes';
import {getSceneDefinition} from './scene-catalog';

/** GLBs are self-contained Blender exports; their empty nodes locate callouts. */
export async function loadBlenderMeaningModel(word:string,parts:VisualPart[],signal:AbortSignal):Promise<MeaningModel|null> {
  const asset=getSceneDefinition(word);if(asset?.format!=='blender')return null;
  if(!asset.asset||!asset.anchors)throw new Error(`The Blender scene for ${word} has no asset or callout definition.`);
  signal.throwIfAborted();
  const url=asset.asset;
  const response=await fetch(url,{signal});
  if(!response.ok)throw new Error(`The Blender scene for ${word} could not load (${response.status}).`);
  const bytes=await response.arrayBuffer();signal.throwIfAborted();
  // Fetch can be cancelled. Parsing cannot, so dispose a late result before
  // handing it to a stage that may already be displaying a different lesson.
  const gltf=await new GLTFLoader().parseAsync(bytes,'');
  const model:MeaningModel={group:gltf.scene,labels:[]};
  try{
    signal.throwIfAborted();
    const group=model.group;group.updateMatrixWorld(true);
    if(parts.length!==asset.anchors.length)throw new Error(`The Blender scene for ${word} has a different number of learning parts.`);
    model.labels=parts.map((part,index)=>{
      const anchorName=asset.anchors![index];
      const node=group.getObjectByName(anchorName);
      if(!node)throw new Error(`The Blender scene for ${word} is missing ${anchorName}.`);
      const anchor=group.worldToLocal(node.getWorldPosition(new THREE.Vector3()));
      return {...part,anchor};
    });
    group.traverse(object=>{
      if(!(object instanceof THREE.Mesh))return;
      for(const material of Array.isArray(object.material)?object.material:[object.material]){
        if(material.userData.baseOpacity===undefined)material.userData.baseOpacity=material.opacity;
        material.transparent=true;material.opacity=0;material.depthWrite=false;
      }
    });
    group.visible=false;group.userData.blenderAsset=url;
    return model;
  }catch(reason){
    disposeBlenderMeaningModel(model);throw reason;
  }
}

/** Texture resources belong to each load, just like its meshes and materials. */
export function disposeBlenderMeaningModel(model:MeaningModel){
  const textures=new Set<THREE.Texture>();
  model.group.traverse(object=>{
    if(!(object instanceof THREE.Mesh))return;
    for(const material of Array.isArray(object.material)?object.material:[object.material]){
      for(const value of Object.values(material))if(value instanceof THREE.Texture)textures.add(value);
    }
  });
  textures.forEach(texture=>{
    const source=texture.source.data;
    if(typeof ImageBitmap!=='undefined'&&source instanceof ImageBitmap)source.close();
    texture.dispose();
  });
  model.group.removeFromParent();disposeObject(model.group);
}
