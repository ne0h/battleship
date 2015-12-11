from playingfield import PlayingField

class Backend:

	def getOwnPlayingField(self):
		return self.__ownPlayingField.getPlayingField()

	def getOwnField(self, field):
		return self.__ownPlayingField.getField(field)

	def __init__(self):
		self.__ownPlayingField = PlayingField(16)