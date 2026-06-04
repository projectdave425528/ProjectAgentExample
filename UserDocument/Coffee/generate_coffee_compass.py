"""
Coffee Compass 中文版 - 基於 Barista Hustle 原版
生成一張圓形指南針風格的咖啡沖煮調整圖
"""
from PIL import Image, ImageDraw, ImageFont
import math
import os

# Canvas settings
WIDTH, HEIGHT = 1600, 1600
CENTER = (WIDTH // 2, HEIGHT // 2)
BG_COLOR = (255, 255, 255)

# Try to find a Chinese font
FONT_PATHS = [
    "C:/Windows/Fonts/msjh.ttc",      # Microsoft JhengHei
    "C:/Windows/Fonts/msyh.ttc",      # Microsoft YaHei
    "C:/Windows/Fonts/simsun.ttc",    # SimSun
    "C:/Windows/Fonts/mingliu.ttc",   # MingLiU
]

def get_font(size):
    for fp in FONT_PATHS:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except:
                continue
    return ImageFont.load_default()

# Fonts
font_title = get_font(48)
font_center = get_font(36)
font_section = get_font(24)
font_detail = get_font(18)
font_axis = get_font(22)

# Color palette
COLORS = {
    'center': (76, 175, 80),        # Green - perfect
    'ring1': (200, 230, 201),       # Light green
    'ring2': (255, 249, 196),       # Light yellow
    'ring3': (255, 224, 178),       # Light orange
    'ring4': (255, 205, 210),       # Light red
    'text_dark': (33, 33, 33),
    'text_mid': (97, 97, 97),
    'axis_line': (158, 158, 158),
    'border': (66, 66, 66),
}

# Compass sections (8 directions)
# Each: (angle_start, label, flavors, color)
SECTIONS = [
    # Top (Under-extracted + Weak)
    (0, "萃取不足\n+太淡", ["酸澀", "水感", "花生味"], (255, 183, 77)),
    # Top-Right
    (45, "萃取不足", ["青澀", "檸檬酸", "尖銳"], (255, 138, 101)),
    # Right (Under-extracted + Strong)
    (90, "萃取不足\n+太濃", ["刺激", "酸辣", "收斂"], (239, 83, 80)),
    # Bottom-Right
    (135, "太濃", ["厚重", "黏膩", "壓迫"], (186, 104, 200)),
    # Bottom (Over-extracted + Strong)
    (180, "萃取過度\n+太濃", ["苦澀", "焦味", "煙味"], (149, 117, 205)),
    # Bottom-Left
    (225, "萃取過度", ["乾澀", "空洞", "木質"], (100, 181, 246)),
    # Left (Over-extracted + Weak)
    (270, "萃取過度\n+太淡", ["苦水", "稀薄", "灰燼"], (129, 199, 132)),
    # Top-Left
    (315, "太淡", ["無味", "茶感", "平淡"], (220, 231, 117)),
]

img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(img)

# Draw concentric rings
radii = [650, 500, 350, 200, 100]
ring_colors = [COLORS['ring4'], COLORS['ring3'], COLORS['ring2'], COLORS['ring1'], COLORS['center']]

for r, color in zip(radii, ring_colors):
    draw.ellipse(
        [CENTER[0] - r, CENTER[1] - r, CENTER[0] + r, CENTER[1] + r],
        fill=color, outline=COLORS['axis_line'], width=1
    )

# Draw section dividers (8 lines)
for i in range(8):
    angle = math.radians(i * 45 - 90)
    x_end = CENTER[0] + 650 * math.cos(angle)
    y_end = CENTER[1] + 650 * math.sin(angle)
    draw.line([CENTER, (x_end, y_end)], fill=COLORS['axis_line'], width=1)

# Draw center text
center_texts = ["完美", "順滑·甜美", "多汁·豐富"]
for i, txt in enumerate(center_texts):
    bbox = draw.textbbox((0, 0), txt, font=font_center if i == 0 else font_section)
    tw = bbox[2] - bbox[0]
    y_offset = -30 + i * 35
    draw.text(
        (CENTER[0] - tw // 2, CENTER[1] + y_offset),
        txt,
        fill=(255, 255, 255) if i == 0 else COLORS['text_dark'],
        font=font_center if i == 0 else font_section
    )

# Draw section labels
for angle_deg, label, flavors, color in SECTIONS:
    # Position label at radius ~420
    angle_rad = math.radians(angle_deg - 90 + 22.5)  # offset to center of section
    label_r = 420
    lx = CENTER[0] + label_r * math.cos(angle_rad)
    ly = CENTER[1] + label_r * math.sin(angle_rad)
    
    # Draw label
    lines = label.split('\n')
    for j, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font_section)
        tw = bbox[2] - bbox[0]
        draw.text(
            (lx - tw // 2, ly - 15 + j * 28),
            line,
            fill=COLORS['text_dark'],
            font=font_section
        )
    
    # Draw flavors at radius ~570
    flavor_r = 570
    fx = CENTER[0] + flavor_r * math.cos(angle_rad)
    fy = CENTER[1] + flavor_r * math.sin(angle_rad)
    flavor_text = " · ".join(flavors)
    bbox = draw.textbbox((0, 0), flavor_text, font=font_detail)
    tw = bbox[2] - bbox[0]
    draw.text(
        (fx - tw // 2, fy - 10),
        flavor_text,
        fill=COLORS['text_mid'],
        font=font_detail
    )

# Draw axis labels (4 directions)
axis_labels = [
    (CENTER[0], 30, "萃取更少 ← 磨粗 / 沖短"),
    (CENTER[0], HEIGHT - 60, "萃取更多 → 磨幼 / 沖耐"),
    (30, CENTER[1], "減少咖啡 ↑"),
    (WIDTH - 220, CENTER[1], "↓ 增加咖啡"),
]

# Top axis
draw.text((CENTER[0] - 150, 25), "↑ 萃取更少（磨粗 / 沖短）", fill=COLORS['text_dark'], font=font_axis)
# Bottom axis
draw.text((CENTER[0] - 150, HEIGHT - 55), "↓ 萃取更多（磨幼 / 沖耐）", fill=COLORS['text_dark'], font=font_axis)
# Left axis
draw.text((25, CENTER[1] - 12), "← 減少咖啡（加水 / 減粉）", fill=COLORS['text_dark'], font=font_axis)
# Right axis
draw.text((WIDTH - 350, CENTER[1] - 12), "增加咖啡（減水 / 加粉）→", fill=COLORS['text_dark'], font=font_axis)

# Title
title = "咖啡指南針 Coffee Compass"
bbox = draw.textbbox((0, 0), title, font=font_title)
tw = bbox[2] - bbox[0]
draw.text((CENTER[0] - tw // 2, HEIGHT - 120), title, fill=COLORS['text_dark'], font=font_title)

# Subtitle
subtitle = "基於 Barista Hustle 原版 · 中文翻譯"
bbox = draw.textbbox((0, 0), subtitle, font=font_detail)
tw = bbox[2] - bbox[0]
draw.text((CENTER[0] - tw // 2, HEIGHT - 70), subtitle, fill=COLORS['text_mid'], font=font_detail)

# Save
output_path = os.path.join(os.path.dirname(__file__), "Coffee_Compass_Chinese.png")
img.save(output_path, "PNG", dpi=(300, 300))
print(f"Saved to: {output_path}")
