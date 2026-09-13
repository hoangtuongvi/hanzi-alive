import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {loadBlenderMeaningModel,disposeBlenderMeaningModel} from '../src/explorer/blender-models';
import {THEATRE_LESSONS} from '../src/theatre/lessons';
import {SCENE_CATALOG} from '../src/explorer/scene-catalog';
import {lessonParts} from '../src/explorer/geometry';
import type {Character,Lesson} from '../src/types';

const lessons=JSON.parse(readFileSync(new URL('../public/data/lessons.json',import.meta.url),'utf8')) as Lesson[];
const characters=JSON.parse(readFileSync(new URL('../public/data/characters.json',import.meta.url),'utf8')) as Record<string,Character>;
const assets=SCENE_CATALOG.filter(scene=>scene.format==='blender');
const manifest=JSON.parse(readFileSync(new URL('../public/models/blender/manifest.json',import.meta.url),'utf8'));

test('every registered Blender export loads with embedded resources, ordered callouts and usable scene bounds',async t=>{
  for(const asset of assets){
    assert.ok(asset.asset);assert.ok(asset.anchors);
    const bytes=readFileSync(new URL(`../public${asset.asset}`,import.meta.url));
    assert.equal(bytes.toString('ascii',0,4),'glTF',asset.word);
    assert.equal(bytes.readUInt32LE(4),2,asset.word);
    assert.equal(bytes.readUInt32LE(8),bytes.byteLength,asset.word);
    const document=JSON.parse(bytes.toString('utf8',20,20+bytes.readUInt32LE(12)));
    assert.match(document.asset.generator,/Blender/i,asset.word);
    assert.ok((document.buffers??[]).every((buffer:{uri?:string})=>!buffer.uri||buffer.uri.startsWith('data:')),asset.word);
    assert.ok((document.images??[]).every((image:{uri?:string})=>!image.uri||image.uri.startsWith('data:')),asset.word);
    const triangles=document.meshes.reduce((sum:number,mesh:{primitives:{indices?:number;attributes:{POSITION:number};mode?:number}[]})=>sum+mesh.primitives.reduce((count,primitive)=>{
      assert.ok(primitive.mode===undefined||primitive.mode===4,`${asset.word}: triangle mesh required`);
      return count+document.accessors[primitive.indices??primitive.attributes.POSITION].count/3;
    },0),0);
    assert.ok(triangles>0&&triangles<=250000,`${asset.word}: ${triangles} triangles exceeds the scene budget`);
    assert.equal(triangles,manifest.assets[asset.scene].triangles,`${asset.word}: exported geometry must match the manifest budget`);
    const authoredOpacity=(document.materials??[]).map((material:{pbrMetallicRoughness?:{baseColorFactor?:number[]}})=>material.pbrMetallicRoughness?.baseColorFactor?.[3]??1);
    if(asset.word==='清')assert.ok(authoredOpacity.some((opacity:number)=>opacity>0&&opacity<1),'The clear pool must retain transparent water.');
    const fetch=t.mock.method(globalThis,'fetch',async()=>new Response(bytes));
    const parts=lessonParts(lessons.find(lesson=>lesson.word===asset.word)!,characters);
    const model=await loadBlenderMeaningModel(asset.word,parts,new AbortController().signal);
    assert.ok(model,asset.word);
    try{
      assert.deepEqual(model.labels.map(label=>label.glyph),parts.map(part=>part.glyph));
      asset.anchors.forEach((name,index)=>{
        const anchor=model.group.getObjectByName(name);assert.ok(anchor,`${asset.word}: ${name}`);
        const local=model.group.worldToLocal(anchor.getWorldPosition(new THREE.Vector3()));
        assert.ok(model.labels[index].anchor.distanceTo(local)<.00001,`${asset.word}: ${name}`);
      });
      const bounds=new THREE.Box3().setFromObject(model.group);
      const size=bounds.getSize(new THREE.Vector3());
      assert.ok(!bounds.isEmpty()&&Math.min(size.x,size.y,size.z)>.1,asset.word);
      assert.ok(Math.max(size.x,size.y,size.z)<6.5,`${asset.word}: scene must fit the explorer camera`);
      const alphas:number[]=[];
      model.group.traverse(object=>{
        if(!(object instanceof THREE.Mesh))return;
        for(const material of Array.isArray(object.material)?object.material:[object.material]){
          assert.equal(material.transparent,true);assert.equal(material.opacity,0);
          alphas.push(material.userData.baseOpacity);
        }
      });
      if(asset.word==='清')assert.ok(alphas.some(opacity=>opacity>0&&opacity<1),'Loading must preserve authored water alpha.');
    }finally{disposeBlenderMeaningModel(model);fetch.mock.restore();}
  }
});

test('changing lessons during GLB parsing discards and disposes the late model',async t=>{
  const controller=new AbortController();
  let signal:AbortSignal|undefined;
  t.mock.method(globalThis,'fetch',async(_url:RequestInfo|URL,init?:RequestInit)=>{
    signal=init?.signal??undefined;return new Response(new Uint8Array());
  });
  const scene=new THREE.Group();
  const geometry=new THREE.BoxGeometry(),texture=new THREE.Texture();
  const material=new THREE.MeshStandardMaterial({map:texture});
  scene.add(new THREE.Mesh(geometry,material));
  let geometryDisposed=false,materialDisposed=false,textureDisposed=false;
  geometry.addEventListener('dispose',()=>{geometryDisposed=true;});
  material.addEventListener('dispose',()=>{materialDisposed=true;});
  texture.addEventListener('dispose',()=>{textureDisposed=true;});
  let finishParsing!:(value:unknown)=>void,startedParsing!:()=>void;
  const started=new Promise<void>(resolve=>{startedParsing=resolve;});
  t.mock.method(GLTFLoader.prototype,'parseAsync',()=>{
    startedParsing();return new Promise(resolve=>{finishParsing=resolve;});
  });
  const loading=loadBlenderMeaningModel('休',THEATRE_LESSONS[0].parts,controller.signal);
  await started;controller.abort();finishParsing({scene});
  await assert.rejects(loading,{name:'AbortError'});
  assert.equal(signal,controller.signal);
  assert.ok(geometryDisposed&&materialDisposed&&textureDisposed);
});

test('other lessons do not fetch a Blender model and failed assets remain explicit to the caller',async t=>{
  const fetch=t.mock.method(globalThis,'fetch',async()=>new Response(null,{status:404}));
  assert.equal(await loadBlenderMeaningModel('not-a-word',[],new AbortController().signal),null);
  assert.equal(fetch.mock.callCount(),0);
  await assert.rejects(loadBlenderMeaningModel('休',THEATRE_LESSONS[0].parts,new AbortController().signal),/could not load \(404\)/);
});
