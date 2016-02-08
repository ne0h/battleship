import logging

from playingfield import *

class ClientStatus(Enum):

	NOTCONNECTED = "notconnected"
	NOGAMERUNNING = "nogamerunning"
	PREPARATIONS = "preparations"
	WAITINGFOROPPONENT = "waitingforopponent"
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
			True if the user has to place more ships and False of the user successfully placed all his ships.
		"""

		moreShips = self.__ownPlayingField.placeShip(bow, rear)
		if not moreShips:
			self.clientStatus = ClientStatus.WAITINGFOROPPONENT
			self.clientStatusUpdates()

			self.__serverHandler.initBoard(self.__ownPlayingField.getShips())

		return moreShips

	def registerClientStatusCallback(self, callback):
		self.__clientStatusCallbacks.append(callback)
		logging.debug("Client status callback added")
		return self.clientStatus

	def clientStatusUpdates(self):
		for callback in self.__clientStatusCallbacks:
			callback.onAction(self.clientStatus)

	def __updateClientStatus(self, status):
		self.clientStatus = status
		self.clientStatusUpdates()

	def registerLobbyUpdateGamesCallback(self, callback):
		self.__lobbyUpdateGamesCallbacks.append(callback)
		logging.debug("Lobby callback added")
		return self.__lobbyCurrentPlayers, self.__lobbyCurrentGames

	def removeLobbyUpdateGamesCallback(self, callback):
		for cb in self.__lobbyUpdateGamesCallbacks:
			if cb is callback:
				self.__lobbyUpdateGamesCallbacks.remove(callback)
		logging.debug("Lobby callback removed")

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
		self.clientStatusUpdates()

	def prepareGame(self):
		self.clientStatus = ClientStatus.PREPARATIONS
		logging.info("ClientStatus changed: Starting game preparations...")

	def leaveGame(self, callback):
		self.__leaveGameCallbacks.append(callback)
		self.__serverHandler.leaveGame()

	def leaveGameResponse(self):
		for cb in self.__leaveGameCallbacks:
			cb.onAction()
		self.__leaveGameCallbacks = []
		self.clientStatus = ClientStatus.NOGAMERUNNING

	def close(self):
		self.__serverHandler.close()
		self.__udpDiscoverer.close()

	def connect(self, hostname, port):
		result = self.__serverHandler.connect(hostname, port)
		if result:
			self.__updateClientStatus(ClientStatus.NOGAMERUNNING)

		return result

	def registerUdpDiscoveryCallback(self, callback):
		self.__udpDiscoveryCallbacks.append(callback)
		logging.debug("UDP discovery callback added")
		print(self.__udpServers)
		return self.__udpServers

	def removeUdpDiscoveryCallback(self, callback):
		for cb in self.__udpDiscoveryCallbacks:
			if cb is callback:
				self.__udpDiscoveryCallbacks.remove(callback)
		logging.debug("UDP Discovery callback removed")

	def udpDiscoveryUpdate(self, server):
		if server not in self.__udpServers:
			self.__udpServers.append(server)
		for cb in self.__udpDiscoveryCallbacks:
			cb.onAction(self.__udpServers)

	def __init__(self, length, hostname, port):
		from serverhandler import ServerHandler
		from udpdiscoverer import UDPDiscoverer

		self.__ownPlayingField = PlayingField(length)
		self.__enemeysPlayingField = PlayingField(length)
		self.clientStatus = ClientStatus.NOTCONNECTED

		# callback stuff
		self.__udpDiscoveryCallbacks = []
		self.__udpServers = []

		self.__clientStatusCallbacks = []
		self.__lobbyCurrentPlayers = []
		self.__lobbyCurrentGames = []
		self.__lobbyUpdateGamesCallbacks = []
		self.__joinGameCallbacks = []
		self.__createGameCallbacks = []
		self.__leaveGameCallbacks = []
		self.__connectCallbacks = []

		self.__serverHandler = ServerHandler(self)		
		if hostname and port:
			if self.connect(hostname, port):
				self.clientStatus = ClientStatus.NOGAMERUNNING

		self.__udpDiscoverer = UDPDiscoverer(self)
