import test from 'node:test';
import assert from 'node:assert/strict';
import {blendExplorerPoses,explorerPose} from '../src/explorer/transitions';

test('a direct scene-to-oracle transition never flashes modern, seal, or bronze forms',()=>{
  const scene=explorerPose(100/6,true,true,true),oracle=explorerPose(100,true,true,true);
  for(const amount of [0,.2,.5,.8,1]){
    const pose=blendExplorerPoses(scene,oracle,amount);
    assert.deepEqual(pose.weights.slice(0,3),[0,0,0]);
    assert.equal(pose.weights[3],amount);
    assert.equal(pose.weights[4],1-amount);
  }
});

test('word-to-parts animation keeps the sourced modern form while separating its components',()=>{
  const word=explorerPose(50,true,true,true),parts=explorerPose(200/6,true,true,true);
  const halfway=blendExplorerPoses(word,parts,.5);
  assert.deepEqual(halfway.weights,[1,0,0,0,0]);
  assert.equal(halfway.explode,.5);
  assert.equal(halfway.labels,.5);
});

test('the story can hold the scene pose without a new visual movement',()=>{
  const scene=explorerPose(100/6,true,true,true);
  assert.deepEqual(blendExplorerPoses(scene,scene,.5),scene);
});

test('interrupted transitions start from the currently visible forms',()=>{
  const scene=explorerPose(100/6,true,true,true),oracle=explorerPose(100,true,true,true);
  const interrupted=blendExplorerPoses(scene,oracle,.3);
  const next=blendExplorerPoses(interrupted,explorerPose(50,true,true,true),.5);
  assert.equal(next.weights[1],0);
  assert.equal(next.weights[2],0);
  assert.equal(next.weights[0],.5);
  assert.equal(next.weights[3],.15);
  assert.equal(next.weights[4],.35);
});
