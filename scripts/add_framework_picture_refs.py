# -*- coding: utf-8 -*-
"""
framework 系 / debug_pack の 12 テックに picture = ... を明示追加
add_picture_refs.py では命名差分（tsf_ prefix）でスキップされていた分を補完
"""
import re
import os

MOD = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod"
TECH = os.path.join(MOD, "common", "technologies", "MVLV_NSB_TSF.txt")

# 明示マッピング: tech_id -> sprite name
MAPPING = {
    "MVLV_research_basic_tsf_framework":         "GFX_tsf_basic_framework_medium",
    "MVLV_research_tsf_1_light_framework":       "GFX_tsf_1_light_framework_medium",
    "MVLV_research_tsf_1_light_mod_framework":   "GFX_tsf_1_light_framework_medium",  # 代用
    "MVLV_research_tsf_1_heavy_framework":       "GFX_tsf_1_heavy_framework_medium",
    "MVLV_research_tsf_2_light_framework":       "GFX_tsf_2_light_framework_medium",
    "MVLV_research_tsf_2_heavy_framework":       "GFX_tsf_2_heavy_framework_medium",
    "MVLV_research_tsf_2_maneuver_framework":    "GFX_tsf_2_maneuver_framework_medium",
    "MVLV_research_tsf_3_light_framework":       "GFX_tsf_3_light_framework_medium",
    "MVLV_research_tsf_3_heavy_framework":       "GFX_tsf_3_heavy_framework_medium",
    "MVLV_research_tsf_3_maneuver_framework":    "GFX_tsf_3_maneuver_framework_medium",
    "MVLV_research_tsf_4_framework":             "GFX_tsf_4_framework_medium",
    "MVLV_research_debug_pack":                  "GFX_tsf_basic_framework_medium",     # 代用
}


def find_block_end(content, open_brace_pos):
    depth = 1
    i = open_brace_pos + 1
    while i < len(content) and depth > 0:
        c = content[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


with open(TECH, "r", encoding="utf-8", errors="replace") as f:
    tech_content = f.read()

added = 0
already = 0
notfound = 0

# 後ろから処理（オフセットずらさないため）
pattern = re.compile(r'^\t([A-Za-z][\w-]+)\s*=\s*\{', re.MULTILINE)
matches = list(pattern.finditer(tech_content))

for m in reversed(matches):
    tech_name = m.group(1)
    if tech_name not in MAPPING:
        continue
    candidate = MAPPING[tech_name]

    brace_pos = m.end() - 1
    block_end = find_block_end(tech_content, brace_pos)
    if block_end < 0:
        continue
    block_body = tech_content[brace_pos + 1:block_end]

    if re.search(r"^\s*picture\s*=", block_body, re.MULTILINE):
        already += 1
        continue

    insert_text = f"\n\t\tpicture = {candidate}"
    tech_content = (
        tech_content[:brace_pos + 1]
        + insert_text
        + tech_content[brace_pos + 1:]
    )
    added += 1
    print(f"  + {tech_name} -> {candidate}")

with open(TECH, "w", encoding="utf-8") as f:
    f.write(tech_content)

print(f"\n追加: {added}")
print(f"既存スキップ: {already}")
