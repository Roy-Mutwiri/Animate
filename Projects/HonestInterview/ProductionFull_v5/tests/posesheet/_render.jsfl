var LOG="file:///D|/Animate/Projects/HonestInterview/ProductionFull_v5/tests/posesheet/_render_log.txt"; var L=""; function w(s){L+=s+"\n";}
try {
var t0=new Date().getTime();
var doc=fl.openDocument("file:///D|/Animate/Projects/HonestInterview/ProductionFull_v5/xfl/posesheet/posesheet.xfl");
var tl=doc.getTimeline(); w("opened frames="+tl.frameCount+" layers="+tl.layerCount+" lib="+doc.library.items.length);
var frames=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36];
var od="file:///D|/Animate/Projects/HonestInterview/ProductionFull_v5/tests/posesheet";
for (var i=0;i<frames.length;i++){ tl.currentFrame=frames[i]; var n=("000000"+frames[i]).slice(-6); doc.exportPNG(od+"/f"+n+".png", true, true); }
w("exported "+frames.length+" frames in "+((new Date().getTime()-t0)/1000)+"s");
fl.closeDocument(doc, false);
} catch(e) { w("ERR "+e); }
FLfile.write(LOG, L+"DONE\n");