# Content system — @ron_tamil

Everything for planning, researching and tracking reels. Ron shoots; Claude edits (see `videos/`).

## Files

| File | What it is |
|---|---|
| `content_calendar.csv` | The calendar + tracker. One row per reel. Open in Google Sheets/Excel. |
| `trends/<date>.md` / `_rising.csv` / `_now.csv` | Weekly Google + YouTube trend pull for Tamil Nadu (auto, Mondays). |
| `reports/<date>.md` | Performance report written by `tools/metrics.py`. |
| `tools/weekly_trends.py` | Trend pull (trendspyg). |
| `tools/metrics.py` | Fills the calculated columns + writes the report. |
| `tools/openverse_sfx.py` | Finds and saves openly-licensed sound effects (Openverse) with a licence ledger. |

## Weekly loop (≈20 minutes of your time)

1. **Monday 07:00 IST** — GitHub Action pulls trends into `trends/`. (Runs once the workflow is on the default branch.)
2. **Monday** — ask Claude: *"Plan next week from the new trends."* Claude reads `trends/`, researches sources, and adds/updates rows (topic, hook, angle, why-now, platform, audience opinion, sources).
3. **You shoot** the 4 reels. Send footage → Claude edits (full edit by default).
4. **After posting** — paste each reel's link and fill the raw numbers from Instagram Insights after ~7 days:
   `views, reach, likes, comments, shares, saves, follows_gained, avg_watch_time_s, skip_rate_pct`.
5. Run `python content/tools/metrics.py` (or ask Claude). It fills `engagement_rate_pct, save_rate_pct, share_rate_pct, outlier_x` and writes `reports/<date>.md`.
6. Anything with **outlier_x ≥ 2** → make a follow-up or part 2 within 2 weeks.

## Column guide

- **format** — Desk / Terrace / Whiteboard. **content_type** — Authority, Reaction, Hook stack, Humour tips, Teaching series.
- **why_now_trend_signal** — the dated reason this topic is hot (news, festival, season, trend data).
- **trending_on** — where the conversation is (Google/YouTube search, News, Instagram comments…). Rows say "verify with content/trends" until the weekly pull confirms it.
- **audience_opinion** — the debate in one line (what people believe vs. what they fear). Desk research; confirm from your own comments.
- **primary_source_url** — a paper or official guideline to quote on screen. Every source in the calendar was checked before it was added; open it and read the abstract before you script.
- **goal** — the one metric this reel is built for: saves (teaching), shares (relatable/humour), comments (questions), follows (series/authority).
- **status** — Backlog → Planned → Scripted → Shot → Edited → Posted.
- **outlier_x** — views ÷ median of your previous 10 reels. Compare yourself to yourself, not to big accounts.

## Weekly slot plan

Two pillars, 7 reels a week. **Fitness trends** (Mon/Wed/Fri/Sun) and **Lifting science** (Tue/Thu/Sat, `content_type` starts with "Lifting science ·").

| Day | Format | Pillar | Works best for |
|---|---|---|---|
| Mon | Desk | Fitness trends | Authority + reaction to the week's news (hook stack: 3 fast claims in the first 3 s) |
| Tue | Desk | Lifting science | One study broken down, or a gym myth reacted to |
| Wed | Whiteboard | Fitness trends | "Gym Basics Ep-N": one concept per episode |
| Thu | Whiteboard | Lifting science | "Lifting Science Ep-N" (LS Ep-N): one training variable per episode |
| Fri | Terrace | Fitness trends | Humour + hacks, relatable, built to be shared |
| Sat | Terrace | Lifting science | Humour myth-bust about lifting |
| Sun | Desk or Terrace | Fitness trends | Myth-bust or seasonal topic |

Seasonal days can swap slots (e.g. World Diabetes Day moves a Desk reel to Saturday).

## Fixing the whiteboard reels

- **Hook before the board.** Open on you (or a 1–2 s meme) with a myth or a question; reveal the board after the hook.
- **One idea per reel.** Ep-1 covered five ideas; split future boards into one number per episode.
- **Put the payoff number on screen early** ("6–10 sets", "1.6 g/kg") so viewers wait for the explanation.
- **Series + binge:** same title card, "Ep-N" in the first frame, pin Ep-1, and say "Ep-N+1 on Wednesday".
- **End with a check:** a quick quiz in the caption ("3×10@60 — volume?") drives comments.
- **Turn each board into a carousel** (same content, slides) — carousels collect saves.

## Automation — what's automatic and what isn't

- **Automatic:** weekly trend pull (GitHub Action); calculated columns + report (`metrics.py`); Claude can fill research columns every week (ask, or set up a weekly Claude routine).
- **Manual (for now):** engagement numbers. Pulling them automatically needs the Instagram Graph API with a token from your Creator/Business account. That means connecting your account, which you have not approved, so it stays manual until you decide otherwise.

## SFX tools

- **Openverse** (`tools/openverse_sfx.py`) — CC0 sound effects with a licence ledger. Needs `api.openverse.org` and `freesound.org` / `cdn.freesound.org` allowed in the cloud environment's network settings.
- **earshot** (github.com/Leonxlnx/earshot) — listens to a cut and suggests/aligns SFX. Not installed: it needs PyTorch (download.pytorch.org) and approval to run third-party code in this environment.
- Current library: `videos/reel-04/assets/sfx2/` (from your Drive folder). Rules in `/CLAUDE.md`.
