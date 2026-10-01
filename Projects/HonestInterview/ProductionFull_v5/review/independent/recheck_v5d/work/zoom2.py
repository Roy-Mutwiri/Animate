import cv2, numpy as np
F='D:/Animate/Projects/HonestInterview/ProductionFull_v5/frames/full_v5d/f%06d.png'
orb=cv2.ORB_create(3000); bf=cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True)
def load(i): return cv2.cvtColor(cv2.imread(F%i),cv2.COLOR_BGR2GRAY)[560:1360,240:840]
prev=None; tot=1.5; out=[]
for i in range(1661,1702):
    g=load(i); kp,d=orb.detectAndCompute(g,None)
    if prev is not None:
        m=sorted(bf.match(prev[1],d),key=lambda x:x.distance)[:300]
        a=np.float32([prev[0][x.queryIdx].pt for x in m]); b=np.float32([kp[x.trainIdx].pt for x in m])
        M,_=cv2.estimateAffinePartial2D(a,b,ransacReprojThreshold=2); s=np.hypot(M[0,0],M[1,0]); tot*=s; out.append((i,round(s,4),round(tot,3)))
    prev=(kp,d)
print(out)
