#!/usr/bin/env python3

import requests

BASE_URL = "http://aes.cryptohack.org/"

def encrypt():
    r = requests.get(f"{BASE_URL}bean_counter/encrypt/")
    return bytes.fromhex(r.json()["encrypted"])

# Get the encrypted PNG
encrypted = encrypt()

# Known PNG header (first 16 bytes are always the same)
png_header = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'

# Recover the keystream block by XORing known plaintext with ciphertext
keystream = bytes([encrypted[i] ^ png_header[i] for i in range(16)])

# Decrypt the entire file using the repeating keystream
decrypted = b''
for i in range(0, len(encrypted), 16):
    block = encrypted[i:i+16]
    decrypted += bytes([block[j] ^ keystream[j] for j in range(len(block))])

# Save the decrypted image
with open("flag.png", "wb") as f:
    f.write(decrypted)

print("Decrypted image saved to flag.png")
