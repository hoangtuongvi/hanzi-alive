"""Render lesson fallbacks from the checked-in native Blender files.

Blender --background --threads 4 --python scripts/blender/render_posters.py -- [names | --all] [--shard INDEX COUNT]
Intermediate PNGs stay in outputs/. Run sync_posters.py to publish WebP assets.
Native scenes and interactive GLBs are never rewritten by this script.
"""
import bpy
import hashlib
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'outputs/blender-posters'
OUT.mkdir(parents=True,exist_ok=True)
assets=json.loads((ROOT/'public/models/blender/manifest.json').read_text())['assets']
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
shard_index,shard_count=0,1
if '--shard' in args:
    index=args.index('--shard')
    shard_index,shard_count=map(int,args[index+1:index+3])
    del args[index:index+3]
    if not 0<=shard_index<shard_count:raise ValueError('Invalid shard')
names=list(assets) if args==['--all'] else args
if not names or any(name not in assets for name in names):raise ValueError('Provide valid scene names or --all')
settings={'version':1,'width':512,'height':460,'samples':4,'transparent':True,'engine':'CYCLES CPU'}
for name in names[shard_index::shard_count]:
    asset=assets[name]
    native=ROOT/asset['blendFile']
    expected={'word':asset['word'],'scene':name,'blendSha256':asset['blendSha256'],'glbSha256':asset['sha256'],'settings':settings}
    metadata=OUT/(name+'.json')
    preview=OUT/(name+'.png')
    if preview.exists() and metadata.exists() and json.loads(metadata.read_text())==expected:
        print('POSTER_CURRENT',name,flush=True)
        continue
    if hashlib.sha256(native.read_bytes()).hexdigest()!=asset['blendSha256']:
        raise ValueError('Native scene changed: '+name)
    bpy.ops.wm.open_mainfile(filepath=str(native))
    scene=bpy.context.scene
    scene.render.engine='CYCLES'
    scene.cycles.device='CPU'
    scene.cycles.samples=settings['samples']
    scene.cycles.use_denoising=True
    scene.render.resolution_x=settings['width'];scene.render.resolution_y=settings['height']
    scene.render.resolution_percentage=100
    scene.render.film_transparent=True
    scene.render.image_settings.file_format='PNG'
    scene.render.image_settings.color_mode='RGBA'
    scene.render.filepath=str(preview)
    if bpy.ops.render.render(write_still=True)!={'FINISHED'}:
        raise RuntimeError('Rendering did not finish: '+name)
    metadata.write_text(json.dumps(expected,ensure_ascii=False,indent=2)+'\n')
    print('POSTER_RENDERED',name,flush=True)
