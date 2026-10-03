"""Admit verified generated scenes to the collection without touching old copy.

Run with ordinary Python after build_assets.py. --check performs a read-only
comparison. Admission requires both the editable source and its checksum-matched
GLB; interrupted batches therefore cannot create broken collection links.
"""
import argparse
import hashlib
import json
from pathlib import Path
from explanation_recipes import RECIPES, source_revision

ROOT=Path(__file__).resolve().parents[2]
EXTRA_SCENES={'root-books':'本','water':'水','snow':'雪','big':'大','too-much':'太','follow':'从'}
INTERPRETATION='Invented visual mnemonic, not historical etymology. Draft, not independently reviewed.'


def synchronize(check=False,require_complete=False):
    catalog_path=ROOT/'src/explorer/scene-catalog.json'
    catalog=json.loads(catalog_path.read_text())
    lessons={item['word']:item for item in json.loads((ROOT/'public/data/lessons.json').read_text())}
    excluded=json.loads((ROOT/'data/curation/illustration-exclusions.json').read_text())
    assets=json.loads((ROOT/'public/models/blender/manifest.json').read_text())['assets']
    planned={**EXTRA_SCENES,**{name:recipe['word'] for name,recipe in RECIPES.items()}}
    new=[]
    for name,word in planned.items():
        if word in excluded:raise ValueError('Excluded illustration: '+word)
        lesson=lessons[word]
        recipe=RECIPES.get(name)
        glyphs=[part['glyph'] for part in lesson['memoryElements']]
        if recipe and recipe['glyphs']!=glyphs:raise ValueError('Changed part order: '+word)
        asset=assets.get(name)
        if not asset:raise ValueError('Build the missing scene first: '+name)
        glb=ROOT/'public'/asset['url'].lstrip('/')
        if not (ROOT/asset['blendFile']).is_file() or not glb.is_file():raise ValueError('Missing model: '+name)
        if asset.get('blendSha256') and hashlib.sha256((ROOT/asset['blendFile']).read_bytes()).hexdigest()!=asset['blendSha256']:
            raise ValueError('Changed native model: '+name)
        if hashlib.sha256(glb.read_bytes()).hexdigest()!=asset['sha256']:raise ValueError('Changed GLB: '+name)
        if asset['word']!=word:raise ValueError('Wrong manifest word: '+name)
        anchors=['anchor_part_'+str(i) for i in range(len(glyphs))]
        if set(anchors)!=set(asset['anchors']):raise ValueError('Wrong anchors: '+name)
        if recipe and asset['design']['story']!=recipe['story']:raise ValueError('Rebuild changed story: '+name)
        if recipe and any(asset['design'].get(key)!=value for key,value in source_revision(name).items()):
            raise ValueError('Rebuild changed recipe or prop library: '+name)
        new.append({'word':word,'scene':name,'format':'blender','asset':asset['url'],
                    'anchors':anchors,'history':False,
                    'story':recipe['story'] if recipe else lesson['story'],
                    'interpretation':INTERPRETATION})
    managed=set(planned.values())
    result=[item for item in catalog if item['word'] not in managed]+new
    if len({item['word'] for item in result})!=len(result):raise ValueError('Duplicate catalog words')
    # Preserved detailed scenes need the same file checks as new compositions;
    # a correct word count alone cannot establish complete usable coverage.
    for scene in result:
        if scene['format']!='blender':continue
        word=scene['word']
        asset=assets.get(scene['scene'])
        if not asset or asset['word']!=word or asset['url']!=scene['asset']:
            raise ValueError('Catalog/manifest binding mismatch: '+word)
        if word not in lessons or word in excluded:raise ValueError('Invalid catalog word: '+word)
        if len(scene['anchors'])!=len(lessons[word]['memoryElements']) or set(scene['anchors'])!=set(asset['anchors']):
            raise ValueError('Invalid ordered callout inventory: '+word)
        glb=ROOT/'public'/asset['url'].lstrip('/')
        native=ROOT/asset['blendFile']
        if not glb.is_file() or hashlib.sha256(glb.read_bytes()).hexdigest()!=asset['sha256']:
            raise ValueError('Missing/changed catalog GLB: '+word)
        if not native.is_file() or not asset.get('blendSha256') or hashlib.sha256(native.read_bytes()).hexdigest()!=asset['blendSha256']:
            raise ValueError('Missing/changed catalog native file: '+word)
    if require_complete:
        actual={item['word'] for item in result if item['format']=='blender'}
        if actual!=set(lessons):
            raise ValueError(f'Incomplete corpus: {len(set(lessons)-actual)} missing Blender explanations; '
                             f'{len(actual-set(lessons))} unexpected words')
        if {asset['word'] for asset in assets.values()}!=actual or len(assets)!=len(actual):
            raise ValueError('Full corpus manifest contains missing or duplicate words')
    text=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if check:
        if text!=catalog_path.read_text():raise ValueError('Scene catalog is stale; run sync_catalog.py')
    else:catalog_path.write_text(text)
    print(f'{len(result)} Blender scene definitions; {len(new)} managed expansion scenes verified.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--require-complete',action='store_true',help='Require a Blender explanation for every database word')
    args=parser.parse_args()
    synchronize(args.check,args.require_complete)
