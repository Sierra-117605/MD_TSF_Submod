# -*- coding: utf-8 -*-
"""
動作確認できているテクスチャを使って、空表示テックの sprite テクスチャを差し替える
カテゴリ別に近い見た目のテクスチャを当てがう
"""
import re

GFX = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod\interface\MVLV_TSF_technology_icons.gfx"

# 動作確認できている texture file path（カテゴリ別）
WORKING_TEXTURES = {
    "weapon":   "gfx/interface/equipmentdesigner/TSF/modules/assault_cannon_1_pic.dds",  # 火器系
    "engine":   "gfx/interface/equipmentdesigner/TSF/modules/engine_normal_pic.dds",     # 推進・エンジン系
    "head":     "gfx/interface/equipmentdesigner/TSF/modules/headUnit_normal_pic.dds",   # センサー・電装系
    "armor":    "gfx/interface/equipmentdesigner/TSF/modules/heavy_armor_pic.dds",       # 装甲・構造材系
    "shield":   "gfx/interface/equipmentdesigner/TSF/modules/aerial_blade_armor_pic.dds", # 盾・ブレード系
    "missile":  "gfx/interface/equipmentdesigner/TSF/modules/assault_cannon_2_pic.dds",  # ミサイル系
    "OS":       "gfx/interface/equipmentdesigner/TSF/modules/OS_normal_pic.dds",         # OS 系
    "supplies": "gfx/interface/equipmentdesigner/TSF/modules/add_armor_pic.dds",         # 物資・整備系
}

# 空表示テックを動作 texture に再マッピング
# テック名 -> 動作 texture (key)
REMAPPING = {
    # 構造材系（装甲扱い）
    "special_structure_1": "armor",
    "special_structure_2": "armor",
    "special_structure_3": "armor",
    "special_structure_4": "armor",
    "reinforced_structure_1": "armor",
    "reinforced_structure_2": "armor",
    "reinforced_structure_3": "armor",
    # 盾系
    "shield": "shield",
    "reactive_shield": "shield",
    # 武器系
    "railgun_1": "weapon",
    "railgun_2": "weapon",
    "railgun_3": "weapon",
    "support_gun": "weapon",
    "support_assault_cannon_1": "weapon",
    "support_assault_cannon_2": "weapon",
    "support_assault_cannon_3": "weapon",
    "combat_sword": "shield",
    # ミサイル系
    "small_missile": "missile",
    "large_missile_1": "missile",
    "large_missile_2": "missile",
    # センサー・電装系
    "add_sensor_1": "head",
    "add_sensor_2": "head",
    "add_sensor_3": "head",
    "deta_link_1": "head",
    "deta_link_2": "head",
    "deta_link_3": "head",
    "custom_sights": "head",
    "custom_shells": "head",
    # 物資・整備系
    "supplies": "supplies",
    "maintenance_team_1": "supplies",
    "maintenance_team_2": "supplies",
    "maintenance_team_3": "supplies",
    "capture_team": "supplies",
    # 特化モジュール
    "custom_module_1": "OS",
    "custom_module_2": "OS",
    # ブレード装甲系（必要なら）
    "add_blade_armor": "shield",
    "add_aerial_blade_armor": "shield",
    "special_blade_armor": "shield",
}

with open(GFX, "r", encoding="utf-8") as f:
    content = f.read()

count = 0
for tech_short, category in REMAPPING.items():
    sprite_name = f"GFX_MVLV_research_{tech_short}_medium"
    new_texture = WORKING_TEXTURES[category]
    # SpriteType ブロック を name 一致で texturefile を置換
    pattern = re.compile(
        r'(SpriteType\s*=\s*\{\s*name\s*=\s*"' + re.escape(sprite_name) + r'"\s*texturefile\s*=\s*")[^"]+(")',
        re.IGNORECASE
    )
    new_content, n = pattern.subn(r'\g<1>' + new_texture + r'\g<2>', content)
    if n > 0:
        content = new_content
        count += n

with open(GFX, "w", encoding="utf-8") as f:
    f.write(content)
print(f"sprite texture 再マッピング: {count}")
