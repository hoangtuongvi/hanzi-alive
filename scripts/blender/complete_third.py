"""Explicitly authored explanations for the final 293 missing words.

Each row specifies its own visual choices and invented mnemonic. Source glyphs
are looked up, never rewritten to fit a convenient prop. The modest ordered
layout lets the app's exact component labels identify each 3D object.
"""
import json
import math
from pathlib import Path


# word | unique descriptive slug | authored story | ordered props | supports
ROWS = r"""
既然|given-condition|An already-completed check stands beside a second so-check: since the first condition is given, the next conclusion can follow.|third-check,third-check|arrow
提醒|lifting-awake|An upward arrow lifts a sleepy face toward an open eye: the reminder wakes your attention.|arrow,eye|third-surprise
演员|stage-member|A performer on a miniature stage wears a member badge: this member of the cast is an actor.|third-theater,third-badge|music
态度|attitude-degree|A facial expression supplies an attitude while a ruler measures its degree: imagine choosing how warm or stern your attitude will be.|face,third-ruler|heart
周围|around-enclosure|A circular path goes around a frame; the frame surrounds the space at its center, showing the surroundings.|third-loop,frame|third-village
丢|king-lost-cocoon|A king's crown remains beside a private cocoon but its owner has lost track of the little coil: picture losing a possession.|third-crown,coil|question
复杂|repeated-mixture|A returning loop feeds a jumble of differently shaped tools: repeated and mixed operations make the task complicated.|third-loop,box|gear,pencil,spoon
表达|display-reaching|A display board sends its message along an arrow that reaches the listener: make your thought visible to express it.|board,arrow|speech
邀请|inviting-please|An invitation envelope travels toward a polite speech bubble saying please: picture asking a guest to join you.|envelope,speech|third-bow-person
交通|crossing-through|Two crossing roads meet a clear gateway through which a vehicle can pass: exchange at the crossing becomes traffic and transportation.|third-crossroads,gate|car
优秀|excellent-elegance|An excellence trophy stands beside an elegant flower: outstanding achievement and graceful presentation suggest excellent.|third-trophy,flower|star
亮|covered-table-lamp|A lid sits over an open mouth-shaped frame, while a cover shelters a small table; imagine a lamp making this odd paired arrangement bright.|lid,mouth,roof,table|lamp
篇|bamboo-banner-writing|Bamboo slips lie beside a flat banner carrying a written work: count the complete composition as one 篇.|third-bamboo,paper|book
儿童|village-children|Little legs stand beside a child from a village: imagine the village children gathering to play.|leg,child|third-village
最好|highest-good-choice|The highest step presents a good green check: choose that top option as the best, or the one you had better take.|third-levels,third-check|third-trophy
味道|taste-path|A tongue tastes a spoonful while a little path leads to the bowl: follow the taste all the way to its flavor.|tongue,road|bowl
断|snapped-bar|A wooden bar has snapped into two separated jagged ends: the visible gap is your cue for break or snap.|third-broken|knife
千万|emphatic-many|A counted group represents a thousand beside a much larger counted group for ten thousand: imagine repeating the warning emphatically, be sure to do it.|count-10,count-20|speech
距离|measured-departure|A ruler marks a distance while an arrow leaves the starting place: measure how far the departure carries you.|third-ruler,arrow|footprints
轻松|light-pine-rest|A feather feels lightweight beside a pine tree with loose spreading branches: imagine resting there, relaxed and at ease.|feather,third-pine|chair
墙|miser-earthen-wall|An earthen block protects a miser's locked box: imagine stacking the earth into a wall around the hoard.|earth,lock|wall,coins
毕业|finished-work|A completion check rests beside a work desk: the course of work is finished, so picture graduating with your books.|third-check,table|book,third-trophy
怀疑|heart-question|A heart holds a question bubble rather than a firm answer: the held-in-heart uncertainty becomes doubt or suspicion.|heart,question|third-no
修|traveler-repairs-stripes|A leisurely traveler finds three loose stripes and puts them back in order: imagine repairing a striped garment on the journey.|walker,third-three-stripes|third-check
戴|ten-unusual-halberd|Ten beads hang beside an unusual masked face and a halberd: imagine wearing these extraordinary accessories for a costume.|count-10,third-mask,third-halberd|hat
究竟|final-investigation|A magnifier investigates deeply until a final check appears: what exactly did the investigation establish, after all?|third-magnifier,third-check|question
轻|hand-work-light-car|A vehicle waits beside a hand and a work gear: imagine the hand's work removing heavy loads until the vehicle is light in weight.|car,hand,gear|feather
然而|so-bearded-objection|A so-check faces a bearded speaker who raises an objection: however interrupts the conclusion that seemed to follow.|third-check,third-beard|third-no,speech
交流|crossing-flow|Opposing arrows trade messages beside flowing water: picture ideas flowing both ways as people communicate and exchange.|third-exchange,water|speech
兴奋|excited-effort|A surprised face bursts with excitement while an arm exerts itself: imagine excited energy making you jump into action.|third-surprise,third-arm|star
符合|matching-fit|A coded token sits beside two fitting puzzle pieces: when the token matches the joined shape, it meets the requirement.|third-tag,third-puzzle|third-check
躺|body-reclining-prize|A body reclines beside a prized star: picture lying down to admire the precious object without getting up.|third-recliner,star|bed
答案|answer-case-file|An answer check is filed beside a closed case book: the solved question now has an answer in its case file.|third-check,book|question
皮肤|skin-surfaces|A pale skin-like sheet sits beside a hand's outer surface: compare both surfaces to remember skin.|lining,hand|face
浪费|wave-of-cost|A wave washes coins away from a full purse: the cost disappears without useful result, making waste visible.|water,coins|third-no
厉害|fierce-harm|A fierce tiger guards a broken plank: its formidable strength can cause harm, making 厉害 feel impressive and powerful.|tiger,third-broken|third-weight
尊重|respect-weight|A bowing person treats a heavy weight with care: imagine giving respect the weight and importance it deserves.|third-bow-person,third-weight|heart
激动|stirred-motion|A splash of water is stirred beside a moving arrow: imagine emotion being stirred until you feel excited and moved.|water,arrow|third-surprise
骗|horse-banner-deception|A horse stands before a flat banner hiding a broken board: the attractive banner conceals the truth, a mnemonic for deception.|horse,paper|third-broken,third-no
可怜|permission-for-pity|A permission check opens the way to a tearful face: let yourself feel pity for the person who needs care.|third-check,third-sad|heart
擦|hand-wipes-inspection|A hand wipes a surface while a magnifier inspects the clean patch: keep rubbing until the dirt is gone.|hand,third-magnifier|towel
成熟|successful-ripening|A successful green check rests beside ripe fruit: imagine the fruit reaching its completed, mature state.|third-check,apple|sun
无聊|empty-conversation|An empty frame sits beside an ear waiting for chat, but no speech arrives: the silence feels boring.|third-empty,ear|clock
文章|writing-chapter|A written sheet joins a bound chapter book: picture the sheets forming one complete article.|paper,book|pencil
信任|trusted-duty|A heart-marked message is given to a duty bearer wearing a badge: handing over responsibility expresses trust.|envelope,third-badge|heart
实际|real-border|A solid cube is placed beside a boundary frame: test what is actually inside the real limits, not merely imagined.|third-weight,frame|third-check
年龄|year-age-count|A year calendar stands beside a row of counted beads: count the completed years to find someone's age.|calendar,count-10|elder
差不多|few-differences|A ruler finds a difference, a red cross says not, and many beads wait: there are not many differences, so the two amounts are almost the same.|third-ruler,third-no,count-10|scale
可惜|allowed-but-regretted|A permission check faces a sad heart: something was possible, yet a cherished chance was lost, what a pity.|third-check,third-sad|heart
回忆|returning-memory|A returning arrow circles back to a memory book: reopen the old scene in your mind and recall it.|third-loop,book|heart
材料|raw-material-ingredients|A wooden board rests beside a bowl of ingredients: these are the materials waiting to become something new.|board,bowl|gear
熟悉|ripe-full-knowledge|Ripe fruit sits beside a thoroughly read book: imagine knowing the fruit's taste so fully that it is familiar.|apple,book|third-check
随便|follow-easy-route|Footprints follow an easy arrow without a fixed rule: take whichever convenient route you like.|footprints,arrow|road
撞|hand-village-bump|A reaching hand bumps into a village child's ball: the imagined collision makes bump into memorable.|hand,child|ball
互相|mutual-reflections|A returning loop links two facing mirrors: each reflects the other, a picture of mutual action.|third-loop,mirror|heart
合适|fitting-fit|Two joined puzzle pieces sit beside a check confirming their fit: what fits the situation is suitable.|third-puzzle,third-check|third-grid
失望|lost-hope|An empty place where a prize should be faces an eye still looking hopefully: the missing prize brings disappointment.|third-empty,eye|third-sad
印象|elephant-impression|A stamp presses an elephant-shaped memory onto a sheet: picture the elephant leaving a lasting impression.|stamp,third-elephant|paper
号码|coded-number|A counted bead panel sits beside a striped code tag: the count receives a code and becomes a number you can identify.|count-5,third-tag|phone
出生|exit-growth|A sprout emerges through an exit doorway: new life comes out and begins to grow, a mnemonic for being born.|door,sprout|child
基础|base-and-stone|A broad base supports a sturdy stone block: together they make a firm foundation for building upward.|earth,third-weight|house
适应|fit-response|A fitting puzzle faces a responsive arrow: adjust your action until it fits the new setting, and you adapt.|third-puzzle,arrow|third-check
赚|shell-two-jobs|A shell stands beside two work tools: imagine doing both jobs together and earning a shell as payment.|shell,gear|axe,coins
猜|animal-green-guess|An animal peers at a green patch hidden in a box: it must guess whether the green thing is a leaf or something else.|dog,leaf|question,box
到处|arrival-every-stop|An arrival arrow points toward a stopping place represented by a bench: imagine the same arrival happening at every place, everywhere.|arrow,chair|map
食品|food-products|A bowl of food stands beside a boxed product: the meal becomes a packaged food product.|bowl,box|rice
大约|big-approximation|A large circle surrounds an appointment clock: its broad margin allows an approximate time, not an exact instant.|ball,clock|third-ruler
提前|lift-to-front|An upward arrow lifts a calendar page in front of the main schedule: finish the task ahead of that date, in advance.|arrow,calendar|third-check
暂时|temporary-time|An hourglass stands beside a clock: the arrangement lasts only while the sand runs, temporarily.|third-hourglass,clock|chair
积极|accumulating-extreme|A growing stack of blocks climbs toward the highest step: active effort accumulates and reaches an enthusiastic extreme.|third-book-stack,third-levels|third-trophy
高级|high-level|A tall tower stands beside ascending steps: reaching the high level makes this an advanced, high-grade stage.|tower,third-levels|star
汤|sunlit-soup|Water catches rising sunshine beside a warm bowl: imagine sunshine heating the water into soup.|water,sun|bowl,steam
收入|collected-inward|A purse collects coins beside an inward-pointing arrow: money entering your collection is income.|bag,arrow|coins
恐怕|fearful-forecast|A worried face huddles beside a protective shield: imagine saying I'm afraid that before a worrying possibility.|third-sad,third-shield|question
仔细|child-fine-detail|A small child studies a fine detail through a magnifier: careful attention notices even tiny marks.|child,third-magnifier|third-spots
严格|strict-grid|A closed lock guards a measured grid: every piece must meet the grid's strict standard before it passes.|lock,third-grid|third-check
及时|reach-before-clock|A reaching hand meets a clock before its deadline: you reach the needed moment promptly, in time.|hand,clock|third-check
知识|knowing-recognition|A learned book stands beside a recognizable code sign: know the lesson and recognize its sign to recall knowledge.|book,third-tag|third-check
专门|specialized-door|One distinctive tool stands beside a dedicated doorway: this entrance is specially reserved for its specialized task.|gear,door|third-target
脱|moon-exchange-off|A moon trades its outer shirt through an exchange loop: picture taking off the garment and leaving it behind.|moon,third-loop|shirt
租|grain-shelf-rental|A bundle of grain sits beside a borrowed shelf: imagine paying grain for temporary use rather than owning it.|wheat,shelf|coins
尤其|especially-that-one|A bright star singles out a tagged object: especially that one deserves your attention.|star,third-tag|third-target
博士|broad-scholarship|A broad stack of books stands beside a scholar's badge: picture extensive learning earned by a doctorate holder.|third-book-stack,third-badge|hat
故意|planned-old-tale|An old storybook sits beside a thought bubble: imagine choosing the action in the story deliberately, with an idea already formed.|book,speech|third-target
看法|view-method|An eye studies an arrangement of tools: the way you look and the method you use shape your opinion.|eye,gear|speech
浪漫|overflowing-waves|A wave meets an overflowing cup beneath a heart: imagine affection overflowing like water in a romantic scene.|water,cup|heart
辛苦|hardship-bitterness|A heavy work tool stands beside a lemon imagined to taste bitter: difficult effort leaves an unpleasant taste, making tiring hardship memorable.|axe,lemon|third-sad
剩|rider-leftover-cut|A seated rider waits beside a knife after part of a meal is cut away: notice the portion that remains.|sitter,knife|bread
正好|correct-and-good|A ruler's correct measure meets a good check: the fit is neither too much nor too little, just right.|third-ruler,third-check|third-target
主动|host-starts-motion|A host wearing a badge sends the first arrow forward: taking the first action shows initiative.|third-badge,arrow|walker
硬|stone-resists-change|A stone block stands beside a changing loop that cannot bend it: the stone remains hard and firm.|third-weight,third-loop|third-no
限制|bounded-making|A boundary frame surrounds a manufacturing gear: the frame limits how far the machine's work may extend.|frame,gear|third-no
判断|judged-cut|A balance judges two possibilities beside a divided plank: decide where to draw the dividing cut.|scale,third-broken|third-check
现代|new-appearance-replacement|A glowing screen appears beside a replacement arrow: the new device replaces the older tool, suggesting modern times.|screen,arrow|gear
弹|single-bow-string|One bow has one taut string: imagine plucking the single string until it sounds, linking the bow and single cues to playing strings.|third-bow,count-1|music
有趣|possessed-interest|A full box holds a surprising little toy: what you have captures interest and feels interesting.|box,third-surprise|ball
公里|public-village-distance|A public group walks toward a village beside a marked ruler: imagine measuring their road distance in kilometers.|third-crowd,third-village|third-ruler,road
好处|good-stopping-place|A good check stands beside a comfortable stopping chair: the useful place gives a benefit.|third-check,chair|heart
区别|district-separation|A district map faces two separated blocks: compare the districts and distinguish their differences.|map,third-broken|third-ruler
暗|sun-sound-dimness|A small sun hides behind a sound symbol: imagine hearing music in a room where the light has become dark and dim.|sun,music|roof
将来|about-to-arrive|An hourglass waits beside an approaching arrow: what is about to come lies in the future.|third-hourglass,arrow|calendar
聊天|ear-chat-sky|An ear catches a speech bubble beneath an open sky: picture relaxed conversation outdoors, chatting.|ear,cloud|speech
小说|small-speaking-book|A little book stands beside a speech bubble: the small imagined speaking world inside becomes a novel.|book,speech|third-theater
鼓励|drum-encouragement|A drum beats beside an encouraging trophy: imagine the rhythm cheering someone onward.|drum,third-trophy|arrow
理想|reason-imagination|A carefully measured grid sits beside an imagined star: reason and imagination shape an ideal dream to aim for.|third-grid,star|third-target
后悔|behind-regret|A backward-pointing path leads to a sad face: look behind at a past choice and feel regret.|third-loop,third-sad|clock
举办|raised-task|An upward arrow raises an event flag while a task book organizes the details: picture holding an event successfully.|arrow,book|flag
感动|felt-motion|A heart feels the scene beside a moving arrow: imagine the feeling moving you emotionally.|heart,arrow|third-sad
顾客|cared-for-guest|A protective hand attends to a visitor beside a shop counter: looking after the guest makes the person a customer.|hand,person|table
组成|group-success|A grouped cluster of blocks fits beside a successful check: the parts compose a completed whole.|count-5,third-check|third-puzzle
流行|flowing-walkers|Flowing water carries the same hat toward walking footprints: imagine the style spreading among people until it is popular.|water,footprints|hat
整理|ordered-reason|An orderly shelf faces a measured grid: put objects into a reasonable arrangement to tidy and organize.|shelf,third-grid|book
丰富|abundant-riches|A plentiful bowl of grain sits beside a full treasure jar: the overflowing supply feels rich and abundant.|rice,pot|coins
哪里|which-village|A question bubble asks which village on a little map: point to the location to answer where.|question,third-village|map
刮风|scraping-wind|A scraping blade faces curled wind streams: imagine the gust scraping loose leaves across the ground.|knife,third-wind|leaf
百分之|hundred-dividing-link|A bead panel stands for a hundred, a knife divides its share, and a linking path connects share to whole: picture a percentage.|count-20,knife,road|third-grid
棒|solid-stick|A straight wooden pole serves as a stick: imagine holding its smooth shaft in your hand.|pole|hand
报名|reporting-name|A reporting envelope sits beside an identity badge: send your name to the organizer to sign up.|envelope,third-badge|pencil
抱歉|hugging-shortfall|A heart offers a hug beside an empty place where a needed piece is missing: acknowledge the shortfall and say sorry.|heart,third-empty|third-sad
笨|clumsy-choice|A heavy block is balanced awkwardly on a tiny stool: picture a clumsy, ill-judged choice as a mnemonic for stupid, not a judgment about a person.|third-weight|chair,third-no
比如|compared-example|A comparison balance stands beside a sample puzzle piece: use the sample as an example of the kind you mean.|scale,third-puzzle|third-grid
表格|displayed-grid|A display board presents a row-and-column grid: fill the visible boxes to complete the form.|board,third-grid|pencil
表扬|displayed-fluttering-prize|A displayed trophy stands beside a fluttering flag: publicly celebrating the achievement is praise.|third-trophy,flag|speech
参观|join-and-observe|A joining group approaches an observing eye: picture joining a visit to look around the exhibits.|third-crowd,eye|third-magnifier
厕所|toilet-place|A porcelain toilet stands beside a marked place on a map: find the place set aside as the toilet.|third-toilet,map|door
尝|sample-taste|A spoon offers a small sample to a tongue: take one taste before deciding whether to eat more.|tongue|spoon
诚实|honest-solid-truth|A transparent-in-spirit check sits beside a solid real block: an honest account matches what is actually there.|third-check,third-weight|speech
吃惊|eating-surprise|A mouth eating from a bowl faces a suddenly wide-eyed face: an unexpected interruption makes you startled.|mouth,third-surprise|bowl
抽烟|drawn-out-smoke|A hand draws out a thin stick while curls of smoke rise beside it: imagine the act of smoking, without treating it as advice.|hand,steam|pole
出差|exit-duty-trip|An exit doorway faces a comparison ruler for a different place: leave your usual desk on a business trip.|door,third-ruler|suitcase
传真|passed-true-copy|A passing arrow carries a faithful copy of a written sheet: imagine a fax transmitting the true page to another desk.|arrow,paper|screen
粗心|rough-hearted-attention|A rough brick stands beside a distracted heart: imagine rough, inattentive handling of a fragile object as carelessness.|wall,heart|third-broken
存|existing-object|A solid cube remains inside an otherwise empty frame: the object is still there, it exists.|third-weight|third-empty
错误|wrong-error|A red cross sits beside a broken puzzle: the wrong choice produces an error rather than a fitting result.|third-no,third-broken|third-puzzle
打扮|struck-costume-decoration|A hand reaches toward a colorful costume mask: imagine arranging and decorating a costume to dress up.|hand,third-mask|shirt
打扰|hit-poking-interruption|A striking hand faces a poking pole beside a reader's book: the intrusive taps disturb the quiet work.|hand,pole|book
打印|hit-the-seal|A hand strikes the top of a stamp to affix its seal: this scene follows the database's selected seal-stamping sense, not the modern printer sense.|hand,stamp|paper
打招呼|hand-summons-breath|A raised hand summons a friend while a mouth releases a greeting breath: word and gesture together greet someone.|hand,flag,mouth|speech
打折|price-hit-break|A hand strikes a broken price bar beside coins: imagine breaking off part of the price to give a discount.|hand,third-broken|coins
打针|hand-and-needle|A careful hand holds a syringe with its thin needle visible: the arrangement recalls giving or having an injection.|hand,third-syringe|medical
大使馆|large-envoy-building|A large star identifies an envoy's badge beside a public building: the important representative works at an embassy.|star,third-badge,house|flag
大夫|large-official-husband|A large crown rests beside an adult man: imagine a dignified senior official, the historical sense selected by this database, rather than the doctor reading.|third-crown,man|third-badge
导游|directed-tour|A guiding arrow leads to a map of a tour: follow the direction given by the tour guide.|arrow,map|walker
倒|collapsed-standing|A formerly upright pole lies diagonally beside an empty support: imagine the instant it falls and collapses.|third-broken|pole
道歉|path-to-apology|A road leads to a missing puzzle piece: acknowledge what was deficient along the way and apologize.|road,third-empty|third-bow-person
得意|obtained-idea-pride|A trophy has been obtained beside a bright thought star: picture being pleased and proud of your successful idea.|third-trophy,star|face
登机牌|rise-machine-pass|Ascending steps lead toward an airplane machine and a coded card: present the boarding pass before rising into the plane.|third-levels,plane,third-tag|third-check
堵车|wall-of-vehicles|A wall blocks a vehicle's road: imagine many cars unable to get past the obstruction, a traffic jam.|wall,car|road
肚子|child-belly|A rounded belly-shaped bowl sits beside a child: imagine the child's full tummy after a meal.|bowl,child|rice
短信|short-trusted-message|A short written note sits beside a trusted envelope: send the brief message to a phone as a text.|paper,envelope|phone
对话|facing-talk|A facing mirror meets a speech bubble: imagine two people facing each other and taking turns talking.|mirror,speech|person
对于|facing-reference-point|A facing eye looks toward a marked target: the target supplies the at-marker, the topic regarding which you speak.|eye,third-target|speech
翻译|turned-translation|A turning loop faces two linked speech bubbles: turn a message into a different language through translation.|third-loop,speech|book
烦恼|annoyed-angry-faces|A worried face sits beside a fierce painted mask: annoyance and anger swirl together into worries.|third-sad,third-mask|question
房东|room-east-owner|A room stands beside an eastward arrow: imagine the owner waiting on the east side of the rental room, a cue for landlord.|house,arrow|key
放暑假|released-hot-fake-school|An outward arrow releases a hot sun from a pretend schoolbook: imagine school pausing for summer vacation, with the fake cue treated only as a mnemonic.|arrow,sun,book|umbrella
放松|released-pine-rest|An outward arrow releases a tightened coil beside a pine tree: let the tension loosen and relax in its shade.|arrow,third-pine|coil
复印|repeated-stamp-copy|A returning loop runs back to a stamp: repeat the page's impression to make a photocopy.|third-loop,stamp|paper
富|roof-full-jar|A protective roof stands above a full jar with coins nearby: the sheltered store of supplies makes rich memorable.|roof,pot|coins
干杯|dry-cup-toast|A dry towel sits beside a cup raised for a toast: imagine draining the cup and saying cheers.|towel,cup|speech
赶|pursuing-overtake|Walking feet follow a forward arrow toward another traveler: imagine speeding up in pursuit until you overtake.|walker|arrow
刚|ridge-knife-hardness|A rocky ridge stands beside a knife that cannot cut it: the ridge feels hard and unyielding.|mountain,knife|third-no
高速公路|high-speed-public-road|A high tower overlooks a speedy arrow, a public group and a clear road: combine the four cues into an expressway.|tower,arrow,third-crowd,road|car
胳膊|arm-and-shoulder|A bent arm meets a rounded shoulder joint: picture the connected limb from shoulder to hand.|third-arm,third-joint|hand
功夫|achieved-work-man|A work gear stands beside a practicing man: skilled work completed through practice gives 功夫, skill.|gear,man|third-trophy
广播|shelter-sowing-sound|A shelter roof stands beside scattered seeds: imagine sowing spoken messages widely from the sheltered station, a mnemonic for broadcast.|roof,count-5|speech
逛|wandering-footsteps|A walking person follows a curling route rather than a straight errand: imagine strolling and rambling at leisure.|walker|third-loop
国籍|country-register|A national flag stands beside a register book: the recorded country identifies nationality.|flag,book|third-badge
害羞|harm-shame|A broken board sits beside a lowered, tearful face: imagine fearing harm to your confidence and feeling shy or ashamed.|third-broken,third-sad|person
寒假|chilly-pretend-school|An ice block chills a pretend schoolbook: imagine the classroom closed for winter vacation, using fake only as the source's mnemonic cue.|ice,book|snow
汗|khan-sweat-association|A ruler's crown floats above a water cue: imagine the perspiration of a khan. This recalls the database's hán cross-reference reading, not ordinary hàn sweat.|water|third-crown
航班|vessel-flight-group|A vessel waits beside an assigned group of passengers: imagine their scheduled airplane flight as a vessel carrying its group.|boat,third-crowd|plane
合格|fit-the-grid|Two fitting puzzle pieces meet a measured grid: they conform to the required standard and qualify.|third-puzzle,third-grid|third-check
厚|generous-thick-stack|A generous stack of books makes the thickness visible: use the source's generous cue as an association with a thick, substantial supply.|third-book-stack|third-ruler
互联网|mutual-linked-net|A mutual loop meets linked ears and a mesh net: imagine conversations interconnected across the Internet.|third-loop,ear,net|third-circuit
活泼|alive-pouring-energy|A fresh sprout grows beside a pouring cup: imagine living energy splashing outward, lively and animated.|sprout,cup|water
积累|accumulation-tiredness|An accumulating stack rises beside a tired seated person: repeated small efforts build the pile, even when tiring.|third-book-stack,sitter|third-levels
寄|mailed-envelope|An envelope waits beside a forward arrow: seal the message and send it away by mail.|envelope|arrow
加班|added-work-group|A plus sign adds another task to a work group: imagine working overtime after the normal session.|third-plus,third-crowd|clock,gear
加油站|add-oil-stop|A plus sign stands beside an oil can and a standing fuel pump: stop at the station to add fuel.|third-plus,third-oil,third-pump|car
家具|home-tools-furniture|A home stands beside a useful chair: the tools and furnishings placed in the home become furniture.|house,chair|table
减肥|subtracting-fat|A minus sign faces a rounded body-like ball beside a scale: imagine reducing excess weight, a mnemonic for lose weight rather than health advice.|third-minus,ball|scale
建议|building-discussion|A house under construction stands beside a discussion bubble: propose an idea about how to build it.|house,speech|third-puzzle
降低|descending-low|A descending staircase ends at a low block: imagine reducing the level step by step.|third-levels,earth|arrow
郊区|outlying-district|A small village on the outskirts sits beside a district map: picture the suburban district beyond the city center.|third-village,map|house
骄傲|proud-crowns|A showy crown stands beside a lifted trophy: imagine pride rising into a haughty display.|third-crown,third-trophy|star
接着|receiving-continuing-hold|A receiving hand holds a cord while an eye keeps watching the grip: catch it and hold on, the sense selected here, with continuing attention.|hand,eye|coil
节|joint-key-point|A hinged joint connects two limbs beside a marked target: this vital connection pictures a critical juncture, the jiē reading selected through 节骨眼.|third-joint|third-target
节约|joint-appointment-saving|A joint allows a tool to fold beside an appointment clock: save space and schedule resources carefully to economize.|third-joint,clock|coins
禁止|restricted-stop|A lock restricts a path beside a red stop cross: the passage is prohibited.|lock,third-no|road
京剧|capital-opera|A capital's tower stands beside an opera mask: imagine the theatrical performance of Beijing opera in the capital.|tower,third-mask|third-theater
景色|landscape-colors|A miniature mountain landscape stands beside a colorful flower: scenery brings the landscape's colors into view.|mountain,flower|tree
举|excited-lifting-hand|An excited face sits beside a hand ready to lift a trophy: the lifted gesture makes 举 memorable.|third-surprise,hand|third-trophy
聚会|assembled-can-do|An assembled group of people stands beside a permission check: everyone can gather, making a party.|third-crowd,third-check|cake
开玩笑|open-play-laughter|An open doorway reveals a play ball and smiling face: imagine a playful joke opening into laughter.|door,ball,face|speech
烤鸭|baked-duck|A cooking flame stands beside a golden-brown duck: picture the duck being roasted until ready to serve.|flame,third-duck|plate
棵|one-counted-tree|A single tree stands in its own marked place: count one tree, plant or cabbage with the classifier 棵.|tree|count-1
咳嗽|cough-and-gargle|A mouth releases a sudden breath beside a cup of gargling water: the paired throat actions make cough memorable.|mouth,cup|steam
来不及|arrival-cannot-reach|An approaching arrow faces a red no-cross before a reaching hand: there is not enough time to reach the deadline.|arrow,third-no,hand|clock
来得及|arrival-gets-to-reach|An approaching arrow obtains a check before meeting a reaching hand: there is enough time to reach the deadline.|arrow,third-check,hand|clock
来自|approach-from-self|An approaching arrow starts from a person's own badge: trace where this arrival comes from.|arrow,third-badge|map
冷静|cold-quiet|A cool ice block stands beside a silent, closed book: imagine settling into calm, quiet attention.|ice,book|heart
礼拜天|courtesy-bow-sky|A courteous gift stands beside a bowing person beneath a sky cloud: use this imagined Sunday ritual to link the three cues.|bag,third-bow-person,cloud|calendar
礼貌|courteous-countenance|A courteous bow faces a pleasant countenance: respectful behavior and expression together show courtesy.|third-bow-person,face|heart
理发|reason-sent-hair|A carefully organized comb-like grid stands beside a sending arrow and loose hair: imagine arranging hair and sending the cut strands away in a haircut.|third-grid,arrow|hair,knife
力气|strength-air|A flexed arm meets curling air: imagine a strong breath supporting the effort of strength.|third-arm,steam|third-weight
例如|precedent-as-if|An earlier written example stands beside a matching puzzle sample: this precedent shows what the next case can be like, for example.|paper,third-puzzle|book
流利|flowing-profitable-speech|A stream flows past a smooth coin: imagine speech flowing without obstruction as smoothly as a useful transaction, fluent.|water,coins|speech
迷路|bewitching-path|A surprising mask distracts a traveler from the correct path: the bewildered walker loses the way.|third-mask,road|question
密码|secret-code|A locked message stands beside a striped code tag: only someone knowing the secret can read the cipher.|lock,third-tag|envelope
秒|second-hand-tick|A thin clock hand crosses one small tick: picture the brief unit of time called a second.|third-second|clock
民族|citizens-related-group|A group of citizen badges faces a branching family-like tree: imagine the shared group identity expressed by nationality or ethnicity.|third-badge,tree|count-5
耐心|resisting-heart|A shield resists impatience beside a steady heart: keep the heart calm while you wait patiently.|third-shield,heart|third-hourglass
难受|difficult-acceptance|A difficult heavy block sits beside a receiving hand: imagine feeling unwell and finding even a small burden hard to accept.|third-weight,hand|third-sad
偶尔|accidental-badge-meeting|A surprising chance encounter meets a personal badge: the accidental meeting happens only occasionally.|third-surprise,third-badge|calendar
批评|commented-appraisal|A comment bubble faces a balance that appraises the work: critical feedback points out what should improve.|speech,scale|third-no
脾气|spleen-air-temper|A model spleen faces a puff of air: imagine the puff carrying a person's temper and character, an invented mnemonic, not a medical explanation.|third-spleen,steam|third-mask
平时|level-usual-clock|A level bar rests beside an ordinary clock: imagine the level, everyday routine followed at ordinary times.|bar,clock|calendar
普遍|general-every-place|A representative group stands beside a map covered with stops: the same pattern occurs throughout, universally.|third-crowd,map|third-spots
其次|that-next-turn|A tagged item stands beside the next step on a staircase: after that one comes the next turn.|third-tag,third-levels|arrow
签证|signature-proof|A signing pencil meets a proof badge: the signed authorization provides the visa needed to travel.|pencil,third-badge|plane
敲|hammering-tap|A wooden tool taps against a solid board: imagine the sharp sound of hitting or knocking.|axe|board
亲戚|parent-shy-relative|An elder parent stands beside a shy-looking family member: the imagined family meeting links parent and ashamed cues to a relative.|elder,third-sad|heart
穷|empty-purse-poverty|An open purse has an empty space where coins should be: the lack of money recalls poor.|third-empty|bag
缺点|missing-dot|An incomplete frame stands beside one isolated dot: notice the missing point where the structure has a weakness.|third-empty,third-spots|third-no
缺少|missing-few|A vacant place stands beside only a few beads: the supply is lacking and too small.|third-empty,count-2|box
热闹|hot-busy-party|A warm flame faces a busy gathering: imagine lively heat, chatter and motion in a bustling place.|flame,third-crowd|speech,music
商量|trade-measure-talk|A trading coin stands beside a measuring balance: discuss the terms until both sides agree.|coins,scale|speech
稍微|somewhat-small|A small partial stack faces one tiny bead: the amount is only a little bit.|count-3,count-1|third-ruler
生意|growing-idea-life-force|A growing sprout stands beside a bright idea-star: imagine life's force generating new growth and ideas, the selected sense here rather than commerce.|sprout,star|heart
师傅|teacher-tutor|Two teaching figures hold the imagined lesson between them: the experienced teacher and tutor together suggest a master.|person,elder|book
是否|is-or-no|A confirming check faces a negative cross: decide whether the statement is so or not.|third-check,third-no|question
收拾|collect-and-sort|A collecting basket sits beside another gathered pile: place the collected objects together in order.|basket,box|book
首都|head-of-all-city|A leader's crown stands beside a group representing all the people: the leading city for the whole group is the capital.|third-crown,third-crowd|tower
受不了|cannot-accept-finish|A receiving hand faces a no-cross and a final hook: imagine a burden you cannot accept through to the end, unbearable.|hand,third-no,hook|third-weight
数量|count-and-measure|A row of beads is counted beside a ruler: count and measure the supply to determine its amount.|count-10,third-ruler|box
顺便|smooth-convenient-route|A smooth route points toward a handy doorway: take the useful stop conveniently along the way.|road,door|arrow
硕士|great-scholar|A large trophy stands beside a scholar's badge: imagine advanced study earning the master's degree.|third-trophy,third-badge|book
塑料袋|sculpted-ingredient-bag|A shaped puzzle block sits beside ingredients and a carrying bag: imagine the material being formed into a plastic bag.|third-puzzle,rice,bag|gear
随着|follow-continuing-eye|Footprints follow a moving object while an eye continues to watch: move along with it rather than independently.|footprints,eye|arrow
孙子|sun-tzu-strategist|A small descendant's badge stands beside a child and a strategy book: the youthful family cues are mnemonic links to the database's selected proper name Sun Tzu, not its ordinary grandson sense.|third-badge,child|book,third-halberd
弹钢琴|plucking-steel-piano|A plucked bowstring meets a steel-colored bar and a stringed lute: combine the instrument cues with the supporting piano to recall playing the piano.|third-bow,bar,third-lute|third-piano
趟|timed-wading-trip|A clock accompanies walking feet through shallow water: the time cue marks one passage, while this database selects the tāng wade reading.|clock|water,footprints
特点|special-point|A distinctive trophy stands beside a conspicuous dot: that special point is the feature that distinguishes the object.|third-trophy,third-spots|third-target
提|hand-carries-confirmed|A hand holds a hanging bag beside an is-check: the hand is carrying the load down from its grip.|hand,third-check|bag
填空|filled-vacancy|A fitting block moves toward an empty frame: fill the vacant place, picturing a job vacancy as the empty position selected by this database.|third-puzzle,third-empty|third-badge
同时|same-time|Two matching pieces stand beside one shared clock: imagine both events occurring at the same time.|third-puzzle,clock|third-check
推迟|pushed-later|A hand pushes a clock farther along the calendar: move the task to a later time and postpone it.|hand,clock|calendar
往往|repeated-route-usually|Two forward paths repeat the same direction: the action happens again and again, usually.|road,road|third-loop
卫生间|guarded-growing-room|A protective shield stands beside growing life and an enclosed gap: picture the bathroom as a room for guarding cleanliness and daily care.|third-shield,sprout,door|third-toilet
污染|dirty-dyed-water|A darkened earth patch sits beside colored threads: imagine dirty dye spilling into water and polluting it.|earth,silk|water,third-no
误会|mistaken-understanding|A broken puzzle faces a can-do check: someone thinks the pieces fit when they do not, a misunderstanding.|third-broken,third-check|question
西红柿|western-red-fruit|A westward arrow meets red silk and a round persimmon-like fruit: use the three cues as an association with the supporting red tomato.|arrow,silk,fruit|third-tomato
咸|all-salt-cues|A salt pile sits beside the entire counted group: imagine salting all the portions to connect the salty cue with this database's selected all sense.|salt|count-10
羡慕|envied-admired-prize|A reaching hand faces an admired trophy: imagine wanting the beautiful prize that someone else has, envy.|hand,third-trophy|eye
详细|complete-fine-detail|A completed grid stands beside a magnifier picking out fine marks: a detailed account covers the whole and the tiny particulars.|third-grid,third-magnifier|third-check
橡皮|oak-skin-rubber|An oak with acorns stands beside a pale skin-like sheet: associate these source cues with a rubber eraser shown nearby, without claiming a botanical origin.|third-oak,lining|third-eraser
小伙子|small-companion-child|A small bead stands beside a companion and a child: imagine the child growing into the young man who joins his companions.|count-1,person,child|man
笑话|laughing-talk|A smiling face sits beside a speaking bubble: words that make the listener laugh form a joke.|face,speech|third-surprise
信息|trusted-breath-message|A trusted envelope stands beside a breath of air: imagine the breath carrying the message's information to its listener.|envelope,steam|speech
性别|identity-separation|An identity badge meets two separate blocks: the labeled distinction supplies a symbolic mnemonic for gender, without prescribing identities or appearances.|third-badge,third-broken|third-tag
性格|identity-pattern|An identity badge stands beside a patterned grid: imagine the person's distinctive pattern of behavior as their nature or character.|third-badge,third-grid|heart
亚洲|second-continent-map|A second-place step stands beside a continent globe: the second cue is an arbitrary mnemonic handle for the proper name Asia, not a geographical ranking.|third-levels,globe|map
研究|grinding-investigation|A grinding gear stands beside a magnifier: work carefully through the evidence, investigating deeply to conduct research.|gear,third-magnifier|book
养成|raised-success|A sprout is carefully raised beside a completed check: continued care cultivates a successful habit or growth.|sprout,third-check|water
要是|wanted-condition|A desired star faces an is-check: if the wanted condition is true, imagine the next action becoming possible.|star,third-check|arrow
应聘|responding-employment|A response arrow meets a work badge: accept the employer's offer and respond by joining the job.|arrow,third-badge|gear
勇敢|brave-daring-step|A protective shield stands beside a forward step over a gap: imagine choosing to dare the difficult action with bravery.|third-shield,footprints|third-broken
优点|excellent-point|An excellence trophy stands beside a highlighted dot: point to the admirable feature that counts as a merit.|third-trophy,third-spots|third-check
幽默|quiet-silent-humor|A quiet closed book sits beside a silent mouth, but a playful toy surprises them: an invented association for the loanword humor, not a literal character translation.|book,mouth|ball,third-surprise
邮局|mail-bureau|A mailed envelope faces an office counter: bring the message to the bureau at the post office.|envelope,table|house
友好|youhao-district-name|A friendly person offers a good check beside a district map: friend and good are mnemonic handles for Youhao district, the proper-name sense selected in this database.|person,third-check|map
友谊|friendship-bond|Two friends face a connecting heart: imagine the companionship and goodwill that bind their friendship.|person,heart|person
愉快|pleasant-quick-spark|A pleasant smiling face meets a quick-moving arrow: imagine happiness arriving in a cheerful burst.|face,arrow|heart
语法|language-method|A speech bubble stands beside an ordered grid: the method arranging words into sentences is grammar.|speech,third-grid|book
原谅|spring-excuse|A source spring of water faces an accepting hand: imagine letting blame wash away at the source and excusing the person.|water,hand|heart
约会|appointed-can-meet|An appointment clock sits beside a can-do check: both people can meet at the agreed time.|clock,third-check|person
脏|internal-organs|A small anatomical model shows liver, stomach and intestines: these internal organs recall the selected zàng viscera reading, not zāng dirty.|third-organs|medical
占线|occupied-telephone-line|A fortune-telling stand sits beside a cord leading to a phone: imagine the stand occupying the line so the call cannot get through.|table,coil|phone
招聘|summoned-employment|A beckoning flag stands beside a work badge: invite applicants to come and take up employment.|flag,third-badge|speech
照|daylight-fire-dots|A bright sun stands beside several little fire-like sparks: imagine their combined illumination shining onto a page.|sun,third-spots|paper
只好|only-good-route|One narrow exit faces a good check while the other routes are blocked: there is no other option but this remaining acceptable choice.|count-1,third-check|door,third-no
质量|essential-measure|A solid core block sits beside a balance: test the object's essential substance and measure its quality.|third-weight,scale|third-check
重|thousand-village-repeat|A counted group stands for a thousand beside a village: imagine the village route repeated many times, preserving this database's chóng repeat reading rather than zhòng heavy.|count-10,third-village|third-loop
重视|weighted-view|A heavy weight sits beside an observing eye: give what you view special weight and attach importance to it.|third-weight,eye|third-target
主意|host-idea|A host's badge faces a bright idea-star: imagine the host forming a plan for the gathering.|third-badge,star|book
祝贺|well-wished-prize|A warm heart offers good wishes beside a celebratory trophy: congratulate the person on the achievement.|heart,third-trophy|speech
转|moving-literary-page|A revolving arrow carries quotations from a book into a speech bubble: imagine parading literary allusions in conversation, the zhuǎi reading selected through 转文, not ordinary turning.|third-loop|book,speech
准确|accurate-certainty|A centered target stands beside a confirming check: the result is accurate and certain, right on the mark.|third-target,third-check|third-ruler
总结|total-knotted-summary|All the counted beads meet a tied coil: gather the total and tie the main points together to sum up.|count-10,coil|book
作家|making-home-writing|A making tool sits beside a home: imagine the writer creating books in a home study, an author.|pencil,house|book
作者|making-narrator|A pencil makes written lines beside a narrator's speech bubble: the person creating and telling the work is its author.|pencil,speech|book
座位|seat-position|A chair stands beside a marked floor target: the seat belongs in this particular position.|chair,third-target|third-tag
"""


# Direction and physical-action scenes need more than an ordinary side-by-side
# comparison. These explicit exceptions position the authored object choices.
# Tuple fields: viewer x, y, scale, z, rotation radians (positive = upward turn).
PART_LAYOUTS = {
    '提醒': [(-.83,-.06,1.15,0,math.pi/2),(.78,.35,1.30,0,0)],
    '亮': [(-1.04,.83,.85,0,0),(-1.04,.12,.93,0,0),
           (.94,.18,.88,0,0),(.94,-.54,1.06,0,0)],
    '猜': [(-1.08,-.18,1.30,0,0),(.73,-.03,.80,.32,0)],
    '收入': [(-.70,-.22,1.32,0,0),(.84,-.08,1.06,0,math.pi)],
    '提前': [(-.87,-.06,1.10,0,math.pi/2),(.79,.05,1.33,.13,0)],
    '限制': [(0,-.02,1.75,-.10,0),(0,-.02,.85,.06,0)],
    '有趣': [(-.65,-.18,1.45,0,0),(.92,.13,1.20,0,0)],
    '举办': [(-.86,-.03,1.12,0,math.pi/2),(.86,-.16,1.26,0,0)],
    '脱': [(-.88,.15,1.25,0,0),(.76,.08,1.18,0,0)],
    '放松': [(-.91,.07,1.16,0,0),(.92,-.02,1.28,0,0)],
    '降低': [(.62,-.03,1.25,0,0),(-1.03,-.62,.95,0,0)],
    '提': [(-.70,.26,1.43,0,0),(.94,.10,1.10,0,0)],
    '西红柿': [(-1.35,-.10,.88,0,math.pi),(0,-.10,.90,0,0),
             (1.32,-.10,.95,0,0)],
}
SUPPORT_LAYOUTS = {
    '提醒': [(0,1.08,.53,-.45,0)],
    '亮': [(0,.65,.76,-.37,0)],
    '猜': [(-.51,1.03,.63,-.38,0),(.73,-.33,1.13,.02,0)],
    '收入': [(-.70,.13,.71,.31,0)],
    '提前': [(0,1.16,.61,-.38,0)],
    '限制': [(1.39,.91,.62,-.20,0)],
    '有趣': [(-.65,.04,.55,.30,0)],
    '举办': [(-.81,.94,.67,-.15,0)],
    '脱': [(.17,-.88,.80,.16,0)],
    '放松': [(-.72,-.71,.81,.21,0)],
    '降低': [(-.16,.94,.78,-.34,math.pi*1.20)],
    '举': [(.63,.98,.65,-.25,0)],
    '提': [(-.70,-.65,.78,.06,0)],
    '西红柿': [(0,1.00,.70,-.28,0)],
}


def _placed(p, kind, spec):
    x, y, scale, z, rotation = spec
    return p(kind, x, y, scale, z=z, rotation=rotation)


def register(add, p):
    lessons = {row['word']: row for row in json.loads(
        (Path(__file__).resolve().parents[2] / 'public/data/lessons.json').read_text())}
    rows = [line.split('|') for line in ROWS.strip().splitlines()]
    if len(rows) != 293:
        raise ValueError(f'Last completion batch must have 293 explicit words, found {len(rows)}')
    for word, slug, story, kinds, supports in rows:
        lesson = lessons[word]
        glyphs = [element['glyph'] for element in lesson['memoryElements']]
        kinds = kinds.split(',')
        if len(kinds) != len(glyphs):
            raise ValueError(f'Wrong ordered part count for {word}: {kinds} vs {glyphs}')
        n = len(kinds)
        scale = {1:1.70, 2:1.20, 3:.90, 4:.73}[n]
        width = {1:0, 2:1.72, 3:2.70, 4:3.15}[n]
        parts = [p(kind, (i-(n-1)/2)*width/max(1,n-1), -.10,
                   scale) for i, kind in enumerate(kinds)]
        if word in PART_LAYOUTS:
            if len(PART_LAYOUTS[word]) != n:
                raise ValueError('Wrong custom layout count for '+word)
            parts = [_placed(p, kind, spec) for kind, spec in zip(kinds, PART_LAYOUTS[word])]
        extras = []
        if supports:
            items = supports.split(',')
            for i, kind in enumerate(items):
                x = (i-(len(items)-1)/2) * .83
                extras.append(p(kind, x, 1.07 if i < 2 else -.98, .62,
                                z=-.38 if i < 2 else .35))
            if word in SUPPORT_LAYOUTS:
                if len(SUPPORT_LAYOUTS[word]) != len(items):
                    raise ValueError('Wrong custom support count for '+word)
                extras = [_placed(p, kind, spec) for kind, spec in zip(items, SUPPORT_LAYOUTS[word])]
        add(word, 'complete-third-'+slug, story, glyphs, parts, extras)
