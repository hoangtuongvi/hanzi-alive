import test from 'node:test';
import assert from 'node:assert/strict';
import {createExplorerRenderer,GraphicsInitializationError,stageFailure} from '../src/explorer/graphics';

// Exercise Three's real constructor with a browser that refuses getContext.
// No GPU or DOM implementation is needed for this failure path.
class UnavailableCanvas extends EventTarget {
  width=300;
  height=150;
  constructor(readonly reason:string){super();}
  setAttribute(){}
  getContext(){
    this.dispatchEvent(Object.assign(new Event('webglcontextcreationerror'),{statusMessage:this.reason}));
    return null;
  }
}

test('a blocked WebGL creation preserves the browser reason and requires a browser reload',t=>{
  t.mock.method(console,'error',()=>{});
  const reason='Web page caused context loss and was blocked';
  const canvas=new UnavailableCanvas(reason);
  assert.throws(()=>createExplorerRenderer(canvas as unknown as HTMLCanvasElement),(error:unknown)=>{
    assert.ok(error instanceof GraphicsInitializationError);
    assert.equal(error.statusMessage,reason);
    assert.ok(error.cause instanceof Error);
    assert.match(error.cause.message,/Error creating WebGL context/);
    const failure=stageFailure(error);
    assert.equal(failure.recovery,'browser-reload');
    assert.match(failure.message,/browser’s Reload button/);
    assert.match(failure.message,/blocked 3D graphics/);
    return true;
  });
});

test('an unavailable graphics context is distinct from a failed lesson download',t=>{
  t.mock.method(console,'error',()=>{});
  assert.throws(()=>createExplorerRenderer(new UnavailableCanvas('') as unknown as HTMLCanvasElement),(error:unknown)=>{
    assert.ok(error instanceof GraphicsInitializationError);
    const failure=stageFailure(error);
    assert.equal(failure.recovery,'browser-reload');
    assert.match(failure.message,/could not start 3D graphics/);
    assert.doesNotMatch(failure.message,/blocked/);
    return true;
  });
  for(const reason of [new Error('A writing source could not load.'),new Error('The authored illustration is unavailable.'),null]){
    const failure=stageFailure(reason);
    assert.equal(failure.recovery,'retry-scene');
    assert.match(failure.message,/Try loading it again/);
  }
});
