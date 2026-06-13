# -*- coding: utf-8 -*-
"""
全 battalion の need { } ブロックに cnc_equipment_1 = 10 を追加
"""
import re
import os

UNITS = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod\common\units"

FILES = [
    "MVLV_asa_battalion.txt",
    "MVLV_tsa_battalion.txt",
    "MVLV_tsf_battalion.txt",
    "MVLV_tsf_specialForces_battalion.txt",
    "MVLV_tsf_support_battalion.txt",
    "MVLV_xg_battalion.txt",
]


def add_cnc(content):
    """
    need = {
        XX = N
    }
    の閉じ } の直前に cnc_equipment_1 = 10 を追加
    既に cnc_equipment_1 が含まれていればスキップ
    """
    def replacer(m):
        need_body = m.group(1)
        if "cnc_equipment" in need_body:
            return m.group(0)
        # 末尾の改行/インデント保持
        # オリジナルが \n\t\t} 形式
        new_body = need_body.rstrip() + "\n\t\t\tcnc_equipment_1 = 10\n\t\t"
        return "need = {" + new_body + "}"

    # need = { ... } を非貪欲で見つける
    pattern = re.compile(r"need\s*=\s*\{([^{}]*)\}", re.DOTALL)
    return pattern.sub(replacer, content)


for fname in FILES:
    path = os.path.join(UNITS, fname)
    if not os.path.exists(path):
        print(fname, ": ファイル無し")
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    new_content = add_cnc(content)
    if new_content != content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        # 追加数カウント
        added = new_content.count("cnc_equipment_1 = 10") - content.count("cnc_equipment_1 = 10")
        print(fname, ": 追加 ", added)
    else:
        print(fname, ": 変更なし（既に追加済み）")
print("完了")
