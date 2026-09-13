"""Compile the checked-in 1,000-entry pilot. No model or network calls at runtime."""
import json, pathlib, re, hashlib, shutil, collections, datetime, unicodedata
from mnemonics import load_mnemonics
ROOT=pathlib.Path(__file__).resolve().parents[1]
def read(p): return json.loads((ROOT/p).read_text())
def write(p,value):
 path=ROOT/p; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(value,ensure_ascii=False,separators=(',',':')))
selection=read('data/selection.json'); overrides=read('data/curation/readings.json'); connections=read('data/curation/connections.json');stress=read('data/curation/stress.json')
stories={}
for path in sorted((ROOT/'data/curation').glob('stories-*.txt')):
 for line in path.read_text().splitlines():
  if not line:continue
  n,meaning,story=line.split('|',2)
  assert n not in stories
  stories[n]=(meaning,story)
assert set(stories)==set(x['simplified'] for x in selection), 'Vocabulary changed: curate stories for the new words before rebuilding.'
chars={x['character']:x for x in map(json.loads,(ROOT/'data/source/makemeahanzi-dictionary.txt').read_text().splitlines())}
operators={'⿰':2,'⿱':2,'⿲':3,'⿳':3,'⿴':2,'⿵':2,'⿶':2,'⿷':2,'⿸':2,'⿹':2,'⿺':2,'⿻':2}
def parse_ids(s):
 i=iter(s)
 def part():
  c=next(i)
  return {'operator':c,'children':[part() for _ in range(operators[c])]} if c in operators else {'glyph':c}
 try:
  node=part()
  try:next(i);return None
  except StopIteration:return node
 except (StopIteration,RecursionError):return None

def tokens(s):return set(re.findall('[a-z]+',s.lower()))-set('a the of to and in is for or be with by as'.split())
def select_form(x,meaning):
 expected=overrides.get(x['simplified'])
 choices=[f for f in x['forms'] if not expected or f['transcriptions']['pinyin']==expected]
 assert choices,(x['simplified'],expected)
 def score(f):
  meanings='; '.join(f['meanings']); p=f['transcriptions']['pinyin']; lower=meanings.lower()
  result=3*len(tokens(meaning)&tokens(meanings))
  if p[0].isupper() and x['simplified'] not in ['中国','北京','汉语','长江']:result-=25
  if lower.startswith(('variant of','old variant','used in','unofficial variant')):result-=20
  if '(archaic)' in lower or 'surname' in lower:result-=10
  return result
 return max(choices,key=score)
lessons=[]
for i,x in enumerate(selection,1):
 word=x['simplified'];meaning,story=stories[word]; f=select_form(x,meaning)
 mode,note,*source=connections.get(word,['mnemonic','Picture the elements together, then recall the meaning and writing.'])
 levels=[int(l[4:]) for l in x['level'] if re.fullmatch('old-[1-6]',l)]
 readings=list(dict.fromkeys(y['transcriptions']['pinyin'] for y in x['forms']))
 lessons.append({'id':f'w{i:04d}','word':word,'traditional':f['traditional'],'pinyin':f['transcriptions']['pinyin'],'meaning':meaning,'dictionaryMeanings':f['meanings'],'story':story,'connection':note,'strategy':mode,'stressTest':word in stress,'level':min(levels) if levels else None,'characters':list(word),'syllables':len([s for s in f['transcriptions']['pinyin'].split() if s!='r']),'readings':readings,'status':'draft','source':source[0] if source else 'https://www.mdbg.net/chinese/dictionary?page=worddict&wdrst=0&wdqb='+word,'formSource':'Make Me a Hanzi' if x.get('supplement') else 'Complete HSK Vocabulary / CC-CEDICT','author':'AI-authored pilot draft; no independent linguistic review','selectedForm':{'traditional':f['traditional'],'pinyin':f['transcriptions']['pinyin']}})
needed=set(''.join(l['word'] for l in lessons)); usages=collections.defaultdict(list)
for l in lessons:
 for c in set(l['characters']):usages[c].append(l['id'])
meta={}; missing=[]
for c in sorted(needed):
 if c not in chars:missing.append(c);continue
 ch=chars[c];tree=parse_ids(ch['decomposition'])
 def label(node):return node.get('glyph') or node['operator']+''.join(label(k) for k in node['children'])
 components=[label(n) for n in tree.get('children',[])] if tree else []
 meta[c]={'character':c,'definition':ch.get('definition',''),'pinyin':ch['pinyin'],'radical':ch['radical'],'decomposition':ch['decomposition'],'tree':tree,'components':components,'etymology':ch.get('etymology'),'usages':usages[c],'source':'https://github.com/skishore/makemeahanzi','geometryUrl':f'/data/characters/{ord(c)}.json'}
geometry_count=0;badmaps=[]
for line in (ROOT/'data/source/makemeahanzi-graphics.txt').open():
 g=json.loads(line);c=g['character']
 if c not in needed:continue
 matches=chars[c]['matches'];assert len(matches)==len(g['strokes']),(c,len(matches),len(g['strokes']))
 rootchildren=len((meta[c]['tree'] or {}).get('children',[]))
 groups=[m[0] if m and rootchildren and 0<=m[0]<rootchildren else -1 for m in matches]
 if rootchildren and any(k<0 for k in groups):badmaps.append(c)
 write(f'public/data/characters/{ord(c)}.json',{'character':c,'strokes':g['strokes'],'groups':groups,'medians':g['medians'],'matches':matches});geometry_count+=1
word_mnemonics,cues,mnemonic_digest=load_mnemonics(meta)
assert set(word_mnemonics)<=set(l['word'] for l in lessons)
for l in lessons:
 word=l['word']
 assert len(word)==1 or word in word_mnemonics,('Missing word story',word)
 l['story']=word_mnemonics.get(word) or meta[word]['mnemonic']['story']
 l['memoryElements']=meta[word]['mnemonic']['elements'] if len(word)==1 else [{'glyph':c,'image':cues[c]} for c in word]
 l['memorySearch']=' '.join(e['glyph']+' '+e['image'] for c in l['characters'] for e in meta[c]['mnemonic']['elements'])
 l['mnemonicKind']=meta[word]['mnemonic']['kind'] if len(word)==1 else 'word'
 l['strategy']='mnemonic'
 l['connection']='Picture each image, join them in the scene, then use the scene to recall the meaning and rebuild the writing.'
 l['contentRevision']='elements-2'
write('public/data/element-cues.json',cues)
write('public/data/characters.json',meta);write('public/data/lessons.json',lessons)
manifest={'version':'elements-2','createdAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'selection':'43 deliberately selected stress cases, followed by HSK 2.0 levels 1–4 ordered by level then the source frequency rank; deduplicated to exactly 1,000. This is not an official exam list or a top-1,000 frequency claim.','words':len(lessons),'uniqueCharacters':len(needed),'characterOccurrences':sum(len(l['word']) for l in lessons),'geometryCoverage':geometry_count,'missingCharacters':missing,'partialStrokeMappings':badmaps,'stressCases':len(stress),'strategies':dict(collections.Counter(l['strategy'] for l in lessons)),'syllables':dict(collections.Counter(l['syllables'] for l in lessons)),'draftStories':len(stories),'characterMnemonics':len(meta),'componentStories':sum(c['mnemonic']['kind']=='parts' for c in meta.values()),'outlineStories':sum(c['mnemonic']['kind']=='outline' for c in meta.values()),'compoundStories':sum(len(l['word'])>1 for l in lessons),'mnemonicSha256':mnemonic_digest,'independentlyReviewed':0,'sourceRevisions':[read('data/source/complete-hsk-vocabulary-revision.json'),read('data/source/makemeahanzi-revision.json')],'curationSha256':hashlib.sha256(''.join(p.read_text() for p in sorted((ROOT/'data/curation').glob('stories-*.txt'))).encode()).hexdigest()}
write('public/data/manifest.json',manifest)
write('data/build-summary.json',manifest)
write('public/data/pilot-download.json',{'manifest':manifest,'lessons':lessons,'characters':meta,'elementCues':cues})
for name,dest in [('complete-hsk-vocabulary-LICENSE','hsk-MIT.txt'),('makemeahanzi-COPYING','makemeahanzi-COPYING.txt'),('makemeahanzi-LGPL','LGPL-3.0.txt'),('makemeahanzi-APL-english-ARPHICPL.TXT','ARPHIC-PUBLIC-LICENSE.txt')]:shutil.copyfile(ROOT/'data/source'/name,ROOT/'public/licenses'/dest)
write('data/form-audit.json',[{'word':l['word'],'pinyin':l['pinyin'],'meaning':l['meaning'],'dictionary':l['dictionaryMeanings'],'traditional':l['traditional']} for l in lessons])
print(json.dumps(manifest,ensure_ascii=False,indent=2))
