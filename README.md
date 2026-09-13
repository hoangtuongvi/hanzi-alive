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

The three illustrated scenes are authored in **Blender 4.5 LTS** and exported as self-contained GLB models. The browser loads those models with Three.js, keeping the existing rotation, component labels, and timed transitions. 休 has a resting traveler and a broadleaf tree; 清 and 晴 share the same curved green grass and river stones, with transparent water or a sculptural sun respectively. Scene meshes and materials are original project assets; no external model pack or texture service is required.

Editable Blender files live in `assets/blender/`, and browser exports live in `public/models/blender/`. The export manifest records Blender version, sizes, mesh counts, anchors, and checksums. If a model cannot load, the existing procedural illustration provides a fallback.

The mnemonic stories are invented memory connections, not historical derivations. For example, 清 uses: “Only in clear water can you see the green grass.” Green remains the image for 青 in both 清 and 晴.

The 3D written forms use sourced stroke geometry from Make Me a Hanzi. The supplied reference assets provide 休’s oracle, bronze, and seal forms, each with a source link shown during its historical phase. The oracle form represents a Shang tradition; the bronze form a Western Zhou tradition; the seal form belongs to the tradition recorded in the Shuowen dictionary, rather than a dated Qin inscription. No historical forms are invented for 清 or 晴.

Reference asset notices remain in `public/reference/assets/`, and dataset licenses remain in `public/licenses/`. See [SOURCES.md](SOURCES.md) for the underlying corpus provenance.

## Rebuild the Blender assets

Open any `.blend` file in `assets/blender/` to inspect its geometry, materials, semantic label anchors, and preview lighting. The authoring scripts reproduce the scenes and exports:

```sh
blender --background --factory-startup --python-exit-code 1 --python scripts/blender/build_assets.py -- rest clear sunny --render
```

Use the path to your Blender executable if `blender` is not on PATH. On this development Mac it is `/Users/vi/Applications/Blender.app/Contents/MacOS/Blender`. Omit `--render` to skip preview PNGs, or provide one scene name to rebuild only that scene. Rendered previews go to `outputs/blender/`; the `.blend` files and GLBs are always saved. Blender's preview lighting is separate from the browser lighting.

## Project organization

- `src/App.tsx` and `src/explorer/demo-lessons.ts`: three-word loading and URL handling.
- `src/explorer/Explorer.tsx` and `focused.css`: focused presentation and word controls.
- `src/explorer/focused-flow.ts`: playback phases, story copy, and word navigation.
- `src/explorer/ExplorerStage.tsx`: persistent 3D viewer, transitions, and component labels.
- `src/explorer/blender-models.ts`: cancellable GLB loading, authored anchor positions, transparency, and resource cleanup.
- `scripts/blender/`: reproducible Blender scene creation and export.
- `src/explorer/usePlaybackTimer.ts`: visibility-aware playback timing.

The original 1,000-word source corpus and previous pilot modules remain as reference material, outside the active demo. The demo does not expose the former library, recall screens, or visual-tutor service, and it does not change saved pilot results. Original mnemonic curation lives in `data/curation/mnemonics/`; generated corpus data remains under `public/data/` for source comparison and validation.

Tests cover demo-only data and routes, navigation in both directions, playback timing and cancellation, sourced forms, and the underlying corpus invariants. Production files are generated in `dist/` and use web-root asset paths.

For graphics lifecycle checks, run the development server and open `/tests/graphics-lifecycle.html`. Its controls exercise 30 Next clicks, actual WebGL context loss/restoration, and navigation while graphics are interrupted. The canvas identity and context count must stay constant during navigation, and the current lesson must resume after restoration. React StrictMode may create and retire one additional context at the initial development mount. This harness is excluded from the production build.
