# -*- coding: utf-8 -*-
"""
開発時期を MD 技術の10年刻み(1995/2005/2015/2025)に合わせて世代別に設定

世代 -> 年:
  Gen1 = 1995, Gen2 = 2005, Gen3 = 2015, Gen4 = 2025

対象:
  - framework tech (start_year)
  - chassis equipment 3系統 (year)
  - 国別 variant (year)
  - module tech (engine/OS/head/weapon... の _1/_2/_3/_4) (start_year)
"""
import re
import os

MOD = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod"
TECH = os.path.join(MOD, "common", "technologies", "MVLV_NSB_TSF.txt")
CHASSIS = [
    os.path.join(MOD, "common", "units", "equipment", "MVLV_TSF_chassis.txt"),
    os.path.join(MOD, "common", "units", "equipment", "MVLV_TSF_support_chassis.txt"),
    os.path.join(MOD, "common", "units", "equipment", "MVLV_TSF_specialForces_chassis.txt"),
]
VARIANTS = os.path.join(MOD, "common", "units", "equipment", "MVLV_TSF_zz_country_variants.txt")

GEN = {1: 1995, 2: 2005, 3: 2015, 4: 2035}

# 個別マッピング（tech_id -> 世代）
TECH_GEN = {
    "MVLV_research_debug_pack": 1,
    "MVLV_research_basic_tsf_framework": 1,
    "MVLV_research_tsf_1_light_framework": 1,
    "MVLV_research_tsf_1_light_mod_framework": 1,
    "MVLV_research_tsf_1_heavy_framework": 1,
    "MVLV_research_tsf_2_light_framework": 2,
    "MVLV_research_tsf_2_heavy_framework": 2,
    "MVLV_research_tsf_2_maneuver_framework": 2,
    "MVLV_research_tsf_3_light_framework": 3,
    "MVLV_research_tsf_3_heavy_framework": 3,
    "MVLV_research_tsf_3_maneuver_framework": 3,
    "MVLV_research_tsf_4_framework": 4,
    # 名前付き機体（Gen1相当）
    "MVLV_research_A6": 1, "MVLV_research_A10": 1, "MVLV_research_A10C": 1,
    "MVLV_research_A12": 1, "MVLV_research_F-4JK": 1,
    # 武御雷
    "MVLV_research_T00": 2, "MVLV_research_T00R": 3,
    "MVLV_research_T00F": 3, "MVLV_research_T00A": 3, "MVLV_research_T00C": 3,
}

# variant id -> 世代
VARIANT_GEN = {
    "USA_TSF_F_5": 1, "USA_TSF_F_22": 3,
    "JAP_TSF_77shiki": 1, "JAP_TSF_shiranui": 3, "JAP_TSF_takemikazuchi": 2,
    "RUS_TSF_MiG_21": 1, "RUS_TSF_Su_37": 2, "CHI_TSF_J_10": 2,
}


def gen_from_modtech(tid):
    """module tech 名から世代を推定（末尾の _N）"""
    m = re.search(r'_(\d)(?:_\w+)?$', tid)
    if m:
        n = int(m.group(1))
        if n in GEN:
            return n
    return None


def find_block_end(s, p):
    d = 1; i = p + 1
    while i < len(s) and d > 0:
        if s[i] == "{": d += 1
        elif s[i] == "}":
            d -= 1
            if d == 0: return i
        i += 1
    return -1


# === 1. テックファイル ===
with open(TECH, "r", encoding="utf-8", errors="replace") as f:
    c = f.read()

new_parts = []
last = 0
updated = 0
for m in re.finditer(r'^\t([A-Za-z][\w\-]+)\s*=\s*\{', c, re.M):
    tid = m.group(1)
    bend = find_block_end(c, m.end() - 1)
    new_parts.append(c[last:m.start()])
    block = c[m.start():bend + 1]

    gen = TECH_GEN.get(tid)
    if gen is None:
        gen = gen_from_modtech(tid)

    if gen and gen in GEN:
        yr = GEN[gen]
        nb, n = re.subn(r'(start_year\s*=\s*)\d+', rf'\g<1>{yr}', block)
        if n > 0:
            updated += 1
            block = nb
    new_parts.append(block)
    last = bend + 1
new_parts.append(c[last:])
c = "".join(new_parts)
with open(TECH, "w", encoding="utf-8") as f:
    f.write(c)
print(f"テック start_year 更新: {updated}")

# === 2. chassis equipment ===
for path in CHASSIS:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        cc = f.read()
    new_parts = []; last = 0; upd = 0
    for m in re.finditer(r'(\t)(MVLV_TSF_(?:support_|specialForces_)?chassis_\w+)\s*=\s*\{', cc):
        cid = m.group(2)
        bend = find_block_end(cc, m.end() - 1)
        new_parts.append(cc[last:m.start()])
        block = cc[m.start():bend + 1]
        # suffix から世代
        sm = re.match(r'MVLV_TSF_(?:support_|specialForces_)?chassis_(\d|\w+)', cid)
        suffix = cid.split("chassis_")[-1]
        if suffix.startswith("0") or suffix.startswith("1"): gen = 1
        elif suffix.startswith("2"): gen = 2
        elif suffix.startswith("3"): gen = 3
        elif suffix.startswith("4"): gen = 4
        else: gen = None
        if gen:
            nb, n = re.subn(r'\byear\s*=\s*\d{4}', f'year = {GEN[gen]}', block)
            if n > 0: upd += 1; block = nb
        new_parts.append(block)
        last = bend + 1
    new_parts.append(cc[last:])
    cc = "".join(new_parts)
    with open(path, "w", encoding="utf-8") as f:
        f.write(cc)
    print(f"{os.path.basename(path)}: {upd} chassis 更新")

# === 3. 国別 variant ===
with open(VARIANTS, "r", encoding="utf-8", errors="replace") as f:
    vc = f.read()
upd = 0
for vid, gen in VARIANT_GEN.items():
    m = re.search(r'(\t' + re.escape(vid) + r'\s*=\s*\{)([^{}]*?)(\n\t\})', vc)
    if not m: continue
    block = m.group(0)
    nb, n = re.subn(r'\byear\s*=\s*\d{4}', f'year = {GEN[gen]}', block)
    if n > 0:
        vc = vc[:m.start()] + nb + vc[m.end():]
        upd += 1
with open(VARIANTS, "w", encoding="utf-8") as f:
    f.write(vc)
print(f"国別 variant year 更新: {upd}")

# ブレース
for p in [TECH] + CHASSIS + [VARIANTS]:
    cc = open(p, encoding="utf-8", errors="replace").read()
    o, x = cc.count("{"), cc.count("}")
    print(f"  {os.path.basename(p):45s} {o}/{x}")
