from PIL import Image

input_path = 'fixed_coconut.png'
output_path = 'coconut_expanded.png'

# Load image
img = Image.open(input_path)

# Atur seberapa banyak kanvas ditambah (bisa sesuaikan)
pad_top = 200
pad_bottom = 500
pad_left = 200
pad_right = 200

new_width = img.width + pad_left + pad_right
new_height = img.height + pad_top + pad_bottom

# Buat kanvas baru (hitam/putih/transparan sesuai kebutuhan)
new_img = Image.new('RGBA', (new_width, new_height), (0, 0, 0, 255))  # hitam
# new_img = Image.new('RGBA', (new_width, new_height), (255, 255, 255, 255))  # putih

# Tempel gambar asli di tengah
new_img.paste(img, (pad_left, pad_top))

# Simpan
new_img.save(output_path)

print(f'Saved expanded image: {output_path}')
