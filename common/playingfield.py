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

class FieldStatus(Enum):
	FOG = "fog"
	WATER = "water"
	SHIP = "ship"
	DAMAGEDSHIP = "damagedship"

conditionCodes = {
	"free":      FieldStatus.WATER,
	"damaged":   FieldStatus.DAMAGEDSHIP,
	"undamaged": FieldStatus.SHIP
}

class Field:
	"""
	Describes a single field on the playing field.

	Args:
		x: horizontal coordinate starting in the top left corner
		y: vertical coordinate starting in the top left corner
	"""

	def toString(self):
		return ("%s%s") % (chr(self.x + 65), str(self.y + 1))

	def equals(self, otherField):
		"""
		Standard equals method.
		"""

		return (otherField.x is self.x and otherField.y is self.y)

	def __init__(self, x, y):
		self.x = int(x)
		self.y = int(y)

def splitShip(bow, rear):
	"""
	Splits a ship up.

	Args:
		bow: the bow of the ship
		rear: the rear of the ship

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
		bow: the starting field of the ship
		rear: the ending field of the ship
	"""

	def addDamage(self, part):
		# we do need a copy here
		self.damages.append(Field(part.x, part.y))

	def isDamaged(self, part):
		for damage in self.damages:
			if damage.equals(part):
				return True
		return False

	def getLength(self):
		return len(self.parts)

	def __initShip(self, bow, rear):
		self.bow  = bow
		self.rear = rear
		self.parts = splitShip(bow, rear)

		# calculate middle elements
		self.middles = []
		for i in range(1, len(self.parts) - 1):
			self.middles.append(self.parts[i])

	def move(self, bowNew, rearNew, direction):
		self.__initShip(bowNew, rearNew)

		# move damages
		for damage in self.damages:
			if direction is Orientation.NORTH:
				damage.y += 1
			elif direction is Orientation.WEST:
				damage.x -= 1
			elif direction is Orientation.SOUTH:
				damage.y -= 1
			elif direction is Orientation.EAST:
				damage.x += 1

	def __init__(self, bow, rear):
		self.__initShip(bow, rear)
		self.damages = []

		# calculate orientation
		if bow.y < rear.y:
			self.orientation = Orientation.SOUTH
		elif bow.y > rear.y:
			self.orientation = Orientation.NORTH
		elif bow.x < rear.x:
			self.orientation = Orientation.WEST
		elif bow.x > rear.x:
			self.orientation = Orientation.EAST

class ShipList:
	"""
	Manages all ships on the playing field.
	"""

	def getFieldStatus(self, field):
		for ship in self.getShips():
			for part in ship.parts:
				if field.equals(part):
					if ship.isDamaged(part):
						return FieldStatus.DAMAGEDSHIP, ship
					else:
						return FieldStatus.SHIP, ship
		return FieldStatus.WATER, None

	def getShipAtPosition(self, field):
		ships = self.getShips()
		for i in range(0, len(ships)):
			for damage in ships[i].parts:
				if damage.equals(field):
					return i
		return -1

	def __checkForCollisionWithOtherShips(self, ship):
		"""
		Validates that there is no collision with an existing Ship.

		Args:
			field: the field to validate

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
			ship: the ship to validate

		Return:
			Returns true if there is no collision or false if not.
		"""

		return (0 <= ship.bow.x < self.__fieldLength
			and  0 <= ship.bow.y < self.__fieldLength
			and 0 <= ship.rear.x < self.__fieldLength
			and 0 <= ship.rear.y < self.__fieldLength)

	def __checkForDiagonal(self, ship):
		return not (ship.bow.x == ship.rear.x or ship.bow.y == ship.rear.y)

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

	def getShip(self, shipId):
		"""
		Returns a specified ship from the own playing field.

		Args:
			shipId: the id of the ship

		Returns:
			Returns a specified ship from the own playing field.
		"""

		if shipId is 0:
			return self.__carriers[0]
		if shipId > 0 and shipId < 3:
			shipId = shipId - 1
			return self.__battleships[shipId]
		if shipId > 2 and shipId < 6:
			shipId = shipId - 3
			return self.__cruisers[shipId]
		else:
			shipId = shipId - 6
			return self.__destroyers[shipId]

	def movePossible(self, shipId, direction):
		ship = self.getShip(shipId)
		fieldsToCheck = []

		if ship.orientation is Orientation.NORTH or ship.orientation is Orientation.SOUTH:
			if ship.orientation is Orientation.NORTH:
				if direction is Orientation.NORTH:
					if ship.bow.y > 14:
						return False
					fieldsToCheck.append(Field(ship.bow.x, ship.bow.y + 1))
				elif direction is Orientation.SOUTH:
					if ship.rear.y < 1:
						return False
					fieldsToCheck.append(Field(ship.rear.x, ship.rear.y - 1))

			elif ship.orientation is Orientation.SOUTH:
				if direction is Orientation.NORTH:
					if ship.rear.y > 14:
						return False
					fieldsToCheck.append(Field(ship.rear.x, ship.rear.y + 1))
				elif direction is Orientation.SOUTH:
					if ship.bow.y < 1:
						return False
					fieldsToCheck.append(Field(ship.bow.x, ship.bow.y - 1))

			# check all fields left of the ship
			if direction is Orientation.WEST:
				for part in ship.parts:
					field = Field(part.x - 1, part.y)
					if field.x < 0:
						return False
					fieldsToCheck.append(field)

			# check all fields right of the ship
			if direction is Orientation.EAST:
				for part in ship.parts:
					field = Field(part.x + 1, part.y)
					if field.x > 15:
						return False
					fieldsToCheck.append(field)

		if ship.orientation is Orientation.WEST or ship.orientation is Orientation.EAST:
			if ship.orientation is Orientation.WEST:
				if direction is Orientation.WEST:
					if ship.bow.x < 1:
						return False
					fieldsToCheck.append(Field(ship.bow.x - 1, ship.bow.y))
				elif direction is Orientation.EAST:
					if ship.rear.x > 14:
						return False
					fieldsToCheck.append(Field(ship.rear.x + 1, ship.rear.y))

			elif ship.orientation is Orientation.EAST:
				if direction is Orientation.WEST:
					if ship.bow.x < 1:
						return False
					fieldsToCheck.append(Field(ship.bow.x - 1, ship.bow.y))
				elif direction is Orientation.EAST:
					if ship.bow.x > 14:
						return False
					fieldsToCheck.append(Field(ship.rear.x + 1, ship.rear.y))

			# check all fields above the ship
			if direction is Orientation.NORTH:
				for part in ship.parts:
					field = Field(part.x, part.y + 1)
					if field.y > 15:
						return False
					fieldsToCheck.append(field)

			# check all fields below the ship
			if direction is Orientation.SOUTH:
				for part in ship.parts:
					field = Field(part.x, part.y - 1)
					if field.y < 0:
						return False
					fieldsToCheck.append(field)

		for f in fieldsToCheck:
			status, _ = self.getFieldStatus(f)
			if status is FieldStatus.SHIP or status is FieldStatus.DAMAGEDSHIP:
				return False
		return True

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

	def __testShipPlacement(self, bow, rear):

		# check if the length of the potential ship is valid
		if bow.x is rear.x:
			length = abs(bow.y - rear.y) + 1
		else:
			length = abs(bow.x - rear.x) + 1

		if length < 2 or length > 5:
			logging.error("This type of ship does not exist.")
			return False

		# build ship
		ship = Ship(bow, rear)

		# check if the ship is diagonal
		if self.__checkForDiagonal(ship):
			logging.error("Diagonal ship!")
			return False

		# check for collisions with previously placed ships
		if not self.__checkForCollisionWithOtherShips(ship):
			logging.error("Collision with ship!")
			return False

		# check playing field borders
		if not self.__checkForCollisionsWithBorders(ship):
			logging.error("Collision with border!")
			return False

		return True

	def add(self, bow, rear):
		"""
		Adds a new Ship to the playing field. Validates if the maximum count of this kind of ship is reached.

		Args:
			bow: the bow of the Ship to add
			rear: the rear of the Ship to add

		Return:
			Returns the id of the newly built ship or -1 if there was any game rule violation. In addition returns if
			the user has to place more ships.
		"""
		import math

		if bow.x is rear.x:
			length = abs(bow.y - rear.y) + 1
		else:
			length = abs(bow.x - rear.x) + 1

		if not self.__testShipPlacement(bow, rear):
			return -1, True

		# all checks done - add ship to specific list
		ship = Ship(bow, rear)
		shipId = -1
		if length is 5 and len(self.__carriers) < self.__maxCarrierCount:
			self.__carriers.append(ship)
			shipId = 0
			logging.info("Added a carrier. Carrier count is now %s" % (len(self.__carriers)))
		elif length is 4 and len(self.__battleships) < self.__maxBattleshipCount:
			self.__battleships.append(ship)
			shipId = len(self.__battleships)
			logging.info("Added a battleship. battleship count is now %s" % (len(self.__battleships)))
		elif length is 3 and len(self.__cruisers) < self.__maxCruiserCount:
			self.__cruisers.append(ship)
			shipId = len(self.__cruisers) + 2
			logging.info("Added a cruiser. Cruiser count is now %s" % (len(self.__cruisers)))
		elif length is 2 and len(self.__destroyers) < self.__maxDestroyerCount:
			self.__destroyers.append(ship)
			shipId = len(self.__destroyers) + 5
			logging.info("Added a destroyer. Destroyer count is now %s" % (len(self.__destroyers)))

		return shipId, self.moreShipsLeftToPlace()

	def getCarrierCount(self):
		return len(self.__carriers)

	def getBattleshipCount(self):
		return len(self.__battleships)

	def getCruiserCount(self):
		return len(self.__cruisers)

	def getDestroyerCount(self):
		return len(self.__destroyers)

	def getShipCount(self):
		return self.getCarrierCount() + self.getBattleshipCount() + self.getCruiserCount() + self.getDestroyerCount()

	def move(self, shipId, direction):
		ship = self.getShip(shipId)
		bow = ship.bow
		rear = ship.rear

		if direction is Orientation.NORTH:
			bowNew  = Field(bow.x , bow.y  + 1)
			rearNew = Field(rear.x, rear.y + 1)
		elif direction is Orientation.WEST:
			bowNew  = Field(bow.x  - 1,  bow.y)
			rearNew = Field(rear.x - 1, rear.y)
		elif direction is Orientation.SOUTH:
			bowNew  = Field(bow.x, bow.y   - 1)
			rearNew = Field(rear.x, rear.y - 1)
		else:
			bowNew  = Field(bow.x  + 1,  bow.y)
			rearNew = Field(rear.x + 1, rear.y)

		ship.move(bowNew, rearNew, direction)

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
	A complete playing field that consists of 16x16 fields.

	Args:
		length: the dimension of playing field
	"""

	def __getFieldStatus(self, field):
		"""
		Returns the status of a field together with the ship (if there is one).

		Args:
		    field: the address of the field

		Returns:
			Returns the status of a field together with the ship (if there is one).
		"""

		# check if there is a part of a ship
		return self.__ships.getFieldStatus(field)

	def attack(self, field):
		"""
		The enemy attacks a field.

		Args:
		    field: the field the enemy attacks

		Returns:
			Returns the status of the field after the attack together with True if it changed or False if not.
		"""

		status, ship = self.__getFieldStatus(field)
		updated = False
		if status is FieldStatus.SHIP:
			status = FieldStatus.DAMAGEDSHIP
			ship.addDamage(field)
			updated = True

		# unfog field
		if not self.isUnfogged(field):
			updated = True
			self.unfog(field)

		return status, updated

	def specialAttack(self, field):
		"""
		The enemy attacks a lot of fields.

		Args:
		    field: the most significant field

		Returns:
			A dictionary of fields and statuses that have been updated. Keys are 'field' and 'status'.
		"""

		# calculate all the fields
		fields = [field, Field(field.x, field.y + 1), Field(field.x, field.y + 2),
				  Field(field.x + 1, field.y), Field(field.x + 1, field.y + 1), Field(field.x + 1, field.y + 2),
				  Field(field.x+2, field.y), Field(field.x+2, field.y+1), Field(field.x+2, field.y+2)]

		updates = []
		for f in fields:
			status, updated = self.attack(f)
			if updated:
				updates.append({
					'field': f,
					'status': status
				})

		return updates

	def movePossible(self, shipId, direction):
		return self.__ships.movePossible(shipId, direction)

	def move(self, shipId, direction):
		"""
		Moves a ship.

		Args:
		    shipId: the id of the ship
		    direction: the direction of the ship

		Returns:
		    A dictionary of fields and statuses that have been updated and are unfogged. Keys are 'field' and 'status'.
		"""

		oldfields = splitShip(self.getShip(shipId).bow, self.getShip(shipId).rear)
		self.__ships.move(shipId, direction)
		newfields = splitShip(self.getShip(shipId).bow, self.getShip(shipId).rear)

		# merge old and new fields
		for f in oldfields:
			found = False
			for g in newfields:
				if f.equals(g):
					found = True
					break
			if not found:
				newfields.append(f)

		updates = []
		for f in newfields:
			logging.debug("Field {} is unfogged = {}".format(f.toString(), self.isUnfogged(f)))
			if self.isUnfogged(f):
				status, _ = self.__getFieldStatus(f)
				updates.append({
					'field': f,
					'status': status
				})
		return updates

	def getShips(self):
		"""
		Returns all ships.

		Returns:
			Returns all ships.
		"""

		return self.__ships.getShips()

	def getShip(self, shipId):
		"""
		Returns a specified ship.

		Args:
		    shipId: the id of the ship

		Returns:
			Returns a specified ship.
		"""

		return self.__ships.getShip(shipId)

	def getShipAtPosition(self, field):
		return self.__ships.getShipAtPosition(field)

	def placeShip(self, bow, rear):
		"""
		Places a ship on the playing field.

		Args:
			bow: bow of the ship
			rear: rear of the ship

		Return:
			Returns the id of the newly built ship or -1 if there was any game rule violation. In addition returns if
			the user has to place more ships.
		"""

		return self.__ships.add(bow, rear)

	def moreShipsLeftToPlace(self):
		return self.__ships.moreShipsLeftToPlace()

	def onAttack(self, params):
		# TODO: validate input
		wasSpecialAttack = True if params["was_special_attack"] == "true" else False
		field  = Field(int(params["coordinate_x"]), int(params["coordinate_y"]))
		fields = [field]

		# add other fields if special attack
		if wasSpecialAttack:
			fields += [Field(field.x, field.y + 1), Field(field.x, field.y + 2),
				  Field(field.x + 1, field.y), Field(field.x + 1, field.y + 1), Field(field.x + 1, field.y + 2),
				  Field(field.x+2, field.y), Field(field.x+2, field.y+1), Field(field.x+2, field.y+2)]

		for f in fields:
			status, ship = self.__getFieldStatus(f)
			logging.debug("Updating field '%s' with status '%s'" % (f.toString(), status))

			if status is FieldStatus.SHIP:
				ship.addDamage(f)
				logging.error("Added damage at '%s'" % f.toString())

			# unfog field
			if f not in self.__unfogged:
				self.__unfogged.append(f)

	def unfog(self, field):
		logging.debug("Unfog {}...".format(field.toString()))
		self.__unfogged.append(field)

	def isUnfogged(self, field):
		#return field in self.__unfogged
		for j in self.__unfogged:
			if field.equals(j):
				return True
		return False

	def getUnfogged(self):
		return self.__unfogged

	def isGameOver(self):
		total = 0
		for s in self.__ships.getShips():
			total += len(s.damages)
		return total == 30

	def __init__(self, fieldLength):
		self.__ships = ShipList(fieldLength)
		self.__fieldLength = fieldLength
		self.__unfogged = []

class EnemyPlayingField:

	def getField(self):
		return self.__fields

	def getUnfogged(self):
		return self.__unfogged

	def onAttack(self, params):
		for i in range(0, int(params["number_of_updated_fields"])):
			x = int(params["field_%s_x" % i])
			y = int(params["field_%s_y" % i])
			status = conditionCodes[params["field_%s_condition" % i]]
			logging.debug("Update at enemy field '%s' to '%s'" % (Field(x, y).toString(), status))
			self.__fields[x][y] = status

	def __init__(self, fieldLength):
		self.__fieldLength = fieldLength
		self.__unfogged = []
		self.__fields = [[0 for x in range(fieldLength)] for x in range(fieldLength)]

		# fill with fog everywhere
		for i in range(0, self.__fieldLength):
			for j in range(0, self.__fieldLength):
				self.__fields[i][j] = FieldStatus.FOG
