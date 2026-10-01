var LOG="file:///D|/Animate/Projects/HonestInterview/ProductionFull_v5/tests/v5d_check/_render_log.txt"; var L=""; function w(s){L+=s+"\n";}
try {
var t0=new Date().getTime();
var doc=fl.openDocument("file:///D|/Animate/Projects/HonestInterview/ProductionFull_v5/xfl/honest_v5d/honest_interview_v5d.xfl");
var tl=doc.getTimeline(); w("opened frames="+tl.frameCount+" layers="+tl.layerCount+" lib="+doc.library.items.length);
var frames=[0, 230, 700, 1440, 1690];
var od="file:///D|/Animate/Projects/HonestInterview/ProductionFull_v5/tests/v5d_check";
for (var i=0;i<frames.length;i++){ tl.currentFrame=frames[i]; var n=("000000"+frames[i]).slice(-6); doc.exportPNG(od+"/f"+n+".png", true, true); }
w("exported "+frames.length+" frames in "+((new Date().getTime()-t0)/1000)+"s");
fl.closeDocument(doc, false);
} catch(e) { w("ERR "+e); }
FLfile.write(LOG, L+"DONE\n");