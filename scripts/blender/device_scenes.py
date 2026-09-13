"""Original Blender dioramas for 手机, 电脑, 分手 and 高手.

All points use the viewer's x/right, y/up, z/front coordinates. Each builder
leaves two ordered empty label anchors and returns scene-design metadata.
"""
import math

import bpy
from mathutils import Vector

from rest_scene import anchor, finish, material, oval, tube, v


def palette(scene):
    return {key: material(scene+' / '+key, color, roughness) for key, color, roughness in [
        ('skin', '#d2a174', .72), ('skin_shadow', '#b77a54', .77), ('nail', '#e4bc95', .67),
        ('sleeve', '#bf7352', .86), ('cuff', '#dda278', .83),
        ('dark', '#273b39', .62), ('edge', '#526b64', .58), ('cream', '#dddcc0', .71),
        ('screen', '#578680', .37), ('screen_light', '#91b8a1', .44),
        ('gold', '#dda84d', .50), ('gold_light', '#f2d789', .50),
        ('wood', '#80694c', .88), ('wood_light', '#aa9270', .85),
        ('brain', '#bc929f', .78), ('brain_light', '#d9b8bb', .76),
        ('ribbon', '#bb6950', .72), ('ribbon_light', '#de9370', .68),
        ('steel', '#aebdb6', .35), ('green', '#466a47', .80),
    ]}


def box(name, pos, size, mat, bevel=.05):
    bpy.ops.mesh.primitive_cube_add(size=1, location=v(pos))
    obj = finish(bpy.context.object, name, mat)
    obj.dimensions=(size[0], size[2], size[1])
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        mod=obj.modifiers.new('Soft crafted edges', 'BEVEL')
        mod.width=min(bevel,min(size)*.40);mod.segments=3
        obj.modifiers.new('Weighted surface normals', 'WEIGHTED_NORMAL')
    return obj


def polygon(name, outline, front, thickness, mat, bevel=.02):
    """Extrude a front-facing silhouette without relying on text or textures."""
    verts=[v((x,y,z)) for z in (front-thickness/2,front+thickness/2) for x,y in outline]
    n=len(outline)
    faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]
    faces += [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
    obj=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(obj);finish(obj,name,mat)
    if bevel:
        mod=obj.modifiers.new('Rounded silhouette edge','BEVEL');mod.width=bevel;mod.segments=3
        obj.modifiers.new('Weighted silhouette normals','WEIGHTED_NORMAL')
    return obj


def lathe(name, pos, profile, mat, segments=32):
    verts=[]
    for y,radius in profile:
        for k in range(segments):
            angle=k/segments*math.tau
            verts.append(v((pos[0]+math.cos(angle)*radius,pos[1]+y,pos[2]+math.sin(angle)*radius)))
    faces=[]
    for j in range(len(profile)-1):
        for k in range(segments):
            a=j*segments+k;b=j*segments+(k+1)%segments
            faces.append((a,b,b+segments,a+segments))
    faces.extend([tuple(reversed(range(segments))),tuple((len(profile)-1)*segments+k for k in range(segments))])
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
    obj=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(obj)
    return finish(obj,name,mat)


def hand(name, center, mats, rotation=0, scale=1, curl=.10, thumb=True):
    def p(point):
        x,y,z=point
        return (center[0]+scale*(x*math.cos(rotation)-y*math.sin(rotation)),
                center[1]+scale*(x*math.sin(rotation)+y*math.cos(rotation)),center[2]+scale*z)
    def o(label,point,size,key):
        obj=oval(name+' '+label,p(point),tuple(n*scale for n in size),mats[key])
        obj.rotation_euler[1]=-rotation
        return obj
    def t(label,points,radii,key):
        return tube(name+' '+label,[p(pt) for pt in points],[r*scale for r in radii],mats[key],2)
    o('palm',(0,0,0),(.36,.48,.16),'skin')
    t('wrist',[(0,-.32,-.015),(.025,-.64,-.055)],[.235,.20],'skin')
    t('linen sleeve',[(.025,-.65,-.055),(.06,-1.14,-.10)],[.245,.275],'sleeve')
    t('turned cuff',[(.025,-.60,-.052),(.026,-.72,-.06)],[.25,.256],'cuff')
    for i in range(4):
        x=(i-1.5)*.174
        height=[.86,1.04,.98,.79][i]
        t('finger %d'%i,[(x,.26,0),(x*1.05,height*.72,.015),(x*.96,height,.04+curl*.5),(x*.91,height-.04,.06+curl)], [.087,.078,.061,.040],'skin')
        o('fingertip %d'%i,(x*.91,height-.04,.06+curl),(.062,.072,.062),'skin')
        o('nail %d'%i,(x*.96,height-.016,-.010+curl*.5),(.044,.071,.009),'nail')
        t('knuckle crease %d'%i,[(x-.046,.51,.078),(x,.50,.09),(x+.046,.51,.078)],[.005,.006,.004],'skin_shadow')
    if thumb:
        t('thumb',[(-.26,-.07,.045),(-.51,.10,.05),(-.57,.34,.11),(-.52,.40,.14)],[.12,.108,.085,.055],'skin')
    t('palm crease',[(-.18,-.05,.159),(0,-.11,.171),(.21,-.02,.136)],[.004,.007,.003],'skin_shadow')
    return p


def island(mats, radius=2.10):
    oval('Rounded presentation island',(0,-1.96,0),(radius,.13,1.14),mats['dark'],40,12)


def set_anchors(points, glyphs, images):
    for index,(point,glyph,image) in enumerate(zip(points,glyphs,images)):
        obj=anchor('anchor_part_'+str(index),point)
        obj['glyph']=glyph;obj['label']=image


def build_phone():
    mats=palette('Phone');island(mats)
    # A warm hand supports a recognisable machine, with fingers wrapping around
    # its left edge while the display remains readable from the opening view.
    hand('Holding hand',(-.65,-.63,.09),mats,rotation=-.18,scale=1.04,curl=.27,thumb=False)
    box('Phone aluminium rounded body',(.37,.38,.20),(1.37,2.46,.23),mats['edge'],.12)
    box('Phone front bezel',(.37,.38,.336),(1.26,2.34,.052),mats['dark'],.10)
    box('Luminous inset display',(.37,.39,.37),(1.10,1.95,.025),mats['screen'],.07)
    box('Earpiece',(.37,1.455,.375),(.29,.035,.020),mats['cream'],.012)
    oval('Front camera lens',(.66,1.455,.375),(.032,.032,.012),mats['dark'])
    box('Home gesture line',(.37,-.71,.384),(.33,.025,.012),mats['cream'],.01)
    for row in range(2):
        for col in range(3):
            box('Raised app icon %d %d'%(row,col),(.05+col*.31,.19-row*.34,.400),(.19,.19,.016),mats['screen_light' if (row+col)%2 else 'cream'],.045)
    # A three-dimensional handset symbol makes the machine's function clear.
    tube('Call handset',[(.04,.94,.408),(.08,.76,.418),(.25,.63,.418),(.47,.61,.418),(.63,.69,.408)],[.067,.052,.048,.052,.067],mats['gold_light'],2)
    box('Volume rocker',(-.342,.76,.21),(.035,.34,.09),mats['cream'],.016)
    box('Power key',(1.075,.79,.21),(.035,.31,.09),mats['cream'],.016)
    # The thumb crosses only the lower corner instead of obscuring the device.
    tube('Thumb wrapped around phone',[(-.88,-.68,.27),(-.45,-.64,.47),(-.10,-.44,.48)],[.15,.12,.085],mats['skin'],3)
    for i in range(3):
        tube('Ringing arc %d'%i,[(1.23+i*.15,.74,.25),(1.34+i*.18,.96,.23),(1.23+i*.15,1.17,.21)],[.018,.026,.014],mats['gold'],2)
    set_anchors([(-1.16,-.61,.44),(.90,.55,.53)],['手','机'],['hand','machine'])
    return {'title':'A machine in your hand','design':'A sculpted hand wraps around a rounded mobile phone with raised call and app details.','anchors':{'anchor_part_0':'手','anchor_part_1':'机'}}


def _command_robot(name, center, mats, waving=False):
    """A small physical robot with articulated arms and a friendly inset face."""
    x,y,z=center
    def p(a):return (x+a[0],y+a[1],z+a[2])
    shell=mats['cream'] if waving else mats['screen_light']
    accent=mats['gold'] if waving else mats['ribbon']
    box(name+' rounded torso',p((0,.58,0)),(.49,.55,.38),shell,.11)
    box(name+' chest panel',p((0,.59,.205)),(.30,.27,.036),mats['edge'],.045)
    oval(name+' command receiver',p((0,.65,.234)),(.047,.047,.015),accent,20,12)
    for index in range(3):
        box(name+' indicator '+str(index),p((-.068+index*.068,.51,.232)),(.036,.026,.014),mats['gold_light'],.008)
    tube(name+' neck', [p((0,.82,0)),p((0,.93,0))],[.092,.077],mats['edge'],2)
    box(name+' soft square head',p((0,1.13,.006)),(.66,.47,.45),shell,.13)
    box(name+' dark face inset',p((0,1.13,.247)),(.53,.31,.032),mats['dark'],.076)
    for sign in (-1,1):
        oval(name+' bright eye '+str(sign),p((sign*.132,1.165,.273)),(.037,.055,.013),mats['gold_light'],20,12)
        oval(name+' cheek '+str(sign),p((sign*.183,1.068,.272)),(.034,.015,.008),accent,16,8)
        oval(name+' round ear '+str(sign),p((sign*.350,1.13,.008)),(.043,.106,.107),accent,20,12)
    tube(name+' smiling mouth',[p((-.069,1.061,.272)),p((0,1.030,.282)),p((.069,1.061,.272))],
         [.008,.010,.008],mats['cream'],1)
    tube(name+' antenna',[p((0,1.366,0)),p((0,1.57,0))],[.021,.016],mats['edge'],2)
    oval(name+' antenna light',p((0,1.592,0)),(.053,.053,.053),accent,20,12)
    for sign in (-1,1):
        tube(name+' lower leg '+str(sign),[p((sign*.14,.34,0)),p((sign*.14,.155,.04))],[.071,.055],mats['edge'],2)
        box(name+' rounded boot '+str(sign),p((sign*.145,.079,.086)),(.225,.155,.35),accent,.057)
        oval(name+' shoulder joint '+str(sign),p((sign*.278,.74,0)),(.077,.079,.075),mats['edge'],20,12)
        # The first robot raises its outside hand; the other grips a block.
        if waving and sign==-1:
            elbow=(-.47,.97,.014);wrist=(-.50,1.205,.026)
        else:
            elbow=(sign*.39,.52,.10);wrist=(sign*(.34 if waving else .20),.54,.30)
        tube(name+' upper arm '+str(sign),[p((sign*.28,.74,0)),p(elbow)],[.059,.048],shell,2)
        oval(name+' elbow '+str(sign),p(elbow),(.066,.063,.062),accent,20,12)
        tube(name+' forearm '+str(sign),[p(elbow),p(wrist)],[.054,.042],shell,2)
        oval(name+' palm '+str(sign),p(wrist),(.063,.072,.041),mats['edge'],20,12)
        if waving and sign==-1:
            for finger in range(3):
                fx=-.55+finger*.045
                tube(name+' waving finger '+str(finger),[p((fx,1.24,.027)),p((fx-.006,1.33+(finger==1)*.032,.027))],[.014,.010],mats['edge'],1)
    if not waving:
        box(name+' carried parcel',p((0,.51,.39)),(.30,.27,.26),mats['wood_light'],.033)
        box(name+' parcel ribbon upright',p((0,.51,.526)),(.040,.276,.014),mats['ribbon'],.006)
        box(name+' parcel ribbon across',p((0,.51,.529)),(.306,.041,.014),mats['ribbon'],.006)


def build_computer():
    mats=palette('Computer')
    box('Desk top',(0,-1.63,0),(3.92,.17,1.72),mats['wood'],.09)
    for x in (-1.55,1.55):
        for z in (-.55,.55):
            box('Desk leg',(x,-1.84,z),(.15,.34,.15),mats['wood_light'],.035)
    box('Monitor stand',(0,-1.19,-.19),(.21,.65,.26),mats['edge'],.05)
    box('Monitor foot',(0,-1.51,.03),(1.16,.08,.71),mats['dark'],.035)
    box('Monitor case',(0,-.11,-.14),(3.13,2.02,.23),mats['edge'],.12)
    box('Monitor bezel',(0,-.10,.004),(3.00,1.89,.067),mats['dark'],.085)
    box('Monitor screen',(0,-.04,.047),(2.76,1.64,.019),mats['screen'],.05)
    oval('Webcam',(0,.785,.073),(.034,.023,.010),mats['cream'])
    oval('Power light',(1.27,-.94,.076),(.023,.012,.010),mats['gold_light'])
    box('Keyboard frame',(-.21,-1.482,.59),(2.21,.085,.53),mats['cream'],.045)
    for row in range(3):
        for col in range(11):
            box('Keyboard key %d %d'%(row,col),(-1.15+col*.188,-1.423,.425+row*.136),(.154,.039,.103),mats['edge'],.009)
    box('Keyboard spacebar',(-.16,-1.421,.775),(.77,.040,.061),mats['edge'],.01)
    oval('Mouse',(1.36,-1.46,.61),(.21,.10,.30),mats['cream'])
    tube('Mouse seam',[(1.36,-1.36,.58),(1.36,-1.37,.41)],[.006,.006],mats['edge'],1)
    # A dimensional brain projects from the screen, with paired hemispheres and
    # sculpted, curved folds rather than a flat brain icon or text.
    for sign in (-1,1):
        oval('Brain hemisphere '+str(sign),(.47+sign*.29,.07,.40),(.42,.43,.25),mats['brain'],32,20)
        for k in range(7):
            angle=-math.pi/2+k*math.pi/6
            x=.47+sign*(.29+math.cos(angle)*.25)
            y=.07+math.sin(angle)*.30
            oval('Cortical lobe %d %d'%(sign,k),(x,y,.49),(.15,.13,.17),mats['brain'],20,12)
        for row in range(4):
            y=-.21+row*.16
            x=.47+sign*.29
            bend=.025 if row%2 else -.025
            tube('Brain fold %d %d'%(sign,row),[(x+sign*.17,y,.57),(x+sign*.21,y+.08,.60),(x+sign*.06,y+.105,.67),(x-sign*.02,y+bend,.69),(x-sign*.12,y+.05,.65)], [.045,.047,.045,.043,.030],mats['brain_light'],2)
    tube('Central brain fissure',[(.47,-.30,.56),(.44,-.10,.66),(.48,.12,.67),(.46,.42,.54)],[.010,.014,.015,.008],mats['brain'],2)
    tube('Brain stem',[(.49,-.26,.30),(.45,-.51,.30)],[.12,.085],mats['brain'])
    polygon('Electricity lightning bolt',[(-.66,.71),(-1.27,-.03),(-.92,-.03),(-1.12,-.71),(-.42,.13),(-.77,.13)],.39,.13,mats['gold'],.026)
    for i in range(3):
        tube('Electric connection %d'%i,[(-.50,.29-i*.22,.29),(-.24,.29-i*.22,.38),(-.15,.21-i*.18,.45)],[.018,.025,.014],mats['gold_light'],2)
    # Keep the brain and electricity central while showing two smaller machines
    # responding to it: one waves, and the other carries a carefully wrapped box.
    oval('Computer workshop floor',(0,-2.09,.12),(2.97,.10,1.29),mats['dark'],48,12)
    _command_robot('Waving helper robot',(-2.23,-2.0,.21),mats,waving=True)
    _command_robot('Parcel helper robot',(2.23,-2.0,.27),mats,waving=False)
    for sign in (-1,1):
        points=[(sign*1.47,-.72,-.14),(sign*1.72,-.78,-.08),
                (sign*1.93,-.80,.02),(sign*2.10,-.74,.13)]
        tube('Robot command cable '+str(sign),points,[.024,.026,.026,.020],mats['gold'],2)
        oval('Computer output socket '+str(sign),(sign*1.505,-.715,-.14),(.056,.060,.054),mats['edge'],20,12)
        for index in range(3):
            oval('Traveling command pulse %d %d'%(sign,index),
                 (sign*(1.66+index*.13),-.76-index*.009,-.055+index*.045),
                 (.035,.035,.035),mats['gold_light'],16,8)
    set_anchors([(-1.16,.49,.53),(1.00,.36,.65)],['电','脑'],['electricity','brain'])
    return {'title':'A brain guides its helpers','story':'A brain powered by electricity is a computer. It thinks and gives other robots their commands.','design':'A crafted desktop computer with a sculpted two-hemisphere brain and a golden electricity bolt powering it sends commands along gold cables to two small, friendly robots. One waves an articulated hand and the other carries a wrapped parcel.','anchors':{'anchor_part_0':'电','anchor_part_1':'脑'}}


def ribbon(name, points, mat, width=.13):
    verts=[]
    for point in points:
        verts.extend([v((point[0],point[1]-width,point[2])),v((point[0],point[1]+width,point[2]))])
    faces=[(i*2,i*2+1,i*2+3,i*2+2) for i in range(len(points)-1)]
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
    obj=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(obj);finish(obj,name,mat)
    sub=obj.modifiers.new('Ribbon bend','SUBSURF');sub.levels=2
    solid=obj.modifiers.new('Ribbon thickness','SOLIDIFY');solid.thickness=.027
    return obj


def build_parting():
    mats=palette('Parting');island(mats,2.23)
    hand('Left hand',(-1.30,-.68,.02),mats,rotation=-.49,scale=.87,curl=.05)
    hand('Right hand',(1.30,-.68,.02),mats,rotation=.49,scale=.87,curl=.05)
    ribbon('Left severed ribbon',[(-1.43,.06,.32),(-1.16,.14,.30),(-.87,.19,.36),(-.62,.18,.30),(-.40,.02,.37),(-.23,-.12,.40)],mats['ribbon'])
    ribbon('Right severed ribbon',[(.23,-.12,.40),(.40,.02,.37),(.62,.18,.30),(.87,.19,.36),(1.16,.14,.30),(1.43,.06,.32)],mats['ribbon'])
    # Small frayed threads make the open gap explicit.
    for sign in (-1,1):
        for k in range(4):
            y=-.19+k*.054
            tube('Frayed ribbon %d %d'%(sign,k),[(sign*.30,y,.405),(sign*.21,y-.02,.411),(sign*.17,y-.065,.406)],[.011,.009,.003],mats['ribbon_light'],1)
    # A crafted knife is lifted directly above the divided ribbon, blade down.
    polygon('Broad dividing blade',[(-.30,.40),(.05,.14),(.30,1.12),(-.07,1.23)],.36,.075,mats['steel'],.014)
    polygon('Polished cutting edge',[(-.30,.40),(.05,.14),(.095,.31),(-.18,.50)],.409,.016,mats['cream'],.005)
    tube('Knife handle',[(.11,1.16,.35),(.28,1.65,.35)],[.15,.14],mats['wood'],3)
    tube('Knife guard',[(-.11,1.12,.35),(.35,1.26,.35)],[.048,.048],mats['gold'],2)
    for y in (1.35,1.53):
        oval('Handle brass rivet',(.11+(y-1.16)*.347,y,.491),(.027,.027,.013),mats['gold'])
    set_anchors([(0,.83,.55),(-1.52,-.54,.40)],['分','手'],['divide','hand'])
    return {'title':'Two hands part ways','design':'Two sculpted hands separate beneath a knife; a ribbon hangs in two frayed, visibly disconnected lengths.','anchors':{'anchor_part_0':'分','anchor_part_1':'手'}}


def chess_piece(name, point, mats, gold=False, king=False, scale=1):
    mat=mats['gold' if gold else 'green']
    profile=[(0,.19),(.07,.19),(.12,.15),(.17,.145),(.22,.095),(.45,.065),(.51,.12),(.56,.12)]
    lathe(name+' turned body',point,[(y*scale,r*scale) for y,r in profile],mat)
    oval(name+' head',(point[0],point[1]+.63*scale,point[2]),(.14*scale,.14*scale,.14*scale),mat)
    if king:
        box(name+' crown upright',(point[0],point[1]+.84*scale,point[2]),(.064*scale,.26*scale,.065*scale),mat,.017*scale)
        box(name+' crown cross',(point[0],point[1]+.88*scale,point[2]),(.23*scale,.065*scale,.065*scale),mat,.017*scale)


def build_expert():
    mats=palette('Expert')
    box('Chessboard wooden rim',(0,-1.64,.02),(3.90,.21,2.63),mats['wood'],.10)
    for x in range(8):
        for z in range(8):
            box('Chess square %d %d'%(x,z),((x-3.5)*.45,-1.519,(z-3.5)*.298+.02),(.445,.023,.293),mats['cream' if (x+z)%2 else 'dark'],.008)
    for i,(x,z) in enumerate([(-1.36,-.72),(-.47,-.43),(1.36,-.43),(-.93,.76),(.90,.77)]):
        chess_piece('Board piece %d'%i,(x,-1.502,z),mats,scale=.66,king=i==2)
    # A high hand pinches the king, carrying it above the board to its final move.
    tube('Raised linen forearm',[(1.69,1.41,-.08),(1.21,1.00,.02)],[.31,.26],mats['sleeve'],4)
    tube('Folded cuff',[(1.23,1.02,.02),(1.10,.90,.065)],[.28,.27],mats['cuff'],3)
    oval('Raised hand palm',(.85,.74,.13),(.40,.29,.18),mats['skin'],28,16)
    tube('Pinching index finger',[(.65,.87,.12),(.30,.78,.13),(.13,.50,.18),(.15,.33,.23)],[.095,.083,.068,.047],mats['skin'],3)
    tube('Pinching thumb',[(.67,.54,.27),(.50,.33,.40),(.29,.28,.39)],[.12,.095,.066],mats['skin'],3)
    for i in range(3):
        tube('Curled raised finger %d'%i,[(.83+i*.12,.62,.10-i*.06),(.64+i*.10,.40,.07-i*.05),(.63+i*.12,.29,.20-i*.04),(.81+i*.10,.37,.26-i*.03)],[.079,.073,.065,.039],mats['skin'],2)
    tube('Palm fold',[(.66,.69,.291),(.84,.64,.316),(1.02,.71,.258)],[.004,.007,.003],mats['skin_shadow'],1)
    chess_piece('Winning golden king',(.16,-.37,.28),mats,gold=True,king=True,scale=.88)
    # A gold destination inset and tiny curved glints link the elevated move to
    # the board without arrows, labels or substitute text cards.
    lathe('Winning square inset',(.16,-1.489,.30),[(0,.20),(.007,.20),(.007,.175),(.015,.175)],mats['gold_light'],32)
    for i in range(3):
        angle=2.2+i*.39
        a=(-.14+math.cos(angle)*.63,.27+math.sin(angle)*.68,.26)
        b=(-.14+math.cos(angle)*.77,.27+math.sin(angle)*.80,.26)
        tube('Winning glint %d'%i,[a,b],[.014,.024],mats['gold_light'],2)
    set_anchors([(-.43,.59,.48),(1.08,.69,.41)],['高','手'],['high','hand'])
    return {'title':'The winning hand','design':'A raised, pinching hand carries a golden king above a crafted chessboard to make the winning move.','anchors':{'anchor_part_0':'高','anchor_part_1':'手'}}
