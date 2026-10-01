import json, numpy as np
from PIL import Image
F='D:/Animate/Projects/HonestInterview/ProductionFull_v5/frames/full_v5a/f%06d.png'
T=json.load(open('D:/Animate/Projects/HonestInterview/ProductionFull_v5/assets/dialogue_turns.json'))['turns']
shots=[(40,60,'G'),(60,74,'C'),(74,92,'G'),(92,109,'C'),(109,173,'G'),(173,396,'C'),(466,562,'G'),(562,613,'C'),(613,666,'G'),(666,910,'C'),(910,951,'G'),(951,1052,'C'),(1052,1140,'G'),(1140,1205,'C'),(1205,1258,'G'),(1258,1350,'C'),(1350,1401,'G'),(1401,1458,'C'),(1458,1500,'G'),(1500,1524,'C'),(1524,1552,'G'),(1552,1620,'C')]
box={'C':(470,800,650,915),'G':(480,800,660,915)}
def speaking(f,who):
    t=f/24
    for u in T:
        if (u['speaker']=='CAP')==(who=='C') and u['start']-0.04<=t<u['end']+0.04: return True
    return False
res={}
for a,b,w in shots:
    prev=None; ch=[]
    for f in range(a,b):
        m=np.asarray(Image.open(F%f).convert('L').crop(box[w]),dtype=np.float32)
        d=0 if prev is None else float(np.abs(m-prev).mean()); prev=m
        ch.append((f,d>1.0,speaking(f,w)))
    # static runs during speech
    run=[];out=[]
    for f,c,s in ch:
        if s and not c: run.append(f)
        else:
            if len(run)>=6: out.append(('STATIC_IN_SPEECH',run[0],run[-1],round(run[0]/24,2),round(run[-1]/24,2)))
            run=[]
    if len(run)>=6: out.append(('STATIC_IN_SPEECH',run[0],run[-1],round(run[0]/24,2),round(run[-1]/24,2)))
    sil=[f for f,c,s in ch if c and not s and f!=a]
    if sil: out.append(('CHANGE_IN_SILENCE',[(f,round(f/24,2)) for f in sil]))
    print(a,b,w,out)
