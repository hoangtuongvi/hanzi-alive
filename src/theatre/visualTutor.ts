import type {TheatreLesson} from './types';

export type TutorAction = 'highlight' | 'replay' | 'compare' | 'none';
export interface VisualHelp {mode:'live'|'scripted';message:string;highlight:string|null;action:TutorAction;}
export interface VisualHelpInput {word:string;selected:string|null;progress:number;screenshot:string;question:string;}

export async function requestVisualHelp(input:VisualHelpInput):Promise<VisualHelp> {
  const response = await fetch('/api/visual-tutor', {
    method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(input),
    signal:AbortSignal.timeout(40000),
  });
  if (!response.ok) throw new Error(response.status === 503 ? 'Live visual help is unavailable. Try the story hint.' : 'Visual help could not read this frame. Please try again.');
  const result = await response.json();
  if (result.mode !== 'live' || typeof result.message !== 'string' || !['highlight','replay','compare','none'].includes(result.action)) {
    throw new Error('Visual help returned an unreadable answer.');
  }
  return result;
}

/** Authored guidance, intentionally separate from the screenshot-reading model. */
export function scriptedHint(lesson:TheatreLesson, selected:string|null, question=''):VisualHelp {
  const part = lesson.parts.find(p=>p.glyph===selected) ?? lesson.parts[0];
  const green = lesson.parts.find(p=>p.glyph==='青');
  if (['清','晴'].includes(lesson.word) && question.includes('清') && question.includes('晴')) {
    return {mode:'scripted',highlight:lesson.word==='清'?'氵':'日',action:'compare',message:'Keep the same green image for 青. In 清, three water drops reveal green plants through clear water. In 晴, the sun lights up green grass on a sunny day. Look to the left: water means clear; sun means sunny.'};
  }
  if (green && (/green|青|colour|color|phonetic/i.test(question) || selected==='青')) {
    return {mode:'scripted',highlight:'青',action:'highlight',message:`Keep 青 as green in your memory picture. ${lesson.story} This is a made-up memory story; the writing reference can explain its sound role separately.`};
  }
  if (/again|replay|move|motion/i.test(question)) {
    return {mode:'scripted',highlight:part?.glyph??null,action:'replay',message:`Watch the action again: ${lesson.action}`};
  }
  return {mode:'scripted',highlight:part?.glyph??null,action:'highlight',message:`${part ? `${part.glyph} is your image of ${part.image}. ` : ''}${lesson.story}`};
}

const svgNS='http://www.w3.org/2000/svg';
const xlinkNS='http://www.w3.org/1999/xlink';
const paintProperties=['fill','fill-opacity','fill-rule','stroke','stroke-width','stroke-opacity','stroke-linecap','stroke-linejoin','stroke-dasharray','stroke-dashoffset','opacity','color','font-family','font-size','font-weight','font-style','letter-spacing','text-anchor','dominant-baseline','visibility','display','transform','transform-origin','transform-box','filter','clip-path','mask','paint-order','vector-effect'];

function readDataURL(blob:Blob):Promise<string> {
  return new Promise((resolve,reject)=>{const reader=new FileReader();reader.onload=()=>resolve(String(reader.result));reader.onerror=()=>reject(new Error('Could not read the scene artwork.'));reader.readAsDataURL(blob);});
}

function loadImage(url:string):Promise<HTMLImageElement> {
  return new Promise((resolve,reject)=>{const img=new Image();img.onload=()=>resolve(img);img.onerror=()=>reject(new Error('Could not capture the scene artwork.'));img.src=url;});
}

/** Capture only the lesson stage. SVG geometry, current transforms, and raster props
 * are copied from the displayed frame; no model-generated substitute is sent. */
export async function captureStage(element:HTMLElement):Promise<string> {
  await document.fonts.ready;
  const bounds=element.getBoundingClientRect();
  if (!bounds.width || !bounds.height) throw new Error('The lesson stage is not visible.');
  const svgs=Array.from(element.querySelectorAll('svg')).filter(svg=>!svg.parentElement?.closest('svg'));
  if (!svgs.length) throw new Error('The lesson scene is still loading.');
  const assetCache=new Map<string,Promise<string>>();
  const frames=svgs.map(svg=>{
    const rect=svg.getBoundingClientRect();
    const clone=svg.cloneNode(true) as SVGSVGElement;
    const originalNodes=[svg,...Array.from(svg.querySelectorAll('*'))];
    const cloneNodes=[clone,...Array.from(clone.querySelectorAll('*'))];
    originalNodes.forEach((node,index)=>{
      const style=getComputedStyle(node);
      const target=cloneNodes[index] as SVGElement;
      for (const property of paintProperties) {
        const value=style.getPropertyValue(property);
        if (value) target.style.setProperty(property,value.replace(/url\(["']?([^"')]+)["']?\)/g,(match,link:string)=>{
          const url=new URL(link,window.location.href);
          return url.origin===window.location.origin&&url.hash?`url("${url.hash}")`:match;
        }));
      }
      target.style.setProperty('animation','none');
      target.style.setProperty('transition','none');
    });
    let ancestorOpacity=1;
    let ancestor=svg.parentElement;
    while (ancestor && ancestor!==element.parentElement) {
      const style=getComputedStyle(ancestor);
      if (style.display==='none'||style.visibility==='hidden') ancestorOpacity=0;
      ancestorOpacity*=Number(style.opacity);
      ancestor=ancestor.parentElement;
    }
    // Its CSS layout is already represented by the actual bounding box below.
    clone.style.removeProperty('transform');
    clone.setAttribute('xmlns',svgNS);
    clone.setAttribute('width',String(rect.width));
    clone.setAttribute('height',String(rect.height));
    clone.style.width=`${rect.width}px`;
    clone.style.height=`${rect.height}px`;
    return {clone,rect,ancestorOpacity};
  });
  await Promise.all(frames.map(async({clone})=>{
    await Promise.all(Array.from(clone.querySelectorAll('image')).map(async node=>{
      const href=node.getAttribute('href')??node.getAttributeNS(xlinkNS,'href');
      if (!href || href.startsWith('data:')) return;
      const url=new URL(href,window.location.href);
      if (url.origin!==window.location.origin) throw new Error('The scene contains unavailable external artwork.');
      let asset=assetCache.get(url.href);
      if (!asset) {
        asset=fetch(url.href).then(async response=>{if(!response.ok)throw new Error('Scene artwork is still loading.');return readDataURL(await response.blob());});
        assetCache.set(url.href,asset);
      }
      node.removeAttributeNS(xlinkNS,'href');
      node.setAttribute('href',await asset);
    }));
  }));
  const scale=Math.min(1,1200/bounds.width,900/bounds.height);
  const canvas=document.createElement('canvas');
  canvas.width=Math.max(1,Math.round(bounds.width*scale));
  canvas.height=Math.max(1,Math.round(bounds.height*scale));
  const context=canvas.getContext('2d');
  if(!context)throw new Error('This browser cannot capture the scene.');
  const background=getComputedStyle(element).backgroundColor;
  context.fillStyle=background==='rgba(0, 0, 0, 0)'?'#fbf7eb':background;
  context.fillRect(0,0,canvas.width,canvas.height);
  for (const {clone,rect,ancestorOpacity} of frames) {
    if (!rect.width||!rect.height||!ancestorOpacity) continue;
    const url=URL.createObjectURL(new Blob([new XMLSerializer().serializeToString(clone)],{type:'image/svg+xml;charset=utf-8'}));
    try {
      const img=await loadImage(url);
      context.globalAlpha=ancestorOpacity;
      context.drawImage(img,(rect.left-bounds.left)*scale,(rect.top-bounds.top)*scale,rect.width*scale,rect.height*scale);
    } finally { URL.revokeObjectURL(url); }
  }
  return canvas.toDataURL('image/png');
}
