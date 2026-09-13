import test from 'node:test';
import assert from 'node:assert/strict';
import {layoutBreakdownCallouts,layoutCallouts,type ScreenBounds,type CalloutPlacement} from '../src/explorer/callout-layout';

const rectangle=(label:CalloutPlacement):ScreenBounds=>({left:label.x-label.width/2,right:label.x+label.width/2,top:label.y-label.height/2,bottom:label.y+label.height/2});
const overlaps=(a:ScreenBounds,b:ScreenBounds)=>a.left<b.right&&a.right>b.left&&a.top<b.bottom&&a.bottom>b.top;
function assertClear(labels:CalloutPlacement[],obstacles:ScreenBounds[],width:number,height:number){
  for(const label of labels){
    assert.equal(label.visible,true,label.key);
    const box=rectangle(label);
    assert.ok(box.left>=8&&box.right<=width-8&&box.top>=8&&box.bottom<=height-8,label.key);
    assert.ok(obstacles.every(obstacle=>!overlaps(box,obstacle)),`${label.key} covers a visual`);
  }
  for(let i=0;i<labels.length;i++)for(let j=i+1;j<labels.length;j++)assert.ok(!overlaps(rectangle(labels[i]),rectangle(labels[j])));
}

test('written-part labels keep a common bottom row even when their anchors have different heights',()=>{
  const measures=[
    {key:'water',anchor:{x:220,y:110},width:90,height:40},
    {key:'green',anchor:{x:560,y:370},width:100,height:48},
  ];
  const labels=layoutBreakdownCallouts(measures,800,500);
  assertClear(labels,[],800,500);
  assert.deepEqual(labels.map(label=>label.key),['water','green']);
  assert.deepEqual(labels.map(label=>label.y),[464,464]);
  assert.deepEqual(labels.map(label=>label.x),[290,510]);
  const rotated=layoutBreakdownCallouts(measures.map(item=>({...item,anchor:{x:800-item.anchor.x,y:500-item.anchor.y}})),800,500);
  assert.deepEqual(rotated.map(({x,y})=>({x,y})),labels.map(({x,y})=>({x,y})));
});

test('the written-parts row stays centered, visible, and separate on narrow screens',()=>{
  for(const width of [390,240]){
    const labels=layoutBreakdownCallouts([
      {key:'sun',anchor:{x:20,y:20},width:80,height:40},
      {key:'green',anchor:{x:width-20,y:160},width:86,height:40},
    ],width,200);
    assertClear(labels,[],width,200);
    assert.equal(labels[0].y,labels[1].y);
    assert.equal((labels[0].x+labels[1].x)/2,width/2);
    assert.equal(labels[0].y+labels[0].height/2,188);
  }
});

test('a written-parts row with insufficient room hides colliding labels',()=>{
  const labels=layoutBreakdownCallouts([
    {key:'water',anchor:{x:20,y:20},width:150,height:40},
    {key:'green',anchor:{x:180,y:100},width:150,height:40},
  ],200,160);
  assert.equal(labels.filter(label=>label.visible).length,1);
  assertClear(labels.filter(label=>label.visible),[],200,160);
});

test('sun label stays beside the sun, independently of the grass below it, on a phone',()=>{
  const obstacles=[{left:80,right:180,top:85,bottom:185},{left:115,right:285,top:225,bottom:360},{left:50,right:330,top:365,bottom:397}];
  const labels=layoutCallouts([
    {key:'sun',anchor:{x:130,y:135},width:80,height:40,preferred:{x:1,y:-.35}},
    {key:'green',anchor:{x:260,y:260},width:86,height:40,preferred:{x:1,y:.1}},
  ],390,500,obstacles);
  assertClear(labels,obstacles,390,500);
  const sun=labels[0],green=labels[1];
  assert.ok(sun.y+sun.height/2<225,'Sun label must stay above the grass');
  assert.ok(Math.hypot(sun.x-130,sun.y-135)<140,'Sun label must remain nearby');
  assert.ok(Math.abs(sun.y-green.y)>60,'Do not align unrelated elements to one row');
});

test('callouts use independent nearby gaps on wide screens without covering any mesh',()=>{
  const obstacles=[{left:225,right:310,top:310,bottom:430},{left:360,right:590,top:90,bottom:270},{left:430,right:470,top:260,bottom:440}];
  const labels=layoutCallouts([
    {key:'person',anchor:{x:265,y:365},width:98,height:40,preferred:{x:-1,y:0}},
    {key:'tree',anchor:{x:450,y:310},width:84,height:40,preferred:{x:1,y:-.3}},
  ],800,550,obstacles);
  assertClear(labels,obstacles,800,550);
  assert.ok(labels[0].x<225);
  assert.ok(labels[1].y<440,'Tree label must not be forced below the whole scene');
});

test('moving a visual element moves its label in both directions',()=>{
  const first=layoutCallouts([{key:'sun',anchor:{x:125,y:110},width:80,height:40,preferred:{x:1,y:-.35}}],390,500,[{left:85,right:165,top:70,bottom:150}]);
  const moved=layoutCallouts([{key:'sun',anchor:{x:165,y:180},width:80,height:40,preferred:{x:1,y:-.35}}],390,500,[{left:125,right:205,top:140,bottom:220}]);
  assert.equal(moved[0].key,'sun');
  assert.ok(Math.abs(moved[0].x-first[0].x-40)<1);
  assert.ok(Math.abs(moved[0].y-first[0].y-70)<1);
});

test('label collisions are resolved without losing their element association',()=>{
  const obstacles=[{left:145,right:230,top:100,bottom:250}];
  const labels=layoutCallouts([
    {key:'water',anchor:{x:167,y:160},width:90,height:40,preferred:{x:-1,y:0}},
    {key:'green',anchor:{x:209,y:170},width:90,height:40,preferred:{x:1,y:0}},
  ],390,420,obstacles);
  assertClear(labels,obstacles,390,420);
  assert.deepEqual(labels.map(label=>label.key),['water','green']);
});

test('a completely filled view cannot force labels over the illustration',()=>{
  const labels=layoutCallouts([{key:'sun',anchor:{x:150,y:150},width:90,height:40}],300,300,[{left:0,right:300,top:0,bottom:300}]);
  assert.equal(labels[0].visible,false);
});
