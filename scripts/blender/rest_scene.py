"""Blender-authored resting traveler and shade tree for the 休 lesson.
All helpers accept the viewer's x/right, y/up, z/front coordinates.
"""
import bpy
import math
import random
from mathutils import Vector


def v(p):
    return Vector((p[0], -p[2], p[1]))


def material(name, color, roughness=.8):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    rgb = [int(color[i:i+2], 16) / 255 for i in (1, 3, 5)]
    linear = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in rgb]
    m.diffuse_color = (*linear, 1)
    p = m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value = (*linear, 1)
    p.inputs['Roughness'].default_value = roughness
    return m


def finish(obj, name, mat):
    obj.name = name
    obj.data.materials.append(mat)
    if obj.type == 'MESH':
        for p in obj.data.polygons:
            p.use_smooth = True
    return obj


def oval(name, pos, scale, mat, segments=24, rings=12):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=v(pos))
    obj = finish(bpy.context.object, name, mat)
    obj.scale = (scale[0], scale[2], scale[1])
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return obj


def tube(name, points, radii, mat, resolution=3):
    c = bpy.data.curves.new(name, 'CURVE')
    c.dimensions = '3D'
    c.resolution_u = 10
    c.bevel_depth = 1
    c.bevel_resolution = resolution
    c.use_fill_caps = True
    s = c.splines.new('BEZIER')
    s.bezier_points.add(len(points)-1)
    for b, p, radius in zip(s.bezier_points, points, radii):
        b.co = v(p)
        b.radius = radius
        b.handle_left_type = 'AUTO'
        b.handle_right_type = 'AUTO'
    obj = bpy.data.objects.new(name, c)
    bpy.context.collection.objects.link(obj)
    return finish(obj, name, mat)


def leaf(name, start, end, width, mat, curl=.09):
    a, b = v(start), v(end)
    direction = (b-a).normalized()
    normal = v((0, .72, .7)).normalized()
    across = direction.cross(normal).normalized()
    normal = across.cross(direction).normalized()
    verts, faces = [], []
    rows = 9
    for i in range(rows):
        t = i/(rows-1)
        w = width * math.sin(math.pi*t) ** .78
        center = a.lerp(b, t) + normal * (math.sin(math.pi*t)*curl)
        for side in (-1, 0, 1):
            q = center + across * w * side + normal * (abs(side)*-.028*math.sin(math.pi*t))
            verts.append(q)
    for i in range(rows-1):
        for k in range(2):
            q = i*3+k
            faces.append((q, q+1, q+4, q+3))
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    finish(obj, name, mat)
    smooth = obj.modifiers.new('Rounded leaf edges', 'SUBSURF')
    smooth.levels = 1
    smooth.render_levels = 1
    mod = obj.modifiers.new('Leaf thickness', 'SOLIDIFY')
    mod.thickness = .008
    return obj


def anchor(name, pos):
    obj = bpy.data.objects.new(name, None)
    obj.location = v(pos)
    obj.empty_display_type = 'SPHERE'
    obj.empty_display_size = .07
    bpy.context.collection.objects.link(obj)
    return obj


def build_rest():
    rng = random.Random(83)
    mats = {key: material('Rest / '+key, color, roughness) for key, color, roughness in [
        ('soil', '#66573f', .98), ('moss', '#577348', .97),
        ('bark', '#77563b', .93), ('bark_light', '#987147', .94),
        ('bark_dark', '#59462f', .98), ('leaf_dark', '#35643f', .88),
        ('leaf', '#57854a', .87), ('leaf_light', '#80a860', .86),
        ('skin', '#d6a775', .72), ('skin_shade', '#ba825d', .81),
        ('shirt', '#bd6742', .91), ('shirt_light', '#d38755', .89),
        ('trousers', '#455e6c', .93), ('trousers_light', '#637785', .95),
        ('hair', '#353a2d', .84), ('shoe', '#4b4b3b', .91),
        ('sole', '#c1b699', .96), ('stone', '#9e9c7d', .97),
    ]}
    oval('Moss covered island', (0, -1.93, 0), (2.13, .19, 1.15), mats['soil'], 48, 16)
    oval('Soft moss bed', (0, -1.80, 0), (2.04, .10, 1.08), mats['moss'], 48, 12)
    tube('Sculpted trunk', [( .67,-1.80,0),(.71,-.95,-.015),(.59,-.1,.03),(.62,.56,-.03),(.46,1.33,0)], [.25,.215,.19,.13,.045], mats['bark'], 4)
    branches = [
        ([(.61,.18,0),(.02,.69,-.02),(-.63,1.00,.05),(-1.29,1.2,.12)], [.14,.1,.059,.013]),
        ([(.60,.5,-.02),(1.10,.99,-.1),(1.61,1.3,-.17)], [.12,.073,.015]),
        ([(.52,.93,0),(.13,1.44,.13),(-.33,1.7,.25)], [.10,.052,.015]),
        ([(.58,.35,.06),(.90,.91,.51),(1.02,1.32,.73)], [.11,.066,.012]),
        ([(.62,.50,-.07),(.59,1.18,-.56),(.31,1.55,-.82)], [.09,.051,.012]),
        ([(0,.68,-.02),(-.16,1.13,.31),(-.49,1.39,.56)], [.062,.032,.011]),
    ]
    for i, (pts, widths) in enumerate(branches):
        tube('Arching branch %02d'%i, pts, widths, mats['bark_light'], 3)
    for i, (x,z) in enumerate([(-.12,.47),(1.36,.48),(1.32,-.35),(.18,-.62)]):
        tube('Exposed root %02d'%i,[(.66,-1.56,0),((x+.66)/2,-1.76,z*.5),(x,-1.8,z)],[.12,.07,.012],mats['bark_light'])
    for i in range(7):
        x=.49+i*.055
        tube('Fine bark ridge %02d'%i,[(x,-1.55,.16),(x-.045,-.75,.19),(x-.04,-.15,.15)],[.008,.012,.005],mats['bark_dark'],1)
    clusters=[(-1.12,1.28,.08,.7),(-.56,1.64,-.13,.85),(.27,1.89,-.10,.9),(1.08,1.74,-.07,.75),(1.59,1.45,.08,.56),(.75,1.30,.64,.66),(-.42,1.35,.58,.73),(.20,1.62,-.68,.69)]
    for ci,(cx,cy,cz,radius) in enumerate(clusters):
        for k in range(17):
            angle=rng.random()*math.tau
            distance=math.sqrt(rng.random())*radius*.70
            x=cx+math.cos(angle)*distance
            z=cz+math.sin(angle)*distance*.65
            y=cy+rng.uniform(-.16,.16)
            heading=angle+rng.uniform(-1,1)
            length=rng.uniform(.38,.70)
            start=(x-math.cos(heading)*length*.4,y-.08,z-math.sin(heading)*length*.4)
            end=(x+math.cos(heading)*length*.6,y+rng.uniform(.05,.29),z+math.sin(heading)*length*.6)
            mat=mats[['leaf_dark','leaf','leaf_light'][(k+ci)%3]]
            leaf('Canopy leaf %02d %02d'%(ci,k),start,end,rng.uniform(.15,.25),mat)
    # A clothed, relaxed seated figure; the leaning body and resting hands carry the meaning.
    oval('Seated shirt hem',(-.01,-1.50,.21),(.31,.22,.31),mats['shirt'])
    torso=tube('Linen shirt torso',[(-.02,-1.44,.21),(.10,-.97,.17),(.29,-.49,.13)],[.275,.25,.235],mats['shirt'],4)
    oval('Shoulder fabric',(.27,-.49,.13),(.25,.20,.26),mats['shirt'])
    tube('Neck',[(.28,-.40,.13),(.23,-.23,.13)],[.083,.076],mats['skin'])
    head=oval('Face',(.18,-.055,.145),(.184,.23,.19),mats['skin'],32,20)
    oval('Soft chin',(.105,-.205,.175),(.12,.07,.132),mats['skin'])
    oval('Nose',(.007,-.074,.208),(.069,.047,.054),mats['skin'])
    oval('Ear',(.29,-.069,.301),(.045,.065,.025),mats['skin_shade'])
    # A cap built from a spherical patch preserves a visible face instead of a second ball.
    verts, faces=[],[]
    for j in range(10):
        theta=(j/9)*1.75
        for i in range(32):
            phi=i/32*math.tau
            verts.append(v((.204+.197*math.sin(theta)*math.cos(phi),.006+.21*math.cos(theta),.133+.197*math.sin(theta)*math.sin(phi))))
    for j in range(9):
        for i in range(32):
            q=j*32+i;r=j*32+(i+1)%32
            faces.append((q,r,r+32,q+32))
    mesh=bpy.data.meshes.new('Hair cap');mesh.from_pydata(verts,[],faces);mesh.update()
    obj=bpy.data.objects.new('Sculpted hair',mesh);bpy.context.collection.objects.link(obj);finish(obj,'Sculpted hair',mats['hair'])
    for i in range(5):
        tube('Swept hair lock %02d'%i,[(.02+i*.045,.105,.24),(.09+i*.041,.177,.18),(.25+i*.02,.16,.1)],[.018,.022,.006],mats['hair'],2)
    tube('Closed resting eye',[(.005,-.021,.274),(.036,-.033,.292),(.078,-.025,.302)],[.007,.009,.004],mats['hair'],2)
    tube('Quiet smile',[(-.009,-.139,.252),(.02,-.152,.27),(.049,-.145,.282)],[.004,.006,.003],mats['skin_shade'],2)
    # Collar, elbow folds and knee seams give the figure a fabric silhouette.
    tube('Open shirt collar',[(.14,-.4,.29),(.20,-.48,.362),(.31,-.40,.30)],[.018,.019,.013],mats['shirt_light'],2)
    for i,z in enumerate([-.02,.48]):
        tube('Bent trouser leg %d'%i,[(-.04,-1.52,z),(-.57,-1.55,z+.05),(-1.12,-1.70,z+.16)],[.19,.16,.095],mats['trousers'],4)
        oval('Fabric knee %d'%i,(-.57,-1.55,z+.05),(.17,.15,.16),mats['trousers'])
        shoe=oval('Soft walking shoe %d'%i,(-1.29,-1.72,z+.19),(.28,.11,.13),mats['shoe'])
        sole=oval('Leather sole %d'%i,(-1.3,-1.793,z+.20),(.276,.022,.131),mats['sole'])
        tube('Trouser seam %d'%i,[(-.55,-1.45,z+.195),(-.85,-1.55,z+.24),(-1.1,-1.64,z+.245)],[.007,.008,.005],mats['trousers_light'],1)
    for i,z in enumerate([-.075,.375]):
        tube('Rolled shirt sleeve %d'%i,[(.28,-.48,z),(.12,-.74,z+.05),(-.03,-.89,z+.09)],[.145,.128,.105],mats['shirt'],3)
        tube('Sleeve cuff %d'%i,[(-.004,-.866,z+.065),(-.052,-.927,z+.11)],[.114,.11],mats['shirt_light'],3)
        tube('Relaxed forearm %d'%i,[(-.047,-.91,z+.11),(-.29,-1.19,z+.15),(-.53,-1.45,z+.15)],[.079,.068,.047],mats['skin'],3)
        palm=oval('Resting hand %d'%i,(-.585,-1.466,z+.15),(.108,.05,.072),mats['skin'])
        for k in range(4):
            tube('Finger %d %d'%(i,k),[(-.6,-1.467,z+.1+k*.031),(-.696,-1.495,z+.11+k*.028),(-.731,-1.51,z+.112+k*.028)],[.015,.014,.005],mats['skin'],1)
        tube('Shirt fold %d'%i,[(.18,-.62,z+.1),(.16,-.69,z+.125),(.06,-.73,z+.137)],[.004,.009,.003],mats['shirt_light'],1)
    for i in range(14):
        a=rng.random()*math.tau
        x=math.cos(a)*rng.uniform(1.35,1.94);z=math.sin(a)*rng.uniform(.62,.91)
        stone=oval('River stone %02d'%i,(x,-1.76,z),(rng.uniform(.055,.13),.045,rng.uniform(.05,.11)),mats['stone'],12,8)
        stone.rotation_euler[2]=rng.random()*math.tau
    for i,(x,z) in enumerate([(-1.65,-.3),(-1.82,.3),(1.36,.56),(1.66,-.28),(.10,-.79)]):
        for k in range(6):
            a=k*math.tau/6
            leaf('Ground grass %d %d'%(i,k),(x,-1.77,z),(x+math.cos(a)*.16,-1.4-rng.random()*.1,z+math.sin(a)*.15),.037,mats['leaf_light' if k%2 else 'leaf'],.025)
    anchor('anchor_person',(-.06,-.52,.42))
    anchor('anchor_tree',(.65,.96,.25))
    return {'design':'A relaxed traveler in draped linen under a layered broadleaf tree; historical clothing is not asserted.'}
