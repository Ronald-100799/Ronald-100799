"""Search Openverse (openverse.org) for openly licensed sound effects and save them
to the shared SFX library with a licence ledger.

  python content/tools/openverse_sfx.py "whoosh" --n 5             # list matches
  python content/tools/openverse_sfx.py "whoosh" --n 5 --download  # save to videos/_library/sfx/openverse/

Defaults to CC0 (no attribution needed). Use --license by,cc0 to include CC BY
(then credit the creator from ledger.csv in your caption). Openverse's API is
anonymous with rate limits, so keep requests small.
Needs network access to api.openverse.org and the audio hosts it returns
(mostly freesound.org / cdn.freesound.org).
"""
import argparse
import csv
import json
import os
import re
import urllib.parse
import urllib.request

API = "https://api.openverse.org/v1/audio/"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LIB = os.path.join(ROOT, "videos", "_library", "sfx", "openverse")


def search(q, n, licenses, max_s):
    params = {"q": q, "license": licenses, "category": "sound_effect", "page_size": min(max(n * 3, 10), 50)}
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(params),
                                 headers={"User-Agent": "ron-reels-sfx/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        res = json.load(r).get("results", [])
    keep = [x for x in res if (x.get("duration") or 0) <= max_s * 1000]
    return keep[:n]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--license", default="cc0")
    ap.add_argument("--max-seconds", type=float, default=4.0)
    ap.add_argument("--download", action="store_true")
    a = ap.parse_args()

    hits = search(a.query, a.n, a.license, a.max_seconds)
    for x in hits:
        print(f"{x['id']}  {x.get('duration', 0) / 1000:4.1f}s  {x.get('license')}  {x.get('title')!r}  by {x.get('creator')}")
    if not a.download:
        return
    os.makedirs(LIB, exist_ok=True)
    ledger = os.path.join(LIB, "ledger.csv")
    new = not os.path.exists(ledger)
    with open(ledger, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["file", "query", "title", "creator", "license", "license_url", "landing_url", "attribution"])
        for x in hits:
            ext = (x.get("filetype") or "mp3").lower()
            name = re.sub(r"[^a-z0-9]+", "-", f"{a.query}-{x.get('title', '')}".lower()).strip("-")[:60]
            path = os.path.join(LIB, f"{name}-{x['id'][:8]}.{ext}")
            req = urllib.request.Request(x["url"], headers={"User-Agent": "ron-reels-sfx/1.0"})
            with urllib.request.urlopen(req, timeout=60) as r, open(path, "wb") as out:
                out.write(r.read())
            w.writerow([os.path.relpath(path, ROOT), a.query, x.get("title"), x.get("creator"), x.get("license"),
                        x.get("license_url"), x.get("foreign_landing_url"), x.get("attribution")])
            print("saved", os.path.relpath(path, ROOT))


if __name__ == "__main__":
    main()
