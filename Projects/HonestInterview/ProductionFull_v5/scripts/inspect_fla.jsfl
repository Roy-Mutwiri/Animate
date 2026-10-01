// Reopen the delivered FLA and report its real editable structure (read-only: closes without saving).
var base = "file:///D|/Animate/Projects/HonestInterview/ProductionFull_v5/";
var LOG = base + "logs/inspect_v5d.txt";
var L = "";
function w(s) { L += s + "\n"; }
try {
  var doc = fl.openDocument(base + "editable/honest_interview_v5d.fla");
  var tl = doc.getTimeline();
  w("document " + doc.name + " " + doc.width + "x" + doc.height + " fps=" + doc.frameRate + " frames=" + tl.frameCount + " layers=" + tl.layerCount);
  for (var i = 0; i < tl.layerCount; i++) {
    var ly = tl.layers[i];
    var keys = 0, snd = "";
    for (var f = 0; f < ly.frameCount; f++) {
      var fr = ly.frames[f];
      if (fr.startFrame == f) { keys++; if (fr.soundLibraryItem) snd = " sound=" + fr.soundLibraryItem.name + " sync=" + fr.soundSync; }
    }
    w("layer " + i + " " + ly.name + " span=" + ly.frameCount + " keyframes=" + keys + snd);
  }
  var it = doc.library.items;
  var names = [];
  for (var j = 0; j < it.length; j++) names.push(it[j].name + "(" + it[j].itemType + (it[j].timeline ? "," + it[j].timeline.frameCount + "f" : "") + ")");
  w("library " + it.length + ": " + names.join(", "));
  var mi = tl.findLayerIndex("CAP_mouth")[0];
  var probe = [216, 253, 1600, 1695];
  for (var p = 0; p < probe.length; p++) {
    var el = tl.layers[mi].frames[probe[p]].elements;
    w("CAP_mouth frame " + probe[p] + ": " + (el.length ? el[0].libraryItem.name + " firstFrame=" + el[0].firstFrame + " loop=" + el[0].loop : "empty"));
  }
  fl.closeDocument(doc, false);
} catch (e) { w("ERR " + e); }
FLfile.write(LOG, L + "DONE\n");
