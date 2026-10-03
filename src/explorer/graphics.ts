import {WebGLRenderer} from 'three';

export interface StageFailure {
  message:string;
  recovery:'retry-scene'|'browser-reload';
}

export class GraphicsInitializationError extends Error {
  constructor(readonly statusMessage:string,cause:unknown){
    super('The browser could not initialize 3D graphics.',{cause});
    this.name='GraphicsInitializationError';
  }
}

/** The creation event has the browser's reason; Three's thrown error does not. */
export function createExplorerRenderer(canvas:HTMLCanvasElement):WebGLRenderer {
  let statusMessage='';
  const capture=(event:Event)=>{
    const message=(event as WebGLContextEvent).statusMessage;
    if(message)statusMessage=message;
  };
  canvas.addEventListener('webglcontextcreationerror',capture);
  try{
    return new WebGLRenderer({canvas,antialias:true,alpha:true,powerPreference:'low-power'});
  }catch(cause){
    throw new GraphicsInitializationError(statusMessage,cause);
  }finally{
    canvas.removeEventListener('webglcontextcreationerror',capture);
  }
}

export function stageFailure(reason:unknown):StageFailure {
  if(reason instanceof GraphicsInitializationError){
    // Chromium clears its graphics block on browser-initiated navigation.
    // window.location.reload(), even from a button, does not clear that block.
    return {
      message:/\bblocked\b/i.test(reason.statusMessage)
        ?'Your browser has blocked 3D graphics after a graphics interruption. Use the browser’s Reload button to restart this view.'
        :'Your browser could not start 3D graphics. Use the browser’s Reload button to try again.',
      recovery:'browser-reload',
    };
  }
  return {message:'This lesson’s 3D view could not load. Try loading it again.',recovery:'retry-scene'};
}

export const interruptedGraphicsFailure:StageFailure={
  message:'The browser could not restore 3D graphics. Use the browser’s Reload button to restart this view.',
  recovery:'browser-reload',
};
