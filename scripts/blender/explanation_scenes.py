"""Compose the explicit recipe inventory into Blender scenes and label anchors."""
import json
from pathlib import Path
from functools import partial
from rest_scene import anchor, oval
from explanation_props import palette, place
from explanation_recipes import RECIPES, source_revision

ROOT=Path(__file__).resolve().parents[2]


def build_explanation(name):
    recipe=RECIPES[name]
    lessons=json.loads((ROOT/'public/data/lessons.json').read_text())
    lesson=next(item for item in lessons if item['word']==recipe['word'])
    if recipe['glyphs'] != [part['glyph'] for part in lesson['memoryElements']]:
        raise ValueError('Recipe parts no longer match the source: '+recipe['word'])
    mats=palette()
    oval('Diorama / earth base',(0,-1.58,0),(2.28,.13,1.25),mats['earth'],32,10)
    oval('Diorama / moss top',(0,-1.48,0),(2.23,.045,1.20),mats['green'],32,8)
    objects=[]
    for index,item in enumerate(recipe['parts']+recipe['extras']):
        title=f'{recipe["word"]} / {index:02d} / {item["prop"]}'
        place(item['prop'],title,item['position'],item['scale'],mats,item['rotation'])
        objects.append({'object':title,**item})
        if index<len(recipe['parts']):
            cue=lesson['memoryElements'][index]
            node=anchor('anchor_part_'+str(index),item['position'])
            node['glyph']=cue['glyph'];node['label']=cue['image']
    return {**source_revision(name),'title':name.replace('-',' ').capitalize(),
            'story':recipe['story'],
            'composition':'Explicit word-specific arrangement of reusable sculpted objects.',
            'objects':objects,
            'anchors':{'anchor_part_'+str(i):glyph for i,glyph in enumerate(recipe['glyphs'])},
            'interpretation':'Invented learning mnemonic, not historical etymology. Draft, not independently reviewed.'}


SCENES={name:(recipe['word'],partial(build_explanation,name)) for name,recipe in RECIPES.items()}
