import logging

from playingfield import *

class ClientStatus(Enum):

	NOGAMERUNNING = "nogamerunning"
	PREPARATIONS = "preparations"
	OWNTURN = "ownturn"
	OPPONENTSTURN = "oppenentsturn"

class Callback:

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

	def registerLobbyUpdateGamesCallback(self, callback):
		self.__lobbyUpdateGamesCallbacks.append(callback)
		logging.info("Lobby callback added")
		return self.__lobbyCurrentPlayers, self.__lobbyCurrentGames

	def removeLobbyUpdateGamesCallback(self, callback):
		for cb in self.__lobbyUpdateGamesCallbacks:
			if cb is callback:
				self.__lobbyUpdateGamesCallbacks.remove(callback)
		logging.info("Lobby observer removed")

	def lobbyUpdateGamesProgress(self, players, games):
		self.__lobbyCurrentPlayers = players
		self.__lobbyCurrentGames = games

		for callback in self.__lobbyUpdateGamesCallbacks:
			callback.onAction(players, games)

	def joinGame(self, gameId, callback):
		self.__joinGameCallbacks.append(callback)
		self.__serverHandler.joinGame(gameId)

	def joinGameResponse(self, success):

		# validate current client status
		if self.clientStatus is not ClientStatus.NOGAMERUNNING:
			success = False

		for cb in self.__joinGameCallbacks:
			cb.onAction(success)
		self.__joinGameCallbacks = []

	def createGame(self, gameId, callback):
		self.__createGameCallbacks.append(callback)
		self.__serverHandler.createGame(gameId)

	def createGameResponse(self, success):

		# validate current client status
		if self.clientStatus is not ClientStatus.NOGAMERUNNING:
			success = False

		for cb in self.__createGameCallbacks:
			cb.onAction(success)
		self.__createGameCallbacks = []

	def prepareGame(self):
		self.clientStatus = ClientStatus.PREPARATIONS
		logging.info("ClientStatus changed: Starting game preparations...")

	def close(self):
		self.__serverHandler.close()

	def __init__(self, length):
		from serverhandler import ServerHandler

		self.__ownPlayingField = PlayingField(length)
		self.__enemeysPlayingField = PlayingField(length)
		self.clientStatus = ClientStatus.NOGAMERUNNING

		# callback stuff
		self.__lobbyCurrentPlayers = []
		self.__lobbyCurrentGames = []
		self.__lobbyUpdateGamesCallbacks = []
		self.__joinGameCallbacks = []
		self.__createGameCallbacks = []

		self.__serverHandler = ServerHandler(self, "localhost", 44444)
