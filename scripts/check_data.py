import json,pathlib,collections,re
root=pathlib.Path(__file__).resolve().parents[1]
def read(p):return json.loads((root/p).read_text())
lessons=read('public/data/lessons.json');chars=read('public/data/characters.json');manifest=read('public/data/manifest.json');selection=read('data/selection.json');byword={x['word']:x for x in lessons}
assert len(lessons)==1000 and len(byword)==1000
assert len({l['id'] for l in lessons})==1000
assert len({l['story'] for l in lessons})==1000,'Duplicate story sentences'
assert len(chars)==919
for i,l in enumerate(lessons):
 assert l['id']==f'w{i+1:04d}' and l['word']==selection[i]['simplified']
 assert l['status']=='draft' and l['meaning'] and l['story'] and l['connection']
 assert len(l['story'].split())>=7,l['word']
 assert any(f['transcriptions']['pinyin']==l['pinyin'] and f['traditional']==l['traditional'] for f in selection[i]['forms']),l['word']
 assert all(c in chars for c in l['characters'])
 assert 1<=l['syllables']<=4
 assert l['source'].startswith('https://')
for c,meta in chars.items():
 data=read(f'public/data/characters/{ord(c)}.json')
 assert data['character']==c and len(data['strokes'])==len(data['groups'])==len(data['medians'])==len(data['matches'])
 assert all(p.startswith('M') for p in data['strokes'])
 assert all(g==-1 or 0<=g<len(meta['components']) for g in data['groups'])
 expected=sorted(l['id'] for l in lessons if c in l['word']);assert sorted(meta['usages'])==expected
critical={'便宜':'pián yi','东西':'dōng xi','音乐':'yīn yuè','快乐':'kuài lè','银行':'yín háng','行走':'xíng zǒu','长大':'zhǎng dà','长江':'Cháng Jiāng','重要':'zhòng yào','重复':'chóng fù','听':'tīng','鸟':'niǎo','得':'de','好处':'hǎo chu','妻子':'qī zi','故事':'gù shi','重点':'zhòng diǎn'}
for w,p in critical.items():assert byword[w]['pinyin']==p,(w,byword[w]['pinyin'])
assert manifest['geometryCoverage']==len(chars) and manifest['independentlyReviewed']==0
assert sum(manifest['syllables'].values())==1000
print(f'PASS: 1,000 unique words and original story sentences; 919 geometries; selected dictionary forms; reuse links; {len(critical)} critical readings; draft labeling; corpus totals.')
# Component memory cues must be complete, repeatable, and aligned with the authored corpus.
from mnemonics import load_mnemonics
_,cues,_=load_mnemonics(chars)
assert len({c['mnemonic']['story'] for c in chars.values()})==919
for l in lessons:
 assert l['strategy']=='mnemonic' and l['contentRevision']=='elements-2'
 assert l['memoryElements'] and l['memorySearch']
 assert all(e['image']==cues[e['glyph']] for e in l['memoryElements']),l['word']
 expected=chars[l['word']]['mnemonic']['elements'] if len(l['word'])==1 else [{'glyph':c,'image':cues[c]} for c in l['word']]
 assert l['memoryElements']==expected,l['word']
 assert 'phonetic component' not in l['story']+l['connection']
for c in '清晴请情睛精猜静':
 m=chars[c]['mnemonic']
 assert {'glyph':'青','image':'green'} in m['elements']
 assert 'green' in m['story'].lower()
assert manifest['componentStories']+manifest['outlineStories']==919
assert manifest['compoundStories']==651
print('PASS: all 1,000 lessons have consistent element images; 919 character mnemonics; sourced ordered parts; eight green-family stories preserve green.')
