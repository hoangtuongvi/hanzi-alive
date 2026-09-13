export interface ExplorerPose {weights:number[];explode:number;labels:number;}
export const TRANSITION_DURATION=1100;
const clamp=(value:number)=>Math.max(0,Math.min(1,value));
export const easeTransition=(value:number)=>{const t=clamp(value);return t*t*(3-2*t);};

/** Convert a requested stop into a pose without animating through other stops. */
export function explorerPose(progress:number,hasHistory:boolean,hasScene:boolean,show3D:boolean):ExplorerPose {
  const position=clamp((Number.isFinite(progress)?progress:0)/100)*6;
  const segment=Math.min(5,Math.floor(position)),mix=easeTransition(position-segment);
  const order=[4,4,0,0,1,2,3],weights=[0,0,0,0,0];
  weights[order[segment]]+=1-mix;weights[order[segment+1]]+=mix;
  if(!hasHistory){weights[0]+=weights[1]+weights[2]+weights[3];weights[1]=weights[2]=weights[3]=0;}
  if(!show3D&&position<1)weights[4]*=easeTransition(position);
  if(!hasScene){weights[0]+=weights[4];weights[4]=0;}
  const explode=position<1?0:position<=2?easeTransition(position-1):position<=3?1-easeTransition(position-2):0;
  return {weights,explode,labels:clamp(weights[4]+explode*weights[0])};
}

/** Source outlines dissolve directly; no unselected historical form is introduced. */
export function blendExplorerPoses(from:ExplorerPose,to:ExplorerPose,amount:number):ExplorerPose {
  const t=clamp(amount),blend=(a:number,b:number)=>a+(b-a)*t;
  return {weights:from.weights.map((weight,index)=>blend(weight,to.weights[index])),explode:blend(from.explode,to.explode),labels:blend(from.labels,to.labels)};
}
