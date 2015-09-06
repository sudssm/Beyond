import moosegesture

gestureMap = {
  ('U',): "up",
  ('L',): "left",
  ('R',): "right",
  ('D',): "down",
  ('UR',): "upright",
  ('UL',): "upleft",
  ('DR',): "downright",
  ('DL',): "downleft",
  #('U', 'DL', 'UR', 'DR',): "up_arrow",
  ('R', 'D', 'L', 'U',): "sq_cw_tl",
  ('D', 'R', 'U', 'L',): "sq_ccw_tl",
  ('DR', 'L', 'UR',): "tr_cw_top",
  ('UR', 'DR', 'L',): "tr_cw_bl",
  ('L', 'UR','DR',): "tr_cw_br",
}


moosegesture._MIN_STROKE_LEN = 60

def importPoints (filename):
  print "importing", filename
  ham = 5
  points = []
  with open(filename,'r') as f:
    points = [[int(p) for p in l.rstrip().split(" ")] for l in f.readlines()]
  return points


def lookup (points):
  strokes = moosegesture.getGesture(points)
  if len(strokes) == 0:
    return None
  possibles = gestureMap.keys()
  gestures = moosegesture.findClosestMatchingGesture(strokes, 
    gestureMap.keys(),
    tolerance=2)

  print strokes

  if gestures == None:
    return None
  for gesture in gestures:
    return gestureMap[gesture]

print lookup (importPoints("in/star.in"))

print lookup (importPoints("in/square.in"))
print ""
print lookup (importPoints("in/square2.in"))
print ""
print lookup (importPoints("in/square3.in"))
print ""
print lookup (importPoints("in/square4.in"))
print ""
print lookup (importPoints("in/triangle.in"))
print ""

print lookup(importPoints("in/superman.in"))
print lookup(importPoints("in/superman2.in"))

print lookup(importPoints("in/right.in"))
print lookup(importPoints("in/down.in"))

