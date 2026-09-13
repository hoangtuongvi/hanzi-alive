# Hanzi Alive — 90-second demo

Revised for Vi + Kuan Yu, team soil-rose, after checking the automatic lesson flow in “Redesign UI with 3D word journey” on 13 September 2026.

**One app screen. Two Next word clicks. 休 → 清 → 晴.** The character breaks down automatically, the 3D scene appears, and its story arrives on that same scene after three seconds. Let the app do the transitions; use Next word only to change characters. Keep the cultural purpose central, with a short excerpt of actual Astra development work near the end.

**Build detail still to align:** the current Next word implementation follows the full corpus and takes 休 to 木. The coding task must expose the requested 休 → 清 → 晴 sequence before the two-click recording below. The script does not use separate tabs, a library picker, or an edited-away series of intermediate words.

## Recording plan

| Time | Show | Say |
| --- | --- | --- |
| 0:00–0:08 | Start on **休** and its pinyin. Let the automatic breakdown reveal 亻 and 木, then the person/tree scene. Small overlay: **Hanzi Alive · Vi + Kuan Yu · soil-rose**. | “Latin letters mainly represent sounds. Chinese writing is logographic: characters connect sound and meaning. Hanzi Alive makes those connections visible.” |
| 0:08–0:16 | The rest story appears over the same 3D scene. Rotate gently, keeping the person and tree labels readable. | “Here is xiū: a person beside a tree, resting in its shade. You can rotate the scene.” |
| 0:16–0:31 | Let 休 automatically show **Oracle → Bronze → Seal → Today**, then return to its scene. Historical source links stay visible. Hold the returned scene for a beat before clicking Next word. | “The forms change, but the person and tree remain recognizable. Historical sources connect today’s writing with the lives and experiences behind it.” |
| 0:31–0:47 | Click **Next word** once for **清**, after 休’s scene has returned. The character separates into 氵 and 青, then becomes water and green grass. After three seconds of the scene, the story appears. | “Next, qīng. Water and green. The writing opens into a scene; three seconds later, the story appears: only in clear water can you see the green grass.” |
| 0:47–1:04 | Click **Next word** once for **晴**. Show 日 and 青, then the sun and green grass. Hold on the story when it arrives. | “Next, qíng. The green stays; water becomes sun. Sunlight over green grass gives us sunny. These memory stories connect shape and meaning; historical explanations stay separate.” |
| 1:04–1:17 | Keep the 晴 scene on screen and slowly rotate it. Let the cultural purpose land while the picture stays readable. | “Our ambition is cultural curiosity. What makes something good? What feels peaceful? We want learning Chinese to open conversations about the experiences and perspectives within Chinese culture.” |
| 1:17–1:27 | Show a short, readable excerpt of actual work in Codex: the requested automatic transition, Astra’s implementation, and a completed test or browser check. This is the development-evidence insert; the lesson itself stays in one tab. | “Astra helped us build the 3D scenes, automatic transitions, and focused interface, then test and refine them.” |
| 1:27–1:30 | End on the 晴 scene with **Hanzi Alive · See meaning. Explore culture.** Team names and final demo URL can appear as small text. | “Hanzi Alive. See meaning. Explore culture.” |

## Clean voiceover

Latin letters mainly represent sounds. Chinese writing is logographic: characters connect sound and meaning. Hanzi Alive makes those connections visible.

Here is xiū: a person beside a tree, resting in its shade. You can rotate the scene.

The forms change, but the person and tree remain recognizable. Historical sources connect today’s writing with the lives and experiences behind it.

Next, qīng. Water and green. The writing opens into a scene; three seconds later, the story appears: only in clear water can you see the green grass.

Next, qíng. The green stays; water becomes sun. Sunlight over green grass gives us sunny. These memory stories connect shape and meaning; historical explanations stay separate.

Our ambition is cultural curiosity. What makes something good? What feels peaceful? We want learning Chinese to open conversations about the experiences and perspectives within Chinese culture.

Astra helped us build the 3D scenes, automatic transitions, and focused interface, then test and refine them.

Hanzi Alive. See meaning. Explore culture.

## Rehearsal details

- **Use one tab:** begin at [休](http://127.0.0.1:5173/?view=theatre&word=%E4%BC%91). Once the demo order is aligned, use Next word for 清, then 晴. Use the final public address when deployed.
- **Warm up the same sequence:** rehearse all three lessons once to load their assets, then return to the starting URL in the same tab. Start recording before reloading 休 so its initial two-second character display is captured.
- **Let the lessons play:** the nominal phases are character for 2 seconds, parts for 3 seconds, scene for 3 seconds, then story over the scene. The story therefore appears about 8 seconds after a word starts, specifically 3 seconds after the visualization starts. Loading and a hidden page pause the relevant timers, so rehearse actual timing.
- **Let 休 complete its history:** its story holds for 8 seconds, then oracle, bronze, seal, and modern each hold for 3.5 seconds. It returns to the scene at roughly 30 seconds. 清 and 晴 hold on their scene and story until Next word.
- **Frame one screen:** include the scene, story, and Next word button. The latest inspected 休 scene fits the 1280×720 viewport. Keep the pointer clear of the story text and rotate slowly.
- **Capture real development evidence:** use the task titled “Redesign UI with 3D word journey.” Choose a short, legible excerpt showing the automatic-transition request, the change, and a completed check. Use checks from the finished build; do not use a stale test count.
- **Stay within 90 seconds:** rehearse aloud with the automatic transitions and pauses for the pictures. The final cultural lines are the product’s ambition; goodness and peace are not additional demo screens.

## Background for the cultural framing

Chinese writing is commonly described as logographic; Unicode’s more precise classification is a logosyllabary. Characters generally correspond to meaningful language units and syllables, and many words use multiple characters. The spoken introduction simplifies that distinction without treating every character as a literal picture. [Unicode, Writing Systems](https://unicode.org/versions/Unicode17.0.0/core-spec/chapter-6/).

For 休, the person-and-tree connection has historical support. [CUHK’s entry on 木 and related characters](https://humanum.arts.cuhk.edu.hk/Lexis/lexi-mf/oraclePiece.php?piece=%E6%9C%A8) describes 休 as a person resting in a tree’s shade. The video’s cultural questions are invitations to explore, rather than claims that a glyph proves what all Chinese people believe.

For 清 and 晴, keep green as the shared memory image for 青. It also has a sound role in these characters; the grass scenes are our mnemonic choices. The script identifies them as memory stories and keeps historical explanations separate.
