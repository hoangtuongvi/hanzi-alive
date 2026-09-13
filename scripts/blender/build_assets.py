"""Rebuild editable Blender sources, self-contained GLBs and preview renders.
Usage: Blender --background --factory-startup --python scripts/blender/build_assets.py -- [scene names|--all] [--render]
"""
import bpy
import sys
import math
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from mathutils import Vector

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
sys.path.insert(0,str(HERE))
from rest_scene import build_rest, v
from nature_scenes import build_clear, build_sunny
from shared_scenes import build_woods, build_forest, build_emotion, build_invite
from device_scenes import build_phone, build_computer, build_parting, build_expert
from family_scene import build_good

SCENES={
    'rest':('休',build_rest), 'clear':('清',build_clear), 'sunny':('晴',build_sunny),
    'woods':('林',build_woods), 'forest':('森',build_forest),
    'emotion':('情',build_emotion), 'invite':('请',build_invite),
    'phone':('手机',build_phone), 'computer':('电脑',build_computer),
    'parting':('分手',build_parting), 'expert':('高手',build_expert),
    'good':('好',build_good),
}


def reset():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for dat in list(bpy.data.materials):
        if dat.users==0:bpy.data.materials.remove(dat)


def prepare_meshes(name):
    # Convert authoring curves and modifiers before export, then combine by
    # material. This retains editable geometry with far fewer browser draw calls.
    for obj in list(bpy.context.scene.objects):
        if obj.type not in {'MESH','CURVE'}:continue
        # Applying modifiers to shared authoring data would apply them again
        # through the next instance, multiplying leaf subdivisions per tree.
        if obj.data.users>1:obj.data=obj.data.copy()
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True);bpy.context.view_layer.objects.active=obj
        bpy.ops.object.convert(target='MESH')
    materials={}
    for obj in list(bpy.context.scene.objects):
        if obj.type=='MESH':
            key=tuple(slot.material.name if slot.material else '' for slot in obj.material_slots)
            materials.setdefault(key,[]).append(obj)
    for i,objects in enumerate(materials.values()):
        if len(objects)>1:
            bpy.ops.object.select_all(action='DESELECT')
            for obj in objects:obj.select_set(True)
            bpy.context.view_layer.objects.active=objects[0]
            bpy.ops.object.join()
        objects[0].name=f'{name}_surface_{i:02d}'
    root=bpy.data.objects.new('Hanzi_'+name+'_Blender',None)
    bpy.context.collection.objects.link(root)
    for obj in list(bpy.context.scene.objects):
        if obj!=root:obj.parent=root
    root['authoring_tool']='Blender'
    root['authoring_version']=bpy.app.version_string
    root['lesson']=SCENES[name][0]
    root['source_script']='scripts/blender/build_assets.py'
    return root


def add_studio():
    scene=bpy.context.scene
    scene.render.engine='CYCLES'
    scene.cycles.device='CPU'
    scene.cycles.samples=24
    scene.cycles.use_denoising=True
    scene.render.resolution_x=1000;scene.render.resolution_y=900
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG'
    scene.render.film_transparent=False
    scene.world.color=(.12,.12,.12)
    scene.world.use_nodes=True
    scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.047,.064,.05,1)
    scene.world.node_tree.nodes['Background'].inputs[1].default_value=.5
    scene.view_settings.view_transform='AgX'
    scene.view_settings.look='AgX - Medium High Contrast'
    scene.view_settings.exposure=.5
    target=v((0,0,0))
    bpy.ops.object.camera_add(location=v((3.4,2.25,10.5)))
    camera=bpy.context.object;camera.name='Preview camera'
    camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
    camera.data.type='ORTHO';camera.data.ortho_scale=6.2
    scene.camera=camera
    for name,pos,power,color,size in [
        ('Warm softbox',(-3,6,6),700,(1,.85,.68),5),
        ('Cool fill',(5,2,4),470,(.70,.86,1),5),
        ('Leaf rim',(1,4,-3),850,(1,.91,.73),4),
    ]:
        bpy.ops.object.light_add(type='AREA',location=v(pos))
        light=bpy.context.object;light.name=name
        light.data.energy=power;light.data.shape='DISK';light.data.size=size
        light.data.color=color
        light.rotation_euler=(target-light.location).to_track_quat('-Z','Y').to_euler()


def run(names, render):
    out=ROOT/'public/models/blender';out.mkdir(parents=True,exist_ok=True)
    native=ROOT/'assets/blender';native.mkdir(parents=True,exist_ok=True)
    previews=ROOT/'outputs/blender';previews.mkdir(parents=True,exist_ok=True)
    manifest_path=out/'manifest.json'
    manifest=json.loads(manifest_path.read_text()) if manifest_path.exists() else {'assets':{}}
    manifest.pop('license',None)
    manifest.update({'authoringTool':'Blender','blenderVersion':bpy.app.version_string,'generatedAt':datetime.now(timezone.utc).isoformat(),'coordinateSystem':'glTF Y-up','generator':'scripts/blender/build_assets.py','notes':'Original scene geometry authored for Hanzi Alive with Blender Python; glyph outlines remain sourced independently.'})
    for name in names:
        reset()
        meta=SCENES[name][1]() or {}
        model=prepare_meshes(name)
        bpy.context.view_layer.update()
        meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
        triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in meshes)
        if triangles>250000:
            raise ValueError(f'{name}: {triangles} triangles exceeds the per-scene browser budget of 250000')
        anchors=[o.name for o in bpy.context.scene.objects if o.name.startswith('anchor_')]
        bpy.ops.object.select_all(action='SELECT')
        glb=out/(name+'.glb')
        bpy.ops.export_scene.gltf(filepath=str(glb),export_format='GLB',use_selection=True,export_yup=True,export_extras=True,export_animations=False,export_apply=True,export_cameras=False,export_lights=False)
        add_studio()
        bpy.context.preferences.filepaths.save_version=0
        bpy.ops.wm.save_as_mainfile(filepath=str(native/(name+'.blend')),compress=True)
        if render:
            bpy.context.scene.render.filepath=str(previews/(name+'.png'))
            bpy.ops.render.render(write_still=True)
        manifest['assets'][name]={'word':SCENES[name][0],'url':'/models/blender/'+name+'.glb','blendFile':'assets/blender/'+name+'.blend','sha256':hashlib.sha256(glb.read_bytes()).hexdigest(),'bytes':glb.stat().st_size,'meshes':len(meshes),'triangles':triangles,'anchors':anchors,'design':meta}
        manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
        print('HANZI_ASSET',name,json.dumps(manifest['assets'][name],ensure_ascii=False),flush=True)

args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
unknown=[a for a in args if a not in SCENES and a not in ['--all','--render']]
if unknown:raise ValueError('Unknown scene names or options: '+', '.join(unknown))
names=list(SCENES) if '--all' in args else [a for a in args if a in SCENES] or ['rest','clear','sunny']
run(names,'--render' in args)
