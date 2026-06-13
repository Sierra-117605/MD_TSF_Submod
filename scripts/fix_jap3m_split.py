# -*- coding: utf-8 -*-
# jap_3m に不知火弐型(通常)と武御雷G3(特務)が混在 → 分離
# 不知火弐型=jap_3m(通常3高機動フレームワーク)、武御雷G3=新tmkz3(T00R)
import re
MOD = r"C:\Users\tkmuh\OneドキュメンOneDrive"
MOD = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod"
VU  = MOD + r"\common\technologies\MVLV_tsf_variant_unlock.txt"
ON  = MOD + r"\common\on_actions\MVLV_tsf_variant_assign.txt"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="").write(s)
def rep(s, old, new, tag):
    assert old in s, "NOT FOUND: " + tag
    return s.replace(old, new, 1)
def chk(s, tag): assert s.count("{") == s.count("}"), tag

# 1) variant_unlock: jap_3m から武御雷を除去 → shiranui_2 のみ。武御雷は新tmkz3へ
s = rd(VU)
old_enable = ("\t\t\tJAP_TSF_shiranui_2\n\t\t\tJAP_TSF_takemikazuchi_r\n"
              "\t\t\tJAP_TSF_takemikazuchi_c\n\t\t\tJAP_TSF_takemikazuchi_a\n\t\t\tJAP_TSF_takemikazuchi_f")
s = rep(s, old_enable, "\t\t\tJAP_TSF_shiranui_2", "VU jap_3m enable")
tmkz = ("\ttsf_variant_jap_tmkz3 = {\n"
        "\t\tenable_equipments = {\n"
        "\t\t\tJAP_TSF_takemikazuchi_r\n\t\t\tJAP_TSF_takemikazuchi_c\n"
        "\t\t\tJAP_TSF_takemikazuchi_a\n\t\t\tJAP_TSF_takemikazuchi_f\n\t\t}\n"
        "\t\tstart_year = 1936\n\t\tallow = { always = no }\n\t\tshow_effect_as_desc = no\n"
        "\t\tcategories = { MVLV_tsf_tech }\n\t}\n\n")
s = rep(s, "\ttsf_variant_jap_4 = {", tmkz + "\ttsf_variant_jap_4 = {", "VU jap_4 anchor")
chk(s, "VU brace"); wr(VU, s)

# 2) on_actions: jap_3m を通常3高機動フレームワークへ戻す + 武御雷tmkz3をT00Rで配布
s = rd(ON)
# monthly jap_3m revert
m3 = "every_country = { if = { limit = { has_tech = MVLV_research_T00R any_owned_state = { is_core_of = JAP } NOT = { has_tech = tsf_variant_jap_3m } } set_technology = { tsf_variant_jap_3m = 1 } } }"
m3n = "every_country = { if = { limit = { has_tech = MVLV_research_tsf_3_maneuver_framework any_owned_state = { is_core_of = JAP } NOT = { has_tech = tsf_variant_jap_3m } } set_technology = { tsf_variant_jap_3m = 1 } } }"
m3t = "every_country = { if = { limit = { has_tech = MVLV_research_T00R any_owned_state = { is_core_of = JAP } NOT = { has_tech = tsf_variant_jap_tmkz3 } } set_technology = { tsf_variant_jap_tmkz3 = 1 } } }"
s = rep(s, m3, m3n + "\n\t\t\t" + m3t, "ON jap_3m monthly")
# daily jap_3m revert
d3 = "JAP = { if = { limit = { has_tech = MVLV_research_T00R NOT = { has_tech = tsf_variant_jap_3m } } set_technology = { tsf_variant_jap_3m = 1 } } }"
d3n = "JAP = { if = { limit = { has_tech = MVLV_research_tsf_3_maneuver_framework NOT = { has_tech = tsf_variant_jap_3m } } set_technology = { tsf_variant_jap_3m = 1 } } }"
d3t = "JAP = { if = { limit = { has_tech = MVLV_research_T00R NOT = { has_tech = tsf_variant_jap_tmkz3 } } set_technology = { tsf_variant_jap_tmkz3 = 1 } } }"
s = rep(s, d3, d3n + "\n\t\t\t" + d3t, "ON jap_3m daily")
chk(s, "ON brace"); wr(ON, s)
print("DONE jap_3m split")
