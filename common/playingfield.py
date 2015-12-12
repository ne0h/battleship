from enum import Enum

class FieldStatus(Enum):
	"""Desribes the status of a field.
	"""

	WATER = "water",
	SHIP = "ship",
	SHIPDAMAGED = "damaged ship"

class FieldAddress:
	"""Describes the address of a single field on the playing field.

	Args:
		x -- horizontal coordinate starting in the top left corner
		y -- vertical coordinate starting in the top left corner
	"""

	def toString(self):
		return chr(self.y + 65) + str(self.x + 1)

	def __init__(self, x, y):
		self.x = x
		self.y = y

class Field:
	"""Describes a single field on the playing field.

	Args:
		x -- horizontal coordinate starting in the top left corner
		y -- vertical coordinate starting in the top left corner
		status -- the status of the field
	"""

	def __init__(self, x, y, status):
		FieldAddress.__init__(self, x, y)
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
		Ship.__init__(self, bow, rear, 5)

class Cruiser(Ship):
	"""A cruiser.

	Args:
		bow -- field where the ship starts
		rear -- field where the ship ends
	"""

	def __init__(self, bow, rear):
		Ship.__init__(self, bow, rear, 4)

class Destroyer(Ship):
	"""A destroyer.

	Args:
		bow -- field where the ship starts
		rear -- field where the ship ends
	"""

	def __init__(self, bow, rear):
		Ship.__init__(self, bow, rear, 3)

class Submarine(Ship):
	"""
	A submarine.

	Args:
		bow -- field where the ship starts
		rear -- field where the ship ends
	"""

	def __init__(self, bow, rear):
		Ship.__init__(self, bow, rear, 2)

class PlayingField:
	"""
	A complete playing field the consists of 16x16 fields

	Args:
		length -- the dimension of playing field
	"""

	def getField(self, fieldAddress):
		"""
		Returns a single field.

		Args:
			fieldAddress -- the field

		Returns:
			A single field
		"""

		return self.__fields[fieldAddress.y - 1][fieldAddress.x - 1]

	def getPlayingField(self):
		"""
		Returns the complete playing field.

		Returns:
			the complete playing field
		"""

		return self.__fields

	def __updateField(self, field):
		self.__fields[field.x][field.y].status = field.status

	def placeShip(self, ship):
		"""
		Places a ship on the playing field.

		Args:
			ship -- the ship to place
		"""

		if ship.bow.x is ship.rear.x:
			print("| " + int(ship.bow.x))
			if ship.bow.y > ship.rear.y:
				for i in range(ship.bow.y, ship.rear.y):
					self.__updateField(FieldAddress(ship.box.x, i, FieldStatus.SHIP))
			else:
				for i in range(ship.rear.y, ship.bow.y):
					print("fu: " + str(i) + ":" + str(ship.bow.y))
					self.__updateField(FieldAddress(ship.box.x, i, FieldStatus.SHIP))
		else:
			if ship.bow.x > ship.rear.x:
				for i in range(ship.bow.x, ship.rear.x):
					self.__updateField(FieldAddress(i, ship.bow.y, FieldStatus.SHIP))
			else:
				for i in range(ship.rear.x, ship.bow.x):
					self.__updateField(FieldAddress(i, ship.bow.y, FieldStatus.SHIP))
		


	def __init__(self, length):
		self.__ships = []

		self.__length = length
		self.__fields = [[0 for x in range(length)] for x in range(length)]
		for i in range(length):
			for j in range(length):
				self.__fields[i][j] = Field(i, j, FieldStatus.WATER)
