"""cmp.py OUT.png PAIRS_PER_ROW TILEW t0:t1:step | t list   -- prod|ref pairs at same timestamps
optional env CROP=x0,y0,x1,y1 in normalized coords (applied to both)"""
import sys, os, cv2, numpy as np
from PIL import Image, ImageDraw
PF='D:/Animate/Projects/HonestInterview/ProductionFull_v5/frames/full_v5a/f%06d.png'
REF='D:/Animate/Goal/Bro was so honest.mp4'
_ref=None
def refframes():
    global _ref
    if _ref is None:
        cap=cv2.VideoCapture(REF); fr=[]
        while True:
            ok,f=cap.read()
            if not ok: break
            fr.append(f)
        _ref=fr
    return _ref
def parse(args):
    out=[]
    for a in args:
        if ':' in a:
            a0,a1,st=map(float,a.split(':')); t=a0
            while t<a1-1e-9: out.append(round(t,4)); t+=st
        else: out.append(float(a))
    return out
def main():
    out,ppr,W=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]); ts=parse(sys.argv[4:])
    crop=os.environ.get('CROP'); src=os.environ.get('SRC','both')
    R=refframes(); tiles=[]
    for t in ts:
        pi=min(int(np.floor(t*24+0.5)),1701); ri=min(int(np.floor(t*25+0.5)),len(R)-1)
        p=Image.open(PF%pi).convert('RGB'); r=Image.fromarray(cv2.cvtColor(R[ri],cv2.COLOR_BGR2RGB))
        ims=[]
        for im,lab in ((p,f'P {t:.2f} f{pi}'),(r,f'R f{ri}')):
            if src=='prod' and lab[0]=='R': continue
            if crop:
                c=[float(v) for v in crop.split(',')]; im=im.crop((int(c[0]*im.width),int(c[1]*im.height),int(c[2]*im.width),int(c[3]*im.height)))
            im=im.resize((W,int(im.height*W/im.width)),Image.LANCZOS)
            d=ImageDraw.Draw(im); d.rectangle([0,0,7*len(lab)+4,12],fill=(0,0,0)); d.text((2,0),lab,fill=(255,90,90) if lab[0]=='P' else (90,255,90))
            ims.append(im)
        h=max(i.height for i in ims); pair=Image.new('RGB',(sum(i.width for i in ims)+4,h),(255,0,255))
        x=0
        for i in ims: pair.paste(i,(x,0)); x+=i.width+4
        tiles.append(pair)
    w=max(t.width for t in tiles)+6; h=max(t.height for t in tiles)+6
    rows=(len(tiles)+ppr-1)//ppr; S=Image.new('RGB',(ppr*w,rows*h),(40,40,40))
    for k,t in enumerate(tiles): S.paste(t,((k%ppr)*w,(k//ppr)*h))
    S.save(out); print(out,S.size,len(tiles))
if __name__=='__main__': main()
