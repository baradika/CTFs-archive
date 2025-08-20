from PIL import Image

# Load image
input_image = "fixed_coconut.png"  # Ganti dengan path gambar Anda
output_image = "resized_image_1_3.png"  # Nama file output
ratio = 3  # Rasio 1:3

# Buka gambar
image = Image.open(input_image)

# Mendapatkan ukuran gambar asli
original_width, original_height = image.size

# Menentukan ukuran baru sesuai rasio 1:3
new_width = original_width
new_height = int(original_width * ratio)  # Mengubah tinggi sesuai dengan rasio 1:3

# Resize gambar
resized_image = image.resize((new_width, new_height))

# Simpan gambar yang sudah diresize
resized_image.save(output_image)

print(f"Gambar telah diresize menjadi {new_width}x{new_height} dan disimpan sebagai {output_image}")
