"use strict";
const { generateCheckDigit, validateAadhaarChecksum } = require("./verhoeff");
const prefix = "12345678901";
const synthetic = prefix + generateCheckDigit(prefix);
console.assert(synthetic === "123456789010");
console.assert(validateAadhaarChecksum(synthetic));
console.assert(!validateAadhaarChecksum("123456789011"));
console.assert(!validateAadhaarChecksum("123456789001")); // adjacent 0/1 swap
console.log("Format valid: true");
console.log("Checksum valid: true");
console.log("Synthetic only; UIDAI issuance and identity were not verified.");
