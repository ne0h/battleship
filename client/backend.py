from playingfield import *

class Backend:
	"""
	Game client backend that does all kind of controller stuff.
	"""

	def getOwnPlayingField(self):
		"""
		Returns the complete player's playing field.

		Returns:
			A two-dimensional array of the own playing field.
		"""

		return self.__ownPlayingField.getPlayingField()

	def getOwnField(self, fieldAddress):
		"""
		Returns a single field from the players own playing field.

		Args:
			fieldAddress -- the address of the field

		Returns:
			The field.
		"""
		return self.__ownPlayingField.getField(fieldAddress)

	def getEnemeysPlayingField(self):
		"""
		Returns the complete playing field of the enemey.

		Returns:
			The complete playing field of the enemey.
		"""

		return self.__enemeysPlayingField.getPlayingField()

	def getEnemeysField(self, fieldAddress):
		"""
		Returns a single field of the enemey's playing field.

		Args:
			fieldAddress -- the address of the field

		Returns:
			The field.
		"""

		return self.__enemeysPlayingField.getField(fieldAddress)

	def placeShip(self, bow, rear):
		"""
		Validates if bow and rear make a valid ship and checks for collisions with other ships.

		Args:
			bow -- address of the bow
			rear -- address of the rear

		Returns:
			The ship or None if there have been any errors.
		"""
		import math

		# check if bow and rear form a valid ship
		if not (bow.x is rear.x or bow.y is bow.y):
			return None
		print("a")
		# check if the length of the potential ship is valid
		if bow.x is rear.x:
			length = math.fabs(bow.y - rear.y) + 1
		else:
			length = math.fabs(bow.x - rear.x) + 1
		print(length)
		
		if length < 2 or length > 5:
			return None
		print("b")
		# check for collisions with previously placed ships
		if bow.x is rear.x:
			if bow.y > rear.y:
				for i in range(bow.y, rear.y):
					if self.__ownPlayingField.getField(FieldAddress(bow.x, i)) is not FieldStatus.WATER:
						return None
			else:
				for i in range(rear.y, bow.y):
					if self.__ownPlayingField.getField(FieldAddess(bow.x, i)) is not FieldStatus.WATER:
						return None
		else:
			if bow.x > rear.x:
				for i in range(bow.x, rear.x):
					if self.__ownPlayingField.getField(FieldAddress(bow.y, i)) is not FieldStatus.WATER:
						return None
			else:
				for i in range(rear.x, bow.x):
					if self.__ownPlayingField.getField(FieldAddress(bow.y, i)) is not FieldStatus.WATER:
						return None
		print("c")

		# check playing field borders

		print("d")

		# all checks done - build ship
		if length is 5:
			ship = Battleship(bow, rear)
		elif length is 4:
			ship = Destroyer(bow, rear)
		elif length is 3:
			ship = Cruiser(bow, rear)
		else:
			ship = Submarine(bow, rear)

		print("yep")

		self.__ownPlayingField.placeShip(ship)
		return ship

	def __init__(self):
		self.__ownPlayingField = PlayingField(16)
		self.__enemeysPlayingField = PlayingField(16)
