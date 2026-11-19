"""transaction_parser.py
TransactionParser turns one line of the merged daily transaction file into a
Transaction object. Each line starts with a two-digit code and then fields of fixed
width separated by single spaces:

  00 end of session, 01 create, 02 delete, 06 add credit:
        code username(15) type(2) credit(9)
  03 sell    : code game name(26) seller(15) price(6)
  04 buy     : code game name(26) seller(15) buyer(15) price(6)
  05 refund  : code buyer(15) seller(15) credit(9)
"""

from constants import (CODE_BUY, CODE_REFUND, CODE_SELL, ALL_CODES, CREDIT_WIDTH,
                       GAME_NAME_WIDTH, PRICE_WIDTH, USERNAME_WIDTH, USER_RECORD_CODES,
                       USER_TYPE_WIDTH)
from errors import FatalError, fatal_message
from formatting import parse_cents
from models import Transaction

CODE_WIDTH = 2

# TransactionParser class is used to parse transaction lines into Transaction objects
class TransactionParser:
    """Splits transaction lines into fields. Needs the file name only so that a
    fatal error can say which file was corrupt."""

    def __init__(self, filename):
        self.filename = filename

    # Parse one line of the merged daily transaction file into a Transaction object
    def parse(self, line, line_number):
        """Return the Transaction for one line, or raise FatalError if the line is
        not in the expected format."""
        code = line[:CODE_WIDTH]
        if code not in ALL_CODES:
            raise self._corrupt(line_number, f"unknown transaction code '{code}'")

        if code in USER_RECORD_CODES:
            widths = [USERNAME_WIDTH, USER_TYPE_WIDTH, CREDIT_WIDTH]
        elif code == CODE_SELL:
            widths = [GAME_NAME_WIDTH, USERNAME_WIDTH, PRICE_WIDTH]
        elif code == CODE_BUY:
            widths = [GAME_NAME_WIDTH, USERNAME_WIDTH, USERNAME_WIDTH, PRICE_WIDTH]
        else:                                   
            widths = [USERNAME_WIDTH, USERNAME_WIDTH, CREDIT_WIDTH]

        fields = self._split(line, widths, line_number)
        try:
            return self._build(code, line, fields)
        except ValueError:
            raise self._corrupt(line_number, "bad money amount")

    # Split the text after the code into fields of the given widths
    def _split(self, line, widths, line_number):
        """Cut the text after the code into fields of the given widths."""
        if len(line) < CODE_WIDTH + sum(w + 1 for w in widths):
            raise self._corrupt(line_number, "line too short")
        fields = []
        position = CODE_WIDTH + 1
        for width in widths:
            fields.append(line[position:position + width])
            position += width + 1
        return fields

    # Build a Transaction object from the code and the text fields
    def _build(self, code, line, fields):
        """Fill a Transaction from the text fields (money becomes whole cents)."""
        if code in USER_RECORD_CODES:
            return Transaction(code, line, username=fields[0].strip(), user_type=fields[1].strip(),
                               amount=parse_cents(fields[2]))
        if code == CODE_SELL:
            return Transaction(code, line, game_name=fields[0].strip(), seller=fields[1].strip(),
                               amount=parse_cents(fields[2]))
        if code == CODE_BUY:
            return Transaction(code, line, game_name=fields[0].strip(), seller=fields[1].strip(),
                               buyer=fields[2].strip(), amount=parse_cents(fields[3]))
        return Transaction(code, line, buyer=fields[0].strip(), seller=fields[1].strip(),
                           amount=parse_cents(fields[2]))

    # Raise a FatalError for a corrupt transaction line
    def _corrupt(self, line_number, description):
        return FatalError(fatal_message("Corrupt transaction file",
                                        f"line {line_number}: {description}", self.filename))