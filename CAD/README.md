# Chronix Enclosure CAD v2

This revision corrects the visible vertical alignment of the 3x3 MX switch opening grid relative to the vertical TFT opening.

## Change from v1
- Switch grid Y positions changed from `[-29.5, -5.5, 18.5]` mm to `[-24.0, 0.0, 24.0]` mm.
- This centers the overall 3x3 key-opening/recess group on the TFT opening instead of leaving the key grid visibly low.

## Files
- Chronix_Enclosure_Assembly_v2.step — assembled two-part enclosure
- Chronix_Enclosure_Top_v2.step / .stl — top cover
- Chronix_Enclosure_Bottom_v2.step / .stl — bottom shell
- Chronix_Enclosure_Parametric_v2.py — editable CadQuery source

## Validation
- Bottom: 1 solid, valid
- Top: 1 solid, valid
- PCB basis: 64 x 87 mm
- Case outer size: 104 x 105 mm

## Important fit note
This is still a pre-physical-fit enclosure. The exact BLARE TFT and delivered switches have not been physically measured. The model uses the dimensions documented in the project context and should be fit-checked when the kit arrives before final printing.
