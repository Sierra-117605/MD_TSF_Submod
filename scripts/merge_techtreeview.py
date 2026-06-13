# -*- coding: utf-8 -*-
"""
countrytechtreeview.gui に元 MOD の MVLV folder セクションを追加マージ
"""
import re
import os

MD_ORIG = r"C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\3372337928\interface\countrytechtreeview.gui"
OUR = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod\interface\countrytechtreeview.gui"

with open(MD_ORIG, "r", encoding="utf-8", errors="replace") as f:
    orig_lines = f.readlines()
with open(OUR, "r", encoding="utf-8", errors="replace") as f:
    our_content = f.read()

# 元 MOD の MVLV セクション抽出（マーカー行は含まない）
def extract_section(lines, start_marker_pattern, end_marker_pattern):
    start_idx = None
    end_idx = None
    for i, line in enumerate(lines):
        if re.search(start_marker_pattern, line):
            start_idx = i + 1
            break
    if start_idx is None:
        return ""
    for i in range(start_idx, len(lines)):
        if re.search(end_marker_pattern, lines[i]):
            end_idx = i
            break
    if end_idx is None:
        return ""
    return "".join(lines[start_idx:end_idx])

# セクション1: folder windows (UNI_tsf, MVLV_tsf, MVLV_xg)
section1 = extract_section(orig_lines, r"##################### MVLV mod start", r"MVLV mod end")
# 元 MOD の line 2845 vs 3601 を区別
# 1番目の MVLV mod start (行2845) からの抽出を再試行
def extract_nth(lines, start_pattern, end_pattern, n):
    """n番目のマーカーペアから抽出"""
    starts = []
    ends = []
    for i, line in enumerate(lines):
        if re.search(start_pattern, line):
            starts.append(i)
        if re.search(end_pattern, line):
            ends.append(i)
    if len(starts) < n or len(ends) < n:
        return ""
    s = starts[n-1] + 1
    e = ends[n-1]
    return "".join(lines[s:e])

# セクション1: 大きな folder window 定義 (2845-3499)
section_folders = extract_nth(orig_lines, r"################################################## MVLV mod start$",
                                r"################################################## MVLV mod end$", 1)

# セクション2: tabs 定義 (3601-3661)
section_tabs = extract_nth(orig_lines, r"##################### MVLV mod start##################",
                            r"################################################## MVLV mod end##########################", 1)

# セクション3: 小窓 items 定義 (4853-5513)
section_smallitems = extract_nth(orig_lines, r"################################################## MVLV mod start###########################",
                                  r"################################################## MVLV mod end################################", 1)

print("section_folders 文字数:", len(section_folders))
print("section_tabs 文字数:", len(section_tabs))
print("section_smallitems 文字数:", len(section_smallitems))

# 我々のファイルへの挿入
# 最も安全な方法: countrytechtreeview のメインウィンドウの } 直前に挿入
# 各セクションごとに別の挿入ポイントが必要

# セクション1（folder windows）の挿入点:
# 最後の "containerWindowType = {" で "name = "infantry_folder"" 等の folder 定義の後

# 簡易アプローチ: countrytechtreeview の最後の } 直前に全部詰める
# countrytechtreeview ブロックを探す
m = re.search(r'containerWindowType\s*=\s*\{\s*name\s*=\s*"countrytechtreeview"', our_content)
if not m:
    print("ERROR: countrytechtreeview window が見つからない")
    exit(1)

# 対応する閉じ }
brace_pos = our_content.find("{", m.end() - 1)
depth = 1
i = brace_pos + 1
while i < len(our_content) and depth > 0:
    c = our_content[i]
    if c == "{":
        depth += 1
    elif c == "}":
        depth -= 1
        if depth == 0:
            break
    i += 1
ctt_end = i  # countrytechtreeview の閉じ } 位置

# folder_tabs ブロックを探す（タブの場所）
m_tabs = re.search(r'containerWindowType\s*=\s*\{\s*name\s*=\s*"folder_tabs"', our_content[:ctt_end])
folder_tabs_end = -1
if m_tabs:
    brace_pos2 = our_content.find("{", m_tabs.end() - 1)
    depth = 1
    i = brace_pos2 + 1
    while i < len(our_content) and depth > 0:
        c = our_content[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                folder_tabs_end = i
                break
        i += 1

# 挿入
# まず folder_tabs の } 直前に tab セクション挿入
new_content = our_content
if folder_tabs_end > 0:
    insert_point = folder_tabs_end
    new_content = new_content[:insert_point] + "\n# === MVLV mod tabs ===\n" + section_tabs + "\n" + new_content[insert_point:]
    # ctt_end も更新
    ctt_end += len("\n# === MVLV mod tabs ===\n") + len(section_tabs) + 1

# 次に countrytechtreeview の } 直前に folder セクション+ smallitems 挿入
new_content = new_content[:ctt_end] + "\n# === MVLV mod folder windows ===\n" + section_folders + "\n# === MVLV mod small items ===\n" + section_smallitems + "\n" + new_content[ctt_end:]

with open(OUR, "w", encoding="utf-8") as f:
    f.write(new_content)

print("マージ完了")
print("新ファイルサイズ:", len(new_content), "bytes")
