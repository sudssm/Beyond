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
  ('DR', 'L', 'UR',): "tr_cw_top",
  ('UR', 'DR', 'L',): "tr_cw_bl",
  ('L', 'UR','DR',): "tr_cw_br",
}

def add_rotations(pattern, name, reverse=False):
  shift = pattern
  while 1:
    shift = shift[1:] + shift[0:1]
    gestureMap[shift] = name

    if shift == pattern:
      if reverse:
        add_rotations(pattern, name)
      return


add_rotations(('R', 'D', 'L', 'U',), "square", True)

add_rotations(('UR', 'DR', 'L',), "triangle", True)
add_rotations(('U', 'DR', 'L',), "triangle", True)
add_rotations(('UR', 'D', 'L',), "triangle", True)

add_rotations(('UL', 'R', 'D',), "triangle", True)
add_rotations(('UL', 'UR', 'D',), "triangle", True)
add_rotations(('UL', 'U', 'DR',), "triangle", True)


moosegesture._MIN_STROKE_LEN = 80

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
    tolerance=3)

  print strokes

  if gestures == None:
    return None
  for gesture in gestures:
    print "potential", gestureMap[gesture]
  
  return gestureMap[gesture]
'''
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
'''
