"use strict";

// Standard decimal Verhoeff tables: multiplication (D), permutation (P),
// inverse (INV). Indexed by digit 0-9.
const D = [[0,1,2,3,4,5,6,7,8,9],[1,2,3,4,0,6,7,8,9,5],[2,3,4,0,1,7,8,9,5,6],[3,4,0,1,2,8,9,5,6,7],[4,0,1,2,3,9,5,6,7,8],[5,9,8,7,6,0,4,3,2,1],[6,5,9,8,7,1,0,4,3,2],[7,6,5,9,8,2,1,0,4,3],[8,7,6,5,9,3,2,1,0,4],[9,8,7,6,5,4,3,2,1,0]];
const P = [[0,1,2,3,4,5,6,7,8,9],[1,5,7,6,2,8,3,0,9,4],[5,8,0,3,7,9,6,1,4,2],[8,9,1,6,0,4,3,5,2,7],[9,4,5,3,1,2,6,8,7,0],[4,2,8,6,5,7,3,9,0,1],[2,7,9,3,8,0,6,4,1,5],[7,0,4,6,9,1,3,2,5,8]];
const INV = [0,4,3,2,1,5,6,7,8,9];

const asciiDigits = (value) => typeof value === "string" && /^[0-9]+$/.test(value);

// Aadhaar-format rules, kept separate from the generic Verhoeff primitive.
const AADHAAR_LENGTH = 12;
const AADHAAR_FIRST_DIGITS = "23456789"; // UIDAI numbers never start with 0 or 1.

// Generic: any non-empty ASCII digit string, leading zeros included.
function verhoeffChecksumValid(number) {
  if (!asciiDigits(number)) return false;
  let check = 0;
  for (let i = 0; i < number.length; i++) {
    const digit = number.charCodeAt(number.length - 1 - i) - 48;
    check = D[check][P[i % 8][digit]];
  }
  return check === 0;
}

// Aadhaar format: exactly 12 ASCII digits, first digit 2-9, valid checksum.
function validateAadhaarChecksum(number) {
  return (
    typeof number === "string" &&
    number.length === AADHAAR_LENGTH &&
    AADHAAR_FIRST_DIGITS.includes(number[0]) &&
    asciiDigits(number) &&
    verhoeffChecksumValid(number)
  );
}

// Generic: exactly 11 ASCII digits, any leading digit. The result is a
// checksum, not an issued identifier.
function generateCheckDigit(first11) {
  if (typeof first11 !== "string" || first11.length !== 11 || !asciiDigits(first11)) {
    throw new Error("first11 must contain exactly 11 ASCII digits");
  }
  let check = 0;
  for (let i = 0; i < first11.length; i++) {
    const digit = first11.charCodeAt(first11.length - 1 - i) - 48;
    check = D[check][P[(i + 1) % 8][digit]];
  }
  return String(INV[check]);
}

module.exports = { verhoeffChecksumValid, validateAadhaarChecksum, generateCheckDigit };
