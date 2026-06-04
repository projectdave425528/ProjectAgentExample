"""
Coffee Compass 中文版 - 合併兩張圖 + 中文翻譯
"""
from PIL import Image, ImageDraw, ImageFont
import os

# 載入圖片
base = Image.open('compass-base.jpg')
guide = Image.open('compass-guide.jpg')

# 兩張都係 1600x1600，左右拼接
# 最終圖：3200 wide x 1600 high + 底部中文翻譯區 600px
canvas_width = 3200
canvas_height = 2200
canvas = Image.new('RGB', (canvas_width, canvas_height), (255, 255, 255))

# 貼上兩張原圖
canvas.paste(base, (0, 0))
canvas.paste(guide, (1600, 0))

# 載入字型
font_path = 'C:/Windows/Fonts/NotoSansTC-VF.ttf'
if not os.path.exists(font_path):
    font_path = 'C:/Windows/Fonts/msjh.ttc'

draw = ImageDraw.Draw(canvas)

# 字型大小
title_font = ImageFont.truetype(font_path, 48)
heading_font = ImageFont.truetype(font_path, 36)
body_font = ImageFont.truetype(font_path, 28)
small_font = ImageFont.truetype(font_path, 24)

# 標題
draw.text((canvas_width // 2, 1620), "☕ 咖啡沖煮羅盤 - 中文翻譯指南", 
           fill=(50, 50, 50), font=title_font, anchor="mt")

# 左邊：羅盤風味翻譯
left_x = 100
y_start = 1700

# 中心風味（理想）
draw.text((left_x, y_start), "【中心（理想風味）】", fill=(0, 100, 0), font=heading_font)
center_flavors = "Smooth 順滑 | Sweet 甜美 | Juicy 多汁 | Round 圓潤 | Transparent 通透"
draw.text((left_x, y_start + 45), center_flavors, fill=(60, 60, 60), font=body_font)

# 外圍風味缺陷
y = y_start + 100
draw.text((left_x, y), "【外圍風味缺陷（需要調整）】", fill=(180, 0, 0), font=heading_font)

defects = [
    ("上方 (萃取不足+太濃)", "Sour 酸 | Vegetal 菜味 | Cereal 穀物味 | Under-developed 發展不足"),
    ("下方 (過萃+太淡)", "Bitter 苦 | Dry 乾澀 | Ashy 灰燼味 | Harsh 刺激"),
    ("左方 (太濃)", "Intense 過濃 | Overwhelming 壓迫感 | Heavy 沉重"),
    ("右方 (太淡)", "Watery 水感 | Thin 單薄 | Insipid 寡淡 | Tea-like 茶感"),
]

for label, desc in defects:
    y += 45
    draw.text((left_x + 20, y), f"• {label}", fill=(80, 80, 80), font=body_font)
    y += 35
    draw.text((left_x + 40, y), desc, fill=(120, 120, 120), font=small_font)

# 右邊：調整方法翻譯
right_x = 1700
y = y_start

draw.text((right_x, y), "【調整方法】", fill=(0, 50, 150), font=heading_font)

adjustments = [
    ("研磨更細 / 沖煮更久", "→ 萃取更多 (Extract More)", "(180, 80, 0)"),
    ("研磨更粗 / 沖煮更短", "→ 萃取更少 (Extract Less)", "(0, 130, 0)"),
    ("減少咖啡粉量 / 增加水量", "→ 減少濃度 (Less Coffee)", "(0, 80, 180)"),
    ("增加咖啡粉量 / 減少水量", "→ 增加濃度 (More Coffee)", "(150, 0, 150)"),
]

y += 50
for method, result, color_str in adjustments:
    color = eval(color_str)
    draw.text((right_x, y), f"• {method}", fill=color, font=body_font)
    y += 38
    draw.text((right_x + 20, y), result, fill=(80, 80, 80), font=small_font)
    y += 50

# 使用說明
y += 20
draw.text((right_x, y), "【使用方法】", fill=(0, 50, 150), font=heading_font)
y += 50
steps = [
    "1. 沖一杯咖啡",
    "2. 品嚐並找出不良風味",
    "3. 在左圖羅盤找到該風味位置",
    "4. 根據右圖指引調整參數",
    "5. 重新沖煮，直到風味回到中心",
]
for step in steps:
    draw.text((right_x, y), step, fill=(60, 60, 60), font=small_font)
    y += 35

# 底部版權
draw.text((canvas_width // 2, canvas_height - 30), 
          "原圖來源：Barista Hustle (baristahustle.com) | 中文翻譯版", 
          fill=(150, 150, 150), font=small_font, anchor="mb")

# 儲存
output_path = 'coffee-compass-zh-combined.png'
canvas.save(output_path, quality=95)
print(f'已儲存：{output_path} ({canvas_width}x{canvas_height})')
