# FAQ

## Does "Checksum valid" mean the number is genuine?

No. It means the input is 12 ASCII digits with a first digit from 2 to 9 and passes Verhoeff. It says nothing about UIDAI issuance or identity.

## Why must the first digit be 2-9?

UIDAI Aadhaar numbers never start with 0 or 1, so `validate_aadhaar_checksum` rejects those even when the Verhoeff checksum is correct. `verhoeff_checksum_valid` and `generate_check_digit` stay generic and accept any ASCII digits, so leading zeros still work for non-Aadhaar uses.

## Why reject spaces, hyphens, and Unicode digits?

The API takes exactly 12 ASCII digits (first digit 2-9) and does not trim, strip, reformat, or transliterate anything. Rejecting malformed input outright avoids ambiguity at the validation boundary.

## Is any real identifier sent anywhere?

No. Everything runs locally with no dependencies. The CLI does not store input or send it anywhere. Passing a value on the command line can still leave it in your shell history, which is why interactive entry is the default.

## Can I use this for production authentication?

No. Treat it as an input-quality check. If your use case really needs verification or authentication, use an authorised mechanism.
