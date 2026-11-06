# Reel 09 — R17 (Desk): mind-muscle connection, desk_red theme

Source: Ron's pre-cut 68.08 s talking-head (Drive `11uBtRBZQdIIn4IInFgqWM-4F7a_o4Gv9`). Ron's own inserts: the study screenshot (22.87–27.10 s) and the text box "In this case adaptations are much quicker" (50.90–55.20 s). v2: the warm grade and caption shade run through the whole reel (Ron wants one consistent look); the two inserts are re-laid from the same graded footage above the shade (`rIns1`, `rIns2` in custom.html, clip-path to the insert rectangle), so they stay crisp. No zoom in those windows; captions move above the head (`caption_top`).

## Build

```sh
python3 -I build/speed.py && python3 -I build/build_v2.py
npx hyperframes@0.8.183 render --quality delivery -o renders/raw.mp4
bash build/master.sh renders/raw.mp4 renders/reel-09-mind-muscle.mp4
```

## Edit

- Straight cuts in and out of 3 graphic blocks: bro-science or real results? (19.1–22.8), biceps result with 3D bars 12.4% vs 6.9% (37.2–41.45), limitations (45.95–50.85; v2 shows only the strength point Ron is making — beginners / 8 weeks appear later at 55.3 s, after he says them).
- Top-band overlays while Ron talks: point A → point B, use / abuse / overuse, group 1 vs group 2, 8 weeks · beginners · not long-term.
- Follow card on the first "follow me" (11.6 s).
- Music: original analytic bed (`tools/analytic_bed.py`, 100 bpm, seed 23), −9 dB, ducked under the voice.

## Sources (checked)

Schoenfeld et al., Eur J Sport Sci 2018;18(5):705–712 (PMID 29533715): 30 untrained men, 8 weeks; elbow-flexor thickness +12.4% (internal focus) vs +6.9% (external); strength differences not significant. Ron's "5.5% more muscle" = 12.4 − 6.9 percentage points.
