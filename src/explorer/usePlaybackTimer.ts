import {useEffect, useRef} from 'react';
import {createPlaybackTimer, type PlaybackTimer} from './playback-timer';

/** Count only enabled, visible time, and deliver the latest callback once per phase. */
export function usePlaybackTimer(
  phaseKey:string,
  durationMs:number|null,
  enabled:boolean,
  onElapsed:()=>void,
):void {
  const callbackRef = useRef(onElapsed);
  const timerRef = useRef<PlaybackTimer|null>(null);

  useEffect(() => {
    callbackRef.current = onElapsed;
  }, [onElapsed]);

  useEffect(() => {
    const timer = createPlaybackTimer(durationMs, () => callbackRef.current(), {
      now:() => performance.now(),
      schedule:(callback, delayMs) => window.setTimeout(callback, delayMs),
      cancel:handle => window.clearTimeout(handle),
    });
    timerRef.current = timer;
    return () => {
      timer.dispose();
      if (timerRef.current === timer) timerRef.current = null;
    };
  }, [phaseKey, durationMs]);

  useEffect(() => {
    const timer = timerRef.current;
    const syncVisibility = ():void => {
      timer?.setRunning(enabled && !document.hidden);
    };
    syncVisibility();
    document.addEventListener('visibilitychange', syncVisibility);
    return () => document.removeEventListener('visibilitychange', syncVisibility);
  }, [phaseKey, durationMs, enabled]);
}
