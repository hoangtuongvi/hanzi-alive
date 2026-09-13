import {createContext,useContext,useId,type KeyboardEvent,type ReactNode} from 'react';
import type {SceneProps} from './types';
import './scenes.css';

// The painted atlas has generous, uneven gutters: explicit crops preserve every object.
const sprites = {
  tree:[20,10,380,380],standing:[430,10,240,380],seated:[738,80,340,312],grass:[1070,60,375,325],
  heart:[30,415,340,290],sun:[397,392,333,322],cloud:[734,428,352,277],invitation:[1100,394,338,316],
  hand:[26,728,376,330],phone:[428,729,267,337],brain:[738,727,329,340],computer:[1095,720,335,340],
};
type SpriteName = keyof typeof sprites;
const clamp = (n:number) => Math.max(0, Math.min(1,n));
const ease = (n:number) => {const p=clamp(n);return p*p*(3-2*p);};
const mix = (a:number,b:number,t:number) => a+(b-a)*t;
const C={green:'#315e4b', mint:'#abc9a0', coral:'#cd7759', gold:'#d0a74d', blue:'#6c9cab', pink:'#bd7f7c', ink:'#254338'};

interface PropProps {kind:SpriteName;x:number;y:number;size:number;glyph?:string;label?:string;rotate?:number;flip?:boolean;opacity?:number;children?:ReactNode;}
type Selection=Pick<SceneProps,'highlight'|'onSelect'>;
const SceneSelection=createContext<Selection>({});
function objectInteraction(glyph:string,label:string,{highlight,onSelect}:Selection){return {
  role:'button',tabIndex:0,'aria-label':label,
  onClick:()=>onSelect?.(glyph),
  onKeyDown:(event:KeyboardEvent<SVGElement>)=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();onSelect?.(glyph);}},
  className:`scene-object scene-object-focus ${highlight===glyph?'is-highlighted':''}`,
  'data-element':glyph,
};}
function HitArea({glyph,label,x,y,width,height}:{glyph:string;label:string;x:number;y:number;width:number;height:number}){
  const selection=useContext(SceneSelection);
  return <rect x={x} y={y} width={width} height={height} rx={Math.min(width,height)*.17} {...objectInteraction(glyph,label,selection)}/>;
}
function Prop({kind,x,y,size,glyph,label,rotate=0,flip=false,opacity=1,children}:PropProps){
  const selection=useContext(SceneSelection),crop=sprites[kind];
  return <g className={`scene-artwork ${glyph&&selection.highlight===glyph?'is-highlighted':''}`} transform={`translate(${x} ${y}) rotate(${rotate} ${size/2} ${size/2})`} opacity={opacity} aria-hidden={opacity<.03?true:undefined}>
    <g transform={flip?`translate(${size} 0) scale(-1 1)`:undefined}>
      <svg width={size} height={size} viewBox={crop.join(' ')} overflow="hidden" aria-hidden="true">
        <image href="/theatre/props.png" x="0" y="0" width="1448" height="1086"/>
      </svg>
    </g>
    {children}
    {glyph&&opacity>=.03&&<HitArea glyph={glyph} label={label||kind} x={kind==='tree'?size*.39:9} y={kind==='tree'?size*.12:9} width={kind==='tree'?size*.53:size-18} height={kind==='tree'?size*.55:size-18}/>}
  </g>;
}

export default function SceneIllustration({scene,progress,reducedMotion,highlight,onSelect}:SceneProps){
  const uid=useId().replace(/:/g,'');
  const t=ease(progress/.48);
  const late=ease((t-.3)/.7);
  const early=ease(t/.65);
  const Shadow=({x,y,rx=90,opacity=.1}:{x:number;y:number;rx?:number;opacity?:number})=><ellipse cx={x} cy={y} rx={rx} ry="10" fill={C.green} opacity={opacity}/>;
  const Leaf=({x,y,angle=0,scale=1,opacity=1}:{x:number;y:number;angle?:number;scale?:number;opacity?:number})=><path d="M0 0 Q-18-29 1-44 Q21-24 0 0 M0 0 1-33" fill={C.green} stroke={C.green} strokeWidth="1.2" transform={`translate(${x} ${y}) rotate(${angle}) scale(${scale})`} opacity={opacity}/>;
  const Orbit=({cx,cy,r=130,opacity=.2}:{cx:number;cy:number;r?:number;opacity?:number})=><ellipse cx={cx} cy={cy} rx={r} ry={r*.27} fill="none" stroke={C.green} strokeWidth="1" strokeDasharray="3 8" opacity={opacity}/>;
  let content:ReactNode;

  switch(scene){
    case 'rest': content=<>
      <ellipse cx="540" cy="384" rx={150+30*t} ry="21" fill={C.green} opacity=".09"/>
      <path d="M166 399 Q298 376 414 391 T745 390" className="scene-ground"/>
      <Prop kind="tree" x={405} y={69} size={335} glyph="木" label="Tree: 木"/>
      <Prop kind="standing" x={mix(150,346,early)} y={134} size={250} rotate={mix(-7,2,early)} opacity={1-late} glyph={late<.5?'亻':undefined} label="Person: 亻"/>
      <Prop kind="seated" x={337} y={206} size={230} opacity={late} glyph={late>=.5?'亻':undefined} label="Resting person: 亻"/>
      <Prop kind="grass" x={545} y={302} size={142}/>
      <g opacity={late*.65} fill="none" stroke={C.green} strokeWidth="2" strokeLinecap="round">
        <path d="M383 237 Q370 224 381 210"/><path d="M398 217 Q388 204 400 193"/>
      </g>
      <Leaf x={487-32*t} y={160+112*t} angle={-40+80*t} scale={.35}/>
    </>;break;
    case 'woods': content=<>
      <path d="M180 392 Q450 365 729 391" className="scene-ground"/>
      <Shadow x={343} y={382} rx={104}/><Shadow x={569} y={382} rx={50+60*t} opacity={.04+.07*t}/>
      <Prop kind="tree" x={185} y={81} size={322} glyph="木" label="First tree: 木"/>
      <Prop kind="tree" x={mix(490,430,t)} y={mix(324,80,t)} size={mix(76,322,t)} glyph="木" label="Second tree: 木"/>
      <Prop kind="grass" x={321} y={311} size={145}/><Prop kind="grass" x={535} y={325} size={115} opacity={.25+.75*t}/>
      <path d={`M355 134 Q451 ${mix(133,61,t)} 550 134`} fill="none" stroke={C.green} strokeWidth="1.5" strokeDasharray="3 7" opacity={late*.32}/>
      <Leaf x={416} y={183-25*t} angle={40} scale={.3} opacity={late}/><Leaf x={516} y={224-40*t} angle={-35} scale={.27} opacity={late}/>
    </>;break;
    case 'clear': content=<>
      <Prop kind="grass" x={201} y={61} size={255} glyph="青" label="Green plants: 青"/>
      <Prop kind="grass" x={428} y={72} size={224} glyph="青" label="Green plants: 青"/>
      <g>
        <path d="M180 277 Q198 215 420 220 Q686 210 723 279 Q755 351 534 388 Q249 412 180 323 Q165 305 180 277Z" fill={`url(#${uid}-water)`}/>
        <path d="M180 277 Q198 215 420 220 Q686 210 723 279 Q755 351 534 388 Q249 412 180 323 Q165 305 180 277Z" fill="#9b7b59" opacity={.61*(1-t)}/>
        <g opacity={.12+.55*t} transform="translate(0 455) scale(1 -.64)" pointerEvents="none">
          <Prop kind="grass" x={241} y={184} size={176}/><Prop kind="grass" x={437} y={202} size={138}/>
        </g>
        {[0,1,2,3,4,5,6].map((n)=><ellipse key={n} cx={267+n*51} cy={mix(260+(n%3)*23,359+(n%2)*8,t)} rx={5+(n%2)*2} ry="3" fill="#977d5d" opacity={.45-.24*t}/>)}
        <path d="M227 276 Q303 253 374 267 M480 251 Q577 245 637 271 M306 346 Q399 363 487 348" fill="none" stroke="#fffef4" strokeWidth="3" strokeLinecap="round" opacity={.23+.64*t}/>
        <ellipse cx="450" cy="303" rx={128+45*t} ry={32+12*t} fill="none" stroke="#fdf9eb" strokeWidth="1.2" opacity={late*.55}/>
        <HitArea glyph="氵" label="Water: 氵" x={181} y={220} width={541} height={172}/>
      </g>
      <Leaf x={651} y={319} angle={75} scale={.38} opacity={.4+.6*t}/>
    </>;break;
    case 'sunny': content=<>
      <g transform={`translate(453 ${mix(228,154,t)})`} opacity={.35+.65*t}>
        {Array.from({length:12},(_,i)=><path key={i} d={`M0 -${91+9*t} L0 -${107+24*t}`} transform={`rotate(${i*30})`} stroke={C.gold} strokeWidth="2.5" strokeLinecap="round" opacity={.55*t}/>) }
        <Prop kind="sun" x={-98} y={-98} size={196}/>
        <HitArea glyph="日" label="Sun: 日" x={-104} y={-104} width={208} height={208}/>
      </g>
      <Prop kind="cloud" x={mix(260,87,t)} y={97} size={246} opacity={1-.36*t}/>
      <Prop kind="cloud" x={mix(429,606,t)} y={120-22*t} size={222} opacity={1-.3*t}/>
      <ellipse cx="450" cy="369" rx="239" ry="20" fill={C.green} opacity=".06"/>
      <g opacity={.46+.54*t}>
        <Prop kind="grass" x={196} y={209} size={250}/><Prop kind="grass" x={374} y={206} size={250}/><Prop kind="grass" x={540} y={242} size={204}/>
        <HitArea glyph="青" label="Green grass: 青" x={206} y={259} width={508} height={128}/>
      </g>
      <path d="M453 242 393 309 M474 239 510 298 M431 228 315 298" stroke={C.gold} strokeWidth="2" strokeDasharray="2 12" opacity={late*.65}/>
    </>;break;
    case 'emotion': content=<>
      <ellipse cx="450" cy="370" rx="222" ry="31" fill={C.green} opacity=".055"/>
      <Orbit cx={450} cy={365} r={195} opacity={.14}/>
      <Prop kind="grass" x={155} y={220} size={237} glyph="青" label="Green nature: 青"/>
      <Prop kind="grass" x={515} y={216} size={239} glyph="青" label="Green nature: 青"/>
      <Prop kind="grass" x={337} y={292} size={235} glyph="青" label="Green nature: 青"/>
      <g transform={`translate(450 ${mix(218,247,t)}) rotate(${mix(-13,0,t)}) scale(${1+.035*Math.sin(t*Math.PI*4)*(1-t)})`}>
        <ellipse cx="0" cy="0" rx={111+38*late} ry={99+32*late} fill="none" stroke={C.pink} strokeWidth="1.1" opacity={late*.22}/>
        <Prop kind="heart" x={-134} y={-134} size={268}/>
        <HitArea glyph="忄" label="Heart: 忄" x={-124} y={-115} width={248} height={230}/>
      </g>
      {[{x:376,y:151,c:C.gold},{x:532,y:150,c:C.blue},{x:447,y:112,c:C.pink},{x:573,y:225,c:C.coral}].map((p,i)=><g key={i} transform={`translate(${mix(450,p.x,late)} ${mix(220,p.y-19*late,late)})`} opacity={late}>
        <path d="M0 -10 Q13 2 0 10 Q-13 2 0 -10" fill={p.c}/><circle cy="-19" r="2" fill={p.c} opacity=".65"/>
      </g>)}
      <path d="M387 384 Q450 398 513 384" fill="none" stroke={C.green} strokeWidth="1.5" opacity={.2+.3*t}/>
    </>;break;
    case 'invite': content=<>
      <g opacity=".6" fill="none" stroke={C.green} strokeWidth="2.5" strokeLinecap="round">
        <path d="M253 382V200 Q255 88 450 88 Q645 88 647 200V382"/>
        <path d="M265 382V202 Q267 101 450 101 Q633 101 635 202V382" opacity=".35"/>
      </g>
      <Prop kind="grass" x={155} y={270} size={201}/><Prop kind="grass" x={567} y={267} size={203}/>
      <Leaf x={261} y={253} angle={-44} scale={.65}/><Leaf x={642} y={216} angle={43} scale={.65}/><Leaf x={616} y={151} angle={60} scale={.45}/>
      <g transform={`translate(${mix(398,339,t)} ${mix(197,153,t)}) rotate(${mix(-10,0,t)} 118 118)`}>
        <path d={`M28 102 117 ${mix(147,31,early)} 217 102V216H28Z`} fill={C.green} stroke="#224c3b" strokeWidth="1.5"/>
        <g clipPath={`url(#${uid}-invitation-window)`}><g transform={`translate(0 ${mix(114,29,late)})`}>
          <rect x="48" y="0" width="144" height="161" rx="3" fill="#fff9e8" stroke="#d6cbaa" strokeWidth="1.3"/>
          <path d="M117 102Q111 69 130 38" fill="none" stroke={C.green} strokeWidth="1.5"/>
          <Leaf x={118} y={85} angle={-42} scale={.39}/><Leaf x={123} y={67} angle={42} scale={.36}/><Leaf x={128} y={48} angle={-17} scale={.28}/>
          <path d="M88 123H150M102 135H136" stroke="#cbbda0" strokeWidth="1.5" strokeLinecap="round"/>
        </g></g>
        <g clipPath={`url(#${uid}-invitation-front)`}><Prop kind="invitation" x={0} y={0} size={235}/></g>
        <path d={`M28 102H217L117 ${mix(178,31,early)}Z`} fill={C.green} stroke="#527250" strokeWidth="1" opacity={1-early}/>
        <HitArea glyph="青" label="Green invitation: 青" x={26} y={25} width={194} height={196}/>
      </g>
      <g transform={`translate(${mix(278,216,late)} ${mix(160,112,late)}) scale(${.78+.22*late})`}>
        <path d="M0 15 Q0 0 18 0H147Q166 0 166 18V64Q166 81 147 81H62L33 101L37 81H18Q0 81 0 64Z" fill="#fdfaf0" stroke={C.coral} strokeWidth="2.5"/>
        <text x="83" y="48" textAnchor="middle" className="scene-note" fill={C.coral}>Please, come in</text>
        <HitArea glyph="讠" label="Words of invitation: 讠" x={0} y={0} width={167} height={102}/>
      </g>
      <path d="M397 368 Q450 350 508 368" className="scene-ground"/>
      <circle cx="451" cy="348" r={3+3*late} fill={C.gold} opacity={late}/>
    </>;break;
    case 'phone': content=<>
      <Shadow x={438} y={395} rx={145}/>
      <g transform={`translate(${mix(354,370,t)} ${mix(169,82,t)}) rotate(${mix(-24,0,t)} 109 109)`}>
        <Prop kind="phone" x={0} y={0} size={239}/>
        <g fill="none" stroke={C.gold} strokeWidth="3" strokeLinecap="round" opacity={late}>
          <path d="M37 81Q18 108 33 129M19 72Q-7 108 14 140M211 80Q232 107 217 130M229 71Q255 107 236 141"/>
        </g>
      </g>
      <Prop kind="hand" x={mix(213,252,t)} y={mix(244,186,t)} size={290} rotate={mix(-16,-5,t)} glyph="手" label="Hand lifting the phone: 手"/>
      <g transform={`translate(${mix(354,370,t)} ${mix(169,82,t)}) rotate(${mix(-24,0,t)} 109 109)`}>
        <HitArea glyph="机" label="Machine becoming a phone: 机" x={25} y={0} width={190} height={230}/>
      </g>
      <g opacity={.62*(1-late)} transform="translate(592 273)">
        <path d="M-30 17H32M-22 17V58M25 17V58" stroke={C.green} strokeWidth="3" strokeLinecap="round"/>
        <Prop kind="tree" x={-58} y={-103} size={121}/>
      </g>
      <path d={`M304 294 Q${mix(292,288,t)} ${mix(248,167,t)} 337 ${mix(236,161,t)}`} fill="none" stroke={C.coral} strokeWidth="1.6" strokeDasharray="3 7" opacity={.25+.3*t}/>
    </>;break;
    case 'computer': content=<>
      <path d="M178 384H735" className="scene-ground"/><path d="M249 388V414M680 388V414" stroke={C.green} strokeWidth="2" opacity=".18"/>
      <g>
        <path d="M170 147 144 206 178 198 154 258 216 180 181 189 208 140Z" fill={C.gold} stroke="#c3973e" strokeWidth="1.5"/>
        <path d="M206 199H265L280 174 299 223 317 199H376" fill="none" stroke={C.gold} strokeWidth="3" strokeLinecap="round" strokeDasharray="220" strokeDashoffset={220*(1-early)}/>
        <circle cx={mix(208,397,early)} cy="199" r="5" fill={C.gold} opacity={1-.5*late}/>
        <HitArea glyph="电" label="Electricity: 电" x={139} y={132} width={81} height={132}/>
      </g>
      <Prop kind="brain" x={271} y={99} size={239} glyph="脑" label="Brain: 脑"/>
      <g opacity={late}>
        <path d="M461 217H501L514 204 527 230 539 217H595" fill="none" stroke={C.gold} strokeWidth="3" strokeDasharray="160" strokeDashoffset={160*(1-late)}/>
        <circle cx={mix(462,583,late)} cy="217" r="4" fill={C.gold}/>
      </g>
      <g transform={`translate(491 ${mix(185,155,t)})`} opacity={.46+.54*late}>
        <ellipse cx="121" cy="218" rx="111" ry="9" fill={C.green} opacity=".08"/>
        <Prop kind="computer" x={0} y={0} size={263}/>
        <path d="M102 119 116 132 143 99" fill="none" stroke={C.green} strokeWidth="4" strokeLinecap="round" strokeLinejoin="round" opacity={late}/>
      </g>
      <circle cx="386" cy="212" r={91+16*t} fill="none" stroke={C.gold} strokeWidth="1.2" strokeDasharray="3 10" opacity={late*.4}/>
    </>;break;
    case 'parting': content=<>
      <Shadow x={mix(354,271,t)} y={388} rx={84}/><Shadow x={mix(548,629,t)} y={388} rx={84}/>
      <g>
        <path d={`M${mix(371,290,t)} 278 Q382 ${281+19*t} ${mix(450,408,t)} ${280+62*t}`} fill="none" stroke={C.coral} strokeWidth="8" strokeLinecap="round"/>
        <path d={`M${mix(450,490,t)} ${280+62*t} Q518 ${281+19*t} ${mix(529,609,t)} 278`} fill="none" stroke={C.coral} strokeWidth="8" strokeLinecap="round"/>
        <g transform={`translate(450 ${mix(105,257,early)}) rotate(-24)`}>
          <path d="M-6 7H10V-50Q8-62 2-62Q-6-62-6-50Z" fill={C.green}/>
          <path d="M-6 4H12V48Q12 68-6 75Z" fill="#c9d6d0" stroke={C.green} strokeWidth="1.5"/>
        </g>
        <HitArea glyph="分" label="Dividing a ribbon: 分" x={413} y={95} width={74} height={250}/>
      </g>
      <Prop kind="hand" x={mix(210,124,t)} y={181} size={275} rotate={29} glyph="手" label="Left hand: 手"/>
      <Prop kind="hand" x={mix(417,501,t)} y={181} size={275} flip rotate={-29} glyph="手" label="Right hand: 手"/>
      <g stroke={C.coral} strokeWidth="1.5" opacity={late*.7}>
        <path d="M431 322 420 332 M469 322 480 332 M450 344V356"/>
      </g>
      <path d={`M${mix(349,272,t)} 412H${mix(377,300,t)} M${mix(526,606,t)} 412H${mix(554,634,t)}`} stroke={C.green} strokeWidth="1.5" opacity=".3"/>
    </>;break;
    case 'expert': content=<>
      <g transform="translate(227 317)">
        <path d="M0 21 326 0 454 56 118 91Z" fill="#e8dfc4" stroke={C.green} strokeWidth="1.5"/>
        {[1,2,3,4].map(n=><path key={n} d={`M${n*65} ${21-n*4.2} L${118+n*67} ${91-n*7}`} stroke={C.green} strokeWidth="1" opacity=".3"/>)}
        {[1,2,3].map(n=><path key={n} d={`M${n*29.5} ${21+n*17.5} L${326+n*32} ${n*14}`} stroke={C.green} strokeWidth="1" opacity=".3"/>)}
        {[[120,38],[216,26],[305,55]].map(([x,y],i)=><g key={i}><ellipse cx={x} cy={y} rx="13" ry="6" fill={i===1?C.coral:C.green}/><ellipse cx={x} cy={y-4} rx="13" ry="6" fill={i===1?'#e49b7c':'#507b5e'}/></g>)}
      </g>
      <g>
        <path d="M274 300V113M264 128 274 113 284 128" fill="none" stroke={C.gold} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" strokeDasharray="3 7"/>
        <circle cx="274" cy={mix(300,121,t)} r="5" fill={C.gold}/>
        <HitArea glyph="高" label="A high reach: 高" x={256} y={109} width={36} height={203}/>
      </g>
      <Prop kind="hand" x={mix(355,369,t)} y={mix(125,27,early)} size={296} rotate={mix(12,-13,t)} glyph="手" label="Expert hand reaching high: 手"/>
      <g transform={`translate(${mix(491,495,t)} ${mix(213,351,late)})`}>
        <ellipse cx="0" cy="5" rx="17" ry="7" fill="#9c732c"/><ellipse cx="0" cy="0" rx="17" ry="7" fill={C.gold}/>
      </g>
      <g transform="translate(496 350)" stroke={C.gold} strokeWidth="2" strokeLinecap="round" opacity={late}>
        <path d="M-31-2H-42M30-2H42M-22-17-30-24M22-17 30-24M0-22V-33"/>
      </g>
    </>;break;
  }

  return <SceneSelection.Provider value={{highlight,onSelect}}><svg className={`scene-illustration scene-${scene}`} viewBox="0 0 900 500" role="group" aria-label="Animated memory scene. Select an object to connect it with its written element." data-scene={scene} data-motion-reduced={reducedMotion}>
    <defs>
      <radialGradient id={`${uid}-wash`}><stop stopColor="#e1e8d7" stopOpacity=".55"/><stop offset="1" stopColor="#e1e8d7" stopOpacity="0"/></radialGradient>
      <linearGradient id={`${uid}-water`} x1="0" y1="0" x2="0" y2="1"><stop stopColor="#b6d5c6"/><stop offset="1" stopColor="#6b9a98" stopOpacity=".58"/></linearGradient>
      <clipPath id={`${uid}-invitation-front`}><path d="M27 97 117 153 219 98 219 219 27 219Z"/></clipPath>
      <clipPath id={`${uid}-invitation-window`}><path d="M27 0H219V218H27Z"/></clipPath>
    </defs>
    <ellipse cx="450" cy="279" rx="310" ry="199" fill={`url(#${uid}-wash)`} pointerEvents="none"/>
    {content}
  </svg></SceneSelection.Provider>;
}
