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
  ('U','D',): "updown",
  ('L','R',): "leftright,"
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

def identify_hold(points):
  if len(points) < 3: 
    return False 
  for i in range(len(points) -1):
    d = moosegesture._distance(points[i], points[i+1])
    if d > 30:
      return False       
  return True 

def lookup (points):
  strokes = moosegesture.getGesture(points)
  if len(strokes) == 0:
    if identify_hold(points):
      if len(points) > 10:
        return "long_hold"
      else: 
        return "short_hold"
    return None
  possibles = gestureMap.keys()
  gestures = moosegesture.findClosestMatchingGesture(strokes, 
    gestureMap.keys(),
    tolerance=3)

  print strokes

  if gestures == None:
    return None

  gestures = [gestureMap[x] for x in gestures]

  for g in gestures:
    print "potential", g
  
  for shape in ["updown", "triangle", "square", "leftright", "upright", \
                "upleft", "downleft", "downright"]:
    if shape in gestures:
      return shape

  return gestures[0]