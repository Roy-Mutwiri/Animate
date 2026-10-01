var LOG="file:///D|/Animate/Projects/HonestInterview/ProductionFull_v5/tests/jawtest/_render_log.txt"; var L=""; function w(s){L+=s+"\n";}
try {
var t0=new Date().getTime();
var doc=fl.openDocument("file:///D|/Animate/Projects/HonestInterview/ProductionFull_v5/xfl/jawtest/jawtest.xfl");
var tl=doc.getTimeline(); w("opened frames="+tl.frameCount+" layers="+tl.layerCount+" lib="+doc.library.items.length);
var frames=[205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 620, 621, 622, 623, 624, 625, 626, 627, 628, 629, 630, 631, 632, 633, 634, 635, 636, 637, 638, 639, 640, 641, 642, 643, 644, 645, 646, 647, 648, 649, 650, 651, 652, 653, 654, 655, 656, 657, 658, 659, 660, 661, 662, 663, 664, 1596, 1597, 1598, 1599, 1600, 1601, 1602, 1603, 1604, 1605, 1606, 1607, 1608, 1609, 1610, 1611, 1612, 1613, 1614, 1615, 1616, 1617, 1618, 1619, 1620, 1621, 1622, 1623, 1624, 1625, 1626, 1627, 1628, 1629, 1630, 1631, 1632, 1633, 1634, 1635, 1636, 1637, 1638, 1639, 1640, 1641, 1642, 1643, 1644, 1645, 1646, 1647, 1648, 1649, 1650, 1651];
var od="file:///D|/Animate/Projects/HonestInterview/ProductionFull_v5/tests/jawtest";
for (var i=0;i<frames.length;i++){ tl.currentFrame=frames[i]; var n=("000000"+frames[i]).slice(-6); doc.exportPNG(od+"/f"+n+".png", true, true); }
w("exported "+frames.length+" frames in "+((new Date().getTime()-t0)/1000)+"s");
fl.closeDocument(doc, false);
} catch(e) { w("ERR "+e); }
FLfile.write(LOG, L+"DONE\n");