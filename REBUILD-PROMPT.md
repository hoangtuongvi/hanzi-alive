# Rebuild Hanzi Alive from scratch

Build and deploy a complete, working prototype called **Hanzi Alive** for our Astra hackathon. This is a fresh implementation in a new folder, not a continuation of the old repository. Proceed with reasonable decisions and finish the product without stopping at a plan.

## Fresh project

- Create `/Users/pky/Documents/ChatGPT/hanzi-alive-fresh` as a new project. If it already contains work, choose a new timestamped sibling folder instead of overwriting it.
- Write the application from scratch. Do not clone or copy the old code, `.git` directory, Git history, hosting configuration, or project records.
- Initialize a new Git repository. All commits must use their actual creation time. Do not backdate commits, alter timestamps, or describe earlier work as newly created.
- The old project at `/Users/pky/Documents/ChatGPT/astra-chinese-hackathon` is only a conceptual reference. Leave it intact.

## Product and demo promise

Help someone understand and remember a Chinese character by revealing the picture behind it. The first complete lesson is **休 (xiū), rest**: a person beside a tree. Take inspiration from an interactive 3D anatomy dissection: the learner can rotate the character, separate its components, and explore how its written form changed.

The learning sequence is **Visual → Breakdown → Meaning → History**. The visual scene is the main landing experience. History comes last.

## Learning experience

1. **Visual:** Open on a beautiful, original Ghibli-style, hand-painted scene. One traveler in orange clothing and blue trousers rests with their back against a leafy green tree. Their face and legs point away from the trunk. Warm sunlight, a peaceful meadow, and a clear person/tree relationship. Keep the complete person visible on mobile. Avoid existing fictional characters and text inside the painting. Generate this artwork fresh. Offer an obvious “Explore in 3D” button for a colored, rotatable person-and-tree scene.
2. **Breakdown:** Reveal the two components **亻 + 木**. Match the person component to a warm orange/coral color and the tree component to green. Use real Chinese stroke shapes. Animate them separating like an exploded anatomical model. Allow dragging to rotate, with a reset-view control.
3. **Meaning:** Bring the components together into **休**. Introduce **xiū — rest**, with a short, memorable explanation connecting the resting person and tree to the character. Keep this easy for a beginner to understand.
4. **History:** Let the learner continue backwards from the modern character through seal, bronze, and oracle forms. Show a sourced glyph, script name, approximate period where supported, and one short explanation of what changed at each stop.

Use one continuous slider with six labeled stops: **Visual, Breakdown, Meaning, Seal, Bronze, Oracle**. Group the last three under History. Also provide previous/next controls and a replay control. The default is Visual. Moving the slider should give clear, smooth feedback without losing the current lesson state.

## Design and implementation

- Aim for a polished, memorable demo. Make the artwork and interactive character the focus, with restrained typography and minimal interface clutter.
- Use TypeScript, a lightweight web stack, and Three.js or React Three Fiber for real 3D geometry. Pick the simplest reliable implementation.
- Make the experience work on desktop and mobile, with accessible controls and reduced-motion support.
- Show the illustration while 3D loads. Provide a useful fallback if WebGL is unavailable.
- Build one excellent lesson. Do not add accounts, payments, a full curriculum, or handwriting recognition to this first slice.
- Use Astra throughout development. Explain its actual contribution honestly; do not claim a runtime AI tutor unless one is implemented.

## Content accuracy

Use reputable sources for the character structure and historical forms. Preserve source links and required asset licenses. Keep a distinction between historical evidence and illustrative teaching choices. Do not present invented mnemonic stories, clothing, 3D depth, or animated transitions as literal historical facts. Label uncertain dates or reconstructions clearly. Avoid substituting the same modern glyph in different fonts for real historical forms.

## Finish and verify

Run the build and relevant checks. I explicitly authorize browser testing: verify the default visual, every slider stop, the 3D toggle, rotation, reset, replay, keyboard controls, and mobile layout. Fix failures and report only checks that actually ran.

Deploy this as a new working site with its own hosting configuration. Create a new public GitHub repository for the finished project with fresh Git history and actual current timestamps. If `phuaky/hanzi-alive` still exists, use `phuaky/hanzi-alive-fresh`; do not overwrite the old repository. Invite **hoangtuongvi** as a collaborator with write access. Return the deployed URL, GitHub URL, exact local folder path, commit timestamp in Singapore time, and invitation status.
