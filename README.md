# Cryptography Learning Notes

Personal notes and solutions from learning cryptography through CTF challenges, primarily from [CryptoHack](https://cryptohack.org) and [Hack The Box](https://hackthebox.com).

---

## Contents

### CryptoHack Courses

| Course | Topics | Status |
|--------|--------|--------|
| [Symmetric Cryptography](Cryptohack/Symmetric%20Cryptography/readme.md) | AES internals, block cipher modes, CBC/CTR/OFB attacks | In Progress |
| [Public-Key Cryptography](Cryptohack/Public-Key%20Cryptography/readme.md) | RSA, Euler's theorem, modular arithmetic, factoring attacks | In Progress |

### Other Resources

| File | Description |
|------|-------------|
| [Python Type Conversions](python_type_conversions.md) | Quick reference for bytes, hex, int, chr/ord conversions |
| [CTF Solutions Log](ctf_solutions_log.md) | Flags and solution notes for completed challenges |
| [Hack The Box - Basic Tools](Hack%20the%20Box/Basic%20Tools.md) | SSH, Netcat, Tmux, Vim essentials |

---

## Quick Reference

### Python Essentials for Crypto

```python
# Hex ↔ Bytes
bytes.fromhex("deadbeef")      # hex string → bytes
b'\xde\xad'.hex()              # bytes → hex string

# Int ↔ Bytes (for RSA)
from Crypto.Util.number import long_to_bytes, bytes_to_long
long_to_bytes(12345)           # int → bytes
bytes_to_long(b'hello')        # bytes → int

# Character ↔ Int (for XOR)
ord('A')                       # char → int (65)
chr(65)                        # int → char ('A')

# Modular arithmetic
pow(base, exp, mod)            # base^exp mod m
pow(e, -1, phi_n)              # modular inverse (Python 3.8+)

# Mutable bytes for in-place modification
data = bytearray(b'\x00\x01\x02')
data[0] = 0xff                 # works (bytearray is mutable)
```

### RSA Cheat Sheet

```python
# Setup
N = p * q                      # modulus
phi_N = (p - 1) * (q - 1)      # Euler's totient
e = 65537                      # public exponent (standard)
d = pow(e, -1, phi_N)          # private exponent

# Operations
c = pow(m, e, N)               # encrypt
m = pow(c, d, N)               # decrypt
sig = pow(hash, d, N)          # sign
hash = pow(sig, e, N)          # verify
```

### Block Cipher Mode Attacks

| Mode | Attack | Exploit |
|------|--------|---------|
| ECB | Byte-at-a-time | Known prefix + brute force each byte |
| CBC | Bit-flipping | `new_iv[i] = iv[i] ^ old[i] ^ new[i]` |
| CBC | Padding oracle | Leak plaintext via padding errors |
| OFB | Symmetric | Encrypt ciphertext with same IV = plaintext |
| CTR | Keystream reuse | Counter bug → XOR with known plaintext header |

### XOR Properties

```
A ^ A = 0           (self-inverse)
A ^ 0 = A           (identity)
A ^ B = B ^ A       (commutative)
(A ^ B) ^ C = A ^ (B ^ C)  (associative)

# If C = A ^ B, then:
A = C ^ B
B = C ^ A
```

---

## Tools & Setup

### Python Libraries

```bash
pip install pycryptodome requests
```

```python
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Util.Padding import pad, unpad
```

### Useful Commands

```bash
# Hex encode/decode
echo -n "hello" | xxd -p          # text → hex
echo "68656c6c6f" | xxd -r -p     # hex → text

# Base64
echo -n "hello" | base64          # encode
echo "aGVsbG8=" | base64 -d       # decode

# OpenSSL
openssl enc -aes-128-ecb -K <key_hex> -in file
openssl rsa -in key.pem -text     # inspect RSA key
```

---

## Key Theorems

### Euler's Theorem
If gcd(a, n) = 1:
```
a^φ(n) ≡ 1 (mod n)
```
This is why RSA decryption works: `m^(ed) = m^(1 + k·φ(N)) = m`

### Fermat's Little Theorem
If p is prime and gcd(a, p) = 1:
```
a^(p-1) ≡ 1 (mod p)
```
Used for modular inverse: `a^(-1) ≡ a^(p-2) (mod p)`

### Euler's Totient φ(n)
- `φ(p) = p - 1` for prime p
- `φ(p·q) = (p-1)(q-1)` for distinct primes
- Counts integers 1..n coprime to n

---

## Learning Path

1. **Introduction** - XOR properties, encoding, basic math
2. **Symmetric Cryptography** - AES, block cipher modes, stream ciphers
3. **Public-Key Cryptography** - RSA, Diffie-Hellman, discrete log
4. **Elliptic Curves** - ECC fundamentals (future)
5. **Hash Functions** - SHA, MD5, length extension (future)

---

## Resources

### Courses & Challenges
- [CryptoHack](https://cryptohack.org) - Interactive crypto challenges
- [Hack The Box](https://hackthebox.com) - Penetration testing labs
- [PicoCTF](https://picoctf.org) - Beginner-friendly CTF

### References
- [CryptoPals](https://cryptopals.com) - Classic crypto challenges
- [A Graduate Course in Applied Cryptography](https://toc.cryptobook.us/) - Boneh & Shoup (free textbook)
- [PyCryptodome Docs](https://pycryptodome.readthedocs.io/)

### Tools
- [CyberChef](https://gchq.github.io/CyberChef/) - Swiss army knife for encoding/crypto
- [dCode](https://www.dcode.fr/en) - Cipher identification and solving
- [FactorDB](http://factordb.com/) - Integer factorization database
