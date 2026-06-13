# -*- coding: utf-8 -*-
"""
Susanoo / F-47 テックを左にシフト & XG系を広くする

Susanoo 横間隔: 2 -> 3
全体 x: -6 シフト（右側に空白を作る）

旧 -> 新
  concept    x=50 -> 44
  70b        x=52 -> 44
  70c        x=54 -> 47
  70d        x=56 -> 50
  weapons    x=52 -> 44
  gravity    x=54 -> 47
  g_bomb     x=56 -> 50
  systems    x=58 -> 53

  F-47 framework  x=50 -> 44
  F-47 charged    x=52 -> 46
  F-47 lazaford   x=54 -> 48
  F-47 g_gen      x=56 -> 50
  F-47 warp       x=58 -> 52
  F-47 systems    x=52 -> 46
"""
import re, os

MOD = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod"
TECH_DIR = os.path.join(MOD, "common", "technologies")

# tech_id -> new x
NEW_X = {
    "tsf_susanoo_concept":          44,
    "tsf_susanoo_2":                44,
    "tsf_susanoo_3":                47,
    "tsf_susanoo_4":                50,
    "tsf_susanoo_weapons":          44,
    "tsf_susanoo_gravity_cannon":   47,
    "tsf_susanoo_g_bomb":           50,
    "tsf_susanoo_systems":          53,
    "tsf_F-47_framework":           44,
    "tsf_F-47_charged_particle_cannon": 46,
    "tsf_F-47_lazaford_shield":     48,
    "tsf_F-47_g_generator":         50,
    "tsf_F-47_warp_drive":          52,
    "tsf_F-47_systems":             46,
}


def find_block_end(s, open_pos):
    depth = 1
    i = open_pos + 1
    while i < len(s) and depth > 0:
        c = s[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


for fname in ["MVLV_susanoo.txt", "MVLV_susanoo_modules.txt", "MVLV_F-47.txt"]:
    path = os.path.join(TECH_DIR, fname)
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        c = f.read()

    # 各 tech_id について、ブロック内の position { x = N ... } を置換
    for tid, new_x in NEW_X.items():
        # tech_id = { ... } を探す
        m = re.search(r'(\t)' + re.escape(tid) + r'\s*=\s*\{', c)
        if not m:
            continue
        bstart = m.end() - 1
        bend = find_block_end(c, bstart)
        body = c[bstart+1:bend]
        # body 内の最初の position { x = N ... } を置換
        new_body = re.sub(r'(position\s*=\s*\{\s*x\s*=\s*)-?\d+', rf'\g<1>{new_x}', body, count=1)
        c = c[:bstart+1] + new_body + c[bend:]
        print(f"  {tid:40s} x -> {new_x}")

    with open(path, "w", encoding="utf-8") as f:
        f.write(c)
    print(f"  -- saved: {fname}")
