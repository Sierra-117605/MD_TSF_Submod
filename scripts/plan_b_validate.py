# -*- coding: utf-8 -*-
"""
Plan B: 各 chassis variant に default_modules を追加（検証付き）
カテゴリ整合性を事前検証してからファイル書き込み
"""
import re
import os
import sys

MOD = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod"
EQ_DIR = os.path.join(MOD, "common", "units", "equipment")
MOD_DIR = os.path.join(EQ_DIR, "modules")

# === Step 1: 全モジュールのカテゴリを取得 ===
module_category = {}
for fname in os.listdir(MOD_DIR):
    if not fname.endswith(".txt"):
        continue
    with open(os.path.join(MOD_DIR, fname), "r", encoding="utf-8") as f:
        lines = f.readlines()
    cur_mod = None
    for line in lines:
        s = line.strip()
        if s.startswith("#"):
            continue
        m = re.match(r"^([A-Za-z][\w-]*)\s*=\s*\{", s)
        if m:
            cur_mod = m.group(1)
        m = re.match(r"^category\s*=\s*([A-Za-z][\w-]*)", s)
        if m and cur_mod:
            module_category[cur_mod] = m.group(1)
            cur_mod = None

print("モジュール総数:", len(module_category))

# === Step 2: スロットの許可カテゴリ（chassis archetype から手動転記） ===
SLOT_ALLOWED = {
    "MVLV_TSF_armor_slot":       ["MVLV_TSF_armor_type"],
    "MVLV_TSF_OS_slot":          ["MVLV_TSF_OS_normal_type", "MVLV_TSF_OS_close_type", "MVLV_TSF_OS_support_type"],
    "MVLV_TSF_engine_slot":      ["MVLV_TSF_engine_normal_type", "MVLV_TSF_engine_maneuver_type", "MVLV_TSF_engine_cruise_type"],
    "MVLV_TSF_headUnit_slot":    ["MVLV_TSF_headUnit_nomal_type", "MVLV_TSF_headUnit_heavy_type", "MVLV_TSF_headUnit_aerial_type"],
    "MVLV_TSF_right_hand_slot":  ["MVLV_TSF_right_hand_type"],
    "MVLV_TSF_left_hand_slot":   ["MVLV_TSF_shield_type", "MVLV_TSF_sword_type", "MVLV_TSF_add_wepon_type"],
    "MVLV_TSF_sp_slot_1":        ["MVLV_TSF_sp_dataLink_type", "MVLV_TSF_sp_fcs_type", "MVLV_TSF_sp_structure_type",
                                  "MVLV_TSF_sp_vibration_sensor_type", "MVLV_TSF_sp_shell_type", "MVLV_TSF_sp_sight_type",
                                  "MVLV_TSF_sp_maintenance_team_type", "MVLV_TSF_sp_custom_module_type"],
}

# === Step 3: variant suffix ごとの default_modules ===
DEFAULTS = {
    "1_light": {
        "armor_slot": "MVLV_TSF_armor_light",
        "OS_slot": "MVLV_TSF_OS_1_normal",
        "engine_slot": "MVLV_TSF_engine_1",
        "headUnit_slot": "MVLV_TSF_head_normal_1",
        "right_hand_slot": "MVLV_TSF_assault_cannon_1",
        "left_hand_slot": "MVLV_TSF_shield",
    },
    "1_light_mod": {
        "armor_slot": "MVLV_TSF_armor_light",
        "OS_slot": "MVLV_TSF_OS_1_normal",
        "engine_slot": "MVLV_TSF_engine_1",
        "headUnit_slot": "MVLV_TSF_head_normal_1",
        "right_hand_slot": "MVLV_TSF_assault_cannon_1",
        "left_hand_slot": "MVLV_TSF_shield",
    },
    "1_heavy": {
        "armor_slot": "MVLV_TSF_armor_heavy",
        "OS_slot": "MVLV_TSF_OS_1_normal",
        "engine_slot": "MVLV_TSF_engine_1",
        "headUnit_slot": "MVLV_TSF_head_heavy_1",
        "right_hand_slot": "MVLV_TSF_assault_cannon_1",
        "left_hand_slot": "MVLV_TSF_shield",
    },
    "2_light": {
        "armor_slot": "MVLV_TSF_armor_light",
        "OS_slot": "MVLV_TSF_OS_2_normal",
        "engine_slot": "MVLV_TSF_engine_2",
        "headUnit_slot": "MVLV_TSF_head_normal_2",
        "right_hand_slot": "MVLV_TSF_assault_cannon_2",
        "left_hand_slot": "MVLV_TSF_shield",
    },
    "2_heavy": {
        "armor_slot": "MVLV_TSF_armor_composite",
        "OS_slot": "MVLV_TSF_OS_2_normal",
        "engine_slot": "MVLV_TSF_engine_2",
        "headUnit_slot": "MVLV_TSF_head_heavy_2",
        "right_hand_slot": "MVLV_TSF_assault_cannon_2",
        "left_hand_slot": "MVLV_TSF_shield",
    },
    "2_maneuver": {
        "armor_slot": "MVLV_TSF_armor_light",
        "OS_slot": "MVLV_TSF_OS_2_close",
        "engine_slot": "MVLV_TSF_engine_maneuver_2",
        "headUnit_slot": "MVLV_TSF_head_normal_2",
        "right_hand_slot": "MVLV_TSF_assault_cannon_2",
        "left_hand_slot": "MVLV_TSF_long_sword",
    },
    "3_light": {
        "armor_slot": "MVLV_TSF_armor_light",
        "OS_slot": "MVLV_TSF_OS_3_normal",
        "engine_slot": "MVLV_TSF_engine_3",
        "headUnit_slot": "MVLV_TSF_head_normal_3",
        "right_hand_slot": "MVLV_TSF_assault_cannon_3",
        "left_hand_slot": "MVLV_TSF_shield",
    },
    "3_heavy": {
        "armor_slot": "MVLV_TSF_armor_composite",
        "OS_slot": "MVLV_TSF_OS_3_normal",
        "engine_slot": "MVLV_TSF_engine_3",
        "headUnit_slot": "MVLV_TSF_head_heavy_3",
        "right_hand_slot": "MVLV_TSF_assault_cannon_3",
        "left_hand_slot": "MVLV_TSF_shield",
    },
    "3_maneuver": {
        "armor_slot": "MVLV_TSF_armor_light",
        "OS_slot": "MVLV_TSF_OS_XM3",
        "engine_slot": "MVLV_TSF_engine_maneuver_3",
        "headUnit_slot": "MVLV_TSF_head_normal_3",
        "right_hand_slot": "MVLV_TSF_assault_cannon_3",
        "left_hand_slot": "MVLV_TSF_long_sword",
    },
    "4": {
        "armor_slot": "MVLV_TSF_armor_composite",
        "sp_slot_1": "MVLV_TSF_special_structure_4",
        "OS_slot": "MVLV_TSF_OS_4_normal",
        "engine_slot": "MVLV_TSF_engine_4",
        "headUnit_slot": "MVLV_TSF_head_aerial_3",
        "right_hand_slot": "MVLV_TSF_assault_cannon_3",
        "left_hand_slot": "MVLV_TSF_reactive_shield",
    },
}


def adjust_for_role(defaults_dict, suffix, role):
    """role に応じてモジュールを置き換え"""
    d = dict(defaults_dict)
    if role == "support" and suffix != "4":
        gen = suffix.split("_")[0]
        if gen in ("1", "2", "3"):
            d["OS_slot"] = "MVLV_TSF_OS_" + gen + "_support"
            d["right_hand_slot"] = "MVLV_TSF_support_assault_cannon_" + gen
    elif role == "specialForces" and suffix != "4":
        gen = suffix.split("_")[0]
        if gen in ("1", "2", "3"):
            d["OS_slot"] = "MVLV_TSF_OS_" + gen + "_close"
        d["left_hand_slot"] = "MVLV_TSF_long_sword"
    return d


# === Step 4: 検証 ===
def validate(suffix, role, defaults_dict):
    errors = []
    for slot_short, mod in defaults_dict.items():
        slot_full = "MVLV_TSF_" + slot_short
        if mod not in module_category:
            errors.append("  [%s %s] %s = %s : モジュール未定義" % (role, suffix, slot_full, mod))
            continue
        cat = module_category[mod]
        if slot_full in SLOT_ALLOWED:
            allowed = SLOT_ALLOWED[slot_full]
            if cat not in allowed:
                errors.append("  [%s %s] %s = %s : カテゴリ %s が許可 %s に含まれない" % (role, suffix, slot_full, mod, cat, allowed))
    return errors


print("\n=== 検証 ===")
all_errors = []
for role in ["chassis", "support", "specialForces"]:
    for suffix, defaults in DEFAULTS.items():
        adjusted = adjust_for_role(defaults, suffix, role)
        errors = validate(suffix, role, adjusted)
        all_errors.extend(errors)

if all_errors:
    print("❌ エラーあり：")
    for e in all_errors:
        print(e)
    print("\n合計エラー数:", len(all_errors))
    sys.exit(1)
else:
    print("✅ 全 default_modules 検証パス")
    print("検証された組合せ: 3 role x 11 suffix = 33 variant")
