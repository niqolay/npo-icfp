import sys
import copy
import random

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

class MapSamples:
  def __init__(self):
    self.maps = []
    self.maps.append(self.map1())
    self.maps.append(self.map2())
    self.maps.append(self.map3())
    self.maps.append(self.map4())
    self.maps.append(self.map5())
    self.maps.append(self.map6())
    self.maps.append(self.map7())
    self.maps.append(self.map8())
    self.maps.append(self.map9())
  def map(self, index):
    return self.maps[index]
  def map1(self):
    map = Map()
    map.load(    \
      [r'######', \
       r'#. *R#', \
       r'#  \.#', \
       r'#\ * #', \
       r'L  .\#', \
       r'######'])
    return map
  def map2(self):
    map = Map()
    map.load(       \
      [r'#######',  \
       r'#..***#',  \
       r'#..\\\#',  \
       r'#...**#',  \
       r'#.*.*\#',  \
       r'LR....#',  \
       r'#######'])
    return map
  def map3(self):
    map = Map()
    map.load(      \
      [r'########', \
       r'#..R...#', \
       r'#..*...#', \
       r'#..#...#', \
       r'#.\.\..L', \
       r'####**.#', \
       r'#\.....#', \
       r'#\..* .#', \
       r'########'])
    return map
  def map4(self):
    map = Map()
    map.load(
      [r'#########', \
       r'#.*..#\.#', \
       r'#.\..#\.L', \
       r'#.R .##.#', \
       r'#.\  ...#', \
       r'#..\  ..#', \
       r'#...\  ##', \
       r'#....\ \#', \
       r'#########'])
    return map
  def map5(self):
    map = Map()
    map.load(          \
      [r'############', \
       r'#..........#', \
       r'#.....*....#', \
       r'#..\\\\\\..#', \
       r'#.     ....#', \
       r'#..\\\\\\\.#', \
       r'#..\..    .#', \
       r'#..\.. ....#', \
       r'#..... ..* #', \
       r'#..### ### #', \
       r'#...R#\#\\.#', \
       r'######L#####'])
    return map
  def map6(self):
    map = Map()
    map.load(             \
      [r'###############', \
       r'#\\\.......** #', \
       r'#\\#.#####...##', \
       r'#\\#.....*##. #', \
       r'#\#####\...## #', \
       r'#\......####* #', \
       r'#\.######* #.\#', \
       r'#\.#. *...##.##', \
       r'#\##. ..  *...#', \
       r'#\...... L#.#.#', \
       r'###########.#.#', \
       r'#\..........#.#', \
       r'##.##########.#', \
       r'#R.#\.........#', \
       r'###############'])
    return map
  def map7(self):
    map = Map()
    map.load(              \
      [r' #######        ', \
       r' ##    *#       ', \
       r'  ##R  *##      ', \
       r'   ##\\\\##     ', \
       r'    ##....##    ', \
       r'   ##..\ . ##   ', \
       r'  ## . L .  ##  ', \
       r' ##\\\# #\\\\## ', \
       r'######   #######'])
    return map
  def map8(self):
    map = Map()
    map.load(
      [r'##############',        \
       r'#\\... ......#',        \
       r'###.#. ...*..#',        \
       r'#.#. ... ..#',          \
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
    return map
  def map9(self):
    map = Map()
    map.load(
      [r'        #L#######         ', \
       r'        #*** \\ #         ', \
       r'        #\\\ .. #         ', \
       r'#########.##    ##########', \
       r'#.......\ ..........*   .#', \
       r'#*******\......#....#\\ .#', \
       r'###\.\\\...**..#....... *#', \
       r'#*****\\  .\\..##     #\.#', \
       r'######### ....  ##########', \
       r'        #       #         ', \
       r'        ####*####         ', \
       r'        #.......#         ', \
       r'#########  \\\\*##########', \
       r'#*\\  **#     *..*\ \\\\\#', \
       r'#.\**\*** .....**.# \\##\#', \
       r'#\R......     .\\.. \\\\\#', \
       r'##########################'])
    return map

class MoveCodes:
  LEFT_MOVE_CODE = 'L'
  RIGHT_MOVE_CODE = 'R'
  UP_MOVE_CODE = 'U'
  DOWN_MOVE_CODE = 'D'
  ABORT_MOVE_CODE = 'A'
  WAIT_MOVE_CODE = 'W'
  @staticmethod
  def movecodecount():
    return 6
  @staticmethod
  def targetx(x, move):
    if (move == MoveCodes.LEFT_MOVE_CODE):
      return x - 1
    elif (move == MoveCodes.RIGHT_MOVE_CODE):
      return x + 1
    else:
      return x
  @staticmethod
  def targety(y, move):
    if (move == MoveCodes.UP_MOVE_CODE):
      return y + 1
    elif (move == MoveCodes.DOWN_MOVE_CODE):
      return y - 1
    else:
      return y
  @staticmethod
  def movecodetoindex(movecode):
    if (movecode == MoveCodes.LEFT_MOVE_CODE):
      return 0
    elif (movecode == MoveCodes.RIGHT_MOVE_CODE):
      return 1
    elif (movecode == MoveCodes.UP_MOVE_CODE):
      return 2
    elif (movecode == MoveCodes.DOWN_MOVE_CODE):
      return 3
    elif (movecode == MoveCodes.ABORT_MOVE_CODE):
      return 4
    elif (movecode == MoveCodes.WAIT_MOVE_CODE):
      return 5
  @staticmethod
  def indextomovecode(index):
    if (index == 0):
      return MoveCodes.LEFT_MOVE_CODE
    elif (index == 1):
      return MoveCodes.RIGHT_MOVE_CODE
    elif (index == 2):
      return MoveCodes.UP_MOVE_CODE
    elif (index == 3):
      return MoveCodes.DOWN_MOVE_CODE
    elif (index == 4):
      return MoveCodes.ABORT_MOVE_CODE
    elif (index == 5):
      return MoveCodes.WAIT_MOVE_CODE

class MapState:
  WINNING = 0
  DEATH = 1
  RUNNING = 2
  ABORT = 3
  @staticmethod
  def tostring(value):
    if value == MapState.WINNING:
      return "WINNING"
    elif value == MapState.DEATH:
      return "DEATH"
    elif value == MapState.RUNNING:
      return "RUNNING"
    elif value == MapState.ABORT:
      return "ABORT"
    else:
      return "UNKNOWN"

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
      map.roboX = self.newX
      map.roboY = self.newY
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
    
class Diff:
  def __init__(self):
    self.moves = []
  def moveRobo(self, oldX, oldY, newX, newY):
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
    self.roboX = -1
    self.roboY = -1
    self.route = []
    self.routeXs = []
    self.routeYs = []
  def rowcount(self):
    return len(self.map)
  def colcount(self):
    return len(self.map[0])
  def load(self, lines):
    self.map = []
    for line in lines:
      self.map.insert(0, line.rstrip('\n'))
    maxlength = 0
    for line in self.map:
      if len(line) > maxlength:
        maxlength = len(line)
    for i in range(len(self.map)):
      self.map[i] = self.map[i].ljust(maxlength)
    for lineIndex in range(len(self.map)):
      self.map[lineIndex] = list(self.map[lineIndex])
    for currentY in range(len(self.map)):
      for currentX in range(len(self.map[currentY])):
        if (self.map[currentY][currentX] == ROBO_CODE):
          self.roboX = currentX
          self.roboY = currentY
    self.distances = [[1.0 for i in range(self.colcount())] for j in range(self.rowcount())]
    self.updatedistances()
  def updatedistances(self):
    WALL_CELL_WEIGHT = sys.maxint
    EMPTY_CELL_WEIGHT = sys.maxint - 1
    TARGET_CELL_WEIGHT = 0
    isliftopened = 0
    for row in range(self.rowcount()):
      for column in range(self.colcount()):    
        if (self.map[row][column] == OPEN_LIFT_CODE):
          isliftopened = 1
    for row in range(self.rowcount()):
      for column in range(self.colcount()):
        if ((isliftopened == 0) & (self.map[row][column] == LAMBDA_CODE)) | \
           ((isliftopened == 1) & (self.map[row][column] == OPEN_LIFT_CODE)):
          self.distances[row][column] = TARGET_CELL_WEIGHT      
        elif (self.map[row][column] in [GRASS_CODE, EMPTY_CODE, OPEN_LIFT_CODE, ROCK_CODE]):
          self.distances[row][column] = EMPTY_CELL_WEIGHT
        else:
          self.distances[row][column] = WALL_CELL_WEIGHT
    for iteration in range(self.rowcount() * self.colcount()):
      for row in range(1, self.rowcount() - 1):
        for column in range(1, self.colcount() - 1):
          if (self.distances[row][column] != WALL_CELL_WEIGHT):
            minvalue = min( \
              self.distances[row - 1][column], \
              self.distances[row + 1][column], \
              self.distances[row][column - 1], \
              self.distances[row][column + 1]) + 1
            if (minvalue < self.distances[row][column]):
              self.distances[row][column] = minvalue
    for row in range(self.rowcount()):
      for column in range(self.colcount()):              
        self.distances[row][column] = float(self.distances[row][column]) / float(sys.maxint)
  def show(self):
    for index in range(len(self.map)):
      print "".join(self.map[len(self.map) - index - 1])
    print "MapState: " + str(MapState.tostring(self.mapState))
    print "Scores: " + str(self.scores)
    print "Lambdas: " + str(self.collectedLambda)
    print "Route: " + str("".join(self.route))
  def apply(self, diff):
    result = copy.deepcopy(self)
    for move in diff.moves:
      move.beforeapply(result)
    for move in diff.moves:
      move.afterapply(result)
    return result
  def getmapitem(self, x, y):
    if (x >= 0) & (x < self.colcount()) & \
       (y >= 0) & (y < self.rowcount()):
      return self.map[y][x]
    else:
      return WALL_CODE
  def setmapitem(self, x, y, value):
    if (x >= 0) & (x <= self.colcount()) & \
       (y >= 0) & (y <= self.rowcount()):
      self.map[y][x] = value
  def move(self, moveCode, resultDiff):        
    if (self.mapState == MapState.RUNNING):
      targetX = MoveCodes.targetx(self.roboX, moveCode)
      targetY = MoveCodes.targety(self.roboY, moveCode)
      if moveCode == MoveCodes.ABORT_MOVE_CODE:
        resultDiff.updateMapState(MapState.ABORT)
      if (self.isallowedmove(targetX, targetY)):
        resultDiff.moveRobo(self.roboX, self.roboY, targetX, targetY)
      if (self.getmapitem(targetX, targetY) == LAMBDA_CODE):
        resultDiff.collectLambda()
      if (self.getmapitem(targetX, targetY) == OPEN_LIFT_CODE):
        resultDiff.updateMapState(MapState.WINNING)
      if (moveCode == MoveCodes.LEFT_MOVE_CODE) & \
         (self.getmapitem(targetX, targetY) == ROCK_CODE) & \
         (self.getmapitem(targetX - 1, targetY) == EMPTY_CODE):
        resultDiff.moveRock(targetX, targetY, targetX - 1, targetY)
      if (moveCode == MoveCodes.RIGHT_MOVE_CODE) & \
         (self.getmapitem(targetX, targetY) == ROCK_CODE) & \
         (self.getmapitem(targetX + 1, targetY) == EMPTY_CODE):
        resultDiff.moveRock(targetX, targetY, targetX + 1, targetY)
    return resultDiff  
  def update(self, resultDiff):
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
              resultDiff.moveRock(currentX, currentY, targetX, targetY)
              if (self.getmapitem(targetX, targetY - 1) == ROBO_CODE):
                resultDiff.updateMapState(MapState.DEATH)
      if (lambdaCount == 0):
        resultDiff.openLift(liftx, lifty)
    return resultDiff
  def fullmove(self, move):
    self.route.append(move)
    map = self.apply(self.move(move, Diff()))
    map.routeXs.append(map.roboX)
    map.routeYs.append(map.roboY)    
    map = map.apply(map.update(Diff()))
    map.updatedistances()
    return map
  def isalive(self):
    if (self.mapState == MapState.RUNNING):
      if (self.map[self.roboY - 1][self.roboX] in [WALL_CODE, ROCK_CODE]) & \
         (self.map[self.roboY + 1][self.roboX] in [WALL_CODE, ROCK_CODE]) & \
         (self.map[self.roboY][self.roboX + 1] in [WALL_CODE, ROCK_CODE]) & \
         (self.map[self.roboY][self.roboX - 1] in [WALL_CODE, ROCK_CODE]):
        return 0
      else:
        return 1
    return 0
  def isallowedmove(self, targetx, targety):
    if (self.getmapitem(targetx, targety) == LAMBDA_CODE) |  \
       (self.getmapitem(targetx, targety) == GRASS_CODE) |   \
       (self.getmapitem(targetx, targety) == EMPTY_CODE) |   \
       (self.getmapitem(targetx, targety) == OPEN_LIFT_CODE):
      return 1
    if (targetx == self.roboX - 1) & \
       (self.getmapitem(targetx, targety) == ROCK_CODE) & \
       (self.getmapitem(targetx - 1, targety) == EMPTY_CODE):
      return 1
    if (targetx == self.roboX + 1) & \
       (self.getmapitem(targetx, targety) == ROCK_CODE) & \
       (self.getmapitem(targetx + 1, targety) == EMPTY_CODE):
      return 1
    return 0
    
class Emulator:
  def play(self):
    map = MapSamples().map(0)
    while map.mapState == MapState.RUNNING:  
      map.show()
      move = raw_input("Enter step:")
      move.rstrip('\n')
      map = map.fullmove(move)
    map.show()
    print map.mapState    
   
class PathFinder:
  def __init__(self, antCount, routeDepth, map, targetScores, volatizing, alpha, beta):
    self.antCount = antCount
    self.routeDepth = routeDepth
    self.targetScores = targetScores
    self.volatizing = volatizing
    self.alpha = alpha
    self.beta = beta
    self.map = map
    self.mapRowCount = map.rowcount()
    self.mapColCount = map.colcount()    
    self.pheromones = [[[1.0 for k in range(MoveCodes.movecodecount())] for i in range(self.mapColCount)] for j in range(self.mapRowCount)]
    self.ants = [self.createant() for i in range(self.antCount)]    
  def createant(self):
    return copy.deepcopy(self.map)  
  def selectmove(self, ant):
    column = ant.roboX
    row = ant.roboY
    probabilities = [0.0 for i in range(MoveCodes.movecodecount())]
    probabilitysum = 0.0
    for moveindex in range(MoveCodes.movecodecount()):
      move = MoveCodes.indextomovecode(moveindex)
      targetcolumn = MoveCodes.targetx(column, move)
      targetrow = MoveCodes.targety(row, move)
      if ant.isallowedmove(targetcolumn, targetrow) | (move == MoveCodes.WAIT_MOVE_CODE):
        probabilities[moveindex] = (self.pheromones[row][column][moveindex] ** self.alpha) * (abs(1.0 - ant.distances[targetrow][targetcolumn]) ** self.beta)
        probabilitysum = probabilitysum + probabilities[moveindex]
    if probabilitysum == 0.0:
      return MoveCodes.WAIT_MOVE_CODE
    for moveindex in range(MoveCodes.movecodecount()):
      probabilities[moveindex] = probabilities[moveindex] / probabilitysum
    r = random.random()
    moveindex = 0
    accumulatedprobability = probabilities[0]
    while (accumulatedprobability < r):
      moveindex = moveindex + 1
      accumulatedprobability += probabilities[moveindex]
    return MoveCodes.indextomovecode(moveindex)
  def updatepheromones(self):
    deltapheromones = [[[0.0 for k in range(MoveCodes.movecodecount())] for i in range(self.mapColCount)] for j in range(self.mapRowCount)] 
    for ant in self.ants:
      delta = (ant.scores + self.routeDepth) / self.targetScores
      if not ant.isalive():
        delta = -delta
      for posIndex in range(len(ant.route)):
        xpos = ant.routeXs[posIndex]
        ypos = ant.routeYs[posIndex]
        movecode = ant.route[posIndex]
        moveindex = MoveCodes.movecodetoindex(movecode)
        deltapheromones[ypos][xpos][moveindex] += delta
    for column in range(self.mapColCount):
      for row in range(self.mapRowCount):
        for move in range(MoveCodes.movecodecount()):
          self.pheromones[row][column][move] = self.pheromones[row][column][move] * self.volatizing + deltapheromones[row][column][move]
  def show(self):
    for antindex in range(len(self.ants)):
      print "AntIndex: " + str(antindex)
      ant = self.ants[antindex]
      ant.show()
    print "Pheromones: " + str(self.pheromones)
  def find(self):
    for time in range(self.routeDepth):
      for antIndex in range(len(self.ants)):
        move = self.selectmove(self.ants[antIndex])
        self.ants[antIndex] = self.ants[antIndex].fullmove(move)
      maxAnt = None
      maxAntScores = -sys.maxint
      for ant in self.ants:
        if ant.scores > maxAntScores:
          maxAntScores = ant.scores
          maxAnt = ant
      for antIndex in range(len(self.ants)):
        if (not self.ants[antIndex].isalive()) & (self.ants[antIndex] != maxAnt):
          self.ants[antIndex] = self.createant()
      self.updatepheromones()
    return maxAnt
  def dofind(self):
    ant = self.find()
    ant.show()
    return
        
map = MapSamples().map(2)
PathFinder(antCount = 50, routeDepth = 50, map = map, targetScores = 225, volatizing = 1.0, alpha = 1.0, beta = 2.0).dofind()