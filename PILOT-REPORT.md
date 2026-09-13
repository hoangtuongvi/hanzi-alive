# Element-memory revision — 13 September 2026

Follow-up: ten illustrated, animated lessons now accompany this corpus in the Memory Theatre. See [THEATRE-REPORT.md](THEATRE-REPORT.md) for the implementation, provenance, and additional verification. The corpus-wide revision below remains unchanged.

The original pilot overemphasized usage examples and phonetic explanations. This revision makes element recognition and story-based reconstruction the primary learning flow across the entire 1,000-word selection.

## New teaching rule

Every visible element receives a stable image. Its role in the writing can be phonetic while its role in the mnemonic remains visual. Stories deliberately connect those images to the selected meaning. Dictionary facts remain accessible without displacing the mnemonic.

| Character | Images | Invented connection |
| --- | --- | --- |
| 清 | water + green | Water reflects green plants with visible clarity. |
| 晴 | sun + green | Sunshine makes green grass glow. |
| 情 | heart + green | A heart relaxes in green nature and feels its emotions. |
| 请 | speech + green | A green invitation says “please come.” |
| 睛 | eye + green | A green garden is reflected in the pupil. |
| 精 | rice + green | Green shoots contain the grain's imagined essence. |
| 猜 | animal + green | Guess which animal is hiding in green grass. |
| 静 | green + conflict | Green grass cushions a quarrel until it becomes quiet. |

These connections are mnemonic inventions. They are not claims about character origins, universal cultural symbolism, or physical causes.

## Corpus-wide work

All 1,000 word stories were rewritten. The 651 multi-character entries join character images into a word story. Selecting a character also reveals its own element story. Single-character lessons use that element story, with selected-sense overrides for grammar and polysemy. For instance, the rice image still supports 米, but its lesson story explicitly connects it to the selected meter sense.

There are 919 character mnemonics. Of these, 816 have ordered parts validated against the preserved source decomposition trees, allowing expansion of a named component into its own sourced parts. The other 103 use explicitly labeled whole-outline cues. Those are not claimed to have a complete verified split. This distinction is separate from the 90 characters with partial stroke-to-component mappings in the geometry source.

The source vocabulary, 919 distinct character geometries and 1,688 character occurrences are unchanged. No independent Chinese-language review or learner evaluation has been completed.

## Interface and practice

- Image cues appear beside the shapes and in the story card.
- Character tabs explain the parts inside multi-character words.
- 青 stays green in the rendered geometry and mnemonic labels.
- Search recognizes both component glyphs and their image names, including within multi-character words.
- Recall defaults to choosing a missing written element; meaning recognition remains an option.
- Earlier reviews and experiments remain stored and are distinguished from this revision.

## Verification

Nine application tests cover search, experiment assignment, meaning distractors, every entry's missing-element question, score calculation and saved-data validation. Corpus checks verify all 1,000 lessons, all 919 character mnemonics, ordered sourced parts, consistent image labels, selected dictionary forms and key readings. Dedicated checks ensure that all eight listed 青-family character stories explicitly retain green.

The production build passes. The separately loaded 3D viewer retains a size advisory of roughly 560 kB before gzip, 146 kB gzipped. Browser verification checks the revised 青 search, single- and multi-character lessons, the element study/recall flow, saved results and responsive layout. QA scores are kept apart from learner results.

Consistency tests establish coverage and application behavior. They do not establish that every story is memorable. Further review should identify weak or overly elaborate connections, ambiguous images, and stories that fail to recover the spelling or selected meaning. Learner testing should include delayed reconstruction of the elements, not only immediate recognition.
