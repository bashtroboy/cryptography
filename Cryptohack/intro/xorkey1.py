#!/usr/bin/env python3

# You either know, XOR you don't

# I've encrypted the flag with my secret key, you'll never be able to guess it.

# Remember the flag format and how it might help you in this challenge!


# 0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104

# cipher = "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e"
# bcipher = bytes.fromhex(cipher)
# key = bytes.fromhex("10")

# boutput = ((c ^ key) for c in bcipher)

# print(*boutput)
from itertools import cycle 

cipher = "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"                           
bcipher = bytes.fromhex(cipher)                                                                                           
                                                                                                                            
# XOR ciphertext with known plaintext to get the key                                                                      
known = b"crypto{"                                                                                                        
#key = bytes([c ^ k for c, k in zip(bcipher, known)])  # produced anough of the key to guess the rest
key = b"myXORkey"                                                              
print(key)  # This reveals the repeating key

print(bytes([c ^ k for c, k in zip(bcipher, cycle(key))]).decode()) ## Solution is crypto{1f_y0u_Kn0w_En0uGH_y0u_Kn0w_1t_4ll}