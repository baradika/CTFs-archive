from pwn import *
from Crypto.Cipher import AES

iv = b'heheAEStheticheh'

def exploit():
    conn = remote('ctf.compfest.id', 7101)
    try:
        conn.sendlineafter(b'> ', b'2')
        conn.recvuntil(b'Here is the flag: [')
        flag_data = conn.recvuntil(b']', drop=True).decode()
        blocks = []
        for block in flag_data.split(', ')[:3]:
            try:
                clean = block[2:-1].encode('latin-1').decode('unicode-escape').encode('latin-1')
                blocks.append(clean)
            except:
                continue
        plaintext = b''
        prev_block = iv
        for i, block in enumerate(blocks):
            conn.sendlineafter(b'> ', b'1')
            conn.sendlineafter(b'> ', block.hex().encode())
            conn.recvuntil(b'Here is the result: ')
            decrypted = bytes.fromhex(conn.recvline().strip().decode())
            plaintext += bytes(a^b for a,b in zip(decrypted, prev_block))
            prev_block = block
        flag = plaintext.split(b'}')[0] + b'}'
        print(flag.decode())
    finally:
        conn.close()

if __name__ == "__main__":
    exploit()
