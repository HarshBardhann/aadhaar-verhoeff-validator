"""Verhoeff checksum primitives. No network access, no UIDAI lookups."""

from typing import Final

# Standard decimal Verhoeff tables: multiplication (D), permutation (P), and
# inverse (INV), each indexed by digit 0-9.
_D: Final[tuple[tuple[int, ...], ...]] = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
    (1, 2, 3, 4, 0, 6, 7, 8, 9, 5),
    (2, 3, 4, 0, 1, 7, 8, 9, 5, 6),
    (3, 4, 0, 1, 2, 8, 9, 5, 6, 7),
    (4, 0, 1, 2, 3, 9, 5, 6, 7, 8),
    (5, 9, 8, 7, 6, 0, 4, 3, 2, 1),
    (6, 5, 9, 8, 7, 1, 0, 4, 3, 2),
    (7, 6, 5, 9, 8, 2, 1, 0, 4, 3),
    (8, 7, 6, 5, 9, 3, 2, 1, 0, 4),
    (9, 8, 7, 6, 5, 4, 3, 2, 1, 0),
)
_P: Final[tuple[tuple[int, ...], ...]] = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
    (1, 5, 7, 6, 2, 8, 3, 0, 9, 4),
    (5, 8, 0, 3, 7, 9, 6, 1, 4, 2),
    (8, 9, 1, 6, 0, 4, 3, 5, 2, 7),
    (9, 4, 5, 3, 1, 2, 6, 8, 7, 0),
    (4, 2, 8, 6, 5, 7, 3, 9, 0, 1),
    (2, 7, 9, 3, 8, 0, 6, 4, 1, 5),
    (7, 0, 4, 6, 9, 1, 3, 2, 5, 8),
)
_INV: Final[tuple[int, ...]] = (0, 4, 3, 2, 1, 5, 6, 7, 8, 9)

# Aadhaar-format rules, kept separate from the generic Verhoeff primitive.
_AADHAAR_LENGTH: Final[int] = 12
_AADHAAR_FIRST_DIGITS: Final[frozenset[str]] = frozenset("23456789")


def _is_ascii_digits(value: object) -> bool:
    return isinstance(value, str) and value.isascii() and value.isdigit()


def verhoeff_checksum_valid(number: str) -> bool:
    """Return True if an ASCII digit string has a valid Verhoeff checksum.

    No Aadhaar length rule here, this is the generic case. Non-string and
    non-ASCII-digit input returns False rather than being coerced. Leading
    zeros survive because the value is never converted to an int.
    """
    if not _is_ascii_digits(number):
        return False
    check = 0
    for position, char in enumerate(reversed(number)):
        check = _D[check][_P[position % 8][int(char)]]
    return check == 0


def validate_aadhaar_checksum(number: str) -> bool:
    """Return True if *number* matches the Aadhaar format with a valid checksum.

    "Aadhaar format" here means exactly 12 ASCII digits whose first digit is 2
    through 9; UIDAI numbers never start with 0 or 1. On top of that the final
    digit must be the correct Verhoeff check digit.

    True means only "format valid" and "checksum valid". It does not establish
    UIDAI issuance, that the record exists, that the number is active, who owns
    it, or anything about identity.
    """
    return (
        isinstance(number, str)
        and len(number) == _AADHAAR_LENGTH
        and number[0] in _AADHAAR_FIRST_DIGITS
        and _is_ascii_digits(number)
        and verhoeff_checksum_valid(number)
    )


def generate_check_digit(first_11: str) -> str:
    """Return the Verhoeff check digit for exactly 11 ASCII digits.

    This is generic: the 11 digits may start with any digit, including 0 or 1.
    The result makes ``first_11 + digit`` checksum-valid, but it does not
    establish Aadhaar issuance, and an 11-digit prefix that starts with 0 or 1
    cannot produce an Aadhaar-format result. Raises ValueError on bad input.
    """
    if not isinstance(first_11, str) or len(first_11) != 11 or not _is_ascii_digits(first_11):
        raise ValueError("first_11 must contain exactly 11 ASCII digits")
    check = 0
    # Generation shifts P by one position; validation does not.
    for position, char in enumerate(reversed(first_11)):
        check = _D[check][_P[(position + 1) % 8][int(char)]]
    return str(_INV[check])
