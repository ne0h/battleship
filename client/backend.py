from playingfield import PlayingField

class Backend:

	def getOwnPlayingField(self):
		return self.__ownPlayingField.getPlayingField()

	def getOwnField(self, field):
		return self.__ownPlayingField.getField(field)

	def getEnemeysPlayingField(self):
		return self.__enemeysPlayingField.getPlayingField()

	def getEnemeysField(self, field):
		return self.__enemeysPlayingField.getField(field)

	def __init__(self):
		self.__ownPlayingField = PlayingField(16)
		self.__enemeysPlayingField = PlayingField(16)
