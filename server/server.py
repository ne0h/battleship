import sys
import logging
import socketserver
import struct
import threading
from messageparser import MessageParser
import messages
from lobby import *

global_clients = []
global_clients_lock = threading.Lock()


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
        self.__player_id = None

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
            else:
                report = self.__unknown_msg()

            # send answer to client
            logging.debug(b"Raw out: " + report)
            self.__socket.sendall(report)

    def on_update_lobby(self):
        logging.debug("on_update_lobby()")
        ngames = self.__lobby_model.get_number_of_games()
        nclients = self.__lobby_model.get_number_of_players()
        gamesinfo = self.__lobby_model.get_games_info()
        logging.debug("Games: " + repr(gamesinfo))

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
            logging.error("Client already in some game.")
            return

        # create the game
        game = self.__lobby_model.add_lobby(params['name'])
        if game:
            self.__game = game
            self.__player_id = 1
            # TODO use a const here
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
            logging.error("Client already in some game.")
            return

        # join the game
        game = self.__lobby_model.join_lobby(params['name'])
        if game:
            self.__game = game
            self.__player_id = 2
            # TODO use a const here
            return self.__message_parser.encode('report', {'status': '27'})
        else:
            return self.__message_parser.encode('report', {'status': '37'})

    def __unknown_msg(self):
        # TODO use a const here
        return self.__message_parser.encode('report', {'status': '40'})

    def __expect_parameter(self, expected, actual):
        keys = list(actual.keys())
        for p in expected:
            if p not in keys:
                return self.__unknown_msg()
        return None
