"""transaction_processor.py
TransactionProcessor applies one transaction at a time to the stores, and enforces
the business constraints. A transaction that breaks a constraint is logged with the
ErrorLog and skipped.
"""

from constants import (CODE_ADD_CREDIT, CODE_BUY, CODE_CREATE, CODE_DELETE,
                       CODE_END_OF_SESSION, CODE_REFUND, CODE_SELL)
from models import Game, User

# TransactionProcessor class is used to apply transactions to the user, game and collection stores
class TransactionProcessor:
    """Applies transactions to the user, game and collection stores."""

    def __init__(self, users, games, collection, error_log):
        self.users = users
        self.games = games
        self.collection = collection
        self.error_log = error_log
        # Map transaction codes to their corresponding handler methods
        self._handlers = {
            CODE_END_OF_SESSION: self.apply_end_of_session,
            CODE_CREATE: self.apply_create,
            CODE_DELETE: self.apply_delete,
            CODE_SELL: self.apply_sell,
            CODE_BUY: self.apply_buy,
            CODE_REFUND: self.apply_refund,
            CODE_ADD_CREDIT: self.apply_add_credit,
        }

    def process(self, transaction):
        """Apply one transaction by calling the handler for its code."""
        self._handlers[transaction.code](transaction)

    # ------------------------------------------------------------ transactions

    def apply_end_of_session(self, transaction):
        """00: marks the end of one Front End session. Nothing to change."""

    def apply_create(self, transaction):
        """01: add a new user with the given type and starting credit.
        Constraint: the name must not belong to an existing user."""
        if self.users.exists(transaction.username):
            self.error_log.constraint_error(
                "Duplicate username", f"user '{transaction.username}' already exists", transaction)
            return
        self.users.add(User(transaction.username, transaction.user_type, transaction.amount))

    def apply_delete(self, transaction):
        """02: remove a user, cancel the games they have for sale and remove the
        games in their collection."""
        if not self.users.exists(transaction.username):
            self.error_log.constraint_error(
                "Unknown user", f"cannot delete '{transaction.username}': no such user", transaction)
            return
        self.games.remove_by_seller(transaction.username)
        self.collection.remove_by_owner(transaction.username)
        self.users.remove(transaction.username)

    def apply_sell(self, transaction):
        """03: put a new game up for sale."""
        if not self.users.exists(transaction.seller):
            self.error_log.constraint_error(
                "Unknown user", f"seller '{transaction.seller}' does not exist", transaction)
            return
        if self.games.exists(transaction.game_name):
            self.error_log.constraint_error(
                "Duplicate game", f"game '{transaction.game_name}' is already for sale", transaction)
            return
        self.games.add(Game(transaction.game_name, transaction.seller, transaction.amount))

    def apply_add_credit(self, transaction):
        """06: add the credit in the record to the user's account."""
        user = self.users.find(transaction.username)
        if user is None:
            self.error_log.constraint_error(
                "Unknown user", f"cannot add credit to '{transaction.username}': no such user",
                transaction)
            return
        user.credit += transaction.amount

    def apply_buy(self, transaction):
        """04: NOT BUILT YET"""
        self.error_log.notice(f"buy (04) is not implemented yet; skipped: {transaction.raw_line.rstrip()}")

    def apply_refund(self, transaction):
        """05: NOT BUILT YET"""
        self.error_log.notice(f"refund (05) is not implemented yet; skipped: {transaction.raw_line.rstrip()}")