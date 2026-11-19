"""file_manager.py
FileManager is the only class that reads or writes files. It reads the three old
files and the merged daily transaction file, and writes the three new files.

Layouts (fields separated by one space, text padded with spaces on the right):
  accounts   : username(15) type(2) credit(9)           ends with a line "END"
  games      : game name(26) seller(15) price(6)        ends with a line "END"
  collection : game name(26) owner(15)                  ends with a line "END"
The Back End may assume the files are well formed. If it notices a corrupt line
it stops with a fatal error (FatalError).
"""

from constants import (CREDIT_WIDTH, END_MARKER, GAME_NAME_WIDTH, PRICE_WIDTH,
                       USERNAME_WIDTH, USER_TYPE_WIDTH)
from errors import FatalError, fatal_message
from formatting import format_cents, pad_right, parse_cents
from models import Game, OwnedGame, User
from transaction_parser import TransactionParser

# FileManager class is used to read the four input files and write the three output files
class FileManager:
    """Reads the four input files and writes the three output files."""

    def __init__(self, accounts_in, games_in, collection_in, transactions_in,
                 accounts_out, games_out, collection_out):
        self.accounts_in = accounts_in
        self.games_in = games_in
        self.collection_in = collection_in
        self.transactions_in = transactions_in
        self.accounts_out = accounts_out
        self.games_out = games_out
        self.collection_out = collection_out

    # --------------------------READING----------------------------------------
    # Read the three old files and the merged daily transaction file, returning lists of objects.
    def read_accounts(self):
        """Return a list of User objects read from the old accounts file."""
        users = []
        for number, line in self._data_lines(self.accounts_in, USERNAME_WIDTH):
            try:
                username = line[0:USERNAME_WIDTH].strip()
                user_type = line[USERNAME_WIDTH + 1:USERNAME_WIDTH + 1 + USER_TYPE_WIDTH]
                credit_start = USERNAME_WIDTH + 1 + USER_TYPE_WIDTH + 1
                credit = parse_cents(line[credit_start:credit_start + CREDIT_WIDTH])
            except ValueError:
                raise self._corrupt(self.accounts_in, number)
            users.append(User(username, user_type, credit))
        return users

    def read_games(self):
        """Return a list of Game objects read from the old available games file."""
        games = []
        for number, line in self._data_lines(self.games_in, GAME_NAME_WIDTH):
            try:
                seller_start = GAME_NAME_WIDTH + 1
                price_start = seller_start + USERNAME_WIDTH + 1
                name = line[0:GAME_NAME_WIDTH].strip()
                seller = line[seller_start:seller_start + USERNAME_WIDTH].strip()
                price = parse_cents(line[price_start:price_start + PRICE_WIDTH])
            except ValueError:
                raise self._corrupt(self.games_in, number)
            games.append(Game(name, seller, price))
        return games

    def read_collection(self):
        """Return a list of OwnedGame objects read from the old collection file."""
        entries = []
        for number, line in self._data_lines(self.collection_in, GAME_NAME_WIDTH):
            owner_start = GAME_NAME_WIDTH + 1
            name = line[0:GAME_NAME_WIDTH].strip()
            owner = line[owner_start:owner_start + USERNAME_WIDTH].strip()
            if not name or not owner:
                raise self._corrupt(self.collection_in, number)
            entries.append(OwnedGame(name, owner))
        return entries

    def read_transactions(self):
        """Return a list of Transaction objects read from the merged daily
        transaction file, in the order they appear."""
        parser = TransactionParser(self.transactions_in)
        transactions = []
        for number, line in self._lines(self.transactions_in):
            if line.strip():
                transactions.append(parser.parse(line, number))
        return transactions

    # ------------------------WRITING------------------------------------------
    # Write the three new files, each ending with the END line. The users, games and collection are written in the order they appear in the given lists.
    def write_accounts(self, users):
        """Write the new accounts file (one line per user, then the END line)."""
        lines = [pad_right(u.username, USERNAME_WIDTH) + " " + pad_right(u.user_type, USER_TYPE_WIDTH)
                 + " " + format_cents(u.credit, CREDIT_WIDTH) for u in users]
        lines.append(pad_right(END_MARKER, USERNAME_WIDTH) + " " + " " * USER_TYPE_WIDTH
                     + " " + format_cents(0, CREDIT_WIDTH))
        self._write_lines(self.accounts_out, lines)

    def write_games(self, games):
        """Write the new available games file (one line per game, then the END line)."""
        lines = [pad_right(g.name, GAME_NAME_WIDTH) + " " + pad_right(g.seller, USERNAME_WIDTH)
                 + " " + format_cents(g.price, PRICE_WIDTH) for g in games]
        lines.append(pad_right(END_MARKER, GAME_NAME_WIDTH) + " " + " " * USERNAME_WIDTH
                     + " " + format_cents(0, PRICE_WIDTH))
        self._write_lines(self.games_out, lines)

    def write_collection(self, entries):
        """Write the new game collection file (one line per entry, then the END line)."""
        lines = [pad_right(e.game_name, GAME_NAME_WIDTH) + " " + pad_right(e.owner, USERNAME_WIDTH)
                 for e in entries]
        lines.append(pad_right(END_MARKER, GAME_NAME_WIDTH) + " " + " " * USERNAME_WIDTH)
        self._write_lines(self.collection_out, lines)

    # ---------------------HELPERS---------------------------------------------
    # Helpers for reading and writing files
    def _lines(self, filename):
        """Yield (line number, text) for every line of a file. A file that cannot be
        opened is a fatal error."""
        try:
            with open(filename, encoding="utf-8") as file:
                for number, line in enumerate(file, start=1):
                    yield number, line.rstrip("\r\n")
        except OSError as problem:
            raise FatalError(fatal_message("Cannot open file", str(problem.strerror), filename))

    def _data_lines(self, filename, name_width):
        """Yield (line number, text) for the data lines of an input file: blank lines
        are skipped and reading stops at the END line (a line whose first field,
        name_width characters wide, is just END)."""
        for number, line in self._lines(filename):
            if not line.strip():
                continue
            if line[:name_width].strip() == END_MARKER:
                return
            yield number, line

    def _corrupt(self, filename, number):
        return FatalError(fatal_message("Corrupt file", f"bad line {number}", filename))

    def _write_lines(self, filename, lines):
        try:
            with open(filename, "w", encoding="utf-8", newline="\n") as file:
                file.write("\n".join(lines) + "\n")
        except OSError as problem:
            raise FatalError(fatal_message("Cannot write file", str(problem.strerror), filename))