import cadquery as cq
from cadquery import exporters
from pathlib import Path

OUT = Path('/mnt/data/Chronix_CAD_v2')

# ---------------- Parameters ----------------
# PCB is fixed by the Chronix project context.
PCB_W = 64.0
PCB_H = 87.0
PCB_T = 1.6

# BLARE 2.25-in 8-pin TFT envelope used for this enclosure model.
# Source-derived dimensions: 21.08 x 73.15 x 3.56 mm module.
TFT_W = 21.08
TFT_H = 73.15
TFT_T = 3.56
TFT_AA_W = 14.797
TFT_AA_H = 55.295

# Case
CASE_W = 104.0
CASE_H = 105.0
CASE_R = 6.0
BOTTOM_H = 25.0
WALL = 4.0
BASE_T = 4.0
TOP_T = 3.0
LOCATING_LIP_T = 2.0

# PCB position in case XY plane (centered at this point)
PCB_CX = 13.0
PCB_CY = 0.0

# Screen position; long axis vertical.
TFT_CX = -38.0
TFT_CY = 0.0

# Standard-ish MX plate opening and grid from the intended 3x3 matrix.
SW_HOLE = 14.2
KEY_RECESS = 18.4
KEY_RECESS_DEPTH = 0.8
# Positions inferred from the 3x3 PCB layout: 3 columns, 3 rows.
SW_X = [-8.5, 10.55, 29.60]
SW_Y = [-24.0, 0.0, 24.0]

# Buzzer vent center (roughly above the lower-right buzzer footprint)
BUZZER_CX = 33.0
BUZZER_CY = -33.0

# Top screw locations. They stay outside the nominal PCB footprint as much as possible.
SCREW_X = [-47.0, 47.0]
SCREW_Y = [-48.0, 48.0]
TOP_SCREW_D = 3.4
INSERT_D = 5.1
BOSS_D = 8.0

# ---------------- Helpers ----------------
def rounded_rect(w, h, r, z=0, depth=1):
    # Single-solid rounded rectangle using vertical edge fillets.
    r = min(r, w/2-0.01, h/2-0.01)
    return (cq.Workplane('XY', origin=(0,0,z))
            .box(w, h, depth, centered=(True,True,False))
            .edges('|Z').fillet(r))

# ---------------- Bottom shell ----------------
outer = rounded_rect(CASE_W, CASE_H, CASE_R, 0, BOTTOM_H)
inner = rounded_rect(CASE_W-2*WALL, CASE_H-2*WALL, CASE_R-WALL if CASE_R > WALL else 2, BASE_T, BOTTOM_H-BASE_T+0.5)
bottom = outer.cut(inner)

# Interior PCB edge supports: four low ledges/clamps under PCB edges.
# They use the board perimeter rather than depending on unspecified PCB mounting holes.
ledge_z = BASE_T
ledge_h = 2.2
for x in (PCB_CX - PCB_W/2 + 3.0, PCB_CX + PCB_W/2 - 3.0):
    for y in (PCB_CY - PCB_H/2 + 2.8, PCB_CY + PCB_H/2 - 2.8):
        # small corner ledge, 7x7 footprint
        clip = (cq.Workplane('XY', origin=(x,y,ledge_z))
                .box(7.0, 7.0, ledge_h, centered=(True,True,False)))
        bottom = bottom.union(clip)

# Four heat-set insert bosses.
for x in SCREW_X:
    for y in SCREW_Y:
        boss = cq.Workplane('XY', origin=(x,y,BASE_T)).cylinder(BOSS_D/2, 19.0, centered=(True,True,False))
        # Insert bore from the top of the boss downward 5.0 mm.
        bore = cq.Workplane('XY', origin=(x,y,BASE_T+14.0)).cylinder(INSERT_D/2, 5.5, centered=(True,True,False))
        bottom = bottom.union(boss).cut(bore)

# USB-C access slot on the lower side wall.
usb_slot = (cq.Workplane('XZ', origin=(0,-CASE_H/2-0.5,0))
            .center(PCB_CX, 11.0)
            .rect(14.0, 6.0)
            .extrude(6.0))
bottom = bottom.cut(usb_slot)

# Small speaker vent slots through bottom/front wall are intentionally omitted;
# top cover has a dedicated vent field above the buzzer.

# ---------------- Top cover ----------------
top = rounded_rect(CASE_W, CASE_H, CASE_R, BOTTOM_H, TOP_T)

# Flat top cover; perimeter screw holes provide alignment and retention.
# TFT recess and active-area opening.
tft_recess_w = TFT_W + 1.2
tft_recess_h = TFT_H + 1.2
recess = cq.Workplane('XY', origin=(TFT_CX, TFT_CY, BOTTOM_H+TOP_T-1.5)).box(tft_recess_w, tft_recess_h, 1.8, centered=(True,True,False))
top = top.cut(recess)

# Active-area opening, with 0.35 mm margin around the stated active area.
active = cq.Workplane('XY', origin=(TFT_CX, TFT_CY, BOTTOM_H-0.2)).box(TFT_AA_W+0.7, TFT_AA_H+0.7, TOP_T+0.6, centered=(True,True,False))
top = top.cut(active)

# TFT mounting holes: 2 x 2.5 mm hole pattern near the bottom of the module.
tft_hole_y = TFT_CY - TFT_H/2 + 2.41
for x in (TFT_CX-8.13, TFT_CX+8.13):
    h = cq.Workplane('XY', origin=(x,tft_hole_y,BOTTOM_H-0.5)).cylinder(1.45, TOP_T+1.0, centered=(True,True,False))
    top = top.cut(h)

# 9 key openings with shallow keycap recesses.
for x in SW_X:
    for y in SW_Y:
        recess2 = cq.Workplane('XY', origin=(x,y,BOTTOM_H+TOP_T-KEY_RECESS_DEPTH)).box(KEY_RECESS, KEY_RECESS, KEY_RECESS_DEPTH+0.2, centered=(True,True,False))
        hole = cq.Workplane('XY', origin=(x,y,BOTTOM_H-0.3)).box(SW_HOLE, SW_HOLE, TOP_T+0.7, centered=(True,True,False))
        top = top.cut(recess2).cut(hole)

# Buzzer vent field: 13 holes, 1.8 mm diameter, in a compact pattern.
vent_pts = [
    (0,0), (-4,0),(4,0),(0,-4),(0,4),(-3,-3),(3,-3),(-3,3),(3,3),
    (-6,0),(6,0),(0,-6),(0,6)
]
for dx,dy in vent_pts:
    vh = cq.Workplane('XY', origin=(BUZZER_CX+dx, BUZZER_CY+dy, BOTTOM_H-0.2)).cylinder(0.9, TOP_T+0.6, centered=(True,True,False))
    top = top.cut(vh)

# Top cover screw holes.
for x in SCREW_X:
    for y in SCREW_Y:
        h = cq.Workplane('XY', origin=(x,y,BOTTOM_H-0.5)).cylinder(TOP_SCREW_D/2, TOP_T+1.0, centered=(True,True,False))
        top = top.cut(h)

# ---------------- Decorative feet / cable strain relief ----------------
# Four shallow cylindrical rubber-foot pockets on the underside of bottom.
feet = [(-44,-45),(44,-45),(-44,45),(44,45)]
for x,y in feet:
    fp = cq.Workplane('XY', origin=(x,y,-0.01)).cylinder(3.5, 1.0, centered=(True,True,False))
    bottom = bottom.cut(fp)

# ---------------- Export ----------------
# Clean compounds for consistent export.
bottom = bottom.combine().clean()
top = top.combine().clean()

# Separate manufacturing files
exporters.export(bottom, str(OUT/'Chronix_Enclosure_Bottom_v2.step'))
exporters.export(top, str(OUT/'Chronix_Enclosure_Top_v2.step'))
exporters.export(bottom, str(OUT/'Chronix_Enclosure_Bottom_v2.stl'), tolerance=0.05, angularTolerance=0.2)
exporters.export(top, str(OUT/'Chronix_Enclosure_Top_v2.stl'), tolerance=0.05, angularTolerance=0.2)

# Assembled STEP compound: top and bottom in installed positions.
assembly = cq.Compound.makeCompound([bottom.val(), top.val()])
exporters.export(assembly, str(OUT/'Chronix_Enclosure_Assembly_v2.step'))

# Source copy in a convenient CAD folder name.

print('Generated:')
for f in [
    'Chronix_Enclosure_Assembly_v2.step',
    'Chronix_Enclosure_Bottom_v2.step',
    'Chronix_Enclosure_Top_v2.step',
    'Chronix_Enclosure_Bottom_v2.stl',
    'Chronix_Enclosure_Top_v2.stl',
]:
    print(f, (OUT/f).stat().st_size)

# Basic CAD validity checks.
for name, obj in [('Bottom', bottom.val()), ('Top', top.val())]:
    print(name, 'solids=', len(obj.Solids()), 'valid=', obj.isValid())
