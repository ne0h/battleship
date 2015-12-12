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

class ShipList:

	def add(self, ship):
		if type(ship).__name__ is "Battleship":
			if len(self.__battleships) < self.__maxBattleshipCount:
				self.__battleships.append(ship)
				return True
			else:
				return False
		elif type(ship).__name__ is "Destroyer":
			if len(self.__destroyers) < self.__maxDestroyerCount:
				self.__destroyers.append(ship)
				return True
			else:
				return False
		elif type(ship).__name__ is "Cruiser":
			if len(self.__cruisers) < self.__maxCruiserCount:
				self.__cruisers.append(ship)
				return True
			else:
				return False
		else:
			if len(self.__submarines) < self.__maxSubmarineCount:
				self.__submarines.append(ship)
				return True
			else:
				return False

	def __init__(self, maxBattleshipCount=1, maxDestroyerCount=2, maxCruiserCount=3, maxSubmarineCount=4):
		self.__battleships = []
		self.__maxBattleshipCount = maxBattleshipCount

		self.__destroyers = []
		self.__maxDestroyerCount = maxDestroyerCount

		self.__cruisers = []
		self.__maxCruiserCount = maxCruiserCount

		self.__submarines = []
		self.__maxSubmarineCount = maxSubmarineCount

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

	def __updateField(self, field, fieldStatus):
		self.__fields[field.y][field.x].status = fieldStatus

	def __splitPotentialShip(self, bow, rear):
		result = []

		# horizontal orientation
		if bow.y is rear.y:
			if rear.x > bow.x:
				for i in range(bow.x, rear.x + 1):
					result.append(FieldAddress(i, bow.y))
			else:
				for i in range(rear.x, bow.x + 1):
					result.append(FieldAddress(i, bow.y))

		# vertical orientation
		if bow.x is rear.x:
			if rear.y > bow.y:
				for i in range(bow.y, rear.y + 1):
					result.append(FieldAddress(bow.x, i))
			else:
				for i in range(rear.y, bow.y + 1):
					result.append(FieldAddress(bow.x, i))

		return result

	def placeShip(self, bow, rear):
		"""
		Places a ship on the playing field.

		Args:
			ship -- the ship to place
			shipParts -- a list with field addresses where the ship is located
		"""
		import math

		# check if bow and rear form a valid ship
		if not (bow.x is rear.x or bow.y is bow.y):
			return None

		# check if the length of the potential ship is valid
		if bow.x is rear.x:
			length = int(math.fabs(bow.y - rear.y)) + 1
		else:
			length = int(math.fabs(bow.x - rear.x)) + 1
		
		if length < 2 or length > 5:
			return None
		
		# check for collisions with previously placed ships
		shipParts = self.__splitPotentialShip(bow, rear)
		for fieldAddress in shipParts:
			if self.getField(fieldAddress).status is not FieldStatus.WATER:
				return None

		# check playing field borders

		# all checks done - build ship
		if length is 5:
			ship = Battleship(bow, rear)
		elif length is 4:
			ship = Destroyer(bow, rear)
		elif length is 3:
			ship = Cruiser(bow, rear)
		else:
			ship = Submarine(bow, rear)

		# updates fields and add ship to list of ships
		if not self.__ships.add(ship):
			return None
		for fieldAddress in shipParts:
			self.__updateField(fieldAddress, FieldStatus.SHIP)

		return ship

	def __init__(self, length):
		self.__ships = ShipList()
		self.__length = length

		self.__fields = [[0 for x in range(length)] for x in range(length)]
		for i in range(length):
			for j in range(length):
				self.__fields[i][j] = Field(i, j, FieldStatus.WATER)
