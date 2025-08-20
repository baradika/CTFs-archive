from struct import pack
print((pack("<I", 0x4861636b) + pack("<I", 0x7468655f) + pack("<I", 0x506c616e)).decode())
# Output: 'Hack_the_Plan'
