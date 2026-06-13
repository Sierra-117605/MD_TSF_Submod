# -*- coding: utf-8 -*-
"""
MOD内テクスチャを活かして国別 variant を追加（18機種）
- variant 定義を zz_country_variants.txt に追記
- loc（機体名）を生成
- 見た目は parent chassis 相当の visual_level（汎用3Dモデル）
"""
import re
import os

MOD = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod"
VARIANTS = os.path.join(MOD, "common", "units", "equipment", "MVLV_TSF_zz_country_variants.txt")
LOC = os.path.join(MOD, "localisation", "japanese", "MVLV_tsf_more_variants_l_japanese.yml")

# (tag, id, abbr, jp_name, parent_chassis, visual_level, year, priority)
NEW = [
    ("USA", "USA_TSF_F_15", "F-15", "F-15 イーグル",        "MVLV_TSF_chassis_2_heavy",    4, 2005, 72),
    ("USA", "USA_TSF_F_18", "F-18", "F-18 ホーネット",      "MVLV_TSF_chassis_2_maneuver", 5, 2005, 74),
    ("USA", "USA_TSF_F_35", "F-35", "F-35 ライトニング II", "MVLV_TSF_chassis_3_light",    6, 2015, 88),
    ("RUS", "RUS_TSF_MiG_29", "MiG-29", "MiG-29 ファルクラム", "MVLV_TSF_chassis_2_light",  3, 2005, 72),
    ("RUS", "RUS_TSF_Su_27", "Su-27", "Su-27 フランカー",    "MVLV_TSF_chassis_2_heavy",    4, 2005, 74),
    ("RUS", "RUS_TSF_Su_47", "Su-47", "Su-47 ベールクト",    "MVLV_TSF_chassis_3_maneuver", 8, 2015, 88),
    ("RUS", "RUS_TSF_Su_57", "Su-57", "Su-57 フェロン",      "MVLV_TSF_chassis_4",         15, 2035, 95),
    ("CHI", "CHI_TSF_J_8",  "J-8",  "J-8",                  "MVLV_TSF_chassis_1_light",    1, 1995, 60),
    ("CHI", "CHI_TSF_J_11", "J-11", "J-11",                 "MVLV_TSF_chassis_2_heavy",    4, 2005, 74),
    ("CHI", "CHI_TSF_J_20", "J-20", "J-20",                 "MVLV_TSF_chassis_3_maneuver", 8, 2015, 88),
    ("JAP", "JAP_TSF_fubuki", "97式", "97式 吹雪",          "MVLV_TSF_chassis_2_maneuver", 5, 2005, 74),
    ("GER", "GER_TSF_EF2000", "EF-2000", "EF-2000 タイフーン", "MVLV_TSF_chassis_3_heavy",  7, 2015, 88),
    ("FRA", "FRA_TSF_Mirage", "M2000", "ミラージュ2000",    "MVLV_TSF_chassis_2_light",    3, 2005, 72),
    ("FRA", "FRA_TSF_Rafale", "Rafale", "ラファール",        "MVLV_TSF_chassis_3_maneuver", 8, 2015, 88),
    ("ENG", "ENG_TSF_EF2000", "EF-2000", "EF-2000 タイフーン", "MVLV_TSF_chassis_3_heavy",  7, 2015, 88),
    ("ENG", "ENG_TSF_Tempest", "Tempest", "テンペスト",      "MVLV_TSF_chassis_4",         15, 2035, 95),
    ("SWE", "SWE_TSF_JA37", "JA-37", "JA-37 ビゲン",         "MVLV_TSF_chassis_1_light",    1, 1995, 60),
    ("SWE", "SWE_TSF_JAS39", "JAS-39", "JAS-39 グリペン",    "MVLV_TSF_chassis_2_light",    3, 2005, 72),
]

# === variant 定義を生成して zz_country_variants.txt の equipments 末尾に追記 ===
with open(VARIANTS, "r", encoding="utf-8", errors="replace") as f:
    vc = f.read()

blocks = ["\n\t# === 追加 variant（MOD内テクスチャ活用・見た目は世代別汎用）===\n"]
for tag, vid, abbr, jp, parent, vl, year, pri in NEW:
    blocks.append(
        f'\t{vid} = {{\n'
        f'\t\tabbreviation = "{abbr}"\n'
        f'\t\tderived_variant_name = {vid}_name\n'
        f'\t\tvisual_level = {vl}\n'
        f'\t\tyear = {year}\n'
        f'\t\tarchetype = MVLV_TSF_chassis\n'
        f'\t\tparent = {parent}\n'
        f'\t\tpriority = {pri}\n'
        f'\t}}\n\n'
    )
add_text = "".join(blocks)

# 最後の } （equipments 閉じ）の前に挿入
idx = vc.rstrip().rfind("}")
vc = vc[:idx] + add_text + vc[idx:]
with open(VARIANTS, "w", encoding="utf-8") as f:
    f.write(vc)
print(f"variant 追加: {len(NEW)}")

# === loc 生成 ===
loc_lines = ["﻿l_japanese:\n", " # === 追加国別 variant 名 ===\n"]
for tag, vid, abbr, jp, parent, vl, year, pri in NEW:
    loc_lines.append(f' {vid}_name: "{jp}"\n')
with open(LOC, "w", encoding="utf-8") as f:
    f.writelines(loc_lines)
print(f"loc 生成: {len(NEW)} -> {os.path.basename(LOC)}")

o, x = vc.count("{"), vc.count("}")
print(f"ブレース: {o}/{x} diff={o-x}")
