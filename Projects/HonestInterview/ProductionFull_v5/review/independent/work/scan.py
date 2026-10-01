import cv2, numpy as np, json
V='D:/Animate/Projects/HonestInterview/ProductionFull_v5/exports/honest_interview_v5a.mp4'
cap=cv2.VideoCapture(V); prev=None; diffs=[]; i=0; smalls=[]
while True:
    ok,f=cap.read()
    if not ok: break
    s=cv2.resize(f,(135,240),interpolation=cv2.INTER_AREA).astype(np.float32)
    if prev is not None: diffs.append(float(np.abs(s-prev).mean()))
    else: diffs.append(0.0)
    # histogram of mean
    smalls.append(s.mean(axis=(0,1)).tolist())
    prev=s; i+=1
print('frames',i)
d=np.array(diffs)
np.save('D:/Animate/Projects/HonestInterview/ProductionFull_v5/review/independent/work/prod_diffs.npy',d)
cuts=[k for k in range(1,len(d)) if d[k]>12]
print('big diffs >12:',[(k,round(k/24,2),round(d[k],1)) for k in cuts])
# frozen runs
runs=[];st=None
for k in range(1,len(d)):
    if d[k]<0.05:
        if st is None: st=k-1
    else:
        if st is not None and k-st>=12: runs.append((st,k-1,round(st/24,2),round((k-1)/24,2)))
        st=None
if st is not None: runs.append((st,len(d)-1))
print('frozen runs >=12 frames:',runs)
