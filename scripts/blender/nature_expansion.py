"""Four literal, sculpted nature mnemonics for the illustrated collection.

Each builder follows public/data/lessons.json without presenting an invented
story as historical etymology. Geometry uses the established viewer coordinates
and exports through Blender's ordinary glTF exporter without external assets.
"""

import math
import random

import bpy
from mathutils import Matrix, Vector

from rest_scene import material, oval, tube, leaf, anchor, v
from nature_scenes import _palette, _pebble, _blade, _mesh
from shared_scenes import _tree_prototype


def _label(index, position, glyph, image):
    obj = anchor('anchor_part_%d' % index, position)
    obj['glyph'] = glyph
    obj['label'] = image


def _box(name, position, dimensions, mat, bevel=.025):
    bpy.ops.mesh.primitive_cube_add(size=1, location=v(position))
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = (dimensions[0], dimensions[2], dimensions[1])
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    mod = obj.modifiers.new('Rounded handmade corners', 'BEVEL')
    mod.width = bevel
    mod.segments = 3
    obj.modifiers.new('Soft corner normals', 'WEIGHTED_NORMAL')
    return obj


def _ground(name, mats, y=-1.5, extent=(2.12, 1.22)):
    _pebble(name + ' / dark earth', (0, y-.16, 0), (extent[0], .23, extent[1]), mats['earth'], 814, 48, 16)
    _pebble(name + ' / moss cover', (0, y, 0), (extent[0]-.08, .085, extent[1]-.055), mats['soil'], 815, 48, 12)


def _edge_plants(name, mats, positions, floor=-1.45):
    rng = random.Random(271)
    for index, (x,z) in enumerate(positions):
        for blade in range(6):
            _blade(name+' / grass %d %d' % (index,blade), (x,floor,z),
                   rng.uniform(.25,.45), .043, blade*math.tau/6+.2,
                   .15, mats[['grass','grass_light','grass_deep'][blade%3]])
        _pebble(name+' / pebble %d' % index, (x+.16,floor+.015,z+.08),
                (.115,.057,.078), mats['stone_light'], 920+index, 16, 8)


def build_tree():
    """木: a living cross-shaped trunk and bough gain two spreading roots."""
    mats = _palette()
    bark = material('Tree / familiar warm bark','#77563b',.93)
    bark_light = material('Tree / branch highlights','#987147',.94)
    bark_dark = material('Tree / bark creases','#59462f',.98)
    _ground('Tree',mats)
    tube('Tree / central trunk of the cross',[(0,-1.43,0),(.02,-.55,0),(0,.35,0),(.03,1.50,0)],
         [.25,.205,.16,.047],bark,4)
    tube('Tree / crossing horizontal bough',[(-1.30,.40,.015),(-.67,.39,0),(0,.38,0),(.65,.39,0),(1.30,.42,.015)],
         [.036,.089,.143,.087,.031],bark_light,3)
    # Ten buds make the selected “ten” memory image concrete without adding
    # typography; the trunk and bough still form the story's wooden cross.
    rng=random.Random(552)
    for side in (-1,1):
        for bud in range(5):
            x=side*(.35+bud*.19)
            tube('Tree / twig %d %d'%(side,bud),[(x,.4,0),(x+side*.04,.69,.01),(x+side*.07,.87,.04)],
                 [.018,.012,.006],bark_light,2)
            for k in range(4):
                a=k*math.tau/4+bud*.7
                leaf('Tree / bud leaf %d %d %d'%(side,bud,k),
                     (x,.71,.02),(x+math.cos(a)*.24,.98+rng.uniform(-.05,.07),math.sin(a)*.19),
                     .078,mats['grass_light' if k%2 else 'grass'],.035)
    for side in (-1,1):
        tube('Tree / spreading main root %d'%side,[(0,-.97,.04),(side*.43,-1.30,.30),(side*1.29,-1.44,.54)],
             [.175,.112,.035],bark_light,3)
        # The two root fans contain eight smaller roots between them, while
        # retaining the two spreading strokes described in the story.
        for branch in range(4):
            x=side*(.52+branch*.23); z=.31+branch*.07
            tube('Tree / eight rootlets %d %d'%(side,branch),
                 [(x,-1.37,z),(x+side*.14,-1.42,z+.19),(x+side*.26,-1.45,z+.27)],
                 [.044,.023,.005],bark,2)
    for index in range(5):
        x=(index-2)*.039
        tube('Tree / fine trunk grain %d'%index,[(x,-1.07,.17),(x+.015,-.49,.202),(x-.006,.13,.156)],
             [.004,.010,.003],bark_dark,1)
    for index,(x,y,z) in enumerate([(-.25,1.40,-.07),(.15,1.48,.10),(.40,1.37,-.05),(-.05,1.57,-.13)]):
        for k in range(7):
            a=k*math.tau/7+index
            leaf('Tree / crown leaf %d %d'%(index,k),(x,y,z),
                 (x+math.cos(a)*.42,y+.23,z+math.sin(a)*.31),.13,
                 mats['grass_light' if k%3 else 'grass'],.07)
    _edge_plants('Tree',mats,[(-1.65,-.28),(1.58,-.24),(-1.62,.54),(1.60,.58)])
    _label(0,(0,.43,.20),'十','ten')
    _label(1,(.75,-1.30,.59),'八','eight')
    return {'title':'A cross grows roots','anchors':{'anchor_part_0':'十','anchor_part_1':'八'},
            'story':'A cross becomes a tree trunk; two spreading strokes become its roots.',
            'design':'A sculpted trunk crosses a living bough with ten leaf buds. Two spreading root fans divide into eight fine roots on a moss island.',
            'interpretation':'An invented visual mnemonic, not a historical reconstruction.'}


def _book(name,position,scale,turn,cover,pages,accent):
    objects=[]
    objects.append(_box(name+' / pages',(0,.04,0),(.34,.54,.105),pages,.015))
    for z in (-.079,.079):
        objects.append(_box(name+' / cloth cover',(0,.045,z),(.40,.60,.030),cover,.018))
    objects.append(_box(name+' / rounded spine',(-.188,.045,0),(.038,.60,.155),cover,.018))
    for y in (-.17,-.08,.01,.10,.19):
        objects.append(tube(name+' / page edge',[(.173,y,-.044),(.176,y,.044)],[.002,.002],accent,1))
    objects.append(_box(name+' / inset cover border',(0,.04,.098),(.28,.44,.010),accent,.014))
    objects.append(_box(name+' / cloth inset',(0,.04,.107),(.235,.395,.008),cover,.012))
    transform=Matrix.Translation(v(position))@Matrix.Rotation(turn,4,'Y')@Matrix.Scale(scale,4)
    for obj in objects:obj.matrix_world=transform@obj.matrix_world


def build_root_books():
    """本: a single physical pointing line leads to books at a tree's root."""
    prototype=_tree_prototype()
    place=Matrix.Translation(v((.14,-1.45,-.16)))@Matrix.Scale(.83,4)@Matrix.Translation(-v((.67,-1.8,0)))
    for obj in prototype:
        obj.name='Book tree / '+obj.name
        obj.matrix_world=place@obj.matrix_world
    mats=_palette()
    _ground('Book tree',mats,extent=(2.22,1.24))
    rootmat=material('Books / familiar warm root','#987147',.94)
    pages=material('Books / ivory pages','#e6d7b5',.88)
    accent=material('Books / faded gold binding','#c0a66d',.8)
    covers=[material('Books / sage cover','#668251',.86),material('Books / terracotta cover','#b96743',.86),material('Books / blue cloth cover','#527686',.88)]
    for index,(x,y,z,scale,turn) in enumerate([(-.84,-1.08,.50,1.02,-.20),(-.17,-1.02,.78,.94,.09),(.73,-1.09,.66,1.08,.25)]):
        tube('Books / growing root %d'%index,[(.14,-1.18,-.05),(x*.6,-1.37,z*.5),(x,-1.42,z),(x,-1.27,z)],
             [.12,.075,.036,.028],rootmat,3)
        _book('Books / sprouting volume %d'%index,(x,y,z),scale,turn,covers[index],pages,accent)
    # The one cue is one brass-tinted wooden pointer, directed to the root.
    # No detached glyph or text card substitutes for the actual story object.
    pointer=material('Books / single pointing line','#d4ad55',.73)
    tube('Books / one line pointing at the root',[(-1.67,-.95,.22),(-.13,-.95,.22)],[.028,.028],pointer,3)
    oval('Books / root meeting point',(.13,-1.10,.0),(.15,.08,.12),rootmat,24,12)
    _edge_plants('Books',mats,[(-1.7,-.29),(1.75,-.28),(1.56,.53)])
    _label(0,(.18,.59,.12),'木','tree')
    _label(1,(-1.04,-.95,.26),'一','one')
    return {'title':'Books grow from the root','anchors':{'anchor_part_0':'木','anchor_part_1':'一'},
            'story':"One line points to a tree's root; imagine books growing from that root, counted with 本.",
            'design':'The established broadleaf tree grows three cloth-bound books from visible roots. One golden pointer leads to the root beneath the trunk.',
            'interpretation':'An invented visual mnemonic for the selected book-classifier sense.'}


def _stream(name,points,widths,mat,depth=.09):
    """A solid, gently rippled ribbon with banks, volume and a closed bottom."""
    vertices=[];faces=[]
    for index,p in enumerate(points):
        before=Vector(points[max(0,index-1)]);after=Vector(points[min(len(points)-1,index+1)])
        tangent=after-before
        side=Vector((-tangent.z,0,tangent.x)).normalized()
        for down in (0,depth):
            for k in range(5):
                fraction=(k-2)/2
                q=Vector(p)+side*widths[index]*fraction
                q.y-=down
                if down==0:q.y+=math.sin(index*.9+k*.55)*.008
                vertices.append(tuple(q))
    for index in range(len(points)-1):
        a=index*10;b=(index+1)*10
        for k in range(4):
            faces.extend([(a+k,a+k+1,b+k+1,b+k),(a+k+6,a+k+5,b+k+5,b+k+6)])
        faces.extend([(a,a+5,b+5,b),(a+4,b+4,b+9,a+9)])
    faces.extend([(4,3,2,1,0,5,6,7,8,9)])
    end=(len(points)-1)*10
    faces.append(tuple(end+k for k in (0,1,2,3,4,9,8,7,6,5)))
    obj=_mesh(name,vertices,faces,mat)
    return obj


def _curve_points(knots,steps=10):
    points=[]
    # Cosine interpolation smooths banks and avoids sharp flat ribbon corners.
    for index in range(len(knots)-1):
        for sample in range(steps):
            t=sample/steps
            eased=(1-math.cos(t*math.pi))/2
            points.append(tuple(knots[index][a]*(1-eased)+knots[index+1][a]*eased for a in range(3)))
    points.append(knots[-1])
    return points


def build_water():
    """水: a raised central stream splashes into four flowing branches."""
    mats=_palette()
    water=material('Stream / jade blue water','#609eaa',.23)
    glint=material('Stream / bright ripple','#c4e2d4',.32)
    _ground('Stream',mats,y=-1.30,extent=(2.26,1.55))
    # An elevated rear spring supplies a sloping main channel, rather than a
    # flat water symbol pasted on the island.
    _pebble('Stream / rear spring rock',(0,-.92,-1.03),(.67,.45,.40),mats['stone_dark'],130,32,16)
    channels=[
        ([(0,-.48,-1.11),(.12,-.63,-.56),(-.03,-.91,.01),(.04,-1.12,.61),(0,-1.15,1.37)],.22),
        ([(.10,-.70,-.43),(-.56,-.87,-.10),(-1.15,-1.08,.25),(-1.85,-1.17,.69)],.15),
        ([(-.01,-.90,.02),(.65,-1.02,.13),(1.24,-1.14,.51),(1.95,-1.18,.78)],.17),
        ([(.11,-.71,-.49),(.59,-.85,-.67),(1.22,-1.05,-.47),(1.90,-1.14,-.30)],.14),
        ([(.02,-1.08,.47),(-.42,-1.12,.70),(-.99,-1.18,1.05),(-1.58,-1.19,1.11)],.14),
    ]
    for index,(knots,width) in enumerate(channels):
        points=_curve_points(knots,8)
        widths=[width*(1+.11*math.sin(i*.65+index)) for i in range(len(points))]
        _stream('Stream / flowing channel %d'%index,points,widths,water)
        for portion in (8,17):
            if portion+5>=len(points):continue
            line=[(p[0]-.04,p[1]+.017,p[2]) for p in points[portion:portion+6]]
            tube('Stream / current glint %d %d'%(index,portion),line,[.006]*len(line),glint,1)
    # Visible airborne droplets show the stream splitting and splashing.
    for index,(x,y,z) in enumerate([(-.50,-.62,-.05),(-.66,-.49,.03),(.50,-.66,.10),(.73,-.51,.19),(.98,-.91,-.32)]):
        oval('Stream / splash droplet %d'%index,(x,y,z),(.037,.074,.037),water,20,12)
    for index,(x,z,size) in enumerate([(-.47,-.90,.21),(.56,-.87,.22),(-.91,-.41,.18),(-1.47,-.09,.17),(.93,-.02,.14),(1.47,.05,.19),(-.56,1.22,.16),(.56,1.03,.13)]):
        _pebble('Stream / bank stone %d'%index,(x,-1.22+size*.2,z),(size,.12,size*.73),mats['stone_light' if index%2 else 'stone'],170+index,24,12)
    _edge_plants('Stream',mats,[(-1.54,-.72),(-1.83,.22),(1.68,-.70),(1.63,.94)],floor=-1.24)
    # Tilt the riverbank toward the opening camera so branching reads before
    # the learner rotates the scene, retaining fully three-dimensional water.
    transform=Matrix.Translation(v((0,.26,0)))@Matrix.Rotation(math.radians(19),4,'X')
    for obj in list(bpy.context.scene.objects):obj.matrix_world=transform@obj.matrix_world
    point=transform@v((.09,-.81,.08))
    obj=anchor('anchor_part_0',(point.x,point.z,-point.y));obj['glyph']='水';obj['label']='water'
    return {'title':'Follow the branching stream','anchors':{'anchor_part_0':'水'},
            'story':'A central stream splits into splashing side branches; trace the flowing water.',
            'design':'A raised rocky spring feeds a sloping jade stream that divides into four side branches, with current glints, splash droplets, river stones and bank grasses.'}


def _snowflake(name,position,size,mat,turn):
    x,y,z=position
    for arm in range(6):
        a=arm*math.tau/6+turn
        dx,dy=math.cos(a),math.sin(a)
        tube(name+' / crystal arm %d'%arm,[(x,y,z),(x+dx*size,y+dy*size,z)],
             [.014,.008],mat,2)
        for side in (-1,1):
            b=a+side*.82
            start=(x+dx*size*.58,y+dy*size*.58,z)
            end=(start[0]+math.cos(b)*size*.34,start[1]+math.sin(b)*size*.34,z)
            tube(name+' / crystal branch %d %d'%(arm,side),[start,end],[.008,.004],mat,1)


def build_snow():
    """雪: one broom sweeps falling rain into a soft white snowbank."""
    mats=_palette()
    snow=material('Snow / soft ivory','#e4e9dc',.92)
    cloud=material('Snow / rain cloud','#90abb0',.86)
    water=material('Snow / falling rain','#70aeb8',.28)
    straw=material('Snow / golden broom straw','#be9e62',.94)
    straw_light=material('Snow / light straw','#dbbd7d',.96)
    wood=material('Snow / carved broom handle','#886440',.88)
    wrap=material('Snow / woven broom binding','#53715c',.90)
    _ground('Snow',mats,y=-1.52,extent=(2.25,1.28))
    # The blue cloud and vertical droplets occupy the left side; beyond the
    # broom's sweep, droplets become snow crystals over a soft drift.
    for index,(x,y,z,scale) in enumerate([(-1.40,1.30,-.16,(.39,.26,.23)),(-1.05,1.50,-.20,(.48,.40,.28)),(-.59,1.43,-.21,(.39,.32,.27)),(-.26,1.23,-.12,(.36,.23,.24))]):
        oval('Snow / cloud lobe %d'%index,(x,y,z),scale,cloud,32,20)
    oval('Snow / rain cloud base',(-.91,1.24,-.16),(.93,.19,.28),cloud,40,16)
    for index,(x,y,z) in enumerate([(-1.50,.72,-.14),(-.99,.85,.02),(-.53,.63,-.02),(-1.33,.13,.12),(-.87,.29,.10),(-.46,.13,.16),(-1.52,-.58,.11),(-1.09,-.52,.23)]):
        oval('Snow / falling raindrop %d'%index,(x,y,z),(.037,.105,.039),water,20,12)
    # Curved rows of straw and their wraps form a real rounded broom head,
    # pointed down and to the right into the snow it has swept together.
    tube('Snow / long wooden broom handle',[(-.26,1.0,.35),(.04,.29,.46),(.37,-.56,.56)],
         [.064,.062,.066],wood,3)
    oval('Snow / handle cap',(-.26,1.0,.35),(.069,.081,.070),wood,24,12)
    for layer in range(3):
        for strand in range(17):
            spread=(strand-8)/8
            endx=.83+spread*.40
            endz=.63+(layer-1)*.10
            points=[(.35+spread*.12,-.53,.54+(layer-1)*.035),
                    (.50+spread*.23,-.86,.59+(layer-1)*.065),
                    (endx,-1.23-abs(spread)*.027,endz)]
            tube('Snow / sweeping straw %d %d'%(layer,strand),points,[.022,.022,.010],straw_light if strand%3==0 else straw,2)
    for index,y in enumerate((-.61,-.72)):
        x=.40+(index*.06)
        points=[]
        for step in range(33):
            a=step*math.tau/32
            points.append((x+math.cos(a)*(.22+index*.045),y, .55+math.sin(a)*.10))
        tube('Snow / bound straw wrap %d'%index,points,[.026]*len(points),wrap,2)
    # Actual rounded snow piles and frozen flakes occupy the destination of
    # the sweep; a pale arc on the ground makes the direction clear.
    for index,(x,y,z,sx,sy,sz) in enumerate([(.82,-1.39,.61,.66,.16,.42),(1.44,-1.30,.40,.59,.27,.56),(1.25,-1.17,.12,.37,.32,.39),(1.71,-1.43,-.15,.37,.12,.34),(.78,-1.47,-.40,.44,.08,.28)]):
        _pebble('Snow / soft snowdrift %d'%index,(x,y,z),(sx,sy,sz),snow,1000+index,32,16)
    for index,(x,y,z,size) in enumerate([(.96,-.67,.49,.12),(1.42,-.40,.17,.15),(1.73,.09,-.01,.12),(.77,.06,.05,.105)]):
        _snowflake('Snow / swept crystal %d'%index,(x,y,z),size,snow,index*.31)
    for index in range(2):
        points=[]
        for step in range(24):
            a=.25+1.55*step/23
            points.append((-.28+math.cos(a)*(1.01+index*.14),-1.415,.09+math.sin(a)*(.72+index*.1)))
        tube('Snow / curved sweep trail %d'%index,points,[.012]*len(points),snow,2)
    _pebble('Snow / wet ground stone',(-1.66,-1.44,.60),(.22,.08,.16),mats['stone_dark'],172,24,12)
    _label(0,(-1.15,.58,.05),'雨','rain')
    _label(1,(.44,-.66,.69),'彐','broom')
    return {'title':'A broom sweeps rain into snow','anchors':{'anchor_part_0':'雨','anchor_part_1':'彐'},
            'story':'A broom sweeps falling rain into soft white snow.',
            'design':'Blue rain falls from a sculpted cloud onto one side of a mossy island. A bound straw broom sweeps a curved trail into snow crystals and rounded ivory snowdrifts.',
            'interpretation':'An invented visual mnemonic, not a claim about weather or etymology.'}
