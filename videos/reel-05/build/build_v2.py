"""V2 reel builder: edit_v2.json + design.json -> index.html, timeline.json, DECISIONS.md

Everything in edit_v2.json is anchored to SOURCE time (seconds in the original
camera file). This script cuts the kept takes into segments, maps every caption,
graphic, camera move and sound effect to OUTPUT time, and writes one
HyperFrames composition.

Usage (from the project root):  python3 -I build/build_v2.py [--edit EDIT.json --out FILE.html]
  A preview edit (a subset of takes) writes a separate composition; timings stay exact.
"""
import json, html, os, sys, subprocess, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "build/design.json")))
EDIT = sys.argv[sys.argv.index("--edit") + 1] if "--edit" in sys.argv else "build/edit_v2.json"
OUT_HTML = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "index.html"
E = json.load(open(os.path.join(ROOT, EDIT)))
VAD = json.load(open(os.path.join(ROOT, "build/vad_fine.json")))
W, H, FPS = D["canvas"]["w"], D["canvas"]["h"], D["canvas"]["fps"]
C, M, SZ, SAFE, F = D["color"], D["motion"], D["size"], D["safe"], D["font"]


def q(t):
    return round(round(t * FPS) / FPS, 4)


def esc(s):
    return html.escape(s, quote=True)


# ------------------------------------------------------------------ 1. segments
P = E["pacing"]
segments = []
t_out = 0.0
kept = [tk for tk in E["takes"] if tk.get("keep")]
for tk in kept:
    s_lo, s_hi = tk["s"], tk["e"]
    pieces = [[max(s, s_lo), min(e, s_hi)] for s, e in VAD if e > s_lo and s < s_hi]
    keep_pauses = tk.get("keep_pauses", [])  # source times of deliberate pauses
    merged = []
    for s, e in pieces:
        gap = s - merged[-1][1] if merged else None
        deliberate = merged and any(merged[-1][1] - 0.05 <= kp <= s + 0.05 for kp in keep_pauses)
        if merged and (gap < P["keep_pause"] or deliberate):
            merged[-1][1] = e
        else:
            merged.append([s, e])
    for k, (s, e) in enumerate(merged):
        pad_in = P["pad"] if k == 0 else P["inner_pad"]
        pad_out = P["pad"] if k == len(merged) - 1 else P["inner_pad"]
        s0, e0 = q(s - pad_in), q(e + pad_out)
        segments.append({"take": tk["id"], "src_s": s0, "src_e": e0, "out_s": q(t_out), "take_start": k == 0})
        t_out = q(t_out + e0 - s0)
TAIL = E.get("tail_hold", 0.6)


def in_kept(t):
    return any(tk["s"] - 0.4 <= t <= tk["e"] + 0.2 for tk in kept)


E["beats"] = [b for b in E["beats"] if in_kept(b["t"])]
E["gfx"] = [g for g in E.get("gfx", []) if in_kept(g["t"])]
E["fx"] = [f for f in E.get("fx", []) if in_kept(f["t"])]
E["camera"] = [c for c in E.get("camera", []) if in_kept(c["t"])]
E["broll"] = [b for b in E.get("broll", []) if in_kept(b["t"])]
E["overlays"] = [ov for ov in E.get("overlays", []) if in_kept(ov["t"])]
E["_in"] = in_kept
TOTAL = q(t_out + TAIL)


def to_out(t):
    """Map a source time to output time (snaps into the next kept segment)."""
    for g in segments:
        if t < g["src_s"]:
            return g["out_s"]
        if t <= g["src_e"]:
            return q(g["out_s"] + t - g["src_s"])
    g = segments[-1]
    return q(g["out_s"] + g["src_e"] - g["src_s"])


def seg_at(t_out_):
    for g in reversed(segments):
        if t_out_ >= g["out_s"] - 1e-6:
            return g
    return segments[0]


# ------------------------------------------------------------------ 2. per-clip grade + gain
cache_p = os.path.join(ROOT, "build/analysis_cache.json")
cache = json.load(open(cache_p)) if os.path.exists(cache_p) else {}


def wall_luma(t):
    key = f"luma:{t:.2f}"
    if key not in cache:
        raw = subprocess.run(
            ["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", os.path.join(ROOT, E["source_video"]),
             "-frames:v", "1", "-vf", "crop=200:300:20:40,scale=1:1", "-f", "rawvideo", "-pix_fmt", "gray", "-"],
            capture_output=True).stdout
        cache[key] = int(raw[0]) if raw else None
    return cache[key]


wv = wave.open(os.path.join(ROOT, E["source_audio"]))
SR = wv.getframerate()
audio = np.frombuffer(wv.readframes(wv.getnframes()), np.int16).reshape(-1, wv.getnchannels())[:, 0].astype(np.float32) / 32768


def speech_db(s, e):
    x = audio[int(s * SR):int(e * SR)]
    if len(x) < SR // 10:
        return None
    frames = x[: len(x) // 480 * 480].reshape(-1, 480)
    rms = np.sqrt((frames ** 2).mean(1) + 1e-12)
    loud = rms[rms > np.percentile(rms, 60)]  # speech frames only
    return float(20 * np.log10(loud.mean() + 1e-9))


levels = []
for g in segments:
    g["luma"] = wall_luma((g["src_s"] + g["src_e"]) / 2)
target_luma = float(np.percentile([g["luma"] for g in segments if g["luma"]], 75))  # match the brighter majority
for g in segments:
    lum = g["luma"]
    ratio = target_luma / lum if lum else 1.0
    g["bright"] = round(min(1.10, max(1.0, ratio)), 3) if ratio > 1.015 else 1.0
    g["db"] = speech_db(g["src_s"], g["src_e"])
    if g["db"] is not None:
        levels.append(g["db"])
ref_db = float(np.median(levels))
for g in segments:
    adj = 0.0 if g["db"] is None else max(-2.5, min(2.5, ref_db - g["db"]))
    g["gain"] = round(10 ** (adj / 20) * D["audio"].get("voice_gain", 1.0), 3)
json.dump(cache, open(cache_p, "w"), indent=0)

# ------------------------------------------------------------------ 3. camera
CAM = D["camera"]
cam_events = sorted(E.get("camera", []), key=lambda c: c["t"])
frames_by_seg = []
prev = "W"
for i, g in enumerate(segments):
    ev = [c for c in cam_events if c.get("frame") and g["src_s"] - 0.01 <= c["t"] <= g["src_e"]]
    if ev:
        fr = ev[0]["frame"]
    elif g["take_start"]:
        fr = prev  # a new take keeps framing unless the edit says otherwise
    else:
        fr = "M" if prev == "W" else "W"  # internal jump cut: subtle reframe hides the jump
    frames_by_seg.append(fr)
    prev = fr

# ------------------------------------------------------------------ 4. html helpers
out = []
o = out.append
js = []
J = js.append
sfx = []


def words_html(text, cls="w"):
    parts = []
    for tok in text.split(" "):
        acc = tok.startswith("*") and tok.rstrip(",.?!:;—").endswith("*")
        clean = tok.replace("*", "")
        parts.append(f'<span class="{cls}{" acc" if acc else ""}">{esc(clean)}</span>')
    return " ".join(parts)


def hero_size(text):
    n = max(len(text), 4)
    return int(max(SZ["hero_min"], min(SZ["hero_max"], SZ["hero_width"] / (0.68 * n))))


def add_sfx(name, t, vol, explicit=False):
    if explicit or E.get("auto_sfx", True):
        sfx.append((name, q(t), vol))


# ------------------------------------------------------------------ 5. captions
beats = sorted(E["beats"], key=lambda b: b["t"])
cap_rows = []
for k, b in enumerate(beats):
    st = to_out(b["t"])
    nxt = to_out(beats[k + 1]["t"]) if k + 1 < len(beats) else None
    seg_end = None
    for g in segments:
        if g["src_s"] - 0.01 <= b["t"] <= g["src_e"]:
            tk_segs = [x for x in segments if x["take"] == g["take"]]
            seg_end = q(tk_segs[-1]["out_s"] + tk_segs[-1]["src_e"] - tk_segs[-1]["src_s"])
    en = min(x for x in [nxt, b.get("until") and to_out(b["until"]), seg_end] if x)
    cap_rows.append((k, b, st, q(en)))

LEFT = [(to_out(a), to_out(z)) for a, z in E.get("caption_left", [])]
for k, b, st, en in cap_rows:
    left = any(a - 0.01 <= st < z for a, z in LEFT)
    hero = b.get("hero", "")
    fx = b.get("fx", "pop")
    sup_size = SZ["support_with_hero"] if hero else SZ["support"]
    hero_html = ""
    if hero:
        hlines = hero.split("|")
        hs = min(hero_size(l) for l in hlines)
        if left:
            hs = min(hs, int(D["left_captions"]["hero_width"] / (0.68 * max(len(l) for l in hlines))))
        inner = "".join(f'<span class="hw" style="font-size:{hs}px">{esc(l)}</span>' for l in hlines)
        if fx == "plate":
            inner = f'<i class="pl"></i>{inner}'
        if fx == "underline":
            inner += '<svg class="ul" viewBox="0 0 400 24" preserveAspectRatio="none"><path d="M4 16 C 120 6, 280 6, 396 14" /></svg>'
        allow = " data-layout-allow-overlap" if fx == "mask" else ""
        hero_html = f'<div class="hero fx-{fx}{" hero-first" if b.get("hero_first", True) else ""}"{allow}>{inner}</div>'
    sup = f'<div class="sup" style="font-size:{sup_size}px">{words_html(b["support"])}</div>' if b.get("support") else ""
    body = hero_html + sup if b.get("hero_first", True) else sup + hero_html
    o(f'      <div id="cap{k}" class="cap clip{" left" if left else ""}" data-start="{st}" data-duration="{q(en - st)}" data-track-index="10">'
      f'<div class="capin">{body}</div></div>')
    # support words: quick phrase reveal (word stagger), starts with the phrase
    J(f'      tl.fromTo("#cap{k} .w", {{ opacity: 0, y: {M["word_rise"]} }}, {{ opacity: 1, y: 0, duration: 0.22, '
      f'ease: "{M["enter_ease"]}", stagger: {M["word_stagger"]} }}, {st});')
    if hero:
        ht = max(st, to_out(b["hero_t"])) if b.get("hero_t") else st + 0.05
        ht = q(min(ht, en - 0.4))
        if fx == "plate":
            J(f'      tl.fromTo("#cap{k} .pl", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.26, ease: "power3.out" }}, {ht});')
            J(f'      tl.fromTo("#cap{k} .hw", {{ opacity: 0, x: -18 }}, {{ opacity: 1, x: 0, duration: 0.26, ease: "{M["enter_ease"]}", stagger: 0.06 }}, {q(ht + 0.1)});')
        elif fx == "mask":
            J(f'      tl.fromTo("#cap{k} .hw", {{ yPercent: 105, opacity: 0 }}, {{ yPercent: 0, opacity: 1, duration: 0.34, ease: "{M["enter_ease"]}", stagger: 0.06 }}, {ht});')
        elif fx == "underline":
            J(f'      tl.fromTo("#cap{k} .hw", {{ opacity: 0, scale: 1.18 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "{M["settle_ease"]}", stagger: 0.06 }}, {ht});')
            J(f'      tl.fromTo("#cap{k} .ul path", {{ strokeDashoffset: 420 }}, {{ strokeDashoffset: 0, duration: 0.38, ease: "power2.inOut" }}, {q(ht + 0.18)});')
        else:  # pop: scale-and-settle
            J(f'      tl.fromTo("#cap{k} .hw", {{ opacity: 0, scale: 1.32 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "{M["settle_ease"]}", stagger: 0.06 }}, {ht});')
        if b.get("pulse"):
            J(f'      tl.fromTo("#cap{k} .hw", {{ scale: 1 }}, {{ scale: 1.06, duration: 0.12, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false }}, {q(ht + 0.45)});')
        if b.get("sfx"):
            add_sfx(b["sfx"], ht, b.get("sfx_vol", 0.5))
    J(f'      tl.to("#cap{k} .capin", {{ opacity: 0, duration: 0.08, ease: "none" }}, {q(en - 0.08)});')

# ------------------------------------------------------------------ 6. graphics
gid = 0
for gx in E.get("gfx", []):
    gid += 1
    t0 = to_out(gx["t"])
    t1 = to_out(gx["until"])
    dur = q(t1 - t0)
    I = f"gx{gid}"
    typ = gx["type"]
    if typ == "section":
        lines = "".join(f'<div class="mk"><div class="sec-line">{esc(l)}</div></div>' for l in gx["title"])
        o(f'      <div id="{I}" class="gx clip" data-start="{t0}" data-duration="{dur}" data-track-index="20">'
          f'<div class="sec-big"><div class="mk"><div class="sec-num">{esc(gx["num"])}</div></div><i class="sec-bar"></i>{lines}</div>'
          f'<div class="sec-tag"><b>{esc(gx["num"])}</b><span>{esc(" ".join(gx["title"]))}</span></div></div>')
        J(f'      tl.fromTo("#{I} .sec-num", {{ yPercent: 105 }}, {{ yPercent: 0, duration: 0.42, ease: "{M["enter_ease"]}" }}, {t0});')
        J(f'      tl.fromTo("#{I} .sec-bar", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.36, ease: "power3.out" }}, {q(t0 + 0.18)});')
        J(f'      tl.fromTo("#{I} .sec-line", {{ yPercent: 105 }}, {{ yPercent: 0, duration: 0.34, ease: "{M["enter_ease"]}", stagger: 0.08 }}, {q(t0 + 0.26)});')
        rs = q(t0 + gx.get("hold", 2.4))
        J(f'      tl.to("#{I} .sec-big", {{ scale: 0.42, opacity: 0, duration: 0.3, ease: "{M["exit_ease"]}" }}, {rs});')
        J(f'      tl.fromTo("#{I} .sec-tag", {{ opacity: 0, x: -24 }}, {{ opacity: 1, x: 0, duration: 0.32, ease: "{M["enter_ease"]}" }}, {q(rs + 0.12)});')
        J(f'      tl.to("#{I} .sec-tag", {{ opacity: 0, y: -16, duration: {M["exit_dur"]}, ease: "{M["exit_ease"]}" }}, {q(t1 - 0.2)});')
        add_sfx("thump", t0, 0.55)
    elif typ == "list":
        rows = "".join(
            f'<div class="li" id="{I}r{n}"><b>{esc(it.get("idx", ""))}</b><span>{esc(it["text"])}</span></div>'
            for n, it in enumerate(gx["items"]))
        head = f'<div class="lh">{esc(gx["header"])}</div>' if gx.get("header") else ""
        o(f'      <div id="{I}" class="gx clip" data-start="{t0}" data-duration="{dur}" data-track-index="21">'
          f'<div class="list{" compact" if gx.get("compact") else ""}">{head}{rows}</div></div>')
        if head:
            J(f'      tl.fromTo("#{I} .lh", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "{M["enter_ease"]}" }}, {t0});')
        for n, it in enumerate(gx["items"]):
            ti = q(max(t0 + 0.1, to_out(it["t"])))
            J(f'      tl.fromTo("#{I}r{n}", {{ opacity: 0, x: -48 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "{M["enter_ease"]}" }}, {ti});')
            J(f'      tl.fromTo("#{I}r{n} b", {{ scale: 0.4 }}, {{ scale: 1, duration: 0.32, ease: "{M["settle_ease"]}" }}, {q(ti + 0.05)});')
            add_sfx("tick", ti, 0.5)
        J(f'      tl.to("#{I} .list", {{ opacity: 0, x: -30, duration: {M["exit_dur"]}, ease: "{M["exit_ease"]}" }}, {q(t1 - 0.2)});')
    elif typ == "week":
        days = "MTWTFSS"
        pills = "".join(f'<div class="day" id="{I}d{n}"><span>{d}</span><i></i></div>' for n, d in enumerate(days))
        o(f'      <div id="{I}" class="gx clip" data-start="{t0}" data-duration="{dur}" data-track-index="21">'
          f'<div class="week"><div class="wk-h"><b>{esc(gx["big"])}</b><span>{esc(gx["label"])}</span></div>'
          f'<div class="days">{pills}</div><div class="wk-rest">{esc(gx.get("rest_label", ""))}</div></div></div>')
        J(f'      tl.fromTo("#{I} .wk-h", {{ opacity: 0, y: 18 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "{M["enter_ease"]}" }}, {t0});')
        J(f'      tl.fromTo("#{I} .day", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "{M["enter_ease"]}", stagger: 0.04 }}, {q(t0 + 0.1)});')
        tt = q(t0 + 0.55)
        for n in gx["train"]:
            J(f'      tl.to("#{I}d{n}", {{ backgroundColor: "{C["yellow"]}", color: "{C["ink"]}", duration: 0.18 }}, {tt});')
            J(f'      tl.fromTo("#{I}d{n}", {{ scale: 1 }}, {{ scale: 1.12, duration: 0.1, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false }}, {tt});')
            add_sfx("tick", tt, 0.4)
            tt = q(tt + 0.16)
        for n in gx.get("optional", []):
            J(f'      tl.to("#{I}d{n}", {{ borderColor: "{C["yellow"]}", color: "{C["yellow"]}", duration: 0.2 }}, {tt});')
            tt = q(tt + 0.16)
        if gx.get("rest_t"):
            rt = to_out(gx["rest_t"])
            rest = [n for n in range(7) if n not in gx["train"] and n not in gx.get("optional", [])]
            for n in rest:
                J(f'      tl.to("#{I}d{n} i", {{ scaleX: 1, duration: 0.3, ease: "power3.out" }}, {rt});')
            J(f'      tl.fromTo("#{I} .wk-rest", {{ opacity: 0, y: 10 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "{M["enter_ease"]}" }}, {q(rt + 0.1)});')
        J(f'      tl.to("#{I} .week", {{ opacity: 0, y: 20, duration: {M["exit_dur"]}, ease: "{M["exit_ease"]}" }}, {q(t1 - 0.2)});')
    elif typ == "steps":
        bars = "".join(f'<div class="st" id="{I}s{n}"><i style="height:{h}px"></i><span>{esc(lbl)}</span></div>'
                       for n, (h, lbl) in enumerate(zip([40, 62, 84, 106], gx["labels"])))
        o(f'      <div id="{I}" class="gx clip" data-start="{t0}" data-duration="{dur}" data-track-index="21">'
          f'<div class="steps"><div class="st-h">{esc(gx["header"])}</div><div class="st-row">{bars}'
          f'<svg class="st-arrow" viewBox="0 0 520 130"><path d="M20 118 L 470 14" /><path d="M432 8 L 474 12 L 458 50" /></svg></div></div></div>')
        J(f'      tl.fromTo("#{I} .st-h", {{ opacity: 0, y: 16 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "{M["enter_ease"]}" }}, {t0});')
        J(f'      tl.fromTo("#{I} .st i", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.4, ease: "power3.out", stagger: 0.12 }}, {q(t0 + 0.15)});')
        J(f'      tl.fromTo("#{I} .st span", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2, stagger: 0.12 }}, {q(t0 + 0.3)});')
        J(f'      tl.fromTo("#{I} .st-arrow path", {{ strokeDashoffset: 520 }}, {{ strokeDashoffset: 0, duration: 0.45, ease: "power2.inOut" }}, {q(t0 + 0.7)});')
        add_sfx("rise", t0 + 0.15, 0.35)
        J(f'      tl.to("#{I} .steps", {{ opacity: 0, y: 20, duration: {M["exit_dur"]}, ease: "{M["exit_ease"]}" }}, {q(t1 - 0.2)});')
    elif typ == "gauge":
        def col(cfg, cls):
            down = cfg["dir"] == "down"
            return (f'<div class="gcol {cls} {"down" if down else "up"}"><div class="g-h">{esc(cfg["header"])}</div>'
                    f'<div class="g-plot"><i class="g-base"></i><i class="g-bar"></i>'
                    f'<div class="g-val">{esc(cfg["value"])}</div></div></div>')
        cols = (col(gx["compare"], "dim") if gx.get("compare") else "") + col(gx, "main")
        o(f'      <div id="{I}" class="gx clip" data-start="{t0}" data-duration="{dur}" data-track-index="21">'
          f'<div class="gauge{" two" if gx.get("compare") else ""}"><div class="g-maint">MAINTENANCE</div>{cols}</div></div>')
        J(f'      tl.fromTo("#{I} .gauge", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.32, ease: "{M["enter_ease"]}" }}, {t0});')
        J(f'      tl.fromTo("#{I} .g-base", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.36, ease: "power3.out" }}, {q(t0 + 0.1)});')
        vt = to_out(gx["value_t"]) if gx.get("value_t") else q(t0 + 0.5)
        J(f'      tl.fromTo("#{I} .main .g-bar", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.5, ease: "power3.out" }}, {vt});')
        J(f'      tl.fromTo("#{I} .main .g-val", {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.32, ease: "{M["settle_ease"]}" }}, {q(vt + 0.3)});')
        if gx.get("compare"):
            J(f'      tl.fromTo("#{I} .dim .g-bar", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.4, ease: "power3.out" }}, {q(t0 + 0.2)});')
        add_sfx("rise", vt, 0.35)
        J(f'      tl.to("#{I} .gauge", {{ opacity: 0, y: 20, duration: {M["exit_dur"]}, ease: "{M["exit_ease"]}" }}, {q(t1 - 0.2)});')
    elif typ == "build":
        rows = "".join(f'<div class="bd" id="{I}b{n}">{esc(it["text"])}</div>' for n, it in enumerate(gx["items"]))
        o(f'      <div id="{I}" class="gx clip" data-start="{t0}" data-duration="{dur}" data-track-index="21">'
          f'<div class="build">{rows}<div class="bd-eq"><span>{esc(gx["result"])}</span>'
          f'<svg class="ul" viewBox="0 0 400 24" preserveAspectRatio="none"><path d="M4 16 C 120 6, 280 6, 396 14" /></svg></div></div></div>')
        for n, it in enumerate(gx["items"]):
            ti = q(max(t0, to_out(it["t"])))
            J(f'      tl.fromTo("#{I}b{n}", {{ opacity: 0, y: 26 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "{M["enter_ease"]}" }}, {ti});')
            add_sfx("tick", ti, 0.45)
        rt = to_out(gx["result_t"])
        J(f'      tl.to("#{I} .bd", {{ opacity: 0.45, scale: 0.92, duration: 0.25, ease: "power2.out" }}, {rt});')
        J(f'      tl.fromTo("#{I} .bd-eq span", {{ opacity: 0, scale: 1.35 }}, {{ opacity: 1, scale: 1, duration: 0.34, ease: "{M["settle_ease"]}" }}, {rt});')
        J(f'      tl.fromTo("#{I} .bd-eq path", {{ strokeDashoffset: 420 }}, {{ strokeDashoffset: 0, duration: 0.4, ease: "power2.inOut" }}, {q(rt + 0.2)});')
        add_sfx("thump", rt, 0.45)
        J(f'      tl.to("#{I} .build", {{ opacity: 0, y: 20, duration: {M["exit_dur"]}, ease: "{M["exit_ease"]}" }}, {q(t1 - 0.2)});')
    elif typ == "tracker":
        tiles = "".join(f'<div class="tk-t" id="{I}t{n}">{esc(L)}</div>' for n, L in enumerate(gx["letters"]))
        labels = "".join(f'<div class="tk-l" id="{I}l{n}">{esc(w)}</div>' for n, w in enumerate(gx["labels"]))
        o(f'      <div id="{I}" class="gx clip" data-start="{t0}" data-duration="{dur}" data-track-index="20">'
          f'<div class="tracker"><div class="tk-row">{tiles}</div><div class="tk-lab">{labels}</div></div></div>')
        J(f'      tl.fromTo("#{I} .tk-t", {{ opacity: 0, y: -24 }}, {{ opacity: 1, y: 0, duration: 0.32, ease: "{M["enter_ease"]}", stagger: 0.06 }}, {t0});')
        sw = [to_out(x) for x in gx["switch"]] + [t1]
        for n in range(len(gx["letters"])):
            a, z = q(max(t0, sw[n])), q(sw[n + 1])
            J(f'      tl.to("#{I}t{n}", {{ backgroundColor: "{C["yellow"]}", color: "{C["ink"]}", scale: 1.12, duration: 0.25, ease: "{M["settle_ease"]}" }}, {a});')
            J(f'      tl.fromTo("#{I}l{n}", {{ opacity: 0, x: -20 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "{M["enter_ease"]}" }}, {q(a + 0.08)});')
            if n + 1 < len(gx["letters"]):
                J(f'      tl.to("#{I}t{n}", {{ backgroundColor: "rgba(12,12,14,0.62)", color: "rgba(255,255,255,0.55)", scale: 1, duration: 0.2 }}, {q(z - 0.05)});')
                J(f'      tl.to("#{I}l{n}", {{ opacity: 0, x: 20, duration: 0.18 }}, {q(z - 0.12)});')
            add_sfx("tick", a, 0.5)
        J(f'      tl.to("#{I} .tracker", {{ opacity: 0, y: -16, duration: {M["exit_dur"]}, ease: "{M["exit_ease"]}" }}, {q(t1 - 0.2)});')
    elif typ == "chips":
        chips = "".join(f'<div class="chip" id="{I}c{n}">{esc(it["text"])}</div>' for n, it in enumerate(gx["items"]))
        o(f'      <div id="{I}" class="gx clip" data-start="{t0}" data-duration="{dur}" data-track-index="21">'
          f'<div class="chips">{chips}</div></div>')
        for n, it in enumerate(gx["items"]):
            ti = q(max(t0, to_out(it["t"])))
            J(f'      tl.fromTo("#{I}c{n}", {{ opacity: 0, scale: 0.6, y: 16 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.3, ease: "{M["settle_ease"]}" }}, {ti});')
            add_sfx("tick", ti, 0.4)
        J(f'      tl.to("#{I} .chips", {{ opacity: 0, y: -12, duration: {M["exit_dur"]}, ease: "{M["exit_ease"]}" }}, {q(t1 - 0.2)});')
    elif typ == "endcard":
        av = (f'<div class="end-av"><img src="{D["avatar"]}" alt="" /></div>'
              if D.get("avatar") and os.path.exists(os.path.join(ROOT, D["avatar"])) else '<div class="end-av"></div>')
        o(f'      <div id="{I}" class="gx clip" data-start="{t0}" data-duration="{dur if gx.get("mini") else q(TOTAL - t0)}" data-track-index="22">'
          f'<div class="end">{av}<div class="end-txt"><b>{esc(D["end_card_text"])}</b>'
          f'<span class="end-handle">{esc(D["handle"])}</span></div>'
          f'<div class="end-btn" data-layout-allow-overlap><span class="b2" data-layout-allow-overlap>Following</span><span class="b1" data-layout-allow-overlap>Follow</span></div></div></div>')
        J(f'      tl.fromTo("#{I} .end", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "{M["enter_ease"]}" }}, {t0});')
        ft = to_out(gx["follow_t"]) if gx.get("follow_t") else q(t0 + 1.2)
        J(f'      tl.fromTo("#{I} .end-btn", {{ scale: 1 }}, {{ scale: 0.9, duration: 0.08, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false }}, {ft});')
        J(f'      tl.fromTo("#{I} .b2", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.01 }}, {q(ft + 0.07)});')
        J(f'      tl.to("#{I} .b1", {{ opacity: 0, duration: 0.14 }}, {q(ft + 0.08)});')
        add_sfx("tick", ft, 0.6)

# ------------------------------------------------------------------ 7. stylised fx on the picture
for fx in E.get("fx", []):
    t0 = to_out(fx["t"])
    if fx["type"] == "whip":
        J(f'      tl.fromTo("#fx", {{ filter: "blur(16px)", y: -70 }}, {{ filter: "blur(0px)", y: 0, duration: 0.3, ease: "power3.out", immediateRender: false }}, {t0});')
        add_sfx("swoosh", t0 - 0.12, 0.7)
    elif fx["type"] == "blurpush":
        J(f'      tl.fromTo("#fx", {{ filter: "blur(10px)", scale: 1.06 }}, {{ filter: "blur(0px)", scale: 1, duration: 0.36, ease: "power3.out", immediateRender: false }}, {t0});')
        add_sfx("swoosh", t0 - 0.1, 0.45)
    elif fx["type"] == "bw":
        t1 = to_out(fx["until"])
        J(f'      tl.fromTo("#fx", {{ filter: "grayscale(0)" }}, {{ filter: "grayscale(1)", duration: 0.2, immediateRender: false }}, {t0});')
        J(f'      tl.to("#fx", {{ filter: "grayscale(0)", duration: 0.2 }}, {q(t1 - 0.2)});')

# ------------------------------------------------------------------ 8. camera timeline
for i, g in enumerate(segments):
    J(f'      tl.set("#cam", {{ scale: {CAM[frames_by_seg[i]]} }}, {g["out_s"]});')
    J(f'      tl.set("#move", {{ scale: 1, transformOrigin: "50% 46%" }}, {g["out_s"]});')
for c in cam_events:
    if c.get("move") == "reset":
        J(f'      tl.to("#move", {{ scale: 1, duration: {c.get("dur", 0.35)}, ease: "power2.inOut" }}, {to_out(c["t"])});')
    elif c.get("move") == "cut":
        J(f'      tl.set("#move", {{ scale: 1, transformOrigin: "50% 46%" }}, {to_out(c["t"])});')
    if c.get("move") in ("push", "punch"):
        t0 = to_out(c["t"])
        g = seg_at(t0)
        seg_end = q(g["out_s"] + g["src_e"] - g["src_s"])
        org = c.get("origin", "50% 46%")
        J(f'      tl.set("#move", {{ transformOrigin: "{org}" }}, {t0});')
        if c["move"] == "push":
            d = q(min(c.get("dur", 3.0), seg_end - t0))
            J(f'      tl.to("#move", {{ scale: {c.get("amount", 1.06)}, duration: {d}, ease: "sine.inOut" }}, {t0});')
        else:
            J(f'      tl.to("#move", {{ scale: {c.get("amount", 1.12)}, duration: {c.get("dur", 0.28)}, ease: "power3.out" }}, {t0});')

# ------------------------------------------------------------------ 9. assemble document
G = D["grade"]
style = f"""
      @font-face {{ font-family: "Poppins"; font-weight: 600; src: url("assets/fonts/poppins-latin-600-normal.woff2") format("woff2"); }}
      @font-face {{ font-family: "Poppins"; font-weight: 800; src: url("assets/fonts/poppins-latin-800-normal.woff2") format("woff2"); }}
      @font-face {{ font-family: "Poppins"; font-weight: 900; src: url("assets/fonts/poppins-latin-900-normal.woff2") format("woff2"); }}
      @font-face {{ font-family: "Poppins"; font-weight: 900; font-style: italic; src: url("assets/fonts/poppins-latin-900-italic.woff2") format("woff2"); }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: {W}px; height: {H}px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; font-family: "Poppins", sans-serif; }}
      #fx, #grade, #move, #cam {{ position: absolute; inset: 0; transform-origin: 50% 46%; }}
      #grade {{ filter: contrast({G["contrast"]}) saturate({G["saturate"]}); }}
      #cam video {{ position: absolute; left: 0; top: 0; width: {W}px; height: {H}px; object-fit: cover; }}
      .brw {{ position: absolute; inset: 0; transform-origin: 50% 50%; filter: contrast({G["contrast"]}) saturate({G["saturate"]}); }}
      .broll {{ position: absolute; left: 0; top: 0; width: {W}px; height: {H}px; object-fit: cover; }}
      #shade {{ position: absolute; inset: 0; background: {D["shade"]}; }}
      .cap {{ position: absolute; left: {SAFE["left"]}px; right: {SAFE["right"]}px; bottom: {H - SAFE["bottom"]}px; }}
      .capin {{ display: flex; flex-direction: column; align-items: center; text-align: center; gap: 10px; }}
      .sup {{ font-weight: {F["support"]}; color: {C["white"]}; line-height: 1.22; text-wrap: balance; letter-spacing: -0.005em;
        text-shadow: {D["caption_shadow"]}; }}
      .sup .w {{ display: inline-block; }}
      .sup .acc {{ color: {C["yellow"]}; }}
      .hero {{ position: relative; display: inline-block; overflow: visible; line-height: 1.0; }}
      .hw {{ display: block; font-weight: {F["hero"]}; color: {C["yellow"]}; letter-spacing: -0.02em; text-transform: uppercase;
        text-shadow: {D["hero_shadow"]}; white-space: nowrap; }}
      .fx-mask {{ overflow: hidden; padding: 0 6px; }}
      .fx-plate {{ padding: 8px 22px 4px; }}
      .fx-plate .pl {{ position: absolute; inset: 0; background: {C["yellow"]}; border-radius: 10px; transform-origin: left center; }}
      .fx-plate .hw {{ position: relative; color: {C["ink"]}; text-shadow: none; }}
      .ul {{ position: absolute; left: 4%; width: 92%; bottom: -16px; height: 22px; overflow: visible; }}
      .ul path {{ fill: none; stroke: {C["white"]}; stroke-width: 7; stroke-linecap: round; stroke-dasharray: 420; }}
      .gx {{ position: absolute; inset: 0; }}
      .mk {{ overflow: hidden; }}
      .sec-big {{ position: absolute; left: {SAFE["left"]}px; top: {SAFE["top"] + 20}px; transform-origin: left top; }}
      .sec-num {{ font-weight: 900; font-size: 190px; line-height: 0.92; color: {C["yellow"]}; letter-spacing: -0.04em;
        text-shadow: 0 8px 28px rgba(0,0,0,0.45); }}
      .sec-bar {{ display: block; width: 150px; height: 8px; background: {C["white"]}; margin: 10px 0 14px; transform-origin: left; border-radius: 4px; }}
      .sec-line {{ font-weight: 800; font-size: 46px; line-height: 1.08; color: {C["white"]}; text-transform: uppercase; letter-spacing: 0.01em;
        text-shadow: 0 3px 14px rgba(0,0,0,0.7); }}
      .sec-tag {{ position: absolute; left: {SAFE["left"]}px; top: {SAFE["top"]}px; display: flex; align-items: center; gap: 14px;
        padding: 10px 20px 10px 10px; background: {C["plate"]}; border-radius: 14px; }}
      .sec-tag b {{ font-weight: 900; font-size: 34px; color: {C["ink"]}; background: {C["yellow"]}; border-radius: 9px; padding: 2px 12px; }}
      .sec-tag span {{ font-weight: 800; font-size: 26px; color: {C["white"]}; letter-spacing: 0.04em; text-transform: uppercase; }}
      .list {{ position: absolute; left: {SAFE["left"]}px; top: {D["layout"]["gfx_top"]}px; display: flex; flex-direction: column; gap: 14px; }}
      .lh {{ font-weight: 800; font-size: 30px; letter-spacing: 0.08em; color: {C["yellow"]}; text-transform: uppercase; text-shadow: 0 2px 10px rgba(0,0,0,0.6); }}
      .li {{ display: flex; align-items: center; gap: 16px; padding: 10px 26px 10px 10px; background: {C["plate"]}; border-radius: 14px; align-self: flex-start; }}
      .li b {{ font-weight: 900; font-size: 30px; color: {C["ink"]}; background: {C["yellow"]}; border-radius: 9px; padding: 4px 12px; }}
      .li span {{ font-weight: 800; font-size: 42px; color: {C["white"]}; text-transform: uppercase; letter-spacing: 0.01em; }}
      .week {{ position: absolute; left: {SAFE["left"]}px; right: {SAFE["right"]}px; top: {D["layout"]["gfx_top"]}px; display: flex; flex-direction: column; align-items: center; gap: 16px; }}
      .wk-h {{ display: flex; align-items: baseline; gap: 14px; text-shadow: 0 3px 14px rgba(0,0,0,0.6); }}
      .wk-h b {{ font-weight: 900; font-size: 92px; color: {C["yellow"]}; letter-spacing: -0.03em; line-height: 1; }}
      .wk-h span {{ font-weight: 800; font-size: 32px; color: {C["white"]}; letter-spacing: 0.06em; text-transform: uppercase; }}
      .days {{ display: flex; gap: 12px; }}
      .day {{ position: relative; width: 98px; height: 104px; border-radius: 16px; border: 3px solid rgba(255,255,255,0.55); background: {C["plate"]};
        color: {C["white"]}; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 40px; overflow: hidden; }}
      .day i {{ position: absolute; left: 0; right: 0; bottom: 0; height: 10px; background: {C["white"]}; transform: scaleX(0); transform-origin: left; }}
      .wk-rest {{ font-weight: 800; font-size: 28px; color: {C["white"]}; letter-spacing: 0.08em; text-transform: uppercase; text-shadow: 0 2px 10px rgba(0,0,0,0.7); }}
      .steps {{ position: absolute; left: {SAFE["left"]}px; right: {SAFE["right"]}px; top: {D["layout"]["gfx_top"]}px; display: flex; flex-direction: column; align-items: center; gap: 14px; }}
      .st-h {{ font-weight: 900; font-size: 58px; color: {C["yellow"]}; text-transform: uppercase; letter-spacing: -0.02em; text-shadow: 0 4px 18px rgba(0,0,0,0.55); line-height: 1; }}
      .st-row {{ position: relative; display: flex; align-items: flex-end; gap: 26px; height: 150px; }}
      .st {{ display: flex; flex-direction: column; align-items: center; gap: 10px; }}
      .st i {{ display: block; width: 92px; background: {C["white"]}; border-radius: 10px 10px 4px 4px; transform-origin: bottom; }}
      .st:last-of-type i {{ background: {C["yellow"]}; }}
      .st span {{ font-weight: 800; font-size: 24px; color: {C["white"]}; letter-spacing: 0.06em; background: {C["plate"]}; border-radius: 8px; padding: 2px 10px; }}
      .st-arrow {{ position: absolute; left: -10px; top: -20px; width: 500px; height: 130px; overflow: visible; }}
      .st-arrow path {{ fill: none; stroke: {C["yellow"]}; stroke-width: 7; stroke-linecap: round; stroke-linejoin: round; stroke-dasharray: 520; }}
      .gauge {{ position: absolute; left: {SAFE["left"]}px; right: {SAFE["right"]}px; top: {D["layout"]["gfx_top"]}px; display: flex; justify-content: center; gap: 24px;
        padding: 20px 26px; background: {C["plate"]}; border-radius: 22px; }}
      .g-maint {{ position: absolute; right: 26px; top: 108px; font-weight: 800; font-size: 20px; letter-spacing: 0.12em; color: {C["muted"]}; }}
      .gcol {{ flex: 1; display: flex; flex-direction: column; align-items: center; }}
      .g-h {{ font-weight: 800; font-size: 28px; color: {C["white"]}; letter-spacing: 0.03em; text-transform: uppercase; text-align: center; height: 40px; }}
      .g-plot {{ position: relative; width: 100%; height: 150px; }}
      .g-base {{ position: absolute; left: 0; right: 0; top: 70px; height: 4px; background: rgba(255,255,255,0.8); transform-origin: left; }}
      .g-bar {{ position: absolute; left: 30%; width: 80px; margin-left: -40px; border-radius: 10px; }}
      .up .g-bar {{ bottom: 82px; height: 62px; background: {C["yellow"]}; transform-origin: bottom; }}
      .down .g-bar {{ top: 76px; height: 70px; background: {C["pink"]}; transform-origin: top; }}
      .g-val {{ position: absolute; left: 44%; right: 0; text-align: left; font-weight: 900; font-size: 44px; color: {C["white"]}; letter-spacing: -0.01em; line-height: 1; }}
      .up .g-val {{ top: 18px; }}
      .down .g-val {{ top: 90px; }}
      .two .g-val {{ font-size: 34px; }}
      .two .g-maint {{ display: none; }}
      .two .g-h {{ font-size: 24px; }}
      .dim {{ opacity: 0.42; }}
      .build {{ position: absolute; left: {SAFE["left"]}px; right: {SAFE["right"]}px; top: {SAFE["top"] + 20}px; display: flex; flex-direction: column; align-items: center; gap: 8px; }}
      .bd {{ font-weight: 800; font-size: 46px; color: {C["white"]}; text-transform: uppercase; letter-spacing: 0.01em; text-shadow: 0 3px 14px rgba(0,0,0,0.7); }}
      .bd-eq {{ position: relative; margin-top: 10px; }}
      .bd-eq span {{ display: inline-block; font-weight: 900; font-size: 120px; color: {C["yellow"]}; letter-spacing: -0.03em; line-height: 1; text-shadow: 0 6px 24px rgba(0,0,0,0.55); }}
      .list.compact {{ gap: 8px; }}
      .list.compact .li {{ padding: 6px 20px 6px 8px; border-radius: 12px; }}
      .list.compact .li b {{ font-size: 24px; padding: 2px 10px; }}
      .list.compact .li span {{ font-size: 32px; }}
      .list.compact .lh {{ font-size: 24px; }}
      .lh, .st-h {{ align-self: flex-start; background: {C["plate"]}; border-radius: 10px; padding: 4px 14px; text-shadow: none; }}
      .st-h {{ align-self: center; }}
      .cap.left {{ left: {D["left_captions"]["left"]}px; right: auto; width: {D["left_captions"]["width"]}px; bottom: auto; top: {D["left_captions"]["top"]}px; }}
      .cap.left .capin {{ align-items: flex-start; text-align: left; }}
      .tracker {{ position: absolute; left: {SAFE["left"]}px; top: {D["layout"]["gfx_top"]}px; display: flex; flex-direction: column; gap: 14px; }}
      .tk-row {{ display: flex; gap: 14px; }}
      .tk-t {{ width: 92px; height: 92px; border-radius: 18px; display: flex; align-items: center; justify-content: center;
        font-weight: 900; font-size: 56px; background: {C["plate"]}; color: rgba(255,255,255,0.55); }}
      .tk-lab {{ position: relative; height: 54px; }}
      .tk-l {{ position: absolute; left: 0; top: 0; white-space: nowrap; font-weight: 900; font-size: 44px; color: {C["white"]};
        text-transform: uppercase; letter-spacing: -0.01em; text-shadow: {D["hero_shadow"]}; opacity: 0; }}
      .chips {{ position: absolute; left: {SAFE["left"]}px; top: {D["layout"]["chips_top"]}px; width: 560px; display: flex; flex-wrap: wrap; gap: 12px; }}
      .chips .chip {{ padding: 8px 20px; border-radius: 12px; background: {C["yellow"]}; color: {C["ink"]}; font-weight: 900; font-size: 34px; }}
      .end {{ position: absolute; left: {SAFE["left"]}px; right: {SAFE["right"]}px; top: {D["layout"]["gfx_top"]}px; display: flex; align-items: center; gap: 20px;
        padding: 20px 22px; background: {C["white"]}; border-radius: 26px; box-shadow: 0 18px 40px rgba(0,0,0,0.35); }}
      .end-av {{ width: 84px; height: 84px; flex: none; border-radius: 50%; background: linear-gradient(135deg, {C["yellow"]}, {C["pink"]}); }}
      .end-av img {{ width: 100%; height: 100%; border-radius: 50%; object-fit: cover; display: block; }}
      .end-txt {{ flex: 1; display: flex; flex-direction: column; }}
      .end-txt b {{ font-weight: 800; font-size: 32px; color: {C["ink"]}; line-height: 1.1; }}
      .end-handle {{ font-weight: 600; font-size: 26px; color: #5b5b63; }}
      .end-btn {{ position: relative; width: 190px; height: 64px; flex: none; }}
      .end-btn span {{ position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; border-radius: 14px; font-weight: 800; font-size: 28px; }}
      .end-btn .b1 {{ background: #0095f6; color: #fff; }}
      .end-btn .b2 {{ background: #efefef; color: {C["ink"]}; }}
"""

o_head = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>Skinny Fat Reel V2</title>
    <script src="assets/gsap.min.js"></script>
    <style>{style}    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}" data-fps="{FPS}">
      <div id="fx"><div id="grade"><div id="move"><div id="cam">"""
vids = []
auds = []
FADE = D["audio"]["clip_fade"]
for n, ov in enumerate(E.get("overlays", [])):
    t0, t1 = to_out(ov["t"]), to_out(ov["until"])
    vids.append(f'        <video id="ov{n}" class="clip" src="{ov["file"]}" data-start="{t0}" data-duration="{q(t1 - t0)}" '
                f'data-media-start="{ov.get("media_start", 0)}" data-track-index="{12 + n}" muted playsinline '
                f'style="left: {ov["left"]}px; top: {ov["top"]}px; width: {ov["w"]}px; height: {ov["h"]}px; filter: {ov["filter"]}"></video>')
for i, g in enumerate(segments):
    d = q(g["src_e"] - g["src_s"])
    vids.append(f'        <video id="v{i}" class="clip" src="{E["source_video"]}" data-start="{g["out_s"]}" data-duration="{d}" '
                f'data-media-start="{g["src_s"]}" data-track-index="{i % 2}" muted playsinline'
                f'{f" style=\"filter: brightness({g["bright"]})\"" if g["bright"] != 1.0 else ""}></video>')
    lane = json.dumps({"version": 1, "lanes": [{"target": "volume", "points": [
        {"t": 0, "v": 0}, {"t": FADE, "v": g["gain"]}, {"t": round(d - FADE, 3), "v": g["gain"]}, {"t": d, "v": 0}]}]})
    auds.append(f"      <audio id=\"a{i}\" src=\"{E['source_audio']}\" data-start=\"{g['out_s']}\" data-duration=\"{d}\" "
                f"data-media-start=\"{g['src_s']}\" data-track-index=\"{2 + i % 2}\" data-automation='{lane}'></audio>")

broll_html = []
for n, b in enumerate(E.get("broll", [])):
    f = b.get("file")
    if not f or not os.path.exists(os.path.join(ROOT, f)):
        continue  # placeholder until fetched
    t0, t1 = to_out(b["t"]), to_out(b["until"])
    d = q(t1 - t0)
    broll_html.append(f'      <div id="brw{n}" class="brw"><video id="br{n}" class="clip broll" src="{f}" data-start="{t0}" data-duration="{d}" '
                      f'data-media-start="{b.get("media_start", 0.4)}" data-track-index="{8 + n % 2}" muted playsinline></video></div>')
    J(f'      tl.fromTo("#brw{n}", {{ scale: 1.08 }}, {{ scale: 1.0, duration: {d}, ease: "none" }}, {t0});')

music_html = ""
for ext in ("mp3", "wav", "m4a"):
    mp = f"assets/music/bed.{ext}"
    if os.path.exists(os.path.join(ROOT, mp)):
        vol = E.get("music_volume", 0.12)
        lane = json.dumps({"version": 1, "lanes": [{"target": "volume", "points": [
            {"t": 0, "v": 0}, {"t": 1.0, "v": vol}, {"t": round(TOTAL - 1.5, 2), "v": vol}, {"t": TOTAL, "v": 0}]}]})
        music_html = (f"      <audio id=\"music\" src=\"{mp}\" data-start=\"0\" data-duration=\"{TOTAL}\" "
                      f"data-track-index=\"4\" data-automation='{lane}'></audio>")
        break

SFX_LEN = {"swoosh": 0.42, "tick": 0.05, "thump": 0.35, "rise": 0.5}
for cue in E.get("sfx_cues", []):
    if E["_in"](cue["t"]):
        add_sfx(cue["name"], to_out(cue["t"]), cue.get("vol", 0.7), explicit=True)


def sfx_len(name):
    if name in SFX_LEN:
        return SFX_LEN[name]
    w_ = wave.open(os.path.join(ROOT, f"assets/{name}.wav"))
    return round(w_.getnframes() / w_.getframerate(), 3)


sfx_html = [f'      <audio id="sfx{n}" src="assets/{name if "/" in name else "sfx/" + name}.wav" data-start="{max(0, t)}" data-duration="{sfx_len(name)}" '
            f'data-track-index="{5 + n % 3}" data-volume="{vol}"></audio>' for n, (name, t, vol) in enumerate(sfx)]

ov_tags = [v for v in vids if 'id="ov' in v]
vids = [v for v in vids if 'id="ov' not in v] + ov_tags
doc = [o_head] + vids + ['      </div></div></div></div>'] + broll_html + ['      <div id="shade"></div>'] + out + auds + \
      ([music_html] if music_html else ["      <!-- MUSIC PLACEHOLDER: drop a licensed track at assets/music/bed.mp3 and rebuild -->"]) + sfx_html + \
      ["    </div>", "    <script>", "      const tl = gsap.timeline({ paused: true });"] + js + \
      ['      window.__timelines["main"] = tl;', "    </script>", "  </body>", "</html>"]
open(os.path.join(ROOT, OUT_HTML), "w").write("\n".join(doc) + "\n")

# ------------------------------------------------------------------ 10. records
json.dump({"total": TOTAL, "segments": segments, "frames": frames_by_seg,
           "captions": [{"k": k, "out_start": st, "out_end": en, "src_t": b["t"], "support": b.get("support", ""), "hero": b.get("hero", "")}
                        for k, b, st, en in cap_rows], "sfx": sfx},
          open(os.path.join(ROOT, "build/timeline.json" if OUT_HTML == "index.html" else "build/timeline_preview.json"), "w"), indent=1)

L = ["# Editorial decision log — V2", "", f"Output duration: **{TOTAL:.2f}s** · segments: {len(segments)} · captions: {len(cap_rows)} · sfx: {len(sfx)}", "",
     "| Take | Source | Decision | Output | Spoken (Tamil, ASR) | Reason |", "|---|---|---|---|---|---|"]
for tk in E["takes"]:
    segs = [g for g in segments if g["take"] == tk["id"]]
    pos = f'{segs[0]["out_s"]:.2f}–{segs[-1]["out_s"] + segs[-1]["src_e"] - segs[-1]["src_s"]:.2f}s' if segs else "—"
    L.append(f'| {tk["id"]} | {tk["s"]:.2f}–{tk["e"]:.2f} | {"KEEP" if tk.get("keep") else "reject"} | {pos} | {tk.get("ta", "")} | {tk.get("why", "")} |')
flags = E.get("flags", [])
if flags:
    L += ["", "## Flagged for review", ""] + [f"- {f}" for f in flags]
(open(os.path.join(ROOT, "build/DECISIONS.md"), "w") if OUT_HTML == "index.html" else open(os.devnull, "w")).write("\n".join(L) + "\n")
print(f"segments={len(segments)} captions={len(cap_rows)} gfx={gid} sfx={len(sfx)} total={TOTAL:.2f}s ref_db={ref_db:.1f}")
