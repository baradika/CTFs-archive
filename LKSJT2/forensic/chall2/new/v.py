from PIL import Image

# Buka gambar yang sudah diresize (terpotong)
img = Image.open("resized.jpg")

# Misal diketahui rasio aslinya 1:3 (tinggi = 3x lebar)
width = img.size[0]
restored_height = width * 3

# Resize ulang untuk mencoba "unlock" bagian tersembunyi
restored = img.resize((width, restored_height), Image.Resampling.BICUBIC)
restored.save("restored.jpg")

print(f"Restored image saved as 'restored.jpg' with size {width}x{restored_height}")
