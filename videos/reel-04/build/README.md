# Reel pipeline (V2 house style) — reusable for future fitness reels

Source footage is never modified. Everything is driven by two files:

| File | What it holds |
|---|---|
| `design.json` | Brand identity: colours, Poppins weights, type scale, safe areas, easing, camera framings, grade, loudness target, `handle` (`@YOUR_HANDLE` placeholder) |
| `edit_v2.json` | Per-video decisions, all in **source seconds**: takes (keep/reject + reason), caption beats, graphics, camera moves, stylised FX, review flags |

## Steps

1. **Prepare media** (once per raw video)
   - Picture: rotate to 1080×1920, 30 fps, short GOP → `assets/footage.mp4`.
   - Voice: original camera audio through `highpass 75 → afftdn (light) → deesser → EQ (−1.5 dB @220 Hz, +1.5 dB @3.2 kHz) → compressor 2.5:1` → `assets/voice.wav`.
   - `vad_fine.json`: Silero VAD speech pieces (150 ms min silence).
2. **Transcribe per utterance** — split at pauses ≥ 0.5 s and run Whisper large-v3 on each utterance separately (Tamil + English translation, word timestamps). Long passes hallucinate on back-to-back retakes; short utterances do not.
3. **Editorial pass** — group utterances that express the same thought (exact or paraphrased repeats, false starts, trailing takes). Keep the best *complete* take, record every decision in `takes[]`.
4. **Write beats** — one beat per spoken phrase, `t` = the source timestamp of the phrase's first word. Optional `hero` (`|` splits lines) with `hero_t` = when the key word is spoken and `fx` ∈ `pop | mask | underline | plate`. `*word*` in `support` = yellow accent.
5. **Graphics** — `section`, `list`, `week`, `steps`, `gauge`, `build`, `endcard` (see `build_v2.py`). One focal point at a time: when a graphic is up, its caption has no hero.
6. **Build** — `python3 -I build/build_v2.py` → `index.html`, `build/timeline.json`, `build/DECISIONS.md`.
   Preview subset: copy the edit with fewer `keep: true` takes → `--edit build/edit_preview.json --out preview.html`.
7. **Verify** — `npx hyperframes check`, snapshots at key moments, render the preview (`-c preview.html`), transcribe its audio to confirm no repeated speech.
8. **Render + master** — `npx hyperframes render --quality delivery -o renders/v2-raw.mp4`, then `build/master.sh renders/v2-raw.mp4 renders/<name>.mp4`.

## Pacing rules (not a fixed silence threshold)

- Gaps < 0.35 s inside a take are kept as natural speech.
- Longer gaps inside a take are cut but keep 0.13 s of air on each side (≈ 0.26 s pause, so speech never sounds breathless).
- Take-to-take joins keep 0.12 s on both sides; each voice clip has 20 ms fades so cuts never click.
- `keep_pauses` (per take, source seconds) preserves a deliberate pause before a reveal.

## Music

No licensed track was available in this environment. Drop one at `assets/music/bed.mp3` and rebuild — it is added automatically at `music_volume` (default 0.12) with fades in/out.
