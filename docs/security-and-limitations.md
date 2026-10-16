# Security, privacy, and limitations

> **Important limitation:** This tool validates the format and Verhoeff checksum of an Aadhaar-formatted number. It does not confirm that the number was issued by UIDAI, exists in official records, is active, or belongs to any individual. A checksum-valid number may be entirely fabricated. Do not use this tool as a substitute for official Aadhaar verification or identity authentication.

## Four things, only two of which this project does

| Concept | Can this project establish it? |
| --- | --- |
| Format validity: exactly 12 ASCII digits | Yes |
| Checksum validity: Verhoeff result is zero | Yes |
| Official issuance verification | No |
| Identity authentication | No |

A **Checksum invalid** result only means the digits fail this test. By itself it says nothing about whether the number was ever issued. When a sample response shows `false` for official verification, that just means this tool did not perform that check; it is not a claim that the number is unissued or that someone is unauthenticated.

## A checksum is not authentication

Verhoeff is good at catching typos. It is public, deterministic, and not cryptographic. Anyone can pick eleven digits and compute the twelfth, so invented but checksum-valid numbers are normal and expected. Whether treating a checksum as a security control is a weakness depends on what the application does and what else it checks. As a local input-quality check it is fine; as an identity decision it is not.

## Frontend, backend, and privacy

Checks that run in the browser are a convenience and are easy to skip, so repeat them on the server. Use synthetic data during development and keep real identifiers out of examples, screenshots, source, telemetry, and logs. Collect as little as you can, don't pass identifiers to unrelated third parties through this project, and follow the applicable law, privacy rules, and UIDAI requirements when real data is involved.

Verifying issuance or identity needs an authorised mechanism. UIDAI covers authentication and its conditions in the [Aadhaar Act](https://uidai.gov.in/en/aadhaar-act) and draws the line between authorised online authentication and offline digital-signature verification in its [19 June 2023 clarification](https://www.uidai.gov.in/images/resource/Authentication_Verification_of_Aadhaar_vide_file_no_10_22_2017_EG_II_Vol-I_dated_19_06_2023.pdf). This project does neither. Accessed 2026-10-16.
