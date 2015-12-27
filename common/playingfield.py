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

		return (otherField.x is self.x and otherField.y is self.y)

	def __init__(self, x, y):
		self.x = x
		self.y = y

def splitShip(bow, rear):
	"""
	Splits a ship up.

	Args:
		bow -- the bow of the ship
		rear -- the rear of the ship

	Return:
		Returns a list of fields.
	"""

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

	def __init__(self, bow, rear):
		self.bow  = bow
		self.rear = rear

		self.parts = splitShip(bow, rear)

class Battleship(Ship):
	"""
	A battleship.

	Args:
		bow -- field where the ship starts
		rear -- field where the ship ends
	"""

	def __init__(self, bow, rear):
		Ship.__init__(self, bow, rear)

class Cruiser(Ship):
	"""
	A cruiser.

	Args:
		bow -- field where the ship starts
		rear -- field where the ship ends
	"""

	def __init__(self, bow, rear):
		Ship.__init__(self, bow, rear)

class Destroyer(Ship):
	"""
	A destroyer.

	Args:
		bow -- field where the ship starts
		rear -- field where the ship ends
	"""

	def __init__(self, bow, rear):
		Ship.__init__(self, bow, rear)

class Submarine(Ship):
	"""
	A submarine.

	Args:
		bow -- field where the ship starts
		rear -- field where the ship ends
	"""

	def __init__(self, bow, rear):
		Ship.__init__(self, bow, rear)

class ShipList:
	"""
	Manages all ships on the playing field.
	"""

	def __checkForCollisionWithOtherShips(self, ship):
		"""
		Validates that there is no collision with an existing Ship.

		Args:
			field -- the field to validate

		Return:
			Returns true if there is no collision or false if not.
		"""

		for part in splitShip(ship.bow, ship.rear):
			for s in self.getShips():
				parts = splitShip(s.bow, s.rear)
				for p in parts:
					if part.equals(p):
						return False

		return True

	def __checkForCollisionsWithBorders(self, ship):
		"""
		Validates that the Ship does not collides of any of the game border.

		Args:
			ship -- the ship to validate

		Return:
			Returns true if there is no collision or false if not.
		"""

		return (ship.bow.x  >= 0 and ship.bow.x  < self.__fieldLength
			and ship.bow.y  >= 0 and ship.bow.y  < self.__fieldLength
			and ship.rear.x >= 0 and ship.rear.x < self.__fieldLength
			and ship.rear.y >= 0 and ship.rear.y < self.__fieldLength)

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
			bow -- the bow of the Ship to add
			rear -- the rear of the Ship to add

		Return:
			Returns the newly built ship or None if there was any game rule violation
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

		# build ship
		if length is 5:
			ship = Battleship(bow, rear)
		elif length is 4:
			ship = Destroyer(bow, rear)
		elif length is 3:
			ship = Cruiser(bow, rear)
		else:
			ship = Submarine(bow, rear)
		
		# check for collisions with previously placed ships
		if not self.__checkForCollisionWithOtherShips(ship):
			return None

		# check playing field borders
		if not self.__checkForCollisionsWithBorders(ship):
			return None

		# all checks done - add ship to specific list
		if length is 5 and len(self.__battleships) < self.__maxBattleshipCount:
			self.__battleships.append(ship)
		elif length is 4 and len(self.__destroyers) < self.__maxDestroyerCount:
			self.__destroyers.append(ship)
		elif length is 3 and len(self.__cruisers) < self.__maxCruiserCount:
			self.__cruisers.append(ship)
		elif length is 2 and len(self.__submarines) < self.__maxSubmarineCount:
			self.__submarines.append(ship)
		else:
			return None

		return ship

	def __init__(self, fieldLength, maxBattleshipCount=1, maxDestroyerCount=2, maxCruiserCount=3, maxSubmarineCount=4):
		self.__fieldLength = fieldLength

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
			bow -- bow of the ship
			rear -- rear of the ship

		Return:
			Returns the newly built ship or None of the Ship could not be placed, because of violation of a game rule.
		"""

		return self.__ships.add(bow, rear)

	def __init__(self, fieldLength):
		self.__ships = ShipList(fieldLength)
		self.__fieldLength = fieldLength
