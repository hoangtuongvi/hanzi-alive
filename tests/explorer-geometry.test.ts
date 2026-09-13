import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from 'three';
import {SVGLoader} from 'three/addons/loaders/SVGLoader.js';
import type {Character,GeometryData,Lesson} from '../src/types';
import {disposeObject,lessonParts,makeModernWord,mnemonicSourcePaths,partStrokeIndices} from '../src/explorer/geometry';

const lessons=JSON.parse(readFileSync(new URL('../public/data/lessons.json',import.meta.url),'utf8')) as Lesson[];
const characters=JSON.parse(readFileSync(new URL('../public/data/characters.json',import.meta.url),'utf8')) as Record<string,Character>;
const lesson=(word:string)=>lessons.find(item=>item.word===word)!;
const geometry=(word:string)=>JSON.parse(readFileSync(new URL(`../public${characters[word].geometryUrl}`,import.meta.url),'utf8')) as GeometryData;

test('nested mnemonic cuts keep each repeated tree and each arm of 爱 attached to its own strokes',()=>{
  const forest=lessonParts(lesson('森'),characters),love=lessonParts(lesson('爱'),characters);
  assert.deepEqual(forest.map(part=>part.sourcePath),[[0],[1,0],[1,1]]);
  assert.deepEqual(forest.map(part=>partStrokeIndices(geometry('森'),part)),[[0,1,2,3],[4,5,6,7],[8,9,10,11]]);
  assert.deepEqual(love.map(part=>part.sourcePath),[[0,0],[0,1],[1]]);
  assert.deepEqual(love.map(part=>partStrokeIndices(geometry('爱'),part)),[[0,1,2,3],[4,5],[6,7,8,9]]);
});

test('a root glyph match is valid even when the legacy top-level grouping is unknown',()=>{
  const [field]=lessonParts(lesson('由'),characters),source=geometry('由');
  assert.deepEqual(source.groups,[-1,-1,-1,-1,-1]);
  assert.deepEqual(field.sourcePath,[]);
  assert.deepEqual(partStrokeIndices(source,field),[0,1,2,3,4]);
});

test('a mnemonic expanded through another character never invents stroke assignments',()=>{
  const parts=lessonParts(lesson('坐'),characters);
  assert.deepEqual(parts.map(part=>part.glyph),['人','人','土']);
  assert.deepEqual(parts.map(part=>part.sourcePath),[null,null,null]);
  assert.deepEqual(parts.map(part=>partStrokeIndices(geometry('坐'),part)),[[],[],[]]);
  assert.equal(mnemonicSourcePaths(null,['木']),null);
});

test('every corpus lesson keeps cue order and no supplied stroke belongs to two mnemonic parts',()=>{
  for(const item of lessons){
    const parts=lessonParts(item,characters);
    assert.deepEqual(parts.map(({glyph,image})=>({glyph,image})),item.memoryElements,item.word);
    item.characters.forEach((glyph,index)=>{
      const source=geometry(glyph),assigned=new Set<number>();
      for(const part of parts.filter(part=>part.characterIndex===index)){
        for(const stroke of partStrokeIndices(source,part)){
          assert.equal(assigned.has(stroke),false,`${item.word}: duplicate stroke ${stroke}`);
          assigned.add(stroke);
        }
      }
      if(item.characters.length>1)assert.equal(assigned.size,source.strokes.length,`${item.word}: whole-character cue`);
    });
  }
});

test('an unmapped cue retains its label slot without stealing the next cue’s anchor or color',t=>{
  // Supply two simple source outlines; the regression concerns their assignments,
  // independent of browser SVG parsing and its DOM dependency.
  const sourcePaths=[0,1].map(index=>{
    const path=new THREE.ShapePath();
    path.moveTo(index*3,0);path.lineTo(index*3+1,0);path.lineTo(index*3+1,1);path.lineTo(index*3,1);path.lineTo(index*3,0);
    return path;
  });
  t.mock.method(SVGLoader.prototype,'parse',()=>({paths:sourcePaths,xml:{} as XMLDocument}));
  const originalDocument=Object.getOwnPropertyDescriptor(globalThis,'document');
  const originalSerializer=Object.getOwnPropertyDescriptor(globalThis,'XMLSerializer');
  Object.defineProperty(globalThis,'document',{configurable:true,value:{createElementNS:(namespaceURI:string)=>({namespaceURI,setAttribute(){},appendChild(){}})}});
  Object.defineProperty(globalThis,'XMLSerializer',{configurable:true,value:class {serializeToString(){return '<svg/>';}}});
  let model:ReturnType<typeof makeModernWord>|undefined;
  try{
    model=makeModernWord([{character:'示',strokes:['first','second'],groups:[1,1],medians:[],matches:[[1],[1]]}],[
      {glyph:'甲',image:'first cue',color:'#ebb08d',characterIndex:0,sourceGroup:null,sourcePath:[0]},
      {glyph:'乙',image:'second cue',color:'#9bcb81',characterIndex:0,sourceGroup:null,sourcePath:[1]},
    ]);
    assert.deepEqual(model.labels.map(label=>label.glyph),['甲','乙']);
    assert.equal(model.labels[0].offset.length(),0,'Unmapped cue must not move the writing.');
    let meshes=0;
    model.group.traverse(object=>{
      if(object instanceof THREE.Mesh){
        meshes++;
        assert.equal(object.userData.part,1,'The mapped strokes belong to the second cue.');
        assert.ok(object.userData.color.equals(new THREE.Color('#9bcb81')));
      }
    });
    assert.equal(meshes,2);
  }finally{
    if(model)disposeObject(model.group);
    if(originalDocument)Object.defineProperty(globalThis,'document',originalDocument);else Reflect.deleteProperty(globalThis,'document');
    if(originalSerializer)Object.defineProperty(globalThis,'XMLSerializer',originalSerializer);else Reflect.deleteProperty(globalThis,'XMLSerializer');
  }
});
