# MG4 artwork preparation tools

Offline scripts from [MG4-360-Camera-App](https://github.com/jamakr4/MG4-360-Camera-App)
(`tools/birdseye`, branch `v0.9`). All six Python scripts and the prepared
reference artwork are kept together here, without subdirectories.

These scripts prepare two independent outputs:

- **2D:** eight pre-rendered, transparent 768 × 1536 PNGs, one per paint color.
  Displaying them does not require loading or rendering the 3D model at runtime.
- **3D:** a simplified body and four separate wheel assemblies, a shared material
  atlas, eight paint palettes and an optional precompiled binary mesh.

## Prepared reference artwork

The following matching files are supplied so you can inspect the results or
continue from the prepared Blender scene without downloading the original GLB.

| Files | Contents |
| --- | --- |
| [mg4-topview.blend](mg4-topview.blend) | Prepared orthographic scene, about 34 MiB. Both image textures are packed into the file. |
| `mg4-topview.png`, `mg4-orientation-check.png`, `render-metadata.json` | Original blue top view, perspective orientation check and scene registration metadata. |
| `car.obj`, `car.mtl`, `car.png`, `model.json` | Reduced 87,995-triangle model, materials, base atlas and geometry metadata. |
| `car.meshbin` | Matching precompiled reference binary, about 8 MiB; see the runtime-format notes below. |
| `paint_*.png`, `paint-variants.json` | Eight matching 1024 × 1024 3D paint palettes and material parameters. |
| `topview_*.png`, `topview.json`, `color-renders.json` | Eight transparent 768 × 1536 2D images, registration bounds and paint metadata. |
| `ATTRIBUTION-SCENE.md`, `ATTRIBUTION-3D.md`, `ATTRIBUTION-2D.md` | Creator, source, artwork license and modification records. |
| [reference-files.json](reference-files.json) | Exact filename mapping, upstream relative paths and SHA-256 checksums. |

The `topview_` and `paint_` prefixes distinguish the two sets of color images in
this flat directory. Image bytes and the original JSON manifests are unchanged.
The source app expects `colors/<id>.png` for 2D and `paints/<id>.png` for 3D;
restore those names/directories when adapting the set for an app. The reference
manifest records both mappings. The scene and geometry were ignored in the
source repository; they are explicitly included in this reference package.

## Requirements and input

Use **Blender 5.x** for importing, rendering and exporting, and **Python 3.9+**
for the standalone binary compiler. No pip packages are required. Blender's
Python provides `bpy`, `bmesh` and `mathutils`.

To rebuild from the original download, obtain **[2025 MG MG4 (GLB)(mgmotor.com.mx)](https://sketchfab.com/3d-models/2025-mg-mg4-glbmgmotorcommx-ee2e3b0e1a7b481cb2c08e6fc6d2ed9e)**
by **[MattDoesBlender](https://sketchfab.com/MattDoesBlender)** yourself. This
download is optional when using the supplied prepared scene.
Use the original GLB, with its original object and material names. In particular,
the scripts expect `Carroceria`, `llantas1`, `polySurface387`, `Discos` and
`Calipers`. Rivela's already modified binary model is not an input to these tools.

The renderers try Metal on supported Macs and otherwise use the CPU. On macOS,
the Blender executable is usually
`/Applications/Blender.app/Contents/MacOS/Blender`; use that path in place of
`blender` if it is not on your PATH.

Keep new downloads, working scenes and generated exports outside this checkout
so they do not overwrite the supplied reference files.

## Scripts

| Script | Purpose |
| --- | --- |
| `inspect_model.py` | Optional GLB inspection: object/material report and an imported Blender scene. |
| `render_topview.py` | Prepare the GLB, studio lighting and orthographic camera; save the shared scene, blue top view, registration metadata and an orientation-check image. |
| `render_car_colors.py` | Render the eight 2D paint variants and write `color-renders.json`. |
| `export_car_model.py` | Decimate the body and four wheel groups; export OBJ, MTL, a 1024 × 1024 material-color atlas and `model.json`. |
| `export_car_paints.py` | Prepare eight matching 3D paint atlases using the existing geometry and the 2D color manifest. |
| `compile_car_mesh.py` | Compile the final OBJ into `car.meshbin` and update its hash/format metadata. |

## Workflow

Run these commands from the repository root. Choose a new output directory;
the exporters refuse to overwrite existing exports.

```sh
MG4_SOURCE_GLB="/absolute/path/to/original-model.glb"
MG4_ARTWORK_WORK="/absolute/path/outside/the/repository/mg4-artwork"
MG4_ARTWORK_BLEND="$MG4_ARTWORK_WORK/topview/mg4-topview.blend"
MG4_BLUE_REFERENCE="$MG4_ARTWORK_WORK/topview/mg4-topview.png"
mkdir -p "$MG4_ARTWORK_WORK"

# 1. Prepare the scene, render the original blue top view, and save image bounds.
blender --background --factory-startup --python tools/render_topview.py -- \
  --input "$MG4_SOURCE_GLB" --output "$MG4_ARTWORK_WORK/topview"

# 2. Render all eight 2D colors; retain the original blue rendering.
blender --background --factory-startup --python tools/render_car_colors.py -- \
  --blend "$MG4_ARTWORK_BLEND" \
  --blue-reference "$MG4_BLUE_REFERENCE" \
  --output "$MG4_ARTWORK_WORK/colors"

# 3. Export the reduced 3D model and its base material-color atlas.
blender --background --factory-startup --python tools/export_car_model.py -- \
  --blend "$MG4_ARTWORK_BLEND" \
  --output "$MG4_ARTWORK_WORK/model"

# 4. Generate eight paint palettes for that exact geometry/material layout.
blender --background --factory-startup --python tools/export_car_paints.py -- \
  --blend "$MG4_ARTWORK_BLEND" \
  --model-dir "$MG4_ARTWORK_WORK/model" \
  --paints "$MG4_ARTWORK_WORK/colors/color-renders.json" \
  --output "$MG4_ARTWORK_WORK/palettes"

# 5. Overlay the prepared palettes and their updated metadata before compiling.
cp "$MG4_ARTWORK_WORK/palettes/car.png" \
   "$MG4_ARTWORK_WORK/palettes/model.json" \
   "$MG4_ARTWORK_WORK/palettes/paint-variants.json" \
   "$MG4_ARTWORK_WORK/model/"
cp -R "$MG4_ARTWORK_WORK/palettes/paints" "$MG4_ARTWORK_WORK/model/"

# 6. Compile the final OBJ once, ahead of the Android build.
python3 tools/compile_car_mesh.py --model-dir "$MG4_ARTWORK_WORK/model"
```

To use the supplied scene instead, choose a fresh `MG4_ARTWORK_WORK`, create it,
set the two variables below and run steps **2–6**, skipping the GLB import:

```sh
MG4_ARTWORK_BLEND="tools/mg4-topview.blend"
MG4_BLUE_REFERENCE="tools/mg4-topview.png"
```

If you need only a new 3D export with the existing paint choices, step 2 can also
be skipped: use `--paints tools/color-renders.json` in step 4. For interactive
Blender use, choose your own render output path before rendering.

The **2D-only** workflow ends after step 2. The PNGs and
`color-renders.json` are in `colors/`; their shared registration bounds are
in `topview/render-metadata.json`.

The **3D** output is in `model/`: `car.obj`, `car.mtl`, `car.png`,
`model.json`, `paint-variants.json`, `paints/*.png` and `car.meshbin`.
Keep the binary, metadata and palettes from the same export together.

For optional inspection, create an empty directory first and pass two positional
arguments to the Blender script:

```sh
mkdir -p "$MG4_ARTWORK_WORK/inspection"
blender --background --factory-startup --python tools/inspect_model.py -- \
  "$MG4_SOURCE_GLB" "$MG4_ARTWORK_WORK/inspection"
```

`render_car_colors.py` supports `--colors hunter_green` to render a subset,
and `--overwrite` to replace existing variants. The 3D palette exporter expects
the complete eight-color manifest. `compile_car_mesh.py --overwrite` replaces
a previously compiled mesh.

## Reduction and materials

The exporter uses Blender's **Decimate** modifier in collapse mode with
`use_collapse_triangulate = True`. It targets **88,000 triangles** in total,
allocating each part's budget proportionally to its source triangle count.

The recorded MG4 export went from **1,036,472 to 87,995 triangles**, an
approximate reduction ratio of **0.0849**. Exact results can vary with the source
and Blender version. The groups are `body`, `front_left`, `front_right`,
`rear_left` and `rear_right`. Wheel pivots use tire-bounds centers for visual
animation, not measured steering axes.

Detailed texture markings are replaced with solid material colors in a shared
**1024 × 1024 atlas**. Each material's UVs sample its palette-cell center.
The eight paint variants share the same geometry; only the body-paint cell changes.
The black roof and the prepared glazing, trim, lamps and wheels are retained.
The source app decodes these solid palettes at **256 × 256** at runtime.
Paint names/codes and colors are screen approximations, not measured paint samples.

## Runtime integration

`car.meshbin` uses the source app's **MG4MSH01, version 1** format.
It is **not a drop-in replacement** for Rivela's `car3d-pub-v4.bin`.
The Rivela importer/loader would need a matching implementation or a separate
export-format adaptation. These standalone tools do not modify the Rivela app.

The binary is little-endian: a 56-byte header, five 36-byte part records,
then non-indexed triangle vertices with eight Float32 values each
(position XYZ, normal XYZ, UV). Part records store the name, first vertex,
vertex count and pivot XYZ. Coordinates are millimeters, X right, front -Y,
Z down. The compiler validates source hashes, part order, counts and pivots.

Bundling the prepared binary with its palettes avoids a runtime model download
or OBJ parsing. Exclude the intermediate OBJ/MTL from the APK if they are unused.
Background CPU preloading, caching across Activities, and GPU uploads when an
OpenGL context becomes available are separate Android-side work; they are not
performed by these offline scripts.

## Licenses and attribution

The six Python scripts are copied from MG4-360-Camera-App under **GNU GPL v3**;
the complete license is included in [LICENSE](LICENSE). This license covers
these standalone tools and does not replace the repository's existing license
for Rivela 360.

The original model and derived artwork remain **[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)**.
The prepared Blender scene, reduced model and reference artwork included here
are derivatives under that license; the original downloaded GLB is not included.
See [scene attribution](ATTRIBUTION-SCENE.md), [3D attribution](ATTRIBUTION-3D.md)
and [2D attribution](ATTRIBUTION-2D.md) for the existing modification records.
When distributing prepared artwork, retain its creator/source/license information
and identify the changes. A starting attribution for outputs from this workflow is:

> Based on "2025 MG MG4 (GLB)(mgmotor.com.mx)" by MattDoesBlender:
> https://sketchfab.com/3d-models/2025-mg-mg4-glbmgmotorcommx-ee2e3b0e1a7b481cb2c08e6fc6d2ed9e
>
> Original model and derived artwork: CC BY-NC-SA 4.0:
> https://creativecommons.org/licenses/by-nc-sa/4.0/
>
> Changes: orthographic top-view renders with transparent background and studio
> lighting; adjusted glazing and exterior lamps disabled; eight body-paint variants;
> simplified 3D body and four wheel assemblies targeting 88,000 triangles;
> detailed textures replaced by material-color atlases; normalized coordinates
> and exported OBJ/binary runtime geometry.

Adapt this change record to the outputs you actually distribute, and retain any
additional notices supplied with your downloaded source.
