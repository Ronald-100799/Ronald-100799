"""Synthesised sounds for the sample (no licence needed): a 2.6 s riser and a quiet pulse bed."""
import numpy as np, wave, sys, os
SR = 48000
rng = np.random.default_rng(7)

def save(name, x):
    x = np.clip(x, -1, 1)
    with wave.open(os.path.join(sys.argv[1], name), "w") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        st = np.stack([x, x], 1)
        w.writeframes((st * 32767).astype(np.int16).tobytes())

def riser(d=2.6):
    t = np.arange(int(SR * d)) / SR
    k = t / d
    f = 140 * (2 ** (k * 2.6))                      # pitch climbs ~2.6 octaves
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.35 * np.sin(2 * np.pi * np.cumsum(f * 2.01) / SR)
    noise = rng.standard_normal(len(t))
    # noise brightens as it rises: one-pole low-pass with a rising cutoff
    out, y = np.zeros_like(noise), 0.0
    a = np.exp(-2 * np.pi * (300 + 7000 * k ** 2) / SR)
    for i, n in enumerate(noise):
        y = a[i] * y + (1 - a[i]) * n
        out[i] = y
    env = k ** 1.8
    trem = 1 + 0.25 * np.sin(2 * np.pi * (4 + 14 * k) * t)  # pulsing speeds up
    x = (0.45 * tone + 1.6 * out) * env * trem
    x[-int(SR * 0.01):] *= np.linspace(1, 0, int(SR * 0.01))
    return 0.55 * x / np.abs(x).max()

def bed(d=15.0, bpm=100):
    t = np.arange(int(SR * d)) / SR
    drone = 0.5 * np.sin(2 * np.pi * 55 * t) + 0.25 * np.sin(2 * np.pi * 82.4 * t) + 0.12 * np.sin(2 * np.pi * 110.3 * t)
    beat = 60 / bpm
    ph = (t % beat)
    kick = np.sin(2 * np.pi * (50 + 90 * np.exp(-ph * 30)) * ph) * np.exp(-ph * 9)
    x = 0.35 * drone * (0.8 + 0.2 * np.sin(2 * np.pi * 0.25 * t)) + 0.6 * kick
    x[t < 2.6] *= 0.0                                # silent under the riser; drops in on the turn
    fade = np.clip((d - t) / 1.2, 0, 1)
    return 0.4 * x * fade / np.abs(x).max()

save("riser.wav", riser())
save("bed.wav", bed())
print("ok")
