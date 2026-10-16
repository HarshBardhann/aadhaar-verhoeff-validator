"use strict";

// Node.js test suite (run with: node --test integrations/javascript/verhoeff.test.js).
// Uses the built-in node:test runner and node:assert, so there are no dependencies.
const test = require("node:test");
const assert = require("node:assert/strict");

const {
  generateCheckDigit,
  validateAadhaarChecksum,
  verhoeffChecksumValid,
} = require("./verhoeff");

// Aadhaar-format synthetic vector: 12 digits, first digit 2-9.
const SYNTHETIC_PREFIX = "23456789012";
const SYNTHETIC_NUMBER = "234567890124"; // Generated locally; never an issuance claim.

// Generic, checksum-valid strings that are NOT Aadhaar-format (leading 0 or 1).
const GENERIC_PREFIX = "12345678901";
const GENERIC_NUMBER = "123456789010";

test("known generic Verhoeff reference vector", () => {
  // 2363 is a commonly published generic Verhoeff example (not Aadhaar data).
  assert.equal(verhoeffChecksumValid("2363"), true);
  assert.equal(verhoeffChecksumValid("2364"), false);
});

test("generated synthetic Aadhaar vector is stable", () => {
  assert.equal(generateCheckDigit(SYNTHETIC_PREFIX), "4");
  assert.equal(SYNTHETIC_NUMBER, SYNTHETIC_PREFIX + generateCheckDigit(SYNTHETIC_PREFIX));
  assert.equal(verhoeffChecksumValid(SYNTHETIC_NUMBER), true);
  assert.equal(validateAadhaarChecksum(SYNTHETIC_NUMBER), true);
});

test("Aadhaar format accepts leading digits 2 through 9", () => {
  for (const firstDigit of "23456789") {
    const prefix = firstDigit + "0000000000"; // 11 digits
    const complete = prefix + generateCheckDigit(prefix);
    assert.equal(complete.length, 12);
    assert.equal(complete[0], firstDigit);
    assert.equal(validateAadhaarChecksum(complete), true);
  }
});

test("Aadhaar format rejects leading zero or one even when checksum is valid", () => {
  for (const value of ["000000000003", GENERIC_NUMBER]) {
    assert.equal(verhoeffChecksumValid(value), true);
    assert.equal(validateAadhaarChecksum(value), false);
  }
});

test("generic generator and validator stay generic", () => {
  assert.equal(generateCheckDigit("00000000000"), "3");
  assert.equal(generateCheckDigit(GENERIC_PREFIX), "0");
  assert.equal(verhoeffChecksumValid("000000000003"), true);
  assert.equal(verhoeffChecksumValid(GENERIC_NUMBER), true);
  assert.equal(validateAadhaarChecksum("000000000003"), false);
  assert.equal(validateAadhaarChecksum(GENERIC_NUMBER), false);
});

test("Aadhaar format rejects malformed values", () => {
  const malformed = [
    "",
    "123",
    SYNTHETIC_NUMBER + "0", // 13 digits
    SYNTHETIC_NUMBER.slice(0, 11) + "X", // non-digit
    "234567890 24", // embedded space
    "23456789012-", // embedded hyphen
    "२३४५६७८९०१२४", // non-ASCII (Devanagari) digits
  ];
  for (const value of malformed) {
    assert.equal(validateAadhaarChecksum(value), false);
  }
});

test("validators reject non-strings", () => {
  for (const value of [null, undefined, 123456789012, [], {}]) {
    assert.equal(verhoeffChecksumValid(value), false);
    assert.equal(validateAadhaarChecksum(value), false);
  }
});

test("single-digit substitution is detected", () => {
  const changed = SYNTHETIC_NUMBER.slice(0, 5) + "0" + SYNTHETIC_NUMBER.slice(6);
  assert.notEqual(changed, SYNTHETIC_NUMBER);
  assert.equal(validateAadhaarChecksum(changed), false);
});

test("adjacent unequal-digit transposition is detected", () => {
  const swapped =
    SYNTHETIC_NUMBER.slice(0, 1) + SYNTHETIC_NUMBER[2] + SYNTHETIC_NUMBER[1] + SYNTHETIC_NUMBER.slice(3);
  assert.notEqual(swapped, SYNTHETIC_NUMBER);
  assert.equal(validateAadhaarChecksum(swapped), false);
});

test("invalid check digit is detected", () => {
  const invalid = SYNTHETIC_NUMBER.slice(0, 11) + "5";
  assert.notEqual(invalid, SYNTHETIC_NUMBER);
  assert.equal(validateAadhaarChecksum(invalid), false);
});

test("generator rejects invalid arguments", () => {
  const bad = ["1234567890", "123456789012", "1234567890X", "１２３４５６７８９０１", 12345678901];
  for (const value of bad) {
    assert.throws(() => generateCheckDigit(value), /exactly 11 ASCII digits/);
  }
});
