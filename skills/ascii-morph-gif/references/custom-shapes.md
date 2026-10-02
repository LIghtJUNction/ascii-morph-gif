# Custom subjects

## Two masks

Prepare two images: bright shape on a black background. White is dense character ink; gray gives lighter texture. Transparent pixels are removed. The script preserves aspect ratio, centers each mask, and samples it into an 88×56 character grid. Crop excess margins in the source images. Do not use a full-color photograph without first making its silhouette readable.

```sh
python <skill-dir>/scripts/render.py \
  --from-mask ./seed.png --to-mask ./tree.png \
  --output ./seed-tree.gif --html
```

These masks hold still while they dissolve through character dust into each other. For a shape that moves while held (wings, tentacles, rotation), add a procedural branch in `mask(kind,t)` and a pair in `PRESETS`. Work on a task-local copy of the script if the installed skill should remain unchanged.

## Procedural shapes

`mask(kind,t)` returns a NumPy array of brightness values in [0,1], 56 rows by 88 columns. Time `t` runs from 0 up to, but excluding, 1. Build large shapes with Pillow at 4× resolution and downsample, or use continuous NumPy fields like the spiral galaxy. Make movement periodic across t=0 and t=1 so the loop has no jump. Keep outermost ink several cells away from the frame edge.

The morph holds the first subject for ~22% of the cycle, reveals the second by ~46%, holds through ~76%, then returns to the first. Use more hold time if the subject is hard to recognize. Dense solid masks need gray shading or internal contours to avoid a flat block of characters.

Deliver the edited source together with generated files for custom procedural work. Explain whether the result uses custom masks or procedural geometry.
