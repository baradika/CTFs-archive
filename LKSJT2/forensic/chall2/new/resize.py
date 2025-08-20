from PIL import Image, ImageOps

def resize_to_aspect_ratio(infile, outfile, ratio_width, ratio_height):
    img = Image.open(infile)
    original_width, original_height = img.size

    # Hitung rasio aspek asli gambar
    original_ratio = original_width / original_height
    target_ratio = ratio_width / ratio_height

    # Tentukan ukuran baru berdasarkan rasio
    if original_ratio > target_ratio:
        # Lebar lebih besar, sesuaikan dengan lebar dan tambahkan padding di atas dan bawah
        new_width = int(original_height * target_ratio)
        new_height = original_height
    else:
        # Tinggi lebih besar, sesuaikan dengan tinggi dan tambahkan padding kiri dan kanan
        new_width = original_width
        new_height = int(original_width / target_ratio)

    # Resize gambar dengan mempertahankan rasio aspek
    resized = img.resize((new_width, new_height), Image.LANCZOS)

    # Membuat canvas baru dengan ukuran target (rasio yang diinginkan)
    final_img = Image.new("RGB", (ratio_width, ratio_height), (255, 255, 255))

    # Hitung posisi untuk menempatkan gambar yang sudah di-resize
    x_offset = (ratio_width - new_width) // 2
    y_offset = (ratio_height - new_height) // 2

    # Tempatkan gambar yang telah di-resize ke dalam canvas dengan padding
    final_img.paste(resized, (x_offset, y_offset))

    # Simpan hasil gambar yang telah di-resize dan diberi padding
    final_img.save(outfile)

# Contoh pemakaian: resize dengan rasio 1:3
resize_to_aspect_ratio("coconut.png", "resized_coconut.png", 1000, 2000)
