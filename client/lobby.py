import logging

class Lobby:

	def onUpdate(self, games, players):
		self.games = games
		self.players = players

		self.__playerNicks = {}
		for player in self.players:
			self.__playerNicks[player.id] = player.nickname

	def getOwnNickname(self):
		return self.nickname if self.nickname is not None and self.nickname is not "" else "Unnamed Player"

	def getNickname(self, playerId):
		return "BOFH" if self.__playerNicks[playerId] is None or self.__playerNicks[playerId] is "" else self.__playerNicks[playerId]

	def hasOpponent(self):
		return False if self.opponent is None else True

	def hasGame(self):
		return False if self.game is None else True

	def setOpponent(self, opponentId):
		self.opponent = opponentId

	def tryToGame(self, gameId):
		self.__tryToGameId = gameId

	def joinSuccessful(self):
		self.playerJoinedGame = True
		for game in self.games:
			if game.name == self.__tryToGameId:
				self.game = game
				self.opponent = game.players[0]
				break

	def createSuccessful(self):
		self.playerCreatedGame = True
		for game in self.games:
			if game.name == self.__tryToGameId:
				self.game = game
				break

	def existsGame(self, gameId):
		for game in self.games:
			if gameId == game.name:
				return True
		return False

	def reset(self):
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
