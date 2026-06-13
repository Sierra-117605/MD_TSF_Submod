# -*- coding: utf-8 -*-
"""
テック側 picture = GFX_tsf_X_medium 参照をベースに、
HOI4 が自動探索する GFX_<tech_id>_medium 名でエイリアス sprite を新規 gfx に作成。

- 入力: common/technologies/MVLV_NSB_TSF.txt の `picture = GFX_tsf_X_medium`
- 入力: interface/MVLV_TSF_technology_icons.gfx の texturefile
- 出力: interface/MVLV_research_tech_icons.gfx (98 sprite 予定、300 未満)
"""
import re
import os

MOD = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod"
TECH = os.path.join(MOD, "common", "technologies", "MVLV_NSB_TSF.txt")
SRC_GFX = os.path.join(MOD, "interface", "MVLV_TSF_technology_icons.gfx")
DST_GFX = os.path.join(MOD, "interface", "MVLV_research_tech_icons.gfx")

# 既存 sprite name -> texturefile マップを構築
with open(SRC_GFX, "r", encoding="utf-8", errors="replace") as f:
    src = f.read()

sprite_tex = {}
for m in re.finditer(
    r'SpriteType\s*=\s*\{\s*name\s*=\s*"([^"]+)"\s*texturefile\s*=\s*"([^"]+)"',
    src,
):
    sprite_tex[m.group(1)] = m.group(2)

print(f"既存 sprite map: {len(sprite_tex)} 件")

# テックファイルから (tech_id, picture_name) を抽出
with open(TECH, "r", encoding="utf-8", errors="replace") as f:
    tech = f.read()

# 各 tech block で tech_id と picture を取り出す
out_blocks = []
pattern = re.compile(r'^\t([A-Za-z][\w-]+)\s*=\s*\{', re.MULTILINE)
matches = list(pattern.finditer(tech))

found_pairs = []
for m in matches:
    tech_id = m.group(1)
    brace_pos = m.end() - 1
    # block end
    depth = 1
    i = brace_pos + 1
    while i < len(tech) and depth > 0:
        if tech[i] == "{":
            depth += 1
        elif tech[i] == "}":
            depth -= 1
            if depth == 0:
                break
        i += 1
    block_body = tech[brace_pos + 1:i]
    pm = re.search(r"^\s*picture\s*=\s*([\w\-]+)", block_body, re.MULTILINE)
    if pm:
        found_pairs.append((tech_id, pm.group(1)))

print(f"テック picture 参照: {len(found_pairs)} 件")

# alias sprite を生成
out = ["spriteTypes = {"]
generated = 0
missing = []
for tech_id, pic in found_pairs:
    if pic not in sprite_tex:
        missing.append((tech_id, pic))
        continue
    texturefile = sprite_tex[pic]
    alias_name = f"GFX_{tech_id}_medium"
    out.append(f'\tSpriteType = {{')
    out.append(f'\t\tname = "{alias_name}"')
    out.append(f'\t\ttexturefile = "{texturefile}"')
    out.append(f'\t}}')
    generated += 1
out.append("}\n")

with open(DST_GFX, "w", encoding="utf-8") as f:
    f.write("\n".join(out))

print(f"\n生成 sprite: {generated}")
print(f"出力: {os.path.basename(DST_GFX)}")
if missing:
    print(f"texture 不明スキップ: {len(missing)}")
    for t, p in missing[:5]:
        print(f"  - {t} -> {p}")
