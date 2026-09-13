"""Compile authored memory images and stories; never infer a mnemonic from etymology."""
import hashlib,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
DIRECTORY=ROOT/'data/curation/mnemonics'

def load_mnemonics(characters):
    rows={}
    for path in sorted(DIRECTORY.glob('characters-*.txt')):
        for line in path.read_text().splitlines():
            char,image,parts,story=line.split('|',3)
            assert char not in rows,('Duplicate character mnemonic',char)
            rows[char]={'image':image,'parts':parts.split(),'story':story}
    assert set(rows)==set(characters),'Character mnemonic coverage changed'
    cues={c:r['image'] for c,r in rows.items()}
    for line in (DIRECTORY/'extra-cues.txt').read_text().splitlines():
        glyph,image=line.split('|',1)
        assert glyph not in cues,('Duplicate image cue',glyph)
        cues[glyph]=image
    words={}
    for path in [*sorted(DIRECTORY.glob('words-*.txt')),DIRECTORY/'single-senses.txt']:
        for line in path.read_text().splitlines():
            word,story=line.split('|',1)
            assert word not in words,('Duplicate word mnemonic',word)
            words[word]=story
    def cuts(node,allowed,seen=()):
        if not node:return []
        if 'glyph' in node:
            g=node['glyph']
            if g not in allowed and g in characters and g not in seen:
                return [[g],*cuts(characters[g]['tree'],allowed,(*seen,g))]
            return [[g]]
        combinations=[[]]
        for child in node['children']:
            combinations=[a+b for a in combinations for b in cuts(child,allowed,seen)]
        def label(n):return n.get('glyph') or n['operator']+''.join(label(x) for x in n['children'])
        return [[label(node)],*combinations]
    for c,r in rows.items():
        assert all(p in cues for p in r['parts']),('Missing image cue',c,r['parts'])
        kind='outline' if r['parts']==[c] else 'parts'
        if kind=='parts':assert r['parts'] in cuts(characters[c]['tree'],set(r['parts']),(c,)),('Parts differ from source structure',c,r['parts'])
        characters[c]['mnemonic']={'image':r['image'],'elements':[{'glyph':p,'image':cues[p]} for p in r['parts']],'story':r['story'],'kind':kind}
    digest=hashlib.sha256(b''.join(p.read_bytes() for p in sorted(DIRECTORY.glob('*.txt')))).hexdigest()
    return words,cues,digest
