# -*- coding: utf-8 -*-
"""
Plan B 適用：検証済み default_modules を chassis ファイルに挿入
plan_b_validate.py の検証ロジックを使い、書き込み実施
"""
import re
import os
import sys
import shutil

# plan_b_validate と同じ MOD パス
MOD = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod"
EQ_DIR = os.path.join(MOD, "common", "units", "equipment")

# 同じ DEFAULTS をインポート（コピペ）
DEFAULTS = {
    "1_light": {"armor_slot": "MVLV_TSF_armor_light", "OS_slot": "MVLV_TSF_OS_1_normal", "engine_slot": "MVLV_TSF_engine_1", "headUnit_slot": "MVLV_TSF_head_normal_1", "right_hand_slot": "MVLV_TSF_assault_cannon_1", "left_hand_slot": "MVLV_TSF_shield"},
    "1_light_mod": {"armor_slot": "MVLV_TSF_armor_light", "OS_slot": "MVLV_TSF_OS_1_normal", "engine_slot": "MVLV_TSF_engine_1", "headUnit_slot": "MVLV_TSF_head_normal_1", "right_hand_slot": "MVLV_TSF_assault_cannon_1", "left_hand_slot": "MVLV_TSF_shield"},
    "1_heavy": {"armor_slot": "MVLV_TSF_armor_heavy", "OS_slot": "MVLV_TSF_OS_1_normal", "engine_slot": "MVLV_TSF_engine_1", "headUnit_slot": "MVLV_TSF_head_heavy_1", "right_hand_slot": "MVLV_TSF_assault_cannon_1", "left_hand_slot": "MVLV_TSF_shield"},
    "2_light": {"armor_slot": "MVLV_TSF_armor_light", "OS_slot": "MVLV_TSF_OS_2_normal", "engine_slot": "MVLV_TSF_engine_2", "headUnit_slot": "MVLV_TSF_head_normal_2", "right_hand_slot": "MVLV_TSF_assault_cannon_2", "left_hand_slot": "MVLV_TSF_shield"},
    "2_heavy": {"armor_slot": "MVLV_TSF_armor_composite", "OS_slot": "MVLV_TSF_OS_2_normal", "engine_slot": "MVLV_TSF_engine_2", "headUnit_slot": "MVLV_TSF_head_heavy_2", "right_hand_slot": "MVLV_TSF_assault_cannon_2", "left_hand_slot": "MVLV_TSF_shield"},
    "2_maneuver": {"armor_slot": "MVLV_TSF_armor_light", "OS_slot": "MVLV_TSF_OS_2_close", "engine_slot": "MVLV_TSF_engine_maneuver_2", "headUnit_slot": "MVLV_TSF_head_normal_2", "right_hand_slot": "MVLV_TSF_assault_cannon_2", "left_hand_slot": "MVLV_TSF_long_sword"},
    "3_light": {"armor_slot": "MVLV_TSF_armor_light", "OS_slot": "MVLV_TSF_OS_3_normal", "engine_slot": "MVLV_TSF_engine_3", "headUnit_slot": "MVLV_TSF_head_normal_3", "right_hand_slot": "MVLV_TSF_assault_cannon_3", "left_hand_slot": "MVLV_TSF_shield"},
    "3_heavy": {"armor_slot": "MVLV_TSF_armor_composite", "OS_slot": "MVLV_TSF_OS_3_normal", "engine_slot": "MVLV_TSF_engine_3", "headUnit_slot": "MVLV_TSF_head_heavy_3", "right_hand_slot": "MVLV_TSF_assault_cannon_3", "left_hand_slot": "MVLV_TSF_shield"},
    "3_maneuver": {"armor_slot": "MVLV_TSF_armor_light", "OS_slot": "MVLV_TSF_OS_XM3", "engine_slot": "MVLV_TSF_engine_maneuver_3", "headUnit_slot": "MVLV_TSF_head_normal_3", "right_hand_slot": "MVLV_TSF_assault_cannon_3", "left_hand_slot": "MVLV_TSF_long_sword"},
    "4": {"armor_slot": "MVLV_TSF_armor_composite", "sp_slot_1": "MVLV_TSF_special_structure_4", "OS_slot": "MVLV_TSF_OS_4_normal", "engine_slot": "MVLV_TSF_engine_4", "headUnit_slot": "MVLV_TSF_head_aerial_3", "right_hand_slot": "MVLV_TSF_assault_cannon_3", "left_hand_slot": "MVLV_TSF_reactive_shield"},
}


def adjust_for_role(defaults_dict, suffix, role):
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


def make_default_modules_block(defaults):
    lines = ["\t\tdefault_modules = {"]
    for slot_short, module in defaults.items():
        lines.append("\t\t\tMVLV_TSF_" + slot_short + " = " + module)
    lines.append("\t\t}")
    return "\n".join(lines)


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


def process_file(path, role):
    """role: chassis, support, specialForces"""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    # archetype 名
    if role == "chassis":
        arche = "MVLV_TSF_chassis"
    elif role == "support":
        arche = "MVLV_TSF_support_chassis"
    else:
        arche = "MVLV_TSF_specialForces_chassis"
    # variant パターン: 名前 = {  (名前は arche_suffix 形式)
    pattern = re.compile(r"(" + re.escape(arche) + r")_(\w+)\s*=\s*\{")
    matches = list(pattern.finditer(content))
    count = 0
    # 後ろから処理してオフセットがズレないようにする
    for m in reversed(matches):
        suffix = m.group(2)
        if suffix not in DEFAULTS:
            continue
        brace_pos = m.end() - 1
        block_end = find_block_end(content, brace_pos)
        if block_end < 0:
            continue
        block = content[m.start():block_end + 1]
        # 既存 default_modules があればスキップ
        if "default_modules" in block:
            continue
        # 挿入
        defaults = adjust_for_role(DEFAULTS[suffix], suffix, role)
        block_text = make_default_modules_block(defaults)
        # 末尾 } 直前に挿入
        new_block = block[:-1] + "\n" + block_text + "\n\t" + block[-1:]
        content = content[:m.start()] + new_block + content[block_end + 1:]
        count += 1
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return count


c1 = process_file(os.path.join(EQ_DIR, "MVLV_TSF_chassis.txt"), "chassis")
c2 = process_file(os.path.join(EQ_DIR, "MVLV_TSF_support_chassis.txt"), "support")
c3 = process_file(os.path.join(EQ_DIR, "MVLV_TSF_specialForces_chassis.txt"), "specialForces")

print("通常 chassis: 追加 variant =", c1)
print("支援 chassis: 追加 variant =", c2)
print("特務 chassis: 追加 variant =", c3)
print("合計:", c1 + c2 + c3)
