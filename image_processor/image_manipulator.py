from PIL import Image

def compress_image(input_path, quality=30):
    with Image.open(input_path) as img:
        img = img.convert("L")
        img.save(input_path, "JPEG", optimize=True, quality=quality)

def compress_image_with_quality(input_path, quality=85, max_width=None, grayscale=False):
    with Image.open(input_path) as img:
        if grayscale:
            img = img.convert("L")
        
        if max_width and img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        img.save(input_path, "JPEG", optimize=True, quality=quality)