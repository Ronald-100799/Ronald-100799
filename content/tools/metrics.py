"""Fill the calculated columns in content_calendar.csv and write a weekly report.

You type the raw numbers from Instagram Insights (views, reach, likes, comments,
shares, saves, follows_gained, avg_watch_time_s, skip_rate_pct). This script fills:
  engagement_rate_pct = (likes + comments + shares + saves) / reach * 100
  save_rate_pct, share_rate_pct = saves or shares / reach * 100
  outlier_x = views / median views of your previous 10 posted reels (above 2x = repeat it)
and writes content/reports/<date>.md comparing formats and content types.

Run:  python content/tools/metrics.py
"""
import csv
import datetime as dt
import os
import statistics as st

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAL = os.path.join(ROOT, "content_calendar.csv")


def num(v):
    try:
        return float(str(v).replace(",", "").strip())
    except ValueError:
        return None


def main():
    with open(CAL, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        cols, rows = reader.fieldnames, list(reader)

    posted = [r for r in rows if num(r.get("views")) is not None]
    posted.sort(key=lambda r: r.get("posted_at") or r.get("post_date") or "")
    history = []
    for r in posted:
        views, reach = num(r["views"]), num(r.get("reach")) or num(r["views"])
        acts = [num(r.get(k)) or 0 for k in ("likes", "comments", "shares", "saves")]
        if reach:
            r["engagement_rate_pct"] = f"{sum(acts) / reach * 100:.2f}"
            r["save_rate_pct"] = f"{(num(r.get('saves')) or 0) / reach * 100:.2f}"
            r["share_rate_pct"] = f"{(num(r.get('shares')) or 0) / reach * 100:.2f}"
        base = history[-10:]
        r["outlier_x"] = f"{views / st.median(base):.2f}" if len(base) >= 3 and st.median(base) else ""
        history.append(views)

    with open(CAL, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    os.makedirs(os.path.join(ROOT, "reports"), exist_ok=True)
    out = os.path.join(ROOT, "reports", f"{dt.date.today().isoformat()}.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(f"# Performance report — {dt.date.today().isoformat()}\n\n")
        f.write(f"Posted reels with numbers: {len(posted)}\n\n")
        for key in ("format", "content_type", "goal"):
            f.write(f"## By {key}\n\n| {key} | reels | median views | avg engagement % | avg save % | avg share % |\n|---|---|---|---|---|---|\n")
            groups = {}
            for r in posted:
                groups.setdefault(r.get(key) or "?", []).append(r)
            for g, rs in sorted(groups.items(), key=lambda kv: -st.median([num(x["views"]) for x in kv[1]])):
                avg = lambda c: st.mean([num(x.get(c)) or 0 for x in rs])
                f.write(f"| {g} | {len(rs)} | {st.median([num(x['views']) for x in rs]):,.0f} | "
                        f"{avg('engagement_rate_pct'):.2f} | {avg('save_rate_pct'):.2f} | {avg('share_rate_pct'):.2f} |\n")
            f.write("\n")
        top = sorted([r for r in posted if r.get("outlier_x")], key=lambda r: -num(r["outlier_x"]))[:5]
        if top:
            f.write("## Outliers (views vs your recent median)\n\n")
            for r in top:
                f.write(f"- {r['outlier_x']}x — {r['topic']} ({r['format']}, {r['content_type']})\n")
    print(f"updated {len(posted)} posted rows; report: {out}")


if __name__ == "__main__":
    main()
