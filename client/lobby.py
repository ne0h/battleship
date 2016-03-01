import logging

class Lobby:
	"""
	Holds all game info and player's info stuff.
	"""

	def onUpdate(self, games, players):
		"""
		Updates everything. Is called automatically when the server sends a new Update_Lobby report.

		Args:
		    games: the games currently active
		    players: the players currently active
		"""

		self.games = games
		self.players = players

		self.__playerNicks = {}
		for player in self.players:
			self.__playerNicks[player.id] = player.nickname

	def getOwnNickname(self):
		"""
		Returns the nickname of the player or BOFH if no nickname is set.

		Returns: the nickname of the player or BOFH if no nickname is set.
		"""

		return self.nickname if self.nickname is not None and self.nickname is not "" else "Unnamed Player"

	def getNickname(self, playerId):
		"""
		Returns the nickname of any player or BOFH if no nickname is set.

		Returns: the nickname of any player or BOFH if no nickname is set.
		"""

		return "BOFH" if self.__playerNicks[playerId] is None or self.__playerNicks[playerId] is "" else self.__playerNicks[playerId]

	def hasOpponent(self):
		"""
		Returns True if the player has currently an opponent or False if not.

		Returns: True if the player has currently an opponent or False if not.

		"""
		return False if self.opponent is None else True

	def hasGame(self):
		"""
		Returns True if there is currently a game active or False if not.
		Returns: True if there is currently a game active or False if not.

		"""

		return False if self.game is None else True

	def setOpponent(self, opponentId):
		"""
		Sets the opponent.

		Args:
		    opponentId: the id of the opponent.
		"""

		self.opponent = opponentId

	def tryToGame(self, gameId):
		"""
		Sets tryToGame.

		Args:
		    gameId: the id of the game
		"""

		self.__tryToGameId = gameId

	def joinSuccessful(self):
		"""
		Is called when the game join has been successful.
		"""

		self.playerJoinedGame = True
		for game in self.games:
			if game.name == self.__tryToGameId:
				self.game = game
				self.opponent = game.players[0]
				break

	def createSuccessful(self):
		"""
		Is called when the game creation has been successful.
		"""

		self.playerCreatedGame = True
		for game in self.games:
			if game.name == self.__tryToGameId:
				self.game = game
				break

	def existsGame(self, gameId):
		"""
		Validates if a game exists.

		Args:
		    gameId: the id of the game

		Returns: True if the game exists or False if not.
		"""

		for game in self.games:
			if gameId == game.name:
				return True
		return False

	def reset(self):
		"""
		Resets the lobby.
		"""

		self.__setup()

	def __setup(self):
		self.game = None
		self.opponent = None

		self.playerCreatedGame = False
		self.playerJoinedGame = False

	def __init__(self, nickname=None):
		self.nickname = nickname
		self.games = []
		self.players = []
		self.__playerNicks = {}

		self.__setup()
