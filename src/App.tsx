import {lazy, Suspense, useCallback, useEffect, useState} from 'react';
import type {Character, Lesson} from './types';
import {demoWordUrl, getDemoWord, isDemoWord, selectDemoCharacters, selectDemoLessons} from './explorer/demo-lessons';
import './explorer/focused.css';

const Explorer = lazy(() => import('./explorer/Explorer'));
interface DemoData {
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
  const [word, setWord] = useState(() => getDemoWord(window.location.search));
  const [error, setError] = useState('');

  useEffect(() => {
    const syncLocation = ():void => {
      const selected = getDemoWord(window.location.search);
      const canonical = demoWordUrl(selected);
      if (window.location.search !== canonical || window.location.hash) {
        window.history.replaceState(null, '', `${window.location.pathname}${canonical}`);
      }
      setWord(selected);
    };
    syncLocation();
    window.addEventListener('popstate', syncLocation);
    return () => window.removeEventListener('popstate', syncLocation);
  }, []);

  useEffect(() => {
    const controller = new AbortController();
    Promise.all([
      getJSON<Lesson[]>('/data/demo-lessons.json', controller.signal),
      getJSON<Record<string, Character>>('/data/demo-characters.json', controller.signal),
    ]).then(([loadedLessons, loadedCharacters]) => {
      if (controller.signal.aborted) return;
      const lessons = selectDemoLessons(loadedLessons);
      const characters = selectDemoCharacters(loadedCharacters, lessons);
      setData({lessons, characters});
    }).catch(() => {
      if (!controller.signal.aborted) setError('The character study could not load. Please try again.');
    });
    return () => controller.abort();
  }, []);

  const changeWord = useCallback((requested:string):void => {
    if (!isDemoWord(requested)) return;
    const target = demoWordUrl(requested);
    if (window.location.search !== target) {
      window.history.pushState(null, '', `${window.location.pathname}${target}`);
    }
    setWord(requested);
  }, []);

  return <div className="app-shell explorer-shell">
    {error ? <main className="app-error" role="alert">
      <h1>The character study couldn’t load.</h1>
      <p>{error}</p>
      <button className="primary" onClick={() => window.location.reload()}>Try again</button>
    </main> : data ? <Suspense fallback={<main className="app-loading" role="status">Opening the character study…</main>}>
      <Explorer lessons={data.lessons} characters={data.characters} word={word} onWordChange={changeWord}/>
    </Suspense> : <main className="app-loading" role="status">Opening the character study…</main>}
  </div>;
}
