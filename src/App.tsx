import {lazy, Suspense, useCallback, useEffect, useState} from 'react';
import type {Character, Lesson} from './types';
import {demoWordUrl, getDemoWord, isDemoWord, selectDemoCharacters, selectDemoLessons} from './explorer/demo-lessons';
import {collectionWordUrl,selectIllustratedCharacters,selectIllustratedLessons} from './explorer/illustrated-lessons';
import './explorer/focused.css';

const Explorer = lazy(() => import('./explorer/Explorer'));
interface DemoData {
  collection:boolean;
  lessons:Lesson[];
  characters:Record<string, Character>;
}

async function getJSON<T,>(path:string, signal:AbortSignal):Promise<T> {
  const response = await fetch(path, {signal});
  if (!response.ok) throw new Error('The character study could not load. Please try again.');
  return response.json() as Promise<T>;
}

export default function App(){
  const [data, setData] = useState<DemoData|null>(null);
  const [collection,setCollection]=useState(()=>new URLSearchParams(window.location.search).get('view')==='collection');
  const [word, setWord] = useState(() => new URLSearchParams(window.location.search).get('word')||'休');
  const [error, setError] = useState('');

  useEffect(() => {
    const syncLocation = ():void => {
      const params=new URLSearchParams(window.location.search);
      const expanded=params.get('view')==='collection';
      setCollection(expanded);
      setWord(expanded?params.get('word')||'休':getDemoWord(window.location.search));
    };
    syncLocation();
    window.addEventListener('popstate', syncLocation);
    return () => window.removeEventListener('popstate', syncLocation);
  }, []);

  useEffect(() => {
    const controller = new AbortController();
    setError('');
    Promise.all([
      getJSON<Lesson[]>(collection?'/data/lessons.json':'/data/demo-lessons.json', controller.signal),
      getJSON<Record<string, Character>>(collection?'/data/characters.json':'/data/demo-characters.json', controller.signal),
    ]).then(([loadedLessons, loadedCharacters]) => {
      if (controller.signal.aborted) return;
      const lessons = collection?selectIllustratedLessons(loadedLessons):selectDemoLessons(loadedLessons);
      if(!lessons.length)throw new Error('No illustrated lessons are available.');
      const characters = collection?selectIllustratedCharacters(loadedCharacters,lessons):selectDemoCharacters(loadedCharacters, lessons);
      setData({lessons, characters,collection});
    }).catch(() => {
      if (!controller.signal.aborted) setError('The character study could not load. Please try again.');
    });
    return () => controller.abort();
  }, [collection]);

  useEffect(()=>{
    if(!data||data.collection!==collection)return;
    const selected=data.lessons.find(lesson=>lesson.word===word)?.word||data.lessons[0].word;
    const canonical=collection?collectionWordUrl(selected):demoWordUrl(selected);
    if(window.location.search!==canonical||window.location.hash)window.history.replaceState(null,'',`${window.location.pathname}${canonical}`);
    if(selected!==word)setWord(selected);
  },[data,collection,word]);

  const changeWord = useCallback((requested:string):void => {
    if (!data?.lessons.some(lesson=>lesson.word===requested)||(!collection&&!isDemoWord(requested))) return;
    const target = collection?collectionWordUrl(requested):demoWordUrl(requested);
    if (window.location.search !== target) {
      window.history.pushState(null, '', `${window.location.pathname}${target}`);
    }
    setWord(requested);
  }, [collection,data]);

  return <div className="app-shell explorer-shell">
    {error ? <main className="app-error" role="alert">
      <h1>The character study couldn’t load.</h1>
      <p>{error}</p>
      <button className="primary" onClick={() => window.location.reload()}>Try again</button>
    </main> : data&&data.collection===collection ? <Suspense fallback={<main className="app-loading" role="status">Opening the character study…</main>}>
      <Explorer lessons={data.lessons} characters={data.characters} word={word} onWordChange={changeWord}/>
    </Suspense> : <main className="app-loading" role="status">Opening the character study…</main>}
  </div>;
}
