from binascii import hexlify, unhexlify
from pwn import *

def xor(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

def exploit():
    conn = remote('ctf.compfest.id', 7103)
    conn.sendlineafter(b'> ', b'3')
    encrypted_flag = conn.recvline().strip()
    encrypted_flag = unhexlify(encrypted_flag)
    block_size = 16
    iv = encrypted_flag[:block_size]
    ciphertext = encrypted_flag[block_size:]
    num_blocks = len(ciphertext) // block_size
    known_flag = b""
    for block_idx in range(num_blocks):
        current_block = ciphertext[block_idx*block_size:(block_idx+1)*block_size]
        decrypted_block = bytearray(block_size)
        for byte_pos in range(block_size-1, -1, -1):
            padding_length = block_size - byte_pos
            crafted_iv = bytearray([0] * block_size)
            for i in range(byte_pos + 1, block_size):
                crafted_iv[i] = decrypted_block[i] ^ padding_length
            found_byte = False
            for guess in range(256):
                crafted_iv[byte_pos] = guess
                payload = hexlify(crafted_iv + current_block).decode()
                conn.sendlineafter(b'> ', b'2')
                conn.sendlineafter(b'> ', payload.encode())
                response = conn.recvline()
                if b"Oops" not in response:
                    decrypted_block[byte_pos] = guess ^ padding_length
                    print(f"Block {block_idx}, pos {byte_pos}: {decrypted_block[byte_pos]}")
                    found_byte = True
                    break
            
            if not found_byte:
                print("Failed to find byte")
                conn.close()
                return
        
        # For first block, XOR with original IV
        if block_idx == 0:
            plaintext_block = xor(iv, decrypted_block)
        else:
            # For subsequent blocks, XOR with previous ciphertext block
            prev_block = ciphertext[(block_idx-1)*block_size:block_idx*block_size]
            plaintext_block = xor(prev_block, decrypted_block)
        
        known_flag += plaintext_block
        print(f"Decrypted so far: {known_flag}")
    
    conn.close()
    print(f"Flag found: {known_flag}")

exploit()
