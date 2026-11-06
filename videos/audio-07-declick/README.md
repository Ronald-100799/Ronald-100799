# Audio 07 — mouse-click removal + voice enhancement (no captions)

Source: talking-head clip (72.5 s). Picture is stream-copied untouched; only the audio is processed.

1. `adeclip` — repairs 132 clipped samples in the source.
2. `build/declick.py` (2 passes, `N=256 MW=61`, floor 1200 Hz, cap 2.2× local median) — caps short
   high-frequency spikes to each frequency bin's local median, only on frames where the band spikes.
   Speech changes slowly per bin, so it passes through.
3. `highpass 75 → afftdn (nr 6) → deesser → EQ (−1.5 dB @220 Hz, +2 dB @3.2 kHz, +1 dB @10 kHz) → compressor 2.5:1`.
4. Two-pass loudnorm → −14 LUFS, −1.5 dBTP.

`build/imp.py` counts impulsive events (clicks). Strong clicks: 22 → 0. Medium: 63 → 12.
