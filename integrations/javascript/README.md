# Node.js implementation

CommonJS module. Run `node example.js`. It checks the shared synthetic Aadhaar-format vector: `23456789012` produces `4`, and `234567890124` is **Format valid** and **Checksum valid**. A generic string such as `123456789010` passes `verhoeffChecksumValid` but is rejected by `validateAadhaarChecksum` because it starts with 1 (UIDAI numbers never start with 0 or 1). Browser-side validation is fine for quick feedback but can be skipped, so repeat it on the server. Nothing here verifies UIDAI issuance or identity.
