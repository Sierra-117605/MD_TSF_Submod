# -*- coding: utf-8 -*-
# 支援突撃砲(support_assault_cannon)を削除し、使用箇所を通常突撃砲に置換、前提条件も整理
import re, os

MOD = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod"
EQ = os.path.join(MOD, "common", "units", "equipment")
TECH = os.path.join(MOD, "common", "technologies", "MVLV_NSB_TSF.txt")
GUN = os.path.join(EQ, "modules", "MVLV_TSF_gun_weapon_modules.txt")

def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="").write(s)
def bal(s): return s.count("{") == s.count("}")

def find_block_end(s, ob):
    d = 1; i = ob + 1
    while i < len(s) and d > 0:
        c = s[i]
        if c == "{": d += 1
        elif c == "}":
            d -= 1
            if d == 0: return i
        i += 1
    return -1

def remove_block(s, name):
    m = re.search(r'(?m)^([ \t]*)' + re.escape(name) + r'\s*=\s*\{', s)
    if not m: return s, False
    line_start = m.start(1)
    brace = s.index("{", m.end() - 1)
    end = find_block_end(s, brace)
    after = end + 1
    if after < len(s) and s[after] == "\n": after += 1
    return s[:line_start] + s[after:], True

# 1) 使用箇所を通常突撃砲へ置換（3ファイル）
for fn in ["MVLV_TSF_support_chassis.txt", "MVLV_TSF_zz_common_variants.txt", "MVLV_TSF_zz_country_variants.txt"]:
    p = os.path.join(EQ, fn); s = rd(p)
    n = s.count("MVLV_TSF_support_assault_cannon_")
    s = s.replace("MVLV_TSF_support_assault_cannon_", "MVLV_TSF_assault_cannon_")
    assert bal(s), fn
    wr(p, s); print("replace", fn, n, "->", s.count("MVLV_TSF_support_assault_cannon_"))

# 2) モジュール定義3つ削除
s = rd(GUN)
for n in (1, 2, 3):
    s, ok = remove_block(s, "MVLV_TSF_support_assault_cannon_%d" % n)
    print("module remove _%d:" % n, ok)
assert bal(s), "GUN"
wr(GUN, s)

# 3) テックファイル整理
s = rd(TECH)
# 3a) 研究ノード3つ削除（enable内のモジュール名も一緒に消える）
for n in (1, 2, 3):
    s, ok = remove_block(s, "MVLV_research_support_assault_cannon_%d" % n)
    print("research node remove _%d:" % n, ok)
# 3b) enable_equipment_modules 内のモジュール名行を削除（基礎研究＋他テック）
s = re.sub(r'(?m)^[ \t]*MVLV_TSF_support_assault_cannon_[123][ \t]*\r?\n', '', s)
# 3c) コメントの leads_to_tech 行を削除
s = re.sub(r'(?m)^[ \t]*#\s*leads_to_tech\s*=\s*MVLV_research_support_assault_cannon_[123][ \t]*\r?\n', '', s)
# 3d) dependencies から support_assault_cannon の前提を除去
s = re.sub(r'\s*MVLV_research_support_assault_cannon_[123]\s*=\s*1', '', s)
assert bal(s), "TECH"
wr(TECH, s)
print("tech remaining 'support_assault_cannon':", s.count("support_assault_cannon"))
print("DONE")
