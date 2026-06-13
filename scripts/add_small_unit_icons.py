# -*- coding: utf-8 -*-
"""
MVLV_subuniticons.gfx の各 _medium ユニットアイコンに対応する _small を追加
HOI4 はマップ上の counter 表示に GFX_unit_<sprite>_icon_small を要求する
"""
import re
import os

GFX = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod\interface\MVLV_subuniticons.gfx"

with open(GFX, "r", encoding="utf-8", errors="replace") as f:
    c = f.read()

# name -> texturefile を取得（textureFile / texturefile 両対応）
sprites = {}
for m in re.finditer(
    r'name\s*=\s*"(GFX_unit_MVLV_[\w]+_icon_medium(?:_white)?)"\s*[\r\n]+\s*texture[fF]ile\s*=\s*"([^"]+)"',
    c,
):
    sprites[m.group(1)] = m.group(2)

# 既に存在する _small
existing_small = set(re.findall(r'name\s*=\s*"(GFX_unit_MVLV_[\w]+_icon_small)"', c))

new_entries = []
for name, tex in sprites.items():
    if not name.endswith("_icon_medium"):
        continue  # _white はベースにしない
    base = name[: -len("_medium")]  # GFX_unit_MVLV_X_icon
    small_name = base + "_small"
    if small_name in existing_small:
        continue
    # onmap 用 texture を優先（_medium_white のもの）
    white_tex = sprites.get(name + "_white")
    small_tex = white_tex if white_tex else tex
    new_entries.append((small_name, small_tex))

# ファイル末尾の最後の } の前に挿入
block = "\n\t### auto-added _small variants (map counter) ###\n"
for name, tex in new_entries:
    block += (
        f'\tSpriteType = {{\n'
        f'\t\tname = "{name}"\n'
        f'\t\ttexturefile = "{tex}"\n'
        f'\t\tnoOfFrames = 2\n'
        f'\t}}\n'
    )

idx = c.rfind("}")
c = c[:idx] + block + c[idx:]

with open(GFX, "w", encoding="utf-8") as f:
    f.write(c)

print(f"既存 medium sprite: {len([s for s in sprites if s.endswith('_icon_medium')])}")
print(f"_small 追加: {len(new_entries)}")
for n, t in new_entries:
    print(f"  + {n}")

# ブレース整合性
o, x = c.count("{"), c.count("}")
print(f"\nブレース: {o}/{x} diff={o-x}")
