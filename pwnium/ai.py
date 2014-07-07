import sys
import random
import math
import socket
import time
import copy

class Board:
  def __init__(self, arr, numempty):
    self.__arr = arr
    self.__numempty = numempty
    self.__max = 0

  def spawn(self):
    if self.__numempty > 1:
      r = random.randrange(0,self.__numempty-1)
    else:
      r = 0
    empty = [i for i in range(16) if self.__arr[i]==0]
    num = 4 if random.random()>=0.9 else 2
    if num > self.__max:
      self.__max = num
    self.__arr[empty[r]] = num
    self.__numempty -= 1

  def getNumempty(self):
    return self.__numempty

  def gameover(self):
    return not (self.canMoveLeft() or self.canMoveRight() or self.canMoveUp() or self.canMoveDown())

  def canMoveRight(self):
    for i in range(4):
      for j in range(3):
        me = self.__arr[4*i+j]
        nbr = self.__arr[4*i+j+1]
        if me !=0 and (me == nbr or nbr == 0):
          return True
    return False

  def canMoveLeft(self):
    for i in range(4):
      for j in range(3,0,-1):
        me = self.__arr[4*i+j]
        nbr = self.__arr[4*i+j-1]
        if me !=0 and (me == nbr or nbr == 0):
          return True
    return False

  def canMoveUp(self):
    for j in range(4):
      for i in range(3,0,-1):
        me = self.__arr[4*i+j]
        nbr = self.__arr[4*(i-1)+j]
        if me !=0 and (me == nbr or nbr == 0):
          return True
    return False

  def canMoveDown(self):
    for j in range(4):
      for i in range(3):
        me = self.__arr[4*i+j]
        nbr = self.__arr[4*(i+1)+j]
        if me !=0 and (me == nbr or nbr == 0):
          return True
    return False

  def left(self):
    for i in range(4):
      # shift left
      j = 0
      while j < 4 :
        val = self.__arr[4*i+j]
        if val == 0 or j == 0:
          j += 1
        elif j > 0 and val != 0 and self.__arr[4*i+j-1] == 0:
          self.__arr[4*i+j-1] = val
          self.__arr[4*i+j] = 0
          j -= 1
        else:
          j += 1
      # combine
      for j in range(3):
        if self.__arr[4*i+j] > 0 and self.__arr[4*i+j] == self.__arr[4*i+j+1]:
          self.__arr[4*i+j] *= 2
          self.__arr[4*i+j+1] = 0
          self.__numempty += 1
          if self.__max < self.__arr[4*i+j]:
            self.__max = self.__arr[4*i+j]

      # shift left
      j = 0
      while j < 4 :
        val = self.__arr[4*i+j]
        if val == 0 or j == 0:
          j += 1
        elif j > 0 and val != 0 and self.__arr[4*i+j-1] == 0:
          self.__arr[4*i+j-1] = val
          self.__arr[4*i+j] = 0
          j -= 1
        else:
          j += 1
    #spawn new tile
    self.spawn()
    return self

  def right(self):
    for i in range(4):
      # shift right
      j = 3
      while j > -1 :
        val = self.__arr[4*i+j]
        if val == 0 or j == 3:
          j -= 1
        elif j < 3 and val != 0 and self.__arr[4*i+j+1] == 0:
          self.__arr[4*i+j+1] = val
          self.__arr[4*i+j] = 0
          j += 1
        else:
          j -= 1
      # combine
      for j in range(3,0,-1):
        if self.__arr[4*i+j] > 0 and self.__arr[4*i+j] == self.__arr[4*i+j-1]:
          self.__arr[4*i+j] *= 2
          self.__arr[4*i+j-1] = 0
          self.__numempty += 1
          if self.__max < self.__arr[4*i+j]:
            self.__max = self.__arr[4*i+j]
      # shift right
      j = 3
      while j > -1 :
        val = self.__arr[4*i+j]
        if val == 0 or j == 3:
          j -= 1
        elif j < 3 and val != 0 and self.__arr[4*i+j+1] == 0:
          self.__arr[4*i+j+1] = val
          self.__arr[4*i+j] = 0
          j += 1
        else:
          j -= 1
    self.spawn()
    return self

  def up(self):
    for j in range(4):
      # shift up
      i = 0
      while i < 4 :
        val = self.__arr[4*i+j]
        if val == 0 or i == 0:
          i += 1
        elif i > 0 and val != 0 and self.__arr[4*(i-1)+j] == 0:
          self.__arr[4*(i-1)+j] = val
          self.__arr[4*i+j] = 0
          i -= 1
        else:
          i += 1
      # combine
      for i in range(3):
        if self.__arr[4*i+j] > 0 and self.__arr[4*i+j] == self.__arr[4*(i+1)+j]:
          self.__arr[4*i+j] *= 2
          self.__arr[4*(i+1)+j] = 0
          self.__numempty += 1
          if self.__max < self.__arr[4*i+j]:
            self.__max = self.__arr[4*i+j]
      # shift up
      i = 0
      while i < 4 :
        val = self.__arr[4*i+j]
        if val == 0 or i == 0:
          i += 1
        elif i > 0 and val != 0 and self.__arr[4*(i-1)+j] == 0:
          self.__arr[4*(i-1)+j] = val
          self.__arr[4*i+j] = 0
          i -= 1
        else:
          i += 1
    self.spawn()
    return self

  def down(self):
    for j in range(4):
      # shift down
      i = 3
      while i > -1 :
        val = self.__arr[4*i+j]
        if val == 0 or i == 3:
          i -= 1
        elif i < 3 and val != 0 and self.__arr[4*(i+1)+j] == 0:
          self.__arr[4*(i+1)+j] = val
          self.__arr[4*i+j] = 0
          i += 1
        else:
          i -= 1
      # combine
      for i in range(3,0,-1):
        if self.__arr[4*i+j] > 0 and self.__arr[4*i+j] == self.__arr[4*(i-1)+j]:
          self.__arr[4*i+j] *= 2
          self.__arr[4*(i-1)+j] = 0
          self.__numempty += 1
          if self.__max < self.__arr[4*i+j]:
            self.__max = self.__arr[4*i+j]
      # shift down
      i = 3
      while i > -1 :
        val = self.__arr[4*i+j]
        if val == 0 or i == 3:
          i -= 1
        elif i < 3 and val != 0 and self.__arr[4*(i+1)+j] == 0:
          self.__arr[4*(i+1)+j] = val
          self.__arr[4*i+j] = 0
          i += 1
        else:
          i -= 1
    self.spawn()
    return self

  def toList(self):
    return self.__arr

  def __str__(self):
    s = "%*d %*d %*d %*d \n%*d %*d %*d %*d \n%*d %*d %*d %*d \n%*d %*d %*d %*d" % tuple([item for list in zip([len(str(self.__max))]*16,self.__arr) for item in list])
    return s


###############################################
# decide - Outer Recursive Function
#
# Input:
# b      - 2048 board
# hf     - heuristic function
# height - recursion height (>= 0)
# Output:
# dir    - which direction to go
###############################################
def decide(b,hf,height):
  dir = "none"
  max = -1*float("inf")
  if height <= 0:
    print("Invalid Recursion Height (Must be > 0)!");
    return "error"
  else:
    if b.canMoveLeft():
      bnew = copy.deepcopy(b)
      val = rec(bnew.left(),hf,height-1)
      if max < val:
        dir = "left"
        max = val
    if b.canMoveRight():
      bnew = copy.deepcopy(b)
      val = rec(bnew.right(),hf,height-1)
      if max < val:
        dir = "right"
        max = val
    if b.canMoveUp():
      bnew = copy.deepcopy(b)
      val = rec(bnew.up(),hf,height-1)
      if max < val:
        dir = "up"
        max = val
    if b.canMoveDown():
      bnew = copy.deepcopy(b)
      val = rec(bnew.down(),hf,height-1)
      if max < val:
        dir = "down"
        max = val
    return dir


###############################################
# rec - Internal Recursive Function
#
# Input:
# b      - 2048 board
# hf     - heuristic function
# height - recursion height (>= 0)
# Output:
# res    - minimum heuristic value
###############################################
def rec(b,hf,height):
  if height < 0:
    print("Recursion height < 0!!!");
    return -1;
  if height == 0:
    return hf(b)
  else:
    children = []
    if b.canMoveLeft():
      bnew = copy.deepcopy(b)
      children.append(bnew.left())
    if b.canMoveRight():
      bnew = copy.deepcopy(b)
      children.append(bnew.right())
    if b.canMoveUp():
      bnew = copy.deepcopy(b)
      children.append(bnew.up())
    if b.canMoveDown():
      bnew = copy.deepcopy(b)
      children.append(bnew.down())

    #bnew = copy.deepcopy(b)
    #children.append(bnew.down())

    if len(children) == 0:
      return -1*float("inf")
    else:
      return max([rec(x,hf,height-1) for x in children])

###############################################
# Empty Spaces Heuristic
#
# Input:
# b - a 2048 board
# Output
# res - number of empty tiles on the board
###############################################
def h1(b):
  return b.getNumempty()

###############################################
# 2 Count
#
# Input:
# b - a 2048 board
# Output
# res - number of twos on the board
###############################################
def h2(b):
  count = b.toList().count(2)
  if count == 0:
    return float("inf")
  else:
    return 1/count

###############################################
# Sum of Squares
#
# Input:
# b - a 2048 board
# Output
# res - sum of the squares of the entries
###############################################
def h3(b):
  return sum([x^2 for x in b.toList()])


###############################################
# Modified Sum of Squares
#
# Input:
# b - a 2048 board
# Output
# res - modified sum of squares of the entries
###############################################
def h4(b):
  return sum([(x-2)^2 for x in b.toList()])

###############################################
# Weighted number of empty spaces
#
# Input:
# b - a 2048 board
# Output
# res - Number of empty spaces times largest tile
###############################################
def h5(b):
  return b.getNumempty()**2  * max(b.toList())

###############################################
# Penalized max tile
#
# Input:
# b - a 2048 board
# Output
# res - Maximum tile penalized if less then 5 tiles present
###############################################
def h6(b):
  return max(b.toList()) * math.e**(b.getNumempty()-5)


###############################################
# Number of 2's w/ too few spaces penalized
#
# Input:
# b - a 2048 board
# Output
# res - 1/(# 2's) penalized if less than 5 tiles present
###############################################
def h7(b):
  count = (b.toList()).count(2)
  if count == 0:
    return math.e**(b.getNumempty()-5)
  else:
    return 1/(count) * math.e**(b.getNumempty()-5)

###############################################
# Number of 2's w/ too few spaces penalized
#
# Input:
# b - a 2048 board
# Output
# res - 1/(# 2's) penalized if less than 5 tiles present
###############################################
def h8(b):
  return sum([x^2 for x in b.toList()]) * math.e**(b.getNumempty()-5)


###############################################
# AI Body
###############################################
def getMove(b, hf=h8, height=3):
  dir = decide(b,hf,height)
  if dir == "error":
    print 'error'
    sys.exit()
  elif dir == "left":
    return 'l'
  elif dir == "right":
    return 'r'
  elif dir == "up":
    return 'u'
  elif dir == "down":
    return 'd'
  elif dir == "none":
    # make an arbitrary choice
    if b.canMoveLeft():
      return 'l'
    elif b.canMoveRight():
      return 'r'
    elif b.canMoveUp():
      return 'u'
    else:
      return 'd'

WTIME = 0.1

URL  = '41.231.53.40'
PORT = 2048

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((URL, PORT))

time.sleep(WTIME)

while True:
  response = s.recv(1024)
  if 'Game Over' in response:
    print response
    break
  if '2048' in response or 'flag' in response:
    print response  

  lines = response.split('\n')
  arr = []
  for line in lines:
    empty = 0
    if len(line) > 0 and line[0] in ['.', '1', '2', '3', '4', '5', '6', '8']:
      tiles = line.split(' ')
      for tile in tiles:
        if tile == '.':
          arr.append(0)
          empty += 1
        elif tile != '':
          # print tile
          arr.append(int(tile))

  board = Board(arr, empty)
  move = getMove(board)
  s.send(move + '\n')