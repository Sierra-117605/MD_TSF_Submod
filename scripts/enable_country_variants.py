# -*- coding: utf-8 -*-
"""
国別 variant を対応する framework テックの enable_equipments に追加
これで variant が生産可能になり、priority(60-90 > 無印5) で AI が優先選択する
"""
import re
import os

MOD = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod"
TECH = os.path.join(MOD, "common", "technologies", "MVLV_NSB_TSF.txt")

# variant -> 有効化するテック（世代・archetypeに対応）
VARIANT_TECH = {
    "USA_TSF_F_5":          "MVLV_research_tsf_1_light_framework",
    "RUS_TSF_MiG_21":       "MVLV_research_tsf_1_light_framework",
    "JAP_TSF_77shiki":      "MVLV_research_tsf_1_heavy_framework",
    "CHI_TSF_J_10":         "MVLV_research_tsf_2_light_framework",
    "RUS_TSF_Su_37":        "MVLV_research_tsf_2_maneuver_framework",
    "USA_TSF_F_22":         "MVLV_research_tsf_3_maneuver_framework",
    "JAP_TSF_shiranui":     "MVLV_research_tsf_3_heavy_framework",
    "JAP_TSF_takemikazuchi": "MVLV_research_T00",  # specialForces 系
}

# tech -> [variant,...] に反転
TECH_VARIANTS = {}
for v, t in VARIANT_TECH.items():
    TECH_VARIANTS.setdefault(t, []).append(v)


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


with open(TECH, "r", encoding="utf-8", errors="replace") as f:
    content = f.read()

added = 0
for tech_id, variants in TECH_VARIANTS.items():
    # tech ブロックを探す
    m = re.search(r'(\t)' + re.escape(tech_id) + r'\s*=\s*\{', content)
    if not m:
        print(f"  ! tech 見つからず: {tech_id}")
        continue
    bstart = m.end() - 1
    bend = find_block_end(content, bstart)
    body = content[bstart:bend + 1]

    # enable_equipments ブロックを探す
    em = re.search(r'(enable_equipments\s*=\s*\{)([^{}]*)(\})', body)
    if not em:
        print(f"  ! enable_equipments なし: {tech_id}")
        continue

    inner = em.group(2)
    # 既に追加済みの variant を除外
    to_add = [v for v in variants if v not in inner]
    if not to_add:
        print(f"  - {tech_id}: 既に追加済み")
        continue

    new_inner = inner.rstrip() + "\n" + "".join(f"\t\t\t{v}\n" for v in to_add) + "\t\t"
    new_em = em.group(1) + new_inner + em.group(3)
    new_body = body[:em.start()] + new_em + body[em.end():]
    content = content[:bstart] + new_body + content[bend + 1:]
    added += len(to_add)
    print(f"  + {tech_id}: {', '.join(to_add)}")

with open(TECH, "w", encoding="utf-8") as f:
    f.write(content)

print(f"\n合計 {added} variant を有効化")
o, x = content.count("{"), content.count("}")
print(f"ブレース: {o}/{x} diff={o-x}")
