# -*- coding: utf-8 -*-
"""
framework/T00 テックの enable_equipments から国別 variant を除去
（国別 hidden tech 方式に移行するため、全国共通 enable を撤回）
"""
import re
import os

MOD = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod"
TECH = os.path.join(MOD, "common", "technologies", "MVLV_NSB_TSF.txt")

VARIANTS = [
    "USA_TSF_F_5", "USA_TSF_F_22", "JAP_TSF_77shiki", "JAP_TSF_shiranui",
    "JAP_TSF_takemikazuchi", "RUS_TSF_MiG_21", "RUS_TSF_Su_37", "CHI_TSF_J_10",
]

with open(TECH, "r", encoding="utf-8", errors="replace") as f:
    c = f.read()

removed = 0
for v in VARIANTS:
    # enable_equipments 内の "\t\t\t<variant>\n" 行を削除
    pat = re.compile(r'\n[\t ]*' + re.escape(v) + r'[\t ]*(?=\n)')
    c, n = pat.subn("", c)
    if n:
        removed += n
        print(f"  - {v}: {n}箇所除去")

with open(TECH, "w", encoding="utf-8") as f:
    f.write(c)

print(f"\n合計除去: {removed}")
o, x = c.count("{"), c.count("}")
print(f"ブレース: {o}/{x} diff={o-x}")
# variant が残っていないか確認
for v in VARIANTS:
    if v in c:
        print(f"  ! まだ残存: {v} ({c.count(v)}回)")
