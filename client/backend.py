from playingfield import PlayingField

class Backend:
	"""
	Dokustuff
	"""

	def getOwnPlayingField(self):
		"""
		Returns the complete player's playing field.

		Returns:
			A two-dimensional array of the own playing field
		"""

		return self.__ownPlayingField.getPlayingField()

	def getOwnField(self, field):
		"""
		Returns a single field from the players own playing field.

		Args:
			field -- the address of the field

		Returns:
			Field: the field
		"""
		return self.__ownPlayingField.getField(field)

	def getEnemeysPlayingField(self):
		"""
		Returns the complete playing field of the enemey.

		Returns:
			the complete playing field of the enemey.
		"""

		return self.__enemeysPlayingField.getPlayingField()

	def getEnemeysField(self, field):
		"""
		Returns a single field of the enemey's playing field.

		Args:
			field -- the address of the field

		Returns:
			the field
		"""

		return self.__enemeysPlayingField.getField(field)

	def __init__(self):
		self.__ownPlayingField = PlayingField(16)
		self.__enemeysPlayingField = PlayingField(16)
