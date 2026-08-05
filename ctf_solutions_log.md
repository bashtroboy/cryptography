# Cryptography Notes

## CTF Challenges

### CryptoHack - Great Snakes
- **Flag:** `crypto{z3n_0f_pyth0n}`
- **Technique:** XOR each byte with `0x32` (50) and convert to ASCII
- **Script:** `scripts/great_snakes_35381fca29d68d8f3f25c9fa0a9026fb.py`

### CryptoHack - Favourite Byte (xorkey0.py)
- **Flag:** `crypto{0x10_15_my_f4v0ur173_by7e}`
- **Technique:** Single-byte XOR brute force
  - Ciphertext XOR'd with unknown single byte
  - Try all 256 possible keys (0-255)
  - Look for output starting with `crypto{`
  - Key was 16 (0x10)
- **Script:** `scripts/intro/xorkey0.py`

### CryptoHack - XOR Properties (xor1.py)
- **Flag:** `crypto{x0r_i5_ass0c1at1v3}`
- **Technique:** Use XOR properties to recover keys and decrypt
  - Self-inverse: A ^ A = 0
  - Given KEY1 and (KEY2 ^ KEY1), recover KEY2 by XORing with KEY1
  - Chain the recoveries to get all keys, then XOR with encrypted flag
- **Script:** `scripts/intro/xor1.py`

### Caesar Cipher
- **Ciphertext:** `JEWUJXUH UNQSJ JMYD UTYJ`
- **Plaintext:** `TOGETHER EXACT TWIN EDIT`
- **Shift:** 16
