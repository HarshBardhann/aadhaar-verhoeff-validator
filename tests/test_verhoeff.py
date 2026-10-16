import pytest

from aadhaar_validator import (
    generate_check_digit,
    validate_aadhaar_checksum,
    verhoeff_checksum_valid,
)


SYNTHETIC_PREFIX = "12345678901"
SYNTHETIC_NUMBER = "123456789010"  # Generated locally; never an issuance claim.


def test_known_verhoeff_reference_vector() -> None:
    # 2363 is a commonly published generic Verhoeff example (not Aadhaar data).
    assert verhoeff_checksum_valid("2363")
    assert not verhoeff_checksum_valid("2364")


def test_generated_synthetic_vector_is_stable() -> None:
    assert generate_check_digit(SYNTHETIC_PREFIX) == "0"
    assert SYNTHETIC_NUMBER == SYNTHETIC_PREFIX + generate_check_digit(SYNTHETIC_PREFIX)
    assert verhoeff_checksum_valid(SYNTHETIC_NUMBER)
    assert validate_aadhaar_checksum(SYNTHETIC_NUMBER)


def test_leading_zeros_are_preserved() -> None:
    prefix = "00000000000"
    complete = prefix + generate_check_digit(prefix)
    assert complete == "000000000003"
    assert validate_aadhaar_checksum(complete)


@pytest.mark.parametrize("value", ["", "123", "1234567890100", "12345678901X", "123 45678901", "1234567890-0", "१२३४५६७८९०१२"])
def test_aadhaar_format_rejects_malformed_values(value: str) -> None:
    assert not validate_aadhaar_checksum(value)


@pytest.mark.parametrize("value", [None, 123456789010, [], {}])
def test_generic_validator_rejects_non_strings(value: object) -> None:
    assert not verhoeff_checksum_valid(value)  # type: ignore[arg-type]


def test_single_digit_substitution_is_detected() -> None:
    changed = SYNTHETIC_NUMBER[:5] + "0" + SYNTHETIC_NUMBER[6:]
    assert changed != SYNTHETIC_NUMBER
    assert not validate_aadhaar_checksum(changed)


def test_adjacent_unequal_digit_transposition_is_detected() -> None:
    # Swap the unequal 3 and 4 in the synthetic string.
    swapped = SYNTHETIC_NUMBER[:2] + SYNTHETIC_NUMBER[3] + SYNTHETIC_NUMBER[2] + SYNTHETIC_NUMBER[4:]
    assert not validate_aadhaar_checksum(swapped)


def test_invalid_check_digit_is_detected() -> None:
    invalid = SYNTHETIC_NUMBER[:-1] + "1"
    assert not validate_aadhaar_checksum(invalid)


@pytest.mark.parametrize("value", ["1234567890", "123456789012", "1234567890X", "１２３４５６７８９０１"])
def test_generator_rejects_invalid_arguments(value: str) -> None:
    with pytest.raises(ValueError, match="exactly 11 ASCII digits"):
        generate_check_digit(value)


def test_generator_rejects_non_string() -> None:
    with pytest.raises(ValueError, match="exactly 11 ASCII digits"):
        generate_check_digit(12345678901)  # type: ignore[arg-type]


def test_checksum_validity_is_not_issuance_evidence() -> None:
    # The function returns a boolean and nothing else; there is no UIDAI
    # lookup or issuance/identity assertion anywhere in the API.
    assert validate_aadhaar_checksum(SYNTHETIC_NUMBER)
    assert "issued" not in validate_aadhaar_checksum.__name__
