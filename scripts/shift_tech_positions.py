# -*- coding: utf-8 -*-
"""
MVLV_NSB_TSF.txt の全テック position を右にシフト + 重なり緩和
- 全テック x 値を 2 倍にして間隔を広げる（ただし大きすぎないよう調整）
- さらに +3 オフセットで右にずらす
"""
import re
import os

path = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod\common\technologies\MVLV_NSB_TSF.txt"

with open(path, "r", encoding="utf-8", errors="replace") as f:
    content = f.read()

# folder ブロック内の position の x を変換
# 元の x 範囲 -11 ~ 20、つまり 32 列
# 倍率 x 1.5 で範囲を広げる: -16 ~ 30 (47 列に拡張)
# さらに +5 オフセット: -11 ~ 35
# でも負の値は left margin 入りでちょっとなので、+11 で全部正にする
# 結果: 0 ~ 46

X_MULTIPLIER = 1.5  # 倍率（重なり緩和）
X_OFFSET = 11       # 全部正の値にする


def transform_x(x):
    return int(round(x * X_MULTIPLIER + X_OFFSET))


def replace_x_in_folder(m):
    """folder { name = MVLV_tsf_folder position = { x = N y = N } } の x を変換"""
    full = m.group(0)
    # x の数値を抽出して置換
    x_match = re.search(r"x\s*=\s*(-?\d+)", full)
    if not x_match:
        return full
    old_x = int(x_match.group(1))
    new_x = transform_x(old_x)
    new = re.sub(r"x\s*=\s*-?\d+", f"x = {new_x}", full, count=1)
    return new


# folder ブロック全体（中の position 含む）をマッチして変換
folder_pattern = re.compile(
    r'folder\s*=\s*\{\s*name\s*=\s*MVLV_tsf_folder\s+position\s*=\s*\{\s*x\s*=\s*(-?\d+)\s+y\s*=\s*(-?\d+)\s*\}\s*\}',
    re.MULTILINE
)

count = 0
def replacer(m):
    global count
    count += 1
    old_x = int(m.group(1))
    old_y = int(m.group(2))
    new_x = transform_x(old_x)
    # フォーマット保持
    return f"folder = {{\n\t\t\tname = MVLV_tsf_folder\n\t\t\tposition = {{\n\t\t\t\tx = {new_x}\n\t\t\t\ty = {old_y}\n\t\t\t}}\n\t\t}}"


new_content = folder_pattern.sub(replacer, content)
print(f"変換した position 数: {count}")

with open(path, "w", encoding="utf-8") as f:
    f.write(new_content)

# 検証
xs = []
for m in re.finditer(r"position\s*=\s*\{\s*x\s*=\s*(-?\d+)", new_content):
    xs.append(int(m.group(1)))
print(f"新 x 範囲: {min(xs)} ~ {max(xs)}")
print(f"新 x ユニーク数: {len(set(xs))}")
