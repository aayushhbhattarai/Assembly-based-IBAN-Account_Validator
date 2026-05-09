# RISC-V IBAN Calculator

A university project from my Bachelor's degree in the course **Programming 2** at Saarland University.

## About the Project

This project implements a German IBAN calculator written entirely in **RISC-V assembly**. It can convert a bank account number (KNR) and bank code (BLZ) into a valid German IBAN, and also extract the KNR and BLZ back from a given IBAN.

A German IBAN follows this structure:

```
D E P P B B B B B B B B K K K K K K K K K K
│ │ │ │ └─────────────┘ └─────────────────┘
│ │ └─┘      BLZ (8)          KNR (10)
│ │ Check digits
└─┘ Country code
```

## What's Implemented

- **`iban2knr.s`** — Extracts the BLZ and KNR from a given 22-character German IBAN.
- **`moduloStr.s`** — Calculates the remainder of a large number (given as a string) divided by a divisor, using Horner's method to handle numbers that exceed register size.
- **`validateChecksum.s`** — Validates the check digits of a German IBAN by rearranging the IBAN, substituting letters with numbers (A=10, ..., Z=35), and computing the result modulo 97. A valid IBAN yields a remainder of 1.
- **`knr2iban.s`** — Generates a complete German IBAN with valid check digits from a given BLZ and KNR.
- **`util.s`** — Utility subroutines provided by the course (memory copy, print, read, etc.).
- **`main.s`** — Entry point of the program.

## How It Works

### Generating an IBAN
1. A temporary IBAN is built with check digits set to `"00"`.
2. The checksum validation function is run on it to get the remainder.
3. The real check digits are computed as `98 - remainder`.
4. The final IBAN is assembled and written to the output buffer.

### Validating a Checksum
1. The first four characters of the IBAN are moved to the end.
2. Any letters are replaced by their numeric equivalents (A=10, B=11, ...).
3. The resulting number string is divided by 97; the remainder is the checksum.

## Built With

- RISC-V Assembly
- [Venus RISC-V Simulator](https://github.com/kvakil/venus)
