"""Hand-built Blender expansions that keep the established visual vocabulary.

All public builders work in a fresh scene and return metadata for the shared
exporter.  Anchors are ordered like the lesson's parts.  The broadleaf trees and
curved meadow are reused directly from the three illustrated demo scenes.
These are memory stories, not claims about a character's historical origin.
"""

import math
import random

import bpy
from mathutils import Matrix, Vector

from rest_scene import build_rest, material, oval, tube, leaf, anchor, v
from nature_scenes import _palette, _meadow, _pebble, _blade, _mesh


def _label(index, pos, glyph, label):
    obj = anchor("anchor_part_%d" % index, pos)
    obj["glyph"] = glyph
    obj["label"] = label


def _tree_prototype():
    """Extract only the established tree, preserving its exact authored form."""
    build_rest()
    tree_prefixes = (
        "Sculpted trunk", "Arching branch", "Exposed root",
        "Fine bark ridge", "Canopy leaf",
    )
    keep = []
    for obj in list(bpy.context.scene.objects):
        if obj.name.startswith(tree_prefixes):
            keep.append(obj)
        else:
            bpy.data.objects.remove(obj, do_unlink=True)
    return keep


def _grove(specs):
    """Place copies by trunk base, leaving the shared tree silhouette intact."""
    prototype = _tree_prototype()
    for index, (x, z, size, turn) in enumerate(specs):
        placement = (
            Matrix.Translation(v((x, -1.58, z)))
            @ Matrix.Rotation(turn, 4, "Z")
            @ Matrix.Scale(size, 4)
            @ Matrix.Translation(-v((.67, -1.80, 0)))
        )
        for source in prototype:
            obj = source.copy()
            # Shared mesh/curve data keeps the native file efficient and makes
            # edits to the repeated tree vocabulary consistent across a grove.
            obj.name = "Tree_%d / %s" % (index + 1, source.name)
            bpy.context.collection.objects.link(obj)
            obj.matrix_world = placement @ source.matrix_world
    for source in prototype:
        bpy.data.objects.remove(source, do_unlink=True)

    colors = {key: material("Grove / " + key, color) for key, color in [
        ("soil", "#514932"), ("moss", "#577348"),
        ("stone", "#9e9c7d"), ("fern", "#679052"),
        ("fern_dark", "#3c6f46"), ("path", "#9b8b63"),
    ]}
    oval("Grove sculpted earth", (0, -1.78, 0), (2.48, .24, 1.35), colors["soil"], 48, 16)
    oval("Grove moss carpet", (0, -1.59, 0), (2.40, .10, 1.28), colors["moss"], 48, 12)
    # A curved, stepping-stone clearing keeps separate trunks visible below
    # the overlapping canopy. Ferns hug the edge instead of masking the roots.
    for index, (x, z, radius) in enumerate([
        (-.23, 1.12, .28), (-.08, .80, .24), (.05, .53, .20), (.14, .28, .16),
    ]):
        oval("Woodland stepping stone %d" % index, (x, -1.475, z),
             (radius, .045, radius * .65), colors["path"], 20, 10)
    rng = random.Random(943)
    for tuft, (x, z) in enumerate([(-1.90, .48), (1.85, .58), (-1.73, -.66), (1.75, -.55), (.80, 1.03)]):
        for blade in range(7):
            angle = blade * math.tau / 7 + .3
            end = (x + math.cos(angle) * .25,
                   -1.12 + rng.uniform(-.12, .12), z + math.sin(angle) * .23)
            leaf("Grove fern %d %d" % (tuft, blade), (x, -1.51, z), end,
                 .055, colors["fern" if blade % 2 else "fern_dark"], .035)
    for index, (x, z) in enumerate([(-2.02, .05), (2.02, .15), (-1.65, .92), (1.46, .97), (.61, -.95)]):
        oval("Grove pebble %d" % index, (x, -1.49, z),
             (.14, .07, .10), colors["stone"], 16, 8)


def build_woods():
    """林: two recognizably identical trees become a little woodland."""
    _grove([(-.99, .02, .76, -.12), (1.02, -.17, .76, .16)])
    _label(0, (-.99, -.29, .24), "木", "Tree")
    _label(1, (1.02, -.29, .07), "木", "Tree")
    return {
        "title": "One tree finds another",
        "anchors": {"anchor_part_0": "木", "anchor_part_1": "木"},
        "design": "Two copies of the original broadleaf shade tree stand side by side on a mossy island, beside a small stepping-stone clearing.",
        "sharedMotifs": ["rest / broadleaf tree"],
    }


def build_forest():
    """森: a rear tree and two foreground trees create a layered forest."""
    _grove([(0, -.52, .89, .04), (-1.15, .28, .67, -.26), (1.12, .35, .67, .25)])
    # The top tree is first, matching 森's top / lower-left / lower-right order.
    _label(0, (0, .82, -.27), "木", "Tree")
    _label(1, (-1.15, -.41, .49), "木", "Tree")
    _label(2, (1.12, -.41, .56), "木", "Tree")
    return {
        "title": "Three trees deepen the woods",
        "anchors": {"anchor_part_0": "木", "anchor_part_1": "木", "anchor_part_2": "木"},
        "design": "Three copies of the established broadleaf tree form a layered forest, with a tall tree behind two lower trees and a path between the trunks.",
        "sharedMotifs": ["rest / broadleaf tree", "woods / woodland clearing"],
    }


def _heart(position, size, mat):
    """A plump, fully closed heart sculpture with rounded front and back."""
    segments = 96
    outline = []
    for index in range(segments):
        angle = math.tau * index / segments
        x = 16 * math.sin(angle) ** 3 / 17
        y = (13 * math.cos(angle) - 5 * math.cos(2 * angle)
             - 2 * math.cos(3 * angle) - math.cos(4 * angle)) / 17
        outline.append((x, y))
    vertices, faces = [], []
    # The boundary is shared by both hemispheres. Each interior ring narrows
    # smoothly while gaining depth, avoiding flat cutout faces.
    px, py, pz = position
    vertices.extend((px + x * size, py + y * size, pz) for x, y in outline)
    for side in (-1, 1):
        previous = 0
        for radius in (.975, .90, .73, .49, .22):
            base = len(vertices)
            depth = side * .31 * math.sqrt(1 - radius * radius) * size
            vertices.extend((px + x * radius * size,
                             py + y * radius * size, pz + depth) for x, y in outline)
            for index in range(segments):
                nxt = (index + 1) % segments
                face = (previous + index, previous + nxt, base + nxt, base + index)
                faces.append(face if side == 1 else tuple(reversed(face)))
            previous = base
        center = len(vertices)
        vertices.append((px, py, pz + side * .31 * size))
        for index in range(segments):
            face = (previous + index, previous + (index + 1) % segments, center)
            faces.append(face if side == 1 else tuple(reversed(face)))
    # Parametric outline runs clockwise viewed from the front.
    faces = [tuple(reversed(face)) for face in faces]
    obj = _mesh("Heart / smooth terracotta sculpture", vertices, faces, mat)
    soften = obj.modifiers.new("Soft sculpted heart lobes", "SUBSURF")
    soften.levels = 1
    soften.render_levels = 1
    return obj


def build_emotion():
    """情: a heart settles into the identical green meadow used for 清/晴."""
    palette = _palette()
    _meadow(palette)
    coral = material("Feeling / warm terracotta", "#bf6555", .67)
    soft_coral = material("Feeling / pale terracotta", "#d99476", .75)
    _heart((-.31, .45, .12), .92, coral)
    # Small companion forms make the centerpiece feel sheltered by the plants.
    # They are sculptures, not detached character glyphs or literal anatomy.
    _heart((1.27, -.27, .53), .22, soft_coral)
    _heart((-1.32, -.30, .34), .16, coral)
    for index, (x, z, direction) in enumerate([(-.99, .11, 2.70), (.45, -.12, .25)]):
        _blade("Feeling / sheltering leaf %d" % index, (x, -.925, z),
               1.21, .075, direction, .27, palette["grass"], .18)
    _label(0, (-.62, .72, .44), "忄", "Heart")
    _label(1, (1.08, -.31, .04), "青", "Green grass")
    return {
        "title": "Let the heart feel",
        "anchors": {"anchor_part_0": "忄", "anchor_part_1": "青"},
        "design": "A rounded terracotta heart rests among the same curved green plants seen in 清 and 晴, sheltered by leaves with two small companion hearts.",
        "sharedMotifs": ["clear / green meadow", "sunny / green meadow"],
    }


def _speech_bubble(mat):
    """Rounded ceramic speech sculpture; no writing or caption texture."""
    outline = [(-1.23, 1.37), (1.20, 1.37)]
    # Soft corners are sampled arcs; the small downward tail clearly identifies
    # a speech bubble even when the viewer orbits around its solid thickness.
    for cx, cy, begin, end in [(1.20, 1.13, math.pi / 2, 0),
                              (1.20, .54, 0, -math.pi / 2)]:
        outline.extend((cx + .24 * math.cos(begin + (end - begin) * k / 8),
                        cy + .24 * math.sin(begin + (end - begin) * k / 8)) for k in range(1, 9))
    outline.extend([(-.28, .30), (-.82, -.10), (-.67, .30), (-1.23, .30)])
    for cx, cy, begin, end in [(-1.23, .54, -math.pi / 2, -math.pi),
                              (-1.23, 1.13, -math.pi, -math.pi * 1.5)]:
        outline.extend((cx + .24 * math.cos(begin + (end - begin) * k / 8),
                        cy + .24 * math.sin(begin + (end - begin) * k / 8)) for k in range(1, 9))
    curve = bpy.data.curves.new("Invitation / rounded speech outline", "CURVE")
    curve.dimensions = "2D"
    curve.fill_mode = "BOTH"
    curve.resolution_u = 1
    curve.extrude = .09
    curve.bevel_depth = .065
    curve.bevel_resolution = 4
    spline = curve.splines.new("POLY")
    spline.points.add(len(outline) - 1)
    for point, (x, y) in zip(spline.points, outline):
        point.co = (x, y, 0, 1)
    spline.use_cyclic_u = True
    obj = bpy.data.objects.new("Invitation / ceramic speech bubble", curve)
    bpy.context.collection.objects.link(obj)
    obj.rotation_euler[0] = math.pi / 2
    obj.location = v((0, .13, -.16))
    curve.materials.append(mat)


def build_invite():
    """请: spoken welcome above a detailed, inviting green garden."""
    palette = _palette()
    _meadow(palette)
    cream = material("Invitation / warm porcelain", "#e2d7b6", .69)
    gold = material("Invitation / honey accent", "#c28c40", .66)
    _speech_bubble(cream)
    for index in range(3):
        _pebble("Invitation / spoken dot %d" % index,
                (-.49 + .49 * index, .96, .036), (.087, .087, .043),
                palette["grass_deep"], 600 + index, 24, 12)
    # A low, curved garden path welcomes the viewer into the scene itself.
    for index, (x, z, size) in enumerate([(-.12, 1.00, .18), (-.02, .73, .155), (.08, .51, .13)]):
        _pebble("Invitation / welcoming path %d" % index, (x, -.887, z),
                (size, .042, size * .60), palette["stone_light"], 610 + index, 24, 10)
    # Quiet gold blossoms reinforce a tended garden without changing 青's
    # established green leaves into a different symbol.
    for index, (x, z) in enumerate([(-1.47, -.25), (1.30, -.25)]):
        tube("Invitation / flower stem %d" % index,
             [(x, -.91, z), (x - .03, -.44, z), (x + .02, -.15, z)],
             [.014, .012, .008], palette["grass_deep"], 1)
        for petal in range(5):
            angle = math.tau * petal / 5
            oval("Invitation / flower %d petal %d" % (index, petal),
                 (x + .02 + math.cos(angle) * .065, -.15 + math.sin(angle) * .065, z + .025),
                 (.057, .050, .025), gold, 16, 8)
        oval("Invitation / flower center %d" % index, (x + .02, -.15, z + .052),
             (.032, .032, .018), palette["seed"], 16, 8)
    _label(0, (-1.18, 1.01, .08), "讠", "Speech bubble")
    _label(1, (1.06, -.32, .17), "青", "Green grass")
    return {
        "title": "A green invitation",
        "anchors": {"anchor_part_0": "讠", "anchor_part_1": "青"},
        "design": "A rounded porcelain speech bubble offers a welcome above the shared green meadow, with a stepping-stone entrance and two small golden flowers.",
        "sharedMotifs": ["clear / green meadow", "sunny / green meadow"],
    }
