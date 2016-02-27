import threading
import logging
from enum import Enum
from game import *

class LobbyError(Enum):
    game_is_full = 1,
    game_does_not_exist = 2

class LobbyEvent(Enum):
    # do not forget to init the event callback list as well
    on_update = 1,
    on_chat = 2

# Map of games by name
games = {}

# Set of waiting games
waiting_games = set()

# Map of connected players by id
players = {}

# Map of callback lists by event type
callbacks = {}
# Initialize an empty list for each event
callbacks[LobbyEvent.on_update] = []
callbacks[LobbyEvent.on_chat] = []

# Locks
games_lock = threading.Lock()
players_lock = threading.Lock()
callbacks_lock = threading.Lock()


class LobbyModel:

    def add_player(self, id):
        global players
        global players_lock

        # add client as player
        players_lock.acquire()
        players[id] = Player(id=id)
        players_lock.release()

        # trigger on_update event
        self.__notify_all(LobbyEvent.on_update)

    def add_lobby(self, name, playerid):
        """
        Create a new lobby and make sure that the name is unique.
        Return True on success and False on failure (i.e., lobby name was already taken).
        """
        global games
        global waiting_games
        global players
        global games_lock
        global players_lock

        # make sure that game name does not exist yet
        games_lock.acquire()
        if name in games:
            games_lock.release()
            return False

        # add new game to list of games
        games[name] = Game(name, playerid)

        # add game to list of waiting games
        waiting_games.add(name)

        games_lock.release()

        # trigger on_update event
        self.__notify_all(LobbyEvent.on_update)

        return True

    def join_lobby(self, name, playerid):
        """
        Join an existing lobby.
        Return True on success and False on failure as first return parameter.
        Return the joined game on success and an error type on failure as second return parameter.
        """
        global games
        global waiting_games
        global players
        global games_lock
        global players_lock

        # make sure game name exists
        games_lock.acquire()
        if name not in games:
            games_lock.release()
            return False, LobbyError.game_does_not_exist

        # make sure the game is not full
        if name not in waiting_games:
            games_lock.release()
            return False, LobbyError.game_is_full

        # set second player id in the game and add the id to the list of players
        games[name].set_second_player(playerid)
        players_lock.acquire()
        players[playerid].set_id(playerid)
        players_lock.release()

        # remove game from the list of waiting games
        waiting_games.remove(name)
        games_lock.release()

        # trigger on_update event
        self.__notify_all(LobbyEvent.on_update)

        return True, None

    def get_number_of_games(self):
        """
        Return number of games, number of waiting games
        """
        global games
        global waiting_games
        return len(games), len(waiting_games)

    def get_number_of_players(self):
        """
        Return number of connected clients.
        """
        global players
        return len(players)

    def get_players_info(self):
        global players
        global players_lock
        players_lock.acquire()

        result = []
        for _, p in players.items():
            info = {}
            info['nickname'] = p.get_nick()
            info['id'] = p.get_id()

            result.append(info)

        players_lock.release()
        return result

    def delete_player(self, id):
        """
        Delete a player and make sure that a joined game is aborted as well.
        """
        global games
        global waiting_games
        global players
        global players_lock
        global games_lock

        # remove player
        players_lock.acquire()
        players.pop(id, None)
        players_lock.release()

        # remove game if joined
        games_lock.acquire()
        for k, g in games.items():
            # id for each first and second player
            id1 = g.get_player(1)
            id2 = g.get_player(2)
            if id == id1 or id == id2:
                games.pop(k, None)
                if k in waiting_games:
                    waiting_games.remove(k)
                break
        games_lock.release()

        # trigger on_game_deleted and on_update
        self.__notify_all(LobbyEvent.on_update)

    def chat(self, player, msg):
        import time
        timestamp = str(int(time.time() * 1000))
        params = {
            'timestamp': timestamp,
            'player': player,
            'msg': msg
        }
        self.__notify_all(LobbyEvent.on_chat, params)

    def delete_game(self, game):
        """
        Destroy the whole game.
        """
        global games
        global waiting_games
        global games_lock

        games_lock.acquire()
        # delete game
        games.pop(game, None)
        if game in waiting_games:
            waiting_games.remove(game)
        games_lock.release()

        # trigger on_update
        self.__notify_all(LobbyEvent.on_update)

    def set_nickname(self, player, nick):
        global players
        global players_lock
        players_lock.acquire()

        if player not in players:
            logging.debug("This should never happen.")
            logging.debug(player)
            players_lock.release()
            return False

        players[player].set_nick(nick)

        players_lock.release()

        # trigger on_update event
        self.__notify_all(LobbyEvent.on_update)

        return True

    def get_games_info(self):
        global games
        global waiting_games
        global games_lock
        global players_lock
        games_lock.acquire()
        players_lock.acquire()

        result = []
        for _, g in games.items():
            info = {}
            number_of_players = 1 if g.is_waiting() else 2
            if g.is_waiting():
                info['nicknames'] = [ players[g.get_player(1)].get_nick() ]
                info['ids'] = [ g.get_player(1) ]
            else:
                info['nicknames'] = [ players[g.get_player(1)].get_nick(), players[g.get_player(2)].get_nick() ]
                info['ids'] = [ g.get_player(1), g.get_player(2) ]

            info['game_name'] = g.get_name()
            info['number_of_players'] = number_of_players

            result.append(info)

        players_lock.release()
        games_lock.release()
        return result

    def get_game(self, name):
        global games
        global games_lock

        games_lock.acquire()
        g = games[name]
        games_lock.release()
        return g

    def register_callback(self, event, callback):
        """
        Register a callback that will be triggered as a given event occurs.
        """
        logging.debug("Lobby register_callback({})".format(event))

        global callbacks
        global callbacks_lock

        callbacks_lock.acquire()
        callbacks[event].append(callback)
        callbacks_lock.release()

    def remove_callback(self, event, callback):
        """
        Remove a callback.
        """
        logging.debug("Lobby remove_callback({})".format(event))

        global callbacks
        global callbacks_lock

        callbacks_lock.acquire()
        callbacks[event].remove(callback)
        callbacks_lock.release()

    def __notify_all(self, event, params = {}):
        logging.debug("Lobby __notify_all({})".format(event))
        global callbacks
        callbacks_lock.acquire()
        for cb in callbacks[event]:
            cb(**params)
        callbacks_lock.release()
