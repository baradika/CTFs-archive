from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
import random

BANNER = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   Tiyaseu Crypto System                                       ║
║                                                               ║
║   Can you exploit the vulnerability in this system?           ║
║   Good Luck :>                                                ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"""

def generate_key_pair(k = 384):
    p = getPrime(k)
    q = getPrime(k)
    n = p*q
    phi = (p-1)*(q-1)
    e = 65537
    d = pow(e, -1, phi)
    
    return (n, e), (n, d), (p, q)

def encrypt_flag(public_key, flag):
    n, e = public_key
    flag = bytes_to_long(flag.encode())
    return pow(flag, e, n)

public_key, private_key, factors = generate_key_pair()
n, e = public_key
n, d = private_key
p, q = factors

flag = "REDACTED"
enc_flag = encrypt_flag(public_key, flag)

k = 384

print(BANNER)
print(f"Info 1: {p >> (k // 2)}")
print(f"Info 2: {q & (2 ** (k - 96) - 1)}")
print(f"Info 3: {n}")

print(f"\nDecrypt this flag now!")
print(f"Encrypted flag: {(enc_flag)}")