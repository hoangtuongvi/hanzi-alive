"""Purpose-built miniature objects for the middle completion batch.

These are modern mnemonic symbols, never proposed historical character origins.
The caller supplies Sculpt so this module stays importable outside Blender.
"""
import math

KINDS = {
    'second-check','second-cross','second-plus','second-crown','second-altar',
    'second-steps','second-cycle','second-chain','second-shield','second-weight',
    'second-knot','second-ruler','second-target','second-tag','second-hammer',
    'second-compass','second-checklist','second-brackets','second-mask',
    'second-breath','second-cradle','second-burden','second-trophy',
    'second-nest','second-leather','second-beard','second-kneeler',
    'second-recliner','second-booth','second-alarm','second-jade',
    'second-broken','second-fence','second-strip','second-spring',
    'second-bin','second-platform','second-puzzle','second-meter',
    'second-ribbons','second-century','second-pipe',
}


def build(kind, s):
    if kind == 'second-check':
        s.line([(-.5,.02,0),(-.15,-.34,0),(.52,.40,0)],.095,'green','check mark')
    elif kind == 'second-cross':
        for sign in (-1,1):
            s.line([(-.40,sign*.40,0),(.40,-sign*.40,0)],.09,'red','no stroke')
    elif kind == 'second-plus':
        s.line([(-.46,0,0),(.46,0,0)],.08,'gold','join horizontally')
        s.line([(0,-.46,0),(0,.46,0)],.08,'gold','join vertically')
    elif kind == 'second-crown':
        s.poly([(-.56,-.26),(-.65,.39),(-.25,.12),(0,.57),(.25,.12),(.65,.39),(.56,-.26)],'gold',d=.30,name='crown')
        for x in (-.34,0,.34):s.ball((x,-.03,.18),(.07,.08,.025),'red','jewel')
    elif kind == 'second-altar':
        s.box((0,-.45,0),(1.15,.16,.65),'wood','altar base')
        for x in (-.4,.4):s.box((x,-.16,0),(.12,.60,.40),'wood','altar leg')
        s.box((0,.18,0),(1.18,.13,.67),'red','offering table')
        s.ball((0,.38,0),(.26,.13,.24),'gold','offering bowl')
        for x in (-.14,0,.14):s.line([(x,.39,0),(x,.77,0)],.013,'dark','incense')
    elif kind == 'second-steps':
        for i in range(4):s.box((-.48+i*.32,-.45+i*.20,0),(.32,.18+i*.38,.52),'woodlight','ascending step')
    elif kind == 'second-cycle':
        angles=[-.15+i*math.tau*.85/24 for i in range(25)]
        s.line([(.49*math.cos(a),.49*math.sin(a),0) for a in angles],.055,'blue','continuing arc')
        a=angles[-1];x=.49*math.cos(a);y=.49*math.sin(a)
        s.poly([(x-.20,y+.09),(x+.14,y+.17),(x+.09,y-.17)],'blue',d=.12,name='return arrow')
    elif kind == 'second-chain':
        for x in (-.34,0,.34):s.ring((x,0,0),.25,'gold',.045)
    elif kind == 'second-shield':
        s.poly([(-.50,.50),(.50,.50),(.45,-.07),(0,-.65),(-.45,-.07)],'blue',d=.19,name='protective shield')
        s.line([(-.25,.1, .12),(-.05,-.10,.12),(.28,.25,.12)],.05,'gold','safe check')
    elif kind == 'second-weight':
        s.poly([(-.58,-.47),(-.32,.36),(.32,.36),(.58,-.47)],'dark',d=.50,name='heavy weight')
        s.ring((0,.43,0),.15,'metal',.055)
    elif kind == 'second-knot':
        s.line([(-.70,0,0),(-.28,0,0),(.21,.30,.05),(.39,0,.05),(.21,-.30,.05),(-.23,.20,-.02),(-.37,0,-.02),(-.23,-.20,-.02),(.30,0,0),(.70,0,0)],.05,'red','tied knot')
    elif kind == 'second-ruler':
        s.box((0,0,0),(1.4,.24,.09),'gold','measuring rule')
        for i in range(11):s.line([(-.60+i*.12,.11,.065),(-.60+i*.12,.01 if i%2 else -.06,.065)],.009,'dark','measure tick')
    elif kind == 'second-target':
        for r,c in ((.54,'red'),(.34,'cream'),(.16,'gold')):s.ball((0,0,.13-r*.1),(r,r,.025),c,'target ring')
        s.line([(-.28,-.17,.22),(.03,0,.13)],.025,'wood','dart')
    elif kind == 'second-tag':
        s.poly([(-.57,-.25),(-.57,.25),(.29,.25),(.60,0),(.29,-.25)],'cream',d=.10,name='name tag')
        s.ring((.31,0,.065),.045,'wood',.012)
        for y in (-.09,.08):s.line([(-.40,y,.07),(.05,y,.07)],.014,'blue','tag writing')
    elif kind == 'second-hammer':
        s.line([(0,-.64,0),(0,.33,0)],.06,'wood','hammer shaft')
        s.box((0,.33,0),(.76,.27,.30),'metal','hammer head')
    elif kind == 'second-compass':
        s.ball((0,0,0),(.60,.60,.09),'gold','compass rim')
        s.ball((0,0,.08),(.51,.51,.022),'cream','compass dial')
        s.poly([(0,.44),(-.12,0),(0,-.44),(.12,0)],'red',z=.13,d=.04,name='north south needle')
        for x,y in ((.45,0),(-.45,0),(0,.45),(0,-.45)):s.ball((x,y,.12),(.025,.025,.012),'dark','direction mark')
    elif kind == 'second-checklist':
        s.box((0,0,0),(.85,1.12,.10),'cream','proof sheet')
        s.box((0,.53,.08),(.34,.15,.08),'metal','clipboard clip')
        for y in (-.32,0,.32):
            s.line([(-.28,y,.075),(-.22,y-.06,.075),(-.12,y+.08,.075)],.018,'green','checked condition')
            s.line([(-.02,y,.075),(.30,y,.075)],.016,'blue','condition')
    elif kind == 'second-brackets':
        for sign in (-1,1):s.line([(sign*.30,.54,0),(sign*.53,.54,0),(sign*.53,-.54,0),(sign*.30,-.54,0)],.055,'blue','including bracket')
    elif kind == 'second-mask':
        s.ball((0,0,0),(.47,.54,.08),'cream','borrowed mask')
        for x in (-.18,.18):s.ball((x,.14,.07),(.095,.08,.025),'dark','eye opening')
        s.line([(-.23,-.18,.10),(0,-.28,.11),(.23,-.18,.10)],.025,'red','painted smile')
        for sign in (-1,1):s.line([(sign*.40,.20,0),(sign*.69,.24,-.04)],.023,'red','mask ribbon')
    elif kind == 'second-breath':
        for y in (-.30,0,.30):s.line([(-.55,y,0),(-.15,y+.10,0),(.16,y-.02,0),(.57,y+.08,0)],.025,'water','breath wave')
    elif kind == 'second-cradle':
        for sign in (-1,1):
            s.line([(sign*.55,-.40,0),(sign*.40,-.13,0),(sign*.31,.13,0)],.08,'skin','receiving arm')
            s.ball((sign*.25,.03,0),(.23,.09,.18),'skin','cupped hand')
    elif kind == 'second-burden':
        s.person('walker')
        s.box((-.28,.03,-.28),(.52,.73,.36),'wood','carried responsibility')
        s.line([(-.31,.36,0),(-.20,-.32,0)],.03,'gold','shoulder strap')
    elif kind == 'second-trophy':
        s.box((0,-.53,0),(.64,.15,.45),'wood','award plinth')
        s.line([(0,-.48,0),(0,-.04,0)],.08,'gold','trophy stem')
        s.ball((0,.22,0),(.32,.31,.22),'gold','winning cup')
        for sign in (-1,1):s.line([(sign*.26,.39,0),(sign*.53,.36,0),(sign*.48,.04,0),(sign*.26,0,0)],.045,'gold','trophy handle')
    elif kind == 'second-nest':
        for i in range(4):s.ring((0,-.28+i*.045,0),.44-i*.025,'woodlight',.045)
        for x in (-.14,.14):s.ball((x,-.03,0),(.12,.18,.12),'cream','nurtured egg')
    elif kind == 'second-leather':
        s.poly([(-.53,-.27),(-.50,.41),(-.10,.49),(.46,.34),(.55,-.42),(.03,-.49)],'wood',d=.09,name='leather patch')
        for x in (-.37,-.15,.07,.29):
            for y in (-.31,.32):s.line([(x,y,.06),(x+.065,y,.06)],.012,'cream','stitch')
    elif kind == 'second-beard':
        for x in (-.30,-.15,0,.15,.30):s.line([(x,.37,0),(x*.9,-.18,.02),(x*.5,-.61,.06)],.06,'wood','and beard')
        s.ball((0,.40,0),(.39,.12,.15),'skin','chin')
    elif kind == 'second-kneeler':
        s.ball((0,.42,0),(.21,.24,.20),'skin','head')
        s.box((0,.02,0),(.30,.44,.26),'blue','torso')
        s.line([(0,-.18,0),(.32,-.42,0),(-.25,-.53,0)],.08,'dark','folded kneeling leg')
        s.line([(.10,.16,.12),(.42,.01,.13)],.06,'skin','arm')
    elif kind == 'second-recliner':
        s.ball((-.46,.08,0),(.23,.23,.21),'skin','reclining head')
        s.box((-.08,.0,0),(.60,.25,.32),'blue','reclining torso')
        for z in (-.10,.10):s.line([(.18,-.04,z),(.65,-.14,z)],.08,'dark','reclining leg')
    elif kind == 'second-booth':
        for x in (-.43,.43):s.box((x,0,-.06),(.10,1.10,.12),'wood','booth post')
        s.box((0,.51,-.06),(1.04,.12,.20),'red','booth roof')
        s.ball((0,.01,.12),(.31,.17,.07),'red','spitting mouth')
        for x,y in ((.48,.03),(.63,-.10),(.68,.14)):s.ball((x,y,.17),(.035,.035,.03),'water','spit bead')
    elif kind == 'second-alarm':
        s.poly([(-.55,-.45),(0,.59),(.55,-.45)],'gold',d=.13,name='warning triangle')
        s.line([(0,-.10,.09),(0,.25,.09)],.035,'dark','urgent stroke')
        s.ball((0,-.26,.09),(.045,.045,.023),'dark','urgent dot')
    elif kind == 'second-jade':
        s.ring((0,0,0),.39,'green',.16)
        s.ball((-.16,.24,.16),(.11,.045,.014),'white','jade glint')
    elif kind == 'second-broken':
        s.poly([(-.59,-.36),(-.54,.38),(-.07,.45),(-.15,.06),(.02,-.21),(-.13,-.40)],'earth',d=.38,name='broken left')
        s.poly([(.10,-.38),(.22,-.08),(.10,.16),(.18,.43),(.59,.35),(.62,-.36)],'earth',d=.38,name='broken right')
    elif kind == 'second-fence':
        for x in (-.57,-.28,0,.28,.57):s.box((x,0,0),(.09,1.1,.11),'wood','fence upright')
        for y in (-.22,.22):s.box((0,y,.06),(1.4,.07,.11),'woodlight','fence rail')
    elif kind == 'second-strip':
        s.line([(-.69,0,0),(0,.16,0),(.69,0,0)],.085,'red','long strip')
    elif kind == 'second-spring':
        s.ball((0,-.30,0),(.68,.10,.49),'earth','spring source')
        for y in (-.2,-.1,0):s.ring((0,y,.0),.24+(y+.2)*.8,'water',.025)
        s.line([(0,-.18,0),(-.14,.20,0),(.02,.55,0),(.17,.21,0)],.055,'water','spring jet')
    elif kind == 'second-bin':
        s.box((0,-.12,-.13),(.68,.86,.37),'metal','discard bin')
        s.box((0,.33,0),(.78,.09,.67),'dark','bin opening')
        for x in (-.23,0,.23):s.line([(x,-.48,.08),(x,.18,.08)],.012,'dark','bin rib')
    elif kind == 'second-platform':
        s.box((0,-.3,0),(1.2,.26,.74),'wood','stage platform')
        for x in (-.49,.49):s.box((x,-.53,0),(.14,.29,.59),'woodlight','stage support')
    elif kind == 'second-puzzle':
        s.box((-.26,0,0),(.47,.64,.16),'blue','left fit')
        s.ball((-.01,0,0),(.16,.16,.10),'blue','joining nub')
        s.box((.32,0,0),(.36,.64,.16),'gold','right fit')
    elif kind == 'second-meter':
        s.box((0,0,0),(1.22,.50,.13),'cream','capacity meter')
        for i in range(5):s.box((-.44+i*.22,0,.09),(.17,.30,.045),'green' if i<4 else 'woodlight','meter segment')
    elif kind == 'second-ribbons':
        s.line([(-.53,-.43,0),(.03,.03,.035),(.53,.43,0)],.045,'pink','crossed pink ribbon')
        s.line([(-.53,.43,0),(0,-.02,-.035),(.53,-.43,0)],.045,'gold','crossed gold ribbon')
        s.ball((0,0,.04),(.10,.08,.06),'red','ribbon tie')
    elif kind == 'second-century':
        s.box((0,0,0),(1.20,1.34,.08),'cream','century calendar')
        s.box((0,.57,.065),(1.19,.16,.045),'red','calendar binding')
        # Ten rows of ten individual years make the century visible exactly.
        for i in range(100):
            s.box(((i%10-4.5)*.105,.42-(i//10)*.105,.065),(.073,.071,.035),'gold','year '+str(i+1))
    elif kind == 'second-pipe':
        s.line([(0,-.65,-.08),(0,.21,-.08),(.16,.40,-.08),(.33,.40,.10)],.135,'metal','bent channel pipe')
        s.ring((.33,.40,.22),.145,'metal',.038)
        s.ball((.33,.40,.211),(.109,.109,.019),'dark','recessed pipe opening')
        for y in (-.36,.02):s.ring((0,y,.06),.14,'woodlight',.022)
    else:
        raise ValueError('Unknown second-batch prop: '+kind)
