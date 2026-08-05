# Symmetric Cryptography - CryptoHack Notes

## Overview

Symmetric-key ciphers use the same key to encrypt and decrypt data. The goal is to use short secret keys to securely and efficiently send long messages.

**Two types:**
- **Block ciphers** - encrypt fixed-size blocks (e.g., AES)
- **Stream ciphers** - encrypt one byte at a time via XOR with keystream

AES (Advanced Encryption Standard) is the most widely used symmetric cipher, standardized in 2001. Modern processors include dedicated AES instruction sets.

---

## Challenge Solutions

### 1. Keyed Permutations
**Answer:** `bijection`

AES performs a "keyed permutation" - maps every input block to a unique output block. A one-to-one correspondence is called a **bijection**.

### 2. Resisting Bruteforce
**Answer:** `biclique`

The biclique attack reduces AES-128 security from 128 bits to 126.1 bits - theoretically "breaks" AES but is completely impractical.

**Quantum impact:** Grover's algorithm halves security (AES-128 → 64-bit effective). This is why AES-256 is recommended for quantum resistance (retains 128-bit security).

### 3. Structure of AES
**Task:** Implement `matrix2bytes` function

```python
def matrix2bytes(matrix):
    return bytes([byte for row in matrix for byte in row])
```

### 4. Round Keys
**Task:** Implement `add_round_key` function

```python
def add_round_key(s, k):
    return [[s[i][j] ^ k[i][j] for j in range(4)] for i in range(4)]
```

### 5. Confusion through Substitution (S-box)
**Task:** Implement `sub_bytes` with inverse S-box

```python
def sub_bytes(s, sbox=s_box):
    return [[sbox[byte] for byte in row] for row in s]

# Usage for decryption:
state = sub_bytes(state, sbox=inv_s_box)
```

### 6. Diffusion through Permutation
**Task:** Implement `inv_shift_rows`

```python
def inv_shift_rows(s):
    s[1][1], s[2][1], s[3][1], s[0][1] = s[0][1], s[1][1], s[2][1], s[3][1]
    s[2][2], s[3][2], s[0][2], s[1][2] = s[0][2], s[1][2], s[2][2], s[3][2]
    s[3][3], s[0][3], s[1][3], s[2][3] = s[0][3], s[1][3], s[2][3], s[3][3]
```

### 7. Bringing It All Together
**Task:** Implement full AES decryption

See `aes6.py` for complete implementation.

---

## AES Structure

### State Matrix (Column-Major)

16 bytes arranged in a 4x4 matrix, filled column by column:

```
Input: b0 b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 b14 b15

State:
┌────┬────┬────┬────┐
│ b0 │ b4 │ b8 │b12 │
│ b1 │ b5 │ b9 │b13 │
│ b2 │ b6 │b10 │b14 │
│ b3 │ b7 │b11 │b15 │
└────┴────┴────┴────┘
```

### Encryption Flow

```
KeyExpansion: Generate 11 round keys from 128-bit key

AddRoundKey (initial, with round_keys[0])

For rounds 1-9:
    SubBytes      (confusion via S-box)
    ShiftRows     (diffusion)
    MixColumns    (diffusion)
    AddRoundKey

Final round 10 (no MixColumns):
    SubBytes
    ShiftRows
    AddRoundKey
```

### Decryption Flow (Reverse Order)

```
AddRoundKey (with round_keys[10])

For rounds 9-1:
    InvShiftRows
    InvSubBytes
    AddRoundKey
    InvMixColumns

Final round 0 (no InvMixColumns):
    InvShiftRows
    InvSubBytes
    AddRoundKey (with round_keys[0])
```

---

## The Four Operations

### 1. SubBytes (Confusion)

Each byte replaced via S-box lookup. Provides non-linearity to resist linear cryptanalysis.

The S-box is derived from the multiplicative inverse in GF(2^8) followed by an affine transformation.

### 2. ShiftRows (Diffusion)

```
Before:          After:
a b c d          a b c d    (row 0: no shift)
e f g h    →     f g h e    (row 1: shift left 1)
i j k l          k l i j    (row 2: shift left 2)
m n o p          p m n o    (row 3: shift left 3)
```

Prevents columns from being encrypted independently.

### 3. MixColumns (Diffusion)

Matrix multiplication in GF(2^8). Each output byte depends on all 4 input bytes in the column.

```
┌         ┐   ┌    ┐   ┌    ┐
│ 2 3 1 1 │   │ b0 │   │ b0'│
│ 1 2 3 1 │ × │ b1 │ = │ b1'│
│ 1 1 2 3 │   │ b2 │   │ b2'│
│ 3 1 1 2 │   │ b3 │   │ b3'│
└         ┘   └    ┘   └    ┘
```

Combined with ShiftRows, ensures full diffusion in 2 rounds.

### 4. AddRoundKey

XOR state with round key. This is the only step that mixes in the key.

---

## Shannon's Principles (1945)

**Confusion:** Relationship between ciphertext and key should be complex. Achieved by SubBytes (S-box substitution).

**Diffusion:** Each plaintext bit should affect many ciphertext bits. Achieved by ShiftRows + MixColumns.

**Avalanche Effect:** Changing 1 input bit should flip ~50% of output bits.

---

## Block Cipher Modes

### ECB (Electronic Codebook)

**How it works:** Each block encrypted independently with the same key.

```
Encrypt: C[n] = E(P[n])
Decrypt: P[n] = D(C[n])
```

**Weakness:** Same plaintext block = same ciphertext block. Patterns leak.

**The ECB Penguin:** Encrypting an image with ECB still shows the outline because repeated colors produce repeated ciphertext blocks.

#### ECB Byte-at-a-Time Attack

When you control part of the plaintext: `encrypt(your_input + SECRET)`

1. Send padding to push unknown byte to end of block
2. Brute-force all 256 values until ciphertext matches
3. Repeat for each byte

```python
def ecb_byte_at_a_time():
    flag = b""
    block_size = 16

    while True:
        # Padding to push unknown byte to end of block
        pad_len = block_size - 1 - (len(flag) % block_size)
        padding = b"A" * pad_len

        # Which block contains our target?
        block_num = (pad_len + len(flag)) // block_size

        # Get target ciphertext
        target = encrypt(padding.hex())
        target_block = target[block_num * 32 : (block_num + 1) * 32]

        # Brute force next byte
        for byte in range(256):
            guess = padding + flag + bytes([byte])
            result = encrypt(guess.hex())
            result_block = result[block_num * 32 : (block_num + 1) * 32]

            if result_block == target_block:
                flag += bytes([byte])
                break

        if flag.endswith(b'}'):
            break

    return flag
```

---

### CBC (Cipher Block Chaining)

**How it works:**
- Each plaintext block is XORed with the previous ciphertext block before encryption
- First block is XORed with the IV
- Decryption: `plaintext[i] = decrypt(ciphertext[i]) XOR ciphertext[i-1]`

**Vulnerability: Bit-Flipping Attack**

Modifying the IV (or previous ciphertext block) directly affects the decrypted plaintext:

```
new_iv[i] = original_iv[i] XOR original_plaintext[i] XOR desired_plaintext[i]
```

**Example (Flipping Cookie):**
```python
original = b"admin=False"
desired  = b"admin=True;"

for i in range(len(desired)):
    iv[i] = iv[i] ^ original[i] ^ desired[i]
```

**Key Takeaway:** CBC provides confidentiality but NOT integrity. Always use authenticated encryption (e.g., AES-GCM) or add a MAC.

---

### OFB (Output Feedback)

**How it works:**
- Generates keystream by repeatedly encrypting the IV
- Keystream is XORed with plaintext to produce ciphertext
- `ciphertext = plaintext XOR keystream`

**Vulnerability: Symmetric Encryption/Decryption**

OFB encryption and decryption are THE SAME operation:
```
encrypt(plaintext) = plaintext XOR keystream
decrypt(ciphertext) = ciphertext XOR keystream
```

If you can call `encrypt()` with the ciphertext and same IV, you get plaintext back:
```python
# Get encrypted flag with IV
iv = encrypted[:16]
ciphertext = encrypted[16:]

# "Encrypt" the ciphertext to get plaintext
plaintext = encrypt(ciphertext, iv)
```

**Key Takeaway:** Never expose an encryption oracle with attacker-controlled IV in OFB mode.

---

### CTR (Counter Mode)

**How it works:**
- Encrypts incrementing counter values to generate keystream
- XORs keystream with plaintext
- `ciphertext = plaintext XOR AES(key, counter++)`

**Vulnerability: Counter Reuse**

If the counter doesn't increment properly (bug or reuse), the same keystream block repeats.

**Exploitation with Known Plaintext:**
```python
# PNG files have a known 16-byte header
png_header = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'

# Recover keystream from known plaintext
keystream = xor(encrypted[:16], png_header)

# Decrypt everything with repeating keystream
for i in range(0, len(encrypted), 16):
    decrypted += xor(encrypted[i:i+16], keystream)
```

**Key Takeaway:** CTR nonce/counter must NEVER repeat with the same key. Each encryption must use a unique (nonce, counter) combination.

---

### GCM (Galois/Counter Mode)

**How it works:** CTR mode + authentication tag.

**Strengths:**
- Authenticated encryption (integrity + confidentiality)
- Detects tampering
- Parallelizable

**Weakness:** Nonce reuse is catastrophic (leaks auth key).

---

### Mode Comparison

| Mode | IV/Nonce | Parallelizable | Auth | Main Weakness |
|------|----------|----------------|------|---------------|
| ECB  | None     | Yes            | No   | Pattern leakage |
| CBC  | IV       | Decrypt only   | No   | Padding oracle, bit flip |
| OFB  | IV       | No             | No   | IV reuse |
| CTR  | Nonce    | Yes            | No   | Nonce reuse |
| GCM  | Nonce    | Yes            | Yes  | Nonce reuse |

---

### Python Examples (PyCryptodome)

```python
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

key = get_random_bytes(16)

# ECB (don't use in production)
cipher = AES.new(key, AES.MODE_ECB)
ciphertext = cipher.encrypt(plaintext)

# CBC
iv = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_CBC, iv)
ciphertext = cipher.encrypt(plaintext)
# Store iv with ciphertext

# CTR
cipher = AES.new(key, AES.MODE_CTR)
ciphertext = cipher.encrypt(plaintext)
nonce = cipher.nonce  # Store with ciphertext

# GCM (recommended)
cipher = AES.new(key, AES.MODE_GCM)
ciphertext, tag = cipher.encrypt_and_digest(plaintext)
# Store nonce and tag with ciphertext
```

#### Manual CBC Decryption with ECB

If you have ECB decrypt but ciphertext was CBC encrypted:

```python
def cbc_decrypt_manual(iv_hex, ciphertext_hex):
    plaintext = b""
    prev_block = bytes.fromhex(iv_hex)

    # Process each 16-byte block (32 hex chars)
    for i in range(0, len(ciphertext_hex), 32):
        block_hex = ciphertext_hex[i:i+32]

        # ECB decrypt the block
        dec = ecb_decrypt(block_hex)['plaintext']
        dec_bytes = bytes.fromhex(dec)

        # XOR with previous block (or IV)
        plain_block = bytes([a ^ b for a, b in zip(dec_bytes, prev_block)])
        plaintext += plain_block

        # Current ciphertext block becomes "previous" for next iteration
        prev_block = bytes.fromhex(block_hex)

    return plaintext
```

---

## Python Byte Manipulation

### Bytes vs Bytearray
```python
# bytes are IMMUTABLE - cannot modify in place
data = b'\x41\x42\x43'
data[0] = 0x44  # ERROR!

# bytearray is MUTABLE
data = bytearray(b'\x41\x42\x43')
data[0] = 0x44  # Works!
```

### Slicing and Indexing
```python
data = b'\x6b\x60\x7c\x25\xcf'

# Indexing returns an INTEGER (0-255)
data[0]      # 107 (int)

# Slicing returns BYTES
data[0:1]    # b'k' (bytes)
data[:16]    # First 16 bytes
data[-16:]   # Last 16 bytes
```

### Hex Conversion
```python
# Hex string to bytes
bytes.fromhex("6b607c25")  # b'k`|%'

# Bytes to hex string
b'k`|%'.hex()  # '6b607c25'
```

---

## Common Attack Patterns

| Mode | Attack | Condition |
|------|--------|-----------|
| CBC | Bit-flipping | Can modify IV or ciphertext |
| CBC | Padding oracle | Server reveals padding errors |
| OFB | Decrypt via encrypt | Can encrypt with chosen IV |
| CTR | Keystream recovery | Counter reuse + known plaintext |
| ECB | Block substitution | Deterministic (same input = same output) |

---

## Key Points

- AES-128: 10 rounds, 11 round keys
- AES-192: 12 rounds, 13 round keys
- AES-256: 14 rounds, 15 round keys

- Functions that modify in-place (`inv_shift_rows`, `inv_mix_columns`) don't return anything
- Functions that return new state (`sub_bytes`, `add_round_key`) must be assigned

- Best attack (biclique): reduces 128-bit to 126.1-bit - still completely infeasible
- Quantum (Grover's): halves security - use AES-256 for future-proofing

---

## General Principles

1. **Never roll your own crypto** - Use established libraries (PyCryptodome, cryptography)

2. **Use authenticated encryption** - AES-GCM, ChaCha20-Poly1305 provide both confidentiality AND integrity

3. **Nonces/IVs must be unique** - Reusing them breaks security in most modes

4. **Encryption != Authentication** - Encryption hides data; authentication prevents tampering. You usually need both.

5. **Known plaintext is powerful** - File headers (PNG, PDF, ZIP) provide known bytes for attacks
