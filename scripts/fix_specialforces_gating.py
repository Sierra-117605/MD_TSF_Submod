# -*- coding: utf-8 -*-
# 特務機(武御雷/瑞鶴)を専用研究(T00系/T82)で解放するよう修正
import re
MOD = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod"
NSB = MOD + r"\common\technologies\MVLV_NSB_TSF.txt"
VU  = MOD + r"\common\technologies\MVLV_tsf_variant_unlock.txt"
ON  = MOD + r"\common\on_actions\MVLV_tsf_variant_assign.txt"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="").write(s)
def rep(s, old, new, tag):
    assert old in s, "NOT FOUND: " + tag
    return s.replace(old, new, 1)
def chk(s, tag): assert s.count("{") == s.count("}"), tag + " brace mismatch"

# ===== 1) NSB: T00系に前提(通常フレームワーク)付与 + T82新設 =====
s = rd(NSB)
deps = {"MVLV_research_T00": "tsf_2_maneuver", "MVLV_research_T00R": "tsf_3_maneuver",
        "MVLV_research_T00A": "tsf_3_heavy", "MVLV_research_T00F": "tsf_3_light",
        "MVLV_research_T00C": "tsf_4"}
for t, fw in deps.items():
    s = re.sub(r'(\n\t' + t + r' = \{\n)',
               r'\1\t\tdependencies = { MVLV_research_' + fw + '_framework = 1 }\n', s, count=1)
t82 = ("\tMVLV_research_T82 = {\n"
       "\t\tenable_equipments = {\n\t\t\tMVLV_TSF_specialForces_chassis_1_heavy\n\t\t}\n"
       "\t\tresearch_cost = 2\n\t\tstart_year = 1995\n"
       "\t\tdependencies = { MVLV_research_tsf_1_heavy_framework = 1 }\n"
       "\t\tfolder = {\n\t\t\tname = MVLV_tsf_folder\n\t\t\tposition = { x = 6 y = 7 }\n\t\t}\n"
       "\t\tcategories = { MVLV_tsf_tech }\n\t\tshow_effect_as_desc = no\n"
       "\t\tai_will_do = {\n\t\t\tfactor = 1\n\t\t\tmodifier = { date > 1994.1.1 factor = 60 }\n\t\t}\n\t}\n")
s = rep(s, "\tMVLV_research_T00 = {", t82 + "\tMVLV_research_T00 = {", "NSB T00 anchor")
chk(s, "NSB"); wr(NSB, s)

# ===== 2) variant_unlock: 瑞鶴をjap_1hから分離 + 専用テック =====
s = rd(VU)
s = rep(s, "enable_equipments = { JAP_TSF_77shiki JAP_TSF_zuikaku_c JAP_TSF_zuikaku_a JAP_TSF_zuikaku_f JAP_TSF_zuikaku_r }",
        "enable_equipments = { JAP_TSF_77shiki }", "VU jap_1h")
ztech = ("\ttsf_variant_jap_zuikaku = {\n"
         "\t\tenable_equipments = { JAP_TSF_zuikaku_c JAP_TSF_zuikaku_a JAP_TSF_zuikaku_f JAP_TSF_zuikaku_r }\n"
         "\t\tstart_year = 1936\n\t\tallow = { always = no }\n\t\tshow_effect_as_desc = no\n"
         "\t\tcategories = { MVLV_tsf_tech }\n\t}\n\n")
s = rep(s, "\ttsf_variant_jap_2h = {", ztech + "\ttsf_variant_jap_2h = {", "VU jap_2h anchor")
chk(s, "VU"); wr(VU, s)

# ===== 3) on_actions: 武御雷をT00/T00Rへ、瑞鶴をT82へ =====
s = rd(ON)
s = rep(s, "has_tech = MVLV_research_tsf_2_maneuver_framework any_owned_state = { is_core_of = JAP } NOT = { has_tech = tsf_variant_jap_2m }",
        "has_tech = MVLV_research_T00 any_owned_state = { is_core_of = JAP } NOT = { has_tech = tsf_variant_jap_2m }", "2m mon")
s = rep(s, "has_tech = MVLV_research_tsf_2_maneuver_framework NOT = { has_tech = tsf_variant_jap_2m }",
        "has_tech = MVLV_research_T00 NOT = { has_tech = tsf_variant_jap_2m }", "2m day")
s = rep(s, "has_tech = MVLV_research_tsf_3_maneuver_framework any_owned_state = { is_core_of = JAP } NOT = { has_tech = tsf_variant_jap_3m }",
        "has_tech = MVLV_research_T00R any_owned_state = { is_core_of = JAP } NOT = { has_tech = tsf_variant_jap_3m }", "3m mon")
s = rep(s, "has_tech = MVLV_research_tsf_3_maneuver_framework NOT = { has_tech = tsf_variant_jap_3m }",
        "has_tech = MVLV_research_T00R NOT = { has_tech = tsf_variant_jap_3m }", "3m day")
mon1h = "every_country = { if = { limit = { has_tech = MVLV_research_tsf_1_heavy_framework any_owned_state = { is_core_of = JAP } NOT = { has_tech = tsf_variant_jap_1h } } set_technology = { tsf_variant_jap_1h = 1 } } }"
monzk = "every_country = { if = { limit = { has_tech = MVLV_research_T82 any_owned_state = { is_core_of = JAP } NOT = { has_tech = tsf_variant_jap_zuikaku } } set_technology = { tsf_variant_jap_zuikaku = 1 } } }"
s = rep(s, mon1h, mon1h + "\n\t\t\t" + monzk, "zuikaku mon")
day1h = "JAP = { if = { limit = { has_tech = MVLV_research_tsf_1_heavy_framework NOT = { has_tech = tsf_variant_jap_1h } } set_technology = { tsf_variant_jap_1h = 1 } } }"
dayzk = "JAP = { if = { limit = { has_tech = MVLV_research_T82 NOT = { has_tech = tsf_variant_jap_zuikaku } } set_technology = { tsf_variant_jap_zuikaku = 1 } } }"
s = rep(s, day1h, day1h + "\n\t\t\t" + dayzk, "zuikaku day")
chk(s, "ON"); wr(ON, s)
print("DONE: 特務機ゲーティング修正完了")
