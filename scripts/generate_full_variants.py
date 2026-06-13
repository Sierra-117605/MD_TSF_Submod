# -*- coding: utf-8 -*-
"""
全面 variant 実装（58機種、国別厳密分離）
- 新規27機種を zz_country_variants.txt に追加 + loc
- hidden tech を全10国で再生成（既存+新規 variant を国別 enable）
- 配布 on_actions を全10国で再生成
"""
import re
import os

MOD = r"C:\Users\tkmuh\OneDrイ\ドキュメント".replace("ドキュメント","")  # placeholder guard
MOD = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod"
ZZ = os.path.join(MOD, "common", "units", "equipment", "MVLV_TSF_zz_country_variants.txt")
UNLOCK = os.path.join(MOD, "common", "technologies", "MVLV_tsf_variant_unlock.txt")
ASSIGN = os.path.join(MOD, "common", "on_actions", "MVLV_tsf_variant_assign.txt")
LOC = os.path.join(MOD, "localisation", "japanese", "MVLV_tsf_full_variants_l_japanese.yml")

# 新規追加 variant: (tag, id, abbr, jp_name, parent, vl, year, priority, archetype_kind)
# archetype_kind: "n"=MVLV_TSF_chassis, "sf"=MVLV_TSF_specialForces_chassis
NEW = [
    ("USA","USA_TSF_F_5G","F-5G","F-5G タイガーシャーク","MVLV_TSF_chassis_1_light_mod",1,1995,62,"n"),
    ("USA","USA_TSF_F_14","F-14","F-14 トムキャット","MVLV_TSF_chassis_2_maneuver",5,2005,73,"n"),
    ("USA","USA_TSF_F_16","F-16","F-16 ファイティングファルコン","MVLV_TSF_chassis_2_light",3,2005,71,"n"),
    ("USA","USA_TSF_F_15E","F-15E","F-15E ストライクイーグル","MVLV_TSF_chassis_2_heavy",4,2010,76,"n"),
    ("USA","USA_TSF_F_18EF","F-18EF","F/A-18E スーパーホーネット","MVLV_TSF_chassis_2_maneuver",5,2010,76,"n"),
    ("USA","USA_TSF_F_15SE","F-15SE","F-15SE サイレントイーグル","MVLV_TSF_chassis_3_heavy",7,2015,86,"n"),
    ("USA","USA_TSF_YF_23","YF-23","YF-23 ブラックウィドウ II","MVLV_TSF_chassis_3_maneuver",8,2015,89,"n"),
    ("JAP","JAP_TSF_zuikaku","Type-82","82式 瑞鶴","MVLV_TSF_chassis_2_light",3,2005,71,"n"),
    ("JAP","JAP_TSF_kagerou","F-15J","89式 陽炎","MVLV_TSF_chassis_2_heavy",4,2005,73,"n"),
    ("JAP","JAP_TSF_shiranui_1c","Type-94-1-C","不知火・壱型丙","MVLV_TSF_chassis_3_heavy",7,2015,86,"n"),
    ("JAP","JAP_TSF_shiranui_2","Type-942","不知火・弐型","MVLV_TSF_chassis_3_maneuver",8,2018,89,"n"),
    ("JAP","JAP_TSF_takemikazuchi_r","Type-00r","武御雷・紅","MVLV_TSF_specialForces_chassis_3_maneuver",8,2015,90,"sf"),
    ("JAP","JAP_TSF_type04","Type-04","04式戦術歩行戦闘機","MVLV_TSF_chassis_4",15,2035,93,"n"),
    ("JAP","JAP_TSF_type10","Type-10","10式戦術歩行戦闘機","MVLV_TSF_chassis_4",15,2035,94,"n"),
    ("RUS","RUS_TSF_Su_11","Su-11","Su-11","MVLV_TSF_chassis_1_light",1,1995,60,"n"),
    ("RUS","RUS_TSF_MiG_23","MiG-23","MiG-23 フロッガー","MVLV_TSF_chassis_2_light",3,2005,71,"n"),
    ("RUS","RUS_TSF_MiG_25","MiG-25","MiG-25 フォックスバット","MVLV_TSF_chassis_2_heavy",4,2005,73,"n"),
    ("RUS","RUS_TSF_MiG_27","MiG-27","MiG-27","MVLV_TSF_chassis_2_light",3,2005,71,"n"),
    ("RUS","RUS_TSF_MiG_31","MiG-31","MiG-31 フォックスハウンド","MVLV_TSF_chassis_2_heavy",4,2010,76,"n"),
    ("RUS","RUS_TSF_MiG_35","MiG-35","MiG-35","MVLV_TSF_chassis_2_maneuver",5,2010,77,"n"),
    ("CHI","CHI_TSF_J_10X","J-10X","J-10X","MVLV_TSF_chassis_3_light",6,2015,85,"n"),
    ("GER","GER_TSF_Me101P","Me-101P","Me-101P","MVLV_TSF_chassis_2_heavy",4,2005,73,"n"),
    ("FRA","FRA_TSF_M2000K","M2000K","ミラージュ2000改","MVLV_TSF_chassis_2_maneuver",5,2010,77,"n"),
    ("ITA","ITA_TSF_EF2000","EF-2000","EF-2000 タイフーン","MVLV_TSF_chassis_3_heavy",7,2015,86,"n"),
    ("ISR","ISR_TSF_kfir","Kfir","クフィル","MVLV_TSF_chassis_1_light",1,1995,60,"n"),
    ("ISR","ISR_TSF_lavi","Lavi","ラビ","MVLV_TSF_chassis_2_light",3,2005,71,"n"),
]

ARCH = {"n": "MVLV_TSF_chassis", "sf": "MVLV_TSF_specialForces_chassis"}

# 全 variant の国別マッピング（hidden tech 用）= 既存 + 新規
COUNTRY_ALL = {
    "USA": ["USA_TSF_F_5","USA_TSF_F_22","USA_TSF_F_15","USA_TSF_F_18","USA_TSF_F_35",
            "USA_TSF_F_5G","USA_TSF_F_14","USA_TSF_F_16","USA_TSF_F_15E","USA_TSF_F_18EF","USA_TSF_F_15SE","USA_TSF_YF_23"],
    "JAP": ["JAP_TSF_77shiki","JAP_TSF_shiranui","JAP_TSF_takemikazuchi","JAP_TSF_fubuki",
            "JAP_TSF_zuikaku","JAP_TSF_kagerou","JAP_TSF_shiranui_1c","JAP_TSF_shiranui_2","JAP_TSF_takemikazuchi_r","JAP_TSF_type04","JAP_TSF_type10"],
    "RUS": ["RUS_TSF_MiG_21","RUS_TSF_Su_37","RUS_TSF_MiG_29","RUS_TSF_Su_27","RUS_TSF_Su_47","RUS_TSF_Su_57",
            "RUS_TSF_Su_11","RUS_TSF_MiG_23","RUS_TSF_MiG_25","RUS_TSF_MiG_27","RUS_TSF_MiG_31","RUS_TSF_MiG_35"],
    "CHI": ["CHI_TSF_J_10","CHI_TSF_J_8","CHI_TSF_J_11","CHI_TSF_J_20","CHI_TSF_J_10X"],
    "GER": ["GER_TSF_EF2000","GER_TSF_Me101P"],
    "FRA": ["FRA_TSF_Mirage","FRA_TSF_Rafale","FRA_TSF_M2000K"],
    "ENG": ["ENG_TSF_EF2000","ENG_TSF_Tempest"],
    "ITA": ["ITA_TSF_EF2000"],
    "SWE": ["SWE_TSF_JA37","SWE_TSF_JAS39"],
    "ISR": ["ISR_TSF_kfir","ISR_TSF_lavi"],
}

# === 1. 新規 variant を zz に追加 ===
with open(ZZ, "r", encoding="utf-8", errors="replace") as f:
    zz = f.read()

existing_ids = set(re.findall(r'((?:USA|JAP|RUS|CHI|GER|FRA|ENG|SWE|ITA|ISR)_TSF_\w+?)\s*=\s*\{', zz))

blocks = ["\n\t# === 全面追加 variant（派生含む・国別厳密）===\n"]
added = 0
for tag, vid, abbr, jp, parent, vl, year, pri, kind in NEW:
    if vid in existing_ids:
        continue
    blocks.append(
        f'\t{vid} = {{\n'
        f'\t\tabbreviation = "{abbr}"\n'
        f'\t\tderived_variant_name = {vid}_name\n'
        f'\t\tvisual_level = {vl}\n'
        f'\t\tyear = {year}\n'
        f'\t\tarchetype = {ARCH[kind]}\n'
        f'\t\tparent = {parent}\n'
        f'\t\tpriority = {pri}\n'
        f'\t}}\n\n'
    )
    added += 1
idx = zz.rstrip().rfind("}")
zz = zz[:idx] + "".join(blocks) + zz[idx:]
with open(ZZ, "w", encoding="utf-8") as f:
    f.write(zz)
print(f"zz に新規 variant 追加: {added}")

# === 2. loc 生成（新規分）===
loc = ["﻿l_japanese:\n", " # === 全面追加 variant 名 ===\n"]
for tag, vid, abbr, jp, parent, vl, year, pri, kind in NEW:
    loc.append(f' {vid}_name: "{jp}"\n')
with open(LOC, "w", encoding="utf-8") as f:
    f.writelines(loc)
print(f"loc 生成: {len(NEW)}")

# === 3. hidden tech 全10国再生成 ===
tech = ["# ============================================================\n",
        "# 国別 variant 有効化用の隠しテック（全10国・全variant）\n",
        "# folder無=ツリー非表示 / allow=no=研究不可 / on_actionsで配布\n",
        "# ============================================================\n",
        "technologies = {\n\n"]
for tag, vids in COUNTRY_ALL.items():
    tech.append(f"\ttsf_variant_{tag.lower()} = {{\n")
    tech.append("\t\tenable_equipments = {\n")
    for v in vids:
        tech.append(f"\t\t\t{v}\n")
    tech.append("\t\t}\n")
    tech.append("\t\tstart_year = 1936\n")
    tech.append("\t\tallow = { always = no }\n")
    tech.append("\t\tshow_effect_as_desc = no\n")
    tech.append("\t\tcategories = { MVLV_tsf_tech }\n")
    tech.append("\t}\n\n")
tech.append("}\n")
with open(UNLOCK, "w", encoding="utf-8") as f:
    f.writelines(tech)
print(f"hidden tech 再生成: {len(COUNTRY_ALL)} 国")

# === 4. 配布 on_actions 全10国再生成 ===
act = ["# ============================================================\n",
       "# 国別 variant 隠しテックを各国へ配布（全10国）\n",
       "# on_startup=新規 / on_weekly=既存セーブ冪等\n",
       "# ============================================================\n",
       "on_actions = {\n\n",
       "\ton_startup = {\n\t\teffect = {\n"]
for tag in COUNTRY_ALL:
    act.append(f"\t\t\t{tag} = {{ set_technology = {{ tsf_variant_{tag.lower()} = 1 }} }}\n")
act.append("\t\t}\n\t}\n\n")
act.append("\ton_weekly = {\n\t\teffect = {\n")
for tag in COUNTRY_ALL:
    t = tag.lower()
    act.append(f"\t\t\t{tag} = {{ if = {{ limit = {{ NOT = {{ has_tech = tsf_variant_{t} }} }} set_technology = {{ tsf_variant_{t} = 1 }} }} }}\n")
act.append("\t\t}\n\t}\n\n}\n")
with open(ASSIGN, "w", encoding="utf-8") as f:
    f.writelines(act)
print(f"配布 on_actions 再生成: {len(COUNTRY_ALL)} 国")

# === ブレース検証 ===
print("\n=== ブレース ===")
for p in [ZZ, UNLOCK, ASSIGN]:
    c = open(p, encoding="utf-8", errors="replace").read()
    o, x = c.count("{"), c.count("}")
    print(f"  {os.path.basename(p):40s} {o}/{x} diff={o-x}")
