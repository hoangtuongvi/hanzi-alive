export interface ScreenPoint {x:number;y:number;}
export interface ScreenBounds {left:number;right:number;top:number;bottom:number;}
export interface CalloutMeasure {key:string;anchor:ScreenPoint;width:number;height:number;preferred?:ScreenPoint;}
export interface CalloutPlacement extends CalloutMeasure {x:number;y:number;visible:boolean;}
interface Candidate extends CalloutPlacement {score:number;box:ScreenBounds;}
const clamp=(value:number,min:number,max:number)=>Math.max(min,Math.min(max,value));
const intersects=(a:ScreenBounds,b:ScreenBounds,gap=0)=>a.left<b.right+gap&&a.right>b.left-gap&&a.top<b.bottom+gap&&a.bottom>b.top-gap;

/** Written parts keep stable, centered rows, independent of their projected anchors. */
export function layoutBreakdownCallouts(measures:CalloutMeasure[],width:number,height:number):CalloutPlacement[] {
  if(!measures.length)return [];
  const margin=12,gap=8;
  if(measures.length>2){
    const availableWidth=width-margin*2,availableHeight=height-margin*2;
    type Row={items:CalloutMeasure[];width:number;height:number};
    let best:Row[]|undefined,bestBalance=Infinity;
    function arrange(start:number,rows:Row[],usedHeight:number){
      if(start===measures.length){
        const average=rows.reduce((sum,row)=>sum+row.width,0)/rows.length;
        const balance=rows.reduce((sum,row)=>sum+(row.width-average)**2,0);
        if(!best||rows.length<best.length||(rows.length===best.length&&balance<bestBalance)){
          best=rows;bestBalance=balance;
        }
        return;
      }
      if(best&&rows.length>=best.length)return;
      let rowWidth=0,rowHeight=0;
      for(let end=start;end<measures.length;end++){
        rowWidth+=measures[end].width+(end>start?gap:0);rowHeight=Math.max(rowHeight,measures[end].height);
        if(rowWidth>availableWidth)break;
        const totalHeight=usedHeight+rowHeight+(rows.length?gap:0);
        if(totalHeight>availableHeight)continue;
        arrange(end+1,[...rows,{items:measures.slice(start,end+1),width:rowWidth,height:rowHeight}],totalHeight);
      }
    }
    arrange(0,[],0);
    if(best){
      let top=height-margin-best.reduce((sum,row)=>sum+row.height,0)-gap*(best.length-1);
      return best.flatMap(row=>{
        let left=(width-row.width)/2;
        const y=top+row.height/2;top+=row.height+gap;
        return row.items.map(item=>{
          const x=left+item.width/2;left+=item.width+gap;
          return {...item,x,y,visible:true};
        });
      });
    }
  }
  // Preserve the two-part demo's existing baseline and spacing. If a larger
  // set cannot fit even in rows, keep only the labels that fit without overlap.
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
  if(measures.length>2&&measures.length<=4&&options.every(items=>items.length)){
    // A bounded joint search lets a tree's label move aside for another tree,
    // instead of allowing the first label to consume the only available gap.
    let arrangements:{labels:Candidate[];score:number}[]=[{labels:[],score:0}];
    for(const choices of options){
      arrangements=arrangements.flatMap(arrangement=>choices.flatMap(choice=>
        arrangement.labels.some(label=>intersects(label.box,choice.box,clearance))?[]:
          [{labels:[...arrangement.labels,choice],score:arrangement.score+choice.score}]
      )).sort((a,b)=>a.score-b.score).slice(0,48);
      if(!arrangements.length)break;
    }
    if(arrangements[0]?.labels.length===measures.length)return arrangements[0].labels;
  }
  const placed:ScreenBounds[]=[];
  return measures.map((item,index)=>{
    const best=options[index].find(candidate=>!placed.some(box=>intersects(candidate.box,box,clearance)))??candidates(item,placed)[0];
    if(best){placed.push(best.box);return best;}
    // A fully zoomed-in object can leave no free space. Never cover it with a label.
    return {...item,x:item.anchor.x,y:item.anchor.y,visible:false};
  });
}
