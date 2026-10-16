# Aadhaar-formatted Verhoeff Checksum Validator

> **This project validates a checksum, not the authenticity of an Aadhaar number.**
>
> **Important limitation:** This tool validates the format and Verhoeff checksum of an Aadhaar-formatted number. It does not confirm that the number was issued by UIDAI, exists in official records, is active, or belongs to any individual. A checksum-valid number may be entirely fabricated. Do not use this tool as a substitute for official Aadhaar verification or identity authentication.

https://github.com/HarshBardhann/aadhaar-verhoeff-validator

This is a small reference project for checking an Aadhaar-formatted string locally. It looks at two things: whether the input is exactly 12 ASCII digits with a first digit from 2 to 9, and whether those digits end in a correct Verhoeff check digit. There is a Python package, a matching Node.js module, a CLI, a test suite, and some notes on the algorithm and on what a checksum can and cannot tell you. Nothing here contacts UIDAI or any other service.

## What it checks

| Result | Meaning |
| --- | --- |
| **Format valid** | Exactly 12 ASCII digits, first digit 2-9 |
| **Checksum valid** | The digits satisfy Verhoeff |
| **Format invalid** | Not 12 ASCII digits, or starts with 0 or 1 |
| **Checksum invalid** | Format-valid input fails Verhoeff |

Only the first two are things this project can actually tell you. It cannot confirm that UIDAI issued the number, and it cannot confirm who the number belongs to. Making up a checksum-valid number is trivial, and failing the checksum says nothing on its own about whether a number was ever issued.

## Features

- Verhoeff validation for any ASCII digit string, leading zeros included.
- Strict Aadhaar-format validation: exactly 12 ASCII digits with a first digit from 2 to 9.
- Generic check-digit generation from any 11 ASCII digits.
- pytest suite covering malformed input, Unicode numerals, leading 0/1 rejection, substitutions, transpositions, and leading zeros.
- A Node.js port that uses the same synthetic test vector.
- CLI that reads input interactively by default, so nothing has to land in shell history.
- Docs for the algorithm, privacy and security, integration, and API responses.

## Requirements and installation

Requires Python 3.9 or newer. Clone the repo and either run straight from the checkout with `PYTHONPATH=src`, or install it:

```sh
python -m pip install -e .
python -m pytest
```

There are no runtime dependencies. pytest is only needed for the tests.

## Quick start

```python
from aadhaar_validator import generate_check_digit, validate_aadhaar_checksum

prefix = "23456789012"              # synthetic, first digit 2-9
synthetic = prefix + generate_check_digit(prefix)
assert synthetic == "234567890124"
assert validate_aadhaar_checksum(synthetic)  # format and checksum ok, identity not checked
```

`verhoeff_checksum_valid(number)` is generic: it works on any non-empty ASCII digit string, leading zeros included. `validate_aadhaar_checksum(number)` adds the Aadhaar format rule on top, requiring exactly 12 ASCII digits whose first digit is 2-9 (UIDAI numbers never start with 0 or 1), plus a valid Verhoeff checksum. `generate_check_digit(first_11)` is also generic: it takes any 11 ASCII digits and raises `ValueError` otherwise, while a prefix starting with 0 or 1 cannot produce an Aadhaar-format number. A generated digit is arithmetic, not an issued identifier.

A checksum-valid string is not automatically an Aadhaar-format number. For example, `123456789010` passes Verhoeff generically but starts with 1, so it is **not** format valid.

## CLI

```sh
PYTHONPATH=src python examples/cli.py
PYTHONPATH=src python examples/cli.py --generate 23456789012
PYTHONPATH=src python examples/cli.py --demo
```

Running it with no arguments prompts for input, which keeps the value out of your shell history. Output uses the labels **Format valid/invalid** and **Checksum valid/invalid**, followed by a line stating that no UIDAI issuance or identity check happened.

## Node.js

The JavaScript port lives in `integrations/javascript`:

```sh
node integrations/javascript/example.js
```

See [integrations/javascript/README.md](integrations/javascript/README.md). Both ports produce `4` for the prefix `23456789012`, giving `234567890124`. Handle input as a string; casting it to a number drops leading zeros.

## Documentation

- [The algorithm](docs/algorithm.md), with a worked example
- [Integration guide](docs/integration-guide.md) and API response examples
- [Security, privacy, and limitations](docs/security-and-limitations.md)
- [FAQ](docs/faq.md)

## Repository layout

```text
src/aadhaar_validator/     Python package
examples/                  CLI and a short Python example
tests/                     pytest suite
integrations/              Node.js implementation
docs/                      Algorithm, integration, FAQ, security notes
```

## Responsible use and privacy

Use synthetic values while developing. Don't log identifiers, don't put them in URLs, and don't send them to third parties. Frontend validation can be bypassed, so repeat the same checks on the backend. If you do handle real identity data, follow the relevant law, privacy rules, and UIDAI requirements.

If you actually need to confirm issuance or an identity claim, use an authorised mechanism instead of a checksum. UIDAI's [Aadhaar Act information](https://uidai.gov.in/en/aadhaar-act) and its [authentication/verification clarification](https://www.uidai.gov.in/images/resource/Authentication_Verification_of_Aadhaar_vide_file_no_10_22_2017_EG_II_Vol-I_dated_19_06_2023.pdf) cover that area. Background on Verhoeff is on [Wikipedia](https://en.wikipedia.org/wiki/Verhoeff_algorithm) and in the original paper ([DOI:10.1002/zamm.19710510323](https://doi.org/10.1002/zamm.19710510323)). Links accessed 2026-10-16.

## Contributing and license

See [CONTRIBUTING.md](CONTRIBUTING.md). Licensed under the [MIT License](LICENSE).
