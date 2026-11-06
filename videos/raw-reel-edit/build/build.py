"""Generate index.html for the raw reel edit from edit.json + fine VAD.

Usage: python3 -I build/build.py   (run from the project root)
"""
import json, html, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = json.load(open(os.path.join(ROOT, "build/edit.json")))
VAD = json.load(open(os.path.join(ROOT, "build/vad_fine.json")))
W, H, FPS = 1080, 1920, 30
PAD = E["gap_keep"]
MAX_GAP = E["max_gap"]


def q(t):  # snap to frame grid
    return round(round(t * FPS) / FPS, 4)


# ---- 1. Cut each kept range into speech pieces, dropping internal gaps > MAX_GAP
segments = []  # dicts: src_s, src_e, out_s, range
t_out = 0.0
for ri, r in enumerate(E["ranges"]):
    pieces = [(max(s, r["s"]), min(e, r["e"])) for s, e in VAD if e > r["s"] and s < r["e"]]
    merged = []
    for s, e in pieces:
        if merged and s - merged[-1][1] <= MAX_GAP:
            merged[-1][1] = e
        else:
            merged.append([s, e])
    for k, (s, e) in enumerate(merged):
        s0 = s - (PAD if k == 0 else PAD / 2)
        e0 = e + (PAD if k == len(merged) - 1 else PAD / 2)
        s0, e0 = q(s0), q(e0)
        segments.append({"src_s": s0, "src_e": e0, "out_s": q(t_out), "range": ri, "first": k == 0})
        t_out = q(t_out + (e0 - s0))
TOTAL = q(t_out)


def to_out(t_src, ri):
    """Map a source time inside range ri to output time."""
    segs = [g for g in segments if g["range"] == ri]
    for g in segs:
        if t_src <= g["src_e"]:
            return g["out_s"] + max(0.0, t_src - g["src_s"])
    g = segs[-1]
    return g["out_s"] + g["src_e"] - g["src_s"]


# ---- 2. Caption cards: spread across each range's output time by text length
cards = []  # dicts: start, end, l1, l2, range, idx
for ri, r in enumerate(E["ranges"]):
    segs = [g for g in segments if g["range"] == ri]
    a = segs[0]["out_s"]
    b = segs[-1]["out_s"] + segs[-1]["src_e"] - segs[-1]["src_s"]
    starts_out = [g["out_s"] for g in segs]
    lens = [len(c[0]) + len(c[1]) for c in r["cards"]]
    tot = sum(lens)
    acc = a
    bounds = [a]
    for L in lens[:-1]:
        acc += (b - a) * L / tot
        # snap to a nearby speech-piece start (a natural phrase boundary)
        near = min(starts_out, key=lambda s: abs(s - acc))
        bounds.append(near if abs(near - acc) < 0.6 and near > bounds[-1] + 0.6 else acc)
    bounds.append(b)
    for ci, (l1, l2) in enumerate(r["cards"]):
        cards.append({"start": q(bounds[ci]), "end": q(bounds[ci + 1]), "l1": l1, "l2": l2, "range": ri, "idx": ci})


def card(ri, ci):
    return next(c for c in cards if c["range"] == ri and c["idx"] == ci)


# ---- 3. Motion graphics, anchored to caption cards
# kind: badge (big number top-left), chip (keyword callout), chips (several), stat, follow
G = [
    {"kind": "chip", "at": (0, 0), "text": "SKINNY FAT?", "style": "serif"},
    {"kind": "badge", "at": (0, 1), "text": "2", "label": "REASONS", "span": 1},
    {"kind": "badge", "at": (0, 2), "text": "1", "label": "RESISTANCE TRAINING", "span": 3},
    {"kind": "chip", "at": (0, 4), "text": "BUILD MUSCLE", "style": "accent"},
    {"kind": "chip", "at": (2, 1), "text": "+ CONFIDENCE", "style": "accent"},
    {"kind": "stat", "at": (2, 2), "big": "3–4", "small": "DAYS / WEEK", "span": 2},
    {"kind": "chip", "at": (3, 0), "text": "PROGRESSIVE OVERLOAD ↑", "style": "accent"},
    {"kind": "chips", "at": (4, 1), "items": ["BENCH PRESS", "SQUAT", "DEADLIFT"], "span": 2},
    {"kind": "badge", "at": (5, 0), "text": "2", "label": "POOR DIET", "span": 3},
    {"kind": "chip", "at": (6, 1), "text": "PROTEIN-RICH WHOLE FOODS", "style": "accent", "span": 2},
    {"kind": "chip", "at": (7, 1), "text": "HORMONAL BALANCE", "style": "serif"},
    {"kind": "chip", "at": (8, 0), "text": "HEALTHY FATS · NUTS", "style": "accent"},
    {"kind": "chip", "at": (9, 0), "text": "MAINTENANCE CALORIES", "style": "serif"},
    {"kind": "stat", "at": (10, 0), "big": "−100–200", "small": "KCAL · ABOVE 15% BODY FAT", "span": 2, "pink": True},
    {"kind": "stat", "at": (11, 0), "big": "+100", "small": "KCAL · BELOW 15% BODY FAT", "span": 2, "pink": True},
    {"kind": "chip", "at": (12, 1), "text": "PATIENCE", "style": "serif"},
    {"kind": "follow", "at": (15, 0), "span": 2},
]

# ---- 4. HTML
out = []
o = out.append
o(f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>Skinny Fat Reel</title>
    <script src="assets/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Poppins"; font-weight: 500; src: url("assets/fonts/poppins-latin-500-normal.woff2") format("woff2"); }}
      @font-face {{ font-family: "Poppins"; font-weight: 700; src: url("assets/fonts/poppins-latin-700-normal.woff2") format("woff2"); }}
      @font-face {{ font-family: "Poppins"; font-weight: 800; src: url("assets/fonts/poppins-latin-800-normal.woff2") format("woff2"); }}
      @font-face {{ font-family: "DM Serif Display"; font-style: italic; font-weight: 400; src: url("assets/fonts/dm-serif-display-latin-400-italic.woff2") format("woff2"); }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: {W}px; height: {H}px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; font-family: "Poppins", sans-serif; }}
      #push, #cam {{ position: absolute; inset: 0; transform-origin: 50% 32%; }}
      #cam video {{ position: absolute; left: 0; top: 0; width: {W}px; height: {H}px; object-fit: cover; }}
      #vignette {{ position: absolute; inset: 0; pointer-events: none;
        background: linear-gradient(to bottom, rgba(0,0,0,0) 55%, rgba(0,0,0,0.38) 100%); }}
      .cap {{ position: absolute; left: 40px; right: 40px; top: 1330px; text-align: center; }}
      .cap .l1, .cap .l2 {{ display: block; font-weight: 700; line-height: 1.22; letter-spacing: -0.01em;
        text-shadow: 0 3px 10px rgba(0,0,0,0.85), 0 0 2px rgba(0,0,0,0.9); text-wrap: balance; }}
      .cap .l1 {{ color: #ffffff; font-size: 44px; }}
      .cap .l2 {{ color: #f8e71c; font-size: 42px; margin-top: 4px; }}
      .g {{ position: absolute; }}
      .badge {{ left: 56px; top: 150px; display: flex; align-items: center; gap: 18px; }}
      .badge .num {{ position: relative; width: 118px; height: 118px; display: flex; align-items: center; justify-content: center;
        color: #fff; font-weight: 800; font-size: 84px; }}
      .badge .num svg {{ position: absolute; inset: -8px; width: 134px; height: 134px; }}
      .badge .lbl {{ color: #fff; font-weight: 800; font-size: 36px; letter-spacing: 0.04em;
        text-shadow: 0 3px 12px rgba(0,0,0,0.7); }}
      .chipwrap {{ left: 0; right: 0; top: 1150px; display: flex; justify-content: center; gap: 18px; }}
      .chip {{ padding: 14px 30px; border-radius: 16px; font-weight: 800; font-size: 44px; letter-spacing: 0.02em; color: #111;
        background: #f8e71c; box-shadow: 0 10px 30px rgba(0,0,0,0.35); }}
      .chip.serif {{ background: none; box-shadow: none; padding: 0; color: #fff; font-family: "DM Serif Display", serif;
        font-style: italic; font-weight: 400; font-size: 92px; letter-spacing: 0; text-shadow: 0 4px 18px rgba(0,0,0,0.65); }}
      .chips .chip {{ font-size: 36px; padding: 12px 24px; background: #fff; }}
      .stat {{ left: 0; right: 0; top: 1080px; display: flex; justify-content: center; }}
      .stat .box {{ display: flex; align-items: center; gap: 22px; padding: 18px 34px; border-radius: 18px; background: #fff;
        box-shadow: 0 12px 34px rgba(0,0,0,0.35); }}
      .stat.pink .box {{ background: #e5007e; }}
      .stat .big {{ font-weight: 800; font-size: 76px; color: #111; letter-spacing: -0.02em; }}
      .stat .small {{ font-weight: 700; font-size: 28px; color: #111; letter-spacing: 0.05em; max-width: 300px; line-height: 1.15; }}
      .stat.pink .big, .stat.pink .small {{ color: #fff; }}
      .follow {{ left: 0; right: 0; top: 1130px; display: flex; justify-content: center; }}
      .follow .card {{ display: flex; align-items: center; gap: 20px; padding: 16px 18px 16px 18px; border-radius: 22px; background: #fff;
        box-shadow: 0 12px 34px rgba(0,0,0,0.35); }}
      .follow .av {{ width: 72px; height: 72px; border-radius: 50%; background: linear-gradient(135deg, #f8e71c, #e5007e); }}
      .follow .txt {{ font-weight: 700; font-size: 32px; color: #111; }}
      .follow .btn {{ position: relative; width: 210px; height: 64px; border-radius: 14px; overflow: hidden; }}
      .follow .btn span {{ position: absolute; inset: 0; display: flex; align-items: center; justify-content: center;
        font-weight: 700; font-size: 30px; border-radius: 14px; }}
      .follow .b1 {{ background: #0095f6; color: #fff; }}
      .follow .b2 {{ background: #efefef; color: #111; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}" data-fps="{FPS}">
      <div id="push"><div id="cam">""")
for i, g in enumerate(segments):
    o(f'        <video id="v{i}" class="clip" src="{E["source"]}" data-start="{g["out_s"]}" data-duration="{q(g["src_e"]-g["src_s"])}" '
      f'data-media-start="{g["src_s"]}" data-track-index="{i % 2}" playsinline data-has-audio="true"></video>')
o('      </div></div>\n      <div id="vignette"></div>')

for k, c in enumerate(cards):
    o(f'      <div id="cap{k}" class="cap clip" data-start="{c["start"]}" data-duration="{q(c["end"]-c["start"])}" data-track-index="5">'
      f'<span class="l1">{html.escape(c["l1"])}</span><span class="l2">{html.escape(c["l2"])}</span></div>')

CIRCLE = ('<svg viewBox="0 0 134 134"><path class="draw" d="M67 8 C 104 6, 128 32, 126 68 C 124 104, 98 128, 64 126 '
          'C 30 124, 8 100, 9 66 C 10 34, 34 12, 72 10" fill="none" stroke="#f8e71c" stroke-width="7" stroke-linecap="round"/></svg>')
gfx_anim = []
sfx = []
for k, g in enumerate(G):
    c0 = card(*g["at"])
    span = g.get("span", 1)
    last = next((c for c in cards if c["range"] == c0["range"] and c["idx"] == c0["idx"] + span - 1), c0)
    st = q(c0["start"] + 0.1)
    du = q(last["end"] - st - 0.05)
    gid = f"g{k}"
    kind = g["kind"]
    if kind == "badge":
        inner = f'<div class="num">{CIRCLE}<span>{g["text"]}</span></div><div class="lbl">{html.escape(g["label"])}</div>'
        o(f'      <div id="{gid}" class="g badge clip" data-start="{st}" data-duration="{du}" data-track-index="6">{inner}</div>')
    elif kind == "chip":
        o(f'      <div id="{gid}" class="g chipwrap clip" data-start="{st}" data-duration="{du}" data-track-index="7">'
          f'<div class="chip {g.get("style","")}">{html.escape(g["text"])}</div></div>')
    elif kind == "chips":
        items = "".join(f'<div class="chip">{html.escape(x)}</div>' for x in g["items"])
        o(f'      <div id="{gid}" class="g chipwrap chips clip" data-start="{st}" data-duration="{du}" data-track-index="7">{items}</div>')
    elif kind == "stat":
        o(f'      <div id="{gid}" class="g stat {"pink" if g.get("pink") else ""} clip" data-start="{st}" data-duration="{du}" data-track-index="7">'
          f'<div class="box"><div class="big">{html.escape(g["big"])}</div><div class="small">{html.escape(g["small"])}</div></div></div>')
    elif kind == "follow":
        o(f'      <div id="{gid}" class="g follow clip" data-start="{st}" data-duration="{du}" data-track-index="7">'
          f'<div class="card"><div class="av"></div><div class="txt">Follow for more fitness tips</div>'
          f'<div class="btn" data-layout-allow-overlap><span class="b2">Following</span><span class="b1">Follow</span></div></div></div>')
    gfx_anim.append((gid, kind, st, du))
    sfx.append(st)

# whip into reason 2 (range 5) + whoosh
whip_t = next(g["out_s"] for g in segments if g["range"] == 5)
for k, t in enumerate(sfx):
    o(f'      <audio id="pop{k}" src="assets/pop.wav" data-start="{t}" data-duration="0.09" data-track-index="20" data-volume="0.5"></audio>')
o(f'      <audio id="whoosh0" src="assets/whoosh.wav" data-start="{q(max(0, whip_t-0.2))}" data-duration="0.45" data-track-index="21" data-volume="0.7"></audio>')
o("    </div>")

# ---- 5. Timeline
js = ["      const tl = gsap.timeline({ paused: true });"]
# camera: alternate wide / punch-in at each cut; segments under 1.2s keep the previous framing
zoom = 1.0
prev_range = None
for g in segments:
    dur = g["src_e"] - g["src_s"]
    if g["out_s"] == 0 or dur >= 1.2 or g["range"] != prev_range:
        zoom = 1.16 if zoom == 1.0 else 1.0
    prev_range = g["range"]
    js.append(f'      tl.set("#cam", {{ scale: {zoom} }}, {g["out_s"]});')
# slow push-in across the hook
js.append(f'      tl.fromTo("#push", {{ scale: 1.0 }}, {{ scale: 1.08, duration: {card(0,0)["end"]}, ease: "none" }}, 0);')
# whip into reason 2
js.append(f'      tl.fromTo("#push", {{ filter: "blur(18px)", y: -60 }}, {{ filter: "blur(0px)", y: 0, duration: 0.28, ease: "power2.out", immediateRender: false }}, {whip_t});')
# black & white emphasis on the "poor diet" consequence
bw = card(5, 2)
js.append(f'      tl.to("#push", {{ filter: "grayscale(1) contrast(1.08)", duration: 0.2 }}, {bw["start"]});')
js.append(f'      tl.to("#push", {{ filter: "grayscale(0) contrast(1)", duration: 0.2 }}, {q(bw["end"]-0.2)});')
# captions: quick pop-in
for k, c in enumerate(cards):
    js.append(f'      tl.fromTo("#cap{k} .l1", {{ y: 16, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.18, ease: "power2.out" }}, {c["start"]});')
    js.append(f'      tl.fromTo("#cap{k} .l2", {{ y: 16, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.18, ease: "power2.out" }}, {q(c["start"]+0.06)});')
for gid, kind, st, du in gfx_anim:
    if kind == "badge":
        js.append(f'      tl.fromTo("#{gid} .num", {{ scale: 0.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.2)" }}, {st});')
        js.append(f'      tl.fromTo("#{gid} .draw", {{ strokeDasharray: 420, strokeDashoffset: 420 }}, {{ strokeDashoffset: 0, duration: 0.5, ease: "power2.inOut" }}, {q(st+0.1)});')
        js.append(f'      tl.fromTo("#{gid} .lbl", {{ x: -24, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.3, ease: "power2.out" }}, {q(st+0.2)});')
    elif kind == "chips":
        js.append(f'      tl.fromTo("#{gid} .chip", {{ scale: 0.6, opacity: 0, y: 20 }}, {{ scale: 1, opacity: 1, y: 0, duration: 0.3, stagger: 0.18, ease: "back.out(2)" }}, {st});')
    elif kind == "stat":
        js.append(f'      tl.fromTo("#{gid} .box", {{ scale: 0.7, opacity: 0, y: 30 }}, {{ scale: 1, opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.8)" }}, {st});')
    elif kind == "follow":
        js.append(f'      tl.fromTo("#{gid} .card", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }}, {st});')
        js.append(f'      tl.to("#{gid} .b1", {{ opacity: 0, duration: 0.15 }}, {q(st+1.4)});')
        js.append(f'      tl.fromTo("#{gid} .btn", {{ scale: 1 }}, {{ scale: 0.92, duration: 0.08, yoyo: true, repeat: 1 }}, {q(st+1.3)});')
    else:
        js.append(f'      tl.fromTo("#{gid} .chip", {{ scale: 0.75, opacity: 0, y: 24 }}, {{ scale: 1, opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }}, {st});')
js.append('      window.__timelines["main"] = tl;')
o("    <script>\n" + "\n".join(js) + "\n    </script>\n  </body>\n</html>")

open(os.path.join(ROOT, "index.html"), "w").write("\n".join(out) + "\n")
json.dump({"total": TOTAL, "segments": segments, "cards": cards}, open(os.path.join(ROOT, "build/timeline.json"), "w"), indent=1)
print(f"segments={len(segments)} cards={len(cards)} graphics={len(G)} total={TOTAL:.2f}s")
