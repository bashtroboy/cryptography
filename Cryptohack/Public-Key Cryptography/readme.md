# Public-Key Cryptography - CryptoHack Notes

## Course Overview

https://cryptohack.org/courses/public-key/course_details/

Whitfield Diffie and Martin Hellman's 1976 paper "New Directions in Cryptography" heralded a huge leap forward for the field of cryptography. The paper defined the concepts of public-key cryptosystems, one-way trapdoor functions, and digital signatures, and described a key-exchange method for securely sharing secrets over an insecure channel.

Public key encryption enables a user, Alice, to distribute a public key and others can use that public key to encrypt messages to her. Alice can then use her private key to decrypt the messages.

Digital signatures enable Alice to use her private key to "sign" a message. Anyone can use Alice's public key to verify that the signature was created with her corresponding private key, and that the message hasn't been tampered with.

RSA's security is based on the difficulty of factoring large composite numbers. Major flaws have been found in common deployments, the most notorious being the ROCA vulnerability which led to Estonia suspending 760,000 national ID cards.

---

## RSA Fundamentals

### Key Generation
1. Choose two large prime numbers: `p` and `q`
2. Compute modulus: `N = p * q`
3. Compute Euler's totient: `φ(N) = (p-1) * (q-1)`
4. Choose public exponent: `e` (commonly 65537 or 0x10001)
5. Compute private exponent: `d = e⁻¹ mod φ(N)` (modular inverse)

**Public key:** `(N, e)`
**Private key:** `(N, d)` or `(p, q, d)`

### Encryption & Decryption
```python
# Encrypt: ciphertext = message^e mod N
ciphertext = pow(message, e, N)

# Decrypt: message = ciphertext^d mod N
message = pow(ciphertext, d, N)
```

---

## Challenge Solutions

### RSA Starter 2 - Encryption
**Task:** Encrypt the number 12 using e=65537, p=17, q=23

```python
p = 17
q = 23
N = p * q          # N = 391
e = 65537
message = 12

ciphertext = pow(message, e, N)
print(ciphertext)  # Answer: 301
```

**Key concept:** RSA encryption is just modular exponentiation.

### RSA Starter 4 - Private Key
**Task:** Find private key d given p, q, and e

```python
p = 857504083339712752489993810777
q = 1029224947942998075080348647219
e = 65537

phi_N = (p - 1) * (q - 1)
d = pow(e, -1, phi_N)  # Modular inverse
print(d)
```

**Key concept:** The private key `d` is the modular inverse of `e` mod `φ(N)`.

**Common mistake:** `e ** -1` computes `1/e` (float), NOT the modular inverse. Use `pow(e, -1, phi_N)`.

### RSA Starter 5 - Decryption
**Task:** Decrypt ciphertext using private key

```python
c = 77578995801157823671636298847186723593814843845525223303932
N = p * q
m = pow(c, d, N)
print(m)
```

---

## Euler's Totient Function φ(n)

### What is it?
Euler's totient function `φ(n)` counts the number of integers from 1 to n that are **coprime** to n (i.e., share no common factors with n other than 1).

### Examples
```
φ(1)  = 1           # {1}
φ(6)  = 2           # {1, 5} - only 1 and 5 share no factors with 6
φ(7)  = 6           # {1,2,3,4,5,6} - 7 is prime, so all smaller numbers work
φ(10) = 4           # {1, 3, 7, 9}
φ(15) = 8           # {1, 2, 4, 7, 8, 11, 13, 14}
```

### Key Formulas

**For a prime p:**
```
φ(p) = p - 1
```
All numbers less than a prime are coprime to it.

**For two distinct primes p and q:**
```
φ(p * q) = (p - 1) * (q - 1)
```
This is why RSA uses two primes!

**For a prime power:**
```
φ(p^k) = p^k - p^(k-1) = p^(k-1) * (p - 1)
```

### Python Implementation
```python
def euler_totient(n):
    """Compute φ(n) by counting coprimes"""
    from math import gcd
    count = 0
    for i in range(1, n + 1):
        if gcd(i, n) == 1:
            count += 1
    return count

# For RSA with known primes (much faster):
def euler_totient_rsa(p, q):
    return (p - 1) * (q - 1)
```

---

## Euler's Theorem

### The Theorem
If `a` and `n` are coprime (gcd(a,n) = 1), then:

```
a^φ(n) ≡ 1 (mod n)
```

### Why it matters for RSA
This is the mathematical foundation that makes RSA decryption work.

**The RSA relationship:**
```
e * d ≡ 1 (mod φ(N))
```
This means: `e * d = 1 + k * φ(N)` for some integer k.

**Why decryption works:**
```
ciphertext^d = (message^e)^d
             = message^(e*d)
             = message^(1 + k*φ(N))
             = message * (message^φ(N))^k
             = message * 1^k          # By Euler's theorem!
             = message (mod N)
```

### Example
```python
# If p=17, q=23, then N=391 and φ(N)=352
# For any message m coprime to N:
# m^352 ≡ 1 (mod 391)

m = 12
N = 391
phi_N = 352

print(pow(m, phi_N, N))  # Outputs: 1
```

---

## Fermat's Little Theorem (Special Case)

When `p` is prime and `a` is not divisible by `p`:
```
a^(p-1) ≡ 1 (mod p)
```

This is a special case of Euler's theorem since `φ(p) = p - 1` for prime `p`.

**Using it to find modular inverse:**
```python
# inverse of a mod p = a^(p-2) mod p
inverse = pow(a, p - 2, p)
```

---

## Euclidean Algorithm (GCD)

Finds the greatest common divisor of two numbers.

```
gcd(a, b) = gcd(b, a % b)  until b = 0, then answer is a
```

**Example:**
```
gcd(66528, 52920)
  → gcd(52920, 13608)
  → gcd(13608, 12096)
  → gcd(12096, 1512)
  → gcd(1512, 0)
  = 1512
```

**Python:** `from math import gcd` or `math.gcd(a, b)`

---

## Extended Euclidean Algorithm (EGCD)

Finds gcd(a, b) AND integers u, v satisfying Bézout's identity:

```
a*u + b*v = gcd(a, b)
```

**Why it matters:** When gcd(a, b) = 1, then u is the modular inverse of a mod b. Essential for RSA.

```python
def egcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        gcd, u1, v1 = egcd(b, a % b)
        u = v1
        v = u1 - (a // b) * v1
        return gcd, u, v

# Example: find inverse of 3 mod 11
gcd, u, v = egcd(3, 11)
# gcd=1, u=4 (so 3*4 = 12 ≡ 1 mod 11)
```

---

## Modular Inverse

### What is it?
The modular inverse of `a` modulo `n` is a number `x` such that:
```
a * x ≡ 1 (mod n)
```
Written as: `x = a⁻¹ mod n`

### When does it exist?
Only when `gcd(a, n) = 1` (a and n are coprime).

### Computing in Python
```python
# Python 3.8+ (preferred)
d = pow(e, -1, phi_N)

# Or using extended Euclidean algorithm
def mod_inverse(a, n):
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    _, x, _ = extended_gcd(a % n, n)
    return (x % n + n) % n
```

---

## Common RSA Attacks

| Attack | Condition |
|--------|-----------|
| Small e, small m | If `m^e < N`, ciphertext doesn't wrap, just take e-th root |
| Common modulus | Same N with different e values leaks plaintext |
| Wiener's attack | d is too small relative to N |
| Factoring N | If you can factor N, you can compute φ(N) and find d |
| Shared prime | Two moduli share a prime factor - find it with GCD |

---

## Quick Reference

```python
# RSA Setup
p, q = large_primes
N = p * q
phi_N = (p - 1) * (q - 1)
e = 65537
d = pow(e, -1, phi_N)

# Encrypt
c = pow(m, e, N)

# Decrypt
m = pow(c, d, N)

# Sign
signature = pow(hash, d, N)

# Verify
hash = pow(signature, e, N)
```
