#!/usr/bin/dev python3

# Imagine you lean over and look at a cryptographer's notebook. You see some notes in the margin:

# 4 + 9 = 1
# 5 - 7 = 10
# 2 + 3 = 5

# At first you might think they've gone mad. Maybe this is why there are so many data leaks nowadays you'd think, but this is nothing more than modular arithmetic modulo 12 (albeit with some sloppy notation).

# You may not have been calling it modular arithmetic, but you've been doing these kinds of calculations since you learnt to tell the time (look again at those equations and think about adding hours).

# Formally, "calculating time" is described by the theory of congruences.

# Find the integers x and y
# 11 ≡ x mod 6
# 8146798528947 ≡ y mod 17

x = 11 % 6
y = 8146798528947 % 17

print(min(x, y))