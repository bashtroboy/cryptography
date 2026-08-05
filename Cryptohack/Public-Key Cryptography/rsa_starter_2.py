#!/usr/bin/env python3

"""
RSA encryption is modular exponentiation of a message with an exponent e and modulus N, 
where N is a product of two primes, p and q

Together, the exponent and modulus in RSA make a public key

    number ^ e MOD (p * q)

"""

e = 65537
p = 17
q = 23

x = 12

print((x ** 65537) % (p*q))

# or

print(pow(12, e, (p*q)))