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


out = {key: (conv(v) if key in ("takes", "beats", "gfx", "fx", "camera") else v) for key, v in E.items()}
json.dump(out, open(os.path.join(ROOT, "build/edit_v2.json"), "w"), ensure_ascii=False, indent=1)
print("speed", k, "→ build/edit_v2.json")
