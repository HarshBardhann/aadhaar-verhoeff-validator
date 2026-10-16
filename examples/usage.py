"""Short usage example. Uses a synthetic, Aadhaar-format prefix only."""
from aadhaar_validator import generate_check_digit, validate_aadhaar_checksum

prefix = "23456789012"  # Synthetic; first digit 2-9. Not a real Aadhaar number.
candidate = prefix + generate_check_digit(prefix)
format_valid = len(candidate) == 12 and candidate[0] in "23456789" and candidate.isascii() and candidate.isdigit()
print("Format valid" if format_valid else "Format invalid")
print("Checksum valid" if validate_aadhaar_checksum(candidate) else "Checksum invalid")
print("UIDAI issuance and identity were not verified.")
