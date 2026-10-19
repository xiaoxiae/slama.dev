# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = ["build123d==0.13.*", "numpy", "scipy"]
# ///
# HDZero Nano 90 V2 camera mount for the DeepSpace Seeker 3 front side plates, by Tomáš Sláma (slama.dev).
# Three parts, all 95A TPU: a cradle between the plates, plus an outer piece on each plate. Print the cradle
# front face down, the outer pieces flat side down.
# Run: `uv run <this file>`; STLs land in out/. Change the constants in
# the "tweak these" block and rerun; the asserts say when a combination doesn't fit.
#
# Frame: X forward, Y left, Z up, origin = centre of the round 4.75 mm plate hole, Y = 0 midway between the plates.
# PROFILE is the plate's side outline, its three holes and the rim recess, traced from a 3D scan.
# Both parts' outlines are the convex hull of the three plate holes grown by a stroke.
# Cradle: a shell around the camera housing, open at the back, with a lens hole at the front; the side screws set
# the camera's position and tilt. Outer piece: sits in the rim recess on the outside of the plate, plugs through the
# three holes into the cradle's sockets; an M2 through the triangle plug (the spacer) goes into the camera's side
# hole, the tilt pivot.
# The screw point is fixed, so the outer pieces are the same for every uptilt: only the cradle changes.
import math
from pathlib import Path

import numpy as np
from build123d import *
from scipy.spatial import ConvexHull

# --- tweak these ---
UPTILT = (
    30  # deg, camera vs level; the front-face overhang assert limits it to about 20..45
)
SIDE_CLEAR = 0.1  # per side, cradle vs plates
CAM_CLEAR = 0.1  # per side, camera pocket
PLUG_CLEAR = 0.15  # per side, plugs vs plate holes; <= 0.2 (with SCREW_D 2.2), see the plug wall assert
WALL = 1.2  # material around the camera housing
SCREW_D = 2.2  # M2 clearance, through the outer pieces and the cradle walls; <= 2.3

# camera, measured on a Nano 90 V2 (calipers) + the HDZero V1 STEP; distances from the side-hole axis
CAM_W, CAM_H = 14, 18  # housing
CAM_BACK = 8  # side hole -> back face
LENS_LEN = 14.5  # side hole -> lens tip
HOUSING_FRONT = 2.0  # side hole -> front of the housing (V1 STEP)
LENS_D = 13  # lens barrel

# --- internal: Seeker 3 plates, print details ---
GAP = 23  # free space between the side plates
STROKE = 3.0  # material around the convex hull of the plate holes
INSET = 0.3  # stay inside the plate outline
SOCKET_DEPTH = 2  # plug engagement past the 1.6 mm plate
PLATE_T = 1.6  # plate face thickness
BASE_T = 1.2  # outer piece (rim top is 2.9 above the plate)
RIM_CLEAR = 0.3  # vs the rim walls
PLUG_SHORT = 0.2  # plug tip vs socket bottom
BAR_ANGLE = -15.6  # rim top bar runs parallel to the plate's top edge (drone XZ)
BAR_MARGIN = 0.8  # outer piece top edge above the oval; the bar's traced edge is too rough to clip to
SCREW = (
    3.20,
    6.12,
)  # X, Z of the camera side-hole axis, the tilt pivot: fixed for every uptilt, at the
# edge of the triangle hole with a 0.45 mm (one line) plug wall around the bore
FRONT = (
    LENS_LEN - 2.5
)  # cradle front face, along the lens axis: flush with the camera (the +1.0 print stood 3.5 proud)
MAX_OVERHANG = 40  # deg from vertical, print orientation (front face down)
FILLET = 2  # top and bottom edges of the front face
AIR_SIDE = 1.0  # cooling: air gap around the housing, sides
AIR_TOP = 2.5  # top
AIR_BOTTOM = 1.0  # bottom: more would push the wall onto the slope, where the plate clips it short
RIB_SIDE = 5  # full-length ribs holding the housing: one around the pivot on each side,
RIB_TB = 2  # one down the middle top and bottom
NOZZLE = 0.4
# plate outline, holes and rim: lists of line/arc (three-point) edges, mm
PROFILE = {
    "plate_outline": [
        {
            "line": [
                [-7.6628517973061, 9.557186067463768],
                [-4.014291060590507, 8.077653560710388],
            ]
        },
        {
            "arc": [
                [-4.014291060590507, 8.077653560710388],
                [-3.0160461771676177, 7.348122064142796],
                [-3.2680315073613375, 6.173525272145662],
            ]
        },
        {
            "arc": [
                [-3.2680315073613375, 6.173525272145662],
                [-1.541371953094243, 5.1145226350236515],
                [0.3973306683586988, 4.498699283304277],
            ]
        },
        {
            "arc": [
                [0.3973306683586988, 4.498699283304277],
                [3.6377389756780154, 2.470619551503966],
                [4.230531339544651, -1.2808841950752967],
            ]
        },
        {
            "arc": [
                [4.230531339544651, -1.2808841950752967],
                [3.718690253692432, -7.012398626813404],
                [7.226710840877427, -11.578724632641784],
            ]
        },
        {
            "arc": [
                [7.226710840877427, -11.578724632641784],
                [8.961992184919712, -14.202347573492286],
                [8.56167230275273, -17.31851418024682],
            ]
        },
        {
            "arc": [
                [8.56167230275273, -17.31851418024682],
                [8.024380712679438, -18.907825222628187],
                [8.32245452291903, -20.566616791570002],
            ]
        },
        {
            "arc": [
                [8.32245452291903, -20.566616791570002],
                [8.921139078472716, -22.77678763013736],
                [7.911461236372231, -24.82002016352184],
            ]
        },
        {
            "line": [
                [7.911461236372231, -24.82002016352184],
                [-1.9910325676896363, -21.87903465009103],
            ]
        },
        {
            "arc": [
                [-1.9910325676896363, -21.87903465009103],
                [-6.005100655080291, -20.448932567635385],
                [-10.211939568259172, -19.831849287820184],
            ]
        },
        {
            "arc": [
                [-10.211939568259172, -19.831849287820184],
                [-11.351873109272699, -20.68712696527195],
                [-12.68538948020945, -20.184451650661583],
            ]
        },
        {
            "arc": [
                [-12.68538948020945, -20.184451650661583],
                [-15.077505893732422, -8.534036146276254],
                [-15.11461116448879, 3.359366460192189],
            ]
        },
        {
            "arc": [
                [-15.11461116448879, 3.359366460192189],
                [-12.571348123646043, 7.7213794139376475],
                [-8.95364048017888, 11.228645708711385],
            ]
        },
        {
            "arc": [
                [-8.95364048017888, 11.228645708711385],
                [-7.727029597928132, 10.799550267088668],
                [-7.6628517973061, 9.557186067463768],
            ]
        },
    ],
    "hole_triangle": [
        {
            "arc": [
                [-9.847272815194255, -7.723156951533593],
                [-9.040355888970433, -4.728198507525388],
                [-8.878387478500699, -1.6563947877409093],
            ]
        },
        {
            "arc": [
                [-8.878387478500699, -1.6563947877409093],
                [-6.364537120565341, 0.17990521135983562],
                [-3.4470764198115207, -0.9063104064371634],
            ]
        },
        {
            "arc": [
                [-3.4470764198115207, -0.9063104064371634],
                [-2.573744197489453, -3.7907059736092092],
                [-0.9083228462915806, -6.303267568967432],
            ]
        },
        {
            "arc": [
                [-0.9083228462915806, -6.303267568967432],
                [-0.4173584749596557, -7.309347845159945],
                [-0.48474256593642756, -8.425588093942848],
            ]
        },
        {
            "arc": [
                [-0.48474256593642756, -8.425588093942848],
                [-4.812847495555709, -11.573996935655469],
                [-9.784986914974507, -9.672016831931954],
            ]
        },
        {
            "arc": [
                [-9.784986914974507, -9.672016831931954],
                [-10.094846474595021, -8.729451463987145],
                [-9.847272815194255, -7.723156951533593],
            ]
        },
    ],
    "hole_oval": [
        {
            "arc": [
                [-1.3753682471230022, -17.962861434340518],
                [-3.117213971799295, -15.631751454543435],
                [-1.091173312733733, -13.51032090058504],
            ]
        },
        {
            "arc": [
                [-1.091173312733733, -13.51032090058504],
                [1.7229973245785009, -13.325623507580758],
                [4.479260197601521, -12.751942124534292],
            ]
        },
        {
            "arc": [
                [4.479260197601521, -12.751942124534292],
                [6.953323950192079, -14.423630735356427],
                [5.847111773696492, -17.197045396745484],
            ]
        },
        {
            "arc": [
                [5.847111773696492, -17.197045396745484],
                [2.298928935987534, -18.18970557451126],
                [-1.3753682471230022, -17.962861434340518],
            ]
        },
    ],
    "rim": [
        {
            "arc": [
                [2.7252156530735343, -23.003137367968513],
                [1.6740144994447248, -22.58026852498609],
                [1.2785369353675735, -21.56753258792477],
            ]
        },
        {
            "line": [
                [1.2785369353675735, -21.56753258792477],
                [3.202422708760322, -21.055880378577683],
            ]
        },
        {
            "arc": [
                [3.202422708760322, -21.055880378577683],
                [5.602210346351532, -20.543666154847774],
                [6.7898301172940805, -22.69096757667779],
            ]
        },
        {
            "arc": [
                [6.7898301172940805, -22.69096757667779],
                [6.782019871666085, -23.567179173736537],
                [5.97602238316341, -23.910946262452708],
            ]
        },
        {
            "arc": [
                [5.97602238316341, -23.910946262452708],
                [6.805522532338461, -24.5334538887356],
                [7.830970981387982, -24.37839996068563],
            ]
        },
        {
            "arc": [
                [7.830970981387982, -24.37839996068563],
                [8.021408018595771, -22.410463461421454],
                [7.398659914244417, -20.53397068797323],
            ]
        },
        {
            "arc": [
                [7.398659914244417, -20.53397068797323],
                [6.109377767687961, -20.249554316431936],
                [4.951675194801954, -19.614837152205965],
            ]
        },
        {
            "arc": [
                [4.951675194801954, -19.614837152205965],
                [3.2799611813563168, -19.73996262747729],
                [1.865613893551283, -20.639910335286437],
            ]
        },
        {
            "arc": [
                [1.865613893551283, -20.639910335286437],
                [0.1511667167183286, -20.48115249144399],
                [-1.3528017750271348, -19.64293297904353],
            ]
        },
        {
            "arc": [
                [-1.3528017750271348, -19.64293297904353],
                [-3.982762489290959, -18.64360521554712],
                [-5.467818081536848, -16.254053118311102],
            ]
        },
        {
            "arc": [
                [-5.467818081536848, -16.254053118311102],
                [-8.230625955125287, -15.641905227980896],
                [-10.821074756344956, -14.502867303126083],
            ]
        },
        {
            "arc": [
                [-10.821074756344956, -14.502867303126083],
                [-12.439845160896667, -5.8299528418210045],
                [-12.729036482266547, 2.9879965374514708],
            ]
        },
        {
            "arc": [
                [-12.729036482266547, 2.9879965374514708],
                [-11.577427019360055, 3.8097510204233136],
                [-10.168075987568733, 3.933097907407805],
            ]
        },
        {
            "line": [
                [-10.168075987568733, 3.933097907407805],
                [-6.937797026329525, 3.7214988940127807],
            ]
        },
        {
            "arc": [
                [-6.937797026329525, 3.7214988940127807],
                [-4.9180151062047806, 5.345850426377863],
                [-3.5080637202245812, 7.520723754811523],
            ]
        },
        {
            "line": [
                [-3.5080637202245812, 7.520723754811523],
                [-7.793571961737104, 8.713554374279855],
            ]
        },
        {
            "arc": [
                [-7.793571961737104, 8.713554374279855],
                [-8.386821683073622, 9.295789573147928],
                [-8.27424020372851, 10.12271347687285],
            ]
        },
        {
            "arc": [
                [-8.27424020372851, 10.12271347687285],
                [-8.181592087174952, 11.108973545749036],
                [-9.090462909255226, 11.479130424633553],
            ]
        },
        {
            "arc": [
                [-9.090462909255226, 11.479130424633553],
                [-13.859826604875265, 8.852432673694965],
                [-17.63754085963564, 4.928122510245373],
            ]
        },
        {
            "arc": [
                [-17.63754085963564, 4.928122510245373],
                [-18.019321434769275, 3.678640257651865],
                [-17.907960346119587, 2.376887203101857],
            ]
        },
        {
            "arc": [
                [-17.907960346119587, 2.376887203101857],
                [-17.507239942151863, 1.4231566898518222],
                [-17.856741560844622, 0.4494897280053336],
            ]
        },
        {
            "arc": [
                [-17.856741560844622, 0.4494897280053336],
                [-17.13212270493002, -2.1623404202391514],
                [-17.257857995406592, -4.869907565547757],
            ]
        },
        {
            "line": [
                [-17.257857995406592, -4.869907565547757],
                [-15.717695040754167, -13.415147951583775],
            ]
        },
        {
            "line": [
                [-15.717695040754167, -13.415147951583775],
                [-14.279247600884112, -17.54053680563423],
            ]
        },
        {
            "arc": [
                [-14.279247600884112, -17.54053680563423],
                [-13.520467026070826, -19.748979078675152],
                [-11.383544769390575, -20.69053550447911],
            ]
        },
        {
            "arc": [
                [-11.383544769390575, -20.69053550447911],
                [-10.611885894722043, -19.34437022708277],
                [-9.060377605797843, -19.32338446234155],
            ]
        },
        {
            "line": [
                [-9.060377605797843, -19.32338446234155],
                [-7.454520894190437, -16.764897714872312],
            ]
        },
        {
            "arc": [
                [-7.454520894190437, -16.764897714872312],
                [-5.717216030588242, -17.832104496621497],
                [-4.465840511430796, -19.441830502549443],
            ]
        },
        {
            "arc": [
                [-4.465840511430796, -19.441830502549443],
                [-3.232077793694461, -19.571275247682987],
                [-2.3575039168637133, -20.45107461099491],
            ]
        },
        {
            "arc": [
                [-2.3575039168637133, -20.45107461099491],
                [-1.4076543439959992, -20.255276889109215],
                [-0.5429445069742038, -20.694398576947957],
            ]
        },
        {
            "arc": [
                [-0.5429445069742038, -20.694398576947957],
                [0.24254685478849786, -21.167824993206995],
                [-0.18712163004382115, -21.978080659128313],
            ]
        },
        {
            "arc": [
                [-0.18712163004382115, -21.978080659128313],
                [1.1565615075904279, -22.83583692200102],
                [2.7252156530735343, -23.003137367968513],
            ]
        },
    ],
}

TILT = (
    UPTILT + BAR_ANGLE
)  # in the scan frame; the plate's top edge is level on the drone
WIDTH = GAP - 2 * SIDE_CLEAR
socket_gap = WIDTH / 2 - SOCKET_DEPTH - (CAM_W / 2 + CAM_CLEAR + AIR_SIDE)
assert socket_gap >= 2 * NOZZLE, (
    f"sockets {socket_gap:.2f} mm from the air gap: reduce CAM_W/CAM_CLEAR/AIR_SIDE"
)


def to_xz(p):  # plate coords (seen from the rim side, y up) -> drone (X, Z): rotate 180
    return (-p[0], -p[1])


def profile_face(edges):
    out = []
    for e in edges:
        if "line" in e:
            out.append(Line(*map(to_xz, e["line"])))
        else:
            out.append(ThreePointArc(*map(to_xz, e["arc"])))
    f = Face(Wire(out))
    return -f if f.normal_at().Z < 0 else f  # scanned contours can be clockwise


def hull(edges):
    return Face(Wire.make_convex_hull(edges))


def point_hull(
    edges, step=0.05
):  # Wire.make_convex_hull takes a minute here and leaves ~1500 sliver edges
    pts = [
        tuple(e.position_at(i / n))[:2]
        for e in edges
        for n in [max(2, int(e.length / step))]
        for i in range(n + 1)
    ]
    return Polygon(*map(tuple, np.array(pts)[ConvexHull(pts).vertices]), align=None)


holes = [
    profile_face(PROFILE["hole_triangle"]),
    profile_face(PROFILE["hole_oval"]),
    Circle(4.75 / 2).face(),
]
screw_wall = (
    offset(holes[0], -PLUG_CLEAR, kind=Kind.ARC)
    .face()
    .outer_wire()
    .distance_to(Vector(*SCREW))
    - SCREW_D / 2
)
assert screw_wall >= NOZZLE - 1e-3, (
    f"triangle plug wall around the M2 {screw_wall:.2f} mm: reduce SCREW_D or PLUG_CLEAR"
)

# 2D side outline in local (u = X, v = Z); camera frame = rotate TILT about the screw axis
cam2d = Pos(*SCREW) * Rot(0, 0, TILT)
shell = (
    cam2d
    * Pos((FRONT - CAM_BACK) / 2, (AIR_TOP - AIR_BOTTOM) / 2)
    * Rectangle(
        FRONT + CAM_BACK, CAM_H + 2 * CAM_CLEAR + AIR_TOP + AIR_BOTTOM + 2 * WALL
    )
)
plate = offset(profile_face(PROFILE["plate_outline"]), -INSET, kind=Kind.ARC)

stroked = offset(hull([e for h in holes for e in h.edges()]), STROKE, kind=Kind.ARC)
outline = point_hull((stroked + shell).face().outer_wire().edges()) & plate
nose = (
    cam2d
    * Pos((FRONT + HOUSING_FRONT) / 2, 0)
    * Rectangle(FRONT - HOUSING_FRONT, CAM_H + 2 * CAM_CLEAR + 2 * WALL)
)
outline += nose  # past the plates

# the nose would print as a flat overhang. Bottom: an S-curve from the lens wall at the front face to the shell
# wall at the housing front, tangent to both, then away at MAX_OVERHANG (outside the outline)
shell_bottom = -(CAM_H / 2 + CAM_CLEAR + WALL)
lens_bottom = -(LENS_D / 2 + CAM_CLEAR + WALL)  # bottom of the front face (lens wall)
half_run, half_rise = (
    (FRONT - HOUSING_FRONT) / 2,
    (lens_bottom - shell_bottom) / 2,
)  # each half of the S
s_r = (half_run**2 + half_rise**2) / (2 * half_rise)
s_steep = math.asin(half_run / s_r)  # steepest, from vertical when printed
max_oh = math.radians(MAX_OVERHANG)
assert s_steep <= max_oh, (
    f"front-face underside overhangs {math.degrees(s_steep):.0f}° > MAX_OVERHANG: "
    "the lens and housing bottoms are too far apart (UPTILT, LENS_D, CAM_H, LENS_LEN)"
)
arc1 = lambda t: (FRONT - s_r * math.sin(t), lens_bottom - s_r + s_r * math.cos(t))
arc2 = lambda t: (
    HOUSING_FRONT + s_r * math.sin(t),
    shell_bottom + s_r - s_r * math.cos(t),
)
s_end = (HOUSING_FRONT, shell_bottom)
far = (s_end[0] - 100 * math.cos(max_oh), s_end[1] - 100 * math.sin(max_oh))
bottom_cut = Face(
    Wire(
        [
            *Polyline(
                (far[0], 200),
                (FRONT + 50, 200),
                (FRONT + 50, lens_bottom),
                (FRONT, lens_bottom),
            ).edges(),
            ThreePointArc((FRONT, lens_bottom), arc1(s_steep / 2), arc1(s_steep)),
            ThreePointArc(arc2(s_steep), arc2(s_steep / 2), s_end),
            *Polyline(s_end, far, (far[0], 200)).edges(),
        ]
    )
)
# top: the oval socket's stroke is in the way of an S, so one arc from the lens wall into a MAX_OVERHANG line
# that just clears the stroke
c_top = max(
    p.Y - (FRONT - p.X) * math.tan(max_oh)
    for e in (cam2d.inverse() * stroked).edges()
    for p in [e.position_at(i / 40) for i in range(41)]
)
top_r = (-lens_bottom - c_top) / (
    math.sin(max_oh) * math.tan(max_oh) - 1 + math.cos(max_oh)
)
arc3 = lambda t: (
    FRONT - top_r * math.sin(t),
    -lens_bottom + top_r - top_r * math.cos(t),
)
far_t = (
    arc3(max_oh)[0] - 100 * math.cos(max_oh),
    arc3(max_oh)[1] + 100 * math.sin(max_oh),
)
top_cut = Face(
    Wire(
        [
            *Polyline(
                (far_t[0], -200),
                (FRONT + 50, -200),
                (FRONT + 50, -lens_bottom),
                (FRONT, -lens_bottom),
            ).edges(),
            ThreePointArc((FRONT, -lens_bottom), arc3(max_oh / 2), arc3(max_oh)),
            *Polyline(arc3(max_oh), far_t, (far_t[0], -200)).edges(),
        ]
    )
)
outline &= cam2d * (bottom_cut & top_cut)

side = Plane.XZ  # local u -> X, v -> Z, normal -Y
body = extrude(side * outline, WIDTH / 2, both=True)

# camera-aligned frame in 3D: a = along the lens axis, origin = side hole
cam3d = Pos(SCREW[0], 0, SCREW[1]) * Rot(0, -TILT, 0)
body = body & (
    cam3d * Pos(FRONT - 50, 0, 0) * Box(100, 100, 100)
)  # front face square to the lens axis
lens_dir = Vector(math.cos(math.radians(TILT)), 0, math.sin(math.radians(TILT)))
front = [f for f in body.faces() if f.normal_at().dot(lens_dir) > 0.999]
body = body.fillet(
    FILLET, [e for f in front for e in f.edges() if abs(e.tangent_at(0.5).Y) > 0.999]
)  # not the sides
body -= (
    cam3d
    * Pos(HOUSING_FRONT - 50, 0, 0)
    * Box(100, CAM_W + 2 * CAM_CLEAR, CAM_H + 2 * CAM_CLEAR)
)  # housing, from the back
body -= (
    cam3d * Rot(0, 90, 0) * Cylinder(LENS_D / 2 + CAM_CLEAR, 100)
)  # lens pokes out the front

# air gap: in the nose only a lens tube is left, held by the ribs; its back end is the housing's front stop.
# Air in at the front, out the open back
ring = Plane.YZ.offset(HOUSING_FRONT) * Cylinder(
    LENS_D / 2 + CAM_CLEAR + WALL, 50, align=(Align.CENTER, Align.CENTER, Align.MIN)
)
air = (
    Pos(0, 0, (AIR_TOP - AIR_BOTTOM) / 2)
    * Box(
        100,
        CAM_W + 2 * CAM_CLEAR + 2 * AIR_SIDE,
        CAM_H + 2 * CAM_CLEAR + AIR_TOP + AIR_BOTTOM,
    )
    - Box(100, 100, RIB_SIDE)
    - Box(100, RIB_TB, 100)
    - ring
)
# the top and bottom walls would start as a line hanging between the rib and the side wall: round arches instead
air_edge = {
    1: CAM_H / 2 + CAM_CLEAR + AIR_TOP,
    -1: CAM_H / 2 + CAM_CLEAR + AIR_BOTTOM,
}  # top (+1), bottom (-1)
wall_front = {
    sz: ((cam2d.inverse() * outline) & Pos(0, sz * air_edge[sz]) * Rectangle(100, 0.01))
    .bounding_box()
    .max.X
    for sz in air_edge
}  # where that wall ends at the front
for sz in (1, -1):
    for sy in (1, -1):
        b1, b2 = (
            sy * RIB_TB / 2,
            sy * (CAM_W / 2 + CAM_CLEAR + AIR_SIDE),
        )  # between the rib and the side
        r, bm = abs(b2 - b1) / 2, sz * (b1 + b2) / 2
        arch = make_face(
            [
                CenterArc((wall_front[sz], bm), r, 90, 180),
                *Polyline(
                    (wall_front[sz], bm - r),
                    (60, bm - r),
                    (60, bm + r),
                    (wall_front[sz], bm + r),
                ).edges(),
            ]
        )
        arch_plane = Plane(
            (0, 0, sz * (air_edge[sz] - 0.5)), x_dir=(1, 0, 0), z_dir=(0, 0, sz)
        )  # local y = sz * b
        air += arch_plane * extrude(arch, 30, dir=(0, 0, 1))
body -= cam3d * air
for y, d in ((WIDTH / 2, 1), (-WIDTH / 2, -1)):  # sockets on both faces
    for h in holes:
        body -= Pos(0, y + d, 0) * extrude(side * h, (SOCKET_DEPTH + 1) * d)
# M2 through both walls into the camera side holes
body -= Pos(SCREW[0], 0, SCREW[1]) * Rot(90, 0, 0) * Cylinder(SCREW_D / 2, WIDTH + 2)

# outer piece, right plate (-Y); the left one is its mirror
rim = offset(profile_face(PROFILE["rim"]), RIM_CLEAR, kind=Kind.ARC)
y_out = -(GAP / 2 + PLATE_T)  # plate outer face
y_tip = -(WIDTH / 2 - SOCKET_DEPTH + PLUG_SHORT)
bar_n = Vector(-math.sin(math.radians(BAR_ANGLE)), math.cos(math.radians(BAR_ANGLE)))
bar_off = (
    max(
        bar_n.dot(e.position_at(t))
        for e in holes[1].edges()
        for t in [i / 20 for i in range(21)]
    )
    + BAR_MARGIN
)
below_bar = Rot(0, 0, BAR_ANGLE) * Pos(0, bar_off - 50) * Rectangle(200, 100)
outer = Pos(0, y_out, 0) * extrude(side * ((stroked & plate & below_bar) - rim), BASE_T)
for h in holes:
    outer += Pos(0, y_out, 0) * extrude(
        side * offset(h, -PLUG_CLEAR, kind=Kind.ARC), -(y_tip - y_out)
    )
outer -= Pos(SCREW[0], 0, SCREW[1]) * Rot(90, 0, 0) * Cylinder(SCREW_D / 2, 100)
outer_left = mirror(outer, Plane.XZ)

y_head = y_out - BASE_T
print(
    f"outer volume {outer.volume / 1000:.2f} cm3   screw head seat -> camera side {-y_head - CAM_W / 2 - CAM_CLEAR:.1f} mm"
)
print(
    f"plug wall around the M2 {screw_wall:.2f} mm   sockets -> air gap {socket_gap:.2f} mm"
)
tip = (
    SCREW[0] + LENS_LEN * math.cos(math.radians(TILT)),
    SCREW[1] + LENS_LEN * math.sin(math.radians(TILT)),
)
print(
    f"lens tip X,Z = {tip[0]:.2f}, {tip[1]:.2f}   volume {body.volume / 1000:.2f} cm3   bbox {body.bounding_box()}"
)

if __name__ == "__main__":
    parts = {"cradle": body, "outer_right": outer, "outer_left": outer_left}
    try:
        import cadlib
    except ImportError:
        cadlib = None
    if cadlib:
        cadlib.build(parts, materials={n: ("tpu", "#2a2a2a") for n in parts})
    else:
        out = Path(__file__).parent / "out"
        out.mkdir(exist_ok=True)
        for name, part in parts.items():
            export_stl(part, str(out / f"{name}.stl"))
        print(f"wrote {out} (no cadlib: STL only)")
