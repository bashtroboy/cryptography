#!/usr/bin/env python3

# Favorte Key
# For the next few challenges, you'll use what you've just learned to solve some more XOR puzzles.

# I've hidden some data using XOR with a single byte, but that byte is a secret. Don't forget to decode from hex first.

# 73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d

cipher = "73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d"

bcipher = bytes.fromhex(cipher)

for i in range(0, 256):
    #print(bytes.fromhex(hex(j ^ i for j in bcipher)[2:]))
   
   boutput = ((c ^ i) for c in bcipher)
   print(''.join(chr(n) for n in boutput))
   print(" ****************")
