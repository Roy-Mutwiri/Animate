var doc = fl.createDocument('timeline');
doc.width = 1080;
doc.height = 1920;
doc.frameRate = 24;
doc.backgroundColor = '#d0ceca';
var tl = doc.getTimeline();
while (tl.layers.length > 1) { tl.deleteLayer(0); }
tl.layers[0].name = 'Background';
tl.addNewLayer('Chair_Back_Seat', 'normal');
tl.addNewLayer('Chair_Foreground', 'normal');
tl.addNewLayer('Body_Legs', 'normal');
tl.addNewLayer('Arms', 'normal');
tl.addNewLayer('Brows_Eyes_Head', 'normal');
tl.addNewLayer('Mouth', 'normal');
tl.insertFrames(1701, true);

var layerIndex = {};
for (var li = 0; li < tl.layers.length; li++) {
  layerIndex[tl.layers[li].name] = li;
}

function selectLayer(name, frame) {
  tl.currentLayer = layerIndex[name];
  tl.currentFrame = frame;
  tl.setSelectedLayers(layerIndex[name]);
  tl.setSelectedFrames(frame, frame + 1, true);
  if (frame > 0) { tl.insertKeyframe(frame); }
}
function stroke(w) { doc.setStrokeColor('#181310'); doc.setStrokeSize(w); }
function fill(c) { doc.setFillColor(c); }
function L(x1,y1,x2,y2,w){ stroke(w); doc.addNewLine({x:x1,y:y1},{x:x2,y:y2}); }
function O(l,t,r,b,f,w){ fill(f); stroke(w); doc.addNewOval({left:l,top:t,right:r,bottom:b},false,false); }
function R(l,t,r,b,f,w){ fill(f); stroke(w); doc.addNewRectangle({left:l,top:t,right:r,bottom:b},0,false,false); }

function bg(frame) {
  selectLayer('Background', frame);
  R(0,0,1080,1920,'#d0ceca',1);
  R(0,1328,1080,1920,'#858e84',1);
  R(690,150,920,430,'#faf9f2',7);
  L(805,150,805,430,3);
  L(690,285,920,285,3);
}
function table(frame, side) {
  var x = side == 'left' ? 300 : side == 'right' ? 790 : 540;
  selectLayer('Chair_Back_Seat', frame);
  R(x-90,1018,x+100,1168,'#45453f',4);
}
function chair(frame, x, y, s, pale, side) {
  var back = pale ? '#efd4d0' : '#a39390';
  var seat = pale ? '#f5d7d5' : '#c9b1ae';
  var front = '#73625e';
  selectLayer('Chair_Back_Seat', frame);
  R(x-150*s,y-205*s,x+150*s,y+105*s,back,7);
  R(x-130*s,y+70*s,x+130*s,y+170*s,seat,7);
  selectLayer('Chair_Foreground', frame);
  if (side == 'left') {
    R(x-205*s,y-20*s,x-105*s,y+180*s,front,7);
  } else if (side == 'right') {
    R(x+105*s,y-20*s,x+205*s,y+180*s,front,7);
  } else {
    R(x-210*s,y-20*s,x-110*s,y+180*s,front,7);
    R(x+110*s,y-20*s,x+210*s,y+180*s,front,7);
  }
}
function body(frame, x, y, s, facing) {
  selectLayer('Body_Legs', frame);
  L(x,y+90*s,x,y+390*s,8*s);
  L(x,y+390*s,x-80*s,y+505*s,8*s);
  L(x-80*s,y+505*s,x-145*s,y+725*s,8*s);
  L(x-145*s,y+725*s,x-220*s,y+730*s,8*s);
  L(x,y+390*s,x+80*s,y+505*s,8*s);
  L(x+80*s,y+505*s,x+35*s,y+725*s,8*s);
  L(x+35*s,y+725*s,x+95*s,y+745*s,8*s);
}
function arms(frame, x, y, s, facing, mode) {
  selectLayer('Arms', frame);
  L(x-45*s,y+110*s,x,y+90*s,7*s);
  L(x,y+90*s,x+45*s,y+112*s,7*s);
  if (mode == 'point') {
    L(x+45*s*facing,y+112*s,x+115*s*facing,y+178*s,8*s);
    L(x+115*s*facing,y+178*s,x+235*s*facing,y+160*s,8*s);
    L(x-45*s*facing,y+112*s,x-80*s*facing,y+275*s,8*s);
  } else if (mode == 'object') {
    L(x+45*s*facing,y+112*s,x+95*s*facing,y+40*s,8*s);
    L(x+95*s*facing,y+40*s,x+170*s*facing,y+72*s,8*s);
    L(x-45*s*facing,y+112*s,x-80*s*facing,y+278*s,8*s);
  } else {
    L(x-45*s,y+112*s,x-115*s,y+275*s,8*s);
    L(x+45*s,y+112*s,x+115*s,y+275*s,8*s);
  }
}
function head(frame, x, y, s, cap, faceMode) {
  selectLayer('Brows_Eyes_Head', frame);
  O(x-78*s,y-78*s,x+78*s,y+78*s,'#d9ddd4',7*s);
  if (cap) {
    fill('#181310'); stroke(1); doc.addNewOval({left:x-80*s,top:y-84*s,right:x+70*s,bottom:y-28*s},false,false);
    R(x-135*s,y-62*s,x-70*s,y-42*s,'#181310',1);
  }
  O(x-54*s,y-42*s,x-8*s,y+34*s,'#fbfff8',5*s);
  O(x+8*s,y-42*s,x+54*s,y+34*s,'#fbfff8',5*s);
  O(x-31*s,y-15*s,x-15*s,y+8*s,'#181310',1);
  O(x+25*s,y-15*s,x+41*s,y+8*s,'#181310',1);
  if (faceMode == 'shock') {
    L(x-60*s,y-58*s,x-18*s,y-78*s,5*s);
    L(x+18*s,y-78*s,x+60*s,y-58*s,5*s);
  } else if (faceMode == 'skeptical') {
    L(x-60*s,y-56*s,x-18*s,y-70*s,5*s);
    L(x+18*s,y-64*s,x+60*s,y-52*s,5*s);
  } else {
    L(x-60*s,y-58*s,x-18*s,y-52*s,5*s);
    L(x+18*s,y-52*s,x+60*s,y-58*s,5*s);
  }
}
function mouth(frame, x, y, s, mode) {
  selectLayer('Mouth', frame);
  if (mode == 'open') {
    O(x-32*s,y+42*s,x+36*s,y+104*s,'#2b1716',5*s);
  } else if (mode == 'teeth') {
    R(x-42*s,y+52*s,x+44*s,y+82*s,'#f4eee9',5*s);
    L(x-38*s,y+67*s,x+40*s,y+67*s,2*s);
  } else if (mode == 'round') {
    O(x-22*s,y+48*s,x+26*s,y+95*s,'#2b1716',5*s);
  } else {
    L(x-38*s,y+66*s,x+38*s,y+62*s,5*s);
  }
}
function pose(frame, mode) {
  bg(frame);
  if (mode == 'two') {
    table(frame, 'center');
    chair(frame, 315, 790, .86, false, 'both');
    chair(frame, 780, 790, .86, true, 'both');
    body(frame, 315, 575, .86, 1); arms(frame,315,575,.86,1,'rest'); head(frame,315,575,.86,false,'skeptical'); mouth(frame,315,575,.86,'closed');
    body(frame, 780, 575, .86, -1); arms(frame,780,575,.86,-1,'rest'); head(frame,780,575,.86,true,'neutral'); mouth(frame,780,575,.86,'closed');
  } else if (mode == 'respondent') {
    table(frame, 'right');
    chair(frame, 415, 885, 1.12, true, 'left');
    body(frame,415,565,1.12,1); arms(frame,415,565,1.12,1,'point'); head(frame,415,565,1.12,true,'neutral'); mouth(frame,415,565,1.12,'teeth');
  } else {
    table(frame, 'left');
    chair(frame, 650, 885, 1.12, false, 'right');
    body(frame,650,565,1.12,-1); arms(frame,650,565,1.12,-1,'object'); head(frame,650,565,1.12,false,'shock'); mouth(frame,650,565,1.12,'open');
  }
}

var keys = [
  [0,'two'],[56,'two'],[59,'respondent'],[61,'respondent'],[64,'respondent'],[68,'respondent'],[73,'respondent'],
  [107,'interviewer'],[118,'interviewer'],[184,'interviewer'],[185,'interviewer'],[193,'interviewer'],
  [207,'respondent'],[449,'respondent'],[455,'two'],[492,'interviewer'],[563,'respondent'],[566,'respondent'],
  [603,'respondent'],[614,'respondent'],[620,'interviewer'],[662,'interviewer'],[898,'respondent'],
  [902,'respondent'],[907,'interviewer'],[912,'interviewer'],[947,'respondent'],[1050,'respondent'],
  [1131,'respondent'],[1196,'respondent'],[1210,'interviewer'],[1252,'respondent'],[1323,'interviewer'],
  [1371,'interviewer'],[1402,'respondent'],[1411,'respondent'],[1490,'interviewer'],[1495,'interviewer'],
  [1549,'interviewer'],[1551,'respondent'],[1574,'respondent'],[1597,'respondent'],[1603,'respondent'],
  [1689,'respondent'],[1701,'respondent']
];
for (var i = 0; i < keys.length; i++) { pose(keys[i][0], keys[i][1]); }
fl.saveDocument(doc, 'file:///D:/Animate/Projects/HonestInterview/ProductionFull_v4/editable/honest_interview_full_v4_layered_keyed_timeline.fla');
