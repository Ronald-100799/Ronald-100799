# Reel 10 — R03 (Terrace): Diwali sweets without the panic — first Terrace edit

Source: Ron's pre-cut 55.6 s clip (Drive `1fvuBtqwnArmpYCOQxKe-Cec5eUXUXo05`), letterboxed: picture band y 598–1321 until 5.067 s (Ron's own reframe), then y 656–1263.

## Build

```sh
python3 -I build/speed.py && python3 -I build/build_v2.py
npx hyperframes@0.8.183 render --quality delivery -o renders/raw.mp4
bash build/master.sh renders/raw.mp4 renders/reel-10-diwali-sweets.mp4
```

## Style (Terrace brief)

- Captions in the bottom black bar: Fraunces 600 support line, Caveat 700 marigold key words (fonts from @fontsource, SIL OFL; licences in `assets/fonts/`).
- No b-roll / analytic graphics. Pexels stock photos as polaroid cards in the top bar (IDs 8819769, 18488312, 18488302, 7991910, 19151502, 806457, 19295553, 10514163), dropped in with a small swing when Ron names the thing.
- One cute hand-drawn note: "+0.37 kg average weight gain over the holiday season — Yanovski et al., NEJM 2000" (Ron says "400 grams of fat"; captions keep his words).
- Zoom ins/outs inside the picture band only (`#fx` clip-path per band).
- Music: `tools/analytic_bed.py … 96 5 warm` (G major, softer drums, pad), −12 dB, ducked; SFX: soft pops on photos only, one swoosh.
- Builder fix: brightness matching skips letterboxed footage (sample corner is black).
