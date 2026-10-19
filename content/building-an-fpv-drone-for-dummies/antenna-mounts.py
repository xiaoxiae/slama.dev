# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = ["build123d==0.13.*"]
# ///
# Rear antenna mounts for the DeepSpace Seeker 3, by Tomáš Sláma (slama.dev): a VTX mount for a TBS Airscrew
# (u.FL) and two holders for a RadioMaster XR1's ELRS T-antenna, replacing the stock TPU VTX block + 2-hole RX bridge
# (stock parts in refs/). Print in 95A TPU: the VTX mount top face down, the holders flat.
# Run: `uv run <this file>`; STLs land in out/. Change the constants in the "tweak these" block and rerun;
# the asserts say when a combination doesn't fit.
#
# Frame: X right, Y forward, Z up; origin midway between the two rear standoffs at the bottom of the
# stack (stock frame: y + 65, z - 5.5). Standoffs at X = +-PITCH/2.
# VTX mount: one block over both standoffs with a tube rising up and back from the low bar to the top face (flat on
# the bed, printed top face down), braced by two rods from the collar tops (side view, a triangle). One straight
# channel runs down its axis, the Airscrew's solid part in it and the helix sticking out of the top; slit at the front
# (inside) so the lead (connector on) presses in. The channel opens into a funnel at the bottom: a heatshrink collar
# on the lead wedges in it, so a hit on the antenna pulls it tighter instead of tugging the u.FL.
# ELRS holders: one per standoff, a collar plus a flat arm back and outward to a sleeve on the T-antenna's inner
# tapered segment. They interlock on each standoff in the lap zone: there the holder keeps the back half of its ring
# and the VTX block the front half (both standoffs alike), so the holder can't spin.
import math
from pathlib import Path

from build123d import *

# --- tweak these ---
STACK_H = 22  # bottom of the holder collar -> top plate (stock 8 + 14)
BORE_D = 3.55  # over the standoff: a little tight (stock 3.5)
ANT_D = 2.9  # VTX antenna channel: a little under the Airscrew's 3 mm solid part, so it squeezes in
ANT_TILT = 45  # deg back from vertical, about 30..50; the tube's underside overhangs this much printed upright
# ELRS holder: a sleeve on the inner of the two tapered segments either side of the T-antenna's
# middle (where the coax leaves), axis along X. The segment goes SEG_D_END at its end -> SEG_D_MID at the middle.
SEG_L = 3.8  # >= 3.2: shorter and the top-view corner rounding fails
SEG_D_END = 4.5
SEG_D_MID = 5  # >= SEG_D_END
SLEEVE_WALL = 1.2

# --- internal: Seeker 3 frame, print details ---
PITCH = 20  # rear standoff spacing
COLLAR_D = 7  # stock 6
SLEEVE = (
    4,
    -12,
)  # sleeve centre: X outboard of the standoff axis, Y (stock antenna hole at Y -12)
# interlock
RX_H = 4  # holder full ring
LAP_H = 4  # half rings, holder back / VTX front
LAP_CLEAR = 0.15  # per mating face
ARM_W = 3  # flat arm at the collar; fans out to the sleeve's full length
ARM_T = 2.5
RAMP = 3  # arm top -> sleeve front wall: concave blend radius
FILLET = 1.5  # top view: inside corners (arm -> collar, arm -> sleeve)
CORNER = 1.0  # top view: outside corners (sleeve ends)
ROUND = 0.6  # convex edges: arm top, sleeve ends

# VTX mount
BAR_T = 3  # bar between the collars
BAR_H = 5  # low bar between the collars, at its middle; rear view, its top is a semicircle between the
# collar walls (an arch when printed top face down)
BAR_FILLET = 1  # rear view: semicircle -> collar wall
INNER_R = 4  # side view: bar -> antenna tube blend
BRIDGE_D = 3  # rods, collar top -> tube
TUBE_BOTTOM_Y = (
    -2
)  # tube axis at the bottom face, over the bar: ANT_TILT pivots about it
ROD_Z = 12  # rods meet the tube's axis at this height (at 45 deg, coming down to it at ~45 deg too)
TUBE_WALL = 1.9
FUNNEL_FLARE = 1.1  # funnel mouth at the bottom face, across the axis, over ANT_D; the heatshrink collar wedges in it
FUNNEL_L = 6  # along the axis: a shallow taper, so the collar jams instead of seating
SLIT_W = 0.5  # lead presses in from the front (inside)

NOZZLE = 0.4
TPU_DENSITY = 1.21  # g/cm3

TUBE_D = ANT_D + 2 * TUBE_WALL
FUNNEL_D = ANT_D + FUNNEL_FLARE
ROD_Y = TUBE_BOTTOM_Y - (ROD_Z - RX_H) * math.tan(math.radians(ANT_TILT))
R = COLLAR_D / 2
X0 = PITCH / 2
up = (Align.CENTER, Align.CENTER, Align.MIN)


def ring(h, z=0):
    return Pos(X0, 0, z) * (
        Cylinder(R, h, align=up) - Cylinder(BORE_D / 2, h, align=up)
    )


def creased(solid, edges, min_angle=10):  # skip the tangent seams the 2D blends leave
    out = []
    for edge in edges:
        f1, f2 = [f for f in solid.faces() if any(edge.is_same(x) for x in f.edges())][
            :2
        ]
        p = edge.center()
        if f1.normal_at(p).get_angle(f2.normal_at(p)) > min_angle:
            out.append(edge)
    return out


def fillet_each(
    solid, edges, r
):  # one edge at a time, re-found by position: OCC fails many of these as a set
    for c in [edge.center() for edge in sorted(edges, key=lambda x: -x.length)]:
        edge = min(solid.edges(), key=lambda x: (x.center() - c).length)
        if (edge.center() - c).length > 0.01:
            continue  # taken up by an earlier fillet
        for r_try in (r, r / 2, r / 4):  # smaller where the full radius doesn't fit
            try:
                solid = solid.fillet(r_try, [edge])
                break
            except Exception:  # ValueError, or OCC's own Standard_Failure
                pass
        else:
            print(f"  no fillet at {tuple(round(v, 1) for v in c)}")
    return solid


def hull2d(*faces):
    f = Face(Wire.make_convex_hull([e for f in faces for e in f.edges()]))
    return -f if f.normal_at().Z < 0 else f  # the hull can come out clockwise


# ELRS holder, right standoff; the left one is its mirror
sock_r = SEG_D_MID / 2 + SLEEVE_WALL
xs, ys = X0 + SLEEVE[0], SLEEVE[1]
x_in = xs - SEG_L / 2  # thin end, towards the drone's centreline
along_x = Pos(x_in, ys, sock_r) * Rot(
    0, 90, 0
)  # +Z -> +X; the sleeve sits on the print bed
rx = ring(RX_H) + (
    ring(LAP_H, RX_H)
    & Pos(X0, 0, 0) * Box(2 * R, R, STACK_H, align=(Align.CENTER, Align.MAX, Align.MIN))
)
at_sleeve = lambda y0, y1: Pos(xs, (y0 + y1) / 2) * Rectangle(SEG_L, y1 - y0)
close2d = lambda f, r: offset(
    offset(f, r, kind=Kind.ARC), -r, kind=Kind.ARC
)  # rounds the inside corners
open2d = lambda f, r: offset(
    offset(f, -r, kind=Kind.ARC), r, kind=Kind.ARC
)  # rounds the outside corners
# top view, every corner rounded; R - 0.05: a footprint circle coincident with the collar wall makes OCC drop the collar
# the arm lands FILLET in from the sleeve's inner end, so the corner rounding stays clear of the hole's mouth
arm_end = Pos(xs + FILLET / 2, ys + sock_r - 0.5) * Rectangle(SEG_L - FILLET, 1)
foot2d = (
    Pos(X0, 0) * Circle(R - 0.05)
    + hull2d(Pos(X0, 0) * Circle(ARM_W / 2), arm_end)
    + at_sleeve(ys - sock_r, ys + sock_r)
)
foot2d = close2d(open2d(foot2d, CORNER), FILLET)
# side view: the sleeve's circle blended into the arm's flat top
side2d = close2d(
    Pos(ys, sock_r) * Circle(sock_r) + Pos(ys + 15, ARM_T / 2) * Rectangle(30, ARM_T),
    RAMP,
)
low = extrude(foot2d, 2 * sock_r) & extrude(Plane.YZ * side2d, 2 * X0 + 10)
top_edges = [
    edge
    for edge in low.edges()
    if edge.center().Z > 0.01
    and math.hypot(edge.center().X - X0, edge.center().Y) > R + 0.3
]
low = fillet_each(low, creased(low, top_edges), ROUND)
rx += low
eps = 0.01
taper = (SEG_D_MID - SEG_D_END) / 2 / SEG_L  # radius per mm along the segment
seg_r0, seg_r1 = SEG_D_END / 2 - taper * eps, SEG_D_MID / 2 + taper * eps
rx -= (
    along_x
    * Pos(0, 0, -eps)
    * (
        Cone(seg_r0, seg_r1, SEG_L + 2 * eps, align=up)
        if taper
        else Cylinder(seg_r0, SEG_L + 2 * eps, align=up)
    )
)  # OCC: no cone with equal radii
rx -= Pos(X0, 0, -10) * Cylinder(BORE_D / 2, STACK_H + 20, align=up)
mouth = (
    Pos(x_in, ys, sock_r) * Rot(0, -90, 0) * Cylinder(SEG_D_END / 2, 10, align=up)
)  # antenna path past the inner end
assert not (hit := rx & mouth) or hit.volume < 1e-6, "holder blocks the antenna hole"
assert (
    len(rx.solids()) == 1
    and abs(rx.bounding_box().max.Z - max(RX_H + LAP_H, 2 * sock_r)) < 1e-6
    and rx.volume > 250
), "holder boolean failed"

# VTX mount
H = STACK_H - RX_H
t = math.radians(ANT_TILT)
boss_r = TUBE_D / 2
axis_y = lambda z: ROD_Y + (ROD_Z - z) * math.tan(t)
# everything runs 1 past the top (and the tube 1 past the bottom), then one trim makes the flat ends:
# coplanar ends between the pieces leave OCC with an invalid solid
Z0, Z1 = RX_H - 1, STACK_H + 1
# low bar: top view (inside corners rounded) & rear view; its collar strips sit inside the collars, so the
# top-view fillets by the collars follow the bar's top, not the collar
top2d = close2d(
    Pos(-X0, 0) * Circle(R - 0.05)
    + Pos(X0, 0) * Circle(R - 0.05)
    + Rectangle(PITCH, BAR_T),
    FILLET,
)  # inside the collar walls
collars2d = Pos(-X0, RX_H + (H - 1) / 2) * Rectangle(R, H - 1) + Pos(
    X0, RX_H + (H - 1) / 2
) * Rectangle(R, H - 1)
arch_r = (
    X0 - R + 0.3
)  # just inside the collar walls: tangent to them leaves OCC with an invalid solid
arch_z = RX_H + BAR_H + arch_r
rear2d = (
    Pos(0, (RX_H + Z1) / 2) * Rectangle(PITCH + COLLAR_D, Z1 - RX_H)
    - Pos(0, arch_z) * Circle(arch_r)
    - Pos(0, (arch_z + Z1 + 1) / 2) * Rectangle(2 * arch_r, Z1 + 1 - arch_z)
)
rear2d = close2d(rear2d + collars2d, BAR_FILLET)
bar = Pos(0, 0, RX_H) * extrude(top2d, H) & extrude(Plane.XZ * rear2d, R, both=True)
bar = fillet_each(
    bar,
    creased(bar, [edge for edge in bar.edges() if edge.center().Z > RX_H + 0.01]),
    ROUND,
)
vtx = (
    bar
    + Pos(-X0, 0, RX_H) * Cylinder(R, Z1 - RX_H, align=up)
    + Pos(X0, 0, RX_H) * Cylinder(R, Z1 - RX_H, align=up)
)
# antenna tube along the axis, joined to the bar by a concave arc (side view)
w = boss_r / math.cos(t)  # tube half-width, horizontal
band = Polygon(
    (axis_y(Z0) + w, Z0),
    (axis_y(Z1) + w, Z1),
    (axis_y(Z1) - w, Z1),
    (axis_y(Z0) - w, Z0),
    align=None,
)
bar_back = Pos(-BAR_T / 4, (RX_H - 1 + RX_H + BAR_H) / 2) * Rectangle(
    BAR_T / 2, BAR_H + 1
)  # back half of the bar only
side2d_v = close2d(band + bar_back, INNER_R)
tube = Pos(-boss_r, 0, 0) * extrude(Plane.YZ * side2d_v, 2 * boss_r)
tube_sides = [
    edge
    for edge in tube.edges()
    if abs(abs(edge.center().X) - boss_r) < 0.01 and RX_H < edge.center().Z < STACK_H
]
tube = fillet_each(tube, tube_sides, 0.9 * boss_r)
ant = Pos(0, axis_y(STACK_H), STACK_H) * Rot(
    ANT_TILT, 0, 0
)  # at the top face, +Z up the antenna
axis_len = (STACK_H - RX_H) / math.cos(t)  # top face -> bottom face, along the axis
# rods, collar top -> the tube's axis
end = Vector(0, ROD_Y, ROD_Z)
bridges = None
for x_ in (-X0, X0):
    p0 = Vector(x_, 0, STACK_H)
    rod = Plane(p0, z_dir=end - p0) * Cylinder(
        BRIDGE_D / 2, (end - p0).length, align=up
    )
    bridges = rod if bridges is None else bridges + rod
vtx = (vtx + tube + bridges) & Pos(0, 0, RX_H) * Box(100, 100, H, align=up)
vtx -= (
    ant
    * Pos(0, 0, 5)
    * Cylinder(ANT_D / 2, 50, align=(Align.CENTER, Align.CENTER, Align.MAX))
)
funnel_k = (FUNNEL_D - ANT_D) / 2 / FUNNEL_L  # radius per mm along the funnel
vtx -= (
    ant
    * Pos(0, 0, -axis_len - 2)
    * Cone(FUNNEL_D / 2 + 2 * funnel_k, ANT_D / 2, FUNNEL_L + 2, align=up)
)  # runs 2 past the bottom
# slit, channel -> front of the tube, through the bar
vtx -= (
    ant * Pos(0, 0, 5) * Box(SLIT_W, 10, 50, align=(Align.CENTER, Align.MIN, Align.MAX))
)
for s in (-1, 1):
    vtx -= Pos(s * X0, 0, -10) * Cylinder(BORE_D / 2, STACK_H + 20, align=up)
    notch = Pos(s * X0, 0, RX_H - 1) * Cylinder(
        R + LAP_CLEAR, LAP_H + LAP_CLEAR + 1, align=up
    )  # holder's back half
    vtx -= notch & Pos(s * X0, LAP_CLEAR, 0) * Box(
        20, 20, 100, align=(Align.CENTER, Align.MAX, Align.CENTER)
    )

assert vtx.is_valid and len(vtx.solids()) == 1, "VTX boolean failed"
rx_left = mirror(rx, Plane.YZ)
clash = max((hit.volume if (hit := vtx & part) else 0) for part in (rx, rx_left))
print(f"stack {STACK_H}: holder ring {RX_H} + lap {LAP_H}, VTX block {H}")
print(
    f"holder bore wall {R - BORE_D / 2:.2f}; arm {ARM_W} x {ARM_T}, fans to {SEG_L} at the sleeve"
)
print(
    f"ELRS sleeve {SEG_D_END}->{SEG_D_MID} over {SEG_L}, wall {SLEEVE_WALL} = {SLEEVE_WALL / NOZZLE:.0f} lines,"
    f" axis Z {sock_r:.2f}; antenna inner ends {2 * x_in:.1f} apart"
)
print(
    f"antenna channel {ANT_D} in a {TUBE_D:.1f} tube, wall {(TUBE_D - ANT_D) / 2:.2f}, {ANT_TILT} deg, top at Y {axis_y(STACK_H):.1f},"
    f" bottom at Y {axis_y(RX_H):.1f}; funnel {ANT_D}->{FUNNEL_D:.1f} over {FUNNEL_L},"
    f" {math.degrees(math.atan(funnel_k)):.0f} deg half-angle, wall at the mouth {(TUBE_D - FUNNEL_D) / 2:.2f}"
)
print(f"VTX vs holders overlap {clash:.4f} mm3")
for name, part in (("vtx", vtx), ("holder", rx)):
    print(
        f"{name} {part.volume / 1000:.2f} cm3 = {part.volume / 1000 * TPU_DENSITY:.1f} g"
    )

if __name__ == "__main__":
    parts = {"vtx_mount": vtx, "rx_holder_right": rx, "rx_holder_left": rx_left}
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
