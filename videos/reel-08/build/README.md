# Reel 08 — R01 (Desk): ₹1,290 Ozempic, full edit in the desk_red theme

Source: Ron's pre-cut 77.97 s talking-head (Drive file `1101.mp4`). Movie clips at 7.433–11.667 s and 32.733–34.333 s are left exactly as they are (no grade, captions, graphics or zoom; their audio is untouched and the music bed is muted under them).

## Build

```sh
python3 -I build/speed.py && python3 -I build/build_v2.py
npx hyperframes@0.8.183 render --quality delivery -o renders/raw.mp4
bash build/master.sh renders/raw.mp4 renders/reel-08-ozempic-v2.mp4
```

## What's where

| File | Holds |
|---|---|
| `build/edit_src.json` | captions (41 beats), camera moves (slow push-ins and pull-outs), SFX cues, follow card, flags |
| `build/custom.html` / `custom.js` / `custom.mjs` | the reel's motion layer (v2): 5 graphic blocks (3.7–7.4 pen→price, 19.2–24.9 padlock→India price, 26.9–31.1 STEP 1, 34.3–36.9 3 things, 49.4–53.9 what the trial did), top-band overlays, 1-2-3 tracker, two fact cards |
| `assets/inserts/patent-unlock.webm` | Remotion 3D padlock (`tools/remotion-3d`, PatentUnlock) |
| `assets/music/bed.wav` | original analytic beat bed from `tools/analytic_bed.py` (D minor, 104 bpm), −9 dB, side-chain ducked under the voice, muted in the movie clips |
| `assets/sfx/riser.wav` | synthesised 2.6 s riser (`tools/synth_sfx.py`); other SFX from Ron's library |

Builder additions used here (also in the template): `"theme": "desk_red"` and `"custom": {html, js, module}` for a per-reel hand-built layer under the captions.

## Media prep

- Picture: light grade (contrast 1.06, saturation 1.08, medium-contrast curve) except the two movie windows.
- Voice: highpass 70 Hz, de-esser, −1.5 dB @230 Hz, +1.2 dB @3.2 kHz, 2:1 compressor; movie windows raw.

## Sources shown on screen (checked)

- STEP 1: Wilding et al., N Engl J Med 2021;384:989–1002 — 1,961 adults, 68 weeks, −14.9% vs −2.4% (lifestyle support in both arms).
- Prices: Business Today, 20–21 Mar 2026 — Natco from ₹1,290/month; Wegovy ₹10,850–16,400/month; patent ended 20 Mar 2026.
- Health Ministry advisory, March 2026: GLP-1 drugs only on prescription (ThePrint; AFP).
- The study "screenshot" is a citation card: nejm.org and PubMed are blocked in this environment.

## v2 changes (Ron's review)

- Cutaways grouped into 5 blocks, mostly in the first half; graphics switch inside a block on a solid backdrop, so they never cut back through Ron's face.
- Face ↔ graphics: 0.32 s dissolve while the footage blurs (into a block) or sharpens (out of a block); hard cuts only next to the movie clips.
- Removed (Ron on camera instead): prescription ℞, side effects, scale vs muscle, dumbbell, sustained-results equation. Kept: padlock/off patent, price slam, STEP 1, 3 things, what the trial did.
- Added: "Semaglutide" (pen scene, padlock, trial equation), 2.4 mg weekly dose on the study card, fact cards for lean-mass loss (−9.7%, STEP 1 body-composition substudy) and weight regain after stopping (~⅔ within a year, STEP 1 extension 2022).
- Ron on screen ≈ 51 s of 78 s (was ≈ 35 s).
