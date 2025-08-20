def fix_ihdr_crc(filename_in, filename_out):
    with open(filename_in, 'rb') as f:
        data = bytearray(f.read())

    # Pastikan IHDR dimulai dari offset 8
    ihdr_start = 8
    length = int.from_bytes(data[ihdr_start:ihdr_start+4], 'big')
    chunk_type = data[ihdr_start+4:ihdr_start+8]
    chunk_data = data[ihdr_start+8:ihdr_start+8+length]

    assert chunk_type == b'IHDR', "Chunk bukan IHDR"

    # Hitung ulang CRC
    import binascii
    crc_data = chunk_type + chunk_data
    crc = binascii.crc32(crc_data) & 0xffffffff
    crc_bytes = crc.to_bytes(4, 'big')

    # Ganti CRC lama
    crc_offset = ihdr_start + 8 + length
    data[crc_offset:crc_offset+4] = crc_bytes

    with open(filename_out, 'wb') as f:
        f.write(data)

# Pakai:
fix_ihdr_crc("coconut.png", "fixed_coconut.png")
