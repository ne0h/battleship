from enum import Enum

class FieldStatus(Enum):
	WATER = "water",
	SHIP = "ship",
	SHIPDAMAGED = "damaged ship"

class Field:

	def __init__(self, x, y, status):
		self.x = x
		self.y = y
		self.status = status

class Ship:

	def __init__(self, bow, rear, size):
		self.bow  = bow
		self.rear = rear
		self.size = size

class Battleship(Ship):

	def __init__(self, bow, rear):
		super(bow, rear, 5)

class Cruiser(Ship):

	def __init__(self, bow, rear):
		super(bow, rear, 4)

class Destroyer(Ship):

	def __init__(self, bow, rear):
		super(bow, rear, 3)

class Submarine(Ship):

	def __init__(self, bow, rear):
		super(bow, rear, 2)

class PlayingField:

	def getField(self, field):
		return self.__fields[ord(field[0])-65][int(field[1])-1]

	def getPlayingField(self):
		return self.__fields

	def placeShip(self, ship):
		pass


	def __init__(self, length):
		self.__ships = []

		self.__length = length
		self.__fields = [[0 for x in range(length)] for x in range(length)]
		for i in range(length):
			for j in range(length):
				self.__fields[i][j] = Field(i, j, FieldStatus.WATER)
