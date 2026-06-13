# -*- coding: utf-8 -*-
"""
countrytechtreeview.gui に元 MOD の MVLV folder セクションを追加マージ（v2: ブレース追跡を正しく）
"""
import re
import os

MD_ORIG = r"C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\3372337928\interface\countrytechtreeview.gui"
OUR = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod\interface\countrytechtreeview.gui"

with open(MD_ORIG, "r", encoding="utf-8", errors="replace") as f:
    orig_content = f.read()
with open(OUR, "r", encoding="utf-8", errors="replace") as f:
    our_content = f.read()


def extract_nth(content, start_pattern, end_pattern, n):
    """n番目（1始まり）のマーカーペアから中身を抽出（マーカー含まない）"""
    starts = [m.end() for m in re.finditer(start_pattern, content, re.MULTILINE)]
    ends = [m.start() for m in re.finditer(end_pattern, content, re.MULTILINE)]
    if len(starts) < n or len(ends) < n:
        return ""
    return content[starts[n - 1]:ends[n - 1]]


# 元 MOD の3セクション
section_folders = extract_nth(orig_content,
                              r"################################################## MVLV mod start$",
                              r"################################################## MVLV mod end$", 1)
section_tabs = extract_nth(orig_content,
                           r"##################### MVLV mod start##################",
                           r"################################################## MVLV mod end##########################", 1)
section_smallitems = extract_nth(orig_content,
                                  r"################################################## MVLV mod start###########################",
                                  r"################################################## MVLV mod end################################", 1)
print("folders:", len(section_folders), "tabs:", len(section_tabs), "smallitems:", len(section_smallitems))


def find_window_end(content, window_name):
    """名前指定で containerWindowType ブロックの開始/終了位置を返す
    返り値: (block_start, opening_brace, closing_brace)
    """
    pattern = re.compile(r'containerWindowType\s*=\s*\{', re.MULTILINE)
    for m in pattern.finditer(content):
        opening = m.end() - 1  # { の位置
        # この { の内側に name = "<window_name>" があるか確認（直後 50 行ほど）
        check_region = content[opening:opening + 500]
        name_match = re.search(r'name\s*=\s*"' + re.escape(window_name) + r'"', check_region)
        if not name_match:
            continue
        # ブレースを辿って終端探す
        depth = 1
        i = opening + 1
        while i < len(content) and depth > 0:
            c = content[i]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return (m.start(), opening, i)
            i += 1
    return None


# countrytechtreeview の範囲
ctt = find_window_end(our_content, "countrytechtreeview")
if ctt is None:
    print("ERROR: countrytechtreeview not found")
    exit(1)
ctt_start, ctt_open, ctt_close = ctt
print("countrytechtreeview at", ctt_start, "open", ctt_open, "close", ctt_close)

# folder_tabs の範囲（countrytechtreeview 内部）
ft = find_window_end(our_content[:ctt_close], "folder_tabs")
if ft is None:
    print("WARN: folder_tabs not found - tabs section will go to countrytechtreeview end")
    folder_tabs_close = -1
else:
    folder_tabs_close = ft[2]
    print("folder_tabs at", ft[0], "open", ft[1], "close", folder_tabs_close)

# 挿入順序: 後ろから前へ挿入してインデックスが狂わないように
new = our_content

# 1. countrytechtreeview の閉じ } 直前に folder windows と small items を挿入
insert_str_1 = "\n# === MVLV mod folder windows ===\n" + section_folders + "\n# === MVLV mod small items ===\n" + section_smallitems + "\n"
new = new[:ctt_close] + insert_str_1 + new[ctt_close:]
print("Inserted folder windows + small items at countrytechtreeview close")

# 2. folder_tabs の閉じ } 直前に tabs を挿入（位置は変わらない）
if folder_tabs_close > 0:
    insert_str_2 = "\n# === MVLV mod tabs ===\n" + section_tabs + "\n"
    new = new[:folder_tabs_close] + insert_str_2 + new[folder_tabs_close:]
    print("Inserted tabs at folder_tabs close")

with open(OUR, "w", encoding="utf-8") as f:
    f.write(new)

print("done. new size:", len(new))
