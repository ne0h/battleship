import logging

from playingfield import *

class ClientStatus(Enum):
	"""
	Encapsulates the different client statuses.
	"""

	NOTCONNECTED = "notconnected"
	NOGAMERUNNING = "nogamerunning"
	PREPARATIONS = "preparations"
	WAITINGFOROPPONENT = "waitingforopponent"
	PREPARATIONSENDED = "preparationsended"
	OWNTURN = "ownturn"
	OPPONENTSTURN = "oppenentsturn"

class Callback:
	"""
	Callback (observer pattern).
	"""

	def onAction(self):
		"""
		Calls the callback.
		"""

		pass

class GameInformation:
	"""
	Represents a game.

	Args:
		name: the name of the game
		firstPlayer: the identifier of the first player
	"""

	def toString(self):
		"""
		Returns a string representativ of the game.
		"""

		result = ("%s: %s vs.") % (self.name, self.players[0])
		if len(self.players) > 1:
			result = ("%s %s") % (result, self.players[1])
		return result

	def __init__(self, name, firstPlayer):
		self.name = name
		self.players = [firstPlayer]

class PlayerInformation:
	"""
	Represents a player.

	Args:
		id: the identifier of the player
		nickname: the nickname of the player
	"""

	def toString(self):
		"""
		Returns a string representativ of the player.
		"""

		return "%s(%s)" % (self.id, self.nickname)

	def __init__(self, id, nickname):
		self.id = id
		self.nickname = nickname

class Backend:
	"""
	Game client backend that does all kind of controller stuff.

	Args:
		length: the length of the playing field
		hostname: the hostname of the server to connect to. If not set do not connect to any server so far
		port: the port of the server to connect to. If not set do not connect to any server so far
	"""

	def getOwnShips(self):
		"""
		Returns the player's ship.

		Returns:
			Returns the player's ship.
		"""

		return self.__ownPlayingField.getShips()

	def getOwnShip(self, shipId):
		"""
		Returns a specified ship from the own playing field.

		Args:
		    shipId: the id of the ship

		Returns:
			Returns a specified ship from the own playing field.
		"""

		return self.__ownPlayingField.getShip(shipId)

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
			bow: address of the bow
			rear: address of the rear

		Returns:
			Returns the id of the newley placed ship. In addition returns True if the user has to place more ships and
			False of the user successfully placed all his ships.
		"""

		shipId, moreShips = self.__ownPlayingField.placeShip(bow, rear)

		if shipId > -1 and shipId < 10:
			self.shipUpdate(shipId)
		if not moreShips:
			self.clientStatus = ClientStatus.WAITINGFOROPPONENT
			self.clientStatusUpdates()

			self.__serverHandler.initBoard(self.__ownPlayingField.getShips())

		return moreShips

	def registerClientStatusCallback(self, callback):
		"""
		Registers a new callback that will be called when the status of the client updates.

		Args:
			callback: the callback

		Returns:
			The current status.
		"""

		self.__clientStatusCallbacks.append(callback)
		logging.debug("Client status callback added")
		return self.clientStatus

	def clientStatusUpdates(self):
		"""
		Calls all client status update callbacks.
		"""

		for callback in self.__clientStatusCallbacks:
			callback.onAction(self.clientStatus)

	def __updateClientStatus(self, status):
		self.clientStatus = status
		self.clientStatusUpdates()

	def registerLobbyUpdateGamesCallback(self, callback):
		"""
		Registers a new callback that is called when the server sends a lobby update.

		Args:
			callback: the callback

		Returns:
			A tuple constisting of the players and the games.
		"""

		self.__lobbyUpdateGamesCallbacks.append(callback)
		logging.debug("Lobby callback added")
		return self.__lobbyCurrentPlayers, self.__lobbyCurrentGames

	def removeLobbyUpdateGamesCallback(self, callback):
		"""
		Removes a lobby update callback.

		Args:
			callback: the callback to remove
		"""

		for cb in self.__lobbyUpdateGamesCallbacks:
			if cb is callback:
				self.__lobbyUpdateGamesCallbacks.remove(callback)
		logging.debug("Lobby callback removed")

	def onLobbyUpdates(self, players, games):
		"""
		Calls all lobby update callbacks when there is any update.

		Args:
			players: complete list of the current players
			games: complete list of the current games
		"""

		self.__lobbyCurrentPlayers = players
		self.__lobbyCurrentGames = games

		for callback in self.__lobbyUpdateGamesCallbacks:
			callback.onAction(players, games)

	def joinGame(self, gameId, callback):
		"""
		Joins a new game and registers a callback that will be called when the server answered.

		Args:
			gameId: the id of the game to join
			callback: the callback
		"""

		self.__joinGameCallbacks.append(callback)
		self.__serverHandler.joinGame(gameId)

	def joinGameResponse(self, success):
		"""
		Calls all registered callbacks when the server answers a game join query.

		Args:
			success: True of the query has been successful or False if not
		"""

		# validate current client status
		if self.clientStatus is not ClientStatus.NOGAMERUNNING:
			success = False

		self.__updateClientStatus(ClientStatus.PREPARATIONS)

		for cb in self.__joinGameCallbacks:
			cb.onAction(success)
		self.__joinGameCallbacks = []
		self.clientStatusUpdates()

	def createGame(self, gameId, callback):
		"""
		Creates a new game on the current servers and registers a callback that will be called when the server answers.

		Args:
			gameId: the identiefier (a name) of the game
			callback: the callback
		"""

		self.__createGameCallbacks.append(callback)
		self.__serverHandler.createGame(gameId)

	def createGameResponse(self, success):
		"""
		Calls all registered callbacks when the servers answers a create game query.

		Args:
			success: True of the query has been successful or False if not
		"""

		# validate current client status
		if self.clientStatus is not ClientStatus.NOGAMERUNNING:
			success = False

		for cb in self.__createGameCallbacks:
			cb.onAction(success)
		self.__createGameCallbacks = []
		self.clientStatusUpdates()

	def prepareGame(self):
		"""
		Startes to prepare a new game.
		"""

		self.clientStatus = ClientStatus.PREPARATIONS
		logging.info("ClientStatus changed: Starting game preparations...")

	def leaveGame(self, callback):
		"""
		Leaves the current game and registers a callback to wait for an answer from the server.

		Args:
			callback: the callback
		"""

		self.__leaveGameCallbacks.append(callback)
		self.__serverHandler.leaveGame()

	def leaveGameResponse(self):
		"""
		Is called when the client received an answer to the leave game query.
		"""

		for cb in self.__leaveGameCallbacks:
			cb.onAction()
		self.__leaveGameCallbacks = []
		self.clientStatus = ClientStatus.NOGAMERUNNING

	def close(self):
		"""
		Closes the client.
		"""

		self.__serverHandler.close()
		self.__udpDiscoverer.close()

	def connect(self, nickname, hostname, port):
		"""
		Connects to a server.

		Args:
			hostname: the hostname or IP address of the server
			port: the port of the server
		"""
		# TODO: Validate input (if it is None)

		result = self.__serverHandler.connect(hostname, port)
		if result:
			self.__updateClientStatus(ClientStatus.NOGAMERUNNING)
			#self.__serverHandler.setNickname(nickname)

		return result

	def registerUdpDiscoveryCallback(self, callback):
		"""
		Registers a callback that informs about newly discovered servers.

		Args:
			callback: the callback
		"""

		self.__udpDiscoveryCallbacks.append(callback)
		logging.debug("UDP discovery callback added")

		return self.__udpServers

	def removeUdpDiscoveryCallback(self, callback):
		"""
		Removes an already registered UDP discovery callback.

		Args:
			callback: the callback to remove
		"""

		for cb in self.__udpDiscoveryCallbacks:
			if cb is callback:
				self.__udpDiscoveryCallbacks.remove(callback)
		logging.debug("UDP Discovery callback removed")

	def udpDiscoveryUpdate(self, server):
		"""
		Is called when there is a server update.

		Args:
			servers: a list of servers discovered by UDP broadcast
		"""

		if server not in self.__udpServers:
			self.__udpServers.append(server)
		for cb in self.__udpDiscoveryCallbacks:
			cb.onAction(self.__udpServers)

	def registerGamePlayCallback(self, callback):
		"""
		Registers a callback to stay informed about game play updates.

		Args:
			callback: the callback
		"""

		self.__gamePlayCallbacks.append(callback)

	def gamePlayUpdate(self, status):
		"""
		Is called when there is a game play update.

		Args:
			status: the received status update
		"""

		for cb in self.__gamePlayCallbacks:
			cb.onAction(status)

	def registerGamePreparationsEndedCallback(self, callback):
		"""
		Registers a callback that will be called when game preparations have finished.

		Args:
			callback: the callback
		"""

		self.__gamePreparationsEndedCallbacks.append(callback)

	def gamePreparationsEndedResponse(self):
		"""
		Is called when the client received an answer to the game preparations query.
		"""

		self.__updateClientStatus(ClientStatus.PREPARATIONSENDED)
		for cb in self.__gamePreparationsEndedCallbacks:
			cb.onAction()

	def registerShipUpdateCallback(self, callback):
		"""
		Registers a new callback to inform about ship updates.

		Args:
			callback: the callback
		"""

		self.__shipUpdateCallbacks.append(callback)

	def shipUpdate(self, shipId):
		"""
		Is called when there is any ship update.

		Args:
			shipId: the id of the updated ship
		"""

		for cb in self.__shipUpdateCallbacks:
			cb.onAction(shipId)

	def attack(self, target):
		"""
		Attacks the enemy at the given field.

		Args:
			target: the address of the field
		"""

		# TODO: validate client status
		self.__serverHandler.attack(target)

	def specialAttack(self, target):
		"""
		Special-attacks the given field.

		Args:
		    target: the address of the bottom-left field
		"""

		# TODO: validate client status
		self.__serverHandler.specialAttack(target)

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
		self.__gamePreparationsEndedCallbacks = []
		self.__gamePlayCallbacks = []
		self.__shipUpdateCallbacks = []

		self.__serverHandler = ServerHandler(self)		
		if hostname and port:
			if self.connect(hostname, port):
				self.clientStatus = ClientStatus.NOGAMERUNNING

		self.__udpDiscoverer = UDPDiscoverer(self)
