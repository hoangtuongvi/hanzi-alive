import {useEffect,useRef,useState} from 'react';
import type {CSSProperties} from 'react';
import type {ReconstructionProps} from './types';
import {reconstructionChoices,THEATRE_META} from './lessons';
import './glyphs.css';

export default function Reconstruction({lesson,onComplete}:ReconstructionProps) {
  const [slot,setSlot]=useState(0);
  const [feedback,setFeedback]=useState('');
  const [wrong,setWrong]=useState<string|null>(null);
  const optionsRef=useRef<HTMLDivElement>(null),successRef=useRef<HTMLDivElement>(null),advanceFocus=useRef(false);
  const complete=slot>=lesson.parts.length;
  const part=lesson.parts[Math.min(slot,lesson.parts.length-1)];
  const choices=reconstructionChoices(lesson,Math.min(slot,lesson.parts.length-1));
  const sense=THEATRE_META[lesson.word];
  useEffect(()=>{setSlot(0);setFeedback('');setWrong(null);},[lesson.word]);
  useEffect(()=>{
    if(!advanceFocus.current)return;
    advanceFocus.current=false;
    if(complete)successRef.current?.focus({preventScroll:true});
    else optionsRef.current?.querySelector('button')?.focus({preventScroll:true});
  },[slot,complete]);
  function choose(glyph:string) {
    if(complete)return;
    if(glyph!==part.glyph) {
      setWrong(glyph);
      setFeedback(`Try again. Remember the ${part.image} in the scene.`);
      return;
    }
    const nextSlot=slot+1;
    advanceFocus.current=true;
    setSlot(nextSlot);setWrong(null);
    if(nextSlot===lesson.parts.length) {
      setFeedback(`${lesson.word} — ${sense.meaning}. You brought every image back.`);
      onComplete();
    } else setFeedback(`${part.glyph} is your ${part.image}. Now find the next piece.`);
  }
  function reset(){advanceFocus.current=slot!==0;setSlot(0);setFeedback('');setWrong(null);if(slot===0)optionsRef.current?.querySelector('button')?.focus({preventScroll:true});}
  return <section className={`theatre-reconstruction${complete?' is-complete':''}`} aria-label="Rebuild the word">
    <div className="theatre-reconstruction-heading"><span className="theatre-recall-eyebrow">YOUR TURN</span><h3>Bring the story back.</h3><p>Rebuild the writing for <strong>{sense.meaning}</strong>.</p></div>
    <div className="theatre-recall-slots" aria-label="Your assembled pieces">
      {lesson.parts.map((piece,index)=><div key={index} className={`theatre-recall-slot${slot>index?' is-filled':''}${slot===index?' is-current':''}`} style={{'--piece-color':piece.color} as CSSProperties} aria-label={`${piece.image}: ${slot>index?piece.glyph:'empty'}`}>
        <span className="theatre-recall-piece">{slot>index?piece.glyph:'?'}</span><span>{piece.image}</span>
      </div>)}
    </div>
    {!complete?<><p className="theatre-recall-prompt" id={`recall-prompt-${lesson.scene}`}>Choose the writing for <strong>{part.image}</strong> <span>({slot+1} of {lesson.parts.length})</span></p>
      <div ref={optionsRef} className="theatre-recall-options" role="group" aria-labelledby={`recall-prompt-${lesson.scene}`}>
        {choices.map(glyph=><button type="button" key={`${slot}-${glyph}`} onClick={()=>choose(glyph)} className={wrong===glyph?'is-wrong':''} aria-label={`Choose ${glyph}`}><span lang="zh-Hans">{glyph}</span></button>)}
      </div></>:<div ref={successRef} tabIndex={-1} className="theatre-recall-success"><span lang="zh-Hans">{lesson.word}</span><div><strong>{sense.pinyin}</strong><p>{sense.meaning}</p></div></div>}
    <p className="theatre-recall-feedback" role="status" aria-live="polite">{feedback||'Picture each image, then choose its shape.'}</p>
    <button type="button" className="theatre-recall-reset" onClick={reset}>{complete?'Try it once more':'Start again'}</button>
  </section>;
}
