"""Convert build/edit_src.json (original-speed times) -> build/edit_v2.json (sped-up timeline).
Durations (`dur`, `hold`) are already in output seconds and are not scaled."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = json.load(open(os.path.join(ROOT, "build/edit_src.json")))
k = E["speed"]
TIME_KEYS = {"t", "until", "hero_t", "value_t", "rest_t", "result_t", "follow_t", "s", "e"}


def conv(x):
    if isinstance(x, dict):
        return {key: (round(v / k, 3) if key in TIME_KEYS and isinstance(v, (int, float)) else conv(v)) for key, v in x.items()}
    if isinstance(x, list):
        return [conv(v) for v in x]
    return x


def nums(x):
    return [nums(v) for v in x] if isinstance(x, list) else (round(x / k, 3) if isinstance(x, (int, float)) else x)


out = {key: (conv(v) if key in ("takes", "beats", "gfx", "fx", "camera", "overlays") else v) for key, v in E.items()}
out["caption_left"] = nums(E.get("caption_left", []))
for g in out.get("gfx", []):
    if "switch" in g:
        g["switch"] = nums(g["switch"])
json.dump(out, open(os.path.join(ROOT, "build/edit_v2.json"), "w"), ensure_ascii=False, indent=1)
print("speed", k, "→ build/edit_v2.json")
