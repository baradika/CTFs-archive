#!/usr/bin/env python3
from pwn import xor
import sys

if len(sys.argv) != 2:
    print("Usage: python3 decrypt_mp4.py <encrypted_mp4_filename>")
    sys.exit(1)

enc_file = sys.argv[1]
with open(enc_file, "rb") as f:
    C = f.read()

K = bytes([
    0x00, 0x00, 0x00, 0x20,   # size = 32
    0x66, 0x74, 0x79, 0x70,   # "ftyp"
    0x69, 0x73, 0x6F, 0x6D,   # "isom"
    0x00, 0x00, 0x02, 0x00    # minor_version = 0x00000200
])

P = xor(C, K)
outname = enc_file + ".dec.mp4"
with open(outname, "wb") as f:
    f.write(P)

print(outname)
