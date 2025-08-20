from PIL import Image

mywidth = 1000

img = Image.open('../fixed_coconut.png')
wpercent = (mywidth / float(img.size[0]))
hsize = int((float(img.size[1]) * float(wpercent)))
img = img.resize((mywidth, hsize), Image.Resampling.LANCZOS)
img = img.convert("RGB")  # Konversi ke RGB agar bisa disimpan sebagai JPEG
img.save('resized.png')
