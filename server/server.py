import sys
import logging
import socketserver
import struct
import threading
import hashlib
from messageparser import MessageParser
import messages
from lobby import *
from helpers import *


class TCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class RequestHandler(socketserver.BaseRequestHandler):

    def setup(self):
        self.__client = ClientHandler(self.request)

    def handle(self):
        self.__client.handle()

    def finish(self):
        self.__client.finish()


class ClientHandler:

    def __init__(self, sock):
        self.__socket = sock
        self.__message_parser = MessageParser()
        self.__lobby_model = LobbyModel()
        # name of the game
        self.__game = None
        # player number (1 or 2)
        self.__player = None
        # player id lol
        self.__id = self.__get_own_player_id()
        # add client as player
        self.__lobby_model.add_player(self.__id)

        # register on_update callback
        self.__lobby_model.register_callback(LobbyEvent.on_update, self.on_update_lobby)

    def handle(self):
        logging.info("Client {} connected.".format(self.__socket.getpeername()))
        while True:
            # receive 2 bytes size header
            size = self.__socket.recv(2)
            if not size:
                logging.info("Client {} disconnected.".format(self.__socket.getpeername()))
                break
            size = struct.unpack('>H', size)[0]
            logging.debug("Size: " + str(size))

            # receive message body
            msg = self.__socket.recv(size)
            if not msg:
                logging.info("Client {} disconnected.".format(self.__socket.getpeername()))
                break
            logging.debug(b"Raw in: " + msg)

            # explode received data into message type and parameters
            msgtype, msgparams = self.__message_parser.decode(msg.decode())
            logging.debug("Msg type: " + msgtype)
            logging.debug("Msg parameters: " + repr(msgparams))

            # dispatch message type
            if msgtype == messages.CREATE_GAME:
                report = self.__create_game(msgparams)
            elif msgtype == messages.JOIN_GAME:
                report = self.__join_game(msgparams)
            elif msgtype == messages.SET_NICK:
                report = self.__set_nickname(msgparams)
            elif msgtype == messages.LEAVE_GAME:
                report = self.__leave_game()
            else:
                report = self.__unknown_msg()

            # send answer to client
            self.__send(report)

    def on_update_lobby(self):
        logging.debug("on_update_lobby()")

        # Get required data for update lobby msg
        number_of_clients = self.__lobby_model.get_number_of_players()
        number_of_games = self.__lobby_model.get_number_of_games()
        games_info = self.__lobby_model.get_games_info()
        players_info = self.__lobby_model.get_players_info()

        # Update_Lobby
        data = {
            'status': 16,
            'number_of_clients': number_of_clients,
            'number_of_games': number_of_games[0]
        }

        i = 0
        weirdkey = 'game_name_{}'
        moreweirdkeys = 'game_players_count_{}'
        whatevenisthis = 'game_player_{}_{}'
        waitwhat = 'player_name_{}'
        yetanotherkey = 'player_identifier_{}'

        for game in games_info:
            # game stuff
            data[weirdkey.format(i)] = game['game_name']
            data[moreweirdkeys.format(i)] = game['number_of_players']
            # player 1 stuff
            data[whatevenisthis.format(i, 0)] = game['ids'][0]
            # player 2 stuff
            if game['number_of_players'] == 2:
                data[whatevenisthis.format(i, 1)] = game['ids'][1]
            i += 1

        i = 0
        for player in players_info:
            # player stuff
            data[yetanotherkey.format(i)] = player['id']
            data[waitwhat.format(i)] = player['nickname']
            i += 1

        msg = self.__message_parser.encode('report', data)
        self.__send(msg)

    def get_socket(self):
        return self.__socket

    def finish(self):
        self.__lobby_model.remove_callback(LobbyEvent.on_update, self.on_update_lobby)

    def __create_game(self, params):
        # make sure parameter list is complete
        report = self.__expect_parameter(['name'], params)
        if report:
            return report

        # check if client is already in a game
        if self.__game:
            logging.debug("Client already in some game.")
            return self.__message_parser.encode('report', {'status': '31'})

        # check game name length
        if 1 > len(params['name']) or len(params['name']) > 64:
            logging.debug("Game name too long.")
            return self.__message_parser.encode('report', {'status': '37'})

        # create the game
        game = self.__lobby_model.add_lobby(params['name'], self.__id)
        if game:
            self.__game = params['name']
            self.__player = 1
            return self.__message_parser.encode('report', {'status': '28'})
        else:
            return self.__message_parser.encode('report', {'status': '37'})

    def __join_game(self, params):
        # make sure parameter list is complete
        report = self.__expect_parameter(['name'], params)
        if report:
            return report

        # check if client is already in a game
        if self.__game:
            logging.debug("Client already in some game.")
            return self.__message_parser.encode('report', {'status': '31'})

        # join the game
        game, e = self.__lobby_model.join_lobby(params['name'], self.__id)

        # handle game join errors
        if e:
            if e == LobbyError.game_is_full:
                return self.__message_parser.encode('report', {'status': '47'})
            elif e == LobbyError.game_does_not_exist:
                return self.__message_parser.encode('report', {'status': '37'})

        self.__game = params['name']
        self.__player = 2
        return self.__message_parser.encode('report', {'status': '27'})

    def __set_nickname(self, params):
        report = self.__expect_parameter(['name'], params)
        if report:
            return report

        # tell lobby to set nickname and hope for the best
        self.__lobby_model.set_nickname(self.__id, params['name'])
        # nothing to report lel
        return b''

    def __get_own_player_id(self):
        addr, port = self.__socket.getpeername()
        playerid = hashlib.sha1(b(addr + str(port))).hexdigest()
        return playerid

    def __leave_game(self):
        if self.__game is None:
            # illegal move
            return self.__message_parser.encode('report', {'status': '31'})

        self.__lobby_model.leave_game(self.__id)
        # if player who created game leaves then destroy the game
        if self.__player == 1:
            self.__lobby_model.delete_game(self.__game)

        self.__game = None
        return self.__message_parser.encode('report', {'status': '19'})

    def __unknown_msg(self):
        return self.__message_parser.encode('report', {'status': '40'})

    def __expect_parameter(self, expected, actual):
        keys = list(actual.keys())
        for p in expected:
            if p not in keys:
                return self.__unknown_msg()
        return None

    def __send(self, msg):
        logging.debug(b"Raw out: " + msg)
        self.__socket.sendall(msg)
