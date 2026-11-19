"""main.py
Games Distribution Service - Back End (Phase 4 rapid prototype)

PURPOSE: the overnight batch processor. It reads the previous day's user accounts,
         available games and game collection files, applies every transaction of the
         merged daily transaction file (produced by the Front End), and writes the
         new accounts, games and collection files for tomorrow's Front End runs.
INPUT  : merged daily transaction file, old accounts file, old available games file,
         old game collection file.
OUTPUT : new accounts file, new available games file, new game collection file, and
         a log of failed constraints on the terminal ("ERROR: <message>").
RUN    : python3 main.py MERGED_TRANSACTIONS OLD_ACCOUNTS OLD_GAMES OLD_COLLECTION \\
                         NEW_ACCOUNTS NEW_GAMES NEW_COLLECTION
EXIT   : 0 when the run finished (constraint errors are only logged); 1 after a
         fatal error or a wrong command line.
"""

import sys

from back_end import BackEnd
from errors import FatalError
from file_manager import FileManager

ARGUMENT_COUNT = 7


def main(arguments):
    """Check the command line, run the batch update, and turn a fatal error into a
    message and a non-zero exit status."""
    if len(arguments) != ARGUMENT_COUNT:
        print("Usage: py main.py MERGED_TRANSACTIONS OLD_ACCOUNTS OLD_GAMES OLD_COLLECTION "
              "NEW_ACCOUNTS NEW_GAMES NEW_COLLECTION", file=sys.stderr)
        return 1

    merged, old_accounts, old_games, old_collection, new_accounts, new_games, new_collection = arguments
    file_manager = FileManager(old_accounts, old_games, old_collection, merged,
                               new_accounts, new_games, new_collection)
    try:
        BackEnd(file_manager).run()
    except FatalError as fatal:
        print(fatal)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))