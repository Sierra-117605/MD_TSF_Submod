# -*- coding: utf-8 -*-
"""
TSF テックと chassis 装備の年代を MD (2000 開始) 用に調整

帯方式マッピング:
  古い年代 -> 新しい年代
   < 1980 -> 1990 (gen 1 = MD 開始時に既に配備済み)
  1980-89 -> 1995 (gen 1 後期 / gen 2 早期)
  1990-99 -> 2003 (gen 2 後期 / 初期 gen 3)
  2000-03 -> +10 (gen 3 = 2010-2013)
  2005+   -> +10 (gen 4 = 2015)

特例:
  - Susanoo / F-47 系は既に MD-friendly なので維持
  - debug_pack は維持 (allow=no で意味なし)

research_cost 微調整:
  - 0.5 -> 1.0 (最低限)
  - gen 3 framework: 3 -> 4 (難易度感)
  - gen 4 framework: 2 -> 5 (最先端)
"""
import re
import os

MOD = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod"
TECH = os.path.join(MOD, "common", "technologies", "MVLV_NSB_TSF.txt")

CHASSIS_FILES = [
    os.path.join(MOD, "common", "units", "equipment", "MVLV_TSF_chassis.txt"),
    os.path.join(MOD, "common", "units", "equipment", "MVLV_TSF_support_chassis.txt"),
    os.path.join(MOD, "common", "units", "equipment", "MVLV_TSF_specialForces_chassis.txt"),
]


def map_year(old):
    """帯方式年代マッピング"""
    if old < 1980:
        return 1990
    elif old < 1990:
        return 1995
    elif old < 2000:
        return 2003
    else:
        # 2000+
        return old + 10


# === 1. テックファイル start_year 更新 ===
print("=== 1. テック start_year 更新 ===")
with open(TECH, "r", encoding="utf-8", errors="replace") as f:
    c = f.read()

# Susanoo/F-47 を除外（テック ID にこれらを含むものは skip）
SKIP_PREFIXES = ("tsf_susanoo_", "tsf_F-47_")
SKIP_IDS = {"MVLV_research_debug_pack"}

updates = 0
def replace_year(m):
    global updates
    full = m.group(0)
    indent = m.group(1)
    old_year = int(m.group(2))
    new_year = map_year(old_year)
    if new_year == old_year:
        return full
    updates += 1
    return f"{indent}start_year = {new_year}"

# 1tech ずつ処理（Susanoo/F-47 をスキップ）
pattern = re.compile(r'^\t([A-Za-z][\w\-]+)\s*=\s*\{', re.MULTILINE)
new_chunks = []
last = 0
for m in pattern.finditer(c):
    tid = m.group(1)
    # ブロック終端
    depth = 1
    i = m.end()
    while i < len(c) and depth > 0:
        if c[i] == "{":
            depth += 1
        elif c[i] == "}":
            depth -= 1
            if depth == 0:
                break
        i += 1
    block_end = i
    block_start = m.start()

    # 直前まで普通に追加
    new_chunks.append(c[last:block_start])

    block_text = c[block_start:block_end + 1]
    if any(tid.startswith(p) for p in SKIP_PREFIXES) or tid in SKIP_IDS:
        new_chunks.append(block_text)
    else:
        # start_year を更新
        def repl(mm):
            global updates
            indent = mm.group(1)
            old_year = int(mm.group(2))
            new_year = map_year(old_year)
            if new_year != old_year:
                updates += 1
                return f"{indent}start_year = {new_year}"
            return mm.group(0)

        new_block = re.sub(r'([\t ]*)start_year\s*=\s*(\d+)', repl, block_text)
        new_chunks.append(new_block)
    last = block_end + 1
new_chunks.append(c[last:])
c = "".join(new_chunks)

# research_cost の微調整
cost_updates = 0

# 0.5 -> 1.0
def bump_low(m):
    global cost_updates
    cost_updates += 1
    return f"{m.group(1)}research_cost = 1"
c, n = re.subn(r'([\t ]*)research_cost\s*=\s*0\.5\b', bump_low, c)

# gen 3/4 framework は別途
GEN_COST = {
    "MVLV_research_tsf_3_light_framework": 4,
    "MVLV_research_tsf_3_heavy_framework": 4,
    "MVLV_research_tsf_3_maneuver_framework": 4,
    "MVLV_research_tsf_4_framework": 5,
}
for tid, new_cost in GEN_COST.items():
    m = re.search(r'(\t' + re.escape(tid) + r'\s*=\s*\{[^{]*?research_cost\s*=\s*)([\d.]+)', c)
    if m:
        old = m.group(2)
        c = c[:m.start(2)] + str(new_cost) + c[m.end(2):]
        cost_updates += 1
        print(f"  cost {tid}: {old} -> {new_cost}")

print(f"  start_year 更新: {updates} 件")
print(f"  research_cost 更新: {cost_updates} 件")

with open(TECH, "w", encoding="utf-8") as f:
    f.write(c)
print(f"  -- saved: {os.path.basename(TECH)}")

# === 2. chassis 装備の year 更新 ===
print("\n=== 2. chassis 装備 year 更新 ===")
for path in CHASSIS_FILES:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        cc = f.read()

    def repl_y(mm):
        old_year = int(mm.group(1))
        new_year = map_year(old_year)
        if new_year == old_year:
            return mm.group(0)
        return f"year = {new_year}"

    new_cc, n = re.subn(r'\byear\s*=\s*(\d{4})\b', repl_y, cc)
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_cc)
    print(f"  {os.path.basename(path)}: {n} chassis 更新")

# === 3. ブレース整合性 ===
print("\n=== 3. ブレース整合性 ===")
for p in [TECH] + CHASSIS_FILES:
    cc = open(p, encoding="utf-8", errors="replace").read()
    o, x = cc.count("{"), cc.count("}")
    print(f"  {os.path.basename(p):45s} {o}/{x} diff={o-x}")
