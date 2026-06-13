# -*- coding: utf-8 -*-
"""
特務戦術機 / 支援戦術機 chassis を全 framework tech で並列解放
+ T00 系を特務 chassis にリファクタ
+ 旧 jeg_equipment_T00 系を削除

変更内容:
1. 11 個の framework tech: enable_equipments に support / specialForces chassis 追加
2. T00 系 5 テック: enable_equipments を jeg_equipment_T00X -> MVLV_TSF_specialForces_chassis_X に変更
3. MVLV_UNI_tsf.txt から jeg_equipment_T00 系 5 装備定義を削除
"""
import re
import os

MOD = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod"
TECH = os.path.join(MOD, "common", "technologies", "MVLV_NSB_TSF.txt")
JEG = os.path.join(MOD, "common", "units", "equipment", "MVLV_UNI_tsf.txt")

# framework tech -> 元の chassis suffix
FRAMEWORK_MAP = {
    "MVLV_research_basic_tsf_framework":    "_0",
    "MVLV_research_tsf_1_light_framework":  "_1_light",
    "MVLV_research_tsf_1_light_mod_framework": "_1_light_mod",
    "MVLV_research_tsf_1_heavy_framework":  "_1_heavy",
    "MVLV_research_tsf_2_light_framework":  "_2_light",
    "MVLV_research_tsf_2_heavy_framework":  "_2_heavy",
    "MVLV_research_tsf_2_maneuver_framework":"_2_maneuver",
    "MVLV_research_tsf_3_light_framework":  "_3_light",
    "MVLV_research_tsf_3_heavy_framework":  "_3_heavy",
    "MVLV_research_tsf_3_maneuver_framework":"_3_maneuver",
    "MVLV_research_tsf_4_framework":        "_4",
}

# T00 系 -> 対応する specialForces chassis
T00_MAP = {
    "MVLV_research_T00":  "MVLV_TSF_specialForces_chassis_2_maneuver",  # 武御雷 canon
    "MVLV_research_T00R": "MVLV_TSF_specialForces_chassis_3_maneuver",  # 改良型
    "MVLV_research_T00F": "MVLV_TSF_specialForces_chassis_3_light",     # 国連型 軽量
    "MVLV_research_T00A": "MVLV_TSF_specialForces_chassis_3_heavy",     # 重装
    "MVLV_research_T00C": "MVLV_TSF_specialForces_chassis_4",           # gen 4
}


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


def find_tech_block(content, tech_id):
    """tech_id = { ... } のブロックを (start, end_inclusive) で返す"""
    m = re.search(r'(\t)' + re.escape(tech_id) + r'\s*=\s*\{', content)
    if not m:
        return None
    brace_open = m.end() - 1
    brace_close = find_block_end(content, brace_open)
    return (m.start(), brace_close)


def modify_enable_equipments(content, tech_id, add_lines=None, replace_lines=None):
    """
    対象 tech の enable_equipments ブロックを書き換える
    - add_lines: 末尾に追加
    - replace_lines: ブロック全体を置き換え
    """
    blk = find_tech_block(content, tech_id)
    if not blk:
        print(f"  ! tech 見つからず: {tech_id}")
        return content
    bstart, bend = blk

    # ブロック内の enable_equipments を探す
    body = content[bstart:bend+1]
    em = re.search(r'(enable_equipments\s*=\s*\{)([^{}]*)(\})', body)
    if not em:
        print(f"  ! enable_equipments なし: {tech_id}")
        return content
    inner = em.group(2)

    if replace_lines is not None:
        new_inner = "\n\t\t\t" + "\n\t\t\t".join(replace_lines) + "\n\t\t"
    else:
        new_inner = inner.rstrip() + "\n\t\t\t" + "\n\t\t\t".join(add_lines) + "\n\t\t"

    new_em = em.group(1) + new_inner + em.group(3)
    new_body = body[:em.start()] + new_em + body[em.end():]
    return content[:bstart] + new_body + content[bend+1:]


# === メイン処理 ===
print("=== 1. テックファイル修正 ===")
with open(TECH, "r", encoding="utf-8", errors="replace") as f:
    content = f.read()

# 1-A. framework tech: support + specialForces chassis を並列追加
for tech_id, suffix in FRAMEWORK_MAP.items():
    support_chassis = f"MVLV_TSF_support_chassis{suffix}"
    sf_chassis = f"MVLV_TSF_specialForces_chassis{suffix}"
    content = modify_enable_equipments(
        content, tech_id,
        add_lines=[support_chassis, sf_chassis]
    )
    print(f"  + {tech_id}: +{support_chassis} +{sf_chassis}")

# 1-B. T00 系: 特務 chassis に置き換え
for tech_id, sf_chassis in T00_MAP.items():
    content = modify_enable_equipments(
        content, tech_id,
        replace_lines=[sf_chassis]
    )
    print(f"  ~ {tech_id}: enable_equipments = {{ {sf_chassis} }}")

# basic_tsf_framework は コメントアウト中の chassis_0 も復活させる
content = content.replace("#MVLV_TSF_chassis_0", "MVLV_TSF_chassis_0")
print("  ~ basic_tsf_framework: #MVLV_TSF_chassis_0 をアンコメント")

with open(TECH, "w", encoding="utf-8") as f:
    f.write(content)
print("  -- saved: MVLV_NSB_TSF.txt")

# === 2. 旧 jeg_equipment_T00 系を MVLV_UNI_tsf.txt から削除 ===
print("\n=== 2. 旧 jeg_equipment_T00 系装備を削除 ===")
with open(JEG, "r", encoding="utf-8", errors="replace") as f:
    jeg_content = f.read()

OLD_EQUIPS = [
    "jeg_equipment_T00",
    "jeg_equipment_T00R",
    "jeg_equipment_T00F",
    "jeg_equipment_T00A",
    "jeg_equipment_T00C",
]

removed_count = 0
for eq in OLD_EQUIPS:
    # eq = { ... } ブロックを探して削除
    m = re.search(r'(\t)' + re.escape(eq) + r'\s*=\s*\{', jeg_content)
    if not m:
        print(f"  ! 既に存在せず: {eq}")
        continue
    bstart = m.start()
    bend = find_block_end(jeg_content, m.end() - 1)
    # 前の空白行も含めて削除
    while bstart > 0 and jeg_content[bstart - 1] in " \t":
        bstart -= 1
    if bstart > 0 and jeg_content[bstart - 1] == "\n":
        bstart -= 1
    jeg_content = jeg_content[:bstart] + jeg_content[bend + 1:]
    removed_count += 1
    print(f"  - {eq} 削除")

with open(JEG, "w", encoding="utf-8") as f:
    f.write(jeg_content)
print(f"  -- saved: MVLV_UNI_tsf.txt ({removed_count} 装備削除)")

# === 3. ブレース整合性チェック ===
print("\n=== 3. ブレース整合性 ===")
for path in [TECH, JEG]:
    c = open(path, encoding="utf-8", errors="replace").read()
    o, x = c.count("{"), c.count("}")
    print(f"  {os.path.basename(path)}: {o}/{x} diff={o-x}")
