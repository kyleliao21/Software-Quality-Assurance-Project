"""formatting.py
Small helper functions for the fixed-width text used by the input and output files:
padding text, and converting money between text ("000500.00") and whole cents (50000).
"""

# ----- Padding function -----
def pad_right(text, width):
    """Left-justify text in a field of the given width, padding with spaces"""
    return text[:width].ljust(width)

# ---- Money formatting functions -----
def parse_cents(text):
    """Convert money text such as "000500.00" or "15.5" into whole cents (an int).
    Raises ValueError if the text is not a valid non-negative amount."""
    text = text.strip()
    dollars, _, cents = text.partition(".")
    if not dollars.isdigit() or (cents and not cents.isdigit()) or len(cents) > 2:
        raise ValueError(f"not a valid money amount: '{text}'")
    return int(dollars) * 100 + int(cents.ljust(2, "0") or 0)

def format_cents(cents, width):
    """Convert whole cents into money text with two decimals, padded with zeros on the left."""
    return f"{cents // 100}.{cents % 100:02d}".zfill(width)