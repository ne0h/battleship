from enum import Enum

class OrientationDirection(Enum):
	"""
	The different directions.
	"""

	NORTH = "north",
	WEST  = "west",
	SOUTH = "south",
	EAST  = "east"

class Orientation:

	def invert(self):
		"""
		Inverts the current orientation orientationDirection.
		"""

		if self.__orientationDirection is OrientationDirection.NORTH:
			self.__orientationDirection = OrientationDirection.SOUTH
		elif self.__orientationDirection is OrientationDirection.WEST:
			self.__orientationDirection = OrientationDirection.EAST
		elif self.__orientationDirection.OrientationDirection.SOUTH:
			self.__orientationDirection = OrientationDirection.NORTH
		else:
			self.__orientationDirection = OrientationDirection.WEST

	def __init__(self, orientationDirection):
		self.__orientationDirection = orientationDirection

class Field:
	"""
	Describes a single field on the playing field.

	Args:
		x -- horizontal coordinate starting in the top left corner
		y -- vertical coordinate starting in the top left corner
	"""

	def toString(self):
		return chr(self.y + 65) + str(self.x + 1)

	def equals(self, otherField):
		"""
		Standard equals method.
		"""

		return (otherField.x is self.x and otherField.y is y)

	def __init__(self, x, y):
		self.x = x
		self.y = y

def splitShip(bow, rear):
	result = []

	# horizontal orientation
	if bow.y is rear.y:
		if rear.x > bow.x:
			for i in range(bow.x, rear.x + 1):
				result.append(Field(i, bow.y))
		else:
			for i in range(rear.x, bow.x + 1):
				result.append(Field(i, bow.y))

	# vertical orientation
	if bow.x is rear.x:
		if rear.y > bow.y:
			for i in range(bow.y, rear.y + 1):
				result.append(Field(bow.x, i))
		else:
			for i in range(rear.y, bow.y + 1):
				result.append(Field(bow.x, i))

	return result

class Ship:
	"""
	Describes a ship.

	Args:
		bow -- the starting field of the ship
		rear -- the ending field of the ship
		size -- the size of the ship
	"""

	def __init__(self, bow, rear, size):
		self.bow  = bow
		self.rear = rear
		self.size = size

		self.parts = splitShip(bow, rear)

class Battleship(Ship):
	"""
	A battleship.

	Args:
		bow -- field where the ship starts
		rear -- field where the ship ends
	"""

	def __init__(self, bow, rear):
		Ship.__init__(self, bow, rear, 5)

class Cruiser(Ship):
	"""
	A cruiser.

	Args:
		bow -- field where the ship starts
		rear -- field where the ship ends
	"""

	def __init__(self, bow, rear):
		Ship.__init__(self, bow, rear, 4)

class Destroyer(Ship):
	"""
	A destroyer.

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
	"""
	Manages all ships on the playing field.
	"""

	def __checkForCollision(self, field):
		"""
		Validates that there is no collision with an existing Ship.

		Args:
			field -- the field to validate

		Return:
			Returns true if there is no collision or false if not.
		"""

		for ship in self.getShips():
			parts = self.__splitShip(ship)
			for part in parts:
				if field.equals(part):
					return False

		return True

	def getShips(self):
		"""
		Returns a list of all Ships.

		Return:
			Returns a list of all Ships.
		"""
		result = []

		result.extend(self.__battleships)
		result.extend(self.__destroyers)
		result.extend(self.__cruisers)
		result.extend(self.__submarines)

		return result

	def add(self, bow, rear):
		"""
		Adds a new Ship to the playing field. Validates if the maximum count of this kind of ship is reached.

		Args:
			ship -- the Ship to add
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
		#if not self.__ships.

		# check playing field borders

		# all checks done - build ship
		if length is 5:
			self.__battleships.append(Battleship(bow, rear))
		elif length is 4:
			self.__destroyers.append(Destroyer(bow, rear))
		elif length is 3:
			self.__cruisers.append(Cruiser(bow, rear))
		else:
			self.__submarines.append(Submarine(bow, rear))

		return True

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

	def getShips(self):
		return self.__ships.getShips()

	def placeShip(self, bow, rear):
		"""
		Places a ship on the playing field.

		Args:

		"""

		return self.__ships.add(bow, rear)

	def __init__(self, length):
		self.__ships = ShipList()
		self.__length = length
