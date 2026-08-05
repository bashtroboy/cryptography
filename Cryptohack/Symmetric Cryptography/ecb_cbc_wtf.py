#!/usr/bin/env python3                                                                                                   
import requests                                                                                                          
                                                                                                                        
BASE_URL = "http://aes.cryptohack.org/ecbcbcwtf"                                                                        
                                                                                                                        
def encrypt():                                                                                              
    r = requests.get(f"{BASE_URL}/encrypt_flag/")                                                             
    return r.json()                                                                                        

def decrypt(ciphertext):
    r = requests.get(f"{BASE_URL}/decrypt/{ciphertext}/")
    return r.json()

flag = b""
iv = b""                                                                                                               

ciphertext = encrypt()['ciphertext']                                                                                     
                                                                                                                           
# Split into hex strings                                                                                                 
iv_hex = ciphertext[:32]           # first 32 hex chars = 16 bytes                                                       
block1_hex = ciphertext[32:64]     # next 32 hex chars              
block2_hex = ciphertext[64:96]     # next 32 hex chars                                                      
                                                                                                                        
# Decrypt the ciphertext block (not the IV!)                                                                             
dec_block1 = decrypt(block1_hex)['plaintext']          
dec_block2 = decrypt(block2_hex)['plaintext']                                                                     
                                                                                                                        
# Now XOR to get plaintext                                                                                               
iv = bytes.fromhex(iv_hex)                                                                                               
dec_block1_bytes = bytes.fromhex(dec_block1)            
dec_block2_bytes = bytes.fromhex(dec_block2)                                                                  
                                                                                                                        
plaintext = bytes([a ^ b for a, b in zip(dec_block1_bytes, iv)])     
plaintext += bytes([a ^ b for a, b in zip(dec_block2_bytes, bytes.fromhex(block1_hex))])                                                   
print(plaintext)  