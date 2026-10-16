# FAQ

## Does "Checksum valid" mean the number is genuine?

No. It means the input is 12 ASCII digits and passes Verhoeff. It says nothing about UIDAI issuance or identity.

## Why reject spaces, hyphens, and Unicode digits?

The API takes exactly 12 ASCII digits and does not trim, strip, reformat, or transliterate anything. Rejecting malformed input outright avoids ambiguity at the validation boundary.

## Is any real identifier sent anywhere?

No. Everything runs locally with no dependencies. The CLI does not store input or send it anywhere. Passing a value on the command line can still leave it in your shell history, which is why interactive entry is the default.

## Can I use this for production authentication?

No. Treat it as an input-quality check. If your use case really needs verification or authentication, use an authorised mechanism.
