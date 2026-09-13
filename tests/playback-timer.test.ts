import test from 'node:test';
import assert from 'node:assert/strict';
import {createPlaybackTimer, type PlaybackClock} from '../src/explorer/playback-timer';

class FakeClock implements PlaybackClock<number> {
  private time = 0;
  private nextId = 0;
  private pending = new Map<number, {at:number; callback:()=>void}>();

  now = ():number => this.time;
  schedule = (callback:()=>void, delayMs:number):number => {
    const id = this.nextId++;
    this.pending.set(id, {at:this.time + delayMs, callback});
    return id;
  };
  cancel = (id:number):void => { this.pending.delete(id); };

  get pendingCount():number { return this.pending.size; }
  get pendingCallbacks():(()=>void)[] { return [...this.pending.values()].map(task => task.callback); }

  advance(ms:number):void {
    const target = this.time + ms;
    while (true) {
      const due = [...this.pending.entries()]
        .filter(([, task]) => task.at <= target)
        .sort(([idA, a], [idB, b]) => a.at - b.at || idA - idB)[0];
      if (!due) break;
      this.time = due[1].at;
      this.pending.delete(due[0]);
      due[1].callback();
    }
    this.time = target;
  }
}

test('the story waits for exactly 3,000 ms after the timer is enabled', () => {
  const clock = new FakeClock();
  let reveals = 0;
  const timer = createPlaybackTimer(3000, () => reveals++, clock);
  clock.advance(5000);
  assert.equal(reveals, 0);
  assert.equal(clock.pendingCount, 0);

  timer.setRunning(true);
  clock.advance(2999);
  assert.equal(reveals, 0);
  clock.advance(1);
  assert.equal(reveals, 1);
  assert.equal(clock.pendingCount, 0);
  timer.setRunning(false);
  timer.setRunning(true);
  clock.advance(3000);
  assert.equal(reveals, 1);
});

test('disabled or hidden time does not consume the remaining countdown', () => {
  const clock = new FakeClock();
  let reveals = 0;
  const timer = createPlaybackTimer(3000, () => reveals++, clock);
  timer.setRunning(true);
  clock.advance(1000);
  timer.setRunning(false);
  assert.equal(clock.pendingCount, 0);
  clock.advance(60000);
  assert.equal(reveals, 0);
  timer.setRunning(true);
  clock.advance(1000);
  timer.setRunning(false);
  clock.advance(60000);
  timer.setRunning(true);
  clock.advance(999);
  assert.equal(reveals, 0);
  clock.advance(1);
  assert.equal(reveals, 1);
});

test('repeated running updates do not restart or duplicate a countdown', () => {
  const clock = new FakeClock();
  let reveals = 0;
  const timer = createPlaybackTimer(3000, () => reveals++, clock);
  timer.setRunning(true);
  clock.advance(2000);
  timer.setRunning(true);
  assert.equal(clock.pendingCount, 1);
  clock.advance(1000);
  assert.equal(reveals, 1);
});

test('replacing a phase resets its duration and blocks an already queued old callback', () => {
  const clock = new FakeClock();
  let oldReveals = 0;
  let newReveals = 0;
  const oldPhase = createPlaybackTimer(3000, () => oldReveals++, clock);
  oldPhase.setRunning(true);
  const [queuedOldCallback] = clock.pendingCallbacks;
  clock.advance(2500);
  oldPhase.dispose();

  const newPhase = createPlaybackTimer(3000, () => newReveals++, clock);
  newPhase.setRunning(true);
  queuedOldCallback();
  clock.advance(2999);
  assert.equal(oldReveals, 0);
  assert.equal(newReveals, 0);
  clock.advance(1);
  assert.equal(newReveals, 1);
});

test('replacing a duration uses the new full delay', () => {
  const clock = new FakeClock();
  let reveals = 0;
  const original = createPlaybackTimer(3000, () => reveals++, clock);
  original.setRunning(true);
  clock.advance(2000);
  original.dispose();
  const replacement = createPlaybackTimer(500, () => reveals++, clock);
  replacement.setRunning(true);
  clock.advance(499);
  assert.equal(reveals, 0);
  clock.advance(1);
  assert.equal(reveals, 1);
});

test('a canceled callback cannot reveal the story after pause and resume', () => {
  const clock = new FakeClock();
  let reveals = 0;
  const timer = createPlaybackTimer(3000, () => reveals++, clock);
  timer.setRunning(true);
  const [canceledCallback] = clock.pendingCallbacks;
  clock.advance(1000);
  timer.setRunning(false);
  timer.setRunning(true);
  canceledCallback();
  assert.equal(reveals, 0);
  clock.advance(2000);
  assert.equal(reveals, 1);
});

test('disposing on unmount prevents the timer from restarting or firing', () => {
  const clock = new FakeClock();
  let reveals = 0;
  const timer = createPlaybackTimer(3000, () => reveals++, clock);
  timer.setRunning(true);
  const [queuedCallback] = clock.pendingCallbacks;
  timer.dispose();
  timer.setRunning(true);
  queuedCallback();
  clock.advance(10000);
  assert.equal(reveals, 0);
  assert.equal(clock.pendingCount, 0);
});

test('a null duration never schedules a callback', () => {
  const clock = new FakeClock();
  let reveals = 0;
  const timer = createPlaybackTimer(null, () => reveals++, clock);
  timer.setRunning(true);
  clock.advance(10000);
  timer.setRunning(false);
  timer.setRunning(true);
  assert.equal(reveals, 0);
  assert.equal(clock.pendingCount, 0);
});
