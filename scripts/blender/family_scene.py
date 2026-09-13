"""A warm meal for 好, authored as an explicit visual memory story.

The girl and boy are the story's characters, not a historical reconstruction
or a claim that one family arrangement defines goodness. Coordinates follow
rest_scene's x-right / y-up / z-front convention.
"""

import math

import bpy
from mathutils import Matrix

from rest_scene import anchor, finish, leaf, material, oval, tube, v


def _box(name, center, dimensions, mat, bevel=.035):
    bpy.ops.mesh.primitive_cube_add(size=1, location=v(center))
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = (dimensions[0], dimensions[2], dimensions[1])
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    rounded = obj.modifiers.new("Soft handmade edges", "BEVEL")
    rounded.width = bevel
    rounded.segments = 3
    obj.modifiers.new("Weighted corner normals", "WEIGHTED_NORMAL")
    return obj


def _head(name, center, scale, turn, adult, mats):
    before = set(bpy.context.scene.objects)
    skin = mats["skin"] if adult else mats["child_skin"]
    oval("Face", (0, 0, 0), (.245, .30, .235), skin, 32, 20)
    oval("Soft chin", (0, -.225, .043), (.145, .088, .145), skin, 24, 12)
    oval("Small nose", (0, -.008, .235), (.052, .058, .055), skin, 20, 12)
    for side in (-1, 1):
        oval("Ear", (side * .238, -.035, 0), (.049, .072, .043), skin, 20, 12)
        tube("Happy closed eye", [(side * .051, .046, .221),
                                   (side * .093, .058, .219),
                                   (side * .133, .041, .205)],
             [.006, .010, .006], mats["hair"], 2)
        tube("Gentle eyebrow", [(side * .05, .107, .210),
                                 (side * .091, .123, .207),
                                 (side * .133, .108, .192)],
             [.006, .008, .004], mats["hair"], 2)
        oval("Warm cheek", (side * .132, -.053, .202),
             (.045, .023, .011), mats["cheek"], 20, 10)
    tube("Contented smile", [(-.062, -.113, .207), (0, -.134, .221),
                              (.062, -.113, .207)],
         [.004, .007, .004], mats["smile"], 2)

    # A curved scalp patch keeps the face open, unlike a second sphere placed
    # over the whole head. The hairline is higher over the forehead.
    vertices, faces = [], []
    columns, rows = 40, 12
    for row in range(rows):
        for column in range(columns):
            phi = column * math.tau / columns
            facing = max(0, math.sin(phi))
            maximum = (1.89 if adult else 1.60) - .78 * facing ** 2
            theta = (row / (rows - 1)) * maximum
            vertices.append(v((.252 * math.sin(theta) * math.cos(phi),
                               .045 + .285 * math.cos(theta),
                               .247 * math.sin(theta) * math.sin(phi))))
    for row in range(rows - 1):
        for column in range(columns):
            a = row * columns + column
            b = row * columns + (column + 1) % columns
            faces.append((a, b, b + columns, a + columns))
    mesh = bpy.data.meshes.new("Swept hair cap")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new("Swept hair cap", mesh)
    bpy.context.collection.objects.link(obj)
    finish(obj, "Swept hair cap", mats["hair"])
    if adult:
        oval("Low gathered hair bun", (.015, -.035, -.253),
             (.166, .158, .139), mats["hair"], 28, 16)
        tube("Cloth hair tie", [(-.11, .037, -.248), (.01, .092, -.293),
                                (.13, .043, -.258)],
             [.018, .02, .014], mats["shirt_light"], 2)
        for index in range(5):
            offset = (index - 2) * .025
            tube("Swept bun strand", [(-.05 + offset, .09, -.24),
                                       (.08 + offset, .035, -.367),
                                       (.07 + offset, -.105, -.318)],
                 [.008, .012, .004], mats["hair_light"], 2)
    else:
        for index in range(3):
            tube("Child soft fringe", [(-.115 + index * .069, .255, .133),
                                        (-.076 + index * .064, .175, .204),
                                        (-.071 + index * .060, .120, .211)],
                 [.018, .025, .006], mats["hair"], 2)
    placement = Matrix.Translation(v(center)) @ Matrix.Rotation(turn, 4, "Z") @ Matrix.Scale(scale, 4)
    for obj in set(bpy.context.scene.objects) - before:
        obj.name = name + " / " + obj.name
        obj.matrix_world = placement @ obj.matrix_world


def _hand(name, center, size, mat, toward=1):
    x, y, z = center
    oval(name + " palm", center, (.09 * size, .048 * size, .071 * size), mat, 20, 12)
    for index in range(4):
        offset = (index - 1.5) * .031 * size
        tube(name + " curled finger %d" % index,
             [(x + toward * .036 * size, y, z + offset),
              (x + toward * .106 * size, y - .01 * size, z + offset),
              (x + toward * .118 * size, y - .040 * size, z + offset)],
             [.014 * size, .014 * size, .006 * size], mat, 1)
    oval(name + " thumb", (x + toward * .04 * size, y + .018 * size, z + .067 * size),
         (.039 * size, .023 * size, .020 * size), mat, 16, 10)


def _girl_head(name, center, scale, turn, mats):
    """Use the same child's face and head scale, with two short tied pigtails."""
    _head(name, center, scale, turn, False, mats)
    before = set(bpy.context.scene.objects)
    for side in (-1, 1):
        for index, (x, y, z, width, height) in enumerate([
            (.250, -.055, -.045, .083, .105),
            (.286, -.145, -.055, .078, .091),
            (.308, -.223, -.043, .063, .079),
        ]):
            oval("Girl's short pigtail %d %d" % (side, index),
                 (side * x, y, z), (width, height, .070), mats["hair"], 24, 14)
        tube("Girl's cloth hair tie %d" % side,
             [(side * .24, -.094, .014), (side * .285, -.087, .023),
              (side * .325, -.098, .010)],
             [.014, .020, .014], mats["shirt_light"], 2)
        for direction in (-1, 1):
            oval("Girl's small ribbon loop %d %d" % (side, direction),
                 (side * .283 + direction * .039, -.093, .025),
                 (.038, .023, .018), mats["shirt_light"], 20, 10)
    placement = Matrix.Translation(v(center)) @ Matrix.Rotation(turn, 4, "Z") @ Matrix.Scale(scale, 4)
    for obj in set(bpy.context.scene.objects) - before:
        obj.name = name + " / " + obj.name
        obj.matrix_world = placement @ obj.matrix_world


def _body(name, x, smaller, mats):
    size = .79 if smaller else 1
    shirt = mats["child_shirt"] if smaller else mats["shirt"]
    shirt_light = mats["child_shirt_light"] if smaller else mats["shirt_light"]
    top = -.31 if smaller else -.06
    # The seat, hips and legs physically meet, and both pairs of shoes reach
    # the floor. The child uses a slightly taller cushion at the same table.
    _box(name + " stool seat", (x, -1.14, -.12), (.68, .11, .63), mats["wood"], .065)
    for dx in (-.22, .22):
        for dz in (-.20, .20):
            tube(name + " stool leg", [(x + dx, -1.18, -.12 + dz),
                                       (x + dx * 1.1, -1.73, -.12 + dz * 1.1)],
                 [.060, .048], mats["wood_dark"], 2)
    oval(name + " seated shirt hem", (x, -1.025, -.10),
         (.29 * size, .20, .27 * size), shirt)
    tube(name + " draped shirt", [(x, -.96, -.1), (x, -.56, -.13), (x, top, -.13)],
         [.255 * size, .233 * size, .23 * size], shirt, 4)
    oval(name + " shoulder fabric", (x, top, -.13),
         (.245 * size, .145 * size, .24 * size), shirt)
    skin = mats["child_skin"] if smaller else mats["skin"]
    tube(name + " neck", [(x, top + .06, -.13), (x, top + .20, -.12)],
         [.076 * size, .067 * size], skin, 2)
    tube(name + " soft collar", [(x - .13 * size, top + .024, .05),
                                 (x, top - .045, .13 * size),
                                 (x + .13 * size, top + .024, .05)],
         [.014, .019, .014], shirt_light, 2)
    sign = -1 if x < 0 else 1
    for index, dz in enumerate((-.10, .19)):
        knee = (x + sign * (.24 if not smaller else .15), -1.16, .32 + dz)
        ankle = (knee[0], -1.61, .38 + dz)
        tube(name + " bent trouser leg %d" % index,
             [(x + sign * .045, -1.02, -.04 + dz), knee, ankle],
             [.17 * size, .135 * size, .075 * size], mats["trousers"], 3)
        oval(name + " knee fold %d" % index, knee,
             (.145 * size, .123 * size, .15 * size), mats["trousers"])
        oval(name + " soft shoe %d" % index, (ankle[0], -1.68, ankle[2] + .12),
             (.13 * size, .085, .235 * size), mats["shoe"])
        oval(name + " shoe sole %d" % index, (ankle[0], -1.742, ankle[2] + .12),
             (.132 * size, .02, .235 * size), mats["sole"], 20, 10)
        tube(name + " trouser seam %d" % index,
             [(knee[0] + sign * .09, -1.15, knee[2] + .073),
              (ankle[0] + sign * .06, -1.56, ankle[2] + .06)],
             [.006, .004], mats["trousers_light"], 1)
    for index in range(3):
        tube(name + " linen fold %d" % index,
             [(x - .12 + index * .11, -.62, .094),
              (x - .10 + index * .10, -.86, .129),
              (x - .13 + index * .12, -.95, .124)],
             [.003, .007, .003], shirt_light, 1)


def _arm(name, points, size, cloth, cuff, skin, hand_direction):
    shoulder, elbow, hand = points
    # A visible short cuff divides the rolled sleeve from the bent forearm.
    sleeve_end = tuple(elbow[i] * .86 + shoulder[i] * .14 for i in range(3))
    tube(name + " rolled sleeve", [shoulder, sleeve_end, elbow],
         [.126 * size, .111 * size, .102 * size], cloth, 3)
    tube(name + " fabric cuff", [sleeve_end, elbow],
         [.113 * size, .108 * size], cuff, 2)
    mid = tuple(elbow[i] * .5 + hand[i] * .5 for i in range(3))
    tube(name + " forearm", [elbow, mid, hand],
         [.073 * size, .060 * size, .039 * size], skin, 3)
    _hand(name, hand, size, skin, hand_direction)


def _bowl(name, center, radius, height, ceramic, broth, mats):
    # Revolved outer wall and inner well form a closed bowl with a real rim.
    profile = [(.43, 0), (.51, .10), (.59, .25), (.83, .54), (1, .95),
               (.99, 1), (.90, 1), (.80, .63), (.56, .33), (.37, .25)]
    vertices, faces = [], []
    count = 48
    x, y, z = center
    for radial, vertical in profile:
        for step in range(count):
            angle = math.tau * step / count
            vertices.append(v((x + radius * radial * math.cos(angle),
                               y + height * vertical,
                               z + radius * radial * math.sin(angle))))
    for row in range(len(profile) - 1):
        for step in range(count):
            nxt = (step + 1) % count
            faces.append((row * count + step, row * count + nxt,
                          (row + 1) * count + nxt, (row + 1) * count + step))
    faces.extend([tuple(reversed(range(count))),
                  tuple((len(profile) - 1) * count + step for step in range(count))])
    faces = [tuple(reversed(face)) for face in faces]
    mesh = bpy.data.meshes.new(name + " closed ceramic bowl")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name + " closed ceramic bowl", mesh)
    bpy.context.collection.objects.link(obj)
    finish(obj, name + " closed ceramic bowl", ceramic)
    oval(name + " warm broth", (x, y + height * .79, z),
         (radius * .81, .021, radius * .81), broth, 40, 12)
    for index, (dx, dz) in enumerate([(-.24, .18), (.27, .13), (.07, -.32)]):
        _box(name + " carrot %d" % index, (x + dx * radius, y + height * .86, z + dz * radius),
             (.047, .025, .039), mats["carrot"], .009)
        leaf(name + " herb %d" % index,
             (x + dx * radius + .026, y + height * .84, z + dz * radius),
             (x + dx * radius + .08, y + height * .91, z + dz * radius + .028),
             .018, mats["green"], .007)


def build_good():
    mats = {key: material("Good / " + key, color, rough) for key, color, rough in [
        ("floor", "#66573f", .98), ("rug", "#b69a6d", .96),
        ("rug_edge", "#867747", .97), ("wood", "#997148", .89),
        ("wood_dark", "#654b32", .94), ("wood_light", "#c0935c", .90),
        ("skin", "#d6a775", .72), ("child_skin", "#dfb487", .73),
        ("cheek", "#c98d78", .79), ("smile", "#985d49", .83),
        ("shirt", "#bd6742", .91), ("shirt_light", "#d38755", .89),
        ("child_shirt", "#5c8790", .90), ("child_shirt_light", "#8dabb0", .91),
        ("trousers", "#455e6c", .93), ("trousers_light", "#637785", .94),
        ("hair", "#353a2d", .84), ("hair_light", "#505242", .88),
        ("shoe", "#4b4b3b", .91), ("sole", "#c1b699", .96),
        ("ceramic", "#c7d4b6", .56), ("cream", "#e6d7b5", .73),
        ("broth", "#b78336", .34), ("carrot", "#d88243", .78),
        ("green", "#57854a", .87), ("steam", "#d4d5bd", .90),
    ]}
    steam = mats["steam"]
    steam.node_tree.nodes["Principled BSDF"].inputs["Alpha"].default_value = .35
    steam.diffuse_color = (*steam.diffuse_color[:3], .35)
    steam.surface_render_method = "DITHERED"
    steam["baseOpacity"] = .35
    oval("Home / rounded floor island", (0, -1.88, .13), (2.25, .16, 1.31), mats["floor"], 48, 16)
    oval("Home / woven circular mat", (0, -1.765, .15), (2.05, .036, 1.17), mats["rug"], 48, 12)
    for index in range(3):
        rx, rz = 1.78 + index * .078, .98 + index * .054
        points = [(rx * math.cos(step * math.tau / 64), -1.73,
                   .15 + rz * math.sin(step * math.tau / 64)) for step in range(65)]
        tube("Home / woven border %d" % index, points, [.007] * len(points), mats["rug_edge"], 1)

    girl_mats = {**mats, "child_shirt": mats["shirt"],
                 "child_shirt_light": mats["shirt_light"]}
    _body("Girl", -1.20, True, girl_mats)
    _body("Boy", 1.20, True, mats)
    _girl_head("Girl", (-1.18, .08, -.08), .91, .43, mats)
    _head("Boy", (1.16, .08, -.08), .91, -.46, False, mats)
    # Table edge remains below their hands, so the act of sharing a meal reads
    # from the initial camera and continues to make sense when rotated.
    _box("Meal / low wooden table", (0, -.675, .34), (1.96, .145, 1.22), mats["wood"], .07)
    for x in (-.77, .77):
        for z in (-.09, .77):
            _box("Meal / table leg", (x, -1.175, z), (.125, .89, .125), mats["wood_dark"], .025)
    for index in range(4):
        z = -.12 + index * .25
        tube("Meal / subtle wood grain %d" % index,
             [(-.82, -.598, z), (-.23, -.596, z + .018), (.42, -.596, z - .012), (.84, -.598, z)],
             [.002, .004, .003, .002], mats["wood_light"], 1)
    _bowl("Girl's meal", (-.55, -.598, .48), .23, .20, mats["ceramic"], mats["broth"], mats)
    _bowl("Boy's meal", (.57, -.598, .46), .23, .20, mats["ceramic"], mats["broth"], mats)
    # A plate in reach of both diners makes the shared meal concrete.
    oval("Meal / shared serving plate", (.01, -.567, .08), (.28, .036, .20), mats["cream"], 32, 12)
    for index, (x, z) in enumerate([(-.11, .04), (.10, .03), (0, .17)]):
        oval("Meal / steamed bun %d" % index, (x, -.478, z),
             (.104, .084, .086), mats["cream"], 24, 16)
        for ridge in range(3):
            tube("Meal / bun fold %d %d" % (index, ridge),
                 [(x - .063 + ridge * .042, -.428, z + .038),
                  (x - .051 + ridge * .036, -.403, z + .002),
                  (x - .037 + ridge * .027, -.425, z - .039)],
                 [.003, .005, .002], mats["sole"], 1)

    _arm("Girl near arm", [(-1.22, -.31, .045), (-1.19, -.61, .34), (-.66, -.33, .60)],
         .79, mats["shirt"], mats["shirt_light"], mats["child_skin"], 1)
    _arm("Girl sharing arm", [(-1.06, -.30, -.23), (-.88, -.56, -.18), (-.35, -.35, .05)],
         .79, mats["shirt"], mats["shirt_light"], mats["child_skin"], 1)
    _arm("Boy cupping arm", [(1.23, -.31, .045), (1.16, -.65, .34), (.77, -.43, .57)],
         .79, mats["child_shirt"], mats["child_shirt_light"], mats["child_skin"], -1)
    _arm("Boy tasting arm", [(1.06, -.30, -.23), (.80, -.49, -.14), (.91, -.16, .20)],
         .79, mats["child_shirt"], mats["child_shirt_light"], mats["child_skin"], 1)
    tube("Meal / girl's spoon handle", [(-.59, -.337, .607), (-.45, -.402, .52)],
         [.013, .011], mats["wood_dark"], 2)
    oval("Meal / girl's spoon bowl", (-.43, -.414, .508),
         (.047, .018, .064), mats["wood_dark"], 20, 10)
    tube("Meal / boy's spoon handle", [(.96, -.166, .21), (1.04, -.050, .247)],
         [.012, .010], mats["wood_dark"], 2)
    oval("Meal / boy's spoon bowl", (1.057, -.025, .258),
         (.040, .016, .050), mats["wood_dark"], 20, 10)
    for index, x in enumerate((-.60, -.42, .52)):
        tube("Meal / rising steam %d" % index,
             [(x, -.37, .35), (x + .030, -.23, .32),
              (x - .025, -.06, .30), (x + .014, .065, .28)],
             [.006, .010, .008, .001], steam, 2)
    girl = anchor("anchor_part_0", (-1.35, .0, .18))
    girl["glyph"] = "女"; girl["label"] = "Girl"
    boy = anchor("anchor_part_1", (1.32, .0, .19))
    boy["glyph"] = "子"; boy["label"] = "Boy"
    # Center the whole meal in the same fixed camera used by the other lessons.
    # Anchors move with the physical people, so labels remain attached.
    for obj in bpy.context.scene.objects:
        obj.location += v((0, .58, 0))
    return {
        "title": "A good meal together",
        "anchors": {"anchor_part_0": "女", "anchor_part_1": "子"},
        "design": "A smiling girl and boy of similar child-sized proportions sit at a low wooden table and share warm soup and steamed buns. The girl has short tied pigtails and coral clothing; the boy has a soft fringe and blue clothing. Sculpted faces, draped clothes, bent arms, little spoons and rising steam make the memory story tangible.",
        "story": "A girl and a boy share a warm family meal and both declare it good.",
        "interpretation": "An invented learning mnemonic; not an etymological reconstruction or a universal claim about family and goodness.",
    }
