# Hanzi Alive — hackathon submission draft

Revised 13 September 2026 for **Vi + Kuan Yu**, pair **soil-rose**, after checking the latest work in “Redesign UI with 3D word journey.” The demo uses one screen and the **Next word** button, with automatic transitions inside each lesson. Public links and the final recording remain outstanding. No portal draft has been saved or submitted.

## Project name

Hanzi Alive

## Description · what does it do?

Hanzi Alive teaches Chinese through visual stories and interactive 3D. Characters unfold into their parts, then into scenes that connect shape to meaning. Starting with 休, 清, and 晴, we make learning the writing an invitation to explore Chinese culture.

## How did you use Astra?

We used Astra in Codex to turn our learning philosophy into a focused, one-screen experience: a character breaks into parts, becomes an interactive 3D scene, and reveals a memory story over that same scene. Astra helped us build the scene rendering and automatic transitions, work on implementation and content in parallel, and test and refine the result in the browser. We also used it to keep historical references distinct from invented memory cues. Our goal is to make learning Chinese an invitation to explore its culture as well as its writing.

## Product philosophy

Hanzi Alive begins with the visual structure of Chinese writing. Latin letters primarily represent sounds; Chinese characters generally represent meaningful language units with associated pronunciations. This is often called logographic writing, or more precisely a logosyllabary. Many Chinese words contain more than one character. This distinction gives us a starting point for connecting written forms, images, and meaning. [Unicode’s account of writing systems](https://unicode.org/versions/Unicode17.0.0/core-spec/chapter-6/).

Our ambition is cultural curiosity. Learning a character can prompt questions about the experiences and perspectives around a language: What does it mean to rest? What do people call good? What makes a place feel peaceful? We want learners to explore those questions through Chinese writing, stories, and historical sources.

The three-character demo starts that conversation with **休**, a person beside a tree, resting in its shade. The historical person-and-tree connection is supported by [CUHK’s character database](https://humanum.arts.cuhk.edu.hk/Lexis/lexi-mf/oraclePiece.php?piece=%E6%9C%A8). **清** and **晴** then show our learning method: reuse green as the memory image for 青, while changing water to sun. These two grass scenes are authored memory stories; 青 also has a phonetic role in the writing. Goodness and peace are questions motivating the product’s cultural direction, not additional lessons demonstrated in this recording.

## Best Project tracks

**Select now: Best example of Agentic Engineering.** Show the actual development process in the video: parallel work on scenes, content, and interface; integration; a test or browser check; and the resulting interaction. The project’s strongest current evidence is Astra’s contribution to building and checking the experience.

**Potential second selection: Best example of Visual Understanding.** Add this if the finished demo includes a verified Astra response to the scene the learner is actually viewing. The earlier tutor code accepts a screenshot and lesson state, but authenticated execution is unverified and the redesigned entry screen currently does not expose its controls. Recheck this when coding is finished. An attractive visual interface alone does not demonstrate the model understanding an image.

The form allows **up to two** tracks, so one supported selection is sufficient. There is currently no verified GPT-Live-1 or Agents API integration, and the generated artwork’s exact model was not exposed. Do not label it GPT-Image-2.5. Consider Computer Use only if the team has a concrete demonstration matching that track’s criteria.

## Links for the form

| Field | Current status | Final value |
| --- | --- | --- |
| Demo URL | Local app inspected; public address pending | To add |
| Video URL | Script prepared; recording and upload pending | To add |
| GitHub repository URL | Public GitHub repository | [hoangtuongvi/hanzi-alive](https://github.com/hoangtuongvi/hanzi-alive) |
| Show project in gallery | Team preference pending | To choose in portal |

Local rehearsal entry: [休 character journey](http://127.0.0.1:5173/?view=theatre&word=%E4%BC%91). This address is for the development machine, not the judges’ Demo URL.

## What the demo can substantiate

| Claim | Evidence in this snapshot |
| --- | --- |
| Character → automatic breakdown → 3D scene → story on the same scene | Latest source implements the automatic sequence; browser inspection confirmed the 休 scene and story together with one Next word control. The story appears after three seconds of the ready visualization. |
| 1,000 word lessons; 919 character entries with geometry | Counted from the bundled lesson and character data; also recorded in `public/data/manifest.json`. |
| Consistent memory images across related characters | 青 retains the green cue in 清 and 晴. See `src/theatre/lessons.ts` and the authored mnemonic corpus. These are learning associations. |
| Historical forms for 休 | The focused lesson automatically shows oracle → bronze → seal → modern, then returns to its scene and story. Entries without sourced history remain on their scene; historical coverage is limited to 休 in this demo. |
| Broader library and recall practice | The underlying app retains 1,000 lessons and immediate recall practice. These are outside the focused recording route and are not shown in the revised 90-second script. |
| Astra-assisted development | The task “Redesign UI with 3D word journey” records parallel scene/content work and browser inspection. Use a readable excerpt from that actual work in the recording. |

The current focused lesson has no timeline, step buttons, library navigation, recall controls, or tutor controls. The earlier theatre report describes a different interface. The revised video stays with the three character journeys and the Astra development evidence.

**Recording sequence to align:** the requested demo order is **休 → Next word → 清 → Next word → 晴**. The inspected `nextFocusedWord()` still follows the full corpus, beginning **休 → 木 → 人 → 林 → 森 → 清 → 晴**. The coding task needs to expose the requested three-word sequence before this script can be recorded with exactly those two clicks. No alternate tabs or hidden navigation are part of the script.

## Finish before submission

1. Finalize the running build, align Next word with **休 → 清 → 晴**, and rehearse the exact route in [VIDEO-SCRIPT.md](VIDEO-SCRIPT.md).
2. Add the public demo and accessible GitHub addresses. Open both as a judge without the team’s signed-in session.
3. Record and upload a video of **90 seconds or less**, including both the product demo and how Astra was used. Check that the shared link plays without requesting access.
4. Recheck track choices and any claims about the tutor against the final build.
5. Paste the fields above, choose the gallery preference, and save the portal draft. Submit before **13 September 2026, 3:30 pm SGT**; allow time to check the confirmation.

Portal requirements and deadline above are from the form supplied in this task. [Submission portal](https://astra-hackathon-singapore.openai.chatgpt.site/portal?tab=build).

## Optional LinkedIn post draft

What if learning a Chinese character also sparked curiosity about the culture around it?

We’re building Hanzi Alive for the GPT-6 Astra Hackathon in Singapore. A character unfolds into its parts, becomes a scene you can explore in 3D, and reveals a story that connects the picture to its meaning.

Our demo follows 休, 清, and 晴: a person resting beside a tree; green grass visible through clear water; sunlight over that same green grass. One screen, with Next word to continue.

Our ambition goes beyond remembering vocabulary. We want learners to ask about the experiences and perspectives around Chinese writing: What does rest look like? What makes something good? What feels peaceful?

We used Astra in Codex to build and check the scenes, automatic transitions, and focused interface. Historical references and invented memory stories each have their place in the experience.

Built by Vi and Kuan Yu · team soil-rose.

Watch the 90-second demo: [ADD VIDEO LINK]
Try it: [ADD PUBLIC DEMO LINK]

Hanzi Alive. See meaning. Explore culture.

*Publishing note: replace the placeholders and attach the demo video. The supplied portal says People’s Choice voting runs from 14 September 2026, 8:00 am to 16 September 2026, 11:59 pm SGT. Add a voting link only when the official link is available. This post has not been published.*
