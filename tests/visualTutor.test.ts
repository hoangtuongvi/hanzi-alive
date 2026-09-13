import test from 'node:test';
import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {readFileSync} from 'node:fs';
import type {AddressInfo} from 'node:net';
import {THEATRE_LESSONS} from '../src/theatre/lessons';
import {buildTutorRequest,createVisualTutorHandler,validateTutorInput,validateTutorResponse} from '../server/visualTutor';
import {scriptedHint} from '../src/theatre/visualTutor';
import type {Lesson} from '../src/types';

const lesson=THEATRE_LESSONS.find(l=>l.word==='情')!;
const corpus:Lesson[]=JSON.parse(readFileSync('public/data/lessons.json','utf8'));
const screenshot='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aN8cAAAAASUVORK5CYII=';
const input={word:'情',selected:'青',progress:0.25,screenshot,question:'Why is this green?'};

test('Visual tutor rejects nonexistent parts, invalid frames and remote image URLs',()=>{
  assert.ok(validateTutorInput(input,lesson));
  for(const change of [{word:'sun'},{selected:'火'},{progress:NaN},{progress:1.1},{screenshot:'https://example.com/image.png'},{screenshot:'data:image/png;base64,YWJj'},{question:''}]) {
    assert.equal(validateTutorInput({...input,...change},lesson),null,JSON.stringify(change));
  }
});

test('Astra receives the actual PNG and authoritative lesson state, with bounded actions',()=>{
  const payload=buildTutorRequest(input,lesson,corpus.find(l=>l.word==='情')!);
  assert.equal(payload.model,'gpt-6-astra');assert.equal(payload.store,false);
  assert.equal(payload.input[0].content[1].image_url,screenshot);
  assert.ok(payload.input[0].content[0].text?.includes(lesson.story));
  assert.deepEqual(payload.text.format.schema.properties.highlight.enum,[...new Set(lesson.parts.map(p=>p.glyph)),null]);
  assert.ok(payload.instructions.includes('Always keep 青 as green'));
  assert.equal(validateTutorResponse({message:'Look at green.',highlight:'青',action:'highlight'},lesson)?.mode,'live');
  for(const change of [{highlight:'火'},{action:'execute'},{highlight:null},{message:''}])assert.equal(validateTutorResponse({message:'Look at green.',highlight:'青',action:'highlight',...change},lesson),null);
});

test('Authored hints remain explicitly scripted and preserve green in the whole green family',()=>{
  for(const word of ['清','晴','情','请']){
    const hint=scriptedHint(THEATRE_LESSONS.find(l=>l.word===word)!,'青','why green?');
    assert.equal(hint.mode,'scripted');assert.equal(hint.highlight,'青');assert.match(hint.message,/green/);assert.match(hint.message,/made-up memory story/);
  }
});

async function withServer(getKey:()=>string|undefined,request:typeof fetch,run:(url:string)=>Promise<void>){
  const handler=createVisualTutorHandler({root:process.cwd(),getKey,request});
  const server=createServer((req,res)=>{void handler(req,res,()=>{res.writeHead(404);res.end();});});
  await new Promise<void>(resolve=>server.listen(0,'127.0.0.1',resolve));
  const url=`http://127.0.0.1:${(server.address() as AddressInfo).port}`;
  try{await run(url);}finally{await new Promise<void>((resolve,reject)=>server.close(error=>error?reject(error):resolve()));}
}

test('No key reports unavailable and cannot pretend to produce a live answer',async()=>{
  let calls=0;
  await withServer(()=>undefined,async()=>{calls++;throw new Error('No request expected');},async url=>{
    const status=await fetch(`${url}/api/visual-tutor/status`);
    assert.deepEqual(await status.json(),{available:false,model:'gpt-6-astra'});
    const answer=await fetch(`${url}/api/visual-tutor`,{method:'POST',headers:{Origin:url,'Content-Type':'application/json'},body:JSON.stringify(input)});
    assert.equal(answer.status,503);assert.equal(calls,0);
  });
});

test('Local endpoint forwards image input and accepts only validated model actions',async()=>{
  let calls=0;let invalid=false;
  const request:typeof fetch=async(url,options)=>{
    calls++;assert.equal(url,'https://api.openai.com/v1/responses');
    const payload=JSON.parse(String(options?.body));
    assert.equal(payload.input[0].content[1].image_url,screenshot);
    return new Response(JSON.stringify({status:'completed',output:[{type:'message',content:[{type:'output_text',text:JSON.stringify({message:'See the green garden beside the heart.',highlight:invalid?'火':'青',action:'highlight'})}]}]}),{status:200});
  };
  await withServer(()=>'test-only-key',request,async url=>{
    const post=(origin=url)=>fetch(`${url}/api/visual-tutor`,{method:'POST',headers:{Origin:origin,'Content-Type':'application/json'},body:JSON.stringify(input)});
    const forbidden=await post('https://unrelated.example');assert.equal(forbidden.status,403);assert.equal(calls,0);
    const answer=await post();assert.equal(answer.status,200);assert.equal((await answer.json()).mode,'live');assert.equal(calls,1);
    invalid=true;const rejected=await post();assert.equal(rejected.status,502);assert.equal(calls,2);
  });
});
