# -*- coding: utf-8 -*-
# 師団テンプレを 軽/重/高機動/混成/支援 に置き換える（B方式）
p = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod\common\on_actions\MVLV_tsf_variant_assign.txt"
s = open(p, encoding="utf-8").read()

flag = s.index("set_country_flag = tsf_div_templates")
start = s.index("division_template = {", flag)
sf = s.index('name = "特務戦術機師団"')  # 特務戦術機師団
end = s.rindex("division_template = {", start, sf)
indent = s[:start].split("\n")[-1]
i1, i2, i3 = indent, indent + "\t", indent + "\t\t"

def tmpl(name, regs):
    out = [i1 + "division_template = {", i2 + 'name = "%s"' % name, i2 + "regiments = {"]
    for bn, x, y in regs:
        out.append(i3 + "%s = { x = %d y = %d }" % (bn, x, y))
    out.append(i2 + "}")
    out.append(i1 + "}")
    return "\n".join(out)

L = "MVLV_tsf_light_battalion"
H = "MVLV_tsf_battalion"          # 重（既存IDを流用）
M = "MVLV_tsf_maneuver_battalion"
S = "MVLV_tsf_support_battalion"

def col(bn, x, n, y0=0):
    return [(bn, x, y0 + k) for k in range(n)]

light = col(L, 0, 5) + col(L, 1, 5)
heavy = col(H, 0, 5) + col(H, 1, 5)
man   = col(M, 0, 5) + col(M, 1, 5)
mixed = col(L, 0, 4) + [(H, 0, 4)] + col(H, 1, 2) + [(M, 1, 2), (M, 1, 3), (M, 1, 4)]
support = col(S, 0, 5) + col(S, 1, 3) + [(L, 1, 3), (H, 1, 4)]

blocks = [
    tmpl("軽戦術機師団", light),       # 軽戦術機師団
    tmpl("重戦術機師団", heavy),       # 重戦術機師団
    tmpl("高機動戦術機師団", man),  # 高機動戦術機師団
    tmpl("混成戦術機師団", mixed),  # 混成戦術機師団
    tmpl("戦術機支援師団", support),# 戦術機支援師団
]

new = s[:start] + "\n".join(blocks) + "\n" + indent + s[end:]

if new.count("{") != new.count("}"):
    print("ERROR brace mismatch", new.count("{"), new.count("}"))
else:
    open(p, "w", encoding="utf-8", newline="").write(new)
    print("OK templates=", new.count("division_template = {"), "braces", new.count("{"), new.count("}"))
