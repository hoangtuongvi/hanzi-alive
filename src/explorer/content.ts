import {componentColor, type Lesson} from '../types';
import {THEATRE_LESSONS} from '../theatre/lessons';
import {getSceneDefinition} from './scene-catalog';

export const JOURNEY_STOPS = [
  {key:'visual', label:'Image', subtitle:'The scene', value:0},
  {key:'explorer', label:'3D explorer', subtitle:'Look around', value:100 / 6},
  {key:'components', label:'Breakdown', subtitle:'The parts', value:200 / 6},
  {key:'meaning', label:'Meaning', subtitle:'The word', value:50},
  {key:'seal', label:'Seal', subtitle:'History', value:400 / 6},
  {key:'bronze', label:'Bronze', subtitle:'History', value:500 / 6},
  {key:'oracle', label:'Oracle', subtitle:'History', value:100},
] as const;

export interface ExplorerContent {
  title:string;
  description:string;
  note:string;
  next:string;
  period:string;
  source?:string;
}

export interface ExplorerPart {
  glyph:string;
  image:string;
  color:string;
}

const restSource = 'https://humanum.arts.cuhk.edu.hk/Lexis/lexi-mf/search.php?word=%E4%BC%91';
const explorerColors:Record<string,string> = {
  '#d37c53':'#ebb08d',
  '#315e4b':'#9bcb81',
  '#527f91':'#95c1d2',
  '#c29a39':'#e2c579',
  '#8b86ad':'#c2b6e5',
  '#b97568':'#e5a89d',
};
const explorerColor = (color:string):string => explorerColors[color] || color;

/** Historical assets and their provenance are supplied for this character only. */
export function historyAvailable(lesson:Lesson):boolean {
  return lesson.word === '休';
}

export function getExplorerParts(lesson:Lesson):ExplorerPart[] {
  const theatreLesson = THEATRE_LESSONS.find(item => item.word === lesson.word);
  const parts=theatreLesson?theatreLesson.parts.map(({glyph,image,color})=>({glyph,image,color:explorerColor(color)})):
    lesson.memoryElements.map(({glyph, image}, index) => ({
    glyph, image, color:explorerColor(componentColor(glyph, index)),
  }));
  const images=getSceneDefinition(lesson.word)?.mnemonicImages;
  return parts.map(part=>({...part,image:images?.[part.glyph]??part.image}));
}

const restHistory:ExplorerContent[] = [
  {
    period:'Recorded in the Han era',
    title:'The lines grow softer.',
    description:'Curved, elongated lines keep the person beside the tree. This seal form belongs to the tradition recorded in the Shuowen dictionary.',
    note:'This is a selected historical form, not a dated Qin inscription. Continue into earlier script traditions.',
    source:'https://commons.wikimedia.org/wiki/File:%E4%BC%91-seal.svg',
    next:'Go further back',
  },
  {
    period:'Western Zhou tradition',
    title:'Cast into memory.',
    description:'This bronze-script form keeps the two figures visibly distinct. The tree reaches over the person resting beside it.',
    note:'Bronze inscriptions also used 休 for ideas such as protection and favor. Meaning can change alongside shape.',
    source:'https://commons.wikimedia.org/wiki/File:%E4%BC%91-bronze.svg',
    next:'See the earliest form',
  },
  {
    period:'Shang tradition',
    title:'The picture is still there.',
    description:'A person leans back against a tree. In this early form, the image you started with is still close to the surface.',
    note:'Notice the person’s back toward the trunk. Now return to the picture and see what you remember.',
    source:'https://commons.wikimedia.org/wiki/File:%E4%BC%91-oracle.svg',
    next:'Back to the picture',
  },
];

const capitalize = (text:string):string => text.charAt(0).toUpperCase() + text.slice(1);

/** Stage is the selected stop index, from image (0) through oracle (6). */
export function getExplorerContent(lesson:Lesson, stage:number):ExplorerContent {
  const index = Math.max(0, Math.min(6, Math.round(Number.isFinite(stage) ? stage : 0)));
  const theatreLesson = THEATRE_LESSONS.find(item => item.word === lesson.word);
  const parts = getExplorerParts(lesson);
  const rest = historyAvailable(lesson);
  const source = rest ? restSource : theatreLesson?.source || lesson.source;
  const partNames = parts.map(part => part.image);
  const partCount = parts.length;
  const partsLabel = partCount === 2 ? 'the two parts' : partCount === 1 ? 'the shape' : 'the parts';
  const story = getSceneDefinition(lesson.word)?.story || theatreLesson?.story || lesson.story;

  if (index >= 4) {
    if (rest) return {...restHistory[index - 4]};
    const script = JOURNEY_STOPS[index].label.toLowerCase();
    return {
      title:'A history still to uncover.',
      description:`No sourced ${script} form in this collection yet.`,
      note:`Keep ${lesson.word} · ${lesson.pinyin} · ${lesson.meaning} in mind as you return to its modern form.`,
      next:index === 6 ? 'Back to the picture' : index === 4 ? 'Continue to bronze' : 'Continue to oracle',
      period:`${capitalize(script)} script`,
    };
  }

  if (index === 0) return {
    title:rest ? 'A little shade. A quiet moment.' : theatreLesson?.title || 'Picture the story.',
    description:rest ? 'A person leans back against a tree, sheltered by its leaves. Hold this little scene in your mind.' : story,
    note:theatreLesson ? 'Next, step inside the scene and look around.' : 'Next, turn the written shapes and look at their depth.',
    next:'Explore in 3D',
    period:'Look closely',
    source,
  };

  if (index === 1) return {
    title:rest ? 'Step into the shade.' : theatreLesson ? 'Step inside the picture.' : 'See the writing in depth.',
    description:rest ? 'Move around the person and tree. Look at how they sit beside each other, then find their shapes in the character.' : (theatreLesson ? `Move around the scene and look for ${partNames.join(' and ')}. Follow the small labels that connect each image to its written shape.` : undefined) || `Turn the written shapes of ${lesson.word} to see their depth. Follow the strokes, then connect them to the memory images.`,
    note:`Drag to turn. Scroll or pinch to move closer. Next, find ${partsLabel}${theatreLesson ? ' hidden in this picture' : ' in the writing'}.`,
    next:`Find ${partsLabel}`,
    period:theatreLesson ? 'A scene you can explore' : 'The writing in 3D',
    source,
  };

  if (index === 2) return {
    title:rest ? 'A person. A tree.' : partCount ? `${partNames.map(capitalize).join('. ')}.` : 'Follow the shape.',
    description:rest ? '亻 is the side form of 人, a person. 木 is a tree. Pull them apart and turn them around. These are the two parts of our picture.' : `${parts.map(part => `${part.glyph} → ${part.image}`).join('. ')}. ${partCount === 1 ? 'Keep this shape and image together.' : 'Pull the parts apart and keep each shape with its image.'}`,
    note:rest ? 'Bring the parts together to discover the character.' : 'Use these images as memory cues as you bring the writing together.',
    next:partCount === 1 ? 'Meet the word' : 'Bring them together',
    period:partNames.map(capitalize).join(' + ') || 'The modern shape',
    source,
  };

  return {
    title:rest ? 'Together, they mean rest.' : `Meet ${lesson.word} · ${lesson.pinyin}.`,
    description:rest ? `The person and tree become ${lesson.word} — ${lesson.pinyin}, “${lesson.meaning}.” Think of leaning into the shade whenever you see these six strokes.` : `${lesson.word} — ${lesson.pinyin} — means “${lesson.meaning}.” ${theatreLesson?.stageCaptions[2] || 'Use the picture to recall its meaning and rebuild its writing.'}`,
    note:rest ? '休息 (xiūxi) means “to rest.” When you are ready, look at how the character was written long ago.' : 'The scene is an invented memory story. The history stops show whether a sourced earlier form is available.',
    next:'Explore its history',
    period:lesson.characters.length > 1 ? 'The modern word' : 'The modern character',
    source,
  };
}
