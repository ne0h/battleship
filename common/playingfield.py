import logging
from enum import Enum

class Orientation(Enum):
	"""
	The different directions.
	"""

	NORTH = "north"
	WEST  = "west"
	SOUTH = "south"
	EAST  = "east"

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
	"""

	def getLength(self):
		return len(self.parts)

	def __init__(self, bow, rear):
		self.bow  = bow
		self.rear = rear

		self.parts = splitShip(bow, rear)

		# calculate orientation
		if bow.y < rear.y:
			self.orientation = Orientation.NORTH
		elif bow.y > rear.y:
			self.orientation = Orientation.SOUTH
		elif bow.x < rear.x:
			self.orientation = Orientation.WEST
		elif bow.x > rear.x:
			self.orientation = Orientation.EAST

		# calculate middle elements
		self.middles = []
		for i in range(1, len(self.parts) - 1):
			self.middles.append(self.parts[i])

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

		result.extend(self.__carriers)
		result.extend(self.__battleships)
		result.extend(self.__cruisers)
		result.extend(self.__destroyers)

		return result

	def moreShipsLeftToPlace(self):
		"""
		Checks if the user has to place more ships.

		Returns:
			Returns True if all ships have been placed or False if not.
		"""

		return not (self.__maxCarrierCount is len(self.__carriers)
			and self.__maxBattleshipCount is len(self.__battleships)
			and self.__maxCruiserCount is len(self.__cruisers)
			and self.__maxDestroyerCount is len(self.__destroyers))

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

		# check if the length of the potential ship is valid
		if bow.x is rear.x:
			length = int(math.fabs(bow.y - rear.y)) + 1
		else:
			length = int(math.fabs(bow.x - rear.x)) + 1
		
		if length < 2 or length > 5:
			print("To small!")
			return None

		# build ship
		ship = Ship(bow, rear)
		
		# check for collisions with previously placed ships
		if not self.__checkForCollisionWithOtherShips(ship):
			print("Collision with ship!")
			return None

		# check playing field borders
		if not self.__checkForCollisionsWithBorders(ship):
			print("Collision with border!")
			return None

		# all checks done - add ship to specific list
		if length is 5 and len(self.__carriers) < self.__maxCarrierCount:
			self.__carriers.append(ship)
			logging.info("Added a carrier. Carrier count is now %s" % (len(self.__carriers)))
		elif length is 4 and len(self.__battleships) < self.__maxBattleshipCount:
			self.__battleships.append(ship)
			logging.info("Added a battleship. battleship count is now %s" % (len(self.__battleships)))
		elif length is 3 and len(self.__cruisers) < self.__maxCruiserCount:
			self.__cruisers.append(ship)
			logging.info("Added a cruiser. Cruiser count is now %s" % (len(self.__cruisers)))
		elif length is 2 and len(self.__destroyers) < self.__maxDestroyerCount:
			self.__destroyers.append(ship)
			logging.info("Added a destroyer. Destroyer count is now %s" % (len(self.__destroyers)))

		return self.moreShipsLeftToPlace()

	def __init__(self, fieldLength, maxCarrierCount=1, maxBattleshipCount=2, maxCruiserCount=3, maxDestroyerCount=4):
		self.__fieldLength = fieldLength

		self.__carriers = []
		self.__maxCarrierCount = maxCarrierCount

		self.__battleships = []
		self.__maxBattleshipCount = maxBattleshipCount

		self.__cruisers = []
		self.__maxCruiserCount = maxCruiserCount

		self.__destroyers = []
		self.__maxDestroyerCount = maxDestroyerCount

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
