"""Per-frame change log for a video range: changed-pixel count and bbox vs previous frame.
usage: python framediff.py VIDEO f0 f1 OUT.csv"""
import sys, cv2, numpy as np
v,f0,f1,out=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),sys.argv[4]
c=cv2.VideoCapture(v); c.set(cv2.CAP_PROP_POS_FRAMES,f0)
prev=None; rows=[]
for i in range(f0,f1):
    ok,fr=c.read()
    if not ok: break
    g=cv2.cvtColor(fr,cv2.COLOR_BGR2GRAY).astype(np.int16)
    if prev is not None:
        d=np.abs(g-prev)>40
        n=int(d.sum())
        if n:
            ys,xs=np.nonzero(d); bb=(xs.min(),ys.min(),xs.max(),ys.max())
        else: bb=(-1,-1,-1,-1)
        rows.append((i,round(i/c.get(5),2),n)+tuple(int(b) for b in bb))
    prev=g
with open(out,'w') as f:
    f.write('frame,t,changed,x0,y0,x1,y1\n')
    for r in rows: f.write(','.join(map(str,r))+'\n')
