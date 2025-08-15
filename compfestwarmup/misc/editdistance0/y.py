import hashlib
import struct

# Data dalam little-endian
data = b""
for q in [
    14665569304904511663,
    5385794698809859774,
    13825184220745982910,
    18416225818507988683,
    18026904693940997814
]:
    data += struct.pack('<Q', q)

out = bytearray(37)
rax, rcx = 0, 0

# Section one: decode first 8 bytes
for _ in range(8):
    bl = data[rax]
    bl = (bl ^ 0x69) & 0xFF
    bl = (bl + 0xE7) & 0xFF
    bl = (bl + 25) & 0xFF  # Loop adds 25
    bl = (bl ^ 0x96) & 0xFF
    out[rcx] = bl
    rax += 1
    rcx += 1

# Section two: decode next 4 bytes
for _ in range(4):
    word = data[rax] | (data[rax+1] << 8)
    bx = (word + 0xBE) & 0xFFFF
    bx ^= 0x42
    bx >>= 4
    bl = (bx & 0xFF) ^ 0x04
    bx >>= 4
    out[rcx] = bl & 0xFF
    rax += 2
    rcx += 1

# Section three: fixed byte processing
dx_mask = 0xFEFF
for _ in range(4):
    # Ambil 2 byte (little-endian word)
    word = data[rax] | (data[rax+1] << 8)
    # Terapkan mask
    masked = word & dx_mask
    
    # Ekstrak byte tinggi dan rendah
    low_byte = masked & 0xFF
    high_byte = (masked >> 8) & 0xFF
    
    # Swap bytes dan bagi 2 (unsigned)
    swapped = (low_byte << 8) | high_byte
    swapped //= 2
    
    # Swap kembali byte untuk little-endian
    new_low = (swapped >> 8) & 0xFF
    new_high = swapped & 0xFF
    result = (new_high << 8) | new_low
    
    # Simpan sebagai 2 byte (little-endian)
    out[rcx] = result & 0xFF
    out[rcx+1] = (result >> 8) & 0xFF
    rax += 2
    rcx += 2

# Section four: dword processing
# First dword
dword = struct.unpack('<I', data[rax:rax+4])[0]
ebx = (~dword) & 0xFFFFFFFF
ebx = (ebx << 2) & 0xFFFFFFFF
bl = (ebx & 0xFF) + 1
ebx = (ebx & 0xFFFFFF00) | (bl & 0xFF)
ebx = (ebx << 2) & 0xFFFFFFFF
bl = (ebx & 0xFF) + 3
ebx = (ebx & 0xFFFFFF00) | (bl & 0xFF)
ebx = (ebx << 3) & 0xFFFFFFFF
bl = (ebx & 0xFF) + 3  # -0xFD = +3 mod 256
ebx = (ebx & 0xFFFFFF00) | (bl & 0xFF)
ebx = (ebx << 1) & 0xFFFFFFFF
bl = (ebx & 0xFF) + 1
ebx = (ebx & 0xFFFFFF00) | (bl & 0xFF)
out[rcx:rcx+4] = struct.pack('<I', ebx)
rax += 4
rcx += 4

# Insert underscore
out[rcx] = 0x5F  # '_'
rcx += 1

# Second dword
dword = struct.unpack('<I', data[rax:rax+4])[0]
ebx = (~dword) & 0xFFFFFFFF
ebx = (ebx << 4) & 0xFFFFFFFF
bl = (ebx & 0xFF) + 1
ebx = (ebx & 0xFFFFFF00) | (bl & 0xFF)
bl ^= 0x06
ebx = (ebx & 0xFFFFFF00) | bl
ebx = (ebx << 2) & 0xFFFFFFFF
bl = (ebx & 0xFF) + 1
ebx = (ebx & 0xFFFFFF00) | (bl & 0xFF)
ebx = (ebx << 2) & 0xFFFFFFFF
out[rcx:rcx+4] = struct.pack('<I', ebx)
rax += 4
rcx += 4

# Section five: bit reversal
qword_bytes = data[rax:rax+8]
qword = struct.unpack('<Q', qword_bytes)[0]
qword >>= 1  # Logical shift right

# Reverse bits
reversed_val = 0
for i in range(64):
    reversed_val = (reversed_val << 1) | (qword & 1)
    qword >>= 1

out[rcx:rcx+8] = struct.pack('<Q', reversed_val)

# Final flag processing
flag_bytes = bytes(out)
flag_str = flag_bytes.decode('latin1')  # Handle extended ASCII

# Compute SHA-256 hash of the flag bytes
sha_hash = hashlib.sha256(flag_bytes).hexdigest()[:10]
final_flag = f"COMPFEST17{{{flag_str}_{sha_hash}}}"
print(final_flag)
