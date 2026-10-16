"use strict";
const assert = require("node:assert/strict");
const { generateCheckDigit, validateAadhaarChecksum, verhoeffChecksumValid } = require("./verhoeff");

const prefix = "23456789012"; // synthetic, first digit 2-9
const synthetic = prefix + generateCheckDigit(prefix);

assert.equal(synthetic, "234567890124");
assert.equal(validateAadhaarChecksum(synthetic), true);
assert.equal(validateAadhaarChecksum("234567890125"), false); // wrong check digit
assert.equal(validateAadhaarChecksum("243567890124"), false); // adjacent 3/4 swap
// "123456789010" passes Verhoeff in general but leading 1 is not Aadhaar format.
assert.equal(verhoeffChecksumValid("123456789010"), true);
assert.equal(validateAadhaarChecksum("123456789010"), false);

console.log("Format valid: true");
console.log("Checksum valid: true");
console.log("Synthetic only; UIDAI issuance and identity were not verified.");
