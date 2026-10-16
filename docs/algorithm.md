# The Verhoeff algorithm

A checksum is a small value derived from a longer piece of data. Its job is to catch mistakes like a dropped or mistyped digit. It is not a signature, a password, or any proof about where the data came from. Verhoeff is a decimal check-digit scheme built on the dihedral group D5. A permutation that depends on the digit's position is what sets it apart from simple weighted-sum schemes: in the standard decimal version it catches every single-digit substitution and every swap of two adjacent, unequal digits. It does not catch every possible multi-digit change, and it is no obstacle to someone who works out a matching digit on purpose.

The tables come from the standard Verhoeff definition: multiplication (`D`), permutation (`P`), and inverse (`INV`). They live as literal data in [`src/aadhaar_validator/verhoeff.py`](../src/aadhaar_validator/verhoeff.py) instead of being copied into this file, because retyping 100 table cells is a good way to introduce an error. In short: `D[a][b]` combines two values, `P[position mod 8][digit]` permutes a digit, and `INV[c]` gives the digit that brings accumulator `c` back to zero.

## Checking a number

Walk the digits from right to left. Start with `c = 0`, and for each digit at zero-based position `i` from the right, do `c = D[c][P[i mod 8][digit]]`. The string is **Checksum valid** when the final `c` is `0`.

Take the widely used generic example `2363` (not Aadhaar data). Reading right to left gives `3, 6, 3, 2`; the permuted values are `3, 3, 3, 1`; and the accumulator moves `0 -> 3 -> 1 -> 4 -> 0`. It ends at zero, so the string is valid.

## Generating the check digit

When you have the first eleven digits and need the twelfth, the loop changes. Read right to left and use `P[(i + 1) mod 8]`, then return `INV[c]`. That one-position shift matters; generation is not the validation loop reused as-is. For example, the generic prefix `12345678901` yields `0`, giving the generic string `123456789010`. For any fixed eleven digits, exactly one of the ten possible final digits works, which is why roughly 10% of uniformly random 12-digit strings pass if you ignore other constraints.

Generation is generic and says nothing about Aadhaar format. The Aadhaar-format check in this repo adds one rule on top of the checksum: the first digit must be 2 through 9, because UIDAI numbers never start with 0 or 1. So `123456789010` is checksum-valid but not an Aadhaar-format number, while `23456789012` plus the generated `4` gives the synthetic Aadhaar-format example `234567890124`.

The [Verhoeff page on Wikipedia](https://en.wikipedia.org/wiki/Verhoeff_algorithm) lists the tables, the `236 -> 3` example, and the error-detection properties. The original work is J. Verhoeff, *Error Detecting Decimal Codes* (1969), DOI [10.1002/zamm.19710510323](https://doi.org/10.1002/zamm.19710510323). Accessed 2026-10-16.

Passing this test says nothing about whether UIDAI issued the number.
