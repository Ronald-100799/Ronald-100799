import wave,sys,numpy as np
from scipy.signal import butter,sosfiltfilt
from scipy.ndimage import uniform_filter1d
w=wave.open(sys.argv[1]);SR=w.getframerate();ch=w.getnchannels()
a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
if ch>1: a=a.reshape(-1,ch).mean(1)
hp=sosfiltfilt(butter(6,4000,'hp',fs=SR,output='sos'),a)
W=SR//100;n=len(hp)//W;x=hp[:n*W].reshape(n,W)
rms=np.sqrt((x**2).mean(1));crest=np.abs(x).max(1)/(rms+1e-9)
score=np.abs(x).max(1)/(np.sqrt(uniform_filter1d(rms**2,21))+1e-9)
for c,s in [(6,10),(5,7),(4.5,6)]:
    idx=np.where((crest>c)&(score>s))[0]; print(f'crest>{c},score>{s}: {len(idx)}', ' '.join(f'{i/100:.2f}' for i in idx[:40]) if c==5 else '')
