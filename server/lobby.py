import threading
import logging
from enum import Enum
from game import *

class LobbyError(Enum):
    game_is_full = 1,
    game_does_not_exist = 2

class LobbyEvent(Enum):
    on_update = 1

# Map of games by name
games = {}

# Set of waiting games
waiting_games = set()

# Set of all connected player ids
players = set()

# Map of callback lists by event type
callbacks = {}
# Initialize an empty list for each event
callbacks[LobbyEvent.on_update] = []

# Locks
games_lock = threading.Lock()
players_lock = threading.Lock()
callbacks_lock = threading.Lock()


class LobbyModel:

    def add_lobby(self, name, playerid):
        """
        Create a new lobby and make sure that the name is unique.
        Return the new game on success and False on failure (i.e., lobby name was already taken).
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

        # add new game to list of games and set first player id
        games[name] = Game(name, playerid)
        players_lock.acquire()
        players.add(playerid)
        players_lock.release()

        # add game to list of waiting games
        waiting_games.add(name)
        games_lock.release()

        # trigger on_update event
        self.__notify_all(LobbyEvent.on_update)

        # return the new game instance
        return games[name]

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
        games[name].get_player(2).set_id(playerid)
        players_lock.acquire()
        players.add(playerid)
        players_lock.release()

        # remove game from the list of waiting games
        waiting_games.remove(name)
        games_lock.release()

        # trigger on_update event
        self.__notify_all(LobbyEvent.on_update)

        # return the joined game instance
        return True, games[name]

    def get_number_of_games(self):
        """
        Return number of games, number of waiting games
        """
        global games
        global waiting_games
        return len(games), len(waiting_games)

    def get_number_of_players(self):
        global games
        global waiting_games
        return 2 * len(games) - len(waiting_games)

    def get_player_ids(self):
        global players
        global players_lock
        players_lock.acquire()
        result = []
        for p in players:
            result.append(p)
        players_lock.release()
        return result

    def leave_lobby(self, name):
        global games
        global waiting_games
        global games_lock
        games_lock.acquire()

        games_lock.release()

    def get_games_info(self):
        global games
        global waiting_games
        global games_lock
        games_lock.acquire()

        result = []
        for _, g in games.items():
            info = {}
            number_of_players = 1 if g.is_waiting() else 2
            if g.is_waiting():
                info['nicknames'] = [ g.get_player(1).get_nick() ]
                info['ids'] = [ g.get_player(1).get_id() ]
            else:
                info['nicknames'] = [ g.get_player(1).get_nick(), g.get_player(2).get_nick() ]
                info['ids'] = [ g.get_player(1).get_id(), g.get_player(2).get_id() ]

            info['game_name'] = g.get_name()
            info['number_of_players'] = number_of_players
            
            result.append(info)

        games_lock.release()
        return result

    def register_callback(self, event, callback):
        """
        Register a callback that will be triggered as a given event occurs.
        """
        logging.debug("register_callback({})".format(event))

        global callbacks
        global callbacks_lock

        callbacks_lock.acquire()
        callbacks[event].append(callback)
        callbacks_lock.release()

    def remove_callback(self, event, callback):
        """
        Remove a callback.
        """
        logging.debug("remove_callback({})".format(event))

        global callbacks
        global callbacks_lock

        callbacks_lock.acquire()
        callbacks[event].remove(callback)
        callbacks_lock.release()

    def __notify_all(self, event):
        logging.debug("__notify_all({})".format(event))
        global callbacks
        for cb in callbacks[event]:
            cb()
