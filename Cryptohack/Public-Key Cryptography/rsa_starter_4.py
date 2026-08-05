#!/usr/bin/env python3

"""
The private key d is used to decrypt ciphertexts created with the corresponding public key (it's also used to "sign" a message but we'll get to that later).

The private key is the secret piece of information, or "trapdoor", which allows us to quickly invert the encryption function. If RSA is implemented well, if you do not have the private key the fastest way to decrypt the ciphertext is to factorise the modulus which is very hard to do for large integers.

In RSA, the private key is the modular multiplicative inverse of the exponent e modulo ϕ(N), Euler's totient of N.
"""

p = 857504083339712752489993810777
q = 1029224947942998075080348647219
e = 65537

c = 77578995801157823671636298847186723593814843845525223303932

phi_N = ((p-1) * (q-1))

# Find private key d

d = pow(e, -1, phi_N)

print(d)

# Now decrypt

N = 882564595536224140639625987659416029426239230804614613279163

m = pow(c, d, N)
print(m)