# Node.js implementation

> **Important limitation:** This module validates local format and Verhoeff checksum only. A checksum-valid string may be fabricated; it does not prove UIDAI issuance, an active record, or anyone's identity.

CommonJS module. Run the test suite with `node --test integrations/javascript/verhoeff.test.js`, and the demo with `node example.js`. It checks the shared synthetic Aadhaar-format vector: `23456789012` produces `4`, and `234567890124` is **Format valid** and **Checksum valid**. A generic string such as `123456789010` passes `verhoeffChecksumValid` but is rejected by `validateAadhaarChecksum` because it starts with 1 (UIDAI numbers never start with 0 or 1). Browser-side validation is fine for quick feedback but can be skipped, so repeat it on the server. Nothing here verifies UIDAI issuance or identity.
