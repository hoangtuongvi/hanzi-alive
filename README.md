# Hanzi Alive — three-character demo

An automatic visual lesson for **休, 清, and 晴**. A word separates into its written parts, becomes an interactive 3D scene, and reveals a story connecting the images to its meaning.

## Run

Use Node.js 20.19+ and Python 3.

```sh
npm ci
npm run dev
```

Open [the demo](http://localhost:5173/?view=theatre&word=休). All assets load locally; no account, API key, or runtime AI service is required.

```sh
npm test
npm run build
npm run preview
```

## The experience

The only navigation controls are **Back** and **Next**. They move between 休 → 清 → 晴, wrapping in either direction. Each word starts a fresh automatic sequence; playback never advances to another word by itself.

1. The word and its pronunciation appear for two seconds while the model loads.
2. The writing unfolds into colored parts over a three-second phase.
3. The parts transition into a 3D illustration.
4. After three seconds on the visualization, its story appears beneath the same scene. The model and camera stay in place.
5. Where historical forms are available, evolution plays after eight seconds to read the story. 休 moves through oracle, bronze, seal, and modern forms, then returns to its scene and story. 清 and 晴 remain on their scene and story.

During the written-character breakdown, component labels align in a stable row along the bottom. As the parts become the visualization, the labels move into nearby open space around their matching objects and follow them as the model rotates: 日 stays beside the sun while 青 stays near the grass. Thin connector lines keep the association clear, and collision checks keep the text off the illustration. There are no stage headings, drag hints, menus, or step controls. Dragging still rotates the model; focused canvas controls support arrow keys, +/−, and 0 for reset. Transitions respect reduced-motion preferences. Playback pauses while the page is hidden or the model is unavailable.

Direct links support the three demo words. Unsupported words and earlier library routes return to 休. The app loads only `public/data/demo-lessons.json` and `public/data/demo-characters.json`, plus the selected word’s geometry and historical assets.

## Images, writing, and history

The mnemonic stories are invented memory connections, not historical derivations. For example, 清 uses: “Only in clear water can you see the green grass.” Green remains the image for 青 in both 清 and 晴.

The 3D written forms use sourced stroke geometry from Make Me a Hanzi. The supplied reference assets provide 休’s oracle, bronze, and seal forms, each with a source link shown during its historical phase. The oracle form represents a Shang tradition; the bronze form a Western Zhou tradition; the seal form belongs to the tradition recorded in the Shuowen dictionary, rather than a dated Qin inscription. No historical forms are invented for 清 or 晴.

Reference asset notices remain in `public/reference/assets/`, and dataset licenses remain in `public/licenses/`. See [SOURCES.md](SOURCES.md) for the underlying corpus provenance.

## Project organization

- `src/App.tsx` and `src/explorer/demo-lessons.ts`: three-word loading and URL handling.
- `src/explorer/Explorer.tsx` and `focused.css`: focused presentation and word controls.
- `src/explorer/focused-flow.ts`: playback phases, story copy, and word navigation.
- `src/explorer/ExplorerStage.tsx`: persistent 3D viewer, transitions, and component labels.
- `src/explorer/usePlaybackTimer.ts`: visibility-aware playback timing.

The original 1,000-word source corpus and previous pilot modules remain as reference material, outside the active demo. The demo does not expose the former library, recall screens, or visual-tutor service, and it does not change saved pilot results. Original mnemonic curation lives in `data/curation/mnemonics/`; generated corpus data remains under `public/data/` for source comparison and validation.

Tests cover demo-only data and routes, navigation in both directions, playback timing and cancellation, sourced forms, and the underlying corpus invariants. Production files are generated in `dist/` and use web-root asset paths.
