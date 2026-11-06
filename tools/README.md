# Motion toolkit for reels

Four tools, each with one job. The reel builder (`videos/reel-06/build/build_v2.py`, the current template) stays the single place where a reel is assembled; the other tools feed it.

| Need | Tool | How it reaches the reel |
|---|---|---|
| Flowcharts, cycles, step-by-step processes | **GSAP** (`flow` graphic in the builder) | Native graphic type in `edit_src.json` |
| A quick 3D object (dumbbell, plate, 3D bars) | **Three.js** (`three` graphic in the builder) | Native graphic type; draws from video time |
| A crafted 3D shot (plates loading, objects building up, camera moves) | **Remotion + Three.js** (`tools/remotion-3d/`) | Renders a transparent WebM; add it as an `overlays` entry |
| Studying a reference reel and planning a motion sequence | **NullMotion** (run on your own computer) | Planning only; nothing is imported into the reel |

House style still applies: graphics sit in clear wall space (never over the face or the whiteboard), yellow for the key item, few quiet sounds.

## 1. GSAP flowchart: `"type": "flow"`

Nodes pop in on their spoken cue (source time), and each arrow draws in just before its node lands. One node can be marked `hot` (yellow). An optional loop arrow runs from the last node back to the first, for cycles like progressive overload.

```json
{"type": "flow", "t": 8.0, "until": 12.4, "header": "Progressive overload", "loop": {"t": 10.6},
 "nodes": [{"text": "Lift", "t": 8.2, "idx": "1"}, {"text": "Recover", "t": 8.9, "idx": "2"},
           {"text": "Add a rep", "t": 9.6, "idx": "3", "hot": true}]}
```

Options: `dir` is `"down"` (stacked, default) or `"right"` (side by side, centred). Node size is set with `w`, `h` and `gap`. Position is set with `left` and `top` in pixels. A node without `t` is auto-staggered every 0.45 s. `loop` is `true` or `{"t": ...}`.

## 2. Three.js 3D object: `"type": "three"`

A transparent WebGL canvas, drawn from HyperFrames time (seek-safe and deterministic). three.js 0.181.2 (MIT) is vendored in `assets/three/`, so renders don't depend on a CDN.

```json
{"type": "three", "t": 12.5, "until": 16.6, "model": "dumbbell", "label": "60 KG", "size": 520, "x": 500, "y": 330}
{"type": "three", "t": 46.2, "until": 52.0, "model": "bars", "size": 460, "x": 560, "y": 440, "label": "Volume",
 "bars": [{"label": "W1", "value": 1800}, {"label": "W2", "value": 1950}, {"label": "W3", "value": 2100, "hot": true}]}
```

There are three models:
- `dumbbell`: springs in and turns.
- `plate`: springs in and turns.
- `bars`: the bars grow one after another, and the `hot` bar is yellow.

`spin` sets the turn speed. A new model is one function in `THREE_JS_BODY` inside the builder.

## 3. Remotion 3D inserts: `tools/remotion-3d/`

Use this for 3D shots that need more craft than a spinning object. It's a React project using `@remotion/three` and Remotion 4.0.290.

```sh
cd tools/remotion-3d && npm install
npm run studio                                    # live preview in the browser
node render.mjs PlateLoad out/plateload.webm '{"plates":4}'
```

`render.mjs` renders to VP9 WebM with an alpha channel, using the sandbox's Chromium when it is present. Copy the file into the reel's `assets/inserts/` and add it as an overlay:

```json
"overlays": [{"file": "assets/inserts/plateload.webm", "t": 32.0, "until": 35.5,
              "left": 380, "top": 300, "w": 640, "h": 640, "filter": "none"}]
```

Tested: the transparency survives the final HyperFrames MP4 render. Example composition: `PlateLoad`, a barbell that loads one plate per side at a time, with the last plate in yellow.

Licence: Remotion is free for individuals and companies of up to 3 people. A larger team needs a company licence (remotion.pro).

## 4. NullMotion: reference breakdowns (github.com/blixvip/NullMotion, MIT)

NullMotion doesn't generate graphics for a reel. It's a local study tool: it plays a finished motion-graphics ad over plain black-and-white HyperFrames drafts, one per section, synced frame for frame. Use it to take apart a reel whose motion you want to borrow, then write the result as `flow`, `three` or overlay entries.

Run it on your own computer. It needs Node 22+ and has no dependencies.

```sh
git clone https://github.com/blixvip/NullMotion && cd NullMotion && npm start   # http://127.0.0.1:4343
```

With FFmpeg installed, `node scripts/plan-sections.mjs` splits imported references into 3–8 sections at scene cuts. You describe each section's beats in `public/references/drafts.json`. Exporting a breakdown MP4 needs Chrome or Edge.

Its server isn't run inside Claude's cloud sandbox: the sandbox's safety check blocks running downloaded third-party code. Send the reference reel and Claude can do the same breakdown with ffmpeg scene detection and contact sheets.
