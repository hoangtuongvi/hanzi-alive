"""Detailed human-action memory dioramas for 人, 大, 太 and 从.

Original mnemonic scenes, not reconstructions of character origins. Builders
use x-right/y-up/z-front coordinates and emit ordered anchor_part_N empties.
"""
import math

import bpy
from mathutils import Matrix

from rest_scene import material, oval, tube, leaf, anchor, v
from family_scene import _head, _arm, _box


def _palette(name):
    return {key:material(name+' / '+key,color,rough) for key,color,rough in [
        ('soil','#63573d',.96),('moss','#527245',.94),('path','#b19b70',.90),
        ('skin','#d6a775',.72),('child_skin','#dfb487',.73),('cheek','#c98d78',.79),('smile','#985d49',.83),
        ('shirt','#b96745',.87),('shirt_light','#d68b5a',.85),('blue','#537b86',.89),('blue_light','#81a5ab',.86),
        ('trousers','#455b65',.91),('trousers_light','#6c7f88',.93),
        ('hair','#343a30',.83),('hair_light','#525540',.87),('shoe','#474b3c',.92),('sole','#b5ab8b',.96),
        ('wood','#9e794c',.87),('wood_dark','#725336',.93),('rope','#d3bd86',.92),
        ('water','#69a9b7',.40),('water_light','#a2d1ce',.40),('stone','#a2a084',.93),
    ]}


def _person(name,center,scale,mats,pose='stride',turn=0,blue=False):
    """A complete clothed figure with articulated limbs, face, hair and fabric."""
    before=set(bpy.context.scene.objects)
    shirt=mats['blue' if blue else 'shirt']; cuff=mats['blue_light' if blue else 'shirt_light']
    # Local feet rest at y=0; head reaches y=3.5.
    oval(name+' shirt hem',(0,1.51,0),(.31,.22,.255),shirt)
    tube(name+' linen torso',[(0,1.56,0),(.04,2.04,-.015),(.10,2.54,0)],[.29,.26,.265],shirt,4)
    oval(name+' shoulders',(.10,2.51,0),(.38,.18,.25),shirt)
    tube(name+' neck',[(.10,2.56,0),(.11,2.79,.015)],[.09,.075],mats['skin'])
    _head(name+' face',(.11,3.08,.025),1,0,False,mats)
    tube(name+' collar',[(-.10,2.57,.17),(.09,2.45,.256),(.28,2.57,.16)],[.02,.024,.018],cuff,2)
    for i in range(3):
        tube(name+' shirt fold%d'%i,[(-.16+i*.14,2.15,.223),(-.18+i*.14,1.86,.25),(-.15+i*.13,1.60,.25)],[.004,.008,.003],cuff,1)
    if pose=='stride':
        legs=[((-.12,1.51,-.045),(-.39,.81,.15),(-.74,.12,.27)),((.15,1.51,-.015),(.43,.89,-.19),(.69,.15,-.39))]
        arms=[((-.20,2.49,.025),(-.44,1.99,.25),(-.61,1.65,.43)),((.40,2.49,0),(.59,2.07,-.22),(.40,1.73,-.37))]
    elif pose=='wide':
        legs=[((-.14,1.51,0),(-.28,.80,.03),(-.43,.10,.03)),((.14,1.51,0),(.32,.80,0),(.51,.10,-.04))]
        arms=[((-.19,2.50,0),(-.80,2.46,.015),(-1.47,2.48,.035)),((.40,2.50,0),(1.00,2.46,.015),(1.64,2.48,.035))]
    else:
        legs=[((-.14,1.51,0),(-.39,.84,.23),(-.49,.10,.16)),((.14,1.51,0),(.48,.84,.22),(.66,.10,.12))]
        arms=[((-.20,2.49,.015),(-.63,2.12,.12),(-.71,2.70,.32)),((.40,2.49,0),(.73,2.12,.12),(.89,2.70,.32))]
    for i,(hip,knee,ankle) in enumerate(legs):
        tube(name+' trouser leg%d'%i,[hip,knee,ankle],[.18,.15,.085],mats['trousers'],3)
        oval(name+' knee fold%d'%i,knee,(.151,.14,.145),mats['trousers'])
        shoe=(ankle[0],.077,ankle[2]+.14)
        oval(name+' walking shoe%d'%i,shoe,(.16,.084,.28),mats['shoe'])
        oval(name+' sole%d'%i,(shoe[0],.017,shoe[2]),(.164,.021,.282),mats['sole'],20,10)
        tube(name+' seam%d'%i,[(knee[0],knee[1]+.08,knee[2]+.145),(ankle[0],ankle[1]+.08,ankle[2]+.082)],[.007,.005],mats['trousers_light'],1)
    for i,points in enumerate(arms):
        _arm(name+' arm%d'%i,points,1,shirt,cuff,mats['skin'],-1 if i==0 else 1)
    transform=Matrix.Translation(v(center))@Matrix.Rotation(turn,4,'Z')@Matrix.Scale(scale,4)
    for obj in set(bpy.context.scene.objects)-before:
        obj.name=name+' / '+obj.name
        obj.matrix_world=transform@obj.matrix_world


def _ground(mats,wide=2.32):
    oval('Land / rounded earth island',(0,-1.84,0),(wide,.18,1.21),mats['soil'],40,14)
    oval('Land / moss carpet',(0,-1.70,0),(wide*.97,.07,1.15),mats['moss'],40,12)
    for i,(x,z) in enumerate([(-1.72,-.38),(1.69,.45),(-1.67,.57),(1.75,-.40)]):
        oval('Land / pebble%d'%i,(x,-1.625,z),(.15,.064,.1),mats['stone'],16,8)
        for k in range(3):
            leaf('Land / grass%d%d'%(i,k),(x+.13,-1.64,z),(x+.17+(k-1)*.10,-1.38-k*.015,z+.06),.035,mats['moss'],.025)


def _anchors(points,glyphs,images):
    for i,(p,g,image) in enumerate(zip(points,glyphs,images)):
        obj=anchor('anchor_part_'+str(i),p);obj['glyph']=g;obj['label']=image


def build_person():
    mats=_palette('Person');_ground(mats,1.98)
    _person('Striding traveler',(0,-1.625,0),1,mats,'stride',-.21)
    # Paired impressions behind the traveler connect the long legs to walking.
    for i,(x,z) in enumerate([(.92,-.67),(1.13,-.45)]):
        oval('Path / footprint%d'%i,(x,-1.614,z),(.11,.012,.23),mats['path'],20,10)
    _anchors([(.10,.36,.39)],['人'],['person'])
    return {'title':'A person in stride','design':'A detailed clothed traveler strides on two long legs, with a warm face, fabric folds, shoes and footprints.','anchors':{'anchor_part_0':'人'}}


def build_big():
    mats=_palette('Big');_ground(mats,2.31)
    _person('Wide-armed person',(-.05,-1.625,0),.96,mats,'wide',0)
    # Exactly one continuous bar defines the reach of both outstretched arms.
    _box('One / continuous broad measuring bar',(.045,.77,.065),(3.49,.105,.10),mats['wood'],.034)
    for x in (-1.66,1.77):
        oval('One / polished rounded bar end',(x,.77,.065),(.075,.074,.077),mats['rope'])
    _anchors([(-1.37,.79,.29),(.12,-.04,.36)],['一','人'],['one','person'])
    return {'title':'Show how big','design':'A person spreads both arms along one wide wooden bar, making the large span visible.','anchors':{'anchor_part_0':'一','anchor_part_1':'人'}}


def _drop(center,size,mat):
    verts=[];faces=[];segments=32;rings=16
    x,y,z=center
    for j in range(rings+1):
        t=j/rings
        radius=math.sin(math.pi*t)**.82*(1-.57*t)*size
        yy=y+(t-.36)*size*2.05
        for k in range(segments):
            a=k/segments*math.tau;verts.append(v((x+radius*math.cos(a),yy,z+radius*math.sin(a))))
    for j in range(rings):
        for k in range(segments):
            a=j*segments+k;b=j*segments+(k+1)%segments;faces.append((a,b,b+segments,a+segments))
    mesh=bpy.data.meshes.new('Extra drop');mesh.from_pydata(verts,[],faces);mesh.update()
    obj=bpy.data.objects.new('Drop / sculpted falling teardrop',mesh);bpy.context.collection.objects.link(obj);obj.data.materials.append(mat)
    for p in mesh.polygons:p.use_smooth=True


def build_too_much():
    mats=_palette('Too much');_ground(mats,2.38)
    _person('Straining carrier',(-.48,-1.625,.13),.75,mats,'carry',-.05)
    # A large, fabric-wrapped load rests across the shoulders. Crossed ropes and
    # a bulging silhouette establish weight; the extra drop tips the story.
    oval('Big / overloaded parcel',(.15,.61,-.19),(1.42,.76,.66),mats['wood'],36,20)
    for z in (-.49,.11):
        tube('Big / taut wrapping rope',[(-1.18,.41,z),(-.88,1.11,z),(.1,1.39,z),(1.18,1.02,z),(1.54,.40,z)],[.029,.03,.027,.03,.029],mats['rope'],2)
    tube('Big / crosswise rope',[(-1.2,.65,-.32),(-.6,.79,.47),(.2,.85,.5),(1.36,.59,.28)],[.027,.026,.027,.022],mats['rope'],2)
    _drop((1.07,1.84,.28),.34,mats['water'])
    oval('Drop / reflected glint',(.95,1.89,.505),(.050,.105,.022),mats['water_light'])
    for x,y in [(-1.39,.11),(-1.57,-.02),(1.48,.01)]:
        tube('Load / strain line',[(x,y,.42),(x-.06,y-.17,.42)],[.018,.025],mats['wood_dark'],2)
    _anchors([(-.25,.88,.59),(1.08,1.89,.47)],['大','丶'],['big','drop'])
    return {'title':'One drop too much','design':'A carrier braces beneath a large rope-wrapped parcel as one oversized extra water drop descends onto the load.','anchors':{'anchor_part_0':'大','anchor_part_1':'丶'}}


def build_follow():
    mats=_palette('From');_ground(mats,2.44)
    # A warm stone threshold marks the origin; successive footprints lead from
    # it to two people walking in the same direction, one behind the other.
    _box('Origin / low starting threshold',(-1.83,-1.57,-.47),(.62,.14,.62),mats['wood'],.055)
    for x in (-2.09,-1.56):
        _box('Origin / doorway post',(x,-1.22,-.57),(.085,.68,.085),mats['rope'],.025)
    _box('Origin / doorway lintel',(-1.83,-.83,-.57),(.62,.09,.09),mats['rope'],.025)
    for i in range(5):
        x=-1.50+i*.50;z=-.18+(i%2)*.18
        oval('Path / departing footprint%d'%i,(x,-1.613,z),(.105,.012,.19),mats['path'],20,10)
    _person('Following person',(-.88,-1.625,-.16),.76,mats,'stride',-.28,False)
    _person('Leading person',(.91,-1.625,.30),.76,mats,'stride',-.28,True)
    _anchors([(-.82,-.04,.27),(.97,-.03,.70)],['人','人'],['person','person'])
    return {'title':'Where they came from','design':'Two detailed travelers move in the same direction, one following the other away from a small doorway threshold and a trail of footprints.','anchors':{'anchor_part_0':'人','anchor_part_1':'人'}}
