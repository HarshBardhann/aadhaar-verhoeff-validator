import os
import subprocess
import sys
from pathlib import Path

import pytest

from aadhaar_validator import (
    generate_check_digit,
    validate_aadhaar_checksum,
    verhoeff_checksum_valid,
)


# Aadhaar-format synthetic vector: 12 digits, first digit 2-9.
SYNTHETIC_PREFIX = "23456789012"
SYNTHETIC_NUMBER = "234567890124"  # Generated locally; never an issuance claim.

# Generic, checksum-valid strings that are NOT Aadhaar-format (leading 0 or 1).
GENERIC_PREFIX = "12345678901"
GENERIC_NUMBER = "123456789010"
ROOT = Path(__file__).resolve().parents[1]


def _run_example(*arguments: str) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(ROOT / "src")
    return subprocess.run(
        [sys.executable, *arguments],
        cwd=ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )


def test_known_verhoeff_reference_vector() -> None:
    # 2363 is a commonly published generic Verhoeff example (not Aadhaar data).
    assert verhoeff_checksum_valid("2363")
    assert not verhoeff_checksum_valid("2364")


def test_generated_synthetic_aadhaar_vector_is_stable() -> None:
    assert generate_check_digit(SYNTHETIC_PREFIX) == "4"
    assert SYNTHETIC_NUMBER == SYNTHETIC_PREFIX + generate_check_digit(SYNTHETIC_PREFIX)
    assert verhoeff_checksum_valid(SYNTHETIC_NUMBER)
    assert validate_aadhaar_checksum(SYNTHETIC_NUMBER)


@pytest.mark.parametrize("first_digit", list("23456789"))
def test_aadhaar_format_accepts_leading_digits_two_through_nine(first_digit: str) -> None:
    prefix = first_digit + "0000000000"  # 11 digits
    complete = prefix + generate_check_digit(prefix)
    assert len(complete) == 12
    assert complete[0] == first_digit
    assert validate_aadhaar_checksum(complete)


@pytest.mark.parametrize("value", ["000000000003", "123456789010"])
def test_aadhaar_format_rejects_leading_zero_or_one(value: str) -> None:
    # Checksum-valid generically, but UIDAI numbers never start with 0 or 1.
    assert verhoeff_checksum_valid(value)
    assert not validate_aadhaar_checksum(value)


def test_generic_validator_and_generator_stay_generic() -> None:
    # generate_check_digit accepts any 11 ASCII digits, leading 0/1 included.
    assert generate_check_digit("00000000000") == "3"
    assert generate_check_digit(GENERIC_PREFIX) == "0"
    # verhoeff_checksum_valid accepts any non-empty ASCII digit string.
    assert verhoeff_checksum_valid("000000000003")
    assert verhoeff_checksum_valid(GENERIC_NUMBER)
    assert verhoeff_checksum_valid("2363")
    # Neither of the leading 0/1 strings is an Aadhaar-format number.
    assert not validate_aadhaar_checksum("000000000003")
    assert not validate_aadhaar_checksum(GENERIC_NUMBER)


@pytest.mark.parametrize(
    "value",
    [
        "",
        "123",
        SYNTHETIC_NUMBER + "0",        # 13 digits
        SYNTHETIC_NUMBER[:-1] + "X",   # non-digit
        "234567890 24",                 # embedded space
        "23456789012-",                 # embedded hyphen
        "२३४५६७८९०१२४",                # non-ASCII (Devanagari) digits
    ],
)
def test_aadhaar_format_rejects_malformed_values(value: str) -> None:
    assert not validate_aadhaar_checksum(value)


@pytest.mark.parametrize("value", [None, 123456789012, [], {}])
def test_validators_reject_non_strings(value: object) -> None:
    assert not verhoeff_checksum_valid(value)  # type: ignore[arg-type]
    assert not validate_aadhaar_checksum(value)  # type: ignore[arg-type]


def test_single_digit_substitution_is_detected() -> None:
    changed = SYNTHETIC_NUMBER[:5] + "0" + SYNTHETIC_NUMBER[6:]
    assert changed != SYNTHETIC_NUMBER
    assert changed[0] in "23456789"
    assert not validate_aadhaar_checksum(changed)


def test_adjacent_unequal_digit_transposition_is_detected() -> None:
    # Swap the unequal 3 and 4 in the synthetic string.
    swapped = SYNTHETIC_NUMBER[:1] + SYNTHETIC_NUMBER[2] + SYNTHETIC_NUMBER[1] + SYNTHETIC_NUMBER[3:]
    assert swapped != SYNTHETIC_NUMBER
    assert not validate_aadhaar_checksum(swapped)


def test_invalid_check_digit_is_detected() -> None:
    invalid = SYNTHETIC_NUMBER[:-1] + "5"
    assert invalid != SYNTHETIC_NUMBER
    assert not validate_aadhaar_checksum(invalid)


@pytest.mark.parametrize("value", ["1234567890", "123456789012", "1234567890X", "１２３４５６７８９０１"])
def test_generator_rejects_invalid_arguments(value: str) -> None:
    with pytest.raises(ValueError, match="exactly 11 ASCII digits"):
        generate_check_digit(value)


def test_generator_rejects_non_string() -> None:
    with pytest.raises(ValueError, match="exactly 11 ASCII digits"):
        generate_check_digit(12345678901)  # type: ignore[arg-type]


def test_checksum_validity_is_not_issuance_evidence() -> None:
    # The functions return booleans and nothing else; there is no UIDAI lookup
    # or issuance/identity assertion anywhere in the API.
    assert validate_aadhaar_checksum(SYNTHETIC_NUMBER)
    assert "issued" not in validate_aadhaar_checksum.__name__
    assert "issued" not in generate_check_digit.__name__


def test_usage_example_runs_with_synthetic_data_only() -> None:
    result = _run_example("examples/usage.py")
    assert result.returncode == 0, result.stderr
    assert result.stdout.splitlines() == [
        "Format valid",
        "Checksum valid",
        "UIDAI issuance and identity were not verified.",
    ]


def test_cli_demo_is_non_interactive_and_uses_standard_result_labels() -> None:
    result = _run_example("examples/cli.py", "--demo")
    assert result.returncode == 0, result.stderr
    assert "Format valid" in result.stdout
    assert "Format invalid" in result.stdout
    assert "Checksum valid" in result.stdout
    assert "Checksum invalid" in result.stdout
    assert "No UIDAI issuance or identity verification was performed." in result.stdout


def test_cli_rejects_bad_generation_input_with_a_nonzero_status() -> None:
    result = _run_example("examples/cli.py", "--generate", "not-a-prefix")
    assert result.returncode == 2
    assert "Format invalid: first_11 must contain exactly 11 ASCII digits" in result.stderr


def test_cli_handles_closed_standard_input_without_a_traceback() -> None:
    result = _run_example("examples/cli.py")
    assert result.returncode == 2
    assert "No input provided; nothing was validated." in result.stderr
