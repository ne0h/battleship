import logging, socket, sys
from threading import Thread

from messageparser import *
from playingfield import Orientation

reportCodes = {
	11: "Begin_Turn",
	13: "Update_Own_Field",
	14: "Update_Enemy_Field",
	15: "Chat_Broadcast",
	16: "Update_Lobby",
	17: "Game_Ended",
	18: "Begin_Ship_Placing",
	19: "Game_Aborted",
	21: "Successful_Move",
	22: "Successful_Attack",
	23: "Surrender_Accepted",
	24: "Successful_Special_Attack",
	27: "Successful_Game_Join",
	28: "Successful_Game_Create",
	29: "Successful_Ship_Placement",
	31: "Illegal_Move",
	32: "Illegal_Special_Attack",
	33: "Illegal_Field",
	34: "Illegal_Ship_Index",
	37: "Illegal_Game_Definition",
	38: "Illegal_Ship_Placement",
	39: "Illegal_Attack",
	40: "Message_Not_Recognized",
	41: "Not_Your_Turn",
	43: "Not_In_Any_Game",
	47: "Game_Join_Denied",
	48: "Game_Preparation_Ended"}

orientationCodes = {
	Orientation.NORTH: "N",
	Orientation.WEST:  "W",
	Orientation.SOUTH: "S",
	Orientation.EAST:  "E"}

class ServerHandler:

	def setNickname(self, nickname):
		"""
		Sets the nickname.

		Args:
			nickname: the new nickname
		"""

		self.__sendMessage("nickname_set", {"name": nickname})

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
	def __onUpdateLobby(self, params):
		from backend import GameInformation, PlayerInformation
		# TODO lots of consistency tests...
		# TODO remove already read values from map that the method runs in O(n)
		# TODO Validate message length (should be already done in the receiveLoop)
		# TODO Validate if empty nicknames work correctly (that there is not 'None' in wireshark)

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
				gamesCounter += 1

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

		self.__backend.onLobbyUpdates(players, games)

	def joinGame(self, gameId):
		"""
		Sends a joinGame request to the server.

		Args:
			gameId: the identifier of the game
		"""

		self.__sendMessage("game_join", {"name": gameId})

	def createGame(self, gameId):
		"""
		Sends a new createGame request to the server.

		Args:
			gameId: the identifier of the new game
		"""

		self.__sendMessage("game_create", {"name": gameId})

	def leaveGame(self):
		"""
		Sends a leaveGame request to the server.
		"""

		self.__sendMessage("game_abort", {})

	def initBoard(self, ships):
		"""
		Sends the playing field to the server.

		Args:
			ships: a list of all ships
		"""

		params = {}
		
		i = 0
		for ship in ships:
			params["ship_" + str(i) + "_x"] = str(ship.bow.x)
			params["ship_" + str(i) + "_y"] = str(ship.bow.y)
			params["ship_" + str(i) + "_direction"] = orientationCodes[ship.orientation]
			i += 1

		self.__sendMessage("board_init", params)

	def attack(self, target):
		"""
		Sends an attack message.

		Args:
			target: the address of the field that is to be attacked
		"""

		self.__sendMessage("attack", {"coordinate_x": target.x, "coordinate_y": target.y})

	def specialAttack(self, target):
		"""
		Special-attacks the given field.

		Args:
		    target: the address of the bottom-left field
		"""

		self.__sendMessage("special_attack", {"coordinate_x": target.x, "coordinate_y": target.y})

	def sendChatMessage(self, msg):
		self.__sendMessage("chat_send", {"text": msg})

	def __receiveLoop(self):
		while not self.__stopReceiveLoop:

			# read the first to byte to receive the byte size of the message
			size = self.__sock.recv(2)
			if not size:
				continue
			else:
				msg = self.__sock.recv(size[0] * 256 + size[1]).decode()
				messageType, params = self.__messageParser.decode(msg)

				# validate that the status code exists
				status = int(params["status"])
				if status in reportCodes:
					logging.debug("%s received: %s" % (messageType, reportCodes[status]))

					if status is 15:
						self.__backend.onIncomingChatMessage(params["author_id"], params["timestamp"],
															params["message_content"])

					elif status is 16:
						self.__onUpdateLobby(params)

					# game creation stuff
					elif status is 19:														# Game_Aborted
						self.__backend.leaveGameResponse()
					elif status is 27 or status is 47:										# Successful_Game_Join
						self.__backend.onJoinGame(status is 27)						# or Game_Join_Denied
					elif status is 28:														# Successful_Game_Create
						self.__backend.createGameResponse(True)
					elif status is 29 or status is 38:										# Successful_Ship_Placement
						self.__backend.placeShipsResponse(status is 29)						# or Illegal_Ship_Placement
					elif status is 37:														# Illegal_Game_Definition
						self.__backend.createGameResponse(False)
					elif status is 48:														# Game_Preparation_Ended
						self.__backend.gamePreparationsEndedResponse()

					# game play stuff
					#  - Successful_Move
					#  - Successful_Attack
					#  - Surrender_Accepted
					#  - Successful_Special_Attack
					#  - Illegal_Move
					#  - Illegal_Special_Attack
					#  - Illegal_Field
					#  - Illegal_Ship_Index
					#  - Illegal_Attack
					#  - Not_Your_Turn
					elif status is 21 or status is 22 or status is 23 or status is 24 or status is 31 or status is 32 \
							or status is 33 or status is 34 or status is 39 or status is 41:
						self.__backend.gamePlayUpdate(status)

					# bad error stuff
					#  - Message_Not_Recognized
					#  - Not_In_Any_Game (what? wtf? :D)
					elif status is 40 or status is 43:
						self.__backend.errorResponse(status)

				else:
					logging.debug("%s received with unknown status code." % (messageType))

	def __sendMessage(self, type, params):
		if not self.__connected:
			logging.error("Not connected.")
			return

		msg = self.__messageParser.encode(type, params)
		logging.debug("Sending message: %s"  % (msg))
		self.__sock.send(msg)

	def close(self):
		"""
		Closes the connection to the server.
		"""

		self.__stopReceiveLoop = True

	def connect(self, hostname, port):
		"""
		Connects to a server.

		Args:
			hostname - the hostname or IP address of the server
			port - the port of the server
		"""

		try:
			self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.__sock.connect((hostname, port))
			self.__connected = True

			Thread(target=self.__receiveLoop).start()
			
			return True

		except socket.error:
			logging.error("Failed to connect to server.")
			return False

	def __init__(self, backend):
		self.__backend = backend
		self.__messageParser = MessageParser()

		self.__stopReceiveLoop = False
		self.__connected = False
