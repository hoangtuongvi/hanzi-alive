# Hanzi Alive

An automatic visual lesson for **休, 清, and 晴**. A word separates into its written parts, becomes an interactive 3D scene, and reveals a story connecting the images to its meaning.

The project now plans 1,251 word lessons: the original 1,000-word corpus plus 251 missing entries from the supplied HSK 1–4 workbook. The original three-word demo remains available, and a growing illustrated collection admits only words with authored scene assets. All 1,251 lessons have draft text and sourced stroke geometry; they are **not yet 1,251 finished illustrations**. See [the current coverage report](docs/word-coverage.md).

## Run

Use Node.js 20.19+ and Python 3.

```sh
npm ci
npm run dev
```

Open [the demo](http://localhost:5173/?view=theatre&word=休). All assets load locally; no account, API key, or runtime AI service is required.

Open [the illustrated collection](http://localhost:5173/?view=collection&word=休) to explore completed scene definitions, with the same simple Back/Next flow as the demo. Words without an illustration remain in the production queue instead of entering this collection.

The hosted demo uses Sites, configured in `.openai/hosting.json`, and serves the static production build from `dist/`. The current source collection contains **371 illustrated lessons** (29.7% of the 1,251-word corpus). Use `?view=collection&word=休` for the collection, or `?view=theatre&word=休` for the original three-word demo. A Git push does not itself republish the hosted demo.

```sh
npm test
npm run build
npm run preview
npm run coverage
npm run coverage:check
```

## The experience

In the original demo, **Back** and **Next** move between 休 → 清 → 晴, wrapping in either direction. The illustrated collection keeps those three first, followed by its other illustrated words. Each word starts a fresh automatic sequence; playback never advances to another word by itself.

1. The word and its pronunciation appear for two seconds while the model loads.
2. The writing unfolds into colored parts over a three-second phase.
3. The parts transition into a 3D illustration.
4. After three seconds on the visualization, its story appears beneath the same scene. The model and camera stay in place.
5. Where historical forms are available, evolution plays after eight seconds to read the story. 休 moves through oracle, bronze, seal, and modern forms, then returns to its scene and story. 清 and 晴 remain on their scene and story.

During the written-character breakdown, component labels align in a stable row along the bottom. As the parts become the visualization, the labels move into nearby open space around their matching objects and follow them as the model rotates: 日 stays beside the sun while 青 stays near the grass. Thin connector lines keep the association clear, and collision checks keep the text off the illustration. There are no stage headings, drag hints, menus, or step controls. Dragging still rotates the model; focused canvas controls support arrow keys, +/−, and 0 for reset. Transitions respect reduced-motion preferences. Playback pauses while the page is hidden or the model is unavailable.

Demo links support the original three words. Collection links use `?view=collection&word=…` and admit words registered in `src/explorer/scene-catalog.json`. Unsupported words return to 休. Each route loads the selected word's geometry and model on demand, retaining one renderer across word changes. Collection mode reads the full corpus metadata, then filters it to authored scene definitions.

## Images, writing, and history

Illustrated scenes are authored in **Blender 4.5 LTS** and exported as self-contained GLB models. The browser loads those models with Three.js, keeping the existing rotation, component labels, and timed transitions. 休 has a resting traveler and a broadleaf tree; 清 and 晴 share the same curved green grass and river stones. The expanding collection reuses that tree and meadow vocabulary across new, individually composed scenes. Scene meshes and materials are original project assets; no external model pack or texture service is required.

The collection includes 27 detailed scene builders and 344 compact explanation dioramas assembled from an original sculpted object library. Each diorama has an explicit word-specific recipe, ordered component anchors and its own mnemonic story. They cover nature, food, family, objects, counts, directions, actions, school, travel and emotions. They are draft learning illustrations, not independently reviewed etymologies. Reusable props broaden coverage; these are not 371 independently sculpted artworks. The remaining 880 words stay outside the illustrated collection, including the explicitly excluded 高手.

Editable Blender files live in `assets/blender/`, and browser exports live in `public/models/blender/`. The export manifest records Blender version, sizes, mesh counts, anchors, and checksums. If a model cannot load, an existing procedural illustration provides a fallback where available; otherwise the lesson pauses and offers a retry.

The mnemonic stories are invented memory connections, not historical derivations. For example, 清 uses: “Only in clear water can you see the green grass.” Green remains the image for 青 in both 清 and 晴.

The scene catalog holds the current presentation stories and any lesson-specific mnemonic labels. 好 uses a girl-and-boy family story, while the source dictionary component records remain separate. The production queue includes these presentation revisions. 高手 is excluded from the illustrated collection.

The 3D written forms use sourced stroke geometry from Make Me a Hanzi. The supplied reference assets provide 休’s oracle, bronze, and seal forms, each with a source link shown during its historical phase. The oracle form represents a Shang tradition; the bronze form a Western Zhou tradition; the seal form belongs to the tradition recorded in the Shuowen dictionary, rather than a dated Qin inscription. No historical forms are invented for 清 or 晴.

Reference asset notices remain in `public/reference/assets/`, and dataset licenses remain in `public/licenses/`. See [SOURCES.md](SOURCES.md) for the underlying corpus provenance.

## Rebuild the Blender assets

Open any `.blend` file in `assets/blender/` to inspect its geometry, materials, semantic label anchors, and preview lighting. The authoring scripts reproduce the scenes and exports:

```sh
blender --background --factory-startup --python-exit-code 1 --python scripts/blender/build_assets.py -- rest clear sunny --render
```

Use the path to your Blender executable if `blender` is not on PATH. On this development Mac it is `/Users/vi/Applications/Blender.app/Contents/MacOS/Blender`. Omit `--render` to skip preview PNGs, provide scene names to rebuild a batch, or use `--all` for every registered builder. Rendered previews go to `outputs/blender/`; the `.blend` files and GLBs are always saved. Blender's preview lighting is separate from the browser lighting. Export stops above 250,000 triangles per scene; instanced authoring data is copied before applying modifiers to avoid multiplying subdivisions.

To rebuild or resume the complete library, then admit verified exports and refresh coverage:

```sh
blender --background --factory-startup --python-exit-code 1 --python scripts/blender/build_assets.py -- --all --missing
python3 scripts/blender/sync_catalog.py
npm run coverage
npm test
npm run build
```

`--missing` skips existing native files paired with checksum-verified GLBs; changed explanation recipes or prop-library sources are rebuilt automatically. Use `--explanations` for just the modular dioramas, or omit `--missing` to rebuild all selected scenes. Catalog synchronization rejects missing files, stale recipes, mismatched component order and the exclusion list. Check it without writing with `npm run blender:check`.

The recipes in `scripts/blender/explanation_recipes.py` list exact objects, positions, sizes and stories. `explanation_props.py` contains the original geometry, and `explanation_scenes.py` composes it. No unsupported word receives a generic fallback illustration. Render contact sheets from saved native files without changing them:

```sh
blender --background --python-exit-code 1 --python scripts/blender/render_previews.py -- --all
```

With the development server running, open `/outputs/blender-review/page-1.html`. Preview images are ignored by Git; native sources, GLBs, scripts and manifests are checked in.

## Project organization

- `src/App.tsx` and `src/explorer/demo-lessons.ts`: three-word loading and URL handling.
- `src/explorer/Explorer.tsx` and `focused.css`: focused presentation and word controls.
- `src/explorer/focused-flow.ts`: playback phases, story copy, and word navigation.
- `src/explorer/ExplorerStage.tsx`: persistent 3D viewer, transitions, and component labels.
- `src/explorer/blender-models.ts`: cancellable GLB loading, authored anchor positions, transparency, and resource cleanup.
- `src/explorer/scene-catalog.json`: authored scene inventory, current story copy, mnemonic labels and ordered model anchors.
- `src/explorer/illustrated-lessons.ts`: scene-gated collection selection and URLs.
- `data/scene-production-queue.json`: all 1,251 lesson IDs with story, shared image cues and remaining illustration work.
- `scripts/audit_coverage.py`: reproducible word, glyph, story, model and source coverage.
- `scripts/blender/`: reproducible Blender scene creation and export.
- `src/explorer/usePlaybackTimer.ts`: visibility-aware playback timing.

The 1,251-word source corpus feeds the production queue and the growing illustrated collection. The former recall screens and visual-tutor service remain outside these routes. Original mnemonic curation lives in `data/curation/mnemonics/`; generated corpus data remains under `public/data/` for source comparison and validation. Nested written components follow source match paths; when a source does not prove a split, its strokes remain intact and neutral.

Tests cover demo-only data and routes, navigation in both directions, playback timing and cancellation, sourced forms, and the underlying corpus invariants. Production files are generated in `dist/` and use web-root asset paths.

For graphics lifecycle checks, run the development server and open `/tests/graphics-lifecycle.html`. Its controls exercise 30 Next clicks, actual WebGL context loss/restoration, and navigation while graphics are interrupted. The canvas identity and context count must stay constant during navigation, and the current lesson must resume after restoration. React StrictMode may create and retire one additional context at the initial development mount. This harness is excluded from the production build.
