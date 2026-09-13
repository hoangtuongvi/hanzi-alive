# Memory theatre — first ten

Built on 13 September 2026, using the existing `elements-2` corpus. [Open the local preview](http://127.0.0.1:5173/?view=theatre&word=休).

The ten lessons pair independently moving painted objects with exact sourced Chinese strokes. Learners play or scrub the scene, separate and assemble its written pieces, then reconstruct the writing from image cues. Explicit steps and a Still steps toggle provide alternatives to playback. System reduced-motion preference initializes the toggle. The original 1,000-word library, 919 character geometries, reviews, and recall experiments remain available.

| Source ID | Entry | Selected sense | Scene action |
| --- | --- | --- | --- |
| w0001 | 休 · xiū | rest | A traveler approaches a tree and settles into its shade. |
| w0004 | 林 · lín | woods | A second tree grows beside the first. |
| w0006 | 清 · qīng | clear | Sediment settles; green plants become clearly reflected in water. |
| w0007 | 晴 · qíng | sunny | Clouds part and sunlight brightens the same green grass. |
| w0009 | 情 · qíng | feeling; emotion | A heart settles in green nature and feelings emerge. |
| w0008 | 请 · qǐng | please; invite | A green invitation opens beneath words of welcome. |
| w0017 | 手机 · shǒu jī | mobile phone | A hand lifts a small machine; it rings. |
| w0150 | 电脑 · diàn nǎo | computer | Electrical pulses pass through a brain and light a screen. |
| w0019 | 分手 · fēn shǒu | break up; part ways | A ribbon divides and two hands separate. |
| w0018 | 高手 · gāo shǒu | expert | A hand reaches high and makes the winning move. |

火山 was not in the selected corpus; 林 supplies the repeated-element example instead. These are invented mnemonic scenes. Green remains the image of 青 in all four illustrated members of that family; all eight green-family stories in the full corpus remain intact. Single-character lessons separate source components. Compounds separate whole characters; their inner component lessons remain in Explore.

## Artwork and sources

- `public/theatre/props.png`: one generated transparent atlas, 1448×1086, copied intact from the image tool output. Twelve reusable props are cropped by SVG viewports and animated through object transforms, opacity, paths, and timed pulses. No generated text is used for the Chinese writing.
- Generation used the built-in `image_gen.imagegen` tool. Its interface exposes no model selector or verified model ID. This asset is **not claimed as GPT-Image-2.5 Sunburst output**. The exact submitted prompt is in `public/theatre/asset-prompt.txt`; the asset checksum and detailed lesson manifest are in `public/theatre/manifest.json`.
- Glyph outlines and groups retain Make Me a Hanzi revision `bddc96d41bef78427ed0e034e9f7e31d71fd1b92`. Every stroke in these lessons is rendered exactly once. Color, separation, and recombination are teaching choices. Stroke and dictionary licenses remain in `public/licenses/`.
- Dictionary senses and readings come from the existing corpus. History is secondary, with outbound CUHK and source references; no historical glyph series was fabricated.

## Screenshot understanding

The local Vite server implements a real `gpt-6-astra` Responses request: a PNG captured from the currently displayed scene plus its lesson, selected element, progress, and learner question. Model output is constrained to text and validated highlight/replay/compare actions. Credentials stay in the server process. The preview-frame control lets the learner inspect and save the exact captured picture without uploading it.

No authenticated API credentials were available, so **no live Astra call was verified**. The current UI says “Guided hints · scripted”; those hints do not analyze images. A scripted 清/晴 comparison keeps green and highlights water versus sun. Integration tests use a mocked upstream response and do not establish real model quality or access. With a server-side `OPENAI_API_KEY`, the same local connection can be exercised; a remotely hosted static build would need its own server endpoint.

Official references: [Sunburst](https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst), [Astra](https://developers.openai.com/api/docs/models/gpt-6-astra), [image input](https://developers.openai.com/api/docs/guides/images-vision), [structured output](https://developers.openai.com/api/docs/guides/structured-outputs).

## Verification performed

- `npm test`: **18 passing tests**, plus the full 1,000-word and 919-character corpus checks. Added checks cover ten source IDs/readings/senses, exact stroke coverage, green consistency, reconstruction options, screenshot input, bounded actions, unavailable credentials, and the local endpoint.
- `npm run build`: passes. Theatre code loads separately. The existing lazy Three.js viewer retains its ~560 kB bundle advisory; no new Three.js dependency was added.
- Browser: all ten scenes change between opening and completed story states; each reveals two sourced pieces, assembles at full progress, and completes both reconstruction prompts successfully. Checked playback advancing, keyboard Home/End/arrow scrubbing, the 清/晴 hint, and actual captured artwork and glyph frames.
- Pointer and keyboard: all visible scene targets checked at initial and moved positions. Fixed SVG hit regions that previously included clipped atlas bounds, and corrected the overlapping traveler/tree targets. Final rest scene recheck selects 木 and 亻 correctly.
- Narrow browser viewport at **390×844**: no horizontal overflow; header controls are visible at 44×44; stage buttons are 90×63; recall choices are about 66×65. Still steps, wrong-answer retry, Enter/Space answers, focus progression, completion, and reset work. Fixed compound answers wrapping vertically. This was viewport testing, not physical-device testing or OS preference emulation.
- Screenshots: `outputs/theatre-mobile-scene.png`, `outputs/theatre-mobile-recall.png`, `outputs/theatre-mobile-recall-success.png`.

Theatre completion ticks last for the current page session. Existing stored reviews and experiment results keep their previous format. QA sessions use the existing separate namespace. No public deployment was performed. These checks establish working lessons; independent Chinese-language review and delayed retention testing remain outstanding.
