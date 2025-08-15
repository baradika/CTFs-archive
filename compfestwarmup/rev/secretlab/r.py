import hashlib

# Convert the five qwords to bytes (little-endian)
q1 = 14665569304904511663
q2 = 5385794698809859774
q3 = 13825184220745982910
q4 = 18416225818507988683
q5 = 18026904693940997814

data = bytearray()
for q in [q1, q2, q3, q4, q5]:
    data.extend(q.to_bytes(8, 'little'))

# Output buffer for the decoded flag (37 bytes)
out = bytearray(37)
rax = 0  # Data pointer
rcx = 0  # Output pointer

# Section one: decode first 8 bytes (correct)
for _ in range(8):
    bl = data[rax]
    bl = (bl ^ 0x69) & 0xFF
    bl = (bl + 0xE7) & 0xFF
    bl = (bl + 25) & 0xFF  # Loop adds 25
    bl = (bl ^ 0x96) & 0xFF
    out[rcx] = bl
    rax += 1
    rcx += 1

# Section two: CORRECTED decoding (store high byte after operations)
for _ in range(4):
    word = data[rax] | (data[rax+1] << 8)
    word = (word + 0xBE) & 0xFFFF
    word ^= 0x42
    # After shifts, we want the high byte of the original operation result
    out[rcx] = (word >> 8) & 0xFF
    rax += 2
    rcx += 1

# Section three: CORRECTED mask and byte swap
dx_mask = 0xFEFF
for _ in range(4):
    word = data[rax] | (data[rax+1] << 8)
    word &= dx_mask
    
    # Swap bytes and divide by 2
    swapped = ((word & 0xFF) << 8) | ((word >> 8) & 0xFF)
    swapped //= 2  # Unsigned division
    
    # Swap bytes back to little-endian
    result = ((swapped & 0xFF) << 8) | ((swapped >> 8) & 0xFF)
    out[rcx] = result & 0xFF
    out[rcx+1] = (result >> 8) & 0xFF
    rax += 2
    rcx += 2

# Section four: first dword - CORRECTED operations
dword = int.from_bytes(data[rax:rax+4], 'little')
ebx = (~dword) & 0xFFFFFFFF

# Operation sequence with proper byte handling
ebx = (ebx << 2) & 0xFFFFFFFF
bl = (ebx & 0xFF) + 1
ebx = (ebx & 0xFFFFFF00) | bl

ebx = (ebx << 2) & 0xFFFFFFFF
bl = (ebx & 0xFF) + 3
ebx = (ebx & 0xFFFFFF00) | bl

ebx = (ebx << 3) & 0xFFFFFFFF
bl = (ebx & 0xFF) + 3  # sub bl,0xFD = add bl,3 mod 256
ebx = (ebx & 0xFFFFFF00) | (bl & 0xFF)

ebx = (ebx << 1) & 0xFFFFFFFF
bl = (ebx & 0xFF) + 1
ebx = (ebx & 0xFFFFFF00) | (bl & 0xFF)

out[rcx:rcx+4] = ebx.to_bytes(4, 'little')
rax += 4
rcx += 4

# Insert underscore
out[rcx] = 0x5F  # '_'
rcx += 1

# Section four: second dword - CORRECTED operations
dword = int.from_bytes(data[rax:rax+4], 'little')
ebx = (~dword) & 0xFFFFFFFF

ebx = (ebx << 4) & 0xFFFFFFFF
bl = (ebx & 0xFF) + 1
ebx = (ebx & 0xFFFFFF00) | bl

bl = (bl ^ 0x06) & 0xFF
ebx = (ebx & 0xFFFFFF00) | bl

ebx = (ebx << 2) & 0xFFFFFFFF
bl = (ebx & 0xFF) + 1
ebx = (ebx & 0xFFFFFF00) | bl

ebx = (ebx << 2) & 0xFFFFFFFF
out[rcx:rcx+4] = ebx.to_bytes(4, 'little')
rax += 4
rcx += 4

# Section five: bit reversal - CORRECTED
qword = int.from_bytes(data[rax:rax+8], 'little')
qword >>= 1  # Initial shift

# Efficient bit reversal
reversed_val = 0
bits = bin(qword)[2:].zfill(64)  # Get 64-bit representation
reversed_val = int(bits[::-1], 2)

out[rcx:rcx+8] = reversed_val.to_bytes(8, 'little')

# Final flag assembly
flag_str = out.decode('latin1')
flag_sha = hashlib.sha256(flag_str.encode('latin1')).hexdigest()[:10]
final_flag = f"COMPFEST17{{{flag_str}_{flag_sha}}}"
print(final_flag)
