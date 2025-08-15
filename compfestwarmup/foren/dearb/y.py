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

out = bytearray(37)  # Output buffer for the decoded flag
rax = 0  # Data pointer
rcx = 0  # Output pointer

# Section one: decode first 8 bytes
for _ in range(8):
    bl = data[rax]
    bl = (bl ^ 0x69) & 0xFF
    bl = (bl + 0xE7) & 0xFF
    bl = (bl + 25) & 0xFF
    bl = (bl ^ 0x96) & 0xFF
    out[rcx] = bl
    rax += 1
    rcx += 1

# Section two: decode next 4 bytes (as words)
for _ in range(4):
    word = data[rax] | (data[rax + 1] << 8)
    bx = (word + 0xBE) & 0xFFFF
    bx ^= 0x42
    bx >>= 4
    bl = (bx & 0xFF) ^ 0x04
    bx >>= 4
    out[rcx] = bl & 0xFF
    rax += 2
    rcx += 1

# Section three: decode next 8 bytes (as words)
dx = 0xFEFF  # Precomputed mask
for _ in range(4):
    word = data[rax] | (data[rax + 1] << 8)
    bx = word & dx
    # Swap bytes and divide by 2
    L = bx & 0xFF
    H = (bx >> 8) & 0xFF
    temp = (L << 8) | H
    temp //= 2
    # Swap bytes again
    L2 = temp & 0xFF
    H2 = (temp >> 8) & 0xFF
    res = (L2 << 8) | H2
    out[rcx] = res & 0xFF
    out[rcx + 1] = (res >> 8) & 0xFF
    rax += 2
    rcx += 2

# Section four: decode next 8 bytes (as dwords) and insert '_'
# First dword
dword = data[rax] | (data[rax + 1] << 8) | (data[rax + 2] << 16) | (data[rax + 3] << 24)
ebx = (~dword) & 0xFFFFFFFF
ebx <<= 2
bl = (ebx & 0xFF) + 1
ebx = (ebx & 0xFFFFFF00) | (bl & 0xFF)
ebx <<= 2
bl = (ebx & 0xFF) + 3
ebx = (ebx & 0xFFFFFF00) | (bl & 0xFF)
ebx <<= 3
bl = (ebx & 0xFF) + 3  # Equivalent to sub bl, 0xFD (add 3)
ebx = (ebx & 0xFFFFFF00) | (bl & 0xFF)
ebx <<= 1
bl = (ebx & 0xFF) + 1
ebx = (ebx & 0xFFFFFF00) | (bl & 0xFF)
out[rcx:rcx + 4] = ebx.to_bytes(4, 'little')
rax += 4
rcx += 4
# Insert underscore
out[rcx] = 0x5F  # '_'
rcx += 1
# Second dword
dword = data[rax] | (data[rax + 1] << 8) | (data[rax + 2] << 16) | (data[rax + 3] << 24)
ebx = (~dword) & 0xFFFFFFFF
ebx <<= 4
bl = (ebx & 0xFF) + 1
ebx = (ebx & 0xFFFFFF00) | (bl & 0xFF)
bl ^= 0x06
ebx = (ebx & 0xFFFFFF00) | bl
ebx <<= 2
bl = (ebx & 0xFF) + 1
ebx = (ebx & 0xFFFFFF00) | (bl & 0xFF)
ebx <<= 2
out[rcx:rcx + 4] = ebx.to_bytes(4, 'little')
rax += 4
rcx += 4

# Section five: decode last 8 bytes (as qword) and reverse bits
qword = data[rax] | (data[rax + 1] << 8) | (data[rax + 2] << 16) | (data[rax + 3] << 24)
qword |= (data[rax + 4] << 32) | (data[rax + 5] << 40) | (data[rax + 6] << 48) | (data[rax + 7] << 56)
qword >>= 1  # Logical right shift
# Reverse bits of the qword
reversed_val = 0
for i in range(64):
    reversed_val = (reversed_val << 1) | (qword & 1)
    qword >>= 1
# Store reversed qword in output
out[rcx:rcx + 8] = reversed_val.to_bytes(8, 'little')
rcx += 8

# Convert to string and compute SHA-256
flag_str = out.decode('latin1')
flag_sha = hashlib.sha256(flag_str.encode()).hexdigest()[:10]
final_flag = f"COMPFEST17{{{flag_str}_{flag_sha}}}"
print(final_flag)
