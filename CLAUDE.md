# Reel editing — standing preferences (Ron, @ron_tamil)

These apply to every reel unless the request for a specific reel says otherwise.

## Scope
- **Default: full edit** — captions with emphasised keywords, motion graphics, camera moves where needed, colour/quality check, audio polish, mastering. Pipeline and house style: `videos/raw-reel-v2/build/README.md`; latest working copies (current template): `videos/reel-06/build/`. Motion toolkit (`tools/README.md`): GSAP flowcharts (`flow` graphic), Three.js 3D objects (`three` graphic), Remotion 3D inserts as transparent overlays (`tools/remotion-3d/`), NullMotion for breaking down reference reels. Use 3D and flowcharts only where they explain something (a process, a cycle, a comparison); same placement rules as other graphics.
- **"Captions only" when the request says so** — add captions for Ron's own voice only. Do not caption meme audio, movie clips or other inserted audio; add no graphics, zooms, SFX or grading.

## Content planning
- Calendar, trend pulls, metrics and the weekly loop: `content/README.md`. Calendar rows: `content/content_calendar.csv`.
- Ron's working copy lives in his Google Drive folder https://drive.google.com/drive/folders/1SFXyvvzMT5uYhDMF_wQmV3I96TdqBeq2 — keep it there and update it each week. The live calendar is the Google Sheet "Ron — Content Calendar & Tracker" (file ID `15Z8c2w5XBNL-v2lsqxVo-yA2aWs_IYawTyhQawrEv3M`). Weekly: read the Sheet first (Ron types metrics there), merge into `content/content_calendar.csv`, then write new/changed rows back into the same Sheet with the Google Sheets connector (edit in place; don't create copies). Tab `Calendar`: columns AF:AH (engagement/save/share rate) are live formulas on every planned row (rows 2–29 as of Nov 2026) — extend them to new rows, never overwrite with values; `outlier_x` (AI) is filled by Claude weekly (views ÷ median of the previous 10 reels). Cells must not start with `'`, `=`, `+`, `-` or `@` (Sheets eats or evaluates them); use curly quotes.
- Two pillars: fitness trends (Mon/Wed/Fri/Sun) and science-based lifting (Tue/Thu/Sat, `content_type` prefixed "Lifting science ·"). Keep both when planning a new week; new rows go above the backlog rows.
- Weekly reel scripts: write them in `content/scripts/scripts_data.py` (English; Ron adapts to Tamil), then `python3 content/scripts/merge_meta.py <weeks.json>` and `node content/scripts/build_docs.js <weeks.json> content/scripts` for the Word files; `build_html.py` makes the Google Doc copies uploaded to the Drive subfolder "Reel Scripts" (folder ID `1GR4i2Z3mtHsBSd_EW-FFgq2CrNXAL9qV`). Script structure (v2, Ron's 7 beats, use for every script): 1 hook = curiosity in 0–3 s (number, price, known claim) + pattern interrupt in 3–6 s (the opposite of what they expect; rising SFX under the curiosity line, movie meme lands on the turn); 2 value by 13 s with the research on screen (authority folded in: 8 years in the gym, 5 consistent; never invent personal claims); 3 first problem; 4 false relief (half the fix); 5 second, bigger problem; 6 solution around 40–55 s closing every loop (save prompts and 'Comment KEYWORD' link tests go here); 7 emotional CTA ending on hope with a soft share ask naming who to send it to. Under 90 s; first and last 20–30 s fast-paced. v1 scripts are archived in the Drive subfolder "Archive (v1)".
- Every source added to the calendar must be checked (search result or the publisher page) before it is added. Never cite from memory.
- Engagement numbers are entered by hand. Do not connect to Ron's Instagram unless he asks.

## Format styles (each format has its own theme and editing style; keep them consistent)
Pick the style from the reel's format (calendar column `format`). Set it in the edit with `"theme"` (builder themes live in `design.json` → `themes`).
- **Desk** — red / black / white (`"theme": "desk_red"`). Level of motion set by the approved Ozempic sample (`videos/sample-ozempic/`): number/price counter in the hook over a rising riser, a hit on the pattern interrupt (strike, shake, stamp; a Remotion 3D hero shot when it fits), a 3D object for the key subject, a GSAP flowchart for the process, a 3D comparison for the payoff, and a sources line on screen for any figure. Facts on screen must be checked first.
- **Whiteboard** — the yellow / white house style below (reels 04 and 06): tracker, chips, steps and week graphics; graphics never over the board.
- **Terrace** — style not set yet. Before the first Terrace edit, propose a theme with still frames and get Ron's approval.
The house style below applies to every format except where the format's theme changes colours or motion.

## House style (approved in V2, refined since)
- English captions translated from Tamil/Thanglish, concise and faithful; never strengthen claims.
- Two-level hierarchy: medium white support line + large yellow hero word on key terms (plate / underline / mask / pop reveals). Poppins 600/800/900.
- Captions go in free space: bottom by default; a side column when Ron stands to one side of frame.
- Graphics sit in clear wall space, never over the face or a whiteboard.
- Follow CTA: only the **first** "follow me" gets a card, with Ron's avatar (`assets/avatar.jpg`) and `@ron_tamil`. No mid/end CTA cards.
- Sound effects: few, quiet, only where they fit the meaning (from Ron's library). Avoid Vine Boom and comedic sounds on serious points.
- Keep Ron's own zooms/cuts; add camera moves only when needed. Don't change speed unless asked.
- Deliver: 1080×1920, −14 LUFS master, plus a 720p review copy under 30 MB.
