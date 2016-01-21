import socket, time
from threading import Thread

from messageparser import *

class ServerHandler:

	def __sendMessage(self, type, params):
		msg = self.__messageParser.encode(type, params)

	def nicknameSet(self, nickname):
		self.__sendMessage("nickname_set", {"name": "nickname"})

	def __setUpdateMessage(self, params):
		

	def __receiveLoop(self):

		msg = "e8type:Update_Lobby;number_of_clients:5;number_of_games:2game_name_0:Game One;game_name_1:Game Two;" \
				+ "game_players_count_0:1;game_players_count_1:2;game_players_count_1:1;game_player_0_0:Hans;" \
				+ "game_player_1_0:Fritz;game_player_1_1:Ludwig;"

		messageType, params = self.__messageParser.decode(msg)
		print(messageType)

		while True:
			self.__backend.lobbyProgress(params)
			time.sleep(1)


	def __init__(self, backend, host, port):
		self.__backend = backend
		self.__messageParser = MessageParser()

		Thread(target=self.__receiveLoop).start()

		#self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#self.__sock.connect((host, port))
