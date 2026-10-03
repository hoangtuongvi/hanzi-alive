"""Small original geometric cues for the first completion batch.

All symbols are explicitly mnemonic, not claims about character history.
The compositor supplies Sculpt so this module stays importable without Blender.
"""
import math


KINDS = {
    'first-not', 'first-check', 'first-badge', 'first-clamp',
    'first-halberd', 'first-spear', 'first-shield', 'first-snake',
    'first-knot', 'first-repeat', 'first-weight', 'first-beard',
    'first-nun', 'first-group', 'first-target', 'first-elephant',
    'first-bamboo', 'first-jewel', 'first-well', 'first-bell',
    'first-ruler', 'first-link', 'first-pin', 'first-silver',
    'first-tail', 'first-claw', 'first-ten-grid', 'first-times',
    'first-trophy', 'first-hourglass', 'first-smile', 'first-frown',
    'first-root', 'first-empty', 'first-bow', 'first-bodyframe',
    'first-drop', 'first-hide', 'first-thirty', 'first-fork',
    'first-shadow', 'first-couple', 'first-fierce', 'first-square',
    'first-clothroll', 'first-generations', 'first-chocolate',
}


def build(kind, s):
    if kind == 'first-not':
        s.ring(r=.55, c='red', thickness=.065)
        s.line([(-.40,-.40,.06),(.40,.40,.06)], .07, 'red', 'negation slash')
    elif kind == 'first-check':
        s.line([(-.48,-.03,0),(-.12,-.35,0),(.49,.39,0)], .085, 'green', 'confirmation tick')
    elif kind == 'first-badge':
        s.box((0,0,0),(.85,1.1,.10),'blue','identity badge')
        s.ball((0,.22,.09),(.14,.16,.07),'skin','portrait head')
        s.ball((0,-.08,.09),(.21,.20,.055),'cream','portrait body')
        s.line([(-.26,-.38,.07),(.26,-.38,.07)], .025,'white','identity stripe')
        s.ring((0,.62,0),.07,'gold',.025)
    elif kind == 'first-clamp':
        s.line([(-.34,.50,0),(-.59,.50,0),(-.59,-.49,0),(.35,-.49,0)],.07,'metal','clamp frame')
        s.box((-.28,.43,0),(.30,.16,.26),'metal','upper jaw')
        s.line([(.22,-.60,0),(.22,.19,0)],.047,'gold','tightening screw')
        s.box((.22,.17,0),(.43,.15,.27),'metal','lower jaw')
        s.line([(-.03,-.60,0),(.47,-.60,0)],.035,'wood','turning handle')
    elif kind in ('first-halberd','first-spear'):
        s.line([(0,-.76,0),(0,.53,0)],.043,'wood','weapon shaft')
        s.poly([(-.12,.37),(0,.78),(.12,.37)],'metal',d=.10,name='point')
        if kind=='first-halberd':
            s.poly([(0,.43),(.39,.53),(.31,.13),(0,.19)],'metal',d=.10,name='halberd blade')
    elif kind == 'first-shield':
        s.poly([(-.53,.46),(0,.64),(.53,.46),(.43,-.31),(0,-.67),(-.43,-.31)],'blue',d=.22,name='shield')
        s.poly([(-.35,.32),(0,.44),(.35,.32),(.28,-.19),(0,-.43),(-.28,-.19)],'gold',z=.13,d=.035,name='shield boss')
    elif kind == 'first-snake':
        s.line([(-.69,-.45,0),(-.35,-.20,0),(.10,-.44,0),(.52,-.22,0),(.34,.19,0),(-.12,.28,0),(-.30,.51,0)],.095,'green','coiling snake')
        s.ball((-.25,.55,0),(.20,.13,.14),'leaf','snake head')
        s.ball((-.27,.60,.12),(.023,.024,.017),'dark','snake eye')
        s.line([(-.07,.54,0),(.10,.54,0)],.015,'red','tongue')
    elif kind == 'first-knot':
        for x in (-.23,.23):s.ring((x,0,0),.31,'red',.055)
        s.line([(-.47,-.20,0),(-.59,-.63,0)],.052,'red','loose end')
        s.line([(.47,-.20,.03),(.59,-.63,.03)],.052,'red','loose end')
        s.ball((0,0,.04),(.13,.13,.08),'gold','crossing knot')
    elif kind == 'first-repeat':
        for sign in (-1,1):
            pts=[(sign*.51*math.cos(a),sign*.51*math.sin(a),0) for a in [i*math.pi/15 for i in range(13)]]
            s.line(pts,.047,'blue','repeat arc')
            x,y,_=pts[-1]
            s.poly([(x-.12,y+.09),(x+.17,y+.10),(x+.05,y-.17)],'blue',d=.08,name='repeat arrow')
    elif kind == 'first-weight':
        s.poly([(-.55,-.53),(.55,-.53),(.33,.30),(-.33,.30)],'dark',d=.40,name='heavy weight')
        s.ring((0,.46,0),.16,'metal',.065)
        s.box((0,-.15,.22),(.35,.20,.025),'metal','weight label')
    elif kind == 'first-beard':
        s.poly([(-.48,.45),(0,.30),(.48,.45),(.32,-.20),(0,-.66),(-.32,-.20)],'metal',d=.16,name='hanging beard')
        for x in (-.25,0,.25):s.line([(x,.24,.10),(x*.62,-.36,.10)],.018,'white','beard strand')
    elif kind == 'first-nun':
        s.person('woman')
        s.poly([(-.35,.76),(.32,.76),(.39,.18),(.20,.22),(.20,.61),(-.20,.61),(-.20,.22),(-.39,.18)],'dark',z=.08,d=.12,name='mnemonic nun veil')
    elif kind == 'first-group':
        for x,y in ((-.47,0),(0,.12),(.47,0)):
            s.ball((x,y+.31,0),(.14,.16,.13),'skin','group member head')
            s.ball((x,y-.14,0),(.17,.28,.12),'blue','group member torso')
            for dx in (-.065,.065):s.line([(x+dx,y-.28,0),(x+dx,y-.61,0)],.04,'dark','group member leg')
    elif kind == 'first-target':
        s.box((0,0,-.10),(1.20,1.20,.12),'cream','target backing')
        for r,c in ((.48,'red'),(.32,'white'),(.16,'red')):s.ring((0,0,.02),r,c,.045)
        s.ball((0,0,.03),(.065,.065,.025),'red','target center')
    elif kind == 'first-elephant':
        s.ball((-.16,-.06,0),(.47,.32,.27),'metal','elephant body')
        s.ball((.33,.23,0),(.27,.29,.23),'metal','elephant head')
        s.ball((.14,.23,.23),(.24,.30,.06),'woodlight','large ear')
        s.line([(.56,.19,0),(.70,-.05,0),(.71,-.35,0),(.54,-.43,0)],.073,'metal','trunk')
        for x in (-.42,.12):
            for z in (-.16,.16):s.line([(x,-.22,z),(x,-.61,z)],.075,'metal','leg')
        s.ball((.40,.30,.22),(.03,.033,.018),'dark','eye')
    elif kind == 'first-bamboo':
        for x in (-.31,.22):
            s.line([(x,-.70,0),(x,.68,0)],.07,'green','bamboo stalk')
            for y in (-.35,0,.35):s.box((x,y,0),(.19,.065,.17),'leaf','bamboo joint')
        for sign in (-1,1):s.poly([(.22,.35),(.22+sign*.43,.62),(.22+sign*.30,.26)],'green',d=.025,name='bamboo leaf')
    elif kind == 'first-jewel':
        s.poly([(-.51,.19),(-.27,.48),(.27,.48),(.51,.19),(0,-.57)],'water',d=.34,name='radiant jewel')
        for x in (-.65,.65):s.line([(x,.34,0),(x*1.14,.44,0)],.021,'gold','sparkle')
        s.line([(0,.61,0),(0,.77,0)],.023,'gold','top sparkle')
    elif kind == 'first-well':
        s.box((0,-.35,0),(1.20,.36,.72),'earth','well curb')
        s.ball((0,-.15,.02),(.41,.025,.25),'water','well water')
        for x in (-.50,.50):s.line([(x,-.23,0),(x,.65,0)],.05,'wood','well post')
        s.line([(-.53,.64,0),(.53,.64,0)],.055,'wood','well crossbar')
        s.line([(0,.62,0),(0,-.02,0)],.024,'cream','bucket rope')
        s.box((0,.04,0),(.29,.25,.26),'woodlight','well bucket')
    elif kind == 'first-bell':
        s.poly([(-.46,-.33),(-.29,.23),(-.14,.47),(.14,.47),(.29,.23),(.46,-.33)],'gold',d=.42,name='bell shell')
        s.ball((0,-.40,0),(.10,.14,.10),'metal','clapper')
        s.ring((0,.59,0),.10,'wood',.04)
        for sign in (-1,1):s.line([(sign*.60,.32,0),(sign*.71,.22,0),(sign*.60,.12,0)],.025,'blue','sound wave')
    elif kind == 'first-ruler':
        s.box((0,0,0),(1.50,.27,.12),'woodlight','measuring ruler')
        for i in range(11):
            x=-.65+i*.13
            s.line([(x,-.12,.07),(x,.10 if i%5==0 else .015,.07)],.012,'dark','division')
    elif kind == 'first-link':
        for x,z in ((-.26,0),(.26,.065)):s.ring((x,0,z),.35,'metal',.055)
    elif kind == 'first-pin':
        s.line([(0,-.64,0),(0,.17,0)],.035,'metal','fixing pin')
        s.ball((0,.32,0),(.22,.20,.14),'red','pin head')
    elif kind == 'first-silver':
        s.poly([(-.55,-.35),(.55,-.35),(.41,.23),(-.41,.23)],'metal',d=.53,name='silver ingot')
        s.line([(-.22,.06,.28),(.19,.13,.28)],.026,'white','silver gleam')
    elif kind == 'first-tail':
        s.line([(-.58,-.48,0),(-.28,-.18,0),(.24,-.25,0),(.49,.03,0),(.24,.40,0),(-.12,.25,0),(-.08,.04,0),(.15,.08,0)],.067,'green','curling tail')
    elif kind == 'first-claw':
        s.ball((0,.22,0),(.27,.22,.12),'skin','reaching palm')
        for i in range(4):
            x=(i-1.5)*.16
            s.line([(x,.16,0),(x,-.15,0),(x+.045,-.38,.13)],.048,'skin','curved reaching finger')
    elif kind == 'first-ten-grid':
        s.box((0,0,-.05),(1.36,1.36,.075),'woodlight','hundred-cell counting board')
        for i in range(100):
            x=(i%10-4.5)*.122;y=(i//10-4.5)*.122
            s.box((x,y,.015),(.082,.082,.035),'gold','one of one hundred cells')
    elif kind == 'first-times':
        for sign in (-1,1):s.line([(-.38,sign*-.38,0),(.38,sign*.38,0)],.060,'blue','multiplication cross')
    elif kind == 'first-trophy':
        s.poly([(-.31,.53),(.31,.53),(.25,.03),(0,-.16),(-.25,.03)],'gold',d=.28,name='trophy cup')
        for x in (-.37,.37):s.ring((x,.24,0),.17,'gold',.035)
        s.line([(0,-.14,0),(0,-.54,0)],.065,'gold','trophy stem')
        s.box((0,-.58,0),(.65,.14,.36),'wood','trophy base')
    elif kind == 'first-hourglass':
        for y in (-.64,.64):s.box((0,y,0),(.94,.09,.43),'wood','hourglass cap')
        for x in (-.39,.39):s.line([(x,-.58,0),(x,.58,0)],.035,'wood','hourglass pillar')
        s.poly([(-.32,.52),(.32,.52),(0,0)],'water',d=.18,name='upper glass chamber')
        s.poly([(0,0),(.32,-.52),(-.32,-.52)],'water',d=.18,name='lower glass chamber')
        s.poly([(-.26,-.49),(.26,-.49),(0,-.09)],'gold',z=.11,d=.025,name='fallen sand')
        s.line([(0,.16,.11),(0,-.11,.11)],.014,'gold','falling sand')
    elif kind in ('first-smile','first-frown'):
        s.ball((0,0,0),(.58,.58,.20),'gold','expression face')
        s.eyes(.15,.20,.18)
        y=-.18 if kind=='first-smile' else -.35
        ym=-.36 if kind=='first-smile' else -.14
        s.line([(-.28,y,.22),(0,ym,.22),(.28,y,.22)],.032,'dark','expression mouth')
    elif kind == 'first-root':
        s.line([(0,.62,0),(0,-.03,0)],.095,'wood','root stem')
        for sign in (-1,1):
            s.line([(0,-.03,0),(sign*.22,-.29,0),(sign*.58,-.52,0)],.060,'wood','branching root')
            s.line([(sign*.22,-.29,0),(sign*.20,-.65,.08)],.043,'wood','fine root')
    elif kind == 'first-empty':
        s.box((0,-.40,0),(1.13,.10,.52),'cream','empty tray bottom')
        for x in (-.52,.52):s.box((x,-.20,0),(.09,.40,.52),'cream','empty tray side')
        s.box((0,-.20,-.23),(1.13,.40,.09),'cream','empty tray back')
    elif kind == 'first-bow':
        s.line([(-.17,-.69,0),(.16,-.43,0),(.27,0,0),(.16,.43,0),(-.17,.69,0)],.047,'wood','arched bow')
        s.line([(-.17,-.69,0),(-.17,.69,0)],.018,'cream','bowstring')
    elif kind == 'first-bodyframe':
        s.ring((0,.53,0),.16,'metal',.035)
        s.line([(0,.35,0),(0,-.23,0)],.036,'metal','body spine')
        s.line([(-.39,.19,0),(.39,.19,0)],.036,'metal','shoulder frame')
        for sign in (-1,1):
            s.line([(sign*.39,.19,0),(sign*.49,-.14,0)],.035,'metal','arm frame')
            s.line([(0,-.23,0),(sign*.18,-.38,0),(sign*.23,-.70,0)],.035,'metal','leg frame')
        for y in (.10,-.05):s.line([(-.17,y,0),(.17,y,0)],.031,'metal','body rib')
    elif kind == 'first-drop':
        s.poly([(0,.65),(-.33,.03),(-.28,-.33),(0,-.49),(.28,-.33),(.33,.03)],'water',d=.22,name='water drop')
        s.line([(-.14,-.15,.13),(-.18,.01,.13)],.020,'white','drop gleam')
    elif kind == 'first-hide':
        s.poly([(-.20,.58),(.20,.58),(.31,.31),(.64,.33),(.56,.03),(.30,-.02),(.37,-.58),(.13,-.47),(-.13,-.47),(-.37,-.58),(-.30,-.02),(-.56,.03),(-.64,.33),(-.31,.31)],'skin',d=.055,name='mnemonic skin hide')
        s.line([(0,.40,.036),(0,-.31,.036)],.020,'woodlight','hide fold')
    elif kind == 'first-thirty':
        s.box((0,0,0),(1.32,.095,.10),'gold','cross bar')
        for x in (-.43,0,.43):s.box((x,0,0),(.085,1.30,.10),'gold','one of three crossing bars')
    elif kind == 'first-fork':
        s.line([(-.68,0,0),(-.12,0,0),(.42,.39,0)],.045,'gold','upper choice branch')
        s.line([(-.12,0,0),(.42,-.39,0)],.045,'gold','lower choice branch')
        for sign in (-1,1):s.poly([(.23,sign*.44),(.61,sign*.46),(.42,sign*.21)],'gold',d=.10,name='branch arrowhead')
    elif kind == 'first-shadow':
        s.ball((0,.40,0),(.17,.18,.035),'dark','head shadow')
        s.poly([(-.20,.20),(.20,.20),(.22,-.26),(.11,-.26),(.17,-.66),(.035,-.66),(0,-.29),(-.035,-.66),(-.17,-.66),(-.11,-.26),(-.22,-.26)],'dark',d=.045,name='body shadow')
        for sign in (-1,1):s.line([(sign*.18,.08,0),(sign*.43,-.18,0)],.045,'dark','arm shadow')
    elif kind in ('first-couple','first-generations'):
        people=[(-.33,0,.85,'blue'),(.33,0,.85,'red')] if kind=='first-couple' else [(-.45,.08,.90,'blue'),(0,-.15,.62,'red'),(.45,.10,.92,'blue')]
        for x,y,size,color in people:
            s.ball((x,y+.37*size,0),(.14*size,.16*size,.13*size),'skin','family head')
            s.ball((x,y-.08*size,0),(.17*size,.28*size,.12*size),color,'family torso')
            for dx in (-.065,.065):s.line([(x+dx*size,y-.25*size,0),(x+dx*size,y-.61*size,0)],.04*size,'dark','family leg')
            if kind=='first-generations' and x>.2:s.ball((x,y+.47*size,-.035),(.14*size,.065*size,.12*size),'metal','elder silver hair')
    elif kind == 'first-fierce':
        s.ball((0,0,0),(.58,.58,.20),'gold','fierce face')
        s.eyes(.15,.20,.18)
        for sign in (-1,1):s.line([(sign*.07,.25,.22),(sign*.32,.38,.22)],.036,'dark','angry eyebrow')
        s.ball((0,-.24,.20),(.28,.12,.028),'dark','fierce mouth')
        for x in (-.16,0,.16):s.poly([(x-.045,-.19),(x+.045,-.19),(x,-.28)],'white',z=.24,d=.025,name='pointed tooth')
    elif kind == 'first-square':
        s.line([(-.55,-.55,0),(-.55,.55,0),(.55,.55,0),(.55,-.55,0),(-.55,-.55,0)],.058,'wood','square frame')
    elif kind == 'first-clothroll':
        s.box((0,-.09,0),(1.16,.58,.035),'cream','unrolled cloth')
        s.line([(-.58,.27,0),(.58,.27,0)],.115,'cream','cloth roll')
        s.ring((.58,.27,.12),.08,'woodlight',.012)
    elif kind == 'first-chocolate':
        s.box((0,0,0),(1.18,.79,.17),'wood','chocolate bar')
        for x in (-.40,0,.40):
            for y in (-.20,.20):
                s.box((x,y,.10),(.33,.32,.10),'wood','raised chocolate square')
        s.poly([(-.61,-.43),(.61,-.43),(.61,-.10),(.18,-.24),(-.15,-.10),(-.61,-.20)],'metal',z=.17,d=.025,name='opened chocolate foil')
    else:
        raise ValueError('No first-batch prop: '+kind)
