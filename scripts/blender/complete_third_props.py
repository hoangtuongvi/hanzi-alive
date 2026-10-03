"""Purpose-built solid props for the last completion batch.

The symbols below are openly mnemonic metaphors, not historical character
origins. Each is assembled from the shared Sculpt primitives, without text,
image planes, external assets or a catch-all unknown-cue renderer.
"""
import math

KINDS = {
    'third-check', 'third-no', 'third-grid', 'third-puzzle', 'third-broken',
    'third-tag', 'third-ruler', 'third-weight', 'third-trophy',
    'third-magnifier', 'third-hourglass', 'third-crown', 'third-halberd',
    'third-bamboo', 'third-beard', 'third-bow', 'third-joint',
    'third-empty', 'third-plus', 'third-minus', 'third-loop', 'third-target',
    'third-shield', 'third-arm', 'third-organs', 'third-spleen',
    'third-toilet', 'third-syringe', 'third-piano', 'third-lute',
    'third-theater', 'third-mask', 'third-tomato', 'third-duck',
    'third-oak', 'third-eraser', 'third-badge', 'third-pine',
    'third-village', 'third-levels', 'third-sad', 'third-surprise',
    'third-wind', 'third-oil', 'third-pump', 'third-bow-person',
    'third-spots', 'third-circuit', 'third-second', 'third-book-stack',
    'third-elephant', 'third-three-stripes', 'third-recliner',
    'third-crowd', 'third-crossroads', 'third-exchange',
}


def build(kind, s):
    if kind not in KINDS:
        raise ValueError('Unknown last-batch prop: ' + kind)
    if kind == 'third-check':
        s.line([(-.48,-.02,0),(-.12,-.36,0),(.50,.40,0)],.075,'green','approval check')
    elif kind == 'third-no':
        for sign in (-1,1):
            s.line([(-.40,sign*.40,0),(.40,-sign*.40,0)],.075,'red','negative cross')
    elif kind == 'third-grid':
        s.box((0,0,0),(1.14,1.06,.10),'cream','standard form')
        for x in (-.35,0,.35):s.line([(x,-.46,.07),(x,.46,.07)],.015,'blue','column')
        for y in (-.30,0,.30):s.line([(-.50,y,.07),(.50,y,.07)],.015,'blue','row')
    elif kind == 'third-puzzle':
        s.box((-.26,0,0),(.52,.70,.24),'blue','left fitting piece')
        s.box((.27,0,0),(.52,.70,.24),'green','right fitting piece')
        s.ball((-.03,.02,.16),(.14,.14,.06),'blue','interlocking knob')
        s.line([(0,-.35,.14),(0,-.14,.14),(.12,0,.14),(0,.14,.14),(0,.35,.14)],.019,'cream','joining seam')
    elif kind == 'third-broken':
        s.poly([(-.64,-.13),(-.11,-.13),(-.03,.01),(-.18,.16),(-.64,.16)],'wood',d=.22,name='broken left')
        s.poly([(.12,-.13),(.65,-.13),(.65,.16),(.03,.16),(.18,.01)],'woodlight',d=.22,name='broken right')
    elif kind == 'third-tag':
        s.poly([(-.43,-.48),(.42,-.48),(.42,.30),(0,.55),(-.43,.30)],'cream',d=.09,name='coded tag')
        s.ring((0,.32,.07),.075,'wood',.012)
        for i in range(5):s.box((-.27+i*.13,-.13,.07),(.055,.18+(i%2)*.17,.035),'dark','code stripe')
    elif kind == 'third-ruler':
        s.box((0,0,0),(1.35,.28,.13),'woodlight','ruler')
        for i in range(11):s.line([(-.6+i*.12,.13,.09),(-.6+i*.12,.015 if i%5 else -.09,.09)],.012,'dark','measure tick')
    elif kind == 'third-weight':
        s.box((0,-.12,0),(.70,.60,.55),'metal','heavy weight')
        s.ring((0,.25,0),.14,'dark',.045)
    elif kind == 'third-trophy':
        s.poly([(-.40,.54),(.40,.54),(.28,-.08),(0,-.30),(-.28,-.08)],'gold',d=.31,name='prize cup')
        for sign in (-1,1):s.line([(sign*.38,.42,0),(sign*.58,.36,0),(sign*.52,.03,0),(sign*.22,-.10,0)],.039,'gold','cup handle')
        s.line([(0,-.28,0),(0,-.48,0)],.08,'gold','prize stem')
        s.box((0,-.54,0),(.65,.13,.43),'wood','prize base')
    elif kind == 'third-magnifier':
        s.ring((-.12,.16,0),.36,'gold',.055)
        s.line([(.14,-.10,0),(.53,-.53,0)],.07,'wood','magnifier handle')
        s.line([(-.31,.26,.03),(-.10,.42,.03)],.018,'water','glass reflection')
    elif kind == 'third-hourglass':
        for y in (-.54,.54):s.box((0,y,0),(.85,.09,.50),'wood','hourglass end')
        for x in (-.35,.35):s.line([(x,-.49,0),(x,.49,0)],.025,'wood','hourglass support')
        s.poly([(-.28,.46),(.28,.46),(.045,0),(.28,-.46),(-.28,-.46),(-.045,0)],'water',d=.12,name='glass neck')
        s.poly([(-.19,-.42),(.19,-.42),(0,-.13)],'gold',z=.09,d=.06,name='gathered sand')
        s.line([(0,.14,.12),(0,-.12,.12)],.016,'gold','falling sand')
    elif kind == 'third-crown':
        s.poly([(-.55,-.25),(.55,-.25),(.57,.34),(.29,.12),(0,.55),(-.29,.12),(-.57,.34)],'gold',d=.27,name='royal crown')
        for x in (-.32,0,.32):s.ball((x,-.10,.15),(.065,.065,.035),'red','crown jewel')
    elif kind == 'third-halberd':
        s.line([(0,-.72,0),(0,.66,0)],.035,'wood','halberd shaft')
        s.poly([(-.04,.34),(.43,.56),(.38,.12),(-.04,.20)],'metal',d=.08,name='halberd side blade')
        s.poly([(-.08,.54),(0,.80),(.08,.54)],'metal',d=.09,name='spear tip')
    elif kind == 'third-bamboo':
        for x,y in ((-.29,0),(0,.09),(.29,-.05)):
            s.line([(x,-.60,0),(x,.58+y,0)],.06,'green','bamboo cane')
            for joint in (-.35,0,.35):s.line([(x-.07,joint,0),(x+.07,joint,0)],.015,'gold','bamboo node')
        s.poly([(.05,.15),(.45,.47),(.27,.13)],'leaf',d=.03,name='bamboo leaf')
    elif kind == 'third-beard':
        s.ball((0,.26,0),(.26,.25,.18),'skin','chin')
        for i in range(7):s.line([(-.23+i*.077,.17,.16),(-.12+i*.04,-.42,.17)],.028,'wood','beard strand')
    elif kind == 'third-bow':
        s.line([(-.25,-.63,0),(.15,-.33,0),(.27,0,0),(.15,.33,0),(-.25,.63,0)],.043,'wood','arched bow')
        s.line([(-.25,-.63,0),(-.25,.63,0)],.013,'cream','taut string')
    elif kind == 'third-joint':
        for sign in (-1,1):s.line([(sign*.65,sign*.31,0),(sign*.16,0,0)],.105,'cream','jointed limb')
        s.ball((0,0,0),(.19,.19,.19),'metal','joint hinge')
        s.ball((0,0,.18),(.055,.055,.02),'gold','hinge pin')
    elif kind == 'third-empty':
        for x in (-.43,.43):s.box((x,0,0),(.08,.90,.10),'metal','vacant outline')
        for y in (-.45,.45):s.box((0,y,0),(.92,.08,.10),'metal','vacant outline')
    elif kind in ('third-plus','third-minus'):
        s.box((0,0,0),(1,.12,.13),'green' if kind=='third-plus' else 'red','quantity sign')
        if kind=='third-plus':s.box((0,0,0),(.12,1,.13),'green','addition upright')
    elif kind == 'third-loop':
        s.line([(-.36,-.34,0),(-.56,.05,0),(-.22,.46,0),(.27,.45,0),(.56,.06,0),(.36,-.34,0)],.045,'blue','returning path')
        s.poly([(.48,-.27),(.18,-.49),(.16,-.12)],'blue',d=.10,name='return arrow')
    elif kind == 'third-target':
        for r,c in ((.52,'red'),(.34,'cream'),(.16,'red')):s.ring((0,0,0),r,c,.04)
        s.ball((0,0,0),(.06,.06,.04),'gold','center')
    elif kind == 'third-shield':
        s.poly([(-.44,.47),(.44,.47),(.38,-.14),(0,-.60),(-.38,-.14)],'blue',d=.22,name='protective shield')
        s.box((0,.05,.13),(.10,.59,.03),'gold','shield boss')
    elif kind == 'third-arm':
        s.line([(-.45,.37,0),(-.13,.34,0),(.05,-.10,0),(.45,-.20,0)],.13,'skin','bent arm')
        s.ball((.55,-.20,0),(.17,.12,.10),'skin','hand')
    elif kind in ('third-organs','third-spleen'):
        if kind=='third-spleen':
            s.ball((0,0,0),(.22,.43,.17),'red','spleen model')
            s.line([(-.12,-.08,.15),(.01,.06,.18),(.05,.29,.12)],.027,'pink','spleen hilum')
        else:
            s.ball((-.18,.25,0),(.27,.21,.13),'red','liver')
            s.ball((.20,.12,0),(.23,.28,.13),'pink','stomach')
            s.line([(-.30,-.15,0),(.28,-.15,0),(.24,-.33,0),(-.24,-.33,0),(-.20,-.50,0),(.23,-.50,0)],.055,'pink','intestines')
    elif kind == 'third-toilet':
        s.box((0,.15,-.27),(.58,.70,.20),'cream','toilet cistern')
        s.ball((0,-.18,.11),(.41,.23,.43),'white','toilet bowl')
        s.ball((0,-.50,.02),(.25,.24,.24),'cream','toilet pedestal')
        s.line([(-.29,-.02,.37),(-.34,.02,.04),(0,.06,-.06),(.34,.02,.04),(.29,-.02,.37)],.045,'metal','seat rim')
    elif kind == 'third-syringe':
        s.box((0,0,0),(.24,.58,.20),'white','syringe barrel')
        s.box((0,.02,.12),(.13,.36,.035),'water','fluid window')
        s.line([(0,.31,0),(0,.55,0)],.035,'metal','plunger')
        s.box((0,.55,0),(.34,.08,.16),'blue','plunger thumb rest')
        s.line([(0,-.30,0),(0,-.72,0)],.015,'metal','needle')
        for y in (-.14,.02,.17):s.line([(.02,y,.15),(.10,y,.15)],.008,'dark','volume tick')
    elif kind == 'third-piano':
        s.box((0,.12,-.05),(1.30,.65,.58),'dark','piano body')
        s.box((0,-.06,.28),(1.30,.15,.29),'cream','keyboard')
        for i in range(9):s.line([(-.56+i*.14,-.14,.44),(-.56+i*.14,.02,.44)],.008,'dark','white key separation')
        for i in (0,1,3,4,5,7):s.box((-.50+i*.14,.005,.43),(.07,.10,.075),'dark','black key')
        for x in (-.49,.49):s.box((x,-.48,-.03),(.10,.43,.10),'wood','piano leg')
    elif kind == 'third-lute':
        s.ball((0,-.25,0),(.36,.40,.17),'woodlight','lute sound box')
        s.box((0,.32,0),(.15,.68,.12),'wood','lute neck')
        s.ball((0,-.20,.17),(.095,.10,.017),'dark','sound hole')
        for x in (-.045,0,.045):s.line([(x,-.46,.18),(x,.65,.09)],.008,'cream','string')
    elif kind == 'third-theater':
        s.box((0,-.53,0),(1.35,.18,.60),'wood','theater stage')
        for x in (-.56,.56):s.box((x,.12,-.20),(.19,1.12,.15),'red','stage curtain')
        s.box((0,.67,-.20),(1.35,.16,.16),'red','curtain pelmet')
        s.ball((0,.22,0),(.18,.22,.06),'cream','performer mask')
        for x in (-.07,.07):s.ball((x,.25,.06),(.02,.03,.02),'dark','mask eye')
        s.line([(-.09,.11,.065),(0,.06,.07),(.09,.11,.065)],.015,'red','mask smile')
    elif kind == 'third-mask':
        s.ball((0,0,0),(.40,.49,.10),'cream','opera mask')
        for x in (-.17,.17):
            s.ball((x,.11,.10),(.13,.17,.035),'red','opera face paint')
            s.ball((x,.12,.14),(.035,.04,.02),'dark','mask eye')
        s.line([(-.18,-.23,.12),(0,-.31,.14),(.18,-.23,.12)],.035,'dark','painted mouth')
    elif kind == 'third-tomato':
        s.ball((0,0,0),(.46,.40,.36),'red','tomato')
        for i in range(5):
            a=i*math.tau/5
            s.line([(0,.38,0),(.20*math.cos(a),.35,.20*math.sin(a))],.025,'green','tomato calyx')
        s.line([(0,.38,0),(.03,.56,0)],.035,'green','tomato stem')
    elif kind == 'third-duck':
        s.ball((0,-.16,0),(.48,.29,.28),'woodlight','roasted duck body')
        s.ball((.42,.20,0),(.21,.22,.20),'woodlight','duck head')
        s.box((.64,.13,0),(.27,.075,.16),'gold','duck bill')
        s.ball((.50,.25,.17),(.025,.025,.02),'dark','duck eye')
        s.ball((-.09,-.12,.26),(.27,.15,.055),'wood','folded duck wing')
        for x in (-.20,.17):s.line([(x,-.35,0),(x+.08,-.57,0)],.038,'gold','duck leg')
    elif kind == 'third-oak':
        s.line([(0,-.62,0),(0,.34,0)],.09,'wood','oak trunk')
        for x in (-.30,0,.30):s.ball((x,.32+(.14 if x==0 else 0),0),(.32,.29,.23),'green','oak crown')
        for x in (-.27,.28):
            s.ball((x,.03,.20),(.08,.12,.065),'woodlight','acorn')
            s.ball((x,.12,.20),(.10,.035,.085),'wood','acorn cap')
    elif kind == 'third-eraser':
        s.box((0,0,0),(.93,.37,.35),'pink','rubber eraser')
        s.box((-.16,0,0),(.53,.39,.37),'blue','eraser sleeve')
        s.line([(.36,.12,.19),(.43,-.11,.19)],.014,'white','rubber highlight')
    elif kind == 'third-badge':
        s.box((0,0,0),(.73,.88,.08),'cream','identity badge')
        s.box((0,.50,0),(.15,.15,.10),'metal','badge clip')
        s.ball((-.12,.14,.07),(.11,.12,.025),'skin','badge portrait head')
        s.ball((-.12,-.07,.07),(.15,.12,.025),'blue','badge portrait torso')
        for y in (-.25,-.36):s.line([(-.25,y,.08),(.25,y,.08)],.012,'dark','identity detail')
    elif kind == 'third-pine':
        s.line([(0,-.68,0),(0,.57,0)],.07,'wood','pine trunk')
        for y,w in ((-.22,.52),(.06,.43),(.34,.31)):s.poly([(-w,y-.15),(0,y+.33),(w,y-.15)],'green',d=.18,name='pine needles')
    elif kind == 'third-village':
        for x,y,z in ((-.35,-.12,0),(.33,-.12,0),(0,.24,-.20)):
            s.box((x,y,z),(.39,.35,.32),'cream','village house')
            s.poly([(x-.25,y+.18),(x,y+.43),(x+.25,y+.18)],'red',z,d=.36,name='village roof')
            s.box((x,y-.02,z+.18),(.10,.16,.025),'wood','village door')
    elif kind == 'third-levels':
        for i in range(3):s.box((-.42+i*.42,-.38+i*.28,0),(.40,.16+i*.25,.40),'woodlight','ascending level')
    elif kind in ('third-sad','third-surprise'):
        s.ball((0,0,0),(.40,.46,.25),'skin','expressive face')
        s.eyes(.10,.24,.14)
        if kind=='third-sad':
            s.line([(-.16,-.23,.24),(0,-.14,.27),(.16,-.23,.24)],.025,'wood','downturned mouth')
            s.ball((.22,-.01,.22),(.033,.085,.025),'water','tear')
        else:s.ring((0,-.22,.24),.075,'wood',.025)
    elif kind == 'third-wind':
        for y in (-.25,0,.25):
            s.line([(-.65,y,0),(.24,y,0),(.44,y+.12,0),(.30,y+.25,0),(.17,y+.17,0)],.023,'water','wind stream')
    elif kind == 'third-oil':
        s.box((0,-.05,0),(.68,.67,.28),'red','oil can')
        s.line([(-.23,.32,0),(-.23,.49,0),(.14,.49,0),(.14,.32,0)],.045,'dark','can handle')
        s.line([(.27,.23,0),(.48,.46,0),(.62,.46,0)],.05,'metal','pouring spout')
        s.ball((0,-.08,.16),(.12,.17,.02),'dark','oil drop symbol')
    elif kind == 'third-pump':
        s.box((0,-.13,0),(.60,.90,.35),'red','fuel pump')
        s.box((0,.19,.20),(.43,.21,.03),'cream','pump meter')
        s.line([(.30,.24,0),(.55,.15,0),(.54,-.47,0),(.40,-.52,0),(.37,-.29,0)],.025,'dark','fuel hose')
        s.box((0,-.61,0),(.86,.10,.50),'metal','pump plinth')
    elif kind == 'third-bow-person':
        s.ball((.32,.30,0),(.22,.24,.20),'skin','bowed head')
        s.line([(-.08,.16,0),(.17,.02,0),(.28,.21,0)],.14,'blue','bowing torso')
        for x in (-.14,.05):s.line([(x,-.03,0),(x,-.57,0)],.075,'dark','bowing leg')
        for z in (-.12,.12):s.line([(.05,.10,z),(.44,-.18,z)],.05,'blue','lowered arm')
    elif kind == 'third-spots':
        for x,y in ((-.35,.20),(0,.35),(.35,.17),(-.18,-.17),(.18,-.28)):
            s.ball((x,y,0),(.12,.12,.09),'gold','distinct dot')
    elif kind == 'third-circuit':
        s.box((0,0,0),(1.06,.84,.06),'green','circuit panel')
        for x in (-.35,0,.35):
            s.line([(x,-.33,.05),(x,.11,.05),(x+.13,.26,.05)],.014,'gold','network trace')
            s.ball((x,-.33,.055),(.05,.05,.025),'gold','contact')
        s.box((0,.10,.075),(.24,.22,.055),'dark','network chip')
    elif kind == 'third-second':
        s.ring((0,0,0),.45,'wood',.045)
        s.line([(0,0,.06),(.35,.24,.06)],.022,'red','second hand')
        for i in range(12):
            a=i*math.tau/12
            s.ball((.38*math.cos(a),.38*math.sin(a),.015),(.013,.013,.014),'gold','second tick')
        s.ball((0,0,.08),(.045,.045,.02),'gold','pivot')
    elif kind == 'third-book-stack':
        for i,c in enumerate(('blue','red','green')):
            s.box((0,-.32+i*.24,0),(.88,.19,.57),c,'stacked book cover')
            s.box((.03,-.31+i*.24,.29),(.78,.13,.025),'cream','stacked book pages')
    elif kind == 'third-elephant':
        s.ball((-.10,-.10,0),(.54,.35,.29),'metal','elephant body')
        s.ball((.36,.19,0),(.29,.30,.25),'metal','elephant head')
        s.ball((.24,.20,.23),(.23,.27,.07),'water','large ear')
        s.line([(.59,.16,0),(.70,-.05,0),(.69,-.38,0),(.57,-.49,0)],.065,'metal','curved trunk')
        s.ball((.46,.27,.22),(.025,.025,.02),'dark','elephant eye')
        for x in (-.43,.17):
            for z in (-.19,.19):s.line([(x,-.28,z),(x,-.60,z)],.07,'metal','elephant leg')
        s.line([(-.56,.01,0),(-.70,-.19,0)],.025,'metal','tail')
    elif kind == 'third-three-stripes':
        for i in range(3):s.line([(-.40,.42-i*.29,0),(.40,.18-i*.29,0)],.035,'blue','one of three stripes')
    elif kind == 'third-recliner':
        s.ball((.48,.08,0),(.22,.25,.20),'skin','reclining head')
        s.ball((-.04,-.01,0),(.39,.20,.18),'blue','reclining torso')
        for z in (-.11,.11):
            s.line([(-.30,-.08,z),(-.59,-.17,z),(-.76,-.19,z)],.065,'dark','outstretched leg')
            s.line([(.11,.12,z),(-.23,.21,z)],.055,'blue','resting arm')
        s.ball((.54,.13,.17),(.025,.025,.02),'dark','reclining eye')
    elif kind == 'third-crowd':
        for x,y,z in ((-.48,0,0),(0,-.05,.15),(.48,0,0),(-.25,.18,-.25),(.25,.18,-.25)):
            s.ball((x,y+.30,z),(.12,.14,.12),'skin','gathered person head')
            s.ball((x,y-.03,z),(.15,.21,.13),'blue' if x<0 else 'red','gathered person torso')
            for dx in (-.065,.065):s.line([(x+dx,y-.19,z),(x+dx,y-.42,z)],.035,'dark','gathered person leg')
    elif kind == 'third-crossroads':
        s.box((0,-.15,0),(1.4,.08,.43),'earth','east-west crossing road')
        s.box((0,-.14,0),(.43,.08,1.4),'earth','north-south crossing road')
        for q in (-.52,.52):
            s.box((q,-.10,0),(.18,.014,.025),'cream','east-west lane mark')
            s.box((0,-.09,q),(.025,.014,.18),'cream','north-south lane mark')
    elif kind == 'third-exchange':
        s.line([(-.58,.20,0),(.35,.20,0)],.042,'blue','outgoing exchange')
        s.poly([(.27,.33),(.60,.20),(.27,.07)],'blue',d=.10,name='outgoing arrow')
        s.line([(.58,-.20,0),(-.35,-.20,0)],.042,'green','return exchange')
        s.poly([(-.27,-.33),(-.60,-.20),(-.27,-.07)],'green',d=.10,name='return arrow')
