#!/usr/bin/env python3

x = 26513
y = 32321

def egcd(a,b):
    if b == 0:                                                                                                            
        return a, 1, 0  # gcd, u, v (base case: a*1 + 0*0 = a)                                                            
    else:                                                                                                                 
        gcd, u1, v1 = egcd(b, a % b)                                                                                      
        # Work backwards to find u, v for current step                                                                    
        u = v1                                                                                                            
        v = u1 - (a // b) * v1                                                                                            
        return gcd, u, v    

gcd, u, v = egcd(x,y)

print(f"gcd={gcd}, u={u}, v={v}")                                                                                         
print(f"Verify: {x}*{u} + {y}*{v} = {x*u + y*v}")                                                                         
print(f"Flag: {min(u, v)}")    