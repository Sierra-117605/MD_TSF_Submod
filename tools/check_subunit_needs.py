# -*- coding: utf-8 -*-
"""sub_unit の need = { ... } が要求している装備が「生産できる原型」かを検査する。

HOI4 の sub_unit は `need` に **原型（is_archetype = yes）** を書く。
派生型（`archetype = ...` を持つ側）を書くと、その派生型が `active = no` の場合
装備枠が永久に埋まらず、師団の戦力と指揮統制率が上がらないまま固まる。
error.log には何も出ないので気づきにくい。

  python tools/check_subunit_needs.py
"""
import glob
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = r"C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\2777392649"
VANILLA = r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV"


def load_equipment(roots):
    """{装備名: {"archetype": bool, "active": bool|None, "src": ファイル}}"""
    eq = {}
    for root in roots:
        for p in glob.glob(os.path.join(root, "common", "units", "equipment", "*.txt")):
            text = io.open(p, encoding="utf-8-sig", errors="replace").read()
            # 深さ1のブロック（装備定義）を切り出す
            for m in re.finditer(r'^\t([A-Za-z0-9_]+)\s*=\s*\{', text, re.M):
                name, start = m.group(1), m.end()
                depth, i = 1, start
                while i < len(text) and depth:
                    if text[i] == "{":
                        depth += 1
                    elif text[i] == "}":
                        depth -= 1
                    i += 1
                body = text[start:i]
                active = None
                a = re.search(r'^\s*active\s*=\s*(yes|no)', body, re.M)
                if a:
                    active = (a.group(1) == "yes")
                eq[name] = {
                    "archetype": bool(re.search(r'^\s*is_archetype\s*=\s*yes', body, re.M)),
                    "active": active,
                    "src": os.path.basename(p),
                }
    return eq


def main():
    eq = load_equipment([HERE, MD, VANILLA])
    print("装備定義を %d 件読み込み\n" % len(eq))

    problems = 0
    for p in sorted(glob.glob(os.path.join(HERE, "common", "units", "*.txt"))):
        text = io.open(p, encoding="utf-8-sig", errors="replace").read()
        unit = None
        in_need = False
        for ln, line in enumerate(text.split("\n"), 1):
            m = re.match(r'^\t([A-Za-z0-9_]+)\s*=\s*\{', line)
            if m:
                unit = m.group(1)
            if re.search(r'\bneed\s*=\s*\{', line):
                in_need = True
                if "}" in line.split("need", 1)[1]:
                    in_need = False
                continue
            if in_need:
                if "}" in line:
                    in_need = False
                for name in re.findall(r'([A-Za-z0-9_]+)\s*=\s*\d', line):
                    info = eq.get(name)
                    if info is None:
                        print("?? %-34s %-30s %s:%d  装備定義が見つからない"
                              % (name, unit or "-", os.path.basename(p), ln))
                        problems += 1
                    elif not info["archetype"]:
                        print("★ %-34s %-30s %s:%d  原型でない（active=%s, %s）"
                              % (name, unit or "-", os.path.basename(p), ln,
                                 info["active"], info["src"]))
                        problems += 1

    print()
    print("問題なし" if problems == 0 else "★ %d 件" % problems)
    return 0


if __name__ == "__main__":
    sys.exit(main())
