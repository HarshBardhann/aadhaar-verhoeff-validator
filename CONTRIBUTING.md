# Contributing

Keep the line between local checksum validation and official verification clear. Don't add real Aadhaar numbers, UIDAI credentials, network lookups, identifier logging, or wording that calls a checksum-valid string genuine.

Run `python -m pytest`, `node --test integrations/javascript/verhoeff.test.js`, and `node integrations/javascript/example.js` before opening a change, and keep the Python and JavaScript test vectors in sync. GitHub Actions runs the same commands on every push and pull request. Use ASCII-only, synthetic test data. Aadhaar-format test vectors must start with a digit from 2 to 9, and any generic checksum example should be labelled as non-Aadhaar. Any documentation change should keep the limitation warning prominent and use the result labels **Format valid**, **Format invalid**, **Checksum valid**, and **Checksum invalid**.
