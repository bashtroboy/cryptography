#!/usr/bin/env python3

# /symmetry/encrypt/<plaintext>/<iv>/
# /symmetry/encrypt_flag/

################ Source

    # from Crypto.Cipher import AES
    # import os


    # KEY = ?
    # FLAG = ?


    # @chal.route('/symmetry/encrypt/<plaintext>/<iv>/')
    # def encrypt(plaintext, iv):
    #     plaintext = bytes.fromhex(plaintext)
    #     iv = bytes.fromhex(iv)
    #     if len(iv) != 16:
    #         return {"error": "IV length must be 16"}

    #     cipher = AES.new(KEY, AES.MODE_OFB, iv)
    #     encrypted = cipher.encrypt(plaintext)
    #     ciphertext = encrypted.hex()

    #     return {"ciphertext": ciphertext}


    # @chal.route('/symmetry/encrypt_flag/')
    # def encrypt_flag():
    #     iv = os.urandom(16)

    #     cipher = AES.new(KEY, AES.MODE_OFB, iv)
    #     encrypted = cipher.encrypt(FLAG.encode())
    #     ciphertext = iv.hex() + encrypted.hex()

    #     return {"ciphertext": ciphertext}


import requests

BASE_URL = 'http://aes.cryptohack.org'

def encrypt(plaintext,iv):
    r = requests.get(f'{BASE_URL}/symmetry/encrypt/{plaintext}/{iv}/')
    return r.json()

def encrypt_flag():
    r = requests.get(f'{BASE_URL}/symmetry/encrypt_flag/')
    return r.json()

flag_ciphertext_full = encrypt_flag()['ciphertext']

enc_flag = flag_ciphertext_full[32:]
iv = flag_ciphertext_full[:32]

resp = encrypt(enc_flag,iv)

print(bytes.fromhex(resp['ciphertext']))

# print(encrypt(str(flag_ciphertext_full),str(iv)))