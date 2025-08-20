from pwn import xor

enc_file = "flag.mp4.enc"
key = bytes.fromhex("000000206674797069736f6d00000200")

with open(enc_file, "rb") as f:
    ciphertext = f.read()

plaintext = xor(ciphertext, key)
with open("flag.mp4", "wb") as f:
    f.write(plaintext)

