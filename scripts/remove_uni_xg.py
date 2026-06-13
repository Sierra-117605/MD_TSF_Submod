# -*- coding: utf-8 -*-
"""
countrytechtreeview.gui から UNI_tsf_folder と MVLV_xg_folder 関連を全削除
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


# 削除対象 name 一覧（containerWindowType と buttonType と iconType の name）
TARGETS = [
    "UNI_tsf_folder",
    "UNI_tsf_folder_tab",
    "highlight_UNI_tsf_folder",
    "techtree_UNI_tsf_folder_item",
    "techtree_UNI_tsf_folder_small_item",
    "MVLV_xg_folder",
    "MVLV_xg_folder_tab",
    "highlight_MVLV_xg_folder",
    "techtree_MVLV_xg_folder_item",
    "techtree_MVLV_xg_folder_small_item",
]

removed = 0
# 各 target を見つけて削除
for target in TARGETS:
    while True:
        pattern = re.compile(r'(containerWindowType|buttonType|iconType)\s*=\s*\{\s*name\s*=\s*"' + re.escape(target) + r'"')
        m = pattern.search(content)
        if not m:
            break
        # この block の開始位置
        block_start = m.start()
        # 直前の空白/改行を含めて削除開始
        while block_start > 0 and content[block_start - 1] in " \t":
            block_start -= 1
        if block_start > 0 and content[block_start - 1] == "\n":
            block_start -= 1
        # 閉じ } 探す（regex には開き { が含まれる）
        block_close = find_block_end_from_pos(content, m.end())
        if block_close < 0:
            break
        # 削除
        content = content[:block_start] + content[block_close + 1:]
        removed += 1
        print(f"  removed: {target}")

# ブレースバランス
opens = content.count("{")
closes = content.count("}")
print(f"\nブレース: {{:{opens}, }}:{closes}, diff:{opens - closes}")

with open(OUR, "w", encoding="utf-8") as f:
    f.write(content)
print(f"\n削除総数: {removed}")
print(f"新サイズ: {len(content)}")
