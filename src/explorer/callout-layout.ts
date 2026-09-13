export interface ScreenPoint {x:number;y:number;}
export interface ScreenBounds {left:number;right:number;top:number;bottom:number;}
export interface CalloutMeasure {key:string;anchor:ScreenPoint;width:number;height:number;preferred?:ScreenPoint;}
export interface CalloutPlacement extends CalloutMeasure {x:number;y:number;visible:boolean;}
interface Candidate extends CalloutPlacement {score:number;box:ScreenBounds;}
const clamp=(value:number,min:number,max:number)=>Math.max(min,Math.min(max,value));
const intersects=(a:ScreenBounds,b:ScreenBounds,gap=0)=>a.left<b.right+gap&&a.right>b.left-gap&&a.top<b.bottom+gap&&a.bottom>b.top-gap;

/** Written parts share a stable bottom row, independent of their projected anchors. */
export function layoutBreakdownCallouts(measures:CalloutMeasure[],width:number,height:number):CalloutPlacement[] {
  if(!measures.length)return [];
  const margin=12,gap=8;
  const rowWidth=Math.min(440,Math.max(0,width-margin*2));
  const slotWidth=rowWidth/measures.length,rowLeft=(width-rowWidth)/2;
  const maxHeight=Math.max(...measures.map(item=>item.height));
  const y=clamp(height-maxHeight/2-margin,0,Math.max(0,height));
  const placed:ScreenBounds[]=[];
  return measures.map((item,index)=>{
    const halfWidth=item.width/2,halfHeight=item.height/2;
    const x=item.width>width-margin*2?width/2:clamp(rowLeft+slotWidth*(index+.5),margin+halfWidth,width-margin-halfWidth);
    const box={left:x-halfWidth,right:x+halfWidth,top:y-halfHeight,bottom:y+halfHeight};
    const visible=box.left>=margin&&box.right<=width-margin&&box.top>=margin&&box.bottom<=height-margin
      &&!placed.some(other=>intersects(box,other,gap));
    if(visible)placed.push(box);
    return {...item,x,y,visible};
  });
}

/** Find nearby empty space for each element, independently of other elements' height. */
export function layoutCallouts(measures:CalloutMeasure[],width:number,height:number,obstacles:ScreenBounds[]):CalloutPlacement[] {
  const margin=8,clearance=8;
  const candidates=(item:CalloutMeasure,extra:ScreenBounds[]=[]):Candidate[]=>{
    const found:Candidate[]=[],seen=new Set<string>();
    const preferred=item.preferred??{x:item.anchor.x<width/2?-1:1,y:-.2};
    const angle=Math.atan2(preferred.y,preferred.x),halfWidth=item.width/2,halfHeight=item.height/2;
    const occupied=[...obstacles,...extra];
    let best=Infinity;
    for(let radius=24;radius<Math.hypot(width,height)+Math.hypot(item.width,item.height);radius+=12){
      for(let direction=0;direction<24;direction++){
        const theta=angle+direction*Math.PI/12;
        const x=clamp(item.anchor.x+Math.cos(theta)*radius,margin+halfWidth,width-margin-halfWidth);
        const y=clamp(item.anchor.y+Math.sin(theta)*radius,margin+halfHeight,height-margin-halfHeight);
        const key=`${Math.round(x)},${Math.round(y)}`;if(seen.has(key))continue;seen.add(key);
        const box={left:x-halfWidth,right:x+halfWidth,top:y-halfHeight,bottom:y+halfHeight};
        if(box.left<margin||box.right>width-margin||box.top<margin||box.bottom>height-margin)continue;
        if(occupied.some(obstacle=>intersects(box,obstacle,clearance)))continue;
        const dx=x-item.anchor.x,dy=y-item.anchor.y;
        const centerDistance=Math.hypot(dx,dy);
        const edgeDistance=Math.hypot(Math.max(0,Math.abs(dx)-halfWidth),Math.max(0,Math.abs(dy)-halfHeight));
        if(edgeDistance<clearance)continue;
        const affinity=(dx*Math.cos(angle)+dy*Math.sin(angle))/Math.max(1,centerDistance);
        const score=edgeDistance+24*(1-affinity)+centerDistance*.035;
        found.push({...item,x,y,visible:true,box,score});best=Math.min(best,score);
      }
      // Once there is enough clear space, distant positions cannot improve proximity.
      if(radius>best+Math.hypot(halfWidth,halfHeight)+90)break;
    }
    return found.sort((a,b)=>a.score-b.score).slice(0,48);
  };
  const options=measures.map(item=>candidates(item));
  if(measures.length===2&&options.every(items=>items.length)){
    let pair:[Candidate,Candidate]|undefined,score=Infinity;
    for(const first of options[0])for(const second of options[1]){
      if(intersects(first.box,second.box,clearance))continue;
      if(first.score+second.score<score){pair=[first,second];score=first.score+second.score;}
    }
    if(pair)return pair;
  }
  const placed:ScreenBounds[]=[];
  return measures.map((item,index)=>{
    const best=options[index].find(candidate=>!placed.some(box=>intersects(candidate.box,box,clearance)))??candidates(item,placed)[0];
    if(best){placed.push(best.box);return best;}
    // A fully zoomed-in object can leave no free space. Never cover it with a label.
    return {...item,x:item.anchor.x,y:item.anchor.y,visible:false};
  });
}
