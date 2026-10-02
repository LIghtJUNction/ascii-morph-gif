---
name: ascii-morph-gif
description: Make clean, looping ASCII character-art GIFs where one recognizable object transforms into another, with optional HTML playback and social copy. Use for black-background character animation like a coffee cup becoming a galaxy, including custom subjects.
---

# ASCII Morph GIF

Create a recognizable object, let it turn into an unexpected second object, hold the result, then return smoothly to the start. Use monochrome character texture and a dark background unless the user chooses another palette.

**The GIF contains only the artwork.** No title, logo, number, watermark, URL, footer, caption, progress indicator or explanatory text. Put copy and attribution in separate files. Preserve this even when using the GIF for promotion.

## Generate

Resolve this skill directory from the location of this file. Use a virtual environment for dependencies:

```sh
python3 -m venv /tmp/ascii-gif-venv
/tmp/ascii-gif-venv/bin/pip install -r <skill-dir>/scripts/requirements.txt
/tmp/ascii-gif-venv/bin/python <skill-dir>/scripts/render.py \
  --preset coffee-galaxy --output <output-dir>/coffee-galaxy.gif --html
```

Built-in pairs: `coffee-galaxy`, `bulb-jellyfish`, `plane-bird`. Defaults: 800×800, 110 frames, 90 ms/frame, endless loop. Options: `--size`, `--frames`, `--frame-ms`, `--font`, `--foreground`, `--background`, `--seed`. GIF frame time is in multiples of 10 ms. Use a real monospace font; if font discovery fails, provide its path through `--font`.

Outputs: GIF, before/after PNGs, and optional standalone HTML. HTML animates text in a `<pre>` using JavaScript; it is not CSS-only, video footage, or a hosted page. The HTML pause button lives outside the art and is never burned into the GIF.

## New subjects

Read [references/custom-shapes.md](references/custom-shapes.md) when the user wants another transformation. Prefer clear silhouettes with enough empty space for the character texture to breathe. The renderer supports two user-owned monochrome masks and can be extended with procedural shapes; do not replace the user's subject with a preset just because it is easier.

## Inspect and deliver

Check the actual exported GIF, including both held shapes, the transition and loop seam. Confirm it has multiple frames, intended timing and `loop=0`, and that no text or branding was added outside the artwork. Inspect the before/after PNGs together to judge recognizability. Validate new subjects once; fix observable problems and repeat only the affected check.

Supply clickable output paths. If social copy is requested, write it separately in the user's languages, with a concrete visual hook. Do not invent personal experiences, claim an HTML file is online, promise traffic, or publish merely because the user requested artwork. Existing explicit authorization to publish still applies.
