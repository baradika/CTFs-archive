import zlib

def extract_idat_chunks(png_path):
    with open(png_path, 'rb') as f:
        data = f.read()

    idat_data = b''
    i = 8  # skip PNG signature
    while i < len(data):
        chunk_len = int.from_bytes(data[i:i+4], 'big')
        chunk_type = data[i+4:i+8]
        chunk_data = data[i+8:i+8+chunk_len]
        i += 8 + chunk_len + 4  # chunk_len + type + data + CRC

        if chunk_type == b'IDAT':
            idat_data += chunk_data

    return idat_data

def save_decompressed_output(png_path):
    idat_combined = extract_idat_chunks(png_path)
    try:
        raw = zlib.decompress(idat_combined)
        with open('raw_rgba_dump.bin', 'wb') as f:
            f.write(raw)
        print("[+] Decompressed IDAT to raw_rgba_dump.bin")
    except Exception as e:
        print("[-] Error decompressing IDAT:", e)

save_decompressed_output("coconut.png")
