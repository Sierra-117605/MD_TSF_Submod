# -*- coding: utf-8 -*-
"""
Susanoo / F-47 テックをバックアップから新ツリーへ統合

入力:
  _backup_pre_tech_import/tsf_susanoo_tech.txt
  _backup_pre_tech_import/tsf_attacker_susanoo_tech.txt  (一部のみ)
  _backup_pre_tech_import/tsf_F-47_tech.txt

出力:
  common/technologies/MVLV_susanoo.txt          (4 techs)
  common/technologies/MVLV_susanoo_modules.txt  (4 techs)
  common/technologies/MVLV_F-47.txt             (6 techs)
  interface/MVLV_susanoo_F47_icons.gfx          (14 sprite)

書き換え:
  folder:    tsf_folder            -> MVLV_tsf_folder
  category:  tsf_tech              -> MVLV_tsf_tech
  dep:       tsf_basic_framework   -> MVLV_research_basic_tsf_framework
  position:  x を +30 シフト（既存ツリー x=41 の右側へ）

除外 tech_id:
  tsf_attacker_conversion
  tsf_specialForces_conversion
"""
import re
import os

MOD = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod"
BAK = os.path.join(MOD, "_backup_pre_tech_import")
TECH_DIR = os.path.join(MOD, "common", "technologies")
GFX_PATH = os.path.join(MOD, "interface", "MVLV_susanoo_F47_icons.gfx")

X_SHIFT = 30  # 旧 x=20-28 -> 新 x=50-58

EXCLUDED = {"tsf_attacker_conversion", "tsf_specialForces_conversion"}

# 出力ファイルマッピング
OUT_MAP = {
    "tsf_susanoo_tech.txt":          os.path.join(TECH_DIR, "MVLV_susanoo.txt"),
    "tsf_attacker_susanoo_tech.txt": os.path.join(TECH_DIR, "MVLV_susanoo_modules.txt"),
    "tsf_F-47_tech.txt":             os.path.join(TECH_DIR, "MVLV_F-47.txt"),
}

# アイコン texture マッピング (tech_id -> texture path)
ICON_MAP = {
    # --- Susanoo backbone ---
    "tsf_susanoo_concept":   "gfx/interface/technologies/TSF/TSF_XG.dds",
    "tsf_susanoo_2":         "gfx/interface/technologies/TSF/TSF_XG-70b 01.dds",
    "tsf_susanoo_3":         "gfx/interface/technologies/TSF/TSF_70d.dds",
    "tsf_susanoo_4":         "gfx/interface/technologies/TSF/TSF_XG.dds",
    # --- Susanoo modules ---
    "tsf_susanoo_weapons":         "gfx/interface/technologies/TSF/TSF_XG.dds",
    "tsf_susanoo_gravity_cannon":  "gfx/interface/technologies/TSF/TSF_XG.dds",
    "tsf_susanoo_g_bomb":          "gfx/interface/technologies/TSF/TSF_XG.dds",
    "tsf_susanoo_systems":         "gfx/interface/technologies/TSF/TSF_XG.dds",
    # --- F-47 ---
    "tsf_F-47_framework":                  "gfx/interface/technologies/TSF/TSF_F-22.dds",
    "tsf_F-47_charged_particle_cannon":    "gfx/interface/technologies/TSF/TSF_F-22.dds",
    "tsf_F-47_lazaford_shield":            "gfx/interface/technologies/TSF/TSF_F-22.dds",
    "tsf_F-47_g_generator":                "gfx/interface/technologies/TSF/TSF_F-22.dds",
    "tsf_F-47_warp_drive":                 "gfx/interface/technologies/TSF/TSF_F-22.dds",
    "tsf_F-47_systems":                    "gfx/interface/technologies/TSF/TSF_F-22.dds",
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


def transform_block(block):
    """旧 tech ブロック内の参照名等を書き換え"""
    # folder name
    block = re.sub(r'name\s*=\s*tsf_folder\b', 'name = MVLV_tsf_folder', block)
    # categories
    block = re.sub(r'\btsf_tech\b', 'MVLV_tsf_tech', block)
    # dependencies / leads_to_tech 内の tsf_basic_framework
    block = re.sub(r'\btsf_basic_framework\b', 'MVLV_research_basic_tsf_framework', block)
    # position x シフト
    def shift_x(m):
        return f'x = {int(m.group(1)) + X_SHIFT}'
    block = re.sub(r'x\s*=\s*(-?\d+)', shift_x, block)
    return block


def extract_techs(src_text):
    """tech_id -> block の OrderedDict を返す"""
    result = []
    # technologies = { の中身
    m = re.search(r'technologies\s*=\s*\{', src_text)
    if not m:
        return result
    inner_start = m.end()
    inner_end = find_block_end(src_text, m.end() - 1)
    inner = src_text[inner_start:inner_end]

    pos = 0
    tech_pat = re.compile(r'(\t)([A-Za-z][\w\-]+)\s*=\s*\{', re.MULTILINE)
    while pos < len(inner):
        tm = tech_pat.search(inner, pos)
        if not tm:
            break
        tech_id = tm.group(2)
        brace_open = tm.end() - 1
        brace_close = find_block_end(inner, brace_open)
        if brace_close < 0:
            break
        # 行頭の \t も含める
        line_start = inner.rfind("\n", 0, tm.start()) + 1
        block_full = inner[line_start:brace_close + 1]
        result.append((tech_id, block_full))
        pos = brace_close + 1
    return result


def main():
    sprite_entries = []
    summary = []

    for src_name, dst_path in OUT_MAP.items():
        src_path = os.path.join(BAK, src_name)
        with open(src_path, "r", encoding="utf-8", errors="replace") as f:
            src = f.read()
        techs = extract_techs(src)
        kept = [(tid, block) for tid, block in techs if tid not in EXCLUDED]
        excluded = [tid for tid, _ in techs if tid in EXCLUDED]

        # 統合 tech block を作成
        out_lines = ["technologies = {\n"]
        for tid, block in kept:
            transformed = transform_block(block)
            out_lines.append(transformed)
            out_lines.append("\n")
        out_lines.append("}\n")
        out_content = "".join(out_lines)

        with open(dst_path, "w", encoding="utf-8") as f:
            f.write(out_content)

        summary.append((src_name, dst_path, len(kept), excluded))

        # sprite エイリアス
        for tid, _ in kept:
            if tid in ICON_MAP:
                sprite_entries.append((tid, ICON_MAP[tid]))

    # sprite ファイル書き出し
    lines = ["spriteTypes = {\n"]
    for tid, tex in sprite_entries:
        sprite_name = f"GFX_{tid}_medium"
        lines.append(f"\tSpriteType = {{\n")
        lines.append(f'\t\tname = "{sprite_name}"\n')
        lines.append(f'\t\ttexturefile = "{tex}"\n')
        lines.append(f"\t}}\n")
    lines.append("}\n")
    with open(GFX_PATH, "w", encoding="utf-8") as f:
        f.write("".join(lines))

    print("=== 統合完了 ===")
    for src, dst, n, exc in summary:
        print(f"  {src} -> {os.path.basename(dst)}: {n} techs (excluded: {exc})")
    print(f"  sprite alias: {len(sprite_entries)} -> {os.path.basename(GFX_PATH)}")


if __name__ == "__main__":
    main()
