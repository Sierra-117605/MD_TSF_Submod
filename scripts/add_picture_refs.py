# -*- coding: utf-8 -*-
"""
MVLV_NSB_TSF.txt の各テックに、対応する GFX_tsf_<short>_medium を picture として明示参照
これで sprite 追加なしでテックアイコン表示
"""
import re
import os

MOD = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod"
TECH = os.path.join(MOD, "common", "technologies", "MVLV_NSB_TSF.txt")
GFX = os.path.join(MOD, "interface", "MVLV_TSF_technology_icons.gfx")

# 既存 GFX_tsf_* sprite を全件取得
with open(GFX, "r", encoding="utf-8", errors="replace") as f:
    gfx_content = f.read()

available_sprites = set()
for m in re.finditer(r'name\s*=\s*"(GFX_tsf_[\w-]+_medium)"', gfx_content):
    available_sprites.add(m.group(1))

print(f"利用可能 GFX_tsf_*_medium sprite: {len(available_sprites)}")

# テック ファイル更新
with open(TECH, "r", encoding="utf-8", errors="replace") as f:
    tech_content = f.read()

# 各テックブロックに picture = ... を追加
# tech 名 MVLV_research_<X> から GFX_tsf_<X>_medium を生成

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


added = 0
skipped = 0
# トップレベル tech 検出
pattern = re.compile(r'^\t([A-Za-z][\w-]+)\s*=\s*\{', re.MULTILINE)
matches = list(pattern.finditer(tech_content))

# 後ろから処理（オフセットずらさないため）
for m in reversed(matches):
    tech_name = m.group(1)
    if not tech_name.startswith("MVLV_research_"):
        continue
    short = tech_name[len("MVLV_research_"):]
    candidate = f"GFX_tsf_{short}_medium"
    if candidate not in available_sprites:
        skipped += 1
        continue

    brace_pos = m.end() - 1
    block_end = find_block_end(tech_content, brace_pos)
    if block_end < 0:
        continue
    block_body = tech_content[brace_pos + 1:block_end]

    # 既に picture = があればスキップ
    if re.search(r"^\s*picture\s*=", block_body, re.MULTILINE):
        continue

    # ブロック先頭（{ の直後）に picture = ... を挿入
    insert_text = f"\n\t\tpicture = {candidate}"
    new_content = (
        tech_content[:brace_pos + 1]
        + insert_text
        + tech_content[brace_pos + 1:]
    )
    tech_content = new_content
    added += 1

with open(TECH, "w", encoding="utf-8") as f:
    f.write(tech_content)

print(f"picture 追加: {added}")
print(f"sprite 不一致でスキップ: {skipped}")
