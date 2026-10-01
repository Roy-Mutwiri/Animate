"""Write a JSFL that opens an XFL in the running Animate, exports PNG frames, optionally attaches
the original audio as a stream sound, saves an FLA, closes the document and writes a log.
Frames are 0-based production frames."""
import os, sys, json


def uri(p):
    p = os.path.abspath(p).replace(os.sep, '/')
    return 'file:///' + p.replace(':', '|', 1)


def make(xfl, out_png_dir, frames, fla=None, log=None, prefix='f', close=True, jsfl_path=None, sound=None):
    os.makedirs(out_png_dir, exist_ok=True)
    log = log or os.path.join(out_png_dir, '_render_log.txt')
    nl = chr(92) + 'n'
    js = []
    js.append('var LOG=%s; var L=""; function w(s){L+=s+"%s";}' % (json.dumps(uri(log)), nl))
    js.append('try {')
    js.append('var t0=new Date().getTime();')
    js.append('var doc=fl.openDocument(%s);' % json.dumps(uri(xfl)))
    js.append('var tl=doc.getTimeline(); w("opened frames="+tl.frameCount+" layers="+tl.layerCount+" lib="+doc.library.items.length);')
    if sound:
        js.append('doc.importFile(%s, true);' % json.dumps(uri(sound)))
        js.append('var snd=null; var it=doc.library.items; for (var i=0;i<it.length;i++){ if(it[i].itemType=="sound") snd=it[i]; }')
        js.append('if (snd) { tl.setSelectedLayers(tl.layerCount-1); tl.addNewLayer("AUDIO_original","normal",false); var li=tl.findLayerIndex("AUDIO_original")[0]; var fr=tl.layers[li].frames[0]; fr.soundLibraryItem=snd; fr.soundSync="stream"; var need=tl.frameCount; tl.setSelectedLayers(li); if (tl.layers[li].frameCount<need) { tl.insertFrames(need-tl.layers[li].frameCount, false, 0); } w("sound attached "+snd.name+" layer "+li+" span "+tl.layers[li].frameCount+" of "+tl.frameCount); } else { w("NO SOUND ITEM"); }')
    js.append('var frames=%s;' % json.dumps(frames))
    js.append('var od=%s;' % json.dumps(uri(out_png_dir)))
    js.append('for (var i=0;i<frames.length;i++){ tl.currentFrame=frames[i]; var n=("000000"+frames[i]).slice(-6); doc.exportPNG(od+"/%s"+n+".png", true, true); }' % prefix)
    js.append('w("exported "+frames.length+" frames in "+((new Date().getTime()-t0)/1000)+"s");')
    if fla:
        js.append('var ok=fl.saveDocument(doc, %s); w("saved fla "+ok);' % json.dumps(uri(fla)))
    if close:
        js.append('fl.closeDocument(doc, false);')
    js.append('} catch(e) { w("ERR "+e); }')
    js.append('FLfile.write(LOG, L+"DONE%s");' % nl)
    jsfl_path = jsfl_path or os.path.join(out_png_dir, '_render.jsfl')
    with open(jsfl_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(js))
    return jsfl_path, log


if __name__ == '__main__':
    xfl, out, frames = sys.argv[1], sys.argv[2], json.loads(sys.argv[3])
    fla = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] != '-' else None
    j, l = make(xfl, out, frames, fla)
    print(j); print(l)
