"use strict";
const { generateCheckDigit, validateAadhaarChecksum, verhoeffChecksumValid } = require("./verhoeff");
const prefix = "23456789012";                 // synthetic, first digit 2-9
const synthetic = prefix + generateCheckDigit(prefix);
console.assert(synthetic === "234567890124");
console.assert(validateAadhaarChecksum(synthetic));
console.assert(!validateAadhaarChecksum("234567890125")); // wrong check digit
console.assert(!validateAadhaarChecksum("243567890124")); // adjacent 3/4 swap
// "123456789010" passes Verhoeff in general but leading 1 is not Aadhaar format.
console.assert(verhoeffChecksumValid("123456789010"));
console.assert(!validateAadhaarChecksum("123456789010"));
console.log("Format valid: true");
console.log("Checksum valid: true");
console.log("Synthetic only; UIDAI issuance and identity were not verified.");
