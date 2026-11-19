"""back_end.py
BackEnd is the controller of the run. It
  1. loads the old accounts, games and collection files,
  2. applies every transaction of the merged daily transaction file in order,
  3. writes the new accounts, games and collection files.
Constraint errors are logged on the terminal as they happen.
"""

from errors import ErrorLog
from stores import CollectionStore, GameStore, UserStore
from transaction_processor import TransactionProcessor

# BackEnd class is used to run one batch update of the master files
class BackEnd:
    """Runs one batch update of the master files."""

    def __init__(self, file_manager, error_log=None):
        self.file_manager = file_manager
        self.error_log = error_log if error_log is not None else ErrorLog()
        self.users = UserStore()
        self.games = GameStore()
        self.collection = CollectionStore()
        self.processor = TransactionProcessor(self.users, self.games, self.collection,
                                              self.error_log)

    def run(self):
        """Do the whole batch update. A FatalError from a corrupt file is not caught
        here: main() prints it and stops."""
        self._load_old_files()
        self._apply_transactions()
        self._write_new_files()

    def _load_old_files(self):
        """Read the three old files into the stores."""
        self.users.load(self.file_manager.read_accounts())
        self.games.load(self.file_manager.read_games())
        self.collection.load(self.file_manager.read_collection())

    def _apply_transactions(self):
        """Apply every transaction of the merged daily transaction file, in order."""
        for transaction in self.file_manager.read_transactions():
            self.processor.process(transaction)

    def _write_new_files(self):
        """Write the stores to the three new files."""
        self.file_manager.write_accounts(self.users.all())
        self.file_manager.write_games(self.games.all())
        self.file_manager.write_collection(self.collection.all())