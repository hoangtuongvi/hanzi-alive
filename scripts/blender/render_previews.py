"""Render a browsable contact sheet from saved native files without changing them.

Blender --background --python scripts/blender/render_previews.py -- [names|--all]
The HTML pages and PNGs are local QA artifacts in outputs/blender-review/.
"""
import bpy
import html
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'outputs/blender-review'
OUT.mkdir(parents=True,exist_ok=True)
assets=json.loads((ROOT/'public/models/blender/manifest.json').read_text())['assets']
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
names=list(assets) if '--all' in args else args
if not names:raise ValueError('Provide scene names or --all')
for name in names:
    if name not in assets:raise ValueError('Unknown scene: '+name)
for name in names:
    asset=assets[name]
    preview=OUT/(name+'.png')
    native=ROOT/asset['blendFile']
    if preview.exists() and preview.stat().st_mtime>=native.stat().st_mtime:continue
    bpy.ops.wm.open_mainfile(filepath=str(native))
    scene=bpy.context.scene
    scene.render.resolution_x=400;scene.render.resolution_y=360
    scene.render.resolution_percentage=100
    scene.cycles.samples=4
    scene.render.filepath=str(preview)
    bpy.ops.render.render(write_still=True)
    print('REVIEW_RENDER',name,flush=True)

pages=(len(names)+23)//24
for page in range(pages):
    cards=[]
    for name in names[page*24:(page+1)*24]:
        asset=assets[name];story=asset.get('design',{}).get('story','')
        cards.append(f'<article><img src="{name}.png" alt="{html.escape(asset["word"])}"><h2>{html.escape(asset["word"])} · {name}</h2><p>{html.escape(story)}</p></article>')
    nav=' · '.join(f'<a href="page-{i+1}.html">{i+1}</a>' for i in range(pages))
    document=f'''<!doctype html><html lang="en"><meta charset="utf-8"><title>Blender review {page+1}</title>
<style>body{{background:#18211c;color:#eee7d5;font:13px system-ui;margin:20px}}nav{{margin:16px 0}}a{{color:#b8d7b0}}main{{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:12px}}article{{background:#29382f;padding:8px}}img{{width:100%;display:block}}h2{{font-size:13px;margin:6px 0}}p{{font-size:11px;line-height:1.4;margin:6px 0}}</style>
<h1>Blender scene review · {page+1} / {pages}</h1><nav>{nav}</nav><main>{''.join(cards)}</main></html>'''
    (OUT/f'page-{page+1}.html').write_text(document)
print(f'{len(names)} previews; {pages} review pages in {OUT}')
