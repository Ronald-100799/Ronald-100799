"""Original, licence-free podcast-style background bed (warm keys, soft bass, light drums).

Usage: python3 -I tools/podcast_bed.py OUT.wav SECONDS [bpm] [seed]
Written by Claude for Ron's reels; safe to use anywhere (no third-party samples).
"""
import sys, wave
import numpy as np

SR = 48000
out, dur = sys.argv[1], float(sys.argv[2])
bpm = float(sys.argv[3]) if len(sys.argv) > 3 else 92
rng = np.random.default_rng(int(sys.argv[4]) if len(sys.argv) > 4 else 3)
N = int(SR * dur)
beat = 60 / bpm
L = np.zeros(N); R = np.zeros(N)


def midi(n):
    return 440 * 2 ** ((n - 69) / 12)


def place(buf, x, t, gain=1.0):
    i = int(t * SR)
    if i >= N:
        return
    x = x[: N - i]
    buf[i:i + len(x)] += gain * x


def keys(f, d):
    """Soft electric-piano tone: two-operator FM with a fast-decaying bell and slow body."""
    t = np.arange(int(SR * d)) / SR
    idx = 1.6 * np.exp(-t * 6)
    tone = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * t))
    tone += 0.25 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 4)
    env = (1 - np.exp(-t * 200)) * np.exp(-t * 1.1)
    rel = np.clip((d - t) / 0.15, 0, 1)
    return tone * env * rel


def bass(f, d):
    t = np.arange(int(SR * d)) / SR
    x = np.sin(2 * np.pi * f * t) + 0.2 * np.sin(2 * np.pi * 2 * f * t)
    return x * (1 - np.exp(-t * 80)) * np.exp(-t * 1.6) * np.clip((d - t) / 0.08, 0, 1)


def kick():
    t = np.arange(int(SR * 0.35)) / SR
    return np.sin(2 * np.pi * (48 + 70 * np.exp(-t * 35)) * t) * np.exp(-t * 11)


def hat(open_=False):
    t = np.arange(int(SR * (0.18 if open_ else 0.05))) / SR
    n = rng.standard_normal(len(t))
    n = np.diff(np.concatenate([[0], n]))  # crude high-pass
    return n * np.exp(-t * (18 if open_ else 70)) * 0.3


def snare():
    t = np.arange(int(SR * 0.22)) / SR
    n = rng.standard_normal(len(t)) * np.exp(-t * 22)
    body = np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30)
    return 0.5 * n + 0.6 * body


# i–VI–III–VII in A minor (Am, F, C, G): calm, forward-moving
prog = [[57, 60, 64, 67], [53, 57, 60, 64], [48, 55, 60, 64], [55, 59, 62, 67]]
roots = [45, 41, 48, 43]
bar = 4 * beat
nb = int(np.ceil(dur / bar))
K, Bs, Dr = np.zeros(N), np.zeros(N), np.zeros(N)
for b in range(nb):
    t0 = b * bar
    ch = prog[b % 4]
    for k, n in enumerate(ch):                       # gently strummed chord
        place(K, keys(midi(n), bar * 0.95), t0 + 0.012 * k, 0.16)
    place(K, keys(midi(ch[-1] + 12), beat * 1.5), t0 + 2.5 * beat, 0.07)   # small melodic answer
    place(Bs, bass(midi(roots[b % 4]), beat * 1.8), t0, 0.5)
    place(Bs, bass(midi(roots[b % 4]), beat * 0.9), t0 + 2.5 * beat, 0.35)
    for q in range(4):
        tq = t0 + q * beat
        if q in (0, 2):
            place(Dr, kick(), tq, 0.55)
        if q in (1, 3):
            place(Dr, snare(), tq, 0.16)
        place(Dr, hat(), tq + beat / 2, 0.5)
        place(Dr, hat(), tq, 0.25)
    place(Dr, hat(True), t0 + 3.5 * beat, 0.3)

# warm the keys: gentle low-pass (one-pole) and slow stereo motion
def lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.zeros_like(x); s = 0.0
    for i in range(len(x)):
        s = a * s + (1 - a) * x[i]; y[i] = s
    return y

K = lp(K, 3200)
t = np.arange(N) / SR
pan = 0.5 + 0.15 * np.sin(2 * np.pi * 0.07 * t)
# kick-driven pump keeps it moving under speech
pump = np.ones(N)
for b in range(int(dur / beat) + 1):
    i = int(b * beat * SR); j = min(N, i + int(0.25 * SR))
    if i < N:
        pump[i:j] = 1 - 0.35 * np.exp(-np.arange(j - i) / SR * 14)
L = (K * (1 - pan) * 2 + Bs + 0.9 * Dr) * pump
R = (K * pan * 2 + Bs + 0.9 * Dr) * pump
fade = np.clip(t / 1.5, 0, 1) * np.clip((dur - t) / 2.0, 0, 1)
L *= fade; R *= fade
m = max(np.abs(L).max(), np.abs(R).max())
st = np.stack([L, R], 1) / m * 0.8
with wave.open(out, "w") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype(np.int16).tobytes())
print(f"wrote {out} {dur:.1f}s @ {bpm} bpm")
