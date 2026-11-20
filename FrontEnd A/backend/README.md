# Digital Games Distribution Service – Back End

**CSCI 3060U | Phase 4: Back End Rapid Prototype**
**Group 26 – Verify Games** (Saad, Ashwin, Kyle)

The Back End is a Python batch processor. Once a day it reads the previous day's account, available games, and game collection files, applies the merged daily transaction file to them, and writes updated files for the next day's Front End sessions.

---

## Status (Phase 4 prototype)

| Transaction | Code | Status |
|---|---|---|
| End of session | `00` | Implemented (no change to data) |
| Create | `01` | Implemented |
| Delete | `02` | Implemented |
| Sell | `03` | Implemented |
| Buy | `04` | **Not yet**: skipped with a `NOTE`|
| Refund | `05` | **Not yet**: skipped with a `NOTE`|
| Add credit | `06` | Implemented |

---

## Requirements

- Python 3.8 or newer
- No third-party dependencies

---

## Running the Backend

Run from `backend/`:

```
python3 main.py
```

> On some systems Python is invoked as `py` or `python` instead of `python3`.


---

## File formats

All files are fixed-width, with fields separated by a single space. Every file except the transaction file ends with a line starting with `END`.

**Accounts** – `username(15) type(2) credit(9)`
```
admin01         AA 000500.00
```
Account types: `AA` admin, `AM` account manager, `FS` full-standard, `BS` buy-standard, `SS` sell-standard.

**Available games** – `game name(26) seller(15) price(6)`

**Game collection** – `game name(26) owner(15)`

**Merged transaction file** – each line starts with a 2-digit code, followed by fixed-width fields:

| Code | Fields |
|---|---|
| `00`, `01`, `02`, `06` | `username(15) type(2) credit(9)` |
| `03` sell | `game name(26) seller(15) price(6)` |
| `04` buy | `game name(26) seller(15) buyer(15) price(6)` |
| `05` refund | `buyer(15) seller(15) credit(9)` |

The merged file is several Front End daily transaction files joined together, ending with a session that contains only the end-of-session record.

---

## How it works

A run has three phases, started by `BackEnd.run()`:

1. **Load** – read the three old files into the in-memory stores.
2. **Apply** – read each transaction in order; `TransactionProcessor.process()` dispatches it to the matching handler.
3. **Save** – write the stores to the three new files.

### Error handling

- **Failed constraint** – printed to the terminal and the transaction is skipped:
  `ERROR: <type>: <description> (transaction: <original record>)`
- **Fatal error** (file can't be opened or written, or malformed input) – raises `FatalError`; the program prints an `ERROR` message naming the problem and file, then exits with status 1.
- **Unimplemented transaction** – prints `NOTE: buy (04) is not implemented yet; skipped: ...` (likewise for refund).

---

## Project structure

```
backend/
├── main.py                   # Entry point: validates arguments, runs BackEnd, sets exit status
├── back_end.py               # BackEnd: controls load → apply → save
├── file_manager.py           # FileManager: all file reading and writing
├── transaction_parser.py     # TransactionParser: transaction line → Transaction
├── transaction_processor.py  # TransactionProcessor: applies transactions, enforces constraints
├── stores.py                 # UserStore, GameStore, CollectionStore (in-memory data)
├── models.py                 # User, Game, OwnedGame, Transaction (data classes)
├── errors.py                 # ErrorLog, FatalError, fatal_message()
├── formatting.py             # pad_right(), parse_cents(), format_cents()
└── constants.py              # Transaction codes, field widths, END marker
```

| Class | Responsibility |
|---|---|
| `BackEnd` | Controller for the batch workflow |
| `FileManager` | The only class that touches files |
| `TransactionParser` | Parses fixed-width transaction records; raises `FatalError` on bad ones |
| `TransactionProcessor` | Maps codes to handlers and applies them |
| `UserStore` / `GameStore` / `CollectionStore` | Hold accounts, listings, and ownership records in memory |
| `ErrorLog` | Prints constraint errors and notices |
| `FatalError` | Exception for corrupt or unreadable files |

---

## Account Manager Code Changes to FrontEnd

Changes were made to the following files in the `FrontEndA/phase2/src/` folder:
- Constants.h
- User.h & User.cpp
- PrivilegedTransaction.cpp
- CreateTransaction.cpp
- DeleteTransaction.cpp
- AddCreditTransaction.cpp
- SearchTransaction.cpp

### Running Account Manager Changes in Frontend
Run from `FrondEndA/phase2`. To test out the account manager feature run the code below in cmd:

```
frontend data/users.txt data/games.txt data/collection.txt data/transout1.atf < data/test.txt
```