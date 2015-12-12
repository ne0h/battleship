from enum import Enum

class FieldStatus(Enum):
	"""Desribes the status of a field.
	"""

	WATER = "water",
	SHIP = "ship",
	SHIPDAMAGED = "damaged ship"

class Field:
	"""Describes a single field on the playing field.

	Args:
		x -- horizontal coordinate starting in the top left corner
		y -- vertical coordinate starting in the top left corner
	"""

	def __init__(self, x, y, status):
		self.x = x
		self.y = y
		self.status = status

class Ship:
	"""Describes a ship.

	Args:
		bow -- the starting field of the ship
		rear -- the ending field of the ship
		size -- the size of the ship
	"""

	def __init__(self, bow, rear, size):
		self.bow  = bow
		self.rear = rear
		self.size = size

class Battleship(Ship):
	"""A battleship.

	Args:
		bow -- field where the ship starts
		rear -- field where the ship ends
	"""

	def __init__(self, bow, rear):
		super(bow, rear, 5)

class Cruiser(Ship):
	"""A cruiser.

	Args:
		bow -- field where the ship starts
		rear -- field where the ship ends
	"""

	def __init__(self, bow, rear):
		super(bow, rear, 4)

class Destroyer(Ship):
	"""A destroyer.

	Args:
		bow -- field where the ship starts
		rear -- field where the ship ends
	"""

	def __init__(self, bow, rear):
		super(bow, rear, 3)

class Submarine(Ship):
	"""
	A submarine.

	Args:
		bow -- field where the ship starts
		rear -- field where the ship ends
	"""

	def __init__(self, bow, rear):
		super(bow, rear, 2)

class PlayingField:
	"""
	A complete playing field the consists of 16x16 fields

	Args:
		length -- the dimension of playing field
	"""

	def getField(self, field):
		"""
		Returns a single field.

		Args:
			field -- the field

		Returns:
			A single field
		"""

		return self.__fields[ord(field[0])-65][int(field[1])-1]

	def getPlayingField(self):
		"""
		Returns the complete playing field.

		Returns:
			the complete playing field
		"""

		return self.__fields

	def placeShip(self, ship):
		"""
		Places a ship on the playing field.

		Args:
			ship -- the ship to place
		"""

		pass


	def __init__(self, length):
		self.__ships = []

		self.__length = length
		self.__fields = [[0 for x in range(length)] for x in range(length)]
		for i in range(length):
			for j in range(length):
				self.__fields[i][j] = Field(i, j, FieldStatus.WATER)
