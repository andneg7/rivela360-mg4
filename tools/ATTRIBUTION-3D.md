# MG4 3D runtime artwork

Based on **2025 MG MG4 (GLB)(mgmotor.com.mx)** by **MattDoesBlender**.

- Creator: https://sketchfab.com/MattDoesBlender
- Original: https://sketchfab.com/3d-models/2025-mg-mg4-glbmgmotorcommx-ee2e3b0e1a7b481cb2c08e6fc6d2ed9e
- Model and derived runtime artwork: **CC BY-NC-SA 4.0**
- License: https://creativecommons.org/licenses/by-nc-sa/4.0/

Changes on 2026-11-10: simplified to approximately 88,000 triangles, eight prepared body-paint
variants with the black roof retained, packed into 1024 x 1024 palette atlases, detailed texture
markings simplified, glazing opaque/tinted, exterior lamps disabled, geometry
uniformly normalized to 4287 mm length and converted to X right, front -Y, Z down.
The vehicle representation was narrowed for the app, and body-paint colors
were modified from the original as described above.
Normals support real-time directional lighting. The OBJ, binary mesh, MTL and PNG are derived
assets under CC BY-NC-SA 4.0, separate from the GPL application code. Source models
are not part of the APK. See model.json and paint-variants.json for dimensions,
triangle count, paint codes, display colors, material parameters and hashes.
The eight variants match the 2D Parking choices, including matte Hunter Green.
Color and gloss/matte parameters are screen approximations, not measured paint samples.
Only the body-paint palette cell changes; glass, trim, lamps and wheels retain their
original base colors. Palettes decode at 256px in the app (solid cell-center samples).

The local `car.meshbin` is an exact Float32 runtime derivative of the OBJ, including
body/wheel group ranges and pivots. Both geometry files are Git-ignored in the
source application and are supplied in this reference package. The source app's
APK packages the binary and excludes the OBJ/MTL export inputs. The binary format,
metadata and validation do not change the artwork license.

Packaging on 2026-11-15: the eight 3D paint atlases use `paint_<id>.png` in this
flat reference directory instead of `paints/<id>.png`. Asset bytes and original
metadata were not changed. See `reference-files.json` for the original filename
mapping and checksums.

The body and four wheel assemblies are exported separately. Front-wheel tires,
rims, brake discs and calipers rotate as rigid assemblies; pivots use tire-bounds
centers. These are visual test pivots, not measured kingpin axes. Steering angles
are visual road-wheel angles. The optional live input uses a provisional mapping
that still requires vehicle validation; the geometry has no measured steering ratio.
