# -*- coding: utf-8 -*-
"""
TSF と MD 戦車の性能比較データを抽出
我々の MOD・元 MOD・MD Beta から
出力: Markdown 表
"""
import re
import os


def extract_stats(content, variant_name):
    """variant ブロックから性能値を抽出"""
    m = re.search(re.escape(variant_name) + r"\s*=\s*\{", content)
    if not m:
        return None
    depth = 1
    i = m.end()
    while i < len(content) and depth > 0:
        if content[i] == "{":
            depth += 1
        elif content[i] == "}":
            depth -= 1
        i += 1
    block = content[m.end():i - 1]
    fields = ["soft_attack", "hard_attack", "air_attack", "defense", "breakthrough",
              "armor_value", "hardness", "ap_attack", "maximum_speed",
              "max_organisation", "max_strength", "reliability",
              "build_cost_ic", "manpower"]
    stats = {}
    for f in fields:
        m2 = re.search(r"^\s*" + f + r"\s*=\s*(-?[\d.]+)", block, re.MULTILINE)
        stats[f] = m2.group(1) if m2 else "-"
    return stats


OUR = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod\common\units\equipment"
ORIG = r"C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\3372337928\common\units\equipment"
MD = r"C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\3374271790\common\units\equipment"


def load(path):
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# TSF chassis variants to compare
TSF_VARIANTS = [
    "MVLV_TSF_chassis_0",
    "MVLV_TSF_chassis_1_light",
    "MVLV_TSF_chassis_1_heavy",
    "MVLV_TSF_chassis_2_light",
    "MVLV_TSF_chassis_2_heavy",
    "MVLV_TSF_chassis_2_maneuver",
    "MVLV_TSF_chassis_3_light",
    "MVLV_TSF_chassis_3_heavy",
    "MVLV_TSF_chassis_3_maneuver",
    "MVLV_TSF_chassis_4",
]

# MD Beta tank chassis variants（実在する名前）
MD_TANK_VARIANTS = [
    "medium_tank_chassis_0",  # 1965
    "medium_tank_chassis_1",
    "medium_tank_chassis_2",
    "medium_tank_chassis_3",
    "medium_tank_chassis_4",
    "medium_tank_chassis_5",
    "medium_tank_chassis_6",  # 最新
    "heavy_tank_chassis_0",
    "heavy_tank_chassis_3",
    "heavy_tank_chassis_6",
    "super_heavy_tank_chassis_0",
    "super_heavy_tank_chassis_2",
    "walker_tank_chassis_0",  # 歩行戦車
    "walker_tank_chassis_1",
]

# 我々の chassis
our_chassis = load(os.path.join(OUR, "MVLV_TSF_chassis.txt"))
# 元 MOD の chassis
orig_chassis = load(os.path.join(ORIG, "MVLV_TSF_chassis.txt"))
# MD Beta の戦車を探す
md_files_to_search = []
if os.path.exists(MD):
    for f in os.listdir(MD):
        if f.endswith(".txt"):
            md_files_to_search.append(os.path.join(MD, f))


def find_in_md(variant):
    for path in md_files_to_search:
        content = load(path)
        stats = extract_stats(content, variant)
        if stats:
            return stats
    return None


# 表生成
print("# 戦術機 性能比較表（我々 MOD vs 元 MOD vs MD Beta 戦車）")
print()
print("## 我々の MOD（Plan B 適用後）")
print()
print("| Variant | soft_atk | hard_atk | air_atk | defense | breakthr | armor | hardness | ap_atk | speed | max_org | max_str | reliability | cost_ic |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for v in TSF_VARIANTS:
    s = extract_stats(our_chassis, v)
    if s:
        print(f"| {v.replace('MVLV_TSF_chassis_', '')} | {s['soft_attack']} | {s['hard_attack']} | {s['air_attack']} | {s['defense']} | {s['breakthrough']} | {s['armor_value']} | {s['hardness']} | {s['ap_attack']} | {s['maximum_speed']} | {s['max_organisation']} | {s['max_strength']} | {s['reliability']} | {s['build_cost_ic']} |")

print()
print("## 元 MOD（参考）")
print()
print("| Variant | soft_atk | hard_atk | air_atk | defense | breakthr | armor | hardness | ap_atk | speed | max_org | max_str | reliability | cost_ic |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for v in TSF_VARIANTS:
    s = extract_stats(orig_chassis, v)
    if s:
        print(f"| {v.replace('MVLV_TSF_chassis_', '')} | {s['soft_attack']} | {s['hard_attack']} | {s['air_attack']} | {s['defense']} | {s['breakthrough']} | {s['armor_value']} | {s['hardness']} | {s['ap_attack']} | {s['maximum_speed']} | {s['max_organisation']} | {s['max_strength']} | {s['reliability']} | {s['build_cost_ic']} |")

print()
print("## MD Beta 戦車・装甲車・自走砲（参考）")
print()
print("| Variant | soft_atk | hard_atk | air_atk | defense | breakthr | armor | hardness | ap_atk | speed | max_org | max_str | reliability | cost_ic |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for v in MD_TANK_VARIANTS:
    s = find_in_md(v)
    if s:
        print(f"| {v} | {s['soft_attack']} | {s['hard_attack']} | {s['air_attack']} | {s['defense']} | {s['breakthrough']} | {s['armor_value']} | {s['hardness']} | {s['ap_attack']} | {s['maximum_speed']} | {s['max_organisation']} | {s['max_strength']} | {s['reliability']} | {s['build_cost_ic']} |")
