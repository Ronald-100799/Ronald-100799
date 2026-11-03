"""Original, licence-free 'analytic' background bed: tight drums, pulsing 16th-note synth, sub bass, minor key.
News / explainer feel, built to sit under a voice. No third-party samples.

Usage: python3 -I tools/analytic_bed.py OUT.wav SECONDS [bpm] [seed] [mood]
  mood: "analytic" (default, D minor, Desk) or "warm" (G major, softer drums, pleasant — Terrace)
"""
import sys, wave
import numpy as np

SR = 48000
out, dur = sys.argv[1], float(sys.argv[2])
bpm = float(sys.argv[3]) if len(sys.argv) > 3 else 104
rng = np.random.default_rng(int(sys.argv[4]) if len(sys.argv) > 4 else 11)
MOOD = sys.argv[5] if len(sys.argv) > 5 else "analytic"
WARM = MOOD == "warm"
N = int(SR * dur)
beat = 60 / bpm
s16 = beat / 4


def midi(n):
    return 440 * 2 ** ((n - 69) / 12)


def place(buf, x, t, g=1.0):
    i = int(t * SR)
    if 0 <= i < N:
        x = x[: N - i]
        buf[i:i + len(x)] += g * x


def lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); s = 0.0
    for i in range(len(x)):
        s = a * s + (1 - a) * x[i]; y[i] = s
    return y


def pluck(f, d, bright):
    """Muted saw pluck: band-limited saw (few partials) with a fast filter-like decay."""
    t = np.arange(int(SR * d)) / SR
    x = sum(np.sin(2 * np.pi * f * k * t) / k * np.exp(-t * (8 + 5 * k / bright)) for k in range(1, 7))
    return x * (1 - np.exp(-t * 400)) * np.clip((d - t) / 0.01, 0, 1)


def sub(f, d):
    t = np.arange(int(SR * d)) / SR
    return np.sin(2 * np.pi * f * t) * (1 - np.exp(-t * 60)) * np.exp(-t * 1.2) * np.clip((d - t) / 0.03, 0, 1)


def kick():
    t = np.arange(int(SR * 0.3)) / SR
    return np.tanh(1.6 * np.sin(2 * np.pi * (45 + 120 * np.exp(-t * 40)) * t) * np.exp(-t * 12))


def clap():
    t = np.arange(int(SR * 0.2)) / SR
    n = rng.standard_normal(len(t))
    env = np.exp(-t * 28) * (1 + 0.6 * (np.sin(2 * np.pi * 90 * t) > 0) * (t < 0.03))
    return np.diff(np.concatenate([[0], n])) * env * 0.6


def hat(o=False):
    t = np.arange(int(SR * (0.12 if o else 0.035))) / SR
    n = np.diff(np.diff(np.concatenate([[0, 0], rng.standard_normal(len(t))])))
    return n * np.exp(-t * (25 if o else 110)) * 0.18


# D minor: Dm – Bb – F – C (i–VI–III–VII), arpeggio patterns per bar
roots = [38, 34, 41, 36]
chords = [[62, 65, 69, 74], [58, 62, 65, 70], [65, 69, 72, 77], [60, 64, 67, 72]]
if WARM:  # G major: G – Em – C – D (I–vi–IV–V), brighter voicings
    roots = [43, 40, 36, 38]
    chords = [[67, 71, 74, 79], [64, 67, 71, 76], [64, 67, 72, 76], [66, 69, 74, 78]]
pattern = [0, 2, 1, 3, 2, 1, 0, 2, 1, 3, 2, 3, 1, 2, 0, 1]
Pl, Bs, Dr = np.zeros(N), np.zeros(N), np.zeros(N)
bar = 4 * beat
for b in range(int(np.ceil(dur / bar))):
    t0 = b * bar
    c = chords[b % 4]
    bright = 1.0 + 0.8 * min(1, b / 6)          # the arp opens up slowly
    for k, p in enumerate(pattern):
        acc = 1.0 if k % 4 == 0 else 0.6
        place(Pl, pluck(midi(c[p]), s16 * 1.6, bright), t0 + k * s16, 0.12 * acc)
    for q in (0, 1.5, 2.5, 3):                  # syncopated sub line
        place(Bs, sub(midi(roots[b % 4]), beat * 0.9), t0 + q * beat, 0.55)
    for q in range(4):
        place(Dr, kick(), t0 + q * beat, 0.6 if q in (0, 2) else 0.35)
        if q in (1, 3):
            place(Dr, clap(), t0 + q * beat, 0.22 if WARM else 0.35)
        for h in range(4):
            if WARM and h % 2:
                continue  # 8th-note hats: lighter, less busy
            place(Dr, hat(), t0 + q * beat + h * s16, (0.6 if h == 2 else 0.35) if WARM else (0.9 if h == 2 else 0.45))
    place(Dr, hat(True), t0 + 3.5 * beat, 0.6)

Pl = lp(Pl, 5200 if WARM else 4200)
if WARM:  # soft sustained pad under the plucks
    Pd = np.zeros(N)
    for b in range(int(np.ceil(dur / bar))):
        t_ = np.arange(int(SR * bar)) / SR
        env = np.clip(t_ / 0.6, 0, 1) * np.clip((bar - t_) / 0.6, 0, 1)
        x = sum(np.sin(2 * np.pi * midi(n - 12) * t_) + 0.3 * np.sin(2 * np.pi * midi(n - 12) * 2.003 * t_) for n in chords[b % 4][:3])
        place(Pd, x * env, b * bar, 0.05)
    Pl = Pl + lp(Pd, 1800)
t = np.arange(N) / SR
pump = np.ones(N)
for k in range(int(dur / beat) + 1):
    i = int(k * beat * SR); j = min(N, i + int(0.2 * SR))
    if i < N:
        pump[i:j] = 1 - 0.45 * np.exp(-np.arange(j - i) / SR * 16)
dly = np.zeros(N); d = int(s16 * 3 * SR); dly[d:] = Pl[:-d] * 0.35   # dotted-8th echo, right side
L = Pl * pump + Bs * pump + Dr
R = (Pl * 0.7 + dly) * pump + Bs * pump + Dr
fade = np.clip(t / 1.0, 0, 1) * np.clip((dur - t) / 1.5, 0, 1)
L, R = L * fade, R * fade
m = max(np.abs(L).max(), np.abs(R).max())
st = np.tanh(np.stack([L, R], 1) / m * 1.2) * 0.8
with wave.open(out, "w") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype(np.int16).tobytes())
print(f"wrote {out} {dur:.1f}s @ {bpm} bpm")
