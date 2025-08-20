def decrypt(text, shift):
    result = ''
    for char in text:
        code = ord(char)
        if 65 <= code <= 90:
            result += chr(((code - 65 - shift) % 26) + 65)
        elif 97 <= code <= 122:
            result += chr(((code - 97 - shift) % 26) + 97)
        elif 48 <= code <= 57:
            result += chr(((code - 48 - shift) % 10) + 48)
        else:
            result += char
    return result

encrypted_username = "hktpu"
encrypted_password = "875j414231k8mi18593kij01l4h3290l"

for shift in range(1, 26):
    decrypted_username = decrypt(encrypted_username, shift)
    decrypted_password = decrypt(encrypted_password, shift)
    print(f"Ke {shift}:")
    print(f"  Username: {decrypted_username}")
    print(f"  Password: {decrypted_password}")
    print("-" * 40)
