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
		
		return self.__ownPlayingField.placeShip(bow, rear)

	def __init__(self):
		self.__ownPlayingField = PlayingField(16)
		self.__enemeysPlayingField = PlayingField(16)
