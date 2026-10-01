import cv2, numpy as np
F='D:/Animate/Projects/HonestInterview/ProductionFull_v5/frames/full_v5a/f%06d.png'
orb=cv2.ORB_create(4000)
def load(i):
    return cv2.cvtColor(cv2.imread(F%i),cv2.COLOR_BGR2GRAY)
prev=load(1612); kp0,d0=orb.detectAndCompute(prev,None)
bf=cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True)
out=[]
for i in range(1613,1662):
    g=load(i); kp,d=orb.detectAndCompute(g,None)
    m=bf.match(d0,d); m=sorted(m,key=lambda x:x.distance)[:800]
    a=np.float32([kp0[x.queryIdx].pt for x in m]); b=np.float32([kp[x.trainIdx].pt for x in m])
    M,inl=cv2.estimateAffinePartial2D(a,b,ransacReprojThreshold=2)
    s=np.hypot(M[0,0],M[1,0]); out.append((i,round(s,4)))
print(out)
