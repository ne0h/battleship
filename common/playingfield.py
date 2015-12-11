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

class PlayingField:

	def getField(self, field):
		return self.__fields[ord(field[0])-65][int(field[1])-1]

	def getPlayingField(self):
		return self.__fields

	def __init__(self, length):
		self.__length = length
		self.__fields = [[0 for x in range(length)] for x in range(length)]
		for i in range(length):
			for j in range(length):
				self.__fields[i][j] = Field(i, j, FieldStatus.WATER)
