import playingfield

class Game:

    def __init__(self, name):
        self.__name = name
        self.__first_field = playingfield.PlayingField(16)
        self.__second_field = playingfield.PlayingField(16)

    def get_name(self):
        return self.__name

    def place_ship(self, player, id, x, y, direction):
        field = self.__get_field_by_player(player)

    def move_ship(self, player, id, direction):
        field = self.__get_field_by_player(player)

    def fire(self, player, x, y):
        field = self.__get_field_by_player(player)

    def nuke(self, player, x, y):
        field = self.__get_field_by_player(player)

    def __get_field_by_player(self, player):
        if player == 1:
            return self.__first_field
        elif player == 2:
            return self.__second_field
        return None
