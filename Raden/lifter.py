import sys
import copy

LEFT_MOVE_CODE = 'L'
RIGHT_MOVE_CODE = 'R'
UP_MOVE_CODE = 'U'
DOWN_MOVE_CODE = 'D'
ABORT_MOVE_CODE = 'A'
WAIT_MOVE_CODE = 'W'

WALL_CODE = '#'
LAMBDA_CODE = '\\'
GRASS_CODE = '.'
EMPTY_CODE = ' '
OPEN_LIFT_CODE = 'O'
CLOSED_LIFT_CODE = 'L'
ROCK_CODE = '*'
ROBO_CODE = 'R'

LAMBDA_COLLECTED_SCORES = 25
WINNING_PER_LAMBDA_SCORES = 50
ABORT_PER_LAMBDA_SCORES = 25

class MapState:
  WINNING = 0
  DEATH = 1
  RUNNING = 2
  ABORT = 3

class Move:
  def __init__(self, oldX, oldY, newX, newY, code):
    self.oldX = oldX
    self.oldY = oldY
    self.newX = newX
    self.newY = newY
    self.code = code
  def beforeapply(self, map):
    map.setmapitem(self.oldX, self.oldY, EMPTY_CODE)
  def afterapply(self, map):
    map.setmapitem(self.newX, self.newY, self.code)
    if (self.code == ROBO_CODE):
      map.scores = map.scores - 1
    
class Transform:
  def __init__(self, x, y, code):
    self.x = x
    self.y = y
    self.code = code
  def beforeapply(self, map):
    return
  def afterapply(self, map):
    map.setmapitem(self.x, self.y, self.code)
    
class CollectLambda:
  def beforeapply(self, map):
    return
  def afterapply(self, map):
    map.scores = map.scores + LAMBDA_COLLECTED_SCORES
    map.collectedLambda = map.collectedLambda + 1
    
class UpdateMapState:
  def __init__(self, code):
    self.code = code
  def beforeapply(self, map):
    return
  def afterapply(self, map):
    map.mapState = self.code
    if (self.code == MapState.WINNING):
      map.scores = map.scores + map.collectedLambda * WINNING_PER_LAMBDA_SCORES
    elif (self.code == MapState.ABORT):
      map.scores = map.scores + map.collectedLambda * ABORT_PER_LAMBDA_SCORES
    
class State:
  def __init__(self, roboX = None, roboY = None, baseState = None):
    if (baseState is None):
      self.roboX = roboX
      self.roboY = roboY
    else:
      self.roboX = baseState.roboX
      self.roboY = baseState.roboY
    self.baseState = baseState
    self.moves = []
  def moveRobo(self, oldX, oldY, newX, newY):
    self.roboX = newX
    self.roboY = newY
    self.moves.append(Move(oldX, oldY, newX, newY, ROBO_CODE))
  def moveRock(self, oldX, oldY, newX, newY):
    self.moves.append(Move(oldX, oldY, newX, newY, ROCK_CODE))
  def openLift(self, x, y):
    self.moves.append(Transform(x, y, OPEN_LIFT_CODE))
  def collectLambda(self):
    self.moves.append(CollectLambda())
  def updateMapState(self, code):
    self.moves.append(UpdateMapState(code))
        
class Map:
  def __init__(self):
    self.scores = 0
    self.collectedLambda = 0
    self.mapState = MapState.RUNNING
  def decompact(self):
    maxlength = 0
    for line in self.map:
      if len(line) > maxlength:
        maxlength = len(line)
    for i in range(len(self.map)):
      self.map[i] = self.map[i].ljust(maxlength)
  # use sys.stdin as parameter to load from standard input
  def load(self, lines):
    self.map = []
    for line in lines:
      self.map.insert(0, line.rstrip('\n'))
    self.decompact()
    for lineIndex in range(len(self.map)):
      self.map[lineIndex] = list(self.map[lineIndex])
  def show(self):
    for index in range(len(self.map)):
      print "".join(self.map[len(self.map) - index - 1])
    print "Scores: " + str(self.scores)
    print "Lambdas: " + str(self.collectedLambda)
  def state(self):
    for currentY in range(len(self.map)):
      for currentX in range(len(self.map[currentY])):
        if (self.map[currentY][currentX] == ROBO_CODE):
          result = State(currentX, currentY, None)
          return result
  def apply(self, state):
    if not (state.baseState is None):
      result = self.apply(state.baseState)
    else:
      result = Map()
      result.map = copy.deepcopy(self.map)
    for move in state.moves:
      move.beforeapply(result)
    for move in state.moves:
      move.afterapply(result)
    return result
  def getmapitem(self, x, y):
    if (x >= 0) & (x <= len(self.map)) & \
       (y >= 0) & (y <= len(self.map[0])):
      return self.map[y][x]
    else:
      return WALL_CODE
  def setmapitem(self, x, y, value):
    if (x >= 0) & (x <= len(self.map)) & \
       (y >= 0) & (y <= len(self.map[0])):
      self.map[y][x] = value
  def move(self, oldState, moveCode):    
    resultState = State(baseState = oldState)
    if (self.mapState == MapState.RUNNING):
      targetX = oldState.roboX
      targetY = oldState.roboY
      if moveCode == LEFT_MOVE_CODE:
        targetX = targetX - 1
      elif moveCode == RIGHT_MOVE_CODE:
        targetX = targetX + 1
      elif moveCode == UP_MOVE_CODE:
        targetY = targetY + 1
      elif moveCode == DOWN_MOVE_CODE:
        targetY = targetY - 1
      elif moveCode == ABORT_MOVE_CODE:
        resultState.updateMapState(MapState.ABORT)
    
      if (self.getmapitem(targetX, targetY) == LAMBDA_CODE) |  \
         (self.getmapitem(targetX, targetY) == GRASS_CODE) |   \
         (self.getmapitem(targetX, targetY) == EMPTY_CODE) |   \
         (self.getmapitem(targetX, targetY) == OPEN_LIFT_CODE):
        resultState.moveRobo(oldState.roboX, oldState.roboY, targetX, targetY)
      if (self.getmapitem(targetX, targetY) == LAMBDA_CODE):
        resultState.collectLambda()
      if (self.getmapitem(targetX, targetY) == OPEN_LIFT_CODE):
        resultState.updateMapState(MapState.WINNING)
      if (moveCode == LEFT_MOVE_CODE) & \
         (self.getmapitem(targetX, targetY) == ROCK_CODE) & \
         (self.getmapitem(targetX - 1, targetY) == EMPTY_CODE):
        resultState.moveRobo(oldState.roboX, oldState.roboY, targetX, targetY)
        resultState.moveRock(targetX, targetY, targetX - 1, targetY)
      if (moveCode == RIGHT_MOVE_CODE) & \
         (self.getmapitem(targetX, targetY) == ROCK_CODE) & \
         (self.getmapitem(targetX + 1, targetY) == EMPTY_CODE):
        resultState.moveRobo(oldState.roboX, oldState.roboY, targetX, targetY)
        resultState.moveRock(targetX, targetY, targetX + 1, targetY)
    return resultState
      
  def update(self, resultState):
    if (self.mapState == MapState.RUNNING):
      liftx = -1
      lifty = -1
      lambdaCount = 0
      for currentY in range(len(self.map)):
        for currentX in range(len(self.map[currentY])):
          if (self.getmapitem(currentX, currentY) == LAMBDA_CODE):
            lambdaCount = lambdaCount + 1
          if (self.getmapitem(currentX, currentY) == CLOSED_LIFT_CODE):
            liftx = currentX
            lifty = currentY
          if (self.getmapitem(currentX, currentY) == ROCK_CODE):
            targetX = -1
            targetY = -1
            if (self.getmapitem(currentX, currentY - 1) == EMPTY_CODE):
              targetX = currentX
              targetY = currentY - 1
            elif ((self.getmapitem(currentX, currentY - 1) == ROCK_CODE) | \
                 (self.getmapitem(currentX, currentY - 1) == LAMBDA_CODE)) & \
                 (self.getmapitem(currentX + 1, currentY) == EMPTY_CODE) & \
                 (self.getmapitem(currentX + 1, currentY - 1) == EMPTY_CODE):
              targetX = currentX + 1
              targetY = currentY - 1
            elif (self.getmapitem(currentX, currentY - 1) == ROCK_CODE) & \
                 (self.getmapitem(currentX - 1, currentY) == EMPTY_CODE) & \
                 (self.getmapitem(currentX - 1, currentY - 1) == EMPTY_CODE):
              targetX = currentX - 1
              targetY = currentY - 1
            if (targetX >= 0) & (targetY >= 0):
              resultState.moveRock(currentX, currentY, targetX, targetY)
              if (self.getmapitem(targetX, targetY - 1) == ROBO_CODE):
                resultState.updateMapState(MapState.DEATH)
      if (lambdaCount == 0):
        resultState.openLift(liftx, lifty)
    return resultState
    
map = Map()
#map.load(    \
#  ['######', \
#   '#. *R#', \
#   '#  \.#', \
#   '#\ * #', \
#   'L  .\#', \
#   '######'])

#map.load(
#[r'##############',        \
# r'#\\... ......#',        \
# r'###.#. ...*..#',        \
# r'#.#. ... ..#',          \
# r'### #.   \ ..#',        \
# r'#. .#..... **#######',  \
# r'#.#\#..... ..\\\*. #',  \
# r'#*\\#.###. ####\\\ #',  \
# r'#\\.#.     ...## \ #',  \
# r'#\#.#..... ....# \ #',  \
# r'###.#..... ....#   ##', \
# r'#\\.#..... ....#\   #', \
# r'########.. ..###*####', \
# r'#......... .........#', \
# r'#......... ....***..#', \
# r'#..\\\\\ # ####.....#', \
# r'#........*R..\\\   .#', \
# r'##########L##########'])

map.load(
  [r'##############',        \
   r'#\\... ......#',        \
   r'###.#. ...*..#',        \
   r'  #.#. ... ..#',        \
   r'### #.   \ ..#',        \
   r'#. .#..... **#######',  \
   r'#.#\#..... ..\\\*. #',  \
   r'#*\\#.###. ####\\\ #',  \
   r'#\\.#.     ...## \ #',  \
   r'#\#.#..... ....# \ #',  \
   r'###.#..... ....#   ##', \
   r'#\\.#..... ....#\   #', \
   r'########.. ..###*####', \
   r'#......... .........#', \
   r'#......... ....***..#', \
   r'#..\\\\\ # ####.....#', \
   r'#........*R..\\\   .#', \
   r'##########L##########'])

state = map.state()
while map.mapState == MapState.RUNNING:  
  map.show()
  move = raw_input("Enter step:")
  move.rstrip('\n')
  state = map.move(state, move)
  map = map.apply(state)
  state = map.update(state)
  map = map.apply(state)
map.show()
print map.mapState


    