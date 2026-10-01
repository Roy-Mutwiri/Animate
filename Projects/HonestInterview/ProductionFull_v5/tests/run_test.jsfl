var base = "file:///D|/Animate/Projects/HonestInterview/ProductionFull_v5/tests/";
var log = "";
try {
  var doc = fl.openDocument(base + "xfl_test/xfl_test.xfl");
  log += "opened " + doc.name + " frames=" + doc.getTimeline().frameCount + " layers=" + doc.getTimeline().layerCount + " lib=" + doc.library.items.length + "\n";
  var tl = doc.getTimeline();
  tl.currentFrame = 0; doc.exportPNG(base + "t_f0.png", true, true);
  tl.currentFrame = 6; doc.exportPNG(base + "t_f6.png", true, true);
  tl.currentFrame = 12; doc.exportPNG(base + "t_f12.png", true, true);
  var ok = fl.saveDocument(doc, base + "xfl_test.fla");
  log += "saved fla " + ok + "\n";
  fl.closeDocument(doc, false);
} catch (e) { log += "ERR " + e + "\n"; }
FLfile.write(base + "run_test_log.txt", log);
