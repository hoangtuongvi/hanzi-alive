import type {Lesson,Session,Saved} from './types';
export const normalize=(s:string)=>s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f\s]/g,'');
export function matchesQuery(l:Lesson,q:string){const n=normalize(q);return !n||[l.word,l.traditional,l.pinyin,l.meaning,l.memorySearch,...l.memoryElements.flatMap(e=>[e.glyph,e.image])].some(s=>normalize(s).includes(n));}
export function shuffle<T>(xs:T[],random:()=>number=Math.random):T[]{const a=[...xs];for(let i=a.length-1;i>0;i--){const j=Math.floor(random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
export function planExperiment(pool:Lesson[],count=20,random:()=>number=Math.random){const words=shuffle(pool,random).slice(0,count);const conditions=shuffle(words.map((_,i)=>i%2===0?'story' as const:'definition' as const),random);return words.map((lesson,i)=>({lesson,condition:conditions[i]}));}
export function overlappingMeanings(a:string,b:string){
 const glosses=(s:string)=>s.toLowerCase().split(/[;,]/).map(g=>g.trim().replace(/^to /,'').replace(/[^a-z0-9 ]/g,'').replace(/\s+/g,' ').trim()).filter(Boolean);
 const left=glosses(a),right=glosses(b);return left.some(g=>right.includes(g));
}
export function distractors(l:Lesson,pool:Lesson[],random:()=>number=Math.random){const candidates=shuffle(pool.filter(x=>x.id!==l.id),random).sort((a,b)=>Number(b.strategy===l.strategy)-Number(a.strategy===l.strategy));const choices=[l.meaning];for(const c of candidates){if(!choices.some(meaning=>overlappingMeanings(meaning,c.meaning)))choices.push(c.meaning);if(choices.length===4)break;}return shuffle(choices,random);}
export function summarize(sessions:Session[]){return (['story','definition'] as const).map(condition=>{const trials=sessions.flatMap(s=>s.trials).filter(t=>t.condition===condition);return {condition,total:trials.length,correct:trials.filter(t=>t.correct).length,meanStudyMs:trials.length?trials.reduce((s,t)=>s+t.studyMs,0)/trials.length:0};});}
export const EMPTY:Saved={version:1,reviews:{},sessions:[]};
export function isSaved(x:unknown):x is Saved {if(!x||typeof x!=='object')return false;const s=x as Saved;const duration=(n:unknown)=>typeof n==='number'&&Number.isFinite(n)&&n>=0;return s.version===1&&!!s.reviews&&typeof s.reviews==='object'&&!Array.isArray(s.reviews)&&Array.isArray(s.sessions)&&Object.values(s.reviews).every(r=>r&&['helpful','misleading','unclear'].includes(r.verdict)&&typeof r.note==='string'&&typeof r.updatedAt==='string')&&s.sessions.every(v=>v&&typeof v.id==='string'&&typeof v.date==='string'&&Array.isArray(v.trials)&&v.trials.every(t=>t&&['story','definition'].includes(t.condition)&&typeof t.correct==='boolean'&&typeof t.lessonId==='string'&&typeof t.selected==='string'&&duration(t.responseMs)&&duration(t.studyMs)));}

export function elementQuestion(l:Lesson,pool:Lesson[],random:()=>number=Math.random){
 const missing=Math.floor(random()*l.memoryElements.length), answer=l.memoryElements[missing];
 const candidates=[...new Set(pool.flatMap(w=>w.memoryElements.map(e=>e.glyph)))].filter(g=>!l.memoryElements.some(e=>e.glyph===g));
 const choices=shuffle([answer.glyph,...shuffle(candidates,random).slice(0,3)],random);
 return {missing,answer,choices};
}
