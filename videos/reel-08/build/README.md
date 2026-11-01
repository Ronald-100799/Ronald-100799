# Reel 08 — R01 (Desk): ₹1,290 Ozempic, full edit in the desk_red theme

Source: Ron's pre-cut 77.97 s talking-head (Drive file `1101.mp4`). Movie clips at 7.433–11.667 s and 32.733–34.333 s are left exactly as they are (no grade, captions, graphics or zoom; their audio is untouched and the music bed is muted under them).

## Build

```sh
python3 -I build/speed.py && python3 -I build/build_v2.py
npx hyperframes@0.8.183 render --quality delivery -o renders/raw.mp4
bash build/master.sh renders/raw.mp4 renders/reel-08-ozempic.mp4
```

## What's where

| File | Holds |
|---|---|
| `build/edit_src.json` | captions (41 beats), camera moves (slow push-ins and pull-outs), SFX cues, follow card, flags |
| `build/custom.html` / `custom.js` / `custom.mjs` | the reel's motion layer: 12 full-screen cutaways, top-band overlays, the 1-2-3 tracker, Three.js pen / STEP 1 bars / dumbbell, price and % counters |
| `assets/inserts/patent-unlock.webm` | Remotion 3D padlock (`tools/remotion-3d`, PatentUnlock) |
| `assets/music/bed.wav` | original bed from `tools/podcast_bed.py` (92 bpm), −11 dB, side-chain ducked under the voice, muted in the movie clips |
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
