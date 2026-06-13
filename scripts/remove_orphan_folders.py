# -*- coding: utf-8 -*-
"""
countrytechtreeview.gui から不要な孤立テンプレートを削除
- techtree_TSF_neo_folder_item / _small_item
- techtree_TSF_module_folder_item / _small_item
- techtree_tsf_folder_item / _small_item (旧 tsf_folder の残骸)
"""
import re

OUR = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod\interface\countrytechtreeview.gui"

with open(OUR, "r", encoding="utf-8", errors="replace") as f:
    content = f.read()


def find_block_end(content, open_brace_pos):
    depth = 1
    i = open_brace_pos + 1
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


TARGETS = [
    "techtree_TSF_neo_folder_item",
    "techtree_TSF_neo_folder_small_item",
    "techtree_TSF_module_folder_item",
    "techtree_TSF_module_folder_small_item",
    "techtree_tsf_folder_item",
    "techtree_tsf_folder_small_item",
]

removed = 0
for target in TARGETS:
    while True:
        pattern = re.compile(r'containerWindowType\s*=\s*\{\s*name\s*=\s*"' + re.escape(target) + r'"')
        m = pattern.search(content)
        if not m:
            break
        # block 開始位置
        block_start = m.start()
        # 直前の空白/改行
        while block_start > 0 and content[block_start - 1] in " \t":
            block_start -= 1
        if block_start > 0 and content[block_start - 1] == "\n":
            block_start -= 1
        # 開き { 位置
        open_brace = m.end() - 1
        block_close = find_block_end(content, open_brace)
        if block_close < 0:
            break
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
