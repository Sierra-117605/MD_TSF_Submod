# -*- coding: utf-8 -*-
"""
MVLV_TSF_old_technology_icons.gfx (301 sprite) を 2 ファイルに分割
HOI4 の 300/file 上限を回避
"""
import re, os

MOD = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod"
SRC = os.path.join(MOD, "interface", "MVLV_TSF_old_technology_icons.gfx")
DST_A = os.path.join(MOD, "interface", "MVLV_TSF_old_technology_icons_a.gfx")
DST_B = os.path.join(MOD, "interface", "MVLV_TSF_old_technology_icons_b.gfx")

with open(SRC, "r", encoding="utf-8", errors="replace") as f:
    content = f.read()

# spriteTypes = { ... } の中身を取得
m = re.search(r'spriteTypes\s*=\s*\{', content)
inner_start = m.end()
# 末尾の } を探す（最後の }）
inner_end = content.rfind("}")
inner = content[inner_start:inner_end]

# 各 SpriteType ブロックを抽出（ブレースカウントで安全に）
sprite_blocks = []
i = 0
while i < len(inner):
    m2 = re.search(r'SpriteType\s*=\s*\{', inner[i:])
    if not m2:
        break
    abs_start = i + m2.start()
    abs_brace = i + m2.end() - 1
    depth = 1
    j = abs_brace + 1
    while j < len(inner) and depth > 0:
        c = inner[j]
        if c == "{": depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0: break
        j += 1
    sprite_blocks.append(inner[abs_start:j+1])
    i = j + 1

print(f"抽出 SpriteType ブロック数: {len(sprite_blocks)}")

# 半分に分割
half = len(sprite_blocks) // 2
part_a = sprite_blocks[:half]
part_b = sprite_blocks[half:]

def emit(blocks):
    body = "\n\t".join(blocks)
    return "spriteTypes = {\n\t" + body + "\n}\n"

with open(DST_A, "w", encoding="utf-8") as f:
    f.write(emit(part_a))
with open(DST_B, "w", encoding="utf-8") as f:
    f.write(emit(part_b))

print(f"  -> {os.path.basename(DST_A)}: {len(part_a)} sprite")
print(f"  -> {os.path.basename(DST_B)}: {len(part_b)} sprite")

# 元ファイルを削除（バックアップ名にリネーム）
import shutil
bak = SRC + ".bak_split"
shutil.move(SRC, bak)
print(f"元ファイルを退避: {os.path.basename(bak)}")
