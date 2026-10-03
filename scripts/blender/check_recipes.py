"""Validate explicit mnemonic inventories without starting Blender.

This checks production invariants, not editorial/etymological truth. Full corpus
coverage includes the original detailed builders, whose files are checked by
sync_catalog.py after export.
"""
import argparse
import ast
import importlib
import importlib.util
import json
import math
import re
from pathlib import Path
from explanation_recipes import RECIPES, COMPLETION_MODULES

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def supported_props():
    kinds=set()
    tree=ast.parse((HERE/'explanation_props.py').read_text())
    for node in ast.walk(tree):
        if not isinstance(node,ast.Compare) or not isinstance(node.left,ast.Name) or node.left.id!='kind':
            continue
        for value in node.comparators:
            values=value.elts if isinstance(value,(ast.Tuple,ast.List,ast.Set)) else [value]
            kinds.update(item.value for item in values if isinstance(item,ast.Constant) and isinstance(item.value,str))
    for prefix,module in COMPLETION_MODULES:
        name=module+'_props'
        if importlib.util.find_spec(name) is not None:
            custom=importlib.import_module(name).KINDS
            if kinds.intersection(custom):raise ValueError('Duplicate prop keys: '+name)
            if any(not key.startswith(prefix+'-') for key in custom):raise ValueError('Unscoped custom props: '+name)
            kinds.update(custom)
    return kinds


def check(require_complete=False):
    lessons={item['word']:item for item in json.loads((ROOT/'public/data/lessons.json').read_text())}
    kinds=supported_props()
    words=set()
    stories=set()
    for name,recipe in RECIPES.items():
        word=recipe['word']
        if word not in lessons or word in words:raise ValueError('Unknown/duplicate word: '+word)
        words.add(word)
        if not re.fullmatch('[a-z]+(?:-[a-z]+)*',name):raise ValueError('Invalid scene slug: '+name)
        glyphs=[part['glyph'] for part in lessons[word]['memoryElements']]
        if recipe['glyphs']!=glyphs or len(recipe['parts'])!=len(glyphs):raise ValueError('Part mismatch: '+word)
        story=recipe['story'].strip()
        if len(story)<40 or len(story)>1200 or story in stories:raise ValueError('Missing/duplicate/oversized explanation: '+word)
        stories.add(story)
        for item in recipe['parts']+recipe['extras']:
            key=item['prop']
            if key not in kinds and not re.fullmatch(r'count-(?:[1-9]|[12][0-9]|30)',key):
                raise ValueError(f'{word}: no designed prop {key}')
            pos=item['position']
            if len(pos)!=3 or not all(isinstance(v,(int,float)) and math.isfinite(v) and abs(v)<=3 for v in pos):
                raise ValueError('Invalid object position: '+word)
            if not isinstance(item['scale'],(int,float)) or not .03<=item['scale']<=4:
                raise ValueError('Invalid scale: '+word)
            if not math.isfinite(item['rotation']):raise ValueError('Invalid rotation: '+word)
    if require_complete:
        assets=json.loads((ROOT/'public/models/blender/manifest.json').read_text())['assets']
        detailed={asset['word'] for asset in assets.values() if 'recipeSha256' not in asset.get('design',{})}
        if words|detailed!=set(lessons):
            raise ValueError('Corpus words missing explicit recipes: '+', '.join(set(lessons)-(words|detailed)))
    print(f'PASS: {len(RECIPES)} explicit recipes; {len(kinds)} supported sculpted props; source glyph order verified.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-complete',action='store_true')
    check(parser.parse_args().require_complete)
