#!/usr/bin/env python3

# Euclidean Algorithm:
# To find GCD of two numbers, repeatedly replace the larger with (larger % smaller)
# until one becomes 0. The other number is the GCD.
#
# Formula: gcd(a, b) = gcd(b, a % b) until b = 0, then answer is a
#
# Example: gcd(66528, 52920)
#   gcd(66528, 52920) → gcd(52920, 13608)
#   gcd(52920, 13608) → gcd(13608, 12096)
#   gcd(13608, 12096) → gcd(12096, 1512)
#   gcd(12096, 1512)  → gcd(1512, 0)
#   Answer: 1512

#   Or just use Python's built-in:                                                                                            
#   import math                                                                                                               
#   print(math.gcd(66528, 52920))   

# Now calculate gcd(a,b) for a = 66528, b = 52920 and enter it below.

a = 66528
b = 52920

def gcd(x,y):
    if y == 0:
        return x
    else: 
        return gcd(y, (x % y))

print(gcd(a,b))