# -*- coding: utf-8 -*-
"""
techtree_MVLV_tsf_folder_small_item を countrytechtreeview の中から
トップレベル（guiTypes 直下）に移動する
"""
import re

OUR = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod\interface\countrytechtreeview.gui"

with open(OUR, "r", encoding="utf-8", errors="replace") as f:
    content = f.read()


def find_block_end_from_pos(content, start_pos):
    depth = 1
    i = start_pos
    while i < len(content) and depth > 0:
        c = content[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


# techtree_MVLV_tsf_folder_small_item のブロックを抽出
m = re.search(r'containerWindowType\s*=\s*\{\s*name\s*=\s*"techtree_MVLV_tsf_folder_small_item"', content)
if not m:
    print("ERROR: not found")
    exit(1)

block_start = m.start()
# 直前の空白
while block_start > 0 and content[block_start - 1] in " \t":
    block_start -= 1
if block_start > 0 and content[block_start - 1] == "\n":
    block_start -= 1

block_close = find_block_end_from_pos(content, m.end())
if block_close < 0:
    print("ERROR: no close brace")
    exit(1)

# block を抽出
block_text = content[block_start:block_close + 1]

# 現在の位置を削除
content = content[:block_start] + content[block_close + 1:]

# countrytechtreeview の終端を見つける
m_ctt = re.search(r'containerWindowType\s*=\s*\{\s*name\s*=\s*"countrytechtreeview"', content)
if not m_ctt:
    print("ERROR: no countrytechtreeview")
    exit(1)
ctt_close = find_block_end_from_pos(content, m_ctt.end())

# countrytechtreeview の閉じ } の直後に block を挿入（top-level guiTypes 直下）
insertion = "\n\n# === techtree_MVLV_tsf_folder_small_item moved to top-level ===" + block_text + "\n"
content = content[:ctt_close + 1] + insertion + content[ctt_close + 1:]

opens = content.count("{")
closes = content.count("}")
print(f"ブレース: {opens}/{closes} diff={opens - closes}")

with open(OUR, "w", encoding="utf-8") as f:
    f.write(content)

# 検証
m_new = re.search(r'name\s*=\s*"techtree_MVLV_tsf_folder_small_item"', content)
depth = 0
for i, c in enumerate(content[:m_new.start()]):
    if c == "{":
        depth += 1
    elif c == "}":
        depth -= 1
print(f"移動後 depth: {depth}")
