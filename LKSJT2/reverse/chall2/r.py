data_encrypted = [
    0x271d54322c352d2a,  # local_b8
    0x560115030a39551f,  # local_b0
    0x141639352d2a3956,  # local_a8
    0x30305080f1009,     # local_a0
    0x39,                # uStack_99
    0x59594759471e1e,    # uStack_98
    0x1b59515555573959    # local_91
]

cipher_bytes = b''.join([val.to_bytes(8, byteorder='little') for val in data_encrypted])
flag = ''.join(chr(b ^ 0x66) for b in cipher_bytes)
print(flag)
