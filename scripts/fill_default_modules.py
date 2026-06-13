# -*- coding: utf-8 -*-
# 通常機(chassis_light/heavy/maneuver)の空き追加スロットを世代相応の追加装備で埋める
import re, os

MOD = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod"
EQ = os.path.join(MOD, "common", "units", "equipment")
FILES = ["MVLV_TSF_zz_country_variants.txt", "MVLV_TSF_zz_common_variants.txt"]
NORMAL_ARCH = {"MVLV_TSF_chassis_light", "MVLV_TSF_chassis_heavy", "MVLV_TSF_chassis_maneuver"}

def addon(slot, T):
    return {
        "MVLV_TSF_head_slot": "MVLV_TSF_add_sensor_%d" % T,
        "MVLV_TSF_shoulder_slot": "MVLV_TSF_add_thruster_%d" % T,
        "MVLV_TSF_leftBackArm_slot": "MVLV_TSF_add_assault_cannon_%d" % T,
        "MVLV_TSF_rigtBackArm_slot": "MVLV_TSF_add_assault_cannon_%d" % T,
        "MVLV_TSF_arm_slot": "MVLV_TSF_add_armor",
        "MVLV_TSF_waist_slot": "MVLV_TSF_add_thruster_%d" % T,
        "MVLV_TSF_leg_slot": "MVLV_TSF_add_armor",
    }.get(slot)

ORDER = ["MVLV_TSF_head_slot","MVLV_TSF_shoulder_slot","MVLV_TSF_leftBackArm_slot",
         "MVLV_TSF_rigtBackArm_slot","MVLV_TSF_arm_slot","MVLV_TSF_waist_slot","MVLV_TSF_leg_slot"]

def bend(s, ob):
    d = 1; i = ob + 1
    while i < len(s) and d > 0:
        if s[i] == "{": d += 1
        elif s[i] == "}": d -= 1
        i += 1
    return i - 1

total = 0
for fn in FILES:
    p = os.path.join(EQ, fn)
    s = open(p, encoding="utf-8").read()
    edits = []  # (abs_insert_pos, text)
    count = 0
    for m in re.finditer(r"(?m)^\t([A-Za-z]\w+)\s*=\s*\{", s):
        vstart = m.end() - 1
        vend = bend(s, vstart)
        body = s[m.end():vend]
        arch = re.search(r"archetype\s*=\s*(\w+)", body)
        par = re.search(r"parent\s*=\s*MVLV_TSF_chassis_(\d)", body)
        if not arch or arch.group(1) not in NORMAL_ARCH or not par:
            continue
        T = min(int(par.group(1)), 3)
        msm = re.search(r"module_slots\s*=\s*\{", body)
        dmm = re.search(r"default_modules\s*=\s*\{", body)
        if not msm or not dmm:
            continue
        ms_text = body[msm.end():bend(body, msm.end() - 1)]
        dm_inner = dmm.end()
        dm_text = body[dm_inner:bend(body, dmm.end() - 1)]
        have = set(re.findall(r"(MVLV_TSF_\w+slot\w*)\s*=", ms_text))
        filled = set(re.findall(r"(MVLV_TSF_\w+slot\w*)\s*=", dm_text))
        im = re.search(r"\n(\t+)MVLV_TSF_\w+slot", dm_text)
        ind = im.group(1) if im else "\t\t\t"
        adds = [ind + sl + " = " + addon(sl, T) for sl in ORDER if sl in have and sl not in filled]
        if not adds:
            continue
        text = "\n" + "\n".join(adds)
        abs_pos = m.end() + dm_inner  # right after default_modules '{'
        edits.append((abs_pos, text))
        count += 1
    # apply edits from end to start
    for pos, text in sorted(edits, key=lambda x: -x[0]):
        s = s[:pos] + text + s[pos:]
    open(p, "w", encoding="utf-8", newline="").write(s)
    print(fn, "filled:", count, "braces_ok:", s.count("{") == s.count("}"))
    total += count
print("TOTAL:", total)
