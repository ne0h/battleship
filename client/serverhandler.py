import socket, time
from threading import Thread

from messageparser import *

class ServerHandler:

	def __sendMessage(self, type, params):
		msg = self.__messageParser.encode(type, params)

	def nicknameSet(self, nickname):
		self.__sendMessage("nickname_set", {"name": "nickname"})

	"""
	Sent whenever the server noticed a change in the lobby.

		number_of_clients:[number n];
			The total number of clients currently connected to the server.

		number_of_games:[number m];
			The total number of open games on this server.

		game_name_0:[name];...;game_name_m-1:[name];
			The name of this game.

		game_players_count_0:[1|2];...;game_players_m-1:[1|2];
			The number of players currently in this game (1 or 2).

		game_player_0_i:[identifier];...;game_player_m-1_i:[identifier]
			For each game k from(0..m-1) games this maps game_players_count_k players to the game by use of their
			identifier. The first value in the name of the parameter is the related game.

		player_name_0:[name];...;player_name_n-1:[name];
			MAY be an empty string, if no nickname was set prior to this report.

		player_identifier_0:[identifier];...;player_identifier_n-1:[identifier];
			Per-server-unique identifier (implementations may map any string as identifier)
	"""
	def __setUpdateLobby(self, params):
		from backend import GameInformation, PlayerInformation

		# TODO lots of consistency tests...
		# TODO remove already read values from map that the method runs in O(n)
		# TODO Validate message length

		games   = []
		players = []

		# extract players count and games count
		playersTotal = int(params["number_of_clients"])
		gamesTotal   = int(params["number_of_games"])

		"""
		We have to make sure that all players in the game actually exist. Therefore players are extracted before the
		games.
		"""

		# extract players
		playersCounter = 0
		for param, value in params.items():
			if param.startswith("player_identifier_"):

				# make sure that there are not more players than passed by players counter
				# TODO error here
				if playersCounter >= playersTotal:
					continue
				playersCounter = playersCounter + 1

				# extract counter and nickname if there is one...
				# TODO: nickname-value may not exist... -> error
				nickname = params["player_name_" + param[18:]]

				players.append(PlayerInformation(value, nickname))

		# extract games
		gamesCounter = 0
		for param, value in params.items():
			if param.startswith("game_name_"):

				# make sure that there are not more games than passed by games counter
				# TODO error
				if gamesCounter >= gamesTotal:
					continue
				gamesCounter = gamesCounter + 1

				counter = int(param[10:])
				numberOfPlayers = int(params["game_players_count_" + str(counter)])
				if numberOfPlayers > 2:
					# error
					pass

				# find the players of this game
				# validate that the players exist
				player0 = params["game_player_" + str(counter) + "_0"]
				game = GameInformation(value, player0)
				if numberOfPlayers > 1:
					player1 = params["game_player_" + str(counter) + "_1"]
					game.players.append(player1)

				games.append(game)

		self.__backend.lobbyProgress(players, games)

	def __receiveLoop(self):

		msg = "00type:Update_Lobby;number_of_clients:5;number_of_games:2;" \
				+ "game_name_0:Game One;game_name_1:Game Two;" \
				+ "game_players_count_0:1;game_players_count_1:2;"\
				+ "game_player_0_0:aaaa;game_player_1_0:bbbb;game_player_1_1:cccc;" \
				+ "player_name_0:Hans;player_identifier_0:cccc;" \
				+ "player_name_1:;player_identifier_1:aaaa;" \
				+ "player_name_2:Fritz Dieter;player_identifier_2:dddd;" \
				+ "player_name_3:Ludwig;player_identifier_3:bbbb;" \
				+ "player_name_4:Erhard;player_identifier_4:eeee;"

		messageType, params = self.__messageParser.decode(msg)

		while True:

			if messageType == "Update_Lobby":
				self.__setUpdateLobby(params)

			time.sleep(1)


	def __init__(self, backend, host, port):
		self.__backend = backend
		self.__messageParser = MessageParser()

		Thread(target=self.__receiveLoop).start()

		#self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#self.__sock.connect((host, port))
