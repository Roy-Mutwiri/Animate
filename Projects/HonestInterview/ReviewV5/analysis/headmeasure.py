import sys, cv2, numpy as np
v=sys.argv[1]; ts=[float(t) for t in sys.argv[2:]]
c=cv2.VideoCapture(v); fps=c.get(5)
for t in ts:
    c.set(1,int(round(t*fps))); ok,fr=c.read()
    g=cv2.medianBlur(cv2.cvtColor(fr,cv2.COLOR_BGR2GRAY),3)
    cs=cv2.HoughCircles(g,cv2.HOUGH_GRADIENT,1.2,40,param1=120,param2=40,minRadius=25,maxRadius=200)
    out=[]
    if cs is not None:
        for x,y,r in cs[0][:4]:
            # require bright interior
            m=np.zeros_like(g); cv2.circle(m,(int(x),int(y)),int(r*0.6),255,-1)
            inside=g[m>0].mean()
            out.append(f"({x:.0f},{y:.0f}) d={2*r:.0f} in={inside:.0f}")
    print(t, int(round(t*fps)), out)
