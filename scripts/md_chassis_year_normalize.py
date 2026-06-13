# -*- coding: utf-8 -*-
"""
chassis equipment の year= を chassis 名のジェネレーション基準で正規化

旧スクリプトは元の year (Muv-Luv canon) を機械的にマップしていたが、
chassis 名 (_1_light, _2_heavy, _3_maneuver, _4) のジェネレーションと
時系列がずれる問題があったので、名前ベースで揃える。

ジェネレーション -> 年:
  _0           : 1990
  _1_X         : 1990 (Gen 1: 既に配備済み)
  _2_X         : 1996 (Gen 2: MD 開始直前)
  _3_X         : 2011 (Gen 3: MD 中盤)
  _4           : 2020 (Gen 4: 後期)

軽い 派生: 同じ世代の年は同じ
support / specialForces 系統も同じ規則
"""
import re
import os

MOD = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod"
FILES = [
    os.path.join(MOD, "common", "units", "equipment", "MVLV_TSF_chassis.txt"),
    os.path.join(MOD, "common", "units", "equipment", "MVLV_TSF_support_chassis.txt"),
    os.path.join(MOD, "common", "units", "equipment", "MVLV_TSF_specialForces_chassis.txt"),
]

GEN_YEAR = {
    "0":         1990,
    "1_light":   1990,
    "1_light_mod": 1990,
    "1_heavy":   1990,
    "2_light":   1996,
    "2_heavy":   1996,
    "2_maneuver":1998,
    "3_light":   2011,
    "3_heavy":   2011,
    "3_maneuver":2013,
    "4":         2020,
}


def gen_suffix_from_name(name):
    """MVLV_TSF_(support_/specialForces_)?chassis_<suffix> -> suffix"""
    m = re.match(r'MVLV_TSF_(?:support_|specialForces_)?chassis_(.+)', name)
    if m:
        return m.group(1)
    return None


for path in FILES:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        c = f.read()

    updates = 0
    # 各 chassis ブロックを探す
    new_chunks = []
    last = 0
    for m in re.finditer(r'(\t)(MVLV_TSF_(?:support_|specialForces_)?chassis_\w+)\s*=\s*\{', c):
        cid = m.group(2)
        depth = 1
        i = m.end()
        while i < len(c) and depth > 0:
            if c[i] == "{":
                depth += 1
            elif c[i] == "}":
                depth -= 1
                if depth == 0:
                    break
            i += 1
        block_end = i

        new_chunks.append(c[last:m.start()])
        block = c[m.start():block_end + 1]

        suffix = gen_suffix_from_name(cid)
        if suffix and suffix in GEN_YEAR:
            new_year = GEN_YEAR[suffix]
            # year を置換
            def repl(mm):
                old = int(mm.group(1))
                return f"year = {new_year}" if old != new_year else mm.group(0)

            new_block, n = re.subn(r'\byear\s*=\s*(\d{4})\b', repl, block)
            if n > 0:
                updates += 1
            new_chunks.append(new_block)
        else:
            new_chunks.append(block)

        last = block_end + 1
    new_chunks.append(c[last:])
    c = "".join(new_chunks)

    with open(path, "w", encoding="utf-8") as f:
        f.write(c)
    print(f"  {os.path.basename(path)}: {updates} chassis 年代正規化")

print("\n=== ブレース整合性 ===")
for p in FILES:
    cc = open(p, encoding="utf-8", errors="replace").read()
    o, x = cc.count("{"), cc.count("}")
    print(f"  {os.path.basename(p):45s} {o}/{x}")
