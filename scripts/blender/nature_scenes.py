"""Blender-authored botanical dioramas for Hanzi Alive's 清 and 晴.

Call ``build_clear()`` or ``build_sunny()`` after clearing the scene.  Mesh
coordinates are authored in the app's x-right / y-up / z-front convention and
rotated into Blender coordinates.  Export with export_yup=True.  The models
need neither textures nor Blender-only shaders, lights, cameras, or modifiers.
"""

import math
import random

import bpy
from mathutils import Vector


TAU = math.tau


def _xyz(point):
    """App coordinates -> Blender; glTF's Y-up export reverses this rotation."""
    x, y, z = point
    return (x, -z, y)


def _material(name, color, roughness=0.68, alpha=1.0, emission=0.0):
    # Palette tuples are display/sRGB colors; Blender shader sockets and glTF
    # factors use linear values. Converting here keeps foliage richly green
    # instead of washing the palette out under the presentation lighting.
    linear_color = tuple(
        channel / 12.92 if channel <= 0.04045
        else ((channel + 0.055) / 1.055) ** 2.4
        for channel in color
    )
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    mat.diffuse_color = (*linear_color, alpha)
    shader = mat.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = (*linear_color, alpha)
    shader.inputs["Roughness"].default_value = roughness
    shader.inputs["Alpha"].default_value = alpha
    if emission:
        shader.inputs["Emission Color"].default_value = (*linear_color, 1.0)
        shader.inputs["Emission Strength"].default_value = emission
    if alpha < 1.0:
        # Blender 4.5 preview and glTF export both preserve the actual alpha.
        mat.surface_render_method = "DITHERED"
        mat.use_backface_culling = True
        mat["baseOpacity"] = alpha
    return mat


def _palette():
    return {
        "earth": _material("nature_earth_forest", (0.115, 0.185, 0.130), 0.93),
        "soil": _material("nature_soil_moss", (0.255, 0.320, 0.185), 0.91),
        "sand": _material("nature_sand_warm", (0.515, 0.480, 0.320), 0.92),
        "stone": _material("nature_stone_sage", (0.440, 0.495, 0.390), 0.82),
        "stone_light": _material("nature_stone_cream", (0.640, 0.650, 0.485), 0.85),
        "stone_dark": _material("nature_stone_forest", (0.220, 0.290, 0.225), 0.88),
        "grass_deep": _material("nature_grass_forest", (0.090, 0.290, 0.145), 0.62),
        "grass": _material("nature_grass_jade", (0.205, 0.445, 0.190), 0.60),
        "grass_light": _material("nature_grass_sage", (0.380, 0.570, 0.250), 0.66),
        "grass_tip": _material("nature_grass_new_growth", (0.500, 0.635, 0.290), 0.69),
        "water_top": _material("water_surface_clear", (0.470, 0.720, 0.645), 0.16, 0.18),
        "water_side": _material("water_edge_clear", (0.330, 0.595, 0.535), 0.21, 0.20),
        "water_light": _material("water_glints", (0.710, 0.865, 0.740), 0.29),
        "sun": _material("nature_sun_honey", (0.970, 0.645, 0.160), 0.53, emission=0.13),
        "sun_light": _material("nature_sun_apricot", (1.000, 0.810, 0.340), 0.53, emission=0.10),
        "sun_rays": _material("nature_sun_ochre", (0.900, 0.535, 0.095), 0.60, emission=0.06),
        "seed": _material("nature_meadow_seed", (0.675, 0.590, 0.275), 0.84),
    }


def _mesh(name, vertices, faces, material, smooth=True):
    data = bpy.data.meshes.new(name)
    data.from_pydata([_xyz(vertex) for vertex in vertices], [], faces)
    data.materials.append(material)
    data.update()
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    for poly in data.polygons:
        poly.use_smooth = smooth
    return obj


def _anchor(name, location, label, glyph):
    obj = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(obj)
    obj.location = _xyz(location)
    obj.empty_display_type = "SPHERE"
    obj.empty_display_size = 0.055
    obj["label"] = label
    obj["glyph"] = glyph
    return obj


def _pebble(name, location, scale, material, seed=0, segments=24, rings=12):
    """A gently weathered pebble, with a smooth silhouette and unequal lobes."""
    rng = random.Random(seed)
    phase = rng.uniform(0, TAU)
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=segments, ring_count=rings, radius=1.0, location=_xyz(location)
    )
    obj = bpy.context.object
    obj.name = name
    for vertex in obj.data.vertices:
        # Sphere's local axes are Blender's axes: x-right, y-back, z-up.
        x, back, up = vertex.co
        theta = math.atan2(back, x)
        shape = 1.0 + 0.055 * math.sin(3 * theta + phase) * (1.0 - up * up)
        shape += 0.028 * math.cos(5 * theta - phase) * (1.0 - up * up)
        vertex.co.x = x * scale[0] * shape
        vertex.co.y = back * scale[2] * shape
        vertex.co.z = up * scale[1] * (1.0 + 0.065 * math.sin(theta + phase))
    obj.data.materials.append(material)
    for poly in obj.data.polygons:
        poly.use_smooth = True
    return obj


def _tube(name, points, radius, material, sides=7, cyclic=False):
    """Create a rounded stem/glint/ray directly as triangles and quads."""
    points = [Vector(point) for point in points]
    vertices = []
    faces = []
    count = len(points)
    for index, point in enumerate(points):
        before = points[index - 1] if index or cyclic else points[0]
        after = points[(index + 1) % count] if index < count - 1 or cyclic else points[-1]
        tangent = (after - before).normalized()
        reference = Vector((0, 1, 0))
        if abs(tangent.dot(reference)) > 0.9:
            reference = Vector((0, 0, 1))
        normal = tangent.cross(reference).normalized()
        binormal = tangent.cross(normal).normalized()
        # Closed tubes retain their width; open tubes end with soft point caps.
        endpoint_scale = 0.42 if not cyclic and index in (0, count - 1) else 1.0
        for side in range(sides):
            angle = TAU * side / sides
            vertex = point + radius * endpoint_scale * (
                math.cos(angle) * normal + math.sin(angle) * binormal
            )
            vertices.append(tuple(vertex))
    for ring in range(count if cyclic else count - 1):
        following = (ring + 1) % count
        for side in range(sides):
            nxt = (side + 1) % sides
            faces.append((ring * sides + side, ring * sides + nxt,
                          following * sides + nxt, following * sides + side))
    if not cyclic:
        faces.extend((tuple(reversed(range(sides))),
                      tuple((count - 1) * sides + side for side in range(sides))))
    return _mesh(name, vertices, faces, material)


def _blade(name, root, height, width, direction, lean, material, twist=0.0):
    """A curved, folded leaf with real thickness, a central ridge and fine tip."""
    steps = 11
    vertices = []
    faces = []
    rx, ry, rz = root
    for level in range(steps + 1):
        t = level / steps
        heading = direction + twist * t
        # Stronger final bend gives organic arcing leaves, not straight cones.
        outward = lean * (0.32 * t + 0.68 * t * t)
        center = Vector((rx + math.cos(heading) * outward,
                         ry + height * (t - 0.10 * t ** 3),
                         rz + math.sin(heading) * outward))
        sideways = Vector((-math.sin(heading), 0, math.cos(heading)))
        tangent = Vector((math.cos(heading) * lean * (0.32 + 1.36 * t),
                          height * (1.0 - 0.30 * t * t),
                          math.sin(heading) * lean * (0.32 + 1.36 * t))).normalized()
        normal = tangent.cross(sideways).normalized()
        leaf_width = width * (math.sin(math.pi * (0.065 + 0.935 * t)) ** 0.72)
        leaf_width = max(0.002, leaf_width)
        thickness = 0.004 * (1.0 - 0.65 * t)
        ridge = leaf_width * 0.25
        # Triangular cross section on each side, folded along a central vein.
        for side in (-1, 0, 1):
            point = center + sideways * (side * leaf_width)
            point += normal * (ridge * (1.0 - abs(side)) + thickness)
            vertices.append(tuple(point))
        for side in (-1, 0, 1):
            point = center + sideways * (side * leaf_width)
            point += normal * (ridge * (1.0 - abs(side)) - thickness)
            vertices.append(tuple(point))
    for level in range(steps):
        a, b = level * 6, (level + 1) * 6
        for strip in range(2):
            faces.append((a + strip, b + strip, b + strip + 1, a + strip + 1))
            faces.append((a + strip + 4, b + strip + 4, b + strip + 3, a + strip + 3))
        faces.append((a, a + 3, b + 3, b))
        faces.append((a + 2, b + 2, b + 5, a + 5))
    faces.append((0, 1, 2, 5, 4, 3))
    end = steps * 6
    faces.append((end + 3, end + 4, end + 5, end + 2, end + 1, end))
    return _mesh(name, vertices, faces, material)


def _meadow(palette):
    """Identical planting layout makes 青 recognizable across both characters."""
    rng = random.Random(719)
    _pebble("Meadow_foundation", (0, -1.225, 0), (2.15, 0.275, 1.19),
            palette["earth"], 70, 64, 20)
    _pebble("Meadow_mossy_top", (0, -1.016, 0), (2.035, 0.125, 1.105),
            palette["soil"], 71, 64, 16)

    # Warm sand breaks up the green carpet and leaves a clear foreground path.
    for index, (x, z, rx, rz) in enumerate([
        (-1.22, 0.53, 0.57, 0.29), (-0.42, 0.68, 0.55, 0.24),
        (0.40, 0.70, 0.44, 0.20), (1.15, 0.49, 0.43, 0.25),
    ]):
        _pebble("Sand_patch_%02d" % index, (x, -0.936, z),
                (rx, 0.034, rz), palette["sand"], 85 + index, 24, 10)

    # Several full tufts are more readable than hundreds of thin identical spikes.
    centers = [
        (-1.43, -0.27, 0.83), (-0.96, -0.59, 0.79), (-0.41, -0.63, 0.94),
        (0.19, -0.68, 0.88), (0.77, -0.52, 0.95), (1.35, -0.25, 0.81),
        (-1.64, 0.08, 0.69), (-1.04, 0.07, 0.83), (-0.48, -0.04, 0.96),
        (0.16, -0.13, 0.90), (0.69, 0.01, 0.95), (1.27, 0.12, 0.75),
        (-1.39, 0.43, 0.65), (-0.67, 0.40, 0.76), (0.08, 0.45, 0.83),
        (0.65, 0.43, 0.74), (1.44, 0.43, 0.62), (-0.29, 0.78, 0.58),
    ]
    greens = [palette["grass_deep"], palette["grass"],
              palette["grass_light"], palette["grass_tip"]]
    for tuft, (x, z, vigor) in enumerate(centers):
        for leaf in range(10):
            direction = TAU * leaf / 10 + rng.uniform(-0.25, 0.25)
            height = vigor * rng.uniform(0.48, 0.77)
            lean = rng.uniform(0.18, 0.34)
            material = greens[(leaf + tuft) % len(greens)]
            _blade("Grass_%02d_%02d" % (tuft, leaf),
                   (x + rng.uniform(-0.052, 0.052), -0.925, z + rng.uniform(-0.052, 0.052)),
                   height, rng.uniform(0.045, 0.070), direction, lean, material,
                   rng.uniform(-0.21, 0.21))
        # One small, young upright shoot adds rhythm inside each curved tuft.
        _blade("Grass_heart_%02d" % tuft, (x, -0.922, z), vigor * 0.82,
               0.035, rng.uniform(0, TAU), 0.07, palette["grass_tip"])

    # Rounded stones, kept mainly on the path and pond edges so the grass reads.
    for index, (x, z, size) in enumerate([
        (-1.68, 0.45, 0.18), (-1.16, 0.62, 0.21), (-0.96, 0.78, 0.12),
        (-0.55, 0.78, 0.17), (0.26, 0.79, 0.14), (0.80, 0.70, 0.24),
        (1.15, 0.54, 0.13), (1.72, 0.07, 0.24), (-1.83, -0.07, 0.15),
        (-1.30, -0.64, 0.18), (1.15, -0.65, 0.17), (0.43, -0.82, 0.13),
        (-0.38, 0.20, 0.13), (0.97, -0.13, 0.13), (-0.83, -0.22, 0.10),
    ]):
        material = palette[["stone", "stone_light", "stone_dark"][index % 3]]
        _pebble("River_stone_%02d" % index, (x, -0.918 + size * 0.31, z),
                (size * 1.25, size * 0.52, size * 0.84), material, index + 100)
        if index % 3 == 0:
            # A smaller neighboring pebble makes deliberate natural clusters.
            _pebble("Small_stone_%02d" % index,
                    (x + size * 1.08, -0.903, z + size * 0.44),
                    (size * 0.36, size * 0.22, size * 0.31),
                    palette["stone_light"], index + 150, 16, 8)


def _pond(palette):
    count = 96
    radius_x, radius_z = 2.13, 1.18
    level = -0.100
    vertices = [(0.0, level, 0.0)]
    for index in range(count):
        angle = TAU * index / count
        ripple = 1.0 + 0.018 * math.sin(3 * angle) + 0.01 * math.sin(5 * angle)
        vertices.append((radius_x * math.cos(angle) * ripple, level,
                         radius_z * math.sin(angle) * ripple))
    faces = [(0, (index + 1) % count + 1, index + 1) for index in range(count)]
    _mesh("Clear_water_surface", vertices, faces, palette["water_top"], False)

    # An open-bottom skin gives water physical depth without a second surface
    # obscuring the leaves.  A slight taper meets the riverbed's rounded edge.
    vertices, faces = [], []
    for y, radius_scale in [(level, 1.0), (-0.88, 0.975), (-1.045, 0.925)]:
        for index in range(count):
            angle = TAU * index / count
            ripple = 1.0 + 0.018 * math.sin(3 * angle) + 0.01 * math.sin(5 * angle)
            vertices.append((radius_x * radius_scale * math.cos(angle) * ripple, y,
                             radius_z * radius_scale * math.sin(angle) * ripple))
    for row in range(2):
        for index in range(count):
            nxt = (index + 1) % count
            faces.append((row * count + index, row * count + nxt,
                          (row + 1) * count + nxt, (row + 1) * count + index))
    _mesh("Clear_water_soft_edge", vertices, faces, palette["water_side"])

    # A few small reflected strokes clarify the transparent water at a glance.
    for index, (cx, cz, rx, rz, start, span) in enumerate([
        (-0.93, 0.65, 0.49, 0.12, 0.13, 1.21),
        (1.10, -0.18, 0.44, 0.16, -0.53, 1.17),
        (-0.64, -0.64, 0.48, 0.14, 2.07, 0.98),
        (0.60, 0.63, 0.37, 0.10, 0.11, 0.86),
    ]):
        points = [(cx + rx * math.cos(start + span * step / 18), level + 0.008,
                   cz + rz * math.sin(start + span * step / 18)) for step in range(19)]
        _tube("Water_glint_%02d" % index, points, 0.009,
              palette["water_light"], sides=6)

    # One restrained edge arc indicates a meniscus without outlining the entire
    # basin.  The foliage and stones remain visible through the actual alpha.
    points = []
    for step in range(35):
        angle = 0.45 + 1.35 * step / 34
        ripple = 1.0 + 0.018 * math.sin(3 * angle) + 0.01 * math.sin(5 * angle)
        points.append((radius_x * math.cos(angle) * ripple, level + 0.005,
                       radius_z * math.sin(angle) * ripple))
    _tube("Water_meniscus_highlight", points, 0.012, palette["water_light"], sides=6)


def _sun(palette):
    center = Vector((0.38, 1.11, -0.56))
    _pebble("Sun_sculpted_body", center, (0.535, 0.535, 0.255),
            palette["sun"], 311, 48, 24)
    # A slightly inset apricot face produces a gentle hand-built ceramic rim.
    _pebble("Sun_warm_face", (center.x - 0.018, center.y + 0.018, center.z + 0.168),
            (0.468, 0.468, 0.110), palette["sun_light"], 312, 48, 20)
    for index in range(12):
        angle = TAU * index / 12 + math.pi / 12
        direction = Vector((math.cos(angle), math.sin(angle), 0))
        start_radius = 0.685
        end_radius = 0.868 if index % 2 == 0 else 0.812
        points = [tuple(center + direction * (start_radius + (end_radius - start_radius) * t))
                  for t in (0, 0.12, 0.35, 0.65, 0.88, 1)]
        _tube("Sun_ray_%02d" % index, points,
              0.032 if index % 2 == 0 else 0.026,
              palette["sun_rays" if index % 2 == 0 else "sun"], sides=10)


def build_clear():
    """Build 清: clear water lets the repeated green plants remain visible."""
    palette = _palette()
    _meadow(palette)
    _pond(palette)
    _anchor("anchor_water", (-1.54, -0.085, 0.57), "Clear water", "氵")
    _anchor("anchor_green", (0.68, -0.24, 0.05), "Green grass", "青")
    return {
        "title": "Clear water, visible green",
        "anchors": {"anchor_water": "氵", "anchor_green": "青"},
        "design": "Transparent pale-jade pond above a detailed riverbed and curved grass leaves.",
    }


def build_sunny():
    """Build 晴: the same green plants under a warm sculptural sun."""
    palette = _palette()
    _meadow(palette)
    _sun(palette)
    _anchor("anchor_sun", (0.38, 1.11, -0.285), "Sun", "日")
    _anchor("anchor_green", (0.68, -0.24, 0.05), "Green grass", "青")
    return {
        "title": "Sun over the same green meadow",
        "anchors": {"anchor_sun": "日", "anchor_green": "青"},
        "design": "An apricot-and-ochre ceramic sun over the identical botanical grass motif.",
    }
