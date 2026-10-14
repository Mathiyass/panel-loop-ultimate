r"""
===============================================================================
CYBERPUNK ESPORTS ICON GENERATOR FOR MATHIYA GAMELOOP PANEL
Creates professional vector-quality multi-resolution .ico and .png assets
===============================================================================
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

ICO_PATH = os.path.join(ASSETS_DIR, "mathiya_icon.ico")
PNG_PATH = os.path.join(ASSETS_DIR, "mathiya_icon.png")
PNG_HEADER_PATH = os.path.join(ASSETS_DIR, "mathiya_header_logo.png")

def create_esports_icon():
    # Render at high resolution (1024x1024) for supreme downscaled anti-aliasing
    size = 1024
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = size // 2, size // 2
    r_outer = 480
    r_inner = 450

    # 1. Calculate Hexagonal Shield Vertices
    def get_hex_points(radius, center_x, center_y):
        points = []
        for i in range(6):
            # Rotate by 30 deg so top is flat/pointed
            angle_deg = 60 * i - 30
            angle_rad = math.radians(angle_deg)
            x = center_x + radius * math.cos(angle_rad)
            y = center_y + radius * math.sin(angle_rad)
            points.append((x, y))
        return points

    outer_hex = get_hex_points(r_outer, cx, cy)
    inner_hex = get_hex_points(r_inner, cx, cy)

    # 2. Draw Glow Layer (Blurred Violet/Cyan Halo)
    glow_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_img)
    glow_draw.polygon(outer_hex, fill=(0, 240, 255, 60))
    glow_img = glow_img.filter(ImageFilter.GaussianBlur(radius=40))
    img.paste(glow_img, (0, 0), glow_img)

    # 3. Draw Deep Obsidian Metallic Base
    draw.polygon(inner_hex, fill=(10, 14, 22, 255))

    # Inner subtle dark radial gradient
    grad_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    grad_draw = ImageDraw.Draw(grad_img)
    for rad in range(r_inner, 0, -20):
        alpha = int(120 * (1 - rad / r_inner))
        grad_draw.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=(18, 28, 48, alpha))
    grad_img = grad_img.filter(ImageFilter.GaussianBlur(radius=30))
    img.paste(grad_img, (0, 0), grad_img)

    # 4. Outer Glowing Cyberpunk Border (Electric Violet + Cyan)
    border_width = 16
    draw.line(outer_hex + [outer_hex[0]], fill=(168, 85, 247, 220), width=border_width) # Ultraviolet
    draw.line(inner_hex + [inner_hex[0]], fill=(0, 240, 255, 255), width=border_width // 2) # Electric Cyan

    # 5. Tactical Crosshair Reticle Notches on Cardinal Edges
    reticle_len = 50
    reticle_color = (0, 240, 255, 255)
    # Top
    draw.line([(cx, cy - r_outer - 10), (cx, cy - r_outer + reticle_len)], fill=reticle_color, width=12)
    # Bottom
    draw.line([(cx, cy + r_outer + 10), (cx, cy + r_outer - reticle_len)], fill=reticle_color, width=12)
    # Left
    draw.line([(cx - r_outer - 10, cy), (cx - r_outer + reticle_len, cy)], fill=reticle_color, width=12)
    # Right
    draw.line([(cx + r_outer + 10, cy), (cx + r_outer - reticle_len, cy)], fill=reticle_color, width=12)

    # 6. Center Monogram: Futuristic Stylized "M"
    # Draw custom polygon coordinates for a sharp, aggressive, esports "M"
    # Left leg, center chevron, right leg with chamfered esports angles
    m_top = 290
    m_bottom = 710
    m_left = 260
    m_right = 764
    m_mid_x = cx
    m_valley_y = 560

    # Main "M" polygon points
    m_points = [
        (m_left, m_bottom),                    # Bottom-left base
        (m_left, m_top + 60),                  # Top-left outer chamfer
        (m_left + 60, m_top),                  # Top-left inner
        (m_left + 140, m_top),                 # Top-left bridge
        (m_mid_x, m_valley_y),                 # Center valley drop
        (m_right - 140, m_top),                # Top-right bridge
        (m_right - 60, m_top),                 # Top-right inner
        (m_right, m_top + 60),                 # Top-right outer chamfer
        (m_right, m_bottom),                   # Bottom-right base
        (m_right - 90, m_bottom),              # Bottom-right inside notch
        (m_right - 90, m_top + 160),           # Inner right column
        (m_mid_x, m_valley_y + 160),           # Inner chevron peak
        (m_left + 90, m_top + 160),            # Inner left column
        (m_left + 90, m_bottom)                # Bottom-left inside notch
    ]

    # Draw "M" Glow (Cyan Halo)
    m_glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    m_glow_draw = ImageDraw.Draw(m_glow)
    m_glow_draw.polygon(m_points, fill=(0, 240, 255, 140))
    m_glow = m_glow.filter(ImageFilter.GaussianBlur(radius=25))
    img.paste(m_glow, (0, 0), m_glow)

    # Fill "M" with Electric Cyan Gradient into White
    draw.polygon(m_points, fill=(0, 240, 255, 255))

    # Inner bevel highlight for 3D metallic feel
    m_inner_highlight = [
        (m_left + 25, m_bottom - 20),
        (m_left + 25, m_top + 70),
        (m_left + 70, m_top + 25),
        (m_left + 120, m_top + 25),
        (m_mid_x, m_valley_y - 20),
        (m_right - 120, m_top + 25),
        (m_right - 70, m_top + 25),
        (m_right - 25, m_top + 70),
        (m_right - 25, m_bottom - 20)
    ]
    draw.line(m_inner_highlight, fill=(230, 255, 255, 220), width=10)

    # 7. Esports Tournament Badge Banner ("120 FPS PRO")
    banner_w = 420
    banner_h = 90
    banner_x1 = cx - banner_w // 2
    banner_y1 = m_bottom + 30
    banner_x2 = cx + banner_w // 2
    banner_y2 = banner_y1 + banner_h

    # Banner Background (Dark with Gold/Cyan Border)
    draw.rounded_rectangle([banner_x1, banner_y1, banner_x2, banner_y2], radius=16, fill=(13, 17, 26, 255), outline=(254, 183, 0, 255), width=8)

    # Add Text to Banner using default font if TrueType not available
    try:
        font = ImageFont.truetype("arialbd.ttf", 52)
    except Exception:
        font = ImageFont.load_default()

    text = "120 FPS PRO"
    # Center text
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = cx - tw // 2
    ty = banner_y1 + (banner_h - th) // 2 - 6

    draw.text((tx, ty), text, fill=(254, 183, 0, 255), font=font)

    # 8. Save High-Res PNG (512x512)
    img_512 = img.resize((512, 512), Image.Resampling.LANCZOS)
    img_512.save(PNG_PATH, format="PNG")
    print(f"[+] Saved High-Res PNG Icon: {PNG_PATH}")

    # Save Header Logo (128x128)
    img_header = img.resize((128, 128), Image.Resampling.LANCZOS)
    img_header.save(PNG_HEADER_PATH, format="PNG")
    print(f"[+] Saved Header PNG Logo: {PNG_HEADER_PATH}")

    # 9. Save Multi-Resolution Windows ICO
    # Windows standard ICO sizes: 256, 128, 64, 48, 32, 16
    icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    img_512.save(ICO_PATH, format="ICO", sizes=icon_sizes)
    print(f"[+] Saved Multi-Resolution Windows ICO: {ICO_PATH}")

if __name__ == "__main__":
    create_esports_icon()
