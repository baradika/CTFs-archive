import zipfile
import itertools
import string

zip_path = 'protected.zip'
charset = string.ascii_lowercase + string.digits
length = 12

with zipfile.ZipFile(zip_path) as zf:
    for pwd_tuple in itertools.product(charset, repeat=length):
        password = ''.join(pwd_tuple)
        try:
            zf.extractall(pwd=password.encode())
            print(f"[+] Password found: {password}")
            break
        except:
            continue
