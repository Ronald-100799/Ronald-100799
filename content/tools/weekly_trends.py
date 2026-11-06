"""Weekly Google Trends pull for the Tamil fitness niche (uses trendspyg).

Writes:
  content/trends/<date>_rising.csv   rising + top related searches per seed keyword (Tamil Nadu)
  content/trends/<date>_now.csv      fitness-related items from "Trending now" (India)
  content/trends/<date>.md           short summary to scan before planning the week

Run:  pip install "trendspyg[analysis]"  &&  python content/tools/weekly_trends.py
Google rate-limits Explore calls: keep the seed list short and run once a week.
"""
import csv
import datetime as dt
import os
import re
import sys
import time

from trendspyg import download_google_trends_explore, download_google_trends_rss

try:
    from trendspyg.exceptions import RateLimitError
except Exception:  # older/newer layouts
    class RateLimitError(Exception):
        pass

GEO = os.environ.get("TRENDS_GEO", "IN-TN")        # Tamil Nadu
TIMEFRAME = os.environ.get("TRENDS_TIMEFRAME", "today 3-m")
# (keyword, gprop): "" = Google web search, "youtube" = YouTube search
SEEDS = [
    ("weight loss", ""),
    ("protein", ""),
    ("gym", ""),
    ("diet", ""),
    ("creatine", ""),
    ("weight loss tamil", "youtube"),
    ("gym tamil", "youtube"),
]
FITNESS_WORDS = re.compile(
    r"gym|fit|diet|protein|weight|fat|muscle|workout|yoga|marathon|creatine|ozempic|semaglutide|"
    r"diabet|sugar|cholesterol|calorie|steps|run|walk|body|transformation|supplement|whey",
    re.I)
PAUSE_S = float(os.environ.get("TRENDS_PAUSE_S", "45"))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "trends")


def main():
    os.makedirs(OUT, exist_ok=True)
    today = dt.date.today().isoformat()
    rising_rows, now_rows, notes = [], [], []

    # 1) Trending now (India) — fast RSS path, no browser
    try:
        env = download_google_trends_rss(geo="IN", normalize=True)
        for t in env.get("trends", []):
            if FITNESS_WORDS.search(t.get("keyword", "")):
                news = (t.get("news") or [{}])[0]
                now_rows.append({"date": today, "keyword": t.get("keyword"), "volume_min": t.get("volume_min"),
                                 "headline": news.get("headline", ""), "url": news.get("url", "")})
        notes.append(f"Trending now (IN): {len(env.get('trends', []))} items, {len(now_rows)} fitness-related.")
    except Exception as e:  # keep going; Explore may still work
        notes.append(f"Trending now failed: {e}")

    # 2) Explore: related searches per seed (Tamil Nadu)
    for n, (kw, gprop) in enumerate(SEEDS):
        if n:
            time.sleep(PAUSE_S)
        src = "YouTube" if gprop == "youtube" else "Google"
        try:
            env = download_google_trends_explore(kw, geo=GEO, timeframe=TIMEFRAME, gprop=gprop,
                                                 include_geo=False, engine="auto", cache="disk", cookies="disk")
        except RateLimitError as e:
            notes.append(f"Rate-limited at '{kw}' ({src}); stopped early: {e}")
            break
        except Exception as e:
            notes.append(f"'{kw}' ({src}) failed: {e}")
            continue
        rq = env.get("related_queries") or {}
        for kind in ("rising", "top"):
            for q in rq.get(kind) or []:
                rising_rows.append({"date": today, "source": src, "geo": GEO, "seed": kw, "kind": kind,
                                    "query": q.get("query"), "value": q.get("formatted_value", q.get("value"))})
        notes.append(f"'{kw}' ({src}): {len(rq.get('rising') or [])} rising, {len(rq.get('top') or [])} top.")

    write(os.path.join(OUT, f"{today}_rising.csv"), rising_rows,
          ["date", "source", "geo", "seed", "kind", "query", "value"])
    write(os.path.join(OUT, f"{today}_now.csv"), now_rows, ["date", "keyword", "volume_min", "headline", "url"])

    with open(os.path.join(OUT, f"{today}.md"), "w", encoding="utf-8") as f:
        f.write(f"# Trends {today} ({GEO}, {TIMEFRAME})\n\n")
        f.write("\n".join(f"- {x}" for x in notes) + "\n\n## Rising searches (Breakout first)\n\n")
        rising = [r for r in rising_rows if r["kind"] == "rising"]
        rising.sort(key=lambda r: (str(r["value"]) != "Breakout", r["seed"]))
        for r in rising[:40]:
            f.write(f"- **{r['query']}** — {r['value']} ({r['source']}, seed: {r['seed']})\n")
        if now_rows:
            f.write("\n## Fitness items in India 'Trending now'\n\n")
            for r in now_rows:
                f.write(f"- {r['keyword']} (≥{r['volume_min']}) — {r['headline']}\n")
    print("\n".join(notes))
    return 0 if rising_rows or now_rows else 1


def write(path, rows, cols):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    sys.exit(main())
