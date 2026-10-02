"""Original low-poly objects for word-specific mnemonic dioramas.

All objects are real closed 3D geometry; no fonts, downloaded models or textures.
Coordinates follow the viewer (X right, Y up, Z toward the reader). Props are
centered near the origin and transformed as a group by the recipe compositor.
"""
import math
import bpy
from mathutils import Matrix
from rest_scene import material, oval, tube, v, finish
from device_scenes import box, polygon, lathe

COLORS = {
    'cream':'#eddfba', 'white':'#f5f0dc', 'dark':'#293e43',
    'wood':'#94653f', 'woodlight':'#bf9465', 'green':'#588e61',
    'leaf':'#8abb70', 'water':'#5cabb9', 'blue':'#547fbe',
    'red':'#cf6758', 'pink':'#db9391', 'gold':'#e7b857',
    'skin':'#d9a879', 'earth':'#74634c', 'metal':'#a8b6b8',
}


def palette():
    return {k:material('Explanation / '+k,c,.72) for k,c in COLORS.items()}


class Sculpt:
    def __init__(self, name, mats):
        self.name, self.m = name, mats

    def ball(self, p, s, c='cream', name='rounded form'):
        return oval(self.name+' / '+name,p,s,self.m[c],16,8)

    def box(self, p, s, c='wood', name='block'):
        return box(self.name+' / '+name,p,s,self.m[c],.035)

    def line(self, pts, r=.035, c='wood', name='curve'):
        obj=tube(self.name+' / '+name,pts,[r]*len(pts),self.m[c],1)
        obj.data.resolution_u=4
        return obj

    def poly(self, pts, c='gold', z=0, d=.12, name='silhouette'):
        return polygon(self.name+' / '+name,pts,z,d,self.m[c],.015)

    def ring(self, p=(0,0,0), r=.5, c='wood', thickness=.035):
        return self.line([(p[0]+r*math.cos(k*math.tau/24),p[1]+r*math.sin(k*math.tau/24),p[2]) for k in range(25)],thickness,c,'ring')

    def eyes(self, y=.25, z=.43, spread=.16):
        for x in (-spread,spread):
            self.ball((x,y,z),(.037,.046,.024),'dark','eye')

    def person(self, kind):
        cloth='blue' if kind in ('person','man','boy','walker') else 'red'
        seated=kind=='sitter'
        self.ball((0,.50,0),(.25,.29,.23),'skin','head')
        self.ball((0,.66,-.025),(.255,.16,.225),'dark','hair')
        self.eyes(.52,.224,.09)
        self.line([(-.07,.41,.219),(0,.38,.231),(.07,.41,.219)],.012,'wood','smile')
        self.ball((0,-.04,0),(.27,.40,.19),cloth,'clothed torso')
        if kind in ('woman','girl'):
            self.poly([(-.17,.10),(.17,.10),(.36,-.43),(-.36,-.43)],cloth,d=.30,name='tunic')
            self.ball((-.25,.43,-.05),(.13,.19,.13),'dark','hair bun')
        if kind=='elder':
            self.ball((0,.68,-.03),(.26,.15,.23),'metal','silver hair')
            self.line([(.40,-.30,.1),(.40,-.83,.1)],.032,'wood','walking stick')
        for sign in (-1,1):
            footx=sign*(.32 if kind=='walker' else .14)
            knee=(sign*.17,-.44,.33 if seated else 0)
            ankle=(footx,-.73,.37 if seated else sign*.12)
            self.line([(sign*.12,-.26,0),knee,ankle],.085,'dark','trouser leg')
            self.ball((ankle[0],-.78,ankle[2]+.065),(.13,.065,.19),'wood','shoe')
            end=(sign*.49,.10 if kind=='dancer' else -.32,.15)
            self.line([(sign*.22,.17,0),(sign*.39,-.08,.04),end],.067,cloth,'sleeve')
            self.ball(end,(.075,.09,.07),'skin','hand')

    def animal(self, kind):
        color={'pig':'pink','cow':'cream','sheep':'white','horse':'wood','cat':'gold','dog':'woodlight','panda':'white','bear':'wood','tiger':'gold'}[kind]
        self.ball((0,-.12,0),(.61,.34,.30),color,'body')
        self.ball((.48,.24,.02),(.29,.29,.26),color,'head')
        self.ball((.70,.16,.07),(.18,.14,.20),'pink' if kind=='pig' else color,'muzzle')
        for z in (-.19,.19):
            for x in (-.36,.32):
                self.line([(x,-.24,z),(x,-.62,z)],.075,'dark' if kind in ('cow','panda') else color,'leg')
        for x,z in ((.34,-.15),(.38,.18)):
            if kind in ('cat','tiger'):
                self.poly([(x-.10,.39),(x,.68),(x+.10,.39)],color,z,.1,'pointed ear')
            else:self.ball((x,.48,z),(.12,.14,.08),'dark' if kind=='panda' else color,'ear')
        self.ball((.57,.31,.249),(.036,.043,.025),'dark','eye')
        if kind=='cow':
            for x in (-.23,.18):self.ball((x,-.04,.275),(.13,.16,.03),'dark','spot')
            self.line([(.33,.44,0),(.29,.64,0)],.034,'gold','horn')
        if kind=='sheep':
            for i in range(9):self.ball((-.40+(i%3)*.28,-.12+(i//3)*.15,.23),(.20,.16,.13),'white','wool curl')
        if kind=='panda':self.ball((.54,.31,.245),(.088,.078,.029),'dark','eye patch')
        if kind in ('cat','dog','tiger'):
            self.line([(-.48,-.10,0),(-.78,.03,0),(-.83,.35,.03)],.05,color,'tail')
        if kind=='pig':
            self.ring((-.65,-.03,0),.09,'pink',.025)
            for z in (-.015,.13):self.ball((.86,.18,z),(.012,.022,.015),'wood','nostril')
        if kind=='horse':
            self.line([(.25,.35,-.08),(.12,.17,-.13),(.09,-.06,-.17)],.075,'dark','mane')
            self.line([(-.51,0,0),(-.72,-.18,0),(-.79,-.49,0)],.065,'dark','tail')
        if kind=='tiger':
            for x in (-.35,-.1,.15):self.line([(x,.13,.19),(x+.07,-.04,.31),(x,-.24,.26)],.027,'dark','stripe')


def build_prop(kind, name, mats):
    """Dispatch only intentionally designed props; an unknown cue is an error."""
    s=Sculpt(name,mats)
    if kind in ('person','woman','man','girl','boy','child','walker','sitter','dancer','elder'):
        s.person(kind)
    elif kind in ('pig','cow','sheep','horse','cat','dog','panda','bear','tiger'):
        s.animal(kind)
    elif kind in ('tree','sprout','grass','wheat','flower','leaf'):
        if kind=='tree':
            s.line([(0,-.75,0),(0,.24,0),(.15,.55,0)],.11,'wood','trunk')
            for x,y,z in [(-.36,.39,0),(.31,.48,0),(0,.69,-.10)]:
                s.line([(0,0,0),(x,y,z)],.045,'wood','branch')
                s.ball((x,y,z),(.37,.31,.30),'green','leaf crown')
            for sign in (-1,1):s.line([(0,-.55,0),(sign*.35,-.75,.16)],.06,'wood','root')
        elif kind=='grass':
            for i in range(9):
                x=(i-4)*.12
                s.poly([(x-.04,-.40),(x+.14,.12+(i%3)*.14),(x+.04,-.40)],'green',z=(i%2)*.10,d=.025,name='grass blade')
        elif kind=='leaf':
            s.poly([(0,-.55),(-.35,-.10),(-.22,.30),(0,.57),(.31,.20),(.27,-.14)],'green',d=.055,name='leaf')
            s.line([(0,-.55, .045),(0,.46,.045)],.016,'cream','vein')
            for y in (-.22,0,.2):
                for sign in (-1,1):s.line([(0,y,.047),(sign*.20,y+.15,.047)],.009,'leaf','side vein')
        else:
            s.line([(0,-.65,0),(0,.35,0)],.028,'green','stem')
            for sign in (-1,1):s.ball((sign*.16,-.10,0),(.20,.065,.10),'leaf','leaf')
            if kind=='flower':
                for i in range(6):
                    a=i*math.tau/6
                    s.ball((math.cos(a)*.23,.35+math.sin(a)*.23,0),(.15,.15,.10),'pink','petal')
                s.ball((0,.35,.09),(.15,.15,.07),'gold','flower center')
            if kind=='wheat':
                for i in range(5):
                    for sign in (-1,1):s.ball((sign*.08,.02+i*.12,0),(.10,.08,.07),'gold','grain')
    elif kind in ('sun','moon','cloud','rain','snow','water','ice','mountain','earth','field'):
        if kind=='sun':
            s.ball((0,0,0),(.44,.44,.18),'gold','sun')
            for i in range(12):
                a=i*math.tau/12
                s.line([(math.cos(a)*.52,math.sin(a)*.52,0),(math.cos(a)*.69,math.sin(a)*.69,0)],.033,'gold','ray')
        elif kind=='moon':
            pts=[(.58*math.cos(a),.58*math.sin(a)) for a in [math.pi/2+i*math.pi/18 for i in range(19)]]
            # Return along a narrower inner arc. Shared tips occur only once;
            # duplicate endpoints or a nearly tangent arc tear under beveling.
            pts += [(.22*math.cos(a),.58*math.sin(a)) for a in [-math.pi/2-i*math.pi/18 for i in range(1,18)]]
            s.poly(pts,'cream',d=.15,name='crescent')
        elif kind in ('cloud','rain','snow'):
            for x,y in ((-.35,.22),(0,.39),(.33,.23)):
                s.ball((x,y,0),(.32,.24,.19),'white','cloud')
            if kind=='rain':
                for i in range(6):s.line([((i%3-1)*.3,-.08-(i//3)*.3,0),((i%3-1)*.3-.05,-.25-(i//3)*.3,0)],.025,'water','raindrop')
            if kind=='snow':
                for x,y in ((-.32,-.24),(.31,-.20),(0,-.51)):
                    for a in (0,math.pi/3,math.pi*2/3):s.line([(x-.1*math.cos(a),y-.1*math.sin(a),0),(x+.1*math.cos(a),y+.1*math.sin(a),0)],.013,'white','snow crystal')
        elif kind=='ice':
            s.box((0,0,0),(.8,.7,.6),'water','ice cube')
            for x in (-.22,0,.22):s.line([(x-.10,-.2,.31),(x+.09,.20,.31)],.012,'white','ice reflection')
        elif kind=='mountain':
            for x,height,z in ((-.32,.7,.15),(.20,1.1,-.12)):
                s.poly([(x-.46,-.5),(x,height),(x+.46,-.5)],'earth',z,.45,'mountain')
                s.poly([(x-.11,height-.37),(x,height+.015),(x+.12,height-.37)],'white',z+.24,.035,'snow cap')
        elif kind=='water':
            s.ball((0,-.23,0),(.75,.09,.49),'water','pool')
            for i in range(3):s.line([(-.45,-.12,-.22+i*.22),(-.13,-.10,-.27+i*.22),(.35,-.12,-.22+i*.22)],.013,'white','ripple')
        else:
            s.box((0,-.30,0),(1.1,.22,.85),'earth','soil')
            if kind=='field':
                for x in (-.33,0,.33):s.line([(x,-.18,-.32),(x,-.18,.32)],.023,'green','crop row')
    elif kind in ('book','board','blackboard','paper','envelope','calendar'):
        if kind=='book':
            s.box((0,0,0),(.77,1,.18),'red','book cover')
            s.box((.025,0,.045),(.67,.88,.17),'cream','page block')
            s.box((0,0,.15),(.77,1,.025),'green','front cover')
            s.box((-.34,0,.18),(.045,.95,.02),'gold','spine')
            s.box((.05,.10,.172),(.35,.06,.025),'gold','cover ornament')
        elif kind=='envelope':
            s.box((0,0,0),(1,.62,.09),'cream','envelope')
            s.line([(-.46,.27,.055),(0,-.08,.07),(.46,.27,.055)],.015,'woodlight','fold')
            s.box((.32,.16,.06),(.17,.17,.015),'red','stamp')
        else:
            s.box((0,0,0),(1.12,.80,.09),'wood' if kind in ('board','blackboard') else 'cream','panel')
            if kind=='blackboard':s.box((0,.01,.06),(1.02,.67,.025),'dark','slate')
            if kind=='calendar':
                s.box((0,.34,.06),(1.1,.15,.035),'red','calendar binding')
                for i in range(12):s.box(((i%4-1.5)*.23,.12-(i//4)*.18,.06),(.12,.10,.03),'gold','day')
            if kind=='paper':
                for y in (-.20,0,.20):s.line([(-.37,y,.06),(.3,y,.06)],.013,'blue','written line')
    elif kind in ('table','chair','bed','sofa','shelf'):
        if kind=='table':
            s.box((0,.24,0),(1.25,.12,.8),'woodlight','tabletop')
            for x in (-.49,.49):
                for z in (-.28,.28):s.box((x,-.23,z),(.10,.85,.10),'wood','table leg')
        elif kind=='chair':
            s.box((0,-.05,0),(.8,.13,.65),'woodlight','seat')
            s.box((0,.40,-.29),(.8,.78,.10),'wood','back')
            for x in (-.29,.29):
                for z in (-.23,.23):s.box((x,-.40,z),(.09,.64,.09),'wood','chair leg')
        elif kind=='bed':
            s.box((0,-.35,0),(1.4,.30,1.0),'wood','bedframe')
            s.box((0,-.14,0),(1.34,.20,.95),'cream','mattress')
            s.box((.20,-.02,0),(.92,.09,.93),'blue','blanket')
            s.ball((-.48,0,0),(.22,.09,.34),'white','pillow')
            s.box((-.7,0,0),(.08,.8,1.05),'wood','headboard')
        elif kind=='sofa':
            s.box((0,-.25,0),(1.3,.35,.70),'green','cushion')
            s.box((0,.08,-.30),(1.3,.80,.22),'green','back')
            for x in (-.65,.65):s.box((x,-.06,0),(.19,.50,.8),'leaf','armrest')
        else:
            for y in (-.5,0,.5):s.box((0,y,0),(1.1,.08,.4),'woodlight','shelf')
            for x in (-.55,.55):s.box((x,0,0),(.08,1.1,.4),'wood','upright')
    elif kind in ('cup','milk','bottle','bowl','plate','pot','basket','bucket'):
        if kind in ('cup','bottle','milk','pot','bucket'):
            bottle=kind in ('bottle','milk')
            profile=[(-.5,.01),(-.5,.27),(.17,.29),(.34,.13),(.50,.13)] if bottle else [(-.40,.01),(-.40,.24),(.32,.35),(.34,.30),(-.31,.19),(-.31,.01)]
            lathe(name+' / vessel',(0,0,0),profile,mats['white' if kind=='milk' else 'water'],20)
            if bottle:s.box((0,.53,0),(.29,.08,.29),'blue','bottle cap')
            if kind=='milk':s.box((0,-.02,.29),(.34,.3,.02),'blue','milk label')
            if kind=='cup':s.line([(.28,.24,0),(.59,.23,0),(.59,-.18,0),(.26,-.22,0)],.065,'water','handle')
        elif kind in ('bowl','plate'):
            profile=[(-.30,.01),(-.30,.18),(-.22,.33),(.05,.52),(.08,.50),(-.17,.28),(-.22,.01)] if kind=='bowl' else [(-.07,.01),(-.07,.45),(.04,.63),(.08,.62),(.0,.40),(.0,.01)]
            lathe(name+' / dish',(0,0,0),profile,mats['cream'],24)
        else:
            lathe(name+' / basket',(0,0,0),[(-.4,.15),(-.4,.25),(.15,.48),(.20,.44),(-.3,.20)],mats['woodlight'],20)
            s.line([(-.43,.12,0),(-.3,.64,0),(.3,.64,0),(.43,.12,0)],.038,'wood','handle')
            for y in (-.22,-.05,.10):
                pts=[((.32+y*.4)*math.cos(a),y,(.32+y*.4)*math.sin(a)) for a in [i*math.tau/24 for i in range(25)]]
                s.line(pts,.017,'wood','weave')
    elif kind in ('apple','fruit','melon','grapes','banana','pepper','lemon','egg','bread','noodles','rice','salt','candy'):
        if kind in ('apple','fruit','melon','lemon','egg'):
            color={'apple':'red','fruit':'gold','melon':'green','lemon':'gold','egg':'cream'}[kind]
            s.ball((0,0,0),(.43,.54 if kind=='egg' else .40,.35),color,kind)
            if kind in ('apple','fruit'):
                s.line([(0,.35,0),(.03,.59,0)],.033,'wood','stem')
                s.ball((.14,.49,0),(.16,.045,.08),'leaf','leaf')
            if kind=='melon':
                for x in (-.27,0,.27):s.line([(x,-.28,.20),(x,.02,.35),(x,.30,.18)],.027,'leaf','melon stripe')
        elif kind=='grapes':
            for row in range(4):
                for i in range(4-row):s.ball(((i-(3-row)/2)*.22,.30-row*.20,0),(.15,.15,.14),'pink','grape')
            s.line([(0,.40,0),(.08,.67,0)],.03,'wood','vine')
        elif kind=='banana':
            for z in (-.12,.04,.20):
                s.line([(-.38,.26,z),(-.31,-.22,z),(.18,-.34,z),(.46,-.01,z) ],.10,'gold','banana')
                s.ball((-.38,.28,z),(.045,.075,.045),'wood','stem')
        elif kind=='pepper':
            s.line([(-.18,.38,0),(-.23,.10,0),(0,-.30,0),(.30,-.42,0)],.12,'red','chili')
            s.line([(-.18,.41,0),(-.10,.59,0)],.035,'green','stem')
        elif kind=='bread':
            s.ball((0,-.08,0),(.64,.34,.35),'woodlight','loaf')
            for x in (-.33,0,.33):s.line([(x-.06,.12,.25),(x,.24,.04),(x+.06,.14,-.22)],.035,'cream','bread score')
        elif kind=='noodles':
            build_prop('bowl',name,mats)
            for i in range(8):s.line([(-.3,.03,-.2+i*.05),(-.2,.13,-.1+i*.05),(.1,.10,-.2+i*.05),(.3,.06,-.1+i*.05)],.025,'gold','noodle')
        elif kind in ('rice','salt'):
            for i in range(20):
                x=((i*7)%11-5)*.08; z=((i*3)%7-3)*.08
                s.ball((x,-.20+(1-abs(x))*.07,z),(.05,.025,.025) if kind=='rice' else (.023,.026,.021),'white','grain')
        else:
            s.ball((0,0,0),(.28,.20,.15),'pink','sweet')
            for sign in (-1,1):s.poly([(sign*.22,0),(sign*.51,.19),(sign*.51,-.19)],'gold',d=.12,name='wrapper')
    elif kind in ('bird','chicken','fish','butterfly'):
        if kind in ('bird','chicken'):
            s.ball((0,-.05,0),(.39,.29,.24),'cream' if kind=='chicken' else 'blue','body')
            s.ball((.27,.28,0),(.21,.22,.19),'cream' if kind=='chicken' else 'blue','head')
            s.poly([(.42,.32),(.68,.23),(.42,.17)],'gold',d=.12,name='beak')
            s.ball((.31,.32,.18),(.034,.035,.022),'dark','eye')
            s.ball((-.10,0,.22),(.25,.16,.055),'woodlight' if kind=='chicken' else 'water','wing')
            for x in (-.16,.13):s.line([(x,-.26,0),(x,-.50,0),(x+.12,-.51,.1)],.027,'gold','foot')
            if kind=='chicken':
                for x in (.12,.26,.38):s.ball((x,.49,0),(.085,.12,.065),'red','comb')
            s.poly([(-.29,.1),(-.65,.28),(-.47,-.15)],'blue' if kind=='bird' else 'wood',d=.1,name='tail')
        elif kind=='fish':
            s.ball((.03,0,0),(.52,.30,.20),'water','fish body')
            s.poly([(-.38,0),(-.80,.34),(-.80,-.34)],'blue',d=.1,name='tail')
            s.ball((.33,.08,.18),(.05,.05,.025),'dark','eye')
            for x in (-.20,0,.20):s.line([(x,-.16,.16),(x-.07,0,.20),(x,.16,.16)],.015,'cream','scale')
        else:
            for sign in (-1,1):
                s.ball((sign*.30,.22,0),(.29,.37,.07),'gold','upper wing')
                s.ball((sign*.24,-.24,0),(.22,.25,.07),'red','lower wing')
                s.ball((sign*.34,.26,.07),(.10,.17,.018),'blue','wing spot')
                s.line([(0,.30,0),(sign*.12,.58,0)],.016,'dark','antenna')
            s.ball((0,0,.07),(.06,.38,.065),'dark','body')
    elif kind in ('house','door','window','frame','tower','room','gate'):
        if kind in ('house','room','tower'):
            s.box((0,-.05,0),(1.1,1.0,.6),'cream','walls')
            s.poly([(-.68,.45),(0,.93),(.68,.45)],'red',d=.83,name='roof')
            s.box((.15,-.23,.315),(.28,.62,.035),'wood','door')
            s.box((-.30,.12,.32),(.23,.24,.04),'water','window')
            if kind=='tower':s.box((0,-.85,0),(.8,.65,.6),'woodlight','tower base')
        else:
            for x in (-.47,.47):s.box((x,0,0),(.10,1.4,.18),'wood','post')
            for y in ((.69,) if kind=='gate' else (-.69,.69)):
                s.box((0,y,0),(1.04,.1,.18),'woodlight','lintel')
            if kind=='door':
                s.box((-.22,0,-.23),(.55,1.25,.09),'green','open door leaf').rotation_euler[2]=-.45
                s.ball((-.09,-.02,.005),(.045,.045,.035),'gold','door handle')
            if kind=='window':
                s.box((0,0,0),(.045,1.35,.15),'woodlight','mullion')
                s.box((0,0,0),(.96,.045,.15),'woodlight','crosspiece')
    elif kind in ('bar','pole','hook','coil','nail','arrow','footprints','road','bridge','roof','lid'):
        if kind=='bar':s.box((0,0,0),(1.3,.095,.12),'gold','one bar')
        elif kind=='pole':s.box((0,0,0),(.085,1.35,.1),'wood','upright pole')
        elif kind=='nail':
            s.line([(0,-.55,0),(0,.45,0)],.04,'metal','nail shaft')
            s.box((0,.45,0),(.27,.07,.20),'metal','nail head')
        elif kind=='hook':s.line([(0,.62,0),(0,-.37,0),(-.18,-.50,0),(-.32,-.31,0)],.055,'gold','hook')
        elif kind=='coil':
            s.line([((.04+i*.006)*math.cos(i*.3),(.04+i*.006)*math.sin(i*.3),0) for i in range(70)],.035,'green','coil')
        elif kind=='arrow':
            s.line([(-.6,0,0),(.42,0,0)],.048,'gold','direction')
            s.poly([(.23,.19),(.64,0),(.23,-.19)],'gold',d=.12,name='arrowhead')
        elif kind=='footprints':
            for i in range(4):s.ball((-.45+i*.3,-.12,(i%2-.5)*.24),(.10,.018,.17),'wood','footprint')
        elif kind=='road':
            s.box((0,-.22,0),(1.5,.08,.55),'earth','road')
            for x in (-.5,0,.5):s.box((x,-.17,0),(.23,.012,.045),'cream','road marking')
        elif kind=='bridge':
            for i in range(11):
                x=(i-5)*.14;y=.35*(1-(x/.85)**2)
                s.box((x,y,0),(.135,.09,.55),'woodlight','bridge plank')
            for z in (-.28,.28):s.line([(-.82,.28,z),(0,.65,z),(.82,.28,z)],.045,'wood','arched rail')
        elif kind=='roof':s.poly([(-.8,.1),(0,.70),(.8,.1),(.68,0),(0,.54),(-.68,0)],'red',d=.75,name='roof')
        else:s.box((0,0,0),(1.15,.11,.65),'woodlight','cover')
    elif kind in ('hand','eye','mouth','ear','nose','heart','foot','leg','hair','tongue','face'):
        if kind=='hand':
            s.ball((0,-.13,0),(.27,.32,.10),'skin','palm')
            for i in range(4):s.line([((i-1.5)*.14,0,0),((i-1.5)*.16,.46-abs(i-1.5)*.065,0)],.058,'skin','finger')
            s.line([(-.22,-.12,0),(-.40,.12,0)],.07,'skin','thumb')
        elif kind=='eye':
            s.ball((0,0,0),(.56,.32,.16),'white','eye white')
            s.ball((0,0,.15),(.20,.23,.045),'green','iris')
            s.ball((0,0,.192),(.09,.12,.025),'dark','pupil')
            s.ball((-.05,.08,.217),(.033,.04,.012),'white','glint')
        elif kind in ('mouth','tongue'):
            s.ball((0,0,0),(.44,.24,.12),'red','lips')
            s.ball((0,.01,.10),(.34,.14,.035),'dark','open mouth')
            s.ball((0,-.06,.14),(.18,.075,.035),'pink','tongue')
        elif kind=='heart':
            s.poly([(0,-.5),(-.5,.04),(-.47,.37),(-.23,.48),(0,.26),(.23,.48),(.47,.37),(.50,.04)],'red',d=.30,name='heart')
        elif kind=='ear':
            s.line([(-.1,-.45,0),(.23,-.20,0),(.31,.20,0),(.11,.45,0),(-.20,.29,0),(-.22,.01,0),(.01,-.10,0)],.085,'skin','ear rim')
            s.line([(.04,-.20,.02),(.15,.08,.02),(-.04,.15,.02)],.04,'pink','inner ear')
        elif kind=='nose':
            s.poly([(-.24,-.3),(0,.54),(.25,-.3)],'skin',d=.30,name='nose bridge')
            for x in (-.17,.17):s.ball((x,-.25,.18),(.13,.10,.1),'skin','nostril wing')
        elif kind in ('foot','leg'):
            s.line([(0,.56,0),(0,-.23,0)],.13,'skin','leg')
            s.ball((.15,-.33,.02),(.30,.12,.16),'skin','foot')
        else:
            s.ball((0,0,0),(.38,.48,.30),'skin','head')
            s.eyes(.12,.29,.13)
            s.line([(-.14,-.16,.28),(0,-.23,.30),(.14,-.16,.28)],.015,'wood','smile')
            for i in range(9):s.line([(-.34+i*.08,.32,-.10),(-.28+i*.07,.51,.03),(-.20+i*.07,.29,.29)],.045,'dark','hair strand')
    elif kind in ('flame','lamp','steam','speech','question','music','lightning'):
        if kind=='flame':
            s.poly([(-.35,-.4),(-.45,-.05),(-.14,.3),(0,.73),(.15,.16),(.32,.39),(.44,-.18),(.25,-.4)],'red',d=.20,name='flame')
            s.poly([(-.15,-.36),(-.18,-.08),(0,.32),(.20,-.15),(.1,-.36)],'gold',z=.13,d=.06,name='hot core')
        elif kind=='lamp':
            s.ball((0,-.52,0),(.40,.07,.25),'gold','lamp base')
            s.line([(0,-.48,0),(0,.25,0)],.047,'wood','lamp stem')
            lathe(name+' / shade',(0,0,0),[(.12,.48),(.55,.24),(.56,.23),(.15,.43)],mats['gold'],20)
        elif kind=='steam':
            for x in (-.25,0,.25):s.line([(x,-.4,0),(x+.1,-.1,0),(x-.05,.2,0),(x,.48,0)],.025,'cream','rising steam')
        elif kind in ('speech','question'):
            s.ball((0,.10,0),(.62,.39,.10),'white','speech bubble')
            s.poly([(-.3,-.10),(-.48,-.43),(-.03,-.20)],'white',d=.1,name='speech tail')
            if kind=='speech':
                for x in (-.25,0,.25):s.ball((x,.1,.10),(.035,.045,.025),'blue','spoken sound')
            else:
                s.line([(-.13,.23,.12),(-.10,.34,.12),(.14,.30,.12),(.12,.10,.12),(0,.02,.12)],.023,'blue','question curve')
                s.ball((0,-.13,.12),(.028,.028,.024),'blue','question dot')
        elif kind=='music':
            for x in (-.25,.23):
                s.line([(x,-.32,0),(x,.44,0)],.03,'dark','note stem')
                s.ball((x-.10,-.31,0),(.15,.10,.05),'dark','note')
            s.box((0,.43,0),(.54,.13,.1),'dark','note beam')
        else:s.poly([(-.07,.7),(-.42,-.05),(-.07,-.05),(-.24,-.65),(.45,.16),(.05,.16)],'gold',d=.10,name='electric bolt')
    elif kind in ('knife','axe','pencil','brush','chopsticks','broom','feather','silk','green-silk','coins'):
        if kind=='knife':
            s.box((-.40,0,0),(.43,.14,.13),'wood','knife handle')
            s.poly([(-.16,.08),(.62,.08),(.48,-.13),(-.16,-.13)],'metal',d=.06,name='blade')
        elif kind=='axe':
            s.line([(0,-.64,0),(0,.50,0)],.05,'wood','axe handle')
            s.poly([(-.08,.45),(.43,.59),(.43,.08),(-.08,.19)],'metal',d=.1,name='axe head')
        elif kind in ('pencil','brush'):
            s.line([(0,-.40,0),(0,.50,0)],.07,'gold' if kind=='pencil' else 'wood','shaft')
            s.poly([(-.067,-.38),(0,-.67),(.067,-.38)],'dark',d=.08,name='writing tip')
            s.box((0,.53,0),(.15,.14,.15),'pink' if kind=='pencil' else 'metal','cap')
        elif kind=='chopsticks':
            for sign in (-1,1):s.line([(sign*.06,-.62,0),(sign*.20,.62,0)],.023,'wood','chopstick')
        elif kind=='broom':
            s.line([(0,-.24,0),(0,.68,0)],.045,'wood','handle')
            for i in range(11):s.line([((i-5)*.01,-.22,0),((i-5)*.06,-.65,0)],.020,'gold','straw')
        elif kind=='feather':
            s.line([(0,-.6,0),(0,.6,0)],.02,'cream','quill')
            for y in (-.35,-.18,0,.18,.35):
                for sign in (-1,1):s.line([(0,y,0),(sign*(.31-abs(y)*.4),y+.12,0)],.038,'white','barb')
        elif kind in ('silk','green-silk'):
            for i in range(7):s.line([(-.5,-.3+i*.08,0),(-.15,-.4+i*.08,.10),(.25,.10+i*.08,0),(.55,-.15+i*.08,0)],.027,'green' if kind=='green-silk' else 'red','silk strand')
        else:
            for i in range(5):
                s.ball((-.30+i*.14,-.22+i*.06,0),(.28,.043,.28),'gold','coin')
                s.box((-.30+i*.14,-.17+i*.06,0),(.09,.012,.09),'wood','square coin hole')
    elif kind in ('hat','shirt','pants','skirt','shoe','sock','bag','suitcase','umbrella'):
        if kind=='hat':
            s.ball((0,0,0),(.56,.055,.40),'woodlight','hat brim')
            s.ball((0,.18,0),(.34,.24,.29),'gold','hat crown')
        elif kind in ('shirt','skirt','pants','sock'):
            outlines={
                'shirt':[(-.16,.5),(-.45,.30),(-.62,.02),(-.37,-.09),(-.27,.10),(-.27,-.5),(.27,-.5),(.27,.10),(.37,-.09),(.62,.02),(.45,.30),(.16,.5)],
                'pants':[(-.35,.5),(.35,.5),(.32,-.6),(.06,-.6),(0,.05),(-.06,-.6),(-.32,-.6)],
                'skirt':[(-.24,.45),(.24,.45),(.55,-.5),(-.55,-.5)],
                'sock':[(-.18,.5),(.18,.5),(.18,-.22),(.48,-.24),(.48,-.45),(-.18,-.45)],
            }
            s.poly(outlines[kind],'blue' if kind in ('pants','shirt') else 'red',d=.16,name=kind)
            if kind=='shirt':
                for y in (-.26,-.02,.22):s.ball((0,y,.10),(.025,.025,.018),'cream','button')
        elif kind=='shoe':
            s.ball((0,-.16,0),(.52,.20,.26),'wood','shoe upper')
            s.box((0,-.32,0),(1.05,.065,.53),'cream','sole')
            for x in (-.1,.05,.2):s.line([(x,.01,-.09),(x-.06,.03,.09)],.018,'cream','lace')
        elif kind in ('bag','suitcase'):
            s.box((0,-.10,0),(.85,.85,.32),'red' if kind=='bag' else 'green','bag body')
            s.line([(-.20,.33,0),(-.20,.62,0),(.20,.62,0),(.20,.33,0)],.047,'wood','handle')
            if kind=='suitcase':
                for x in (-.30,.30):s.ball((x,-.59,0),(.08,.08,.08),'dark','wheel')
        else:
            s.line([(0,.40,0),(0,-.55,0),(.15,-.64,0),(.23,-.49,0)],.035,'wood','umbrella handle')
            # Eight colored wedge meshes form a genuinely domed canopy.
            for i in range(8):
                a=i*math.tau/8;b=(i+1)*math.tau/8
                verts=[v((0,.66,0)),v((math.cos(a)*.66,.24,math.sin(a)*.66)),v((math.cos(b)*.66,.24,math.sin(b)*.66))]
                mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],[(0,1,2)]);mesh.update()
                obj=bpy.data.objects.new(name+' / canopy',mesh);bpy.context.collection.objects.link(obj);finish(obj,obj.name,mats['gold' if i%2 else 'red'])
                solid=obj.modifiers.new('Canopy thickness','SOLIDIFY');solid.thickness=.025
    elif kind in ('clock','mirror','globe','ball','net','racket','shuttle','flag','key','lock','scale'):
        if kind=='clock':
            s.ball((0,0,0),(.55,.55,.10),'wood','clock rim')
            s.ball((0,0,.09),(.48,.48,.035),'cream','clock face')
            for i in range(12):
                a=i*math.tau/12
                s.ball((.40*math.cos(a),.40*math.sin(a),.13),(.021,.021,.016),'wood','hour mark')
            s.line([(0,.32,.15),(0,0,.15),(.23,-.1,.15)],.022,'dark','clock hands')
        elif kind=='mirror':
            s.ball((0,0,0),(.44,.58,.10),'gold','mirror frame')
            s.ball((0,0,.09),(.36,.50,.03),'water','reflective surface')
            s.line([(-.20,-.25,.13),(.16,.29,.13)],.022,'white','shine')
        elif kind in ('globe','ball'):
            s.ball((0,0,0),(.53,.53,.53),'water' if kind=='globe' else 'gold',kind)
            if kind=='globe':
                for p,sz in [((-.2,.19,.45),(.19,.27,.09)),((.25,-.2,.43),(.16,.18,.09)),((.1,.40,.25),(.2,.07,.13))]:s.ball(p,sz,'green','land')
            else:
                s.ring((0,0,.05),.53,'wood',.017)
                s.line([(-.45,0,.28),(0,0,.55),(.45,0,.28)],.018,'wood','ball seam')
        elif kind=='net':
            for x in (-.60,.60):s.box((x,0,0),(.045,1.2,.045),'wood','net post')
            for i in range(7):
                x=-.6+i*.2;s.line([(x,-.28,0),(x,.5,0)],.009,'cream','net vertical')
            for y in (-.28,-.08,.12,.32,.5):s.line([(-.6,y,0),(.6,y,0)],.009,'cream','net horizontal')
        elif kind=='racket':
            s.ring((0,.20,0),.37,'red',.038)
            s.line([(0,-.16,0),(0,-.70,0)],.047,'wood','handle')
            for i in (-2,-1,0,1,2):
                q=i*.1;span=math.sqrt(.34**2-q*q)
                s.line([(q,.2-span,0),(q,.2+span,0)],.009,'cream','strings')
                s.line([(-span,.2+q,0),(span,.2+q,0)],.009,'cream','strings')
        elif kind=='shuttle':
            s.ball((0,-.27,0),(.17,.18,.17),'cream','cork')
            for i in range(10):
                a=i*math.tau/10
                s.line([(.12*math.cos(a),-.18,.12*math.sin(a)),(.34*math.cos(a),.40,.34*math.sin(a))],.025,'white','feather')
        elif kind=='flag':
            s.line([(-.3,-.65,0),(-.3,.65,0)],.035,'wood','flagpole')
            s.poly([(-.3,.61),(.51,.51),(.36,.12),(-.3,.22)],'red',d=.025,name='flag')
        elif kind=='key':
            s.ring((-.30,0,0),.22,'gold',.06)
            s.line([(-.08,0,0),(.58,0,0)],.05,'gold','key shaft')
            for x in (.30,.48):s.line([(x,0,0),(x,-.17,0)],.04,'gold','key tooth')
        elif kind=='lock':
            s.box((0,-.18,0),(.66,.60,.25),'gold','lock')
            s.line([(-.22,.07,0),(-.22,.45,0),(.22,.45,0),(.22,.07,0)],.065,'metal','shackle')
            s.ball((0,-.15,.14),(.05,.07,.02),'dark','keyhole')
        else:
            s.box((0,-.50,0),(.8,.12,.5),'wood','scale foot')
            s.line([(0,-.44,0),(0,.5,0)],.055,'wood','scale post')
            s.line([(-.64,.4,0),(.64,.4,0)],.04,'gold','beam')
            for x in (-.55,.55):
                s.line([(x,.4,0),(x,-.10,0)],.018,'gold','chain')
                s.ball((x,-.13,0),(.28,.045,.24),'gold','weighing pan')
    elif kind in ('boat','plane','car','train','bicycle','screen','phone','gear'):
        if kind=='boat':
            s.poly([(-.8,.05),(.8,.05),(.55,-.36),(-.48,-.36)],'wood',d=.55,name='hull')
            s.line([(0,0,0),(0,.83,0)],.033,'wood','mast')
            s.poly([(.04,.75),(.04,.12),(.53,.12)],'cream',d=.027,name='sail')
        elif kind=='plane':
            s.ball((0,0,0),(.83,.15,.18),'white','fuselage')
            s.box((0,-.02,0),(.24,.08,1.45),'blue','wings')
            s.poly([(-.62,.05),(-.65,.48),(-.35,.05)],'blue',d=.055,name='tail fin')
            for x in (-.15,.07,.29,.51):s.ball((x,.025,.165),(.045,.045,.022),'water','window')
        elif kind in ('car','train'):
            s.box((0,-.10,0),(1.30,.40,.55),'red' if kind=='car' else 'green','vehicle')
            s.box((-.12,.22,0),(.72,.36,.51),'water','cab')
            for x in (-.41,.41):
                for z in (-.29,.29):s.ball((x,-.36,z),(.17,.17,.07),'dark','wheel')
            if kind=='train':s.box((.4,.27,0),(.16,.40,.19),'dark','chimney')
        elif kind=='bicycle':
            for x in (-.47,.47):s.ring((x,-.28,0),.32,'dark',.035)
            s.line([(-.47,-.28,0),(-.15,.20,0),(.15,-.28,0),(-.47,-.28,0)],.033,'red','rear frame')
            s.line([(-.15,.20,0),(.34,.20,0),(.15,-.28,0)],.033,'red','front frame')
            s.line([(.47,-.28,0),(.32,.43,0),(.51,.46,0)],.033,'metal','handlebar')
            s.box((-.16,.28,0),(.29,.07,.14),'dark','saddle')
        elif kind in ('screen','phone'):
            s.box((0,0,0),(.55 if kind=='phone' else 1.18,.92,.13),'dark','device frame')
            s.box((0,.02,.078),(.45 if kind=='phone' else 1.02,.72,.02),'water','screen')
            s.ball((0,-.40,.08),(.035,.028,.014),'cream','button')
            if kind=='screen':s.box((0,-.62,0),(.55,.08,.35),'dark','stand')
        else:
            s.ring((0,0,0),.32,'metal',.11)
            for i in range(10):
                a=i*math.tau/10
                s.box((.44*math.cos(a),.44*math.sin(a),0),(.14,.14,.16),'metal','gear tooth')
    elif kind in ('cake','bun','dumpling','cookie','pill','medical','tooth','brush-teeth','towel','box','camera','map','ladder','wall','star','drum','shell','stamp'):
        if kind=='cake':
            lathe(name+' / cake',(0,0,0),[(-.35,.48),(.15,.48),(.18,.46)],mats['cream'],24)
            lathe(name+' / icing',(0,0,0),[(.14,.50),(.25,.50),(.25,.01)],mats['pink'],24)
            for x in (-.22,0,.22):
                s.line([(x,.25,0),(x,.59,0)],.025,'blue','candle')
                s.ball((x,.66,0),(.035,.075,.035),'gold','candle flame')
        elif kind=='bun':
            s.ball((0,-.1,0),(.48,.34,.40),'cream','steamed bun')
            for i in range(8):
                a=i*math.tau/8
                s.line([(.10*math.cos(a),.24,.1*math.sin(a)),(.34*math.cos(a),.11,.30*math.sin(a))],.013,'woodlight','bun pleat')
        elif kind=='dumpling':
            s.ball((0,-.1,0),(.5,.22,.24),'cream','dumpling')
            s.line([(-.44,-.02,0),(-.18,.20,0),(.18,.20,0),(.44,-.02,0)],.045,'gold','sealed edge')
            for x in (-.30,-.15,0,.15,.30):s.line([(x,.20-abs(x)*.3,-.08),(x,.20-abs(x)*.3,.08)],.023,'cream','pleat')
        elif kind=='cookie':
            s.ball((0,0,0),(.47,.065,.42),'woodlight','biscuit')
            for x,z in ((-.2,0),(0,.15),(.2,0),(0,-.15)):
                s.ball((x,.065,z),(.052,.018,.052),'wood','chocolate chip')
        elif kind=='pill':
            s.ball((0,0,0),(.18,.44,.17),'white','capsule')
            s.ball((0,.20,.003),(.183,.25,.173),'red','capsule cap')
        elif kind=='medical':
            s.box((0,0,0),(.90,.70,.25),'white','medical case')
            s.line([(-.20,.36,0),(-.20,.52,0),(.20,.52,0),(.20,.36,0)],.035,'wood','case handle')
            s.box((0,0,.14),(.15,.44,.03),'green','first aid vertical')
            s.box((0,0,.16),(.44,.15,.03),'green','first aid horizontal')
        elif kind=='tooth':
            s.ball((0,.20,0),(.33,.29,.22),'white','tooth crown')
            for sign in (-1,1):s.line([(sign*.16,.02,0),(sign*.19,-.46,0)],.095,'cream','tooth root')
        elif kind=='brush-teeth':
            s.line([(0,-.62,0),(0,.48,0)],.054,'blue','toothbrush handle')
            s.box((0,.36,.04),(.20,.33,.10),'blue','brush head')
            for i in range(12):
                s.line([((i%3-1)*.056,.25+(i//3)*.07,.10),((i%3-1)*.056,.25+(i//3)*.07,.23)],.015,'white','bristle')
        elif kind=='towel':
            s.box((0,0,0),(.65,1.0,.055),'cream','towel')
            for y in (-.35,.35):s.box((0,y,.035),(.64,.045,.015),'water','woven stripe')
            for x in (-.25,-.12,0,.12,.25):s.line([(x,-.48,0),(x,-.60,0)],.015,'cream','fringe')
        elif kind=='box':
            s.box((0,-.10,-.24),(1,.75,.05),'woodlight','box back')
            s.box((0,-.10,.24),(1,.75,.05),'woodlight','box front')
            for x in (-.5,.5):s.box((x,-.10,0),(.05,.75,.5),'wood','box side')
            s.box((0,-.46,0),(1,.05,.5),'wood','box bottom')
        elif kind=='camera':
            s.box((0,0,0),(1.0,.65,.32),'dark','camera body')
            s.box((-.23,.38,0),(.36,.12,.25),'metal','viewfinder')
            s.ball((.13,0,.24),(.27,.27,.14),'metal','lens barrel')
            s.ball((.13,0,.36),(.19,.19,.045),'water','lens glass')
            s.box((-.34,.14,.18),(.15,.11,.025),'cream','flash')
        elif kind=='map':
            s.box((0,0,0),(1.1,.85,.04),'cream','map sheet')
            s.line([(-.45,-.32,.035),(-.17,.04,.035),(.0,-.04,.035),(.38,.32,.035)],.018,'red','route')
            for x,y in ((-.32,.21),(.24,-.19)):
                s.ball((x,y,.04),(.15,.12,.022),'green','park on map')
            s.ball((.38,.32,.06),(.05,.05,.025),'red','destination')
        elif kind=='ladder':
            for x in (-.32,.32):s.line([(x,-.70,0),(x,.70,0)],.035,'wood','ladder rail')
            for y in (-.55,-.25,.05,.35,.65):s.line([(-.32,y,0),(.32,y,0)],.026,'woodlight','rung')
        elif kind=='wall':
            for row in range(4):
                for col in range(4):s.box(((col-1.5)*.32+(row%2)*.08,(row-1.5)*.20,0),(.30,.18,.25),'earth','brick')
        elif kind=='star':
            s.poly([(math.cos(math.pi/2+i*math.pi/5)*(.60 if i%2==0 else .27),math.sin(math.pi/2+i*math.pi/5)*(.60 if i%2==0 else .27)) for i in range(10)],'gold',d=.15,name='star')
        elif kind=='drum':
            lathe(name+' / drum',(0,0,0),[(-.4,.4),(.25,.4),(.25,.01)],mats['red'],24)
            s.ball((0,.26,0),(.40,.025,.40),'cream','drumhead')
            for z in (-.15,.15):s.line([(-.50,.55,z),(.16,.45,z)],.028,'woodlight','drumstick')
        elif kind=='shell':
            s.ball((0,0,0),(.42,.5,.12),'cream','shell')
            for i in range(7):
                a=.3+i*.42
                s.line([(0,-.40,.11),(.34*math.cos(a),.05+.33*math.sin(a),.11)],.017,'gold','shell rib')
        else:
            s.box((0,-.24,0),(.5,.16,.45),'red','stamp base')
            s.line([(0,-.15,0),(0,.34,0)],.085,'wood','stamp handle')
            s.ball((0,.34,0),(.16,.10,.13),'wood','stamp grip')
    elif kind in ('food-meat','spoon','horns','bean','fur','plum','lining','zero'):
        if kind=='food-meat':
            s.ball((0,0,0),(.43,.11,.29),'pink','cut of meat')
            s.ball((.12,.10,0),(.095,.018,.095),'cream','bone')
        elif kind=='spoon':
            s.line([(0,-.6,0),(0,.18,0)],.04,'metal','spoon handle')
            s.ball((0,.32,0),(.18,.27,.05),'metal','spoon bowl')
        elif kind=='horns':
            for sign in (-1,1):s.line([(sign*.15,-.15,0),(sign*.35,.06,0),(sign*.32,.46,0)],.045,'gold','horn')
        elif kind=='bean':
            s.ball((0,0,0),(.26,.13,.16),'green','bean')
            s.line([(-.08,-.07,.13),(0,.0,.16),(.08,.07,.13)],.012,'cream','bean seam')
        elif kind=='fur':
            s.box((0,0,0),(.60,.60,.09),'wood','fur swatch')
            for i in range(25):
                x=(i%5-2)*.12;y=(i//5-2)*.12
                s.line([(x,y,.07),(x+.05,y+.16,.11)],.021,'cream','fur strand')
        elif kind=='plum':
            s.ball((0,0,0),(.34,.39,.32),'pink','plum')
            s.line([(0,.33,0),(.03,.53,0)],.025,'wood','stem')
        elif kind=='zero':
            s.ring((0,0,0),.48,'gold',.065)
        else:
            s.poly([(-.27,.45),(.27,.45),(.27,-.50),(-.27,-.50)],'cream',d=.025,name='cloth lining')
            for x in (-.22,.22):s.line([(x,-.43,.025),(x,.38,.025)],.008,'woodlight','stitched seam')
    elif kind.startswith('count-'):
        count=int(kind.split('-')[1])
        cols=min(count,5)
        for i in range(count):
            s.ball(((i%cols-(cols-1)/2)*.19,(i//cols)*.22-.15,0),(.071,.071,.071),'gold','counting bead %d'%(i+1))
    else:
        raise ValueError('No designed object for '+kind)


def place(kind, name, position, scale, mats, rotation=0):
    before=set(bpy.context.scene.objects)
    build_prop(kind,name,mats)
    # A positive angle rotates counterclockwise in the viewer's X/Y plane.
    transform=Matrix.Translation(v(position)) @ Matrix.Rotation(-rotation,4,'Y') @ Matrix.Scale(scale,4)
    for obj in set(bpy.context.scene.objects)-before:
        obj.matrix_world=transform @ obj.matrix_world
    return position
