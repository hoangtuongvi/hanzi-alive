import * as THREE from 'three';

type Point = [number, number, number];

/** A teaching illustration of rest, not a reconstruction of historical dress. */
export function makeMeaningScene(){
  const world=new THREE.Group();world.name='visual-meaning';
  const tree=new THREE.Group();tree.name='tree';
  const person=new THREE.Group();person.name='person';
  world.add(tree,person);
  const materials={
    bark:new THREE.MeshStandardMaterial({color:0x885b37,roughness:.91}),
    barkLight:new THREE.MeshStandardMaterial({color:0xa4774a,roughness:.87}),
    leaf:new THREE.MeshStandardMaterial({color:0x3f7f47,roughness:.94}),
    leafLight:new THREE.MeshStandardMaterial({color:0x729943,roughness:.94}),
    leafDark:new THREE.MeshStandardMaterial({color:0x285f3b,roughness:.96}),
    shirt:new THREE.MeshStandardMaterial({color:0xd8784d,roughness:.85}),
    pants:new THREE.MeshStandardMaterial({color:0x355466,roughness:.88}),
    skin:new THREE.MeshStandardMaterial({color:0xd5a477,roughness:.82}),
    hair:new THREE.MeshStandardMaterial({color:0x282a22,roughness:.92}),
    shoes:new THREE.MeshStandardMaterial({color:0x303c35,roughness:.92}),
    earth:new THREE.MeshStandardMaterial({color:0x344932,roughness:1}),
    grass:new THREE.MeshStandardMaterial({color:0x638548,roughness:.97})
  };
  const V=(a:Point)=>new THREE.Vector3(...a);
  function ball(parent:THREE.Object3D,point:Point,scale:Point,material:THREE.Material,detail=2){
    const mesh=new THREE.Mesh(new THREE.IcosahedronGeometry(1,detail),material);
    mesh.position.copy(V(point));mesh.scale.set(...scale);parent.add(mesh);return mesh;
  }
  function limb(parent:THREE.Object3D,a:Point,b:Point,r1:number,r2:number,material:THREE.Material,sides=12){
    const start=V(a),end=V(b),direction=end.clone().sub(start);
    const mesh=new THREE.Mesh(new THREE.CylinderGeometry(r2,r1,direction.length(),sides,1),material);
    mesh.position.copy(start).add(end).multiplyScalar(.5);
    mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),direction.normalize());
    parent.add(mesh);return mesh;
  }
  // Ground and exposed roots anchor both figures to the same place.
  ball(world,[0,-2.15,0],[2.05,.13,1.04],materials.earth,3);
  limb(tree,[.72,-2.08,0],[.79,-.74,0],.24,.19,materials.bark,14);
  limb(tree,[.79,-.76,0],[.63,.48,0],.19,.13,materials.bark,14);
  limb(tree,[.63,.47,0],[.48,1.29,.01],.13,.07,materials.barkLight);
  const branches:[Point,Point,number,number][]=[
    [[.67,.13,0],[-.13,.92,.02],.115,.065],
    [[-.13,.92,.02],[-.94,1.39,.04],.065,.025],
    [[-.12,.93,.02],[-.25,1.76,.02],.057,.026],
    [[.60,.64,0],[1.41,1.20,-.08],.10,.045],
    [[1.41,1.20,-.08],[1.70,1.80,-.13],.045,.022],
    [[.50,1.08,.01],[.93,1.99,.06],.068,.018],
    [[.65,.74,.02],[.77,1.38,.54],.08,.025]
  ];
  for(const [a,b,r1,r2] of branches)limb(tree,a,b,r1,r2,materials.barkLight);
  for(const [x,z] of [[.10,.4],[1.25,.40],[.9,-.57],[1.42,-.2]])limb(tree,[.74,-1.87,0],[x,-2.08,z],.13,.035,materials.bark);
  // Overlapping volumes form a broad canopy above the resting person.
  const canopy=new THREE.Group();canopy.name='canopy';tree.add(canopy);
  const crowns:[number,number,number,number,number,number,keyof typeof materials][]=[
    [-.98,1.47,.02,.75,.55,.57,'leafDark'],[-.45,1.85,-.15,.90,.68,.69,'leaf'],
    [.40,2.01,-.17,.94,.69,.66,'leafLight'],[1.17,1.94,-.16,.81,.62,.69,'leaf'],
    [1.77,1.59,-.08,.65,.53,.52,'leafDark'],[-.42,1.30,.40,.72,.50,.57,'leaf'],
    [.43,1.49,.49,.82,.57,.64,'leafLight'],[1.24,1.37,.41,.78,.48,.57,'leaf'],
    [.33,1.42,-.60,.86,.57,.58,'leafDark']
  ];
  crowns.forEach(([x,y,z,sx,sy,sz,key],i)=>{const mesh=ball(canopy,[x,y,z],[sx,sy,sz],materials[key],2);mesh.rotation.set(i*.33,i*.7,i*.27)});
  // The person's back is on the right, against the trunk. Their face points left.
  ball(person,[.18,-1.66,.21],[.29,.22,.30],materials.shirt);
  limb(person,[.17,-1.55,.21],[.47,-.83,.13],.25,.225,materials.shirt,16);
  ball(person,[.47,-.83,.13],[.23,.20,.25],materials.shirt);
  limb(person,[.44,-.72,.13],[.40,-.53,.13],.087,.081,materials.skin);
  const head=ball(person,[.36,-.34,.13],[.20,.245,.205],materials.skin,3);
  head.rotation.z=-.13;
  ball(person,[.18,-.36,.13],[.072,.062,.071],materials.skin,2);
  const hair=new THREE.Mesh(new THREE.SphereGeometry(.209,20,12,0,Math.PI*2,0,Math.PI*.57),materials.hair);
  hair.position.set(.39,-.295,.13);hair.rotation.z=-.17;person.add(hair);
  ball(person,[.43,-.37,.322],[.045,.060,.028],materials.skin,2);
  // A closed eye is a short dark curve, emphasizing relaxation.
  const eyeCurve=new THREE.CatmullRomCurve3([V([.195,-.316,.265]),V([.219,-.326,.275]),V([.246,-.322,.283])]);
  person.add(new THREE.Mesh(new THREE.TubeGeometry(eyeCurve,8,.009,5,false),materials.hair));
  for(const z of [-.02,.43]){
    limb(person,[.16,-1.66,z],[-.51,-1.78,z+.015],.155,.133,materials.pants,14);
    ball(person,[-.51,-1.78,z+.015],[.137,.135,.137],materials.pants);
    limb(person,[-.51,-1.78,z+.015],[-1.19,-2.00,z+.05],.123,.077,materials.pants,14);
    ball(person,[-1.32,-2.027,z+.07],[.237,.09,.126],materials.shoes,2);
  }
  for(const z of [-.065,.375]){
    limb(person,[.42,-.89,z],[-.02,-1.32,z+.035],.11,.09,materials.shirt);
    ball(person,[-.02,-1.32,z+.035],[.09,.09,.09],materials.skin);
    limb(person,[-.02,-1.32,z+.035],[-.57,-1.66,z+.055],.073,.049,materials.skin);
    ball(person,[-.61,-1.69,z+.06],[.103,.056,.062],materials.skin,2);
  }
  // Small grass blades bring color to the base without hiding the silhouette.
  [[-1.60,-.29],[-1.66,-.19],[1.42,.54],[1.52,.53],[.08,-.67],[-.04,-.70]].forEach(([x,z],i)=>{
    limb(world,[x,-2.12,z],[x+(i%2?.055:-.055),-1.91-(i%3)*.025,z],.018,.003,materials.grass,5);
  });
  // Common material flags allow an exact cross-fade with the historical model.
  for(const material of Object.values(materials)){material.transparent=true;material.opacity=0;material.depthWrite=false;}
  world.userData.materials=Object.values(materials);
  world.userData.person=person;world.userData.tree=tree;
  world.visible=false;
  return world;
}
