"""constants.py
Every fixed value the Back End uses, in one place: field widths of the fixed-width
files, the transaction codes, and the name of the end-of-file marker.
"""

# ----- Field widths (number of characters) -----
USERNAME_WIDTH = 15
USER_TYPE_WIDTH = 2
CREDIT_WIDTH = 9
GAME_NAME_WIDTH = 26
PRICE_WIDTH = 6

# ----- Special line that ends every input file -----
END_MARKER = "END"

# ----- Transaction codes in the merged daily transaction file -----
CODE_END_OF_SESSION = "00"
CODE_CREATE = "01"
CODE_DELETE = "02"
CODE_SELL = "03"
CODE_BUY = "04"
CODE_REFUND = "05"
CODE_ADD_CREDIT = "06"

# Transaction codes that require a user record to be present in the user accounts file
USER_RECORD_CODES = (CODE_END_OF_SESSION, CODE_CREATE, CODE_DELETE, CODE_ADD_CREDIT)
ALL_CODES = USER_RECORD_CODES + (CODE_SELL, CODE_BUY, CODE_REFUND)