import logging

from playingfield import *
from lobby import Lobby

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
	YOUWIN = "youwin"
	YOULOSE = "youlose"

class Error(Enum):
	NOTYOURTURN = "It is not your turn."

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
		if 0 <= shipId < 10:
			self.shipUpdate(shipId)
		if not moreShips:
			self.clientStatus = ClientStatus.WAITINGFOROPPONENT
			self.clientStatusUpdates()

			self.__serverHandler.boardInit(self.__ownPlayingField.getShips())
			self.__updateClientStatus(ClientStatus.WAITINGFOROPPONENT)

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

	def __updateClientStatus(self, status):
		self.clientStatus = status
		for cb in self.__clientStatusCallbacks:
			cb.onAction()

	def registerLobbyUpdateGamesCallback(self, callback):
		"""
		Registers a new callback that is called when the server sends a lobby update.

		Args:
			callback: the callback

		Returns:
			A tuple consisting of the players and the games.
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

		self.lobby.onUpdate(games, players)

		# check if there was an update with the own game. E.g. opponent joined or changed nickname
		if self.lobby.hasGame():
			for game in games:
				if game.name == self.lobby.game.name:
					if self.lobby.hasOpponent():
						# TODO: Check if opponent changed nickname
						pass
					else:
						# check if anybody joined
						if len(game.players) > 1:
							self.lobby.setOpponent(game.players[1])
							self.__onOpponentJoinedGame()
					break

		for callback in self.__lobbyUpdateGamesCallbacks:
			callback.onAction()

	def joinGame(self, gameId, callback):
		"""
		Joins a new game and registers a callback that will be called when the server answered.

		Args:
			gameId: the id of the game to join
			callback: the callback
		"""

		self.__joinGameCallbacks.append(callback)
		self.lobby.tryToGame(gameId)
		self.__serverHandler.joinGame(gameId)

	def onJoinGame(self, success):
		"""
		Calls all registered callbacks when the server answers a game join query.

		Args:
			success: True of the query has been successful or False if not
		"""

		if success:
			self.lobby.joinSuccessful()
			logging.info("Successfully join game '%s' against '%s'" % (self.lobby.game.name,
																	   self.lobby.getNickname(self.lobby.opponent)))

		# TODO: validate current client status
		self.__updateClientStatus(ClientStatus.PREPARATIONS)

		for cb in self.__joinGameCallbacks:
			cb.onAction(success)
		self.__joinGameCallbacks = []

	def createGame(self, gameId, callback):
		"""
		Creates a new game on the current servers and registers a callback that will be called when the server answers.

		Args:
			gameId: the identiefier (a name) of the game
			callback: the callback
		"""

		self.__createGameCallbacks.append(callback)
		self.lobby.tryToGame(gameId)
		self.__serverHandler.createGame(gameId)

	def onCreateGame(self, success):
		"""
		Calls all registered callbacks when the servers answers a create game query.

		Args:
			success: True of the query has been successful or False if not
		"""

		#TODO: validate current client status
		if success:
			self.lobby.createSuccessful()
			self.__updateClientStatus(ClientStatus.PREPARATIONS)

		for cb in self.__createGameCallbacks:
			cb.onAction(success)
		self.__createGameCallbacks = []

	def leaveGame(self, callback):
		"""
		Leaves the current game and registers a callback to wait for an answer from the server.

		Args:
			callback: the callback
		"""

		self.__leaveGameCallbacks.append(callback)
		self.__serverHandler.leaveGame()

	def onLeaveGame(self):
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

		self.nickname = nickname
		result = self.__serverHandler.connect(hostname, port)
		if result:
			self.__updateClientStatus(ClientStatus.NOGAMERUNNING)
			self.__serverHandler.setNickname(nickname)

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

	def onGamePlayUpdate(self, status):
		"""
		Is called when there is a game play update.

		Args:
			status: the received status update
		"""

		if status is 11:
			self.__updateClientStatus(ClientStatus.OWNTURN)
		elif status is 21 or status is 22 or status is 24:
			self.__updateClientStatus(ClientStatus.OPPONENTSTURN)
		elif status is 31:
			self.__onError("Move not allowed")
		elif status is 32:
			self.__onError("Special Attack not allowed")
		elif status is 39:
			self.__onError("Attack not allowed")

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
		# TODO: validate field

		if self.clientStatus is not ClientStatus.OWNTURN:
			self.__onError("It is not your turn.")
			return

		self.__serverHandler.attack(target)

	def specialAttack(self, target):
		"""
		Special-attacks the given field.

		Args:
		    target: the address of the bottom-left field
		"""
		# TODO: validate field

		if self.clientStatus is not ClientStatus.OWNTURN:
			self.__onError("It is not your turn.")
			return

		self.__serverHandler.specialAttack(target)

	def move(self, shipId, direction):
		# TODO: validate direction
		if self.clientStatus is not ClientStatus.OWNTURN:
			self.__onError("It is not your turn.")
			return

		self.__serverHandler.move(shipId, direction)

	def errorResponse(self, status):
		pass

	def sendChatMessage(self, msg):
		self.__serverHandler.sendChatMessage(msg)

	def registerChatCallback(self, callback):
		self.__chatCallbacks.append(callback)

	def onIncomingChatMessage(self, authorId, timestamp, message):
		for cb in self.__chatCallbacks:
			cb.onAction(authorId, timestamp, message)

	def registerJoinGameCallback(self, callback):
		self.__joinGameCallbacks.append(callback)

	def registerErrorCallback(self, callback):
		self.__errorCallbacks.append(callback)

	def __onError(self, error):
		for cb in self.__errorCallbacks:
			cb.onAction(error)

	def registerOpponentJoinedGameCallback(self, callback):
		self.__opponentJoinedGameCallbacks.append(callback)

	def __onOpponentJoinedGame(self):
		for cb in self.__opponentJoinedGameCallbacks:
			cb.onAction()

	def getShipAtPosition(self, field):
		return self.__ownPlayingField.getShipAtPosition(field)

	def __init__(self, length, hostname, port, nickname):
		from serverhandler import ServerHandler
		from udpdiscoverer import UDPDiscoverer

		self.lobby = Lobby(nickname)
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
		self.__chatCallbacks = []
		self.__joinGameCallbacks = []
		self.__errorCallbacks = []
		self.__opponentJoinedGameCallbacks = []

		self.__serverHandler = ServerHandler(self)		
		if hostname and port and nickname:
			if self.connect(nickname, hostname, port):
				self.clientStatus = ClientStatus.NOGAMERUNNING

		self.__udpDiscoverer = UDPDiscoverer(self)
