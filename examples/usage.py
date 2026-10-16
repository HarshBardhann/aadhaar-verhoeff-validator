"""Short usage example. Uses a synthetic prefix only."""
from aadhaar_validator import generate_check_digit, validate_aadhaar_checksum

prefix = "12345678901"  # Synthetic; not an Aadhaar number.
candidate = prefix + generate_check_digit(prefix)
print("Format valid" if candidate.isascii() and candidate.isdigit() and len(candidate) == 12 else "Format invalid")
print("Checksum valid" if validate_aadhaar_checksum(candidate) else "Checksum invalid")
print("UIDAI issuance and identity were not verified.")
