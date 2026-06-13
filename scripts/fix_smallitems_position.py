# -*- coding: utf-8 -*-
"""
techtree_MVLV_*_folder_item / techtree_UNI_*_folder_item ブロックを countrytechtreeview の外に移動
"""
import re

OUR = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod\interface\countrytechtreeview.gui"

with open(OUR, "r", encoding="utf-8", errors="replace") as f:
    content = f.read()


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


# countrytechtreeview ブロックを特定
m_ctt = re.search(r'containerWindowType\s*=\s*\{\s*name\s*=\s*"countrytechtreeview"', content)
if not m_ctt:
    print("ERROR")
    exit(1)
ctt_brace = content.find("{", m_ctt.end() - 1)
ctt_close = find_block_end(content, ctt_brace)
print("countrytechtreeview at", m_ctt.start(), "open", ctt_brace, "close", ctt_close)

# countrytechtreeview の中にある小窓 item ブロックを全部抽出して削除
items_pattern = re.compile(
    r'\n[\t ]*containerWindowType\s*=\s*\{[\s\n]*name\s*=\s*"techtree_(MVLV|UNI)_[^"]+_folder_item"',
    re.MULTILINE
)

extracted = []  # 抽出した block
modifications = []  # (start, end) の削除範囲

# countrytechtreeview 内のみ走査
ctt_region = content[m_ctt.start():ctt_close + 1]
ctt_offset = m_ctt.start()

for m_item in items_pattern.finditer(ctt_region):
    block_start = ctt_offset + m_item.start()
    item_brace = content.find("{", block_start + 20)  # containerWindowType = { の {
    # 確実にこの match の対応する { を取る
    # ですが、match に "containerWindowType = {" が含まれるので、その { は match.start() ~ match.end() の中にある
    # 改めて: match の中で最初の { を探す
    rel_brace = m_item.group(0).find("{")
    if rel_brace < 0:
        continue
    abs_brace = block_start + rel_brace
    block_end = find_block_end(content, abs_brace)
    if block_end < 0:
        continue
    block_text = content[block_start:block_end + 1]
    extracted.append(block_text)
    modifications.append((block_start, block_end + 1))

print("抽出した item ブロック数:", len(extracted))

# 後ろから削除
modifications.sort(key=lambda x: x[0], reverse=True)
new_content = content
for start, end in modifications:
    new_content = new_content[:start] + new_content[end:]

# 抽出したブロックを countrytechtreeview の外（} の後）に追加
# countrytechtreeview の close brace を再計算（削除後の位置）
m_ctt2 = re.search(r'containerWindowType\s*=\s*\{\s*name\s*=\s*"countrytechtreeview"', new_content)
ctt_brace2 = new_content.find("{", m_ctt2.end() - 1)
ctt_close2 = find_block_end(new_content, ctt_brace2)

insertion = "\n\n# === MVLV mod small items (top-level) ===\n" + "\n\n".join(extracted) + "\n"
new_content = new_content[:ctt_close2 + 1] + insertion + new_content[ctt_close2 + 1:]

with open(OUR, "w", encoding="utf-8") as f:
    f.write(new_content)

# ブレースバランス確認
opens = new_content.count("{")
closes = new_content.count("}")
print("ブレース: {:", opens, "}:", closes, "diff:", opens - closes)
print("新サイズ:", len(new_content))
