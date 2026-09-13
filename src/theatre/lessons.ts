import type {TheatreLesson, VisualPart} from './types';

const part = (glyph:string,image:string,color:string,characterIndex=0,sourceGroup:number|null=0):VisualPart => ({glyph,image,color,characterIndex,sourceGroup});
const dictionary = (word:string) => `https://www.mdbg.net/chinese/dictionary?page=worddict&wdrst=0&wdqb=${encodeURIComponent(word)}`;

/** Stable mnemonic images, paired with the existing pilot's selected sense. */
export const THEATRE_LESSONS:TheatreLesson[] = [
  {
    word:'休',wordId:'w0001',scene:'rest',title:'A place to rest',
    story:'A person leans against a tree and finally rests in its shade.',
    action:'Follow the traveler into the shade. Watch the person and tree become 亻 and 木.',
    parts:[part('亻','person','#d37c53'),part('木','tree','#315e4b',0,1)],
    source:'https://humanum.arts.cuhk.edu.hk/Lexis/lexi-mf/search.php?word=休',
    stageCaptions:['A traveler finds shade and sits beside a tree.','Keep both images: person 亻 and tree 木.','Bring person and tree together: 休 — rest.']
  },
  {
    word:'林',wordId:'w0004',scene:'woods',title:'One tree finds another',
    story:'Two trees stand together, forming a small patch of woods.',
    action:'Grow a second tree beside the first. Both keep the same tree image.',
    parts:[part('木','tree','#315e4b'),part('木','tree','#315e4b',0,1)],source:dictionary('林'),
    stageCaptions:['One tree is joined by a second: a little patch of woods.','Two tree shapes, 木 and 木, stand side by side.','Join the two trees: 林 — woods.']
  },
  {
    word:'清',wordId:'w0006',scene:'clear',title:'See the green through water',
    story:'Water reflects green plants so clearly that you can see every leaf through the clear pool.',
    action:'Watch the sediment settle and the green reflection become visible in the clear water.',
    parts:[part('氵','water','#527f91'),part('青','green','#315e4b',0,1)],
    source:'https://humanum.arts.cuhk.edu.hk/Lexis/lexi-mf/search.php?word=清',
    stageCaptions:['As the water clears, you can see the green plants reflected in it.','Water stays 氵; green stays 青. Keep both pictures.','Join water and green: 清 — clear.']
  },
  {
    word:'晴',wordId:'w0007',scene:'sunny',title:'Green under the sun',
    story:'The sun lights up green grass; its vivid green announces a sunny day.',
    action:'Move the clouds aside. The sun makes the green grass shine.',
    parts:[part('日','sun','#c29a39'),part('青','green','#315e4b',0,1)],source:dictionary('晴'),
    stageCaptions:['Clouds part. Green grass brightens under the sun.','Sun becomes 日; the vivid green becomes 青.','Join sun and green: 晴 — sunny.']
  },
  {
    word:'情',wordId:'w0009',scene:'emotion',title:'Let the heart feel',
    story:'A heart rests in green nature; as it relaxes, its hidden emotions begin to flow.',
    action:'Let the heart settle among green plants. Watch its feelings emerge.',
    parts:[part('忄','heart','#b97568'),part('青','green','#315e4b',0,1)],source:dictionary('情'),
    stageCaptions:['A heart rests in green nature and lets its feelings flow.','Hold onto heart 忄 and green 青 as two visible images.','Join heart and green: 情 — feeling; emotion.']
  },
  {
    word:'请',wordId:'w0008',scene:'invite',title:'A green invitation',
    story:'A speech bubble offers a green invitation: “Please come into my garden.”',
    action:'Open the green invitation and welcome the visitor into the garden.',
    parts:[part('讠','speech bubble','#c29a39'),part('青','green','#315e4b',0,1)],source:dictionary('请'),
    stageCaptions:['A green invitation opens: “Please come into my garden.”','Speech bubble becomes 讠. The invitation keeps green 青.','Join speech and green: 请 — please; invite.']
  },
  {
    word:'手机',wordId:'w0017',scene:'phone',title:'A machine in your hand',
    story:'A hand picks up a tiny tree-and-table machine; it rings and becomes your mobile phone.',
    action:'Lift the little machine into a hand and answer its ring.',
    parts:[part('手','hand','#d37c53',0,null),part('机','machine','#315e4b',1,null)],source:dictionary('手机'),
    stageCaptions:['A hand raises a little machine. It rings: a mobile phone.','Recognize the two characters: hand 手 and machine 机.','Read the pair together: 手机 — mobile phone.']
  },
  {
    word:'电脑',wordId:'w0150',scene:'computer',title:'A brain comes to life',
    story:'Electricity sparks through a moon-shaped brain on your desk: the computer begins thinking.',
    action:'Send a spark through the brain and watch the computer wake up.',
    parts:[part('电','electricity','#c29a39',0,null),part('脑','brain','#8b86ad',1,null)],source:dictionary('电脑'),
    stageCaptions:['Electricity flows into a brain and lights the computer screen.','Keep electricity 电 and brain 脑 as the two character images.','Read the pair together: 电脑 — computer.']
  },
  {
    word:'分手',wordId:'w0019',scene:'parting',title:'Two hands part ways',
    story:'A dividing knife cuts a ribbon between two hands; the hands separate as the couple breaks up.',
    action:'Let the ribbon divide, then watch the hands move apart.',
    parts:[part('分','divide','#c29a39',0,null),part('手','hand','#d37c53',1,null)],source:dictionary('分手'),
    stageCaptions:['The connecting ribbon divides. Two hands move apart.','Keep divide 分 and hand 手 in the same parting scene.','Read the pair together: 分手 — break up; part ways.']
  },
  {
    word:'高手',wordId:'w0018',scene:'expert',title:'The winning hand',
    story:"A hand reaches high above every player to make the winning move: the expert's high hand.",
    action:'Raise the hand above the board and make the winning move.',
    parts:[part('高','high','#8b86ad',0,null),part('手','hand','#d37c53',1,null)],source:dictionary('高手'),
    stageCaptions:['A hand reaches high and makes the winning move.','Remember high 高 and hand 手 as a single winning scene.','Read the pair together: 高手 — expert.']
  }
];

export const THEATRE_META:Record<string,{pinyin:string;meaning:string}> = {
  '休':{pinyin:'xiū',meaning:'rest'}, '林':{pinyin:'lín',meaning:'woods'},
  '清':{pinyin:'qīng',meaning:'clear'}, '晴':{pinyin:'qíng',meaning:'sunny'},
  '情':{pinyin:'qíng',meaning:'feeling; emotion'}, '请':{pinyin:'qǐng',meaning:'please; invite'},
  '手机':{pinyin:'shǒu jī',meaning:'mobile phone'}, '电脑':{pinyin:'diàn nǎo',meaning:'computer'},
  '分手':{pinyin:'fēn shǒu',meaning:'break up; part ways'}, '高手':{pinyin:'gāo shǒu',meaning:'expert'}
};

const distractors:Record<string,string[]> = {
  '亻':['氵','忄','讠'], '木':['本','禾','日'], '氵':['忄','亻','讠'],
  '青':['清','晴','情'], '日':['月','目','木'], '忄':['氵','亻','扌'], '讠':['忄','氵','亻'],
  '手':['毛','牛','才'], '机':['林','休','本'], '电':['田','由','申'],
  '脑':['月','明','朋'], '分':['公','八','刀'], '高':['京','亭','亮']
};

/** Fixed options remain still while a learner retries; position varies by slot. */
export function reconstructionChoices(lesson:TheatreLesson,slot:number):string[] {
  const correct=lesson.parts[slot].glyph;
  const choices=[correct,...(distractors[correct]??['日','月','木']).filter(glyph=>glyph!==correct)].slice(0,4);
  const rotation=(Array.from(lesson.word).reduce((sum,glyph)=>sum+glyph.codePointAt(0)!,0)+slot)%4;
  return [...choices.slice(rotation),...choices.slice(0,rotation)];
}
