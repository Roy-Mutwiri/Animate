var out = "file:///D|/Animate/Projects/HonestInterview/ProductionFull_v5/logs/probe.txt";
var s = "version=" + fl.version + "\n";
var docs = fl.documents;
for (var i = 0; i < docs.length; i++) s += "doc " + i + ": " + docs[i].name + " path=" + docs[i].pathURI + " frames=" + docs[i].getTimeline().frameCount + " layers=" + docs[i].getTimeline().layerCount + "\n";
FLfile.write(out, s);
