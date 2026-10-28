"""Write build/TRANSCRIPT.md: kept speech (Tamil ASR) -> approved English caption -> output time."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = json.load(open(os.path.join(ROOT, "build/edit_v2.json")))
T = json.load(open(os.path.join(ROOT, "build/timeline.json")))
fmt = lambda t: f"{int(t // 60)}:{t % 60:05.2f}"
L = ["# Corrected transcript → English captions (V2)", "",
     "Tamil is Whisper large-v3 output per kept take (lightly cleaned in the take notes). Edit captions in `edit_v2.json` → `beats`.", ""]
caps = T["captions"]
for tk in [t for t in E["takes"] if t.get("keep")]:
    L += [f"## {tk['id']} · source {fmt(tk['s'])}–{fmt(tk['e'])}", "", f"**Spoken (Tamil/Thanglish):** {tk['ta']}", "",
          "| Output | Source | Caption (support) | Hero |", "|---|---|---|---|"]
    for c in caps:
        if tk["s"] - 0.4 <= c["src_t"] <= tk["e"] + 0.2:
            L.append(f"| {fmt(c['out_start'])}–{fmt(c['out_end'])} | {fmt(c['src_t'])} | {c['support'].replace('*', '')} | {c['hero'].replace('|', ' ')} |")
    L.append("")
L += ["## Flags for review", ""] + [f"- {f}" for f in E.get("flags", [])]
open(os.path.join(ROOT, "build/TRANSCRIPT.md"), "w").write("\n".join(L) + "\n")
print("ok", len(caps))
