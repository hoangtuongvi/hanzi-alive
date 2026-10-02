"""Mnemonic dioramas for the next ten non-illustrated corpus lessons."""
import math

import bpy

from rest_scene import material, oval, tube, leaf, anchor, v


def _mat(name, color, rough=.88):
    return material(name, color, rough)


def _box(name, position, dimensions, mat, bevel=.04):
    bpy.ops.mesh.primitive_cube_add(size=1, location=v(position))
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = (dimensions[0], dimensions[2], dimensions[1])
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    modifier = obj.modifiers.new('Rounded edges', 'BEVEL')
    modifier.width = bevel
    modifier.segments = 3
    return obj


def _ground(name, color='#557047'):
    soil = _mat(name + ' earth', '#62523c', .96)
    moss = _mat(name + ' moss', color, .94)
    oval(name + ' earth island', (0, -1.62, 0), (2.34, .20, 1.24), soil, 40, 14)
    oval(name + ' moss top', (0, -1.47, 0), (2.26, .07, 1.18), moss, 40, 12)
    return soil, moss


def _label(index, position, glyph, image):
    obj = anchor('anchor_part_%d' % index, position)
    obj['glyph'] = glyph
    obj['label'] = image


def _hand(name, center, scale=1, facing=1, raised=False):
    skin = _mat(name + ' warm skin', '#d7a575', .76)
    nail = _mat(name + ' nails', '#efd0b7', .72)
    x, y, z = center
    oval(name + ' palm', (x, y, z), (.48*scale, .16*scale, .58*scale), skin, 28, 16)
    for index, (offset, length) in enumerate([(-.34,.56),(-.12,.76),(.10,.84),(.31,.70)]):
        start = (x+offset*scale, y+.22*scale, z+.15*scale)
        end = (start[0]+facing*.04*scale, start[1]+length*scale, start[2])
        tube(name + ' finger %d' % index, [start, end], [.10*scale, .075*scale], skin, 3)
        oval(name + ' nail %d' % index, (end[0], end[1]-.03*scale, end[2]+.075*scale), (.055*scale,.065*scale,.024*scale), nail, 16, 8)
    thumb_start = (x+facing*.36*scale, y+.12*scale, z+.02*scale)
    thumb_end = (x+facing*.68*scale, y+(.34 if raised else .02)*scale, z+.10*scale)
    tube(name + ' thumb', [thumb_start, thumb_end], [.12*scale,.075*scale], skin, 3)
    tube(name + ' wrist', [(x,y-.45*scale,z-.02*scale),(x,y-.86*scale,z-.04*scale)], [.29*scale,.22*scale], skin, 3)


def build_green():
    _ground('Green')
    stem = _mat('Green shoots', '#6f9a55', .88)
    moon = _mat('Green moonlight', '#d8d9ad', .72)
    for index, x in enumerate((-.95,-.53,-.10,.36,.80)):
        tube('Plant shoot %d' % index, [(x,-1.42,.15),(x+.04, -.75+index*.05,.10)], [.055,.025], stem, 3)
        for side in (-1,1):
            leaf('Plant leaf %d %d' % (index,side), (x,-1.00,.1), (x+side*.32,-.70,.12), .11, stem, .055)
    oval('Moon', (1.12,.87,-.20), (.62,.62,.18), moon, 40, 20)
    _label(0,(-.27,-.66,.34),'龶','plant shoots')
    _label(1,(1.12,.86,.04),'月','moon')
    return {'title':'Moonlit green shoots','design':'Fresh shoots and leaves grow across a moss island beneath a large pale moon.','anchors':{'anchor_part_0':'龶','anchor_part_1':'月'}}


def build_river():
    _ground('River')
    water = _mat('River water', '#62a7b4', .35)
    wood = _mat('Permission gate', '#9a7448', .88)
    for branch, x in enumerate((-.30,0,.31)):
        tube('River channel %d' % branch, [(x,-1.36,-1.05),(x*.55,-1.27,-.35),(x*.2,-1.18,.35),(x+.20,-1.13,1.05)], [.18,.16,.14,.11], water, 4)
    _box('Gate left post',(-.90,-.58,.45),(.16,1.55,.18),wood)
    _box('Gate right post',(.90,-.58,.45),(.16,1.55,.18),wood)
    _box('Gate lintel',(0,.10,.45),(2.08,.18,.22),wood)
    mouth = _mat('Speaking mouth','#a85646',.78)
    tube('Gate speaking mouth',[(-.27,-.47,.68),(0,-.57,.74),(.27,-.47,.68)],[.045,.060,.045],mouth,3)
    _label(0,(-.28,-1.05,.62),'氵','water')
    _label(1,(.68,-.05,.72),'可','permission')
    return {'title':'Water passes the gate','design':'Three blue channels merge and pass beneath a carved permission gate with a speaking mouth.','anchors':{'anchor_part_0':'氵','anchor_part_1':'可'}}


def build_permission():
    _ground('Permission','#66734b')
    metal = _mat('Nail gate','#8b7658',.72)
    mouth = _mat('Permission mouth','#b45e4d',.72)
    _box('Tall nail post',(0,-.30,.08),(.18,2.15,.18),metal)
    _box('Nail head',(0,.68,.08),(1.44,.20,.26),metal)
    for side in (-1,1):
        tube('Open mouth lip %d'%side,[(-.62,-.64,.52),(0,-.76+side*.05,.60),(.62,-.64,.52)],[.055,.075,.055],mouth,3)
    _label(0,(0,.59,.35),'丁','nail')
    _label(1,(.60,-.65,.76),'口','mouth')
    return {'title':'The gate says you may enter','design':'A monumental nail-shaped gate stands beside a sculpted speaking mouth.','anchors':{'anchor_part_0':'丁','anchor_part_1':'口'}}


def build_moon():
    _ground('Moon','#455e58')
    frame = _mat('Moon frame','#d2c79a',.68)
    light = _mat('Moon bands','#f2e6ac',.48)
    tube('Curved open moon frame',[(-.72,-.82,0),(-.95,-.10,0),(-.77,.72,0),(0,1.10,0),(.76,.72,0),(.94,-.12,0),(.70,-.82,0)],[.16]*7,frame,5)
    for index, y in enumerate((-.16,.34)):
        tube('Pale band %d'%index,[(-.56,y,.04),(.56,y,.04)],[.065,.065],light,3)
    _label(0,(-.76,.64,.26),'冂','open frame')
    _label(1,(.48,.32,.28),'二','two')
    return {'title':'Two bands inside the moon','design':'A thick curved moon frame contains exactly two luminous horizontal bands.','anchors':{'anchor_part_0':'冂','anchor_part_1':'二'}}


def build_liver():
    _ground('Liver','#665b43')
    body = _mat('Body model','#d6a577',.78)
    organ = _mat('Liver organ','#8f3f38',.70)
    dry = _mat('Dry texture','#a87955',.94)
    oval('Body torso',(0,-.15,0),(1.16,1.43,.38),body,36,20)
    oval('Liver',(0,-.18,.48),(1.02,.48,.24),organ,36,18)
    for index in range(8):
        angle=index*math.tau/8
        oval('Dry raisin wrinkle %d'%index,(math.cos(angle)*.36,-.16+math.sin(angle)*.16,.72),(.09,.035,.025),dry,16,8)
    _label(0,(-.78,-.20,.74),'⺼','moon')
    _label(1,(.70,-.30,.74),'干','dry')
    return {'title':'A dried moon becomes a liver','design':'A friendly torso model reveals a liver shaped like a wrinkled, dried moon.','anchors':{'anchor_part_0':'⺼','anchor_part_1':'干'}}


def build_hand():
    _ground('Hand')
    _hand('Open hand',(0,-.50,.20),1.05,1,True)
    _label(0,(.58,.22,.55),'手','hand')
    return {'title':'Trace the open hand','design':'A sculpted open hand shows four fingers, a crossing thumb, broad palm and long wrist.','anchors':{'anchor_part_0':'手'}}


def build_palm():
    _ground('Palm')
    _hand('Supporting hand',(-.82,-.68,.05),.72,1,True)
    _hand('Giant palm',(.42,-.03,.10),.98,-1,False)
    marble = _mat('Palm marble','#d6b45c',.52)
    oval('Balanced marble',(.40,.98,.17),(.24,.24,.24),marble,28,16)
    _label(0,(-.92,-.10,.46),'手','hand')
    _label(1,(.80,.22,.52),'掌','palm')
    return {'title':'A marble balanced on the palm','design':'One hand lifts a much larger open palm like a tray, balancing a polished marble.','anchors':{'anchor_part_0':'手','anchor_part_1':'掌'}}


def build_opponent():
    _ground('Opponent','#4d6848')
    board = _mat('Game board','#b5905e',.86)
    dark = _mat('Dark pieces','#38433d',.76)
    light = _mat('Light pieces','#e2d5b3',.82)
    _box('Game board',(0,-.92,.10),(1.72,.12,1.24),board,.06)
    for index in range(6):
        x=-.57+(index%3)*.57; z=-.22+(index//3)*.50
        oval('Game piece %d'%index,(x,-.76,z),(.12,.06,.12),dark if index%2 else light,20,10)
    _hand('Left opponent',(-1.25,-.20,.18),.62,1,True)
    _hand('Right opponent',(1.25,-.20,.18),.62,-1,True)
    _label(0,(-1.15,.27,.56),'对','facing')
    _label(1,(1.18,.27,.56),'手','hand')
    return {'title':'Hands face across the board','design':'Two sculpted hands face each other over a wooden strategy board and opposing pieces.','anchors':{'anchor_part_0':'对','anchor_part_1':'手'}}
