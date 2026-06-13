# -*- coding: utf-8 -*-
"""
countrytechtreeview.gui から古い tsf_folder のウィンドウ・タブ定義を削除
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


# tsf_folder の containerWindowType を削除（先頭から走査）
removed_count = 0
result_parts = []
i = 0
while i < len(content):
    # 次の containerWindowType を探す
    m = re.search(r'containerWindowType\s*=\s*\{', content[i:])
    if not m:
        result_parts.append(content[i:])
        break
    block_start = i + m.start()
    brace_pos = i + m.end() - 1
    # この block 内の name を確認
    end_pos = find_block_end(content, brace_pos)
    if end_pos < 0:
        result_parts.append(content[i:])
        break
    block_body = content[brace_pos + 1:end_pos]
    # 最初の name 文字列を取得
    name_match = re.search(r'name\s*=\s*"([^"]+)"', block_body)
    if name_match:
        name = name_match.group(1)
        # tsf_folder, tsf_folder_tab, highlight_tsf_folder を削除対象に
        if name in ("tsf_folder", "tsf_folder_tab", "highlight_tsf_folder"):
            # block 全体を削除（直前の空白/改行も含める）
            pre = content[i:block_start]
            pre = re.sub(r"\n[ \t]*$", "\n", pre)
            result_parts.append(pre)
            i = end_pos + 1
            removed_count += 1
            continue
    # 削除しない場合、この block 開始位置までを result に追加
    result_parts.append(content[i:brace_pos + 1])
    # block 内部に入って走査続行（ネスト走査）
    i = brace_pos + 1

new_content = "".join(result_parts)
with open(OUR, "w", encoding="utf-8") as f:
    f.write(new_content)

print("削除した tsf_folder 系ブロック:", removed_count)
print("新サイズ:", len(new_content), "bytes")
