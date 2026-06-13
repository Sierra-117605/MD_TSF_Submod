# -*- coding: utf-8 -*-
"""
support chassis を regular chassis から差別化

役割設計:
  Regular (通常戦術機):    バランス型、地上戦主力
  Support (支援戦術機):    対空特化、火力支援、装甲援護
  SpecialForces (特務):    精鋭、全方位高性能（既に 1.5x で差別化済み）

Support chassis に適用する変換:
  soft_attack    : x 0.7  (地上対人攻撃低め)
  hard_attack    : x 0.7  (対装甲低め)
  air_attack     : x 1.5  (対空特化)
  defense        : x 1.2  (耐久型)
  breakthrough   : x 0.6  (突破役ではない)
  ap_attack      : x 0.7
  armor_value    : x 1.1  (やや装甲厚)
  hardness       : 維持
  reliability    : x 1.1  (整備性能)
  maximum_speed  : x 1.0  (維持)
"""
import re
import os

MOD = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod"
SUPPORT = os.path.join(MOD, "common", "units", "equipment", "MVLV_TSF_support_chassis.txt")

MULTIPLIERS = {
    "soft_attack":    0.7,
    "hard_attack":    0.7,
    "air_attack":     1.5,
    "defense":        1.2,
    "breakthrough":   0.6,
    "ap_attack":      0.7,
    "armor_value":    1.1,
    "reliability":    1.1,
}


def round_smart(v):
    """整数なら整数、それ以外は小数点1桁"""
    rounded = round(v, 1)
    if rounded == int(rounded):
        return str(int(rounded))
    return str(rounded)


with open(SUPPORT, "r", encoding="utf-8", errors="replace") as f:
    c = f.read()

# 各 chassis ブロックを処理
new_chunks = []
last = 0
total_changes = 0
for m in re.finditer(r'(\t)(MVLV_TSF_support_chassis_\w+)\s*=\s*\{', c):
    cid = m.group(2)
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

    new_chunks.append(c[last:m.start()])
    block = c[m.start():block_end + 1]

    # 各 stat を multiplier 適用
    chassis_changes = 0
    for stat, mult in MULTIPLIERS.items():
        block, n = re.subn(rf'(\s)({stat})\s*=\s*([\d.]+)', lambda mm, _s=stat, _m=mult: (
            f"{mm.group(1)}{_s} = {round_smart(float(mm.group(3)) * _m)}"
        ), block)
        if n > 0:
            chassis_changes += n

    if chassis_changes > 0:
        print(f"  {cid}: {chassis_changes} stats 更新")
        total_changes += chassis_changes
    new_chunks.append(block)
    last = block_end + 1
new_chunks.append(c[last:])
c = "".join(new_chunks)

with open(SUPPORT, "w", encoding="utf-8") as f:
    f.write(c)

print(f"\n合計: {total_changes} stat 更新")

# ブレース整合性
o, x = c.count("{"), c.count("}")
print(f"\nブレース: {o}/{x} diff={o-x}")
