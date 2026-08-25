import os
from PIL import Image, ImageDraw

def create_cute_icon(size=256):
    # Create 32-bit RGBA image
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Outer rounded container / background glow (Cute Squircle)
    # Gradient-like layered rounded rectangle
    pad = 12
    draw.rounded_rectangle([pad, pad, size - pad, size - pad], radius=56, fill="#4338ca")
    draw.rounded_rectangle([pad + 4, pad + 4, size - pad - 4, size - pad - 4], radius=50, fill="#6366f1")
    draw.rounded_rectangle([pad + 8, pad + 8, size - pad - 8, size - pad - 8], radius=44, fill="#818cf8")

    # 2. Cute Magical Eraser Character (萌萌的粉蓝魔法橡皮擦)
    # Body (Cute angled capsule / rounded rectangle)
    ew, eh = 140, 150
    ex0 = (size - ew) // 2
    ey0 = (size - eh) // 2 + 10

    # Eraser top part (Soft Cream White)
    draw.rounded_rectangle([ex0, ey0, ex0 + ew, ey0 + eh], radius=32, fill="#ffffff")

    # Eraser sleeve / cute wrapper (Pastel Rose Pink #fb7185)
    sw_top = ey0 + 60
    draw.rounded_rectangle([ex0, sw_top, ex0 + ew, ey0 + eh], radius=32, fill="#f43f5e")
    draw.rectangle([ex0, sw_top, ex0 + ew, sw_top + 20], fill="#f43f5e") # flat top

    # Sleeve decorative stripe
    draw.rectangle([ex0, sw_top + 24, ex0 + ew, sw_top + 34], fill="#ffe4e6")

    # 3. Cute Mascot Face on the Eraser (萌萌哒表情)
    # Happy curve eyes
    # Left eye
    draw.arc([ex0 + 32, ey0 + 26, ex0 + 52, ey0 + 44], start=190, end=350, fill="#1e1b4b", width=4)
    # Right eye
    draw.arc([ex0 + ew - 52, ey0 + 26, ex0 + ew - 32, ey0 + 44], start=190, end=350, fill="#1e1b4b", width=4)

    # Cute blush cheeks (粉嫩腮红)
    draw.ellipse([ex0 + 24, ey0 + 38, ex0 + 42, ey0 + 48], fill="#fbcfe8")
    draw.ellipse([ex0 + ew - 42, ey0 + 38, ex0 + ew - 24, ey0 + 48], fill="#fbcfe8")

    # Smiling mouth (小猫嘴 ‿ )
    draw.arc([ex0 + 58, ey0 + 36, ex0 + 82, ey0 + 52], start=20, end=160, fill="#1e1b4b", width=3)

    # 4. Sparkles / Magic Stars ✨ (代表去水印的魔法闪光)
    # Top-right magic star
    def draw_star(cx, cy, r, color="#fef08a"):
        points = [
            (cx, cy - r),
            (cx + r * 0.28, cy - r * 0.28),
            (cx + r, cy),
            (cx + r * 0.28, cy + r * 0.28),
            (cx, cy + r),
            (cx - r * 0.28, cy + r * 0.28),
            (cx - r, cy),
            (cx - r * 0.28, cy - r * 0.28),
        ]
        draw.polygon(points, fill=color)

    draw_star(size - 38, 38, 22, color="#fef08a")
    draw_star(size - 64, 22, 10, color="#ffffff")
    draw_star(36, size - 44, 14, color="#fde047")
    draw_star(48, size - 68, 8, color="#ffffff")

    return img

def save_all_icon_formats():
    target_dir = r"l:\我的云端硬盘\2026产业经济学\notebooklm-watermark-remover"
    img_256 = create_cute_icon(256)
    
    # Save PNG
    png_path = os.path.join(target_dir, "app_icon.png")
    img_256.save(png_path, format="PNG")
    print(f"Saved PNG icon: {png_path}")

    # Save multi-resolution ICO
    ico_path = os.path.join(target_dir, "app_icon.ico")
    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img_256.save(ico_path, format="ICO", sizes=icon_sizes)
    print(f"Saved Multi-resolution ICO icon: {ico_path}")

if __name__ == "__main__":
    save_all_icon_formats()
