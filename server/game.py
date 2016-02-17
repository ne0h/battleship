import playingfield
import logging

class Game:

    def __init__(self, name):
        self.__name = name
        self.__first_field = playingfield.PlayingField(16)
        self.__second_field = playingfield.PlayingField(16)
        self.__first_player = None
        self.__second_player = None

    def add_player(self, player, nick, id):
        if player == 1:
            self.__first_player = Player(nick, id)
        elif player == 2:
            self.__second_player = Player(nick, id)

    def remove_player(self, player):
        if player == 1:
            self.__first_player = None
        elif player == 2:
            self.__second_player = None

    def get_name(self):
        return self.__name

    def get_player(self, player):
        if player == 1:
            return self.__first_player
        elif player == 2:
            return self.__second_player
        return False

    def place_ship(self, player, id, x, y, direction):
        field = self.__get_field_by_player(player)
        logging.debug('place_ship()')

    def move_ship(self, player, id, direction):
        field = self.__get_field_by_player(player)
        logging.debug('move_ship()')

    def fire(self, player, x, y):
        field = self.__get_field_by_player(player)
        logging.debug('fire()')

    def nuke(self, player, x, y):
        field = self.__get_field_by_player(player)
        logging.debug('nuke()')

    def __get_field_by_player(self, player):
        if player == 1:
            return self.__first_field
        elif player == 2:
            return self.__second_field
        return None


class Player:

    def __init__(self, nick = None, id = None):
        self.__nick = nick
        self.__id = id

    def get_nick(self):
        return self.__nick

    def get_id(self):
        return self.__id

    def set_nick(self, nick):
        self.__nick = nick

    def set_id(self, id):
        self.__id = id
