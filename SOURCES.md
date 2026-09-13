# Sources and attribution

## Vocabulary

**Complete HSK Vocabulary**, by drkameleon and contributors:
https://github.com/drkameleon/complete-hsk-vocabulary/tree/7ac65bf1a6387d35f1ade478906172a19311c7f9

Snapshot: `7ac65bf1a6387d35f1ade478906172a19311c7f9`. Original source and MIT notice are preserved under `data/source/`; the notice is also served at `public/licenses/hsk-MIT.txt`. Source forms supply vocabulary, traditional spellings, Mandarin readings and dictionary senses. Four supplementary standalone characters are selected from Make Me a Hanzi.

The vocabulary source derives dictionary material from **CC-CEDICT**, by its contributors:
https://www.mdbg.net/chinese/dictionary?page=cc-cedict

CC-CEDICT uses Creative Commons Attribution-ShareAlike 4.0:
https://creativecommons.org/licenses/by-sa/4.0/

The pilot selects one sense per entry, shortens English glosses, chooses contextual readings, and adds original AI-authored memory scenes and explanations. The elements-2 revision rewrites all 1,000 word stories and adds 919 character mnemonics with a consistent image-cue inventory. Assigned mnemonic images are separate from dictionary meanings and historical roles. Dictionary-derived adaptations retain CC BY-SA 4.0 terms. The original scenes and connection notes are offered under CC BY-SA 4.0 as well. Source definitions remain distinguishable in `dictionaryMeanings`; the application does not claim independent linguistic review.

## Character structures and stroke outlines

**Make Me a Hanzi**, by skishore and contributors:
https://github.com/skishore/makemeahanzi/tree/bddc96d41bef78427ed0e034e9f7e31d71fd1b92

Snapshot: `bddc96d41bef78427ed0e034e9f7e31d71fd1b92`. Dictionary data uses LGPL version 3 or later. Stroke graphics derive from Arphic fonts and use the Arphic Public License. Original data and notices are preserved in `data/source/`; copies of the notices are in `public/licenses/`.

Changes: subset to the 919 selected characters, parse ideographic descriptions into trees, associate vocabulary usage IDs, and derive top-level stroke groups from source matches. Stroke path strings and medians are preserved. The viewer adds extrusion, material, lighting and motion at runtime. Unassigned strokes remain unassigned. Historical structure explanations are source analyses, not independently established facts.

Selected reference links point to the **Chinese University of Hong Kong Multi-function Chinese Character Database**:
https://humanum.arts.cuhk.edu.hk/Lexis/lexi-mf/

No historical glyph images or article passages from that site are bundled.

## Fonts and application dependencies

DM Sans and Libre Caslon Display are served locally with their SIL Open Font License notices in `public/licenses/`. Chinese glyph text uses the device's Chinese font fallbacks; the interactive glyphs use the sourced stroke paths.

React, Vite, Three.js and Lucide are dependencies listed in `package.json` and locked in `package-lock.json`. Their package distributions retain their own license notices. This attribution file does not replace any upstream terms.
