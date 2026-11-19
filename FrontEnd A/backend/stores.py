"""stores.py
The in-memory collections the Back End works on while it applies transactions:
  UserStore        all accounts
  GameStore        all games that are for sale
  CollectionStore  which user owns which game
Each one is loaded from the old files, changed by the transactions, and then written
to the new files.
"""

from models import OwnedGame

# UseStore class is used to keep all accounts in memory while the Back End applies transactions
class UserStore:
    """All accounts, kept in the order they were loaded."""

    def __init__(self):
        self._users = {}          

    def load(self, users):
        """Replace the contents with this list of User objects."""
        self._users = {user.username: user for user in users}

    def find(self, username):
        """Return the User with this username, or None."""
        return self._users.get(username)

    def exists(self, username):
        return username in self._users

    def add(self, user):
        self._users[user.username] = user

    def remove(self, username):
        self._users.pop(username, None)

    def all(self):
        """Every user, in order."""
        return list(self._users.values())


# GameStore class is used to keep all games for sale in memory while the Back End applies transactions
class GameStore:
    """All games for sale, kept in the order they were loaded."""

    def __init__(self):
        self._games = {}          

    def load(self, games):
        self._games = {game.name: game for game in games}

    def find(self, name):
        return self._games.get(name)

    def exists(self, name):
        return name in self._games

    def add(self, game):
        self._games[game.name] = game

    def remove_by_seller(self, seller):
        """Cancel every game this user has for sale (used when a user is deleted)."""
        self._games = {name: game for name, game in self._games.items()
                       if game.seller != seller}

    def all(self):
        return list(self._games.values())


# CollectionStore class is used to keep track of which user owns which game while the Back End applies transactions
class CollectionStore:
    """Which user owns which game."""

    def __init__(self):
        self._entries = []        

    def load(self, entries):
        self._entries = list(entries)

    def owns(self, owner, game_name):
        return any(e.owner == owner and e.game_name == game_name for e in self._entries)

    def add(self, owner, game_name):
        self._entries.append(OwnedGame(game_name, owner))

    def remove_by_owner(self, owner):
        """Remove every entry of this user (used when a user is deleted)."""
        self._entries = [e for e in self._entries if e.owner != owner]

    def all(self):
        return list(self._entries)