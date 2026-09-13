import * as THREE from 'three';
import {makeMeaningScene} from './meaning-scene';
import type {VisualPart} from '../theatre/types';
import {THEATRE_LESSONS} from '../theatre/lessons';

type Point=[number,number,number];
export interface SceneLabel {glyph:string;image:string;color:string;anchor:THREE.Vector3;}
export interface MeaningModel {group:THREE.Group;labels:SceneLabel[];}

/** These are mnemonic illustrations, never historical reconstructions. */
export function createMeaningModel(word:string,parts:VisualPart[]):MeaningModel|null {
  const sceneId=THEATRE_LESSONS.find(lesson=>lesson.word===word)?.scene;
  if(sceneId==='rest')return {group:makeMeaningScene(),labels:parts.map((part,i)=>({...part,anchor:new THREE.Vector3(...(i===0?[.12,-1.30,.43]:[.75,.35,.06]) as Point)}))};
  if(sceneId==='woods'){
    const world=makeMeaningScene();
    (world.userData.person as THREE.Group).visible=false;
    const tree=world.userData.tree as THREE.Group;
    const trees=[tree,tree.clone(true)];
    trees.forEach((item,index)=>{
      item.scale.setScalar(.80);
      item.position.set((index-.5)*2.4-.42,-.4,0);
      if(index)world.add(item);
    });
    const ground=world.children.find(object=>object instanceof THREE.Mesh);
    if(ground)ground.scale.x=3.05;
    return {group:world,labels:parts.map((part,index)=>({...part,anchor:new THREE.Vector3((index-(parts.length-1)/2)*2.6,-.75,.4)}))};
  }
  if(!sceneId)return null;
  const group=new THREE.Group();
  const materials={
    bark:new THREE.MeshStandardMaterial({color:0x885b37,roughness:.91}),
    green:new THREE.MeshStandardMaterial({color:0x729943,roughness:.94}),
    darkGreen:new THREE.MeshStandardMaterial({color:0x285f3b,roughness:.96}),
    skin:new THREE.MeshStandardMaterial({color:0xd5a477,roughness:.82}),
    coral:new THREE.MeshStandardMaterial({color:0xd8784d,roughness:.85}),
    blue:new THREE.MeshStandardMaterial({color:0x355466,roughness:.88}),
    water:new THREE.MeshStandardMaterial({color:0x639b9e,roughness:.23,metalness:.35}),
    yellow:new THREE.MeshStandardMaterial({color:0xd6af58,roughness:.63}),
    purple:new THREE.MeshStandardMaterial({color:0xa59abc,roughness:.74}),
    dark:new THREE.MeshStandardMaterial({color:0x263933,roughness:.8}),
    cream:new THREE.MeshStandardMaterial({color:0xe5e8d8,roughness:.71}),
    earth:new THREE.MeshStandardMaterial({color:0x344932,roughness:1}),
  };
  const sceneMaterials=Object.values(materials);
  function ball(parent:THREE.Object3D,point:Point,scale:Point,material:THREE.Material,detail=2){
    const mesh=new THREE.Mesh(new THREE.IcosahedronGeometry(1,detail),material);
    mesh.position.set(...point);mesh.scale.set(...scale);parent.add(mesh);return mesh;
  }
  function box(parent:THREE.Object3D,point:Point,scale:Point,material:THREE.Material){
    const mesh=new THREE.Mesh(new THREE.BoxGeometry(...scale),material);mesh.position.set(...point);parent.add(mesh);return mesh;
  }
  function limb(parent:THREE.Object3D,a:Point,b:Point,width:number,material:THREE.Material){
    const start=new THREE.Vector3(...a),end=new THREE.Vector3(...b),direction=end.clone().sub(start);
    const mesh=new THREE.Mesh(new THREE.CylinderGeometry(width*.8,width,direction.length(),12),material);
    mesh.position.copy(start).add(end).multiplyScalar(.5);
    mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),direction.normalize());parent.add(mesh);return mesh;
  }
  function plants(x:number,z=0){
    for(let index=0;index<5;index++){
      const px=x+(index-2)*.25,top=-.5+(index%3)*.25;
      limb(group,[px,-2.0,z],[px,top,z],.035,materials.darkGreen);
      for(let leaf=0;leaf<3;leaf++){
        const sign=leaf%2?-1:1;
        const mesh=ball(group,[px+sign*.14,top-.15-leaf*.29,z],[.29,.105,.17],leaf%2?materials.darkGreen:materials.green);
        mesh.rotation.z=sign*.40;
      }
    }
  }
  function hand(point:Point,rotation=0,scale=1){
    const hand=new THREE.Group();hand.position.set(...point);hand.rotation.z=rotation;hand.scale.setScalar(scale);group.add(hand);
    ball(hand,[0,0,0],[.37,.46,.15],materials.skin);
    limb(hand,[0,-.3,0],[0,-1.0,0],.22,materials.coral);
    for(let finger=0;finger<4;finger++){
      const x=(finger-1.5)*.17,height=.69+(finger===1?.13:finger===2?.10:0);
      limb(hand,[x,.24,0],[x,height,0],.079,materials.skin);
      ball(hand,[x,height,0],[.064,.075,.067],materials.skin);
    }
    limb(hand,[-.28,-.10,.02],[-.56,.21,.05],.11,materials.skin);
    return hand;
  }
  function heart(point:Point,scale=1){
    const shape=new THREE.Shape();shape.moveTo(0,-.78);shape.bezierCurveTo(-1.65,.25,-.85,1.22,0,.57);shape.bezierCurveTo(.85,1.22,1.65,.25,0,-.78);
    const mesh=new THREE.Mesh(new THREE.ExtrudeGeometry(shape,{depth:.27,bevelEnabled:true,bevelThickness:.12,bevelSize:.12,bevelSegments:3,steps:1,curveSegments:18}),materials.coral);
    mesh.position.set(...point);mesh.scale.setScalar(scale);group.add(mesh);return mesh;
  }
  if(sceneId!=='clear')ball(group,[0,-2.15,0],[2.40,.13,1.30],materials.earth,3);
  let anchors:Point[]=[[-1.40,.20,.40],[1.40,-.75,.40]];
  if(sceneId==='clear'){
    // Tilt the diorama toward its opening view so the transparent surface and
    // the grass below it are both legible before the learner rotates the scene.
    const pool=new THREE.Group();pool.rotation.x=.52;pool.position.y=.32;group.add(pool);
    const sand=new THREE.MeshStandardMaterial({color:0x728475,roughness:1});
    const pebble=new THREE.MeshStandardMaterial({color:0xb7c2aa,roughness:.95});
    const grass=new THREE.MeshStandardMaterial({color:0x37814a,roughness:.9,side:THREE.DoubleSide});
    const grassLight=new THREE.MeshStandardMaterial({color:0x70a343,roughness:.9,side:THREE.DoubleSide});
    const waterSide=new THREE.MeshStandardMaterial({color:0x77c7cf,roughness:.13,metalness:.08,side:THREE.DoubleSide});
    const waterSurface=new THREE.MeshStandardMaterial({color:0xb4e6e7,roughness:.16,metalness:.03,side:THREE.DoubleSide});
    const waterLine=new THREE.MeshStandardMaterial({color:0xc5eff0,roughness:.35});
    waterSide.userData.baseOpacity=.21;waterSurface.userData.baseOpacity=.12;waterLine.userData.baseOpacity=.65;
    sceneMaterials.push(sand,pebble,grass,grassLight,waterSide,waterSurface,waterLine);
    ball(pool,[0,-.96,0],[2.45,.23,1.73],sand,2);
    ball(pool,[0,-.81,0],[2.20,.10,1.46],materials.darkGreen,3);

    const tufts:[number,number,number][]=[[-1.35,-.45,.78],[-.57,-.83,.94],[.34,-.78,1.04],[1.12,-.44,.91],[-.94,.35,.88],[-.13,.08,1.06],[.82,.29,.98],[.05,.87,.80]];
    tufts.forEach(([x,z,height],tuftIndex)=>{
      for(let bladeIndex=0;bladeIndex<9;bladeIndex++){
        const angle=bladeIndex/9*Math.PI*2+tuftIndex*.81;
        const dx=Math.cos(angle),dz=Math.sin(angle),width=.055+(bladeIndex%3)*.016;
        const length=height*(.69+(bladeIndex%4)*.10),bend=.24+(bladeIndex%3)*.055;
        const vertices=new Float32Array([
          -dz*width,0,dx*width, dz*width,0,-dx*width,
          dx*bend*.42-dz*width*.72,length*.59,dz*bend*.42+dx*width*.72,
          dx*bend*.42+dz*width*.72,length*.59,dz*bend*.42-dx*width*.72,
          dx*bend,length,dz*bend,
        ]);
        const geometry=new THREE.BufferGeometry();geometry.setAttribute('position',new THREE.BufferAttribute(vertices,3));
        geometry.setIndex([0,1,2,1,3,2,2,3,4]);geometry.computeVertexNormals();
        const blade=new THREE.Mesh(geometry,(bladeIndex+tuftIndex)%3?grass:grassLight);
        blade.position.set(x+dx*.075,-.76,z+dz*.075);pool.add(blade);
      }
    });

    // A glasslike shallow volume preserves the silhouette of every green tuft.
    const water=new THREE.Mesh(new THREE.CylinderGeometry(1,1,.86,64,1,false),[waterSide,waterSurface,waterSurface]);
    water.scale.set(2.22,1,1.49);water.position.y=-.32;water.renderOrder=2;pool.add(water);
    const rim=new THREE.Mesh(new THREE.TorusGeometry(1,.008,6,96),waterLine);
    rim.rotation.x=-Math.PI/2;rim.scale.set(2.22,1.49,1);rim.position.y=.12;rim.renderOrder=3;pool.add(rim);
    for(let i=0;i<3;i++){
      const ripple=new THREE.Mesh(new THREE.TorusGeometry(.18+i*.145,.007,6,64,Math.PI*1.55),waterLine);
      ripple.rotation.x=-Math.PI/2;ripple.rotation.z=.35;ripple.position.set(-1.25,.135,.30);ripple.renderOrder=3;pool.add(ripple);
    }
    for(let i=0;i<9;i++){
      const angle=.1+i*.24,radius=2.24+(i%2)*.045;
      const stone=ball(pool,[Math.cos(angle)*radius,-.73,Math.sin(angle)*1.53],[.12+(i%3)*.035,.10,.09+(i%2)*.06],pebble,1);
      stone.rotation.set(i*.4,i*.7,i*.2);
    }
    pool.updateMatrix();
    anchors=([[-1.45,.14,.3],[.95,.28,-.35]] as Point[]).map(point=>new THREE.Vector3(...point).applyMatrix4(pool.matrix).toArray() as Point);
  }else if(sceneId==='sunny'){
    plants(.7);plants(-.8,-.45);
    ball(group,[-1.2,1.15,0],[.59,.59,.34],materials.yellow,3);
    for(let i=0;i<10;i++){
      const angle=i/10*Math.PI*2;
      limb(group,[-1.2+Math.cos(angle)*.78,1.15+Math.sin(angle)*.78,0],[-1.2+Math.cos(angle)*1.03,1.15+Math.sin(angle)*1.03,0],.036,materials.yellow);
    }
    anchors=[[-1.2,1.15,.34],[.9,-.55,.35]];
  }else if(sceneId==='emotion'){
    plants(-1.35,-.4);plants(1.15,-.35);heart([-.35,.3,.15],.83);
    anchors=[[-1.3,.7,.5],[1.15,-.85,.5]];
  }else if(sceneId==='invite'){
    plants(-1.15,-.4);plants(1.1,-.45);
    const speech=new THREE.Shape();speech.moveTo(-1.3,1.45);speech.lineTo(1.3,1.45);speech.quadraticCurveTo(1.5,1.45,1.5,1.2);speech.lineTo(1.5,.2);speech.quadraticCurveTo(1.5,0,1.2,0);speech.lineTo(-.3,0);speech.lineTo(-.8,-.45);speech.lineTo(-.65,0);speech.lineTo(-1.3,0);speech.quadraticCurveTo(-1.5,0,-1.5,.25);speech.lineTo(-1.5,1.2);speech.quadraticCurveTo(-1.5,1.45,-1.3,1.45);
    const mesh=new THREE.Mesh(new THREE.ExtrudeGeometry(speech,{depth:.16,bevelEnabled:true,bevelThickness:.05,bevelSize:.05,bevelSegments:3,steps:1}),materials.cream);mesh.position.z=.3;group.add(mesh);
    for(let i=0;i<3;i++)ball(group,[-.55+i*.55,.73,.6],[.10,.10,.06],materials.darkGreen);
    anchors=[[-1.5,.75,.8],[1.25,-.85,.5]];
  }else if(sceneId==='phone'){
    hand([-.77,-.85,.05],-.48,1.2);
    const phone=new THREE.Group();phone.position.set(.50,.20,.24);phone.rotation.z=-.14;group.add(phone);
    box(phone,[0,0,0],[1.22,2.05,.20],materials.dark);
    box(phone,[0,.08,.115],[1.02,1.69,.03],materials.water);
    ball(phone,[0,-.90,.13],[.072,.072,.025],materials.cream);
    box(phone,[0,.94,.12],[.29,.035,.03],materials.cream);
    anchors=[[-1.55,-.9,.6],[1.45,.45,.5]];
  }else if(sceneId==='computer'){
    box(group,[0,-1.76,0],[3.75,.15,1.20],materials.bark);
    box(group,[0,-.2,0],[3.13,1.92,.18],materials.dark);
    box(group,[0,-.2,.11],[2.85,1.64,.035],materials.blue);
    box(group,[0,-1.33,0],[.20,.40,.24],materials.dark);box(group,[0,-1.56,.1],[1.10,.10,.65],materials.dark);
    box(group,[0,-1.61,.7],[2.0,.08,.60],materials.cream);
    for(let i=0;i<8;i++){
      const angle=i/8*Math.PI*2;
      ball(group,[.55+Math.cos(angle)*.48,-.2+Math.sin(angle)*.37,.24],[.30,.25,.10],materials.purple);
    }
    const bolt=new THREE.Shape();bolt.moveTo(-.55,.53);bolt.lineTo(-1.10,-.14);bolt.lineTo(-.72,-.12);bolt.lineTo(-.93,-.78);bolt.lineTo(-.26,.05);bolt.lineTo(-.61,.02);bolt.closePath();
    const spark=new THREE.Mesh(new THREE.ExtrudeGeometry(bolt,{depth:.06,bevelEnabled:false}),materials.yellow);spark.position.z=.23;group.add(spark);
    anchors=[[-1.55,.45,.5],[1.55,.45,.5]];
  }else if(sceneId==='parting'){
    hand([-1.26,-.53,0],-.72,1.0);hand([1.26,-.53,0],.72,1.0);
    const ribbonLeft=box(group,[-.6,.28,.22],[1.05,.12,.07],materials.coral);ribbonLeft.rotation.z=.20;
    const ribbonRight=box(group,[.6,.28,.22],[1.05,.12,.07],materials.coral);ribbonRight.rotation.z=-.20;
    limb(group,[-.32,.79,.23],[.20,.50,.23],.035,materials.cream);
    limb(group,[-.20,.50,.23],[.32,.79,.23],.035,materials.cream);
    anchors=[[-.05,1.35,.5],[-1.55,-.65,.5]];
  }else if(sceneId==='expert'){
    box(group,[0,-1.90,.1],[3.2,.15,2.0],materials.bark);
    for(let x=0;x<6;x++)for(let z=0;z<4;z++)box(group,[(x-2.5)*.49,-1.806,(z-1.5)*.47+.1],[.47,.025,.45],(x+z)%2?materials.cream:materials.dark);
    hand([.58,.45,0],-.18,1.14);
    ball(group,[.62,1.64,.03],[.15,.21,.15],materials.yellow);
    for(const [x,z] of [[-1,.35],[-.45,-.45],[1.05,-.3]]){
      limb(group,[x,-1.74,z],[x,-1.32,z],.12,materials.darkGreen);ball(group,[x,-1.24,z],[.14,.14,.14],materials.darkGreen);
    }
    anchors=[[-.64,1.30,.5],[1.55,-.1,.5]];
  }
  sceneMaterials.forEach(material=>{material.transparent=true;material.opacity=0;material.depthWrite=false;});
  group.userData.materials=sceneMaterials;group.visible=false;
  return {group,labels:parts.map((part,index)=>({...part,anchor:new THREE.Vector3(...(anchors[index]??[0,-1.3,.4]))}))};
}
