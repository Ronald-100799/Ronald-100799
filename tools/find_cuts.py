"""List the creator's own jump cuts / inserts in a pre-edited video (frame-difference spikes).

Usage: python3 -I tools/find_cuts.py VIDEO.mp4
Use the times to place graphic blocks: start or end a block exactly on one of these cuts,
never leave less than ~0.7 s of face between a block edge and a cut.
"""
import subprocess, sys
import numpy as np

raw = subprocess.run(["ffmpeg", "-v", "error", "-i", sys.argv[1], "-vf", "scale=90:160,format=gray", "-f", "rawvideo", "-"],
                     capture_output=True, check=True).stdout
a = np.frombuffer(raw, np.uint8).reshape(-1, 160, 90).astype(np.float32)
d = np.abs(np.diff(a, axis=0)).mean((1, 2))
thr = max(6.0, 4 * float(np.median(d)))
cuts = [(i + 1) / 30 for i in np.where(d > thr)[0]]
print(" ".join(f"{c:.3f}" for c in cuts))
