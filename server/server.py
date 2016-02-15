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
        self.__game = None

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
            data[waitwhat.format(i, 0)] = game['nicknames'][0]
            # player 2 stuff
            if game['number_of_players'] == 2:
                data[whatevenisthis.format(i, 1)] = game['ids'][1]
                data[waitwhat.format(i, 1)] = game['nicknames'][1]
            i += 1

        # concat all player ids
        ids = self.__lobby_model.get_player_ids()
        j = 0
        for id in ids:
            data[yetanotherkey.format(j)] = id
            j += 1

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
            # TODO fix this crap
            logging.debug("Client already in some game.")
            return

        # create the game
        addr, port = self.__socket.getpeername()
        playerid = hashlib.sha1(b(addr + str(port))).hexdigest()
        game = self.__lobby_model.add_lobby(params['name'], playerid)
        if game:
            self.__game = game
            # TODO use consts here
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
            # TODO fix this crap
            logging.debug("Client already in some game.")
            return

        # join the game
        addr, port = self.__socket.getpeername()
        playerid = hashlib.sha1(b(addr + str(port))).hexdigest()
        game = self.__lobby_model.join_lobby(params['name'], playerid)
        if game:
            self.__game = game
            # TODO use consts here
            return self.__message_parser.encode('report', {'status': '27'})
        else:
            return self.__message_parser.encode('report', {'status': '37'})

    def __leave_game(self):
        self.__lobby_model.leave_lobby
        # TODO use consts here
        return self.__message_parser.encode('report', {'status': '19'})

    def __unknown_msg(self):
        # TODO use consts here
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
