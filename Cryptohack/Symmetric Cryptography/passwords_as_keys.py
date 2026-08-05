#!/usr/bin/env python3

# http://aes.cryptohack.org/ecb_oracle/
# @chal.route('/passwords_as_keys/decrypt/<ciphertext>/<password_hash>/')

import requests                                                                                                                    
from hashlib import md5                                                                                                            
                                                                                                                                    
BASE_URL = "http://aes.cryptohack.org/passwords_as_keys"                                                                           
WORDLIST_URL = "https://gist.githubusercontent.com/wchargin/8927565/raw/d9783627c731268fb2935a731a618aa8e95cf465/words"            
                                                                                                                                    
# Get the encrypted flag                                                                                                           
r = requests.get(f"{BASE_URL}/encrypt_flag/")                                                                                      
ciphertext = r.json()['ciphertext']                                                                                                
print(f"Ciphertext: {ciphertext}")                                                                                                 
                                                                                                                                    
# Fetch wordlist                                                                                                                   
print("Fetching wordlist...")                                                                                                      
words = requests.get(WORDLIST_URL).text.splitlines()                                                                               
print(f"Loaded {len(words)} words")                                                                                                
                                                                                                                                    
# Brute force                                                                                                                      
for i, word in enumerate(reversed(words)):                                                                                                   
    password_hash = md5(word.encode()).hexdigest()                                                                                 
    r = requests.get(f"{BASE_URL}/decrypt/{ciphertext}/{password_hash}/")                                                          
    result = r.json()    

    print(f"Trying {word}...")                                                                                                          
                                                                                                                                    
    if 'plaintext' in result:                                                                                                      
        plaintext = bytes.fromhex(result['plaintext'])                                                                             
        if b'crypto{' in plaintext:                                                                                                
            print(f"\nFound! Password: {word}")                                                                                    
            print(f"Flag: {plaintext.decode()}")                                                                                   
            break                                                                                                                  
                                                                                                                                    
    if i % 100 == 0:                                                                                                               
        print(f"Tried {i} words...", end='\r')    