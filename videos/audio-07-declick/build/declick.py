# Spectral median clamp: caps short high-frequency spikes (mouse clicks) to the
# per-bin local median level. Speech changes slowly per bin and is left alone.
import sys,numpy as np,soundfile as sf
from scipy.signal import stft,istft
from scipy.ndimage import median_filter
x,SR=sf.read(sys.argv[1],dtype='float32',always_2d=True)
lo=float(sys.argv[3]) if len(sys.argv)>3 else 1800   # Hz
k =float(sys.argv[4]) if len(sys.argv)>4 else 2.0    # allowed factor over median
import os; N=int(os.environ.get("N",512)); H=N//4
out=np.zeros_like(x); flagged=0
for c in range(x.shape[1]):
    f,t,Z=stft(x[:,c],SR,nperseg=N,noverlap=N-H,boundary='even')
    M=np.abs(Z); band=f>=lo
    med=median_filter(M[band],size=(1,int(os.environ.get("MW",31))))          # ~83 ms temporal median per bin
    cap=med*k
    # only act on frames where the band as a whole spikes (sharp event)
    e=M[band].sum(0); em=median_filter(e,size=int(os.environ.get("MW",31)))
    spike=e>em*1.8
    spike=np.convolve(spike.astype(float),np.ones(5),'same')>0  # widen ±2 hops (decay tail)
    g=np.ones_like(M[band])
    over=(M[band]>cap)&spike[None,:]
    g[over]=cap[over]/M[band][over]
    flagged+=int(spike.sum())
    Z2=Z.copy(); Z2[band]*=g
    _,y=istft(Z2,SR,nperseg=N,noverlap=N-H,boundary=True)
    out[:,c]=y[:len(x)]
sf.write(sys.argv[2],out,SR,subtype='PCM_24')
print('frames touched',flagged,'of',M.shape[1]*x.shape[1])
