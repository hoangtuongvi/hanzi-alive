"""Publish/verify compact stills tied to the exact native scenes and GLBs."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'outputs/blender-posters'
OUT=ROOT/'public/models/posters'
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--check',action='store_true')
parser.add_argument('--allow-partial',action='store_true')
args=parser.parse_args()
assets=json.loads((ROOT/'public/models/blender/manifest.json').read_text())['assets']
manifest_path=OUT/'manifest.json'
if args.check:
    manifest=json.loads(manifest_path.read_text())
    posters=manifest['assets']
    if set(posters)!=set(assets):raise ValueError('Poster coverage does not match the Blender scenes')
    for name,asset in assets.items():
        poster=posters[name]
        path=OUT/(name+'.webp')
        if poster['word']!=asset['word'] or poster['blendSha256']!=asset['blendSha256'] or poster['glbSha256']!=asset['sha256']:
            raise ValueError('Stale poster: '+name)
        if poster['sha256']!=hashlib.sha256(path.read_bytes()).hexdigest():raise ValueError('Poster changed: '+name)
        with Image.open(path) as image:
            image.load()
            if image.size!=(512,460) or image.mode!='RGBA':raise ValueError('Invalid poster: '+name)
            if not image.getchannel('A').getbbox():raise ValueError('Empty poster: '+name)
else:
    OUT.mkdir(parents=True,exist_ok=True)
    posters={}
    for name,asset in assets.items():
        source=SOURCE/(name+'.png')
        metadata=SOURCE/(name+'.json')
        if not source.exists() or not metadata.exists():
            if args.allow_partial:continue
            raise ValueError('Missing rendered poster: '+name)
        recorded=json.loads(metadata.read_text())
        if recorded['blendSha256']!=asset['blendSha256'] or recorded['glbSha256']!=asset['sha256']:
            raise ValueError('Stale rendered poster: '+name)
        target=OUT/(name+'.webp')
        encoding={'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'quality':85,'method':3}
        cache=SOURCE/(name+'.webp.json')
        if not target.exists() or not cache.exists() or json.loads(cache.read_text())!=encoding:
            with Image.open(source) as image:
                temporary=target.with_suffix('.tmp.webp')
                image.save(temporary,'WEBP',quality=encoding['quality'],method=encoding['method'])
                temporary.replace(target)
            cache.write_text(json.dumps(encoding)+'\n')
        posters[name]={**recorded,'url':'/models/posters/'+name+'.webp','sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'bytes':target.stat().st_size}
    manifest_path.write_text(json.dumps({'generator':'scripts/blender/render_posters.py + sync_posters.py','assets':posters},ensure_ascii=False,indent=2)+'\n')
print(f'PASS: {len(posters):,} Blender posters '+('verified.' if args.check else 'published.'))
