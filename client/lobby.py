class Lobby:

	def onUpdate(self, games, players):
		self.games = games
		self.players = players

		self.__playerNicks = {}
		for player in players:
			self.__playerNicks[player.id] = player.nickname

	def getOwnNickname(self):
		return self.nickname if self.nickname else "Unnamed Player"

	def getNickname(self, playerId):
		return "Unnamed Player" if self.__playerNicks[playerId] is "" else self.__playerNicks[playerId]

	def hasOpponent(self):
		return self.opponent

	def hasGame(self):
		return False if self.game is None else True

	def setOpponent(self, opponentId):
		from backend import PlayerInformation
		self.opponent = PlayerInformation(opponentId, self.getNickname(opponentId))

	def tryToJoinGame(self, gameId):
		self.__tryToJoinGameId = gameId

	def joinSuccessful(self):
		for game in self.games:
			if game.name == self.__tryToJoinGameId:
				self.game = game
				self.opponent = game.players[0]
				break

	def __init__(self, nickname=None):
		self.nickname = nickname
		self.games = []
		self.players = []
		self.__playerNicks = {}

		self.game = None
		self.opponent = None
