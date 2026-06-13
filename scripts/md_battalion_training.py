# -*- coding: utf-8 -*-
"""
MOD 追加 battalion の training_time を MD 用に調整

MD Beta 標準: modern armor = 180
TSF MOD 設計:
  通常戦術機 line battalion : 180
  支援戦術機 line battalion : 150
  攻撃支援 (asa) line       : 180
  戦術支援 (tsa) line       : 180
  特務戦術機 (精鋭)         : 240
  XG (凄ノ皇 超兵器)        : 400 (維持)
  各 support_company        : 150
"""
import re
import os

MOD = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod"

# subunit_id -> new training_time
NEW_TIMES = {
    "MVLV_tsf_battalion":                    180,
    "MVLV_tsf_support_battalion":            150,
    "MVLV_tsf_support_company":              150,
    "MVLV_tsf_specialForces_battalion":      240,
    "MVLV_asa_battalion":                    180,
    "MVLV_asa_support_company":              150,
    "MVLV_tsa_battalion":                    180,
    "MVLV_tsa_support":                      150,
    "MVLV_xg_battalion":                     400,  # 維持
}

FILES = [
    "MVLV_tsf_battalion.txt",
    "MVLV_tsf_support_battalion.txt",
    "MVLV_tsf_specialForces_battalion.txt",
    "MVLV_asa_battalion.txt",
    "MVLV_tsa_battalion.txt",
    "MVLV_xg_battalion.txt",
]


def find_block_end(s, open_pos):
    depth = 1
    i = open_pos + 1
    while i < len(s) and depth > 0:
        c = s[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


total = 0
for fname in FILES:
    path = os.path.join(MOD, "common", "units", fname)
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        c = f.read()

    # 各 sub_unit ブロックを処理
    new_chunks = []
    last = 0
    for m in re.finditer(r'(\t)(MVLV_\w+)\s*=\s*\{', c):
        sid = m.group(2)
        if sid not in NEW_TIMES:
            continue
        # ブロック終端
        bend = find_block_end(c, m.end() - 1)
        new_chunks.append(c[last:m.start()])
        block = c[m.start():bend + 1]
        new_t = NEW_TIMES[sid]
        # training_time を置換（ブロック内のみ）
        new_block, n = re.subn(
            r'(training_time\s*=\s*)\d+',
            rf'\g<1>{new_t}',
            block
        )
        if n > 0:
            print(f"  {sid:50s} -> {new_t} ({n}個置換)")
            total += n
        new_chunks.append(new_block)
        last = bend + 1
    new_chunks.append(c[last:])
    c = "".join(new_chunks)

    with open(path, "w", encoding="utf-8") as f:
        f.write(c)

print(f"\n合計: {total} training_time 更新")
