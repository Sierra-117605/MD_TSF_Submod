# -*- coding: utf-8 -*-
"""
MVLV_NSB_TSF.txt から `picture = GFX_...` 行を全削除
HOI4 tech は picture フィールド未対応 -> 「Unknown modifier」エラーで
後続の enable_subunits 等が処理されない症状の修正
"""
import re
import os

MOD = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod"
TECH = os.path.join(MOD, "common", "technologies", "MVLV_NSB_TSF.txt")

with open(TECH, "r", encoding="utf-8", errors="replace") as f:
    content = f.read()

# `\t\tpicture = GFX_...` の行を丸ごと削除
# (タブ+picture+任意の値+改行)
new_content, n = re.subn(r'\n[\t ]*picture\s*=\s*\S+[ \t]*', '', content)

with open(TECH, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"picture = ... 行を削除: {n} 件")
