from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import string
from itertools import product

ciphertext = bytes.fromhex('fa8f90c719cebf259cd1ee92c9e0e39cf2244f3482004f6d408db979eee25870db4ce707b67550fdfa08197fcb766201')
iv = b'z' * 16
charset = string.digits + string.ascii_lowercase

for k in product(charset, repeat=3):
    key = ''.join(k).encode()
    padded_key = pad(key, 16)
    cipher = AES.new(padded_key, AES.MODE_CBC, iv)
    try:
        decrypted = unpad(cipher.decrypt(ciphertext), 16)
        if decrypted.startswith(b'LKSJT2{'):
            print(f'{key.decode()}')
            print(f'{decrypted.decode()}')
            break
    except:
        continue
