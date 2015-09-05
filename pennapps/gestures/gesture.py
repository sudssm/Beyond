import moosegesture

gestureMap = {
  ('U',): "up",
  ('L',): "left",
  ('R',): "right",
  ('D',): "down",
  ('R', 'D', 'L', 'U',): "sq_cw_tl",
  ('D', 'R', 'U', 'L',): "sq_ccw_tl",
  ('DR', 'L', 'UR',): "tr_cw_top",
  ('R', 'UL', 'DL',): "tr_cw_bl",
  ('R', 'DR', 'DL', 'UL', 'UR',): "superman",
  ('DR', 'U', 'DL', 'UR', 'L',): "star"
}


def importPoints (filename):
  ham = 20
  points = []
  with open(filename,'r') as f:
    for l in f.readlines():
      [x,y]= [int(p) for p in l.rstrip().split(" ")]

      if len(points) == 0 or abs(points[-1][0] - x) > ham or abs(points[-1][1] - y) > ham:
        points.append((x,y))

  return points

def lookup (points):
  strokes = moosegesture.getGesture(points)
  gestures = moosegesture.findClosestMatchingGesture(strokes, 
    gestureMap.keys(),
    tolerance=10)

  print strokes

  for gesture in gestures:
    if gesture in gestureMap:
      return gestureMap[gesture]
    else:
      print "NOT FOUND:",gesture

print lookup (importPoints("in/star.in"))

'''
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
'''
#print("cross:", g.get_score(cross))
#print("check:", g.get_score(check))
#print("circle:", g.get_score(circle))
#print("square:", g.get_score(square))

# use database to find the more alike gesture, if any



#print lookup("in/square2.in")

