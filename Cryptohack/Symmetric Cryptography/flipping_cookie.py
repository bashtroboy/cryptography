#!/usr/bin/env python3

# {"cookie":"44b68ed94df78131471fac288c62a42b85c7436aa90c0c097faf7078d7b04e343372abee5768514ed9603e3673730b8f"}

# /flipping_cookie/get_cookie/
# /flipping_cookie/check_admin/<cookie>/<iv>/

  #!/usr/bin/env python3                                                             
                                                                                     
import requests                                                                    
                                                                                    
BASE_URL = "http://aes.cryptohack.org/"                                            
                                                                                    
def get_cookie():                                                                  
    r = requests.get(f"{BASE_URL}flipping_cookie/get_cookie")                      
    return r.json()                                                                
                                                                                    
def check_admin(cookie, iv):                                                       
    r = requests.get(f"{BASE_URL}flipping_cookie/check_admin/{cookie}/{iv}")       
    return r.json()                                                                
                                                                                    
cookie_json = get_cookie()                                                         
full_cookie = cookie_json['cookie']                                                
                                                                                    
# Split: IV is first 16 bytes (32 hex chars), ciphertext is the rest               
iv = bytearray(bytes.fromhex(full_cookie[:32]))                                    
ciphertext = full_cookie[32:]  # NOT the full cookie                               
                                                                                    
# Original plaintext starts with: "admin=False;expiry=..."                         
# We want:                        "admin=True;;expiry=..."                         
original = b"admin=False"                                                          
desired  = b"admin=True;"  # same length (11 bytes)                                
                                                                                    
# XOR to flip the bits                                                             
for i in range(len(desired)):                                                      
    iv[i] = iv[i] ^ original[i] ^ desired[i]                                       
                                                                                    
print(check_admin(ciphertext, iv.hex()))   