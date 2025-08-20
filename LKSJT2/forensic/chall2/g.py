from PIL import Image

with open('raw_rgba_dump.bin', 'rb') as f:
    raw = f.read()

# coba-coba dimensi, misal 1024x2000
width = 1024
height = len(raw) // (width * 4)

img = Image.frombytes('RGBA', (width, height), raw)
img.save('reconstructed.png')
