# -*- coding: utf-8 -*-
"""
techtree_MVLV_*_folder_item / techtree_UNI_*_folder_item ブロックを
countrytechtreeview の外（top-level guiTypes 子）に移動
v2: ブレース追跡を正しく
"""
import re

OUR = r"C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod\interface\countrytechtreeview.gui"

with open(OUR, "r", encoding="utf-8", errors="replace") as f:
    content = f.read()


def find_block_end_from_pos(content, start_pos):
    """start_pos には開いた状態（depth=1）として、対応する } を探す"""
    depth = 1
    i = start_pos
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


# countrytechtreeview の範囲（regex には開き { を含む）
m_ctt = re.search(r'containerWindowType\s*=\s*\{\s*name\s*=\s*"countrytechtreeview"', content)
if not m_ctt:
    print("ERROR no countrytechtreeview")
    exit(1)
# regex 末尾 = 既に depth=1 の状態
ctt_close = find_block_end_from_pos(content, m_ctt.end())
print("countrytechtreeview close at:", ctt_close)
ctt_start = m_ctt.start()

# 中の item ブロックを抽出（直接位置で探す）
# 各 item は containerWindowType = { \n name = "techtree_*_folder_item"
items_to_extract = []
# 内部のみ走査
inner = content[m_ctt.end():ctt_close]
inner_offset = m_ctt.end()

for m_name in re.finditer(r'name\s*=\s*"(techtree_(?:MVLV|UNI)_[a-zA-Z_]+_folder_item)"', inner):
    name = m_name.group(1)
    # この name の前にある containerWindowType = { を探す
    # 名前は通常 containerWindowType ブロックの最初の name フィールド
    # 名前位置から遡って containerWindowType = { を探す
    abs_name_pos = inner_offset + m_name.start()
    # 名前位置から少し前を見て containerWindowType = { を探す
    look_back_region = content[max(0, abs_name_pos - 100):abs_name_pos]
    cwt_match = list(re.finditer(r'containerWindowType\s*=\s*\{', look_back_region))
    if not cwt_match:
        continue
    last_cwt = cwt_match[-1]
    block_start = max(0, abs_name_pos - 100) + last_cwt.start()
    # depth=1 の状態で開き { 直後から close を探す
    open_after = max(0, abs_name_pos - 100) + last_cwt.end()
    block_close = find_block_end_from_pos(content, open_after)
    if block_close < 0:
        continue
    items_to_extract.append((block_start, block_close + 1, name))

print("抽出予定:", len(items_to_extract), "件")
for s, e, n in items_to_extract:
    print(f"  {n} at {s}-{e}")

# 後ろから削除（インデックスズレ防止）
items_to_extract_sorted = sorted(items_to_extract, key=lambda x: x[0], reverse=True)
extracted_blocks = []
new_content = content
for start, end, name in items_to_extract_sorted:
    extracted_blocks.append(new_content[start:end])
    new_content = new_content[:start] + new_content[end:]

# countrytechtreeview の close を再特定
m_ctt2 = re.search(r'containerWindowType\s*=\s*\{\s*name\s*=\s*"countrytechtreeview"', new_content)
ctt_close2 = find_block_end_from_pos(new_content, m_ctt2.end())
print("再計算 countrytechtreeview close:", ctt_close2)

# top-level 挿入（countrytechtreeview の close } の直後）
insertion = "\n\n# === MVLV mod small items (moved to top-level) ===\n" + "\n\n".join(reversed(extracted_blocks)) + "\n"
new_content = new_content[:ctt_close2 + 1] + insertion + new_content[ctt_close2 + 1:]

# ブレースバランス確認
opens = new_content.count("{")
closes = new_content.count("}")
print("balance: {", opens, "} ", closes, "diff:", opens - closes)

with open(OUR, "w", encoding="utf-8") as f:
    f.write(new_content)
print("done. new size:", len(new_content))
