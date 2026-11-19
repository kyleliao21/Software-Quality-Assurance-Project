"""errors.py
How the Back End reports problems. Every message starts with "ERROR: ".

  * A FAILED CONSTRAINT (a transaction that breaks a business rule) is logged on the
    terminal and the transaction is skipped.
  * A FATAL ERROR (a file that is not in the expected format) stops the program.
"""

import sys


class FatalError(Exception):
    """Raised when an input file is corrupt."""


# ErrorLog class is used to log failed constraints and other notices
class ErrorLog:
    """Prints error messages in the required form: ERROR: <message>."""

    def __init__(self, stream=None):
        self.stream = stream if stream is not None else sys.stdout

    def constraint_error(self, error_type, description, transaction):
        """Log a failed constraint: its type, a description and the transaction that
        caused it. The transaction is then skipped by the caller."""
        print(f"ERROR: {error_type}: {description} "
              f"(transaction: {transaction.raw_line.rstrip()})", file=self.stream)

    def notice(self, message):
        """Log something that is not an error (for example a transaction type that
        this version does not implement yet)."""
        print(f"NOTE: {message}", file=self.stream)


def fatal_message(error_type, description, filename):
    """Build the text of a fatal error: its type, a description and the file that
    caused it."""
    return f"ERROR: {error_type}: {description} (file: {filename})"