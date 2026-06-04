"""
Coffee Compass 中文版 - 單一圓形羅盤
合併風味 + 調整方法到一個圓形圖
"""
from PIL import Image, ImageDraw, ImageFont
import math
import os

# 設定
SIZE = 2400
CENTER = SIZE // 2
canvas = Image.new('RGB', (SIZE, SIZE), (255, 255, 255))
draw = ImageDraw.Draw(canvas)

# 字型
font_path = 'C:/Windows/Fonts/NotoSansTC-VF.ttf'
if not os.path.exists(font_path):
    font_path = 'C:/Windows/Fonts/msjh.ttc'

title_font = ImageFont.truetype(font_path, 52)
zone_font = ImageFont.truetype(font_path, 34)
flavor_font = ImageFont.truetype(font_path, 26)
small_font = ImageFont.truetype(font_path, 22)
adjust_font = ImageFont.truetype(font_path, 28)
center_font = ImageFont.truetype(font_path, 38)

# 顏色
colors = {
    'center': (76, 153, 0),        # 綠色 - 理想
    'ring_outer': (240, 240, 240),
    'ring_mid': (250, 250, 250),
    'sour': (255, 200, 0),         # 黃色
    'bitter': (139, 69, 19),       # 棕色
    'strong': (180, 0, 0),         # 紅色
    'weak': (100, 149, 237),       # 藍色
    'extract_more': (220, 100, 0), # 橙色
    'extract_less': (0, 150, 50),  # 綠色
    'more_coffee': (150, 0, 150),  # 紫色
    'less_coffee': (0, 100, 200),  # 天藍
}

# 圓圈半徑
R_OUTER = 1050      # 最外圈（風味缺陷）
R_MID_OUTER = 850   # 中外圈（次要風味）
R_MID = 650         # 中圈（調整方法）
R_INNER = 400       # 內圈（方向標籤）
R_CENTER = 200      # 中心（理想風味）

# 畫圓圈
def draw_circle(r, fill=None, outline=(200, 200, 200), width=2):
    draw.ellipse(
        [CENTER - r, CENTER - r, CENTER + r, CENTER + r],
        fill=fill, outline=outline, width=width
    )

# 畫底色圈
draw_circle(R_OUTER, fill=(248, 248, 248), outline=(180, 180, 180), width=3)
draw_circle(R_MID_OUTER, fill=(252, 252, 252), outline=(200, 200, 200), width=2)
draw_circle(R_MID, fill=(255, 255, 255), outline=(200, 200, 200), width=2)
draw_circle(R_INNER, fill=(240, 255, 240), outline=(180, 200, 180), width=2)
draw_circle(R_CENTER, fill=(220, 255, 220), outline=(100, 180, 100), width=3)

# 畫分隔線（8 等分）
for i in range(8):
    angle = math.radians(i * 45 - 90)
    x1 = CENTER + int(R_CENTER * math.cos(angle))
    y1 = CENTER + int(R_CENTER * math.sin(angle))
    x2 = CENTER + int(R_OUTER * math.cos(angle))
    y2 = CENTER + int(R_OUTER * math.sin(angle))
    draw.line([x1, y1, x2, y2], fill=(220, 220, 220), width=1)

# 畫粗分隔線（4 等分 - 主方向）
for i in range(4):
    angle = math.radians(i * 90 - 90)
    x1 = CENTER + int(R_CENTER * math.cos(angle))
    y1 = CENTER + int(R_CENTER * math.sin(angle))
    x2 = CENTER + int(R_OUTER * math.cos(angle))
    y2 = CENTER + int(R_OUTER * math.sin(angle))
    draw.line([x1, y1, x2, y2], fill=(180, 180, 180), width=2)

# 中心文字
draw.text((CENTER, CENTER - 30), "理想風味", fill=colors['center'], font=center_font, anchor="mm")
draw.text((CENTER, CENTER + 20), "順滑·甜美", fill=colors['center'], font=zone_font, anchor="mm")
draw.text((CENTER, CENTER + 60), "多汁·圓潤", fill=colors['center'], font=zone_font, anchor="mm")

# 8 個方向嘅風味區域
# 定義：角度(度), 方向名, 風味列表, 顏色
# 上=萃取不足, 下=過度萃取, 左=太濃, 右=太淡
# 對角線=混合

sectors = [
    # (角度, 距離環, 標籤, 顏色)
    # 上方 - 萃取不足
    (270, "萃取不足", ["酸味", "青草味", "穀物味"], (200, 150, 0)),
    # 右上 - 萃取不足 + 太淡
    (315, "不足+淡", ["酸澀", "花生味", "未熟"], (150, 150, 100)),
    # 右方 - 太淡
    (0, "太淡", ["水感", "單薄", "寡淡", "茶感"], (100, 149, 237)),
    # 右下 - 過萃 + 太淡
    (45, "過萃+淡", ["空洞", "乏味", "紙板味"], (100, 120, 150)),
    # 下方 - 過度萃取
    (90, "過度萃取", ["苦味", "乾澀", "灰燼味"], (139, 69, 19)),
    # 左下 - 過萃 + 太濃
    (135, "過萃+濃", ["刺激", "尖銳", "焦苦"], (150, 50, 50)),
    # 左方 - 太濃
    (180, "太濃", ["過濃", "壓迫感", "沉重"], (180, 0, 0)),
    # 左上 - 萃取不足 + 太濃
    (225, "不足+濃", ["鹹味", "澀感", "粗糙"], (150, 100, 0)),
]

# 放置風味文字
for angle_deg, label, flavors, color in sectors:
    angle = math.radians(angle_deg)
    
    # 方向標籤（中圈）
    lx = CENTER + int(R_INNER * 0.7 * math.cos(angle))
    ly = CENTER + int(R_INNER * 0.7 * math.sin(angle))
    draw.text((lx, ly), label, fill=color, font=zone_font, anchor="mm")
    
    # 風味詞（外圈）
    for i, flavor in enumerate(flavors):
        offset = (i - len(flavors) / 2 + 0.5) * 40
        # 計算垂直於半徑方向嘅偏移
        perp_angle = angle + math.pi / 2
        fx = CENTER + int(R_MID_OUTER * 0.85 * math.cos(angle)) + int(offset * math.cos(perp_angle))
        fy = CENTER + int(R_MID_OUTER * 0.85 * math.sin(angle)) + int(offset * math.sin(perp_angle))
        draw.text((fx, fy), flavor, fill=color, font=flavor_font, anchor="mm")

# 調整方法 - 放在四個象限嘅中圈位置
adjustments = [
    # (角度, 文字行, 顏色)
    (270, ["▲ 萃取更多", "研磨更細", "沖煮更久"], colors['extract_more']),
    (90, ["▼ 萃取更少", "研磨更粗", "沖煮更短"], colors['extract_less']),
    (180, ["◀ 增加濃度", "加多咖啡粉", "或減少水量"], colors['more_coffee']),
    (0, ["▶ 減少濃度", "減少咖啡粉", "或增加水量"], colors['less_coffee']),
]

for angle_deg, lines, color in adjustments:
    angle = math.radians(angle_deg)
    base_x = CENTER + int((R_MID + 30) * math.cos(angle))
    base_y = CENTER + int((R_MID + 30) * math.sin(angle))
    
    for i, line in enumerate(lines):
        y_offset = (i - 1) * 35
        # 偏移方向跟半徑垂直
        if angle_deg in [0, 180]:
            draw.text((base_x, base_y + y_offset), line, fill=color, font=adjust_font, anchor="mm")
        else:
            draw.text((base_x + 0, base_y + y_offset), line, fill=color, font=adjust_font, anchor="mm")

# 標題
draw.text((CENTER, 60), "☕ 咖啡沖煮羅盤（Coffee Compass）", fill=(50, 50, 50), font=title_font, anchor="mt")

# 底部說明
draw.text((CENTER, SIZE - 80), "找到你嘅風味問題 → 跟隨箭頭方向調整 → 回到中心「理想風味」", 
          fill=(100, 100, 100), font=small_font, anchor="mm")
draw.text((CENTER, SIZE - 45), "原設計：Barista Hustle | 中文翻譯版", 
          fill=(180, 180, 180), font=small_font, anchor="mm")

# 儲存
output = 'coffee-compass-zh-circle.png'
canvas.save(output, quality=95)
print(f'已儲存：{output} ({SIZE}x{SIZE})')
