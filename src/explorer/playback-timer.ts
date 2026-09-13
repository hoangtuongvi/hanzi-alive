export interface PlaybackClock<Handle> {
  now:()=>number;
  schedule:(callback:()=>void, delayMs:number)=>Handle;
  cancel:(handle:Handle)=>void;
}

export interface PlaybackTimer {
  setRunning:(running:boolean)=>void;
  dispose:()=>void;
}

/** One phase's countdown. Replacing it starts a fresh phase with the full duration. */
export function createPlaybackTimer<Handle>(
  durationMs:number|null,
  onElapsed:()=>void,
  clock:PlaybackClock<Handle>,
):PlaybackTimer {
  let remaining = durationMs === null ? null : Math.max(0, durationMs);
  let startedAt = 0;
  let running = false;
  let elapsed = false;
  let disposed = false;
  let handle:Handle|undefined;
  let generation = 0;

  const cancel = ():void => {
    generation++;
    if (handle !== undefined) clock.cancel(handle);
    handle = undefined;
  };

  const schedule = ():void => {
    const scheduledGeneration = ++generation;
    handle = clock.schedule(() => {
      if (disposed || elapsed || !running || scheduledGeneration !== generation) return;
      handle = undefined;
      const now = clock.now();
      remaining = Math.max(0, remaining! - Math.max(0, now - startedAt));
      startedAt = now;
      // A scheduler can round fractional delays down. Never finish early.
      if (remaining > 0) {
        schedule();
        return;
      }
      running = false;
      elapsed = true;
      onElapsed();
    }, remaining!);
  };

  return {
    setRunning(nextRunning:boolean):void {
      if (disposed || elapsed || remaining === null || running === nextRunning) return;
      if (!nextRunning) {
        remaining = Math.max(0, remaining - Math.max(0, clock.now() - startedAt));
        running = false;
        cancel();
        return;
      }
      running = true;
      startedAt = clock.now();
      schedule();
    },
    dispose():void {
      disposed = true;
      running = false;
      cancel();
    },
  };
}
