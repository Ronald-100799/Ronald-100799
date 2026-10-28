"""Fetch B-roll from Pexels for every `broll` entry in edit_v2.json that has a `query` but no local file yet.

Needs PEXELS_API_KEY in the environment and api.pexels.com / videos.pexels.com reachable.
Picks a portrait (or squarest available) HD clip at least as long as the insert, downloads it,
normalises it to 1080x1920 / 30 fps / short GOP, and records credits in assets/broll/CREDITS.md.

Usage (from the project root):
  python3 -I build/fetch_broll.py            # fetch missing clips
  python3 -I build/fetch_broll.py --list     # show candidates per query without downloading
"""
import json, os, subprocess, sys, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EDIT = os.path.join(ROOT, "build/edit_v2.json")
OUT = os.path.join(ROOT, "assets/broll")
KEY = os.environ.get("PEXELS_API_KEY")
LIST_ONLY = "--list" in sys.argv


def api(query, per_page=15):
    url = "https://api.pexels.com/videos/search?" + urllib.parse.urlencode(
        {"query": query, "orientation": "portrait", "size": "medium", "per_page": per_page})
    req = urllib.request.Request(url, headers={"Authorization": KEY, "User-Agent": "reel-builder"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["videos"]


def best_file(video):
    files = [f for f in video["video_files"] if f.get("file_type") == "video/mp4" and f.get("width") and f.get("height")]
    portrait = [f for f in files if f["height"] >= f["width"]] or files
    hd = [f for f in portrait if f["height"] >= 1280] or portrait
    return min(hd, key=lambda f: abs(f["height"] - 1920))


def main():
    if not KEY:
        sys.exit("PEXELS_API_KEY is not set — add it under the environment's Environment variables.")
    E = json.load(open(EDIT))
    os.makedirs(OUT, exist_ok=True)
    credits = []
    used = set()
    for n, b in enumerate(E.get("broll", [])):
        need = b["until"] - b["t"] + 0.5
        if b.get("file") and os.path.exists(os.path.join(ROOT, b["file"])) and not LIST_ONLY:
            continue
        vids = [v for v in api(b["query"]) if v["duration"] >= need and v["id"] not in used]
        if LIST_ONLY:
            print(f'[{n}] {b["query"]!r} needs {need:.1f}s:')
            for v in vids[:5]:
                f = best_file(v)
                print(f'    {v["id"]}  {v["duration"]}s  {f["width"]}x{f["height"]}  {v["url"]}')
            continue
        if not vids:
            print(f'[{n}] no clip long enough for {b["query"]!r}; edit the query'); continue
        pick = next((v for v in vids if str(v["id"]) == str(b.get("pexels_id"))), vids[0])
        used.add(pick["id"])
        f = best_file(pick)
        raw = os.path.join(OUT, f'{pick["id"]}_src.mp4')
        dst = f'assets/broll/{pick["id"]}.mp4'
        urllib.request.urlretrieve(f["link"], raw)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-an",
                        "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-g", "15", "-movflags", "+faststart",
                        os.path.join(ROOT, dst)], check=True)
        os.remove(raw)
        b["file"], b["pexels_id"] = dst, pick["id"]
        credits.append(f'- {dst}: "{b["query"]}" — video by {pick["user"]["name"]} on Pexels ({pick["url"]})')
        print(f'[{n}] {b["query"]!r} -> {dst} ({f["width"]}x{f["height"]}, {pick["duration"]}s)')
    if not LIST_ONLY:
        json.dump(E, open(EDIT, "w"), ensure_ascii=False, indent=1)
        if credits:
            with open(os.path.join(OUT, "CREDITS.md"), "a") as fh:
                fh.write("\n".join(credits) + "\n")


if __name__ == "__main__":
    main()
