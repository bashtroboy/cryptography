# Python Type Conversions Primer

## String to Integer

```python
# Basic conversion
int("42")          # 42

# With base specified
int("42", 10)      # 42 (base 10, decimal)
int("101", 2)      # 5  (base 2, binary)
int("77", 8)       # 63 (base 8, octal)
int("ff", 16)      # 255 (base 16, hex)
```

## Integer to String

```python
str(42)            # "42"
```

## Hexadecimal

```python
# Hex string to int
int("ff", 16)      # 255
int("0xff", 16)    # 255 (0x prefix works too)

# Int to hex string
hex(255)           # "0xff"
hex(255)[2:]       # "ff" (strip the 0x prefix)

# Format without 0x prefix
format(255, 'x')   # "ff"
format(255, 'X')   # "FF" (uppercase)
format(255, '04x') # "00ff" (zero-padded to 4 chars)
```

## Octal

```python
# Octal string to int
int("77", 8)       # 63
int("0o77", 8)     # 63 (0o prefix works too)

# Int to octal string
oct(63)            # "0o77"
oct(63)[2:]        # "77" (strip prefix)

# Format without prefix
format(63, 'o')    # "77"
```

## Binary

```python
# Binary string to int
int("1010", 2)     # 10
int("0b1010", 2)   # 10

# Int to binary string
bin(10)            # "0b1010"
bin(10)[2:]        # "1010"

# Format without prefix
format(10, 'b')    # "1010"
format(10, '08b')  # "00001010" (zero-padded to 8 bits)
```

## Bytes and Strings

```python
# String to bytes
"hello".encode()           # b'hello'
"hello".encode('utf-8')    # b'hello'

# Bytes to string
b'hello'.decode()          # "hello"
b'hello'.decode('utf-8')   # "hello"

# Bytes to hex string
b'hello'.hex()             # "68656c6c6f"

# Hex string to bytes
bytes.fromhex("68656c6c6f")  # b'hello'
```

## Character and ASCII/Ordinal (chr / ord)

These are essential for XOR operations on strings.

```python
# ord() - character to ASCII integer
ord('A')           # 65
ord('a')           # 97
ord('0')           # 48

# chr() - ASCII integer to character
chr(65)            # 'A'
chr(97)            # 'a'
chr(48)            # '0'

# Convert string to list of ASCII values
[ord(c) for c in "HELLO"]  # [72, 69, 76, 76, 79]

# Convert list of ASCII values back to string
''.join(chr(n) for n in [72, 69, 76, 76, 79])  # "HELLO"
```

### XOR with chr/ord

```python
# XOR a single character with an integer
char = 'l'
key = 13
result = chr(ord(char) ^ key)  # 'a'

# XOR an entire string with a key
plaintext = "label"
key = 13
ciphertext = ''.join(chr(ord(c) ^ key) for c in plaintext)  # "aloha"

# Common mistake: int('l') does NOT work!
# int('l')  # ValueError - use ord('l') instead
```

## Crypto-Specific: Long to Bytes

```python
from Crypto.Util.number import long_to_bytes, bytes_to_long

# Large int to bytes
long_to_bytes(310400273487)  # b'HELLO'

# Bytes to large int
bytes_to_long(b'HELLO')      # 310400273487
```

## Control Flow for Crypto

### For Loops

```python
# Loop over characters in a string
for char in "hello":
    print(char)  # h, e, l, l, o

# Loop over bytes (gives integers directly!)
for byte in b"hello":
    print(byte)  # 104, 101, 108, 108, 111

# Loop with index using enumerate
for i, char in enumerate("hello"):
    print(i, char)  # 0 h, 1 e, 2 l, ...

# Loop over a range of numbers
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

for i in range(65, 91):
    print(chr(i))  # A, B, C, ... Z

# range(stop)         - 0 to stop-1
# range(start, stop)  - start to stop-1
# range(start, stop, step)

for i in range(0, 10):       # 0, 1, 2, ... 9
    print(i)

for i in range(0, 10, 2):    # 0, 2, 4, 6, 8 (step by 2)
    print(i)

for i in range(10, 0, -1):   # 10, 9, 8, ... 1 (countdown)
    print(i)

for i in range(0, 256):      # all possible byte values
    print(i)

# Brute force all printable ASCII
for i in range(32, 127):
    print(chr(i))  # space through ~
```

### List Comprehensions (compact loops)

```python
# Transform each element
[ord(c) for c in "hello"]           # [104, 101, 108, 108, 111]
[chr(b ^ 13) for b in b"hello"]     # XOR each byte with 13
[c.upper() for c in "hello"]        # ['H', 'E', 'L', 'L', 'O']

# Filter elements
[c for c in "h3ll0" if c.isalpha()]  # ['h', 'l', 'l']
[x for x in range(20) if x % 2 == 0] # [0, 2, 4, 6, ...]
```

### Joining Results

```python
# Join list of strings into one string
''.join(['h', 'e', 'l', 'l', 'o'])   # "hello"
'-'.join(['a', 'b', 'c'])            # "a-b-c"

# Common pattern: transform and join
''.join(chr(ord(c) ^ 13) for c in "hello")  # XOR string with key

# Join bytes
bytes([104, 101, 108, 108, 111])     # b'hello'
```

### Zip (parallel iteration)

```python
# Loop over two sequences together
plaintext = "hello"
key = "keyke"
for p, k in zip(plaintext, key):
    print(p, k)  # h k, e e, l y, l k, o e

# XOR two strings together
''.join(chr(ord(p) ^ ord(k)) for p, k in zip(plaintext, key))
```

### Repeating a Key (cycling)

```python
from itertools import cycle

plaintext = "hello world"
key = "key"

# cycle() repeats the key forever: k, e, y, k, e, y, k, ...
result = ''.join(chr(ord(p) ^ ord(k)) for p, k in zip(plaintext, cycle(key)))
```

## Lists

### Creating Lists with list()

```python
# Convert string to list of characters
list("hello")           # ['h', 'e', 'l', 'l', 'o']

# Convert range to list
list(range(5))          # [0, 1, 2, 3, 4]

# Convert bytes to list of integers
list(b"hello")          # [104, 101, 108, 108, 111]

# Convert tuple to list
list((1, 2, 3))         # [1, 2, 3]

# Consume a generator
list(x * 2 for x in range(4))  # [0, 2, 4, 6]

# Create directly with brackets
[1, 2, 3]
['a', 'b', 'c']
```

### Reversing Lists

```python
my_list = [1, 2, 3, 4, 5]

# Slicing (returns new list)
my_list[::-1]           # [5, 4, 3, 2, 1]

# reversed() (returns iterator)
list(reversed(my_list)) # [5, 4, 3, 2, 1]

# .reverse() (modifies in place, returns None)
my_list.reverse()
print(my_list)          # [5, 4, 3, 2, 1]

# Also works on strings/bytes
"hello"[::-1]           # "olleh"
b"hello"[::-1]          # b"olleh"
```

### Checking if Value in List

```python
my_list = [10, 20, 30, 40]

# Check if value exists
if 20 in my_list:
    print("found")

# Check if not in list
if 50 not in my_list:
    print("not found")

# Works with strings
if "e" in "hello":      # True
if "z" in "hello":      # False
```

### Finding Index of Value

```python
my_list = [10, 20, 30, 40]

my_list.index(30)       # 2 (position of value)
my_list.index(99)       # ValueError if not found

# Safe way
if 30 in my_list:
    idx = my_list.index(30)

# Find all matching indices
my_list = [1, 2, 3, 2, 4, 2]
[i for i, x in enumerate(my_list) if x == 2]  # [1, 3, 5]
```

---

## Functions

### Default and Keyword Arguments

```python
def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}")

# Using default
greet("Alice")                    # "Hello, Alice"

# Override with positional argument
greet("Alice", "Hi")              # "Hi, Alice"

# Override with keyword argument
greet("Alice", greeting="Hi")     # "Hi, Alice"
```

**Keyword arguments** are useful when:
- More readable for complex function calls
- Skipping parameters to use defaults

```python
def func(a, b=1, c=2, d=3):
    print(a, b, c, d)

func(10)                # 10, 1, 2, 3 (all defaults)
func(10, 99)            # 10, 99, 2, 3 (override b)
func(10, d=99)          # 10, 1, 2, 99 (skip b and c, override d)
func(10, c=5, d=6)      # 10, 1, 5, 6 (skip b, override c and d)
```

**Example from AES S-box:**
```python
def sub_bytes(s, sbox=s_box):
    return [[sbox[byte] for byte in row] for row in s]

# Encrypt (use default s_box)
sub_bytes(state)

# Decrypt (override with inv_s_box)
sub_bytes(state, inv_s_box)          # positional
sub_bytes(state, sbox=inv_s_box)     # keyword (more readable)
```

---

## Quick Reference Table

| From | To | Method |
|------|-----|--------|
| str (decimal) | int | `int("42")` |
| str (hex) | int | `int("ff", 16)` |
| str (octal) | int | `int("77", 8)` |
| str (binary) | int | `int("1010", 2)` |
| int | str | `str(42)` |
| int | hex str | `hex(255)` or `format(255, 'x')` |
| int | octal str | `oct(63)` or `format(63, 'o')` |
| int | binary str | `bin(10)` or `format(10, 'b')` |
| str | bytes | `"hello".encode()` |
| bytes | str | `b'hello'.decode()` |
| bytes | hex str | `b'hello'.hex()` |
| hex str | bytes | `bytes.fromhex("68656c6c6f")` |
| char | int | `ord('A')` |
| int | char | `chr(65)` |
