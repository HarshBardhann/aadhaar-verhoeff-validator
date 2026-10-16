#!/usr/bin/env python3
"""Small local CLI for the Verhoeff checksum. Synthetic data works fine."""
from __future__ import annotations

import argparse

from aadhaar_validator import generate_check_digit, validate_aadhaar_checksum

LIMITATION = ("Important limitation: this tool validates format and Verhoeff checksum only; "
              "it does not verify UIDAI issuance, records, active status, or identity.")


def report(value: str) -> None:
    format_valid = len(value) == 12 and value.isascii() and value.isdigit()
    print(f"Format {'valid' if format_valid else 'invalid'}")
    print(f"Checksum {'valid' if format_valid and validate_aadhaar_checksum(value) else 'invalid'}")
    print("No UIDAI issuance or identity verification was performed.")


def demo() -> None:
    prefix = "12345678901"
    valid = prefix + generate_check_digit(prefix)
    substitution = valid[:4] + ("0" if valid[4] != "0" else "1") + valid[5:]
    swapped = valid[:2] + valid[3] + valid[2] + valid[4:]
    print("Synthetic demonstration (no identifiers are stored or transmitted):")
    for label, value in (("Checksum-valid synthetic string", valid),
                         ("Single-digit substitution", substitution),
                         ("Adjacent unequal-digit swap", swapped),
                         ("Invalid check digit", valid[:-1] + str((int(valid[-1]) + 1) % 10)),
                         ("Malformed input", valid[:6] + "X" + valid[7:])):
        print(f"\n{label}:")
        report(value)


def main() -> None:
    parser = argparse.ArgumentParser(description=LIMITATION)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--validate", metavar="VALUE", help="Validate locally (may remain in shell history).")
    group.add_argument("--generate", metavar="PREFIX", help="Generate for an 11-digit synthetic prefix.")
    group.add_argument("--demo", action="store_true", help="Run synthetic error-detection demonstration.")
    args = parser.parse_args()
    print(LIMITATION)
    if args.generate is not None:
        try:
            print(f"Check digit: {generate_check_digit(args.generate)}")
        except ValueError as error:
            print(f"Format invalid: {error}")
    elif args.demo:
        demo()
    else:
        value = args.validate if args.validate is not None else input("12-digit test string (not stored): ")
        report(value)


if __name__ == "__main__":
    main()
