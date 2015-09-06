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
  ('R', 'D', 'L', 'U',): "sq_cw_tl",
  ('D', 'R', 'U', 'L',): "sq_ccw_tl",
  ('DR', 'L', 'UR',): "tr_cw_top",
  ('R', 'UL', 'DL',): "tr_cw_bl",
  ('UL', 'DL','R',): "tr_cw_br",
  #('R', 'DR', 'DL', 'UL', 'UR',): "superman",
  #('DR', 'U', 'DL', 'UR', 'L',): "star"
}


def importPoints (filename):
  print "importing", filename
  ham = 5
  points = []
  with open(filename,'r') as f:
    for l in f.readlines():
      [x,y]= [int(p) for p in l.rstrip().split(" ")]

      if len(points) == 0 or (abs(points[-1][0] - x) + abs(points[-1][1] - y)) > ham:
        points.append((x,y))
  return points

def lookup (points):
  strokes = moosegesture.getGesture(points)
  if len(strokes) == 0:
    return None
  possibles = gestureMap.keys()
  gestures = moosegesture.findClosestMatchingGesture(strokes, 
    gestureMap.keys(),
    tolerance=15)

  print strokes

  for gesture in gestures:
    return gestureMap[gesture]

# print lookup (importPoints("in/star.in"))

# print lookup (importPoints("in/square.in"))
# print ""
# print lookup (importPoints("in/square2.in"))
# print ""
# print lookup (importPoints("in/square3.in"))
# print ""
# print lookup (importPoints("in/square4.in"))
# print ""
# print lookup (importPoints("in/triangle.in"))
# print ""

# print lookup(importPoints("in/superman.in"))
# print lookup(importPoints("in/superman2.in"))

# print lookup(importPoints("in/right.in"))
# print lookup(importPoints("in/down.in"))

