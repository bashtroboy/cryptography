#!/usr/bin/env python3

# CryptoHack: Modular Inverting
# https://cryptohack.org/courses/modular/mdiv/
#
# Challenge: Find d such that 3 * d ≡ 1 (mod 13)
# This means: find the multiplicative inverse of 3 mod 13
#
# Method: Use Fermat's Little Theorem
#   a^(p-1) ≡ 1 (mod p)
#   a * a^(p-2) ≡ 1 (mod p)
#   Therefore: a^(p-2) is the modular inverse of a
#
# Solution: inverse of 3 = 3^(13-2) = 3^11 mod 13

a = 3
p = 13

inverse = pow(a, p - 2, p)
print(f"Inverse of {a} mod {p} = {inverse}")

# Verify
print(f"Verify: {a} * {inverse} mod {p} = {(a * inverse) % p}")