/// <reference types="vite/client" />
import React from 'react';
import {createRoot} from 'react-dom/client';
import App from '../src/App';
import '../src/styles.css';

// This is a separate Vite development entry point. It is neither linked from
// the application nor included among the production build's entry points.
if (!import.meta.env.DEV) throw new Error('The graphics test harness is development-only.');

type GraphicsContext = WebGLRenderingContext | WebGL2RenderingContext;
const root = document.getElementById('root')!;
const text = (id:string, value:string|number):void => {
  document.getElementById(id)!.textContent = String(value);
};
const button = (id:string):HTMLButtonElement => document.getElementById(id) as HTMLButtonElement;
const events:string[] = [];
function log(message:string):void {
  events.push(`${new Date().toLocaleTimeString()} ${message}`);
  text('test-events', events.slice(-40).join('\n'));
}
function result(message:string):void { text('test-result', message); log(message); }

// Keep these references weak so the harness does not keep retired contexts
// alive and introduce the resource leak it is intended to detect.
const seenContexts = new WeakSet<GraphicsContext>();
const seenCanvases = new WeakSet<HTMLCanvasElement>();
const contexts = new WeakMap<HTMLCanvasElement, GraphicsContext>();
const canvasIds = new WeakMap<HTMLCanvasElement, number>();
const restoreExtensions = new WeakMap<HTMLCanvasElement, WEBGL_lose_context>();
let contextCount = 0, canvasSequence = 0, losses = 0, restores = 0;
let expectedLoss = false;
let restoreTimer:number|undefined;
let stressTimer:number|undefined;
let stressClicks = 0, stressBaseline = 0, stressLosses = 0;
let stressCanvas:HTMLCanvasElement|undefined;
let pendingAutoRestore = false;
let runtimeError = '';

function appCanvas():HTMLCanvasElement|null { return root.querySelector('canvas'); }
function currentContext():GraphicsContext|undefined {
  const canvas = appCanvas();
  return canvas ? contexts.get(canvas) : undefined;
}
function stopStress(message?:string):void {
  window.clearTimeout(stressTimer);
  stressTimer = undefined;
  stressCanvas = undefined;
  button('test-stress').disabled = false;
  button('test-stop').disabled = true;
  if (message) result(message);
}
function appError():string {
  if (runtimeError) return runtimeError;
  const status = root.querySelector('.explorer-three-loading, .app-error')?.textContent?.trim() ?? '';
  return /could not|couldn’t|paused|unavailable|failed/i.test(status) ? status : '';
}

const originalGetContext = HTMLCanvasElement.prototype.getContext;
HTMLCanvasElement.prototype.getContext = function(this:HTMLCanvasElement, kind:string, options?:unknown) {
  const getContext = originalGetContext as (this:HTMLCanvasElement, kind:string, options?:unknown) => RenderingContext|null;
  const context = getContext.call(this, kind, options);
  if (context && ['webgl', 'webgl2', 'experimental-webgl'].includes(kind)) {
    const graphics = context as GraphicsContext;
    contexts.set(this, graphics);
    if (!seenContexts.has(graphics)) {
      seenContexts.add(graphics);
      contextCount++;
      log(`WebGL context ${contextCount} created.`);
    }
    if (!seenCanvases.has(this)) {
      seenCanvases.add(this);
      canvasIds.set(this, ++canvasSequence);
      this.addEventListener('webglcontextlost', () => {
        losses++;
        log(`Canvas ${canvasIds.get(this)} lost its context${expectedLoss ? ' (requested by harness)' : ''}.`);
        if (stressTimer !== undefined) stopStress(`FAIL: context lost after ${stressClicks} Next clicks.`);
        refresh();
      });
      this.addEventListener('webglcontextrestored', () => {
        restores++;
        log(`Canvas ${canvasIds.get(this)} restored its context.`);
        if (pendingAutoRestore) {
          pendingAutoRestore = false;
          result('Context restored. Confirm that the scene and lesson playback resume on the same canvas.');
        }
        expectedLoss = false;
        refresh();
      });
    }
  }
  return context;
} as typeof originalGetContext;

function refresh():void {
  const canvas = appCanvas();
  const context = currentContext();
  const phase = root.querySelector<HTMLElement>('.focused-content');
  text('test-context-count', contextCount);
  text('test-canvas-count', root.querySelectorAll('canvas').length);
  text('test-canvas-identity', canvas ? `Canvas ${canvasIds.get(canvas) ?? '?'}` : 'None');
  text('test-context-state', context ? context.isContextLost() ? 'Lost' : 'Available' : 'Waiting');
  text('test-loss-count', losses);
  text('test-restore-count', restores);
  text('test-phase', phase ? `${phase.getAttribute('aria-label')} · ${phase.dataset.phase}` : 'Waiting');
  text('test-scene-source', canvas?.dataset.sceneSource ?? 'Waiting');
  text('test-app-status', runtimeError || root.querySelector('.explorer-three-loading, .app-error, .app-loading')?.textContent?.trim() || (canvas ? 'Scene available' : 'Waiting for the app'));
}

function loseContext(autoRestore:boolean):void {
  stopStress();
  window.clearTimeout(restoreTimer);
  const context = currentContext();
  const extension = context?.getExtension('WEBGL_lose_context');
  if (!context || !extension) { result('Cannot run: this canvas has no WEBGL_lose_context extension yet.'); return; }
  if (context.isContextLost()) { result('The context is already lost. Use Restore graphics context.'); return; }
  expectedLoss = true;
  restoreExtensions.set(appCanvas()!, extension);
  pendingAutoRestore = autoRestore;
  result(autoRestore ? 'Losing the context now; restoration will be requested in one second.' : 'Context loss requested. The app should pause until restoration.');
  extension.loseContext();
  if (autoRestore) restoreTimer = window.setTimeout(() => {
    extension.restoreContext();
    log('Requested native restoration on the same context.');
    restoreTimer = undefined;
  }, 1000);
}

button('test-auto-recover').addEventListener('click', () => loseContext(true));
button('test-lose').addEventListener('click', () => loseContext(false));
button('test-restore').addEventListener('click', () => {
  window.clearTimeout(restoreTimer);
  restoreTimer = undefined;
  const context = currentContext();
  const canvas = appCanvas();
  // getExtension may return null while a context is lost, so retain the
  // extension obtained before the loss for this exact canvas.
  const extension = canvas ? restoreExtensions.get(canvas) ?? context?.getExtension('WEBGL_lose_context') : undefined;
  if (!context || !extension) { result('Cannot restore: no current graphics context.'); return; }
  if (!context.isContextLost()) { result('The current graphics context is already available.'); return; }
  result('Requested native restoration on the current canvas.');
  extension.restoreContext();
});
button('test-stop').addEventListener('click', () => stopStress(`Stopped after ${stressClicks} Next clicks.`));
button('test-stress').addEventListener('click', () => {
  stopStress();
  const canvas = appCanvas();
  if (!canvas || !currentContext() || currentContext()!.isContextLost()) { result('Cannot start: wait for an available app graphics context.'); return; }
  const error = appError();
  if (error) { result(`Cannot start while the app reports an error: ${error}`); return; }
  stressClicks = 0;
  stressBaseline = contextCount;
  stressLosses = losses;
  stressCanvas = canvas;
  button('test-stress').disabled = true;
  button('test-stop').disabled = false;
  result(`Starting 30 real Next clicks, 350 ms apart. Baseline: ${stressBaseline} contexts, canvas ${canvasIds.get(canvas)}.`);
  function tick():void {
    const error = appError();
    if (error || losses !== stressLosses) { stopStress(`FAIL after ${stressClicks} clicks: ${error || 'unexpected context loss'}`); return; }
    if (contextCount !== stressBaseline || appCanvas() !== stressCanvas || root.querySelectorAll('canvas').length !== 1) {
      stopStress(`FAIL after ${stressClicks} clicks: canvas or context changed (${stressBaseline} → ${contextCount} contexts).`);
      return;
    }
    if (stressClicks === 30) {
      stopStress(`PASS: 30 Next clicks completed; the same canvas and ${contextCount} WebGL context(s) remain, with no context loss or app errors.`);
      return;
    }
    const next = root.querySelector<HTMLButtonElement>('button.focused-next');
    if (!next) { stopStress(`FAIL after ${stressClicks} clicks: the app’s Next button disappeared.`); return; }
    next.click();
    stressClicks++;
    text('test-result', `Stress test running: ${stressClicks}/30 Next clicks; ${contextCount} WebGL context(s).`);
    // Give the final word a little longer to finish its actual asset load.
    stressTimer = window.setTimeout(tick, stressClicks === 30 ? 2000 : 350);
  }
  stressTimer = window.setTimeout(tick, 350);
});

window.addEventListener('error', event => {
  runtimeError = event.message;
  log(`Runtime error: ${runtimeError}`);
  if (stressTimer !== undefined) stopStress(`FAIL: ${runtimeError}`);
  refresh();
});
window.addEventListener('unhandledrejection', event => {
  runtimeError = String(event.reason);
  log(`Unhandled rejection: ${runtimeError}`);
  if (stressTimer !== undefined) stopStress(`FAIL: ${runtimeError}`);
  refresh();
});
window.setInterval(refresh, 200);
log('Instrumentation installed before the application mounted.');
createRoot(root).render(<React.StrictMode><App/></React.StrictMode>);
