import sys
import logging
import socketserver
import struct
import threading
import hashlib
from messageparser import MessageParser
import messages
from lobby import *
from game import *
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

        # register callbacks
        # TODO consistently rename on_update into on_update_lobby
        self.__lobby_model.register_callback(LobbyEvent.on_update, self.on_update_lobby)
        self.__lobby_model.register_callback(LobbyEvent.on_game_deleted, self.on_game_deleted)

    def handle(self):
        logging.info("Client {} connected.".format(self.__socket.getpeername()))
        while True:
            # receive 2 bytes size header
            size = self.__socket.recv(2)
            if not size:
                logging.debug("Did not receive 2 bytes header.")
                break
            size = struct.unpack('>H', size)[0]
            logging.debug("Size: " + str(size))

            # receive message body
            msg = self.__socket.recv(size)
            if not msg:
                logging.debug("Did not receive {} bytes body.".format(str(size)))
                break
            logging.debug(b"Raw in: " + msg)

            # explode received data into message type and parameters
            msgtype, msgparams = self.__message_parser.decode(msg.decode())
            logging.debug("Msg type: " + msgtype)
            logging.debug("Msg parameters: " + repr(msgparams))

            # dispatch message type
            if msgtype == messages.CREATE_GAME:
                self.__create_game(msgparams)
            elif msgtype == messages.JOIN_GAME:
                self.__join_game(msgparams)
            elif msgtype == messages.SET_NICK:
                self.__set_nickname(msgparams)
            elif msgtype == messages.LEAVE_GAME:
                self.__leave_game()
            elif msgtype == messages.INIT_BOARD:
                self.__init_board(msgparams)
            else:
                self.__unknown_msg()

    #
    # Callbacks
    #

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

    def on_game_deleted(self):
        self.__game = None
        self.__send(self.__message_parser.encode('report', {'status': '19'}))

    def on_ship_edit(self):
        logging.debug('on_ship_edit()')
        self.__send(self.__message_parser.encode('report', {'status': '18'}))

    def on_game_start(self):
        logging.debug('on_game_start()')
        self.__send(self.__message_parser.encode('report', {'status': '48'}))

    def on_update_field(self):
        logging.debug('on_update_field()')

    def get_socket(self):
        return self.__socket

    def finish(self):
        logging.info("Client {} disconnected.".format(self.__socket.getpeername()))

        # remove any left callbacks
        self.__lobby_model.remove_callback(LobbyEvent.on_update, self.on_update_lobby)
        self.__lobby_model.remove_callback(LobbyEvent.on_game_deleted, self.on_game_deleted)

        self.__lobby_model.delete_player(self.__id)

        # TODO remove game callbacks

    def __create_game(self, params):
        # make sure parameter list is complete
        if not self.__expect_parameter(['name'], params):
            return

        # check if client is already in a game
        if self.__game:
            logging.debug("Client already in some game.")
            self.__send(self.__message_parser.encode('report', {'status': '31'}))
            return

        # check game name length
        if 1 > len(params['name']) or len(params['name']) > 64:
            logging.debug("Game name too long.")
            self.__send(self.__message_parser.encode('report', {'status': '37'}))
            return

        # create the game
        game = self.__lobby_model.add_lobby(params['name'], self.__id)
        if game:
            self.__game = params['name']
            self.__player = 1
            self.__send(self.__message_parser.encode('report', {'status': '28'}))
            return

        self.__send(self.__message_parser.encode('report', {'status': '37'}))

        # register game callbacks
        self.__lobby_model.get_game(self.__game).register_callback(GameEvent.on_ship_edit, self.on_ship_edit)
        self.__lobby_model.get_game(self.__game).register_callback(GameEvent.on_game_start, self.on_game_start)
        self.__lobby_model.get_game(self.__game).register_callback(GameEvent.on_update_field, self.on_update_field)

    def __join_game(self, params):
        # make sure parameter list is complete
        if not self.__expect_parameter(['name'], params):
            return

        # check if client is already in a game
        if self.__game:
            logging.debug("Client already in some game.")
            self.__send(self.__message_parser.encode('report', {'status': '31'}))
            return

        # join the game
        game, e = self.__lobby_model.join_lobby(params['name'], self.__id)

        # handle game join errors
        if e:
            if e == LobbyError.game_is_full:
                self.__send(self.__message_parser.encode('report', {'status': '47'}))
                return
            elif e == LobbyError.game_does_not_exist:
                self.__send(self.__message_parser.encode('report', {'status': '37'}))
                return

        # ack game join
        self.__send(self.__message_parser.encode('report', {'status': '27'}))

        self.__game = params['name']
        self.__player = 2

        # register game callbacks
        self.__lobby_model.get_game(self.__game).register_callback(GameEvent.on_ship_edit, self.on_ship_edit)
        self.__lobby_model.get_game(self.__game).register_callback(GameEvent.on_game_start, self.on_game_start)
        self.__lobby_model.get_game(self.__game).register_callback(GameEvent.on_update_field, self.on_update_field)

        self.__lobby_model.get_game(self.__game).just_begin_ship_placement_already()

    def __set_nickname(self, params):
        if not self.__expect_parameter(['name'], params):
            return

        if len(params['name']) > 64:
            logging.debug("Nickname too long.")
            # 31 is the new 42
            self.__send(self.__message_parser.encode('report', {'status': '31'}))
            return

        # tell lobby to set nickname and hope for the best
        self.__lobby_model.set_nickname(self.__id, params['name'])

    def __get_own_player_id(self):
        addr, port = self.__socket.getpeername()
        playerid = hashlib.sha1(b(addr + str(port))).hexdigest()
        return playerid

    def __init_board(self, params):
        shipx = 'ship_{}_x'
        shipy = 'ship_{}_y'
        shipdir = 'ship_{}_direction'
        if not self.__expect_parameter(
            [shipx.format(i) for i in range(0, 10)] +
            [shipy.format(i) for i in range(0, 10)] +
            [shipdir.format(i) for i in range(0, 10)], params):
            return

        # init board
        left = True
        for id in range(0, 10):
            x = params[shipx.format(i)]
            y = params[shipy.format(i)]
            dir = params[shipdir.format(i)]
            suc, left = self.__lobby_model.get_game(self.__game).place_ship(self.__player, x, y, dir, id)
            # catch illegal placement
            if suc == -1:
                logging.debug("Nonsense ship placement.")
                self.__send(self.__message_parser.encode('report', {'status': '38'}))
                return

        if left:
            logging.debug("Something is still wrong with ship placement.")
            self.__send(self.__message_parser.encode('report', {'status': '38'}))
            return

        # ack init board
        self.__send(self.__message_parser.encode('report', {'status': '29'}))

    def __leave_game(self):
        if self.__game is None:
            # illegal move
            self.__send(self.__message_parser.encode('report', {'status': '31'}))
            return

        self.__lobby_model.leave_game(self.__id)
        # if player who created game leaves then destroy the game else just leave
        #if self.__player == 1:
        #    self.__lobby_model.delete_game(self.__game)
        #else:
        #    self.__lobby_model.leave_game(self.__game)

        # nevermind lulz
        self.__lobby_model.delete_game(self.__game)

        # TODO remove game callbacks

    def __unknown_msg(self):
        self.__send(self.__message_parser.encode('report', {'status': '40'}))

    def __expect_parameter(self, expected, actual):
        keys = list(actual.keys())
        for p in expected:
            if p not in keys:
                self.__unknown_msg()
                return False
        return True

    def __send(self, msg):
        logging.debug(b"Raw out: " + msg)
        self.__socket.sendall(msg)
