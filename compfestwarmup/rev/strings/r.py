import struct
from elftools.elf.elffile import ELFFile

binary_path = "chall"
PTR_TABLE_ADDR = 0x4cbae0  
PTR_COUNT = 0x1e2
XOR_KEY = 0x17

def vaddr_to_offset(elffile, vaddr):
    for seg in elffile.iter_segments():
        if seg['p_type'] == 'PT_LOAD':
            start = seg['p_vaddr']
            end = start + seg['p_memsz']
            if start <= vaddr < end:
                return vaddr - start + seg['p_offset']
    raise ValueError(f"Vaddr {hex(vaddr)} not in any LOAD segment")

with open(binary_path, "rb") as f:
    elffile = ELFFile(f)

    ptr_table_offset = vaddr_to_offset(elffile, PTR_TABLE_ADDR)
    f.seek(ptr_table_offset)

    table = []
    for _ in range(PTR_COUNT):
        ptr_val = struct.unpack("<Q", f.read(8))[0]
        len_val = struct.unpack("<Q", f.read(8))[0]
        table.append((ptr_val, len_val))

    flag_bytes = bytearray(PTR_COUNT)
    for i, (ptr_val, _len) in enumerate(table):
        try:
            data_offset = vaddr_to_offset(elffile, ptr_val) + (i ^ XOR_KEY)
            f.seek(data_offset)
            b = f.read(1)
            if not b:
                b = b'?'
            flag_bytes[i] = b[0]
        except ValueError:
            flag_bytes[i] = ord('?')

print(flag_bytes.decode(errors="replace"))
