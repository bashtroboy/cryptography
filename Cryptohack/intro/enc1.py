#!/usr/bin/env python3

# https://cryptohack.org/courses/intro/enc1/

# ASCII is a 7-bit encoding standard which allows the representation of text using the integers 0-127.

# Using the below integer array, convert the numbers to their corresponding ASCII characters to obtain a flag.

# [99, 114, 121, 112, 116, 111, 123, 65, 83, 67, 73, 73, 95, 112, 114, 49, 110, 116, 52, 98, 108, 51, 125]

#  In Python, the chr() function can be used to convert an ASCII ordinal number to a character (the ord() function does the opposite).

import sys
# import this

if sys.version_info.major == 2:
    print("You are running Python 2, which is no longer supported. Please update to Python 3.")

ords = [99, 114, 121, 112, 116, 111, 123, 65, 83, 67, 73, 73, 95, 112, 114, 49, 110, 116, 52, 98, 108, 51, 125]

print("Here is your flag:")
print("".join(chr(o) for o in ords))