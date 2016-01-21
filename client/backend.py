from playingfield import *

class ClientStatus(Enum):

	NOGAMERUNNING = "nogamerunning"
	PREPARATIONS = "preparations"
	OWNTURN = "ownturn"
	OPPONENTSTURN = "oppenentsturn"

class Observer:

	def onAction(self):
		pass

class GameInformation:

	def toString(self):
		result = ("%s: %s vs.") % (self.name, self.players[0])
		if len(self.players) > 1:
			result = ("%s %s") % (result, self.players[1])
		return result

	def __init__(self, name, firstPlayer):
		self.name = name
		self.players = [firstPlayer]

class PlayerInformation:

	def toString(self):
		return "%s(%s)" % (self.id, self.nickname)

	def __init__(self, id, nickname):
		self.id = id
		self.nickname = nickname

class Lobby:

	def __init__(self):
		pass

class Backend:
	"""
	Game client backend that does all kind of controller stuff.
	"""

	def getOwnShips(self):
		"""
		Returns the player's ship.

		Returns:
			Returns the player's ship.
		"""

		return self.__ownPlayingField.getShips()

	def getEnemeysShips(self):
		"""
		Returns the enemey's ships.

		Returns:
			Returns the enemey's ships.
		"""

		return self.__enemeysPlayingField.getShips()

	def placeShip(self, bow, rear):
		"""
		Places a new Ship on the own playing field.

		Args:
			bow -- address of the bow
			rear -- address of the rear

		Returns:
			The ship or None if there have been any errors.
		"""
		
		return self.__ownPlayingField.placeShip(bow, rear)

	def getClientStatus(self):
		return self.__clientStatus

	def registerLobbyObserver(self, observer):
		self.__lobbyObservers.append(observer)
		print("Observer added")

	def lobbyProgress(self, players, games):
		for observer in self.__lobbyObservers:
			observer.onAction()

	def __init__(self, length):
		from serverhandler import ServerHandler

		self.__ownPlayingField = PlayingField(length)
		self.__enemeysPlayingField = PlayingField(length)
		self.__clientStatus = ClientStatus.NOGAMERUNNING

		self.__lobbyObservers = []

		self.__serverHandler = ServerHandler(self, "localhost", 11000)
