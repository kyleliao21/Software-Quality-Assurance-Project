"""models.py
The plain data objects of the Back End: a User, a Game for sale, an OwnedGame (one
entry of the game collection) and a Transaction read from the daily transaction file.
"""

from dataclasses import dataclass

# ----- Data classes for the Back End -----
@dataclass
class User:
    """One account. credit is in whole cents."""
    username: str
    user_type: str
    credit: int

    def has_enough_credit(self, cents):
        """True if the account can pay this many cents without going negative."""
        return self.credit >= cents


@dataclass
class Game:
    """One game that is for sale. price is in whole cents."""
    name: str
    seller: str
    price: int


@dataclass
class OwnedGame:
    """One line of the game collection: this user owns this game."""
    game_name: str
    owner: str


@dataclass
class Transaction:
    """One line of the daily transaction file, split into its fields.
    Only the fields that belong to the transaction's code are filled in:
      00, 01, 02, 06: username, user_type, amount   (amount = credit, or credit added for 06)
      03 sell:        game_name, seller, amount      (amount = price)
      04 buy:         game_name, seller, buyer, amount
      05 refund:      buyer, seller, amount
    raw_line keeps the original text so errors can quote it."""
    code: str
    raw_line: str
    username: str = ""
    user_type: str = ""
    game_name: str = ""
    seller: str = ""
    buyer: str = ""
    amount: int = 0