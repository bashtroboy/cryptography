#!/usr/bin/env python3                                                                                                   
import requests                                                                                                          
                                                                                                                        
BASE_URL = "http://aes.cryptohack.org/ecb_oracle"                                                                        
                                                                                                                        
def encrypt(plaintext_hex):                                                                                              
    r = requests.get(f"{BASE_URL}/encrypt/{plaintext_hex}/")                                                             
    return r.json()['ciphertext']                                                                                        
                                                                                                                        
flag = b""                                                                                                               
block_size = 16                                                                                                          
                                                                                                                        
print("=== ECB Byte-at-a-Time Attack ===\n")                                                                             
                                                                                                                        
while True:                                                                                                              
    # Padding to push unknown byte to end of block                                                                       
    pad_len = block_size - 1 - (len(flag) % block_size)                                                                  
                                                                                                                        
    # FIX: Can't send empty plaintext, use full block instead                                                            
    if pad_len == 0:                                                                                                     
        pad_len = block_size                                                                                             
                                                                                                                        
    padding = b"A" * pad_len                                                                                             
                                                                                                                        
    # Which block contains our target?                                                                                   
    block_num = (pad_len + len(flag)) // block_size                                                                      
                                                                                                                        
    print(f"--- Byte {len(flag) + 1} ---")                                                                               
    print(f"Flag length so far: {len(flag)}")                                                                            
    print(f"Padding length: {pad_len}")                                                                                  
    print(f"Block to compare: {block_num}")                                                                              
                                                                                                                        
    # Get target ciphertext                                                                                              
    target = encrypt(padding.hex())                                                                                      
    target_block = target[block_num * 32 : (block_num + 1) * 32]                                                         
    print(f"Target block: {target_block}")                                                                               
                                                                                                                        
    # Brute force the next byte                                                                                          
    found = False                                                                                                        
    for byte in range(256):                                                                                              
        guess = padding + flag + bytes([byte])                                                                           
        result = encrypt(guess.hex())                                                                                    
        result_block = result[block_num * 32 : (block_num + 1) * 32]                                                     
                                                                                                                        
        if result_block == target_block:                                                                                 
            flag += bytes([byte])                                                                                        
            char = chr(byte) if 32 <= byte < 127 else f'\\x{byte:02x}'                                                   
            print(f"MATCH! Byte {byte} = '{char}'")                                                                      
            print(f"Flag: {flag}\n")                                                                                     
            found = True                                                                                                 
            break                                                                                                        
                                                                                                                        
    if not found:                                                                                                        
        print("No match found - likely hit padding")                                                                     
        break                                                                                                            
                                                                                                                        
    if flag.endswith(b'}'):                                                                                              
        print("Found closing brace - flag complete!")                                                                    
        break                                                                                                            
                                                                                                                        
print(f"\n=== Final flag: {flag.decode()} ===")