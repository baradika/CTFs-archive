from PIL import Image, UnidentifiedImageError

def fix_and_resize_png(input_path, output_path, scale_y=2):
    try:
        # 1. Buka gambar
        img = Image.open(input_path)
        img.load()  # Paksa muat semua data gambar

        # 2. Convert ke RGB jika PNG dengan alpha (RGBA) supaya aman saat disimpan ulang
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # 3. Resize ke skala vertikal (rasio 1:scale_y)
        width, height = img.size
        new_size = (width, height * scale_y)
        img_resized = img.resize(new_size, Image.Resampling.NEAREST)

        # 4. Simpan hasilnya
        img_resized.save(output_path)
        print(f"[✔] Gambar berhasil diperbaiki dan diresize: {output_path}")

    except UnidentifiedImageError:
        print("[✘] Gagal membuka gambar. Mungkin filenya rusak parah atau bukan PNG.")
    except Exception as e:
        print(f"[✘] Terjadi error: {e}")

# Ganti nama file sesuai kebutuhanmu
fix_and_resize_png("fixed_coconut.png", "resized_output.png", scale_y=3)
