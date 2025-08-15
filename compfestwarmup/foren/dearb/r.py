import os
import struct

def deep_jpeg_repair(input_file, output_file):
    with open(input_file, 'rb') as f:
        data = f.read()

    MARKERS = {
        0xC0: "SOF0", 0xC1: "SOF1", 0xC2: "SOF2", 0xC3: "SOF3",
        0xC5: "SOF5", 0xC6: "SOF6", 0xC7: "SOF7", 0xC8: "JPG",
        0xC9: "SOF9", 0xCA: "SOF10", 0xCB: "SOF11", 0xCD: "SOF13",
        0xCE: "SOF14", 0xCF: "SOF15", 0xDB: "DQT", 0xE0: "APP0",
        0xE1: "APP1", 0xE2: "APP2", 0xE3: "APP3", 0xE4: "APP4",
        0xE5: "APP5", 0xE6: "APP6", 0xE7: "APP7", 0xE8: "APP8",
        0xE9: "APP9", 0xEA: "APP10", 0xEB: "APP11", 0xEC: "APP12",
        0xED: "APP13", 0xEE: "APP14", 0xEF: "APP15", 0xFE: "COM"
    }

    output = bytearray()
    i = 0
    in_scan = False

    # Find SOI marker
    soi_pos = data.find(b'\xFF\xD8')
    if soi_pos == -1:
        output.extend(b'\xFF\xD8')
    else:
        output.extend(b'\xFF\xD8')
        i = soi_pos + 2

    while i < len(data):
        if not in_scan:
            if i+1 < len(data) and data[i] == 0xFF:
                marker = data[i+1]
                
                if marker == 0xFF:
                    i += 1
                    continue
                
                if marker == 0xD9:
                    output.extend(b'\xFF\xD9')
                    break
                
                if marker == 0xDA:
                    output.extend(b'\xFF\xDA')
                    in_scan = True
                    i += 2
                    continue
                
                if marker in MARKERS:
                    if i+3 >= len(data):
                        break
                    
                    length = struct.unpack('>H', data[i+2:i+4])[0]
                    
                    if length < 2 or i+length >= len(data):
                        output.extend(bytes([0xFF, marker, 0x00, 0x02]))
                    else:
                        output.extend(data[i:i+length+2])
                        i += length + 1
                else:
                    i += 1
            i += 1
        else:
            if i+1 < len(data) and data[i] == 0xFF and data[i+1] != 0x00:
                in_scan = False
                i -= 1
            else:
                output.append(data[i])
            i += 1

    if len(output) < 2 or output[-2:] != b'\xFF\xD9':
        output.extend(b'\xFF\xD9')

    with open(output_file, 'wb') as f:
        f.write(output)

    print(f"Repaired {input_file} -> {output_file}")

# Process all files from photo73 to photo80
for n in range(73, 81):
    input_file = f"photo{n}.jpg"
    output_file = f"photo{n}_repaired.jpg"
    
    if os.path.exists(input_file):
        deep_jpeg_repair(input_file, output_file)
    else:
        print(f"File {input_file} not found, skipping")

print("Semua file telah diproses!")
