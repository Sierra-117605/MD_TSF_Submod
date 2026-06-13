# -*- coding: utf-8 -*-
"""
Plan B 撤回：variant 単位の default_modules ブロックを削除
（archetype の default_modules は残す）
"""
import re
import os

MOD = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod"
EQ_DIR = os.path.join(MOD, "common", "units", "equipment")

FILES = ["MVLV_TSF_chassis.txt", "MVLV_TSF_support_chassis.txt", "MVLV_TSF_specialForces_chassis.txt"]


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


for fname in FILES:
    path = os.path.join(EQ_DIR, fname)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # equipments = { から開始
    eq_m = re.search(r"equipments\s*=\s*\{", content)
    if not eq_m:
        continue
    inner_start = eq_m.end()
    eq_end = find_block_end(content, eq_m.end() - 1)

    # 各 装備ブロック を走査
    pos = inner_start
    parts = [content[:inner_start]]
    removed = 0
    while pos < eq_end:
        m = re.search(r"^(\w+)\s*=\s*\{", content[pos:eq_end], re.MULTILINE)
        if not m:
            parts.append(content[pos:eq_end])
            pos = eq_end
            break
        block_start = pos + m.start()
        brace_pos = pos + m.end() - 1
        block_end = find_block_end(content, brace_pos)
        body = content[brace_pos + 1:block_end]
        # is_archetype yes は残す
        if re.search(r"is_archetype\s*=\s*yes", body):
            parts.append(content[pos:block_end + 1])
        else:
            # variant: default_modules を削除
            new_body, n = re.subn(r"\n[\t ]*default_modules\s*=\s*\{[^{}]*\}", "", body)
            if n > 0:
                removed += n
            parts.append(content[pos:brace_pos + 1])
            parts.append(new_body)
            parts.append(content[block_end:block_end + 1])
        pos = block_end + 1
    parts.append(content[eq_end:])

    with open(path, "w", encoding="utf-8") as f:
        f.write("".join(parts))
    print(fname, ": removed", removed)
print("Plan B 撤回完了")
