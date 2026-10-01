var LOG="file:///D|/Animate/Projects/HonestInterview/ProductionFull_v5/tests/sound_test/_render_log.txt"; var L=""; function w(s){L+=s+"\n";}
try {
var t0=new Date().getTime();
var doc=fl.openDocument("file:///D|/Animate/Projects/HonestInterview/ProductionFull_v5/xfl/stills_v5a/stills_v5a.xfl");
var tl=doc.getTimeline(); w("opened frames="+tl.frameCount+" layers="+tl.layerCount+" lib="+doc.library.items.length);
doc.importFile("file:///D|/Animate/Sounds/Bro was so honest.mp3", true);
var snd=null; var it=doc.library.items; for (var i=0;i<it.length;i++){ if(it[i].itemType=="sound") snd=it[i]; }
if (snd) { tl.setSelectedLayers(tl.layerCount-1); tl.addNewLayer("AUDIO_original","normal",false); var li=tl.findLayerIndex("AUDIO_original")[0]; var fr=tl.layers[li].frames[0]; fr.soundLibraryItem=snd; fr.soundSync="stream"; w("sound attached "+snd.name+" layer "+li); } else { w("NO SOUND ITEM"); }
var frames=[0];
var od="file:///D|/Animate/Projects/HonestInterview/ProductionFull_v5/tests/sound_test";
for (var i=0;i<frames.length;i++){ tl.currentFrame=frames[i]; var n=("000000"+frames[i]).slice(-6); doc.exportPNG(od+"/f"+n+".png", true, true); }
w("exported "+frames.length+" frames in "+((new Date().getTime()-t0)/1000)+"s");
var ok=fl.saveDocument(doc, "file:///D|/Animate/Projects/HonestInterview/ProductionFull_v5/tests/sound_test/sound_test.fla"); w("saved fla "+ok);
fl.closeDocument(doc, false);
} catch(e) { w("ERR "+e); }
FLfile.write(LOG, L+"DONE\n");