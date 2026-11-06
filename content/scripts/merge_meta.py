"""Merge scripts_data.py with calendar rows into weeks.json for build_docs.js."""
import csv, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scripts_data import SCRIPTS

ROOT = os.path.dirname(os.path.abspath(__file__))
rows = {r["id"]: r for r in csv.DictReader(open(os.path.join(ROOT, "..", "content_calendar.csv"), encoding="utf-8"))}
weeks = {}
for rid, sc in SCRIPTS.items():
    r = rows[rid]
    words = sum(len(t.split()) for sec in sc["sections"] for typ, t in sec[3] if typ == "S")
    item = {"id": rid, "date": r["post_date"], "day": r["day"], "format": r["format"],
            "type": r["content_type"], "topic": r["topic"], "goal": r["goal"],
            "source": r["primary_source"], "url": r["primary_source_url"], "url2": r["secondary_source_url"],
            "words": words, "secs": round(words / 2.6 + 3), "link": sc.get("link"),
            "sections": [{"time": t, "label": l, "fast": f == "fast", "lines": ln} for t, l, f, ln in sc["sections"]]}
    weeks.setdefault(r["week_start"], []).append(item)
for w in weeks.values():
    w.sort(key=lambda x: x["date"])
json.dump(weeks, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print({k: len(v) for k, v in weeks.items()})
