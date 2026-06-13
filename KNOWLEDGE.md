# KNOWLEDGE.md — MD_TSF_Submod ハマりポイント・学び集

## 🔴 技術カテゴリは focus / continuous_focus の modifier では無効（idea 経由が必須）

### 症状
- `continuous_focus` の focus に `modifier = { MVLV_tsf_tech = 0.10 }` と書くと
  error.log に `Unknown modifier: MVLV_tsf_tech`
- そのパースエラーで**その focus 以降の戦術機フォーカス群が表示されない**

### 原因
- 技術カテゴリ（`MVLV_tsf_tech` 等）の研究速度ボーナスは「country modifier」ではない
- focus / continuous_focus の `modifier` ブロックは country modifier のみ受け付ける

### 修正
- `research_bonus` を持つ hidden idea を作り、focus で `idea = X` で付与
```
# common/ideas/
hidden_ideas = { MVLV_tsf_research_idea = { research_bonus = { MVLV_tsf_tech = 0.10 } } }
# common/continuous_focus/
focus = { id = ... idea = MVLV_tsf_research_idea ... }
```

### 使い分け
- **カテゴリ別研究速度** → idea の `research_bonus`
- **軍事ボーナス**（`army_armor_attack_factor`, `experience_gain_army_factor` 等）→ focus の `modifier` に直書きでOK

### 継続フォーカスの共存（1国1パレット）
- `continuous_focus_palette` は1国1つ・マージ不可。MD の `id=focus`（全国default）を submod で**コピー保持**し末尾に追加する（MD本体ツリーは無改変）

---


## 🔴 1 つの .gfx ファイル内の sprite 数過多で他 UI 巻き込みクラッシュ

### 症状
- 開発者コンソール（`キー）の **テキスト入力欄が描画されない**
- 入力欄の `|` カーソルは見えるが、背景・枠は出ない
- 我々の MOD 無効化で正常に戻る
- error.log には目立った警告なし

### 原因
- 我々の `MVLV_TSF_technology_icons.gfx` に **96 個の `GFX_MVLV_research_*_medium` sprite を追加した結果、ファイル内 sprite 数が 309 個**
- 元 MOD 由来の既存 `GFX_tsf_*_medium` 系 213 個と併存して総数 309
- 1 つの .gfx ファイル内 sprite 数が**約 300 個を超える**と HOI4 の GUI ロードが部分的に失敗し、**同じ起動セッションの他 GUI（コンソール等）の描画も巻き込まれる**

### 修正（最終版）
- ⚠️ **`picture = ...` はテックでは無効フィールド**（バニラ tech ファイル全てで未使用、grep で 0 件確認）
- 正しい解：**別 gfx ファイル** (`MVLV_research_tech_icons.gfx`) に `GFX_<tech_id>_medium` 自動命名 sprite を作成
- texturefile は既存 sprite と同じ dds を指せばよい（エイリアス）
- これで各 gfx ファイル 300 未満を維持しつつテックアイコンが解決される

### ⚠️ 過去のミスリード
- 一時期「テック側 `picture = GFX_X_medium` で参照する」と書いていたが**間違い**
- 実際は picture フィールドが無視され、すべてフォールバック (`GFX_technology_medium` = 空シルエット) になっていた
- 切り分け：完全再起動しても全テックが同じ silhouette → 自動命名 lookup が失敗している証拠

### 🔴 さらに有害：picture = ... は「Unknown modifier」を吐く + 同テック内の後続フィールドを破壊
- HOI4 はテックで `picture = ...` を見ると error.log に「Unknown modifier: picture」を出す
- それだけでなく、**そのテック内の後続フィールド処理が中断**される模様
- 症状：`enable_subunits` が無視され、本来解放されるはずの battalion が division designer に出現しない
- 影響範囲：picture = 行を含む 98 テック全て
- 教訓：**HOI4 で未対応 field を一括追加してはいけない**。エラー 1 件 = 単独の警告と思いきや、cascading な動作不良を引き起こす。
- 修正：全 picture = 行を削除（`scripts/remove_picture_refs.py`）

### 教訓
- 1 つの .gfx ファイルに大量の sprite を詰め込むと**思わぬ副作用**（他 UI が描画されない等）
- 既存 sprite があれば `picture = ...` で明示参照する方が安全
- 「異なるネーミング規則の重複 sprite」は HOI4 内部で衝突しなくても**ロード負荷**になる
- 切り分け手順：`interface/` フォルダごと退避 → 半分復元 → 1 ファイルずつ復元、で犯人を特定可能

### 再発（2026-05-30）と二次原因
- 2026-05-30、テック側に `picture = GFX_tsf_*_medium` を 98 個追加したが**テックツリーのアイコンが全部空シルエット**
- 原因：もう 1 つの `MVLV_TSF_old_technology_icons.gfx`（旧版・equipment 等で参照されている）が **301 sprite** で上限超え
- → 同じ interface フォルダ内の他 gfx (`MVLV_TSF_technology_icons.gfx`) の sprite ロードも巻き込まれた
- **修正**：旧 gfx を `_a` (153) と `_b` (153) に分割、元ファイルは `.bak_split` にリネームして無効化
- 教訓：sprite 上限は**プロジェクト内の同フォルダ全体のロードバジェット**に影響する。1 ファイルが超えると周辺もダメ。新規追加時は**そのフォルダ内に既存の 300 超ファイルがないか**もチェックする。

---

## 🔴 新しいルートテックは gridboxtype を手動追加しないとツリーに表示されない

### 症状
- 新しい tech (dependencies なし) を folder に追加
- ゲーム上は技術として登録されている（コマンド `research_on_unlock` で解放可能）
- しかしテックツリー画面では**描画されない**（存在自体が見えない）

### 原因
HOI4 の `countrytechtreeview.gui` 内の folder containerWindowType は、各**ルートテック**につき個別の `gridboxtype = { name = "<tech_id>_tree" ... }` を要求する。  
子テック（dependencies 付き）は親に自動で連結されるが、ルートは描画指示が必要。

### 修正
folder の他の gridbox 群の末尾に追加：
```
gridboxtype = {
    name = "<root_tech_id>_tree"
    position = { x = 10% y = 172 }
    size = { width = 90% height = 90% }
    slotsize = { width = 70 height = 70 }
    format = "UP"
}
```

### 教訓
- 新規ルートテック追加時は必ず gui の gridbox も追加する
- 「技術は読み込まれているのにツリーに出ない」→ gridbox 漏れを真っ先に疑う

---

## 🔴 装備モジュールカテゴリの localization

### 症状
- 装備デザイナーでモジュール選択時、カテゴリ名が **`EQ_MOD_CAT_<category>_TITLE`** のように生の key で表示される

### 原因
モジュール定義の `category = X` で使った X に対する localization key (`EQ_MOD_CAT_X_TITLE` / `_DESC`) が未定義。

### 修正
loc yml に追加：
```
EQ_MOD_CAT_F47_g_generator_type_TITLE: "G 発生機"
EQ_MOD_CAT_F47_g_generator_type_DESC: "F-47 専用の長期運用 G 発生器。"
```

---

## 🔴 countrytechtreeview.gui のテンプレ depth 要件

### 症状
- テックツリーを開くと、画面左上にタブ風スタイル（斜め縞）+ 緑の「+」マークの**謎の四角**が表示される
- クリックしても何も起きない
- カスタム folder を持つ MOD でよく発生

### 原因
HOI4 の `countrytechtreeview.gui` では、テックボックス用テンプレ（`techtree_*_folder_item`, `techtree_*_folder_small_item`）が **`guiTypes` 直下（depth 2）にある場合のみテンプレとして扱われ、テックツリーで動的にインスタンス化される**。

それより深い場所（例：`countrytechtreeview` の中、depth 3 以上）にあると、HOI4 は**スタンドアロンのウィンドウ**として position (0, 0) で描画してしまう。

そのテンプレが持つ:
- `background = "GFX_technology_unavailable_item_bg"` → タブ風斜め縞
- `iconType { name = "Icon" spriteType = "GFX_technology_medium" }` → 緑の「+」（デフォルト未割当アイコン）

→ 結果として「左上に出現する謎の +付き四角」になる。

### 修正
テンプレを `guiTypes` 直下（depth 2）に移動：
```python
# countrytechtreeview ブロックを find_block_end_from_pos で特定
# 該当テンプレを抽出して countrytechtreeview の閉じ } の直後に挿入
```

### 教訓
- カスタム folder の small_item / item テンプレは必ず **depth 2（guiTypes 直下）** に置く
- マージ時は元 MOD のテンプレ depth を確認しておく
- ブレースバランスだけでなく、各要素の depth も検証する

---

## 🟡 PNG ファイルを .dds 拡張子で扱う HOI4 の挙動

### 症状
- 元 MOD と同じ dds ファイルを使っているのに、テックツリーで一部のモジュールアイコンが表示されない
- 表示成功するアイコンと失敗するアイコンに、ファイル形式（PNG vs 実 DDS）の明確な相関なし

### 原因
- 元 MOD の dds ファイルの多くは実は **PNG ファイルに .dds 拡張子をつけたもの**
- HOI4 はこの偽装 dds を**条件付きで読み込める**が、すべての PNG-as-DDS が動作するわけではない
- 元 MOD でも一部のアイコンは表示されていなかった可能性

### 暫定対策
- 表示成功している texture file を「カテゴリ別代表アイコン」として、空表示テックの sprite 定義を再ポイント
- ゲーム機能には影響なし、見た目はバラエティに欠けるが空白よりはマシ

### 完全解決策（未実装）
- 外部の DDS 変換ツール（DirectXTex 等）で本物の DDS に変換
- またはオリジナルの PNG 素材から再エクスポート

### 教訓
- HOI4 では拡張子 .dds でも PNG 形式の場合があるが、表示動作は保証されない
- アイコン作成時は実 DDS（DXT1/DXT5 圧縮）で保存することを推奨

---

## 🟡 scripted_gui の visible 条件で UI 非表示化

### 用途
- MD Beta 等が `scripted_gui` で定義する UI（research_slot ボタン等）を**完全非表示**にしたい場合

### 方法
1. 元の scripted_gui ファイルを `common/scripted_guis/` にコピー
2. 該当エントリに `visible = { always = no }` を追加

例：
```
open_research_window = {
    window_name = "open_research_slot_gui"
    context_type = player_context
    parent_window_token = technology_tab
    dirty = global.research_screen_ui

    visible = {
        always = no
    }
    ...
}
```

### 注意
- `interface/*.gui` の position 変更（画面外に移動）だけでは scripted_gui で再生成される場合あり
- 確実に非表示にするには scripted_gui 側で `visible` を制御する

---

## 🔴 `ai_strategy_plans/` フォルダのフォーマット要件（重要・難解バグ）

### 症状
- ゲーム開始後、**最初の自動セーブ（2000年2月1日）でクラッシュ**
- `error.log`: `Invalid subunit.: none, near line: 0 in file: save games/autosave_temp.hoi4`
- `exception.txt`: EXCEPTION_ACCESS_VIOLATION + PHYSFS_writeULE64 系のスタックトレース
- 「ロード時」と勘違いしやすいが実際は **autosave 書き出し時** のクラッシュ
- ゲーム内日付 `2000.02.01.02` 前後で必ず発生

### 原因
`common/ai_strategy_plans/` フォルダは **MD Beta 独自の拡張プラン形式** を要求する：
```
plan_name = {
    allowed = { ... }
    name = "..."          # 必須
    desc = "..."          # 必須
    enable = { ... }
    abort = { ... }
    ai_national_focuses = { ... }
    weight = {            # 必須（これがないと autosave 時に内部状態が壊れる）
        factor = 1.0
        modifier = { factor = 1.0 }
    }
}
```

ところが我々のファイルは **vanilla HOI4 の素朴な ai_strategy 形式** で書かれていた：
```
plan_name = {
    allowed = { original_tag = USA }
    enable = { date > 1999.1.1 }
    abort = { always = no }
    ai_strategy = { type = research_tech id = "..." value = 200 }
}
```

`weight` ブロック等が無いため、AI プランの登録時にデフォルト値で埋められず内部状態が破損 → autosave 時に subunit 参照解決が "none" にフォールバックして `Invalid subunit.: none` で死亡。

### 修正
**`ai_strategy/` フォルダに移動する**（vanilla 形式を受け付ける）：
- `common/ai_strategy_plans/tsf_country_priority_plans.txt` → `common/ai_strategy/tsf_country_priority.txt`
- `common/ai_strategy_plans/tsf_ai_strategy_plans.txt` → `common/ai_strategy/tsf_research_priority.txt`

### 教訓
- **`ai_strategy/` と `ai_strategy_plans/` は全く別物**
- `ai_strategy/` = vanilla 形式（`ai_strategy = { type = X id = Y value = Z }` を並べる）
- `ai_strategy_plans/` = MD Beta 拡張形式（`weight` / `name` / `desc` 等必須）
- 既存の `tsf_generic_strategy.txt` は `ai_strategy/` 配下なので問題なし → 同じパターンで配置すれば OK
- ファイル名に `_plans.txt` が付いていても、配置フォルダで判定される

### 検出方法
- error.log で `Invalid subunit.: none` + `autosave_temp.hoi4` のセットを探す
- これは subunit 定義の問題ではなく **AI プラン構造の破損** のサイン
- 切り分け: `common/ai_strategy_plans/` 内のファイルを全部 .bak にして起動できれば確定

---

## 🔴 HOI4 識別子（equipment / tech ID）にハイフン使用不可

### 症状
- 装備名やテック名に `F-22`, `MiG-21`, `Su-37` のようなハイフンを含む識別子を定義
- ゲーム挙動が不安定（パーサーがハイフンを「マイナス記号」と誤解する可能性）

### 教訓
- 内部 ID は **アルファベット・数字・アンダースコア（`_`）のみ**
- 表示名（abbreviation, 翻訳テキスト）は **文字列なのでハイフン OK**
- 修正例：
  - `equipment_id = USA_TSF_F-22` → `equipment_id = USA_TSF_F_22`
  - `abbreviation = "F-22"` はそのまま（OK）
  - 日本語訳 `"F-22 ラプター"` もそのまま（OK）

---

## 🟡 default_modules の slot category 不一致

### 症状
- chassis のスロットに category が合わないモジュールを default で割り当てる
- 装備としては作れるが、設計が無効状態になる
- autosave 時に "none" として serialize されて Invalid subunit エラー

### 具体例（実際にあったバグ）
- `MVLV_TSF_chassis_4` の `default_modules`:
  ```
  MVLV_TSF_armor_slot = MVLV_TSF_special_structure_4   ← WRONG
  ```
- `MVLV_TSF_armor_slot` の allowed_module_categories は `MVLV_TSF_armor_type`
- `MVLV_TSF_special_structure_4` の category は `MVLV_TSF_sp_structure_type`（armor_type ではない！）

### 修正
```
MVLV_TSF_armor_slot = MVLV_TSF_armor_composite           # 正しい armor 系
MVLV_TSF_sp_slot_1 = MVLV_TSF_special_structure_4        # sp_structure 系は sp_slot
```

### 教訓
- スロットには `allowed_module_categories` で許可されたカテゴリのモジュールしか入れられない
- モジュールの category を必ず確認してから default_modules に割り当てる
- 全 chassis variant に default_modules を付けるのは過剰。元 MOD は **archetype レベルにだけ** default_modules を置く設計（variants は inherit）

---

## 🟡 +JP 系翻訳 MOD との相性

- `+JP: Millennium Dawn: A Modern Day mod` (ugc_2778141436) は **MD Modern Day 用** であり **MD Beta 用ではない**
- MD Beta（最新版）と組み合わせると別の不整合の原因になり得る
- MD Beta を使う場合は +JP 系 MOD は無効化する

---

## 🟡 同名 localisation file による翻訳衝突

### 症状
- MD Beta の装備名が `infantry_weapon_1` のような生キーで表示される
- 翻訳が効かない

### 原因
- `localisation/japanese/equipment_l_japanese.yml` を作っていた
- MD Beta も同名のファイル `equipment_l_japanese.yml` を持っており、我々の方が優先されて MD Beta の翻訳がブロックされる

### 修正
- ファイル名をユニークに：`MVLV_TSF_equipment_l_japanese.yml` のように prefix を付ける

### 教訓
- localisation ファイル名は **他 MOD と衝突しないユニークな名前** にする
- `replace/` フォルダ配下のファイルは特に注意（バニラ翻訳を上書きするため意図しない衝突を起こしやすい）

---

## 🟡 localisation yml ファイルの BOM

### 症状
- 新規作成した `*_l_japanese.yml` ファイルが Claude プレビューや一部エディタで日本語識別できず化ける
- HOI4 自体は BOM なしでも読めるので動作には影響しないが、編集時に困る

### 原因
- `Write` ツールで作成した yml ファイルは **UTF-8 BOM なし**
- 既存の MD Beta / muvluvJP 由来の yml は全部 **UTF-8 with BOM**

### 修正
PowerShell で BOM を付与：
```powershell
$content = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)
$utf8WithBOM = New-Object System.Text.UTF8Encoding $true  # true = emit BOM
[System.IO.File]::WriteAllText($path, $content, $utf8WithBOM)
```

### 教訓
- yml を新規作成したら必ず BOM を付与する
- BOM 有無確認: 先頭3バイトが `0xEF 0xBB 0xBF` なら BOM あり

---

## 🟡 国別装備名（country-prefix localisation）

### 機構
HOI4 は装備名を解決する時、**`<TAG>_<derived_variant_name>` を最初に探し**、なければ `<derived_variant_name>` にフォールバックする。

### 例
- 装備 `MVLV_TSF_chassis_1_heavy` の `derived_variant_name = MVLV_TSF_equipment_1_heavy`
- 日本プレイ時: `JAP_MVLV_TSF_equipment_1_heavy` を探す → 「77式戦術歩行戦闘機 撃震」
- 中国プレイ時: `CHI_MVLV_TSF_equipment_1_heavy` を探す → 「殲撃八型 (J-8)」
- それ以外: フォールバックして「第一世代重戦術機」

### 注意
- support_chassis / specialForces_chassis も同じ `derived_variant_name` キーを共有するので、1 ファイルで 3 種類カバー可能
- ただし用途は分かれていても表示名は同じになる（支援機も "77式撃震" と表示されてしまう）→ 細分化したい場合は個別キーが必要

### MD Beta の使用例
```
JAP_mbt_equipment_0: "Type 74G"
JAP_mbt_equipment_1: "Type 90"
USA_mbt_equipment_0: "M60A3 Patton"
```

---

## 🟢 国別機体を「独立素体（デザイナー編集可）＋固有画像＋世代研究で解放」にする成功パターン

### 目的
各国の機体を、素体（chassis）とは別にデザイナーで編集でき、固有画像を持ち、
「対応する世代×型の素体を研究したら解放」されるようにする。

### 3点セット（これが揃わないと必ずどれか欠ける）
1. **独立素体化**（デザイナーが開く）
   - variant に `parent` だけでなく **明示的な `module_slots`（全13スロット = inherit）** を書く
   - parent から stats（maximum_speed〜build_cost_ic）も丸ごとコピーする
   - `allowed_module_categories` の再定義は**してはいけない**（default_modules が反映されなくなる）
2. **固有画像**（生産・デザイナーに絵が出る）
   - variant に `picture = <そのvariantのID>`（例 `picture = USA_TSF_F_22`）
   - `interface/*.gfx` に `GFX_<picture>_medium`（spriteType）を追加し dds を指す
   - ⚠️ `GFX_MVLV_pic_xxx`（technologies命名）は独立素体では**表示されない**。必ず `_medium`
3. **世代研究で解放**（ゲーム開始時に即使えない）
   - 隠しテック `tsf_variant_<nat>_<世代型>`（`allow={always=no}` `show_effect_as_desc=no`）に
     その世代型の機体だけを `enable_equipments` で列挙
   - `on_actions` の `on_daily` で `has_tech = MVLV_research_<対応framework> NOT={has_tech=その隠しテック}` 条件で付与
   - on_startup では基本フレームワークだけ全国配布。国別の機体は即付与しない

### 機体差別化は「ステータス」でなく「初期装備モジュール（default_modules）」で
- stats は素体準拠のまま、`default_modules` の中身（OS・装甲・武器・センサー・ミサイル等）で個性を出す
- 例：ステルス機=複合装甲+XM3、近接機=長刀/モーターブレード、対地機=支援砲/大型ミサイル、電子戦機=センサー追加

### XM3（マブラヴ次世代OS）の搭載ルール
- 日本：不知火・弐型**以降**のみ（武御雷系には載せない）
- 外国機：**第3世代機（本編終了後＝2015〜開発）以降**に搭載
- 第4世代機（2035〜：Su-57・テンペスト・04式・10式）は XM3 より上の `OS_4_normal`
- F-22 は「本編中に存在する機体」なので例外的に XM3 を載せず `OS_3_normal`
- OS性能の序列：OS_3_normal ＜ OS_XM3 ＜ OS_4_normal（XM3は第3世代の最新という位置づけ）

### framework研究ID と素体（chassis）の対応
```
chassis           → MVLV_research_basic_tsf_framework
chassis_1_light   → MVLV_research_tsf_1_light_framework
chassis_1_light_mod→ MVLV_research_tsf_1_light_mod_framework
chassis_1_heavy   → MVLV_research_tsf_1_heavy_framework
chassis_2_light   → MVLV_research_tsf_2_light_framework
chassis_2_heavy   → MVLV_research_tsf_2_heavy_framework
chassis_2_maneuver→ MVLV_research_tsf_2_maneuver_framework
chassis_3_light   → MVLV_research_tsf_3_light_framework
chassis_3_heavy   → MVLV_research_tsf_3_heavy_framework
chassis_3_maneuver→ MVLV_research_tsf_3_maneuver_framework
chassis_4         → MVLV_research_tsf_4_framework
```

### 表示名（生産・デザイナーで生IDにならないように）
- `derived_variant_name` では生産画面の表示名は決まらない
- **variantのID をキーにした loc**（例 `USA_TSF_F_22:0 "F-22 ラプター"`）を localisation に置く

### 部隊規模
- 支援戦術機中隊 = 1機 / それ以外の戦術機中隊 = 12機

### 🔴 division_template に「未解放の subunit」を入れるとクラッシュ（2026-06-06 実例）
- 症状：ゲーム内 2002.06.01 で EXCEPTION_ACCESS_VIOLATION（autosave/AI処理系）
- 原因：on_actions で全国に付与した師団テンプレートのうち「凄ノ皇師団」が **MVLV_xg_battalion** を使用。だが xg_battalion は `tsf_susanoo_concept`（凄ノ皇研究）で解放されるのに、テンプレ付与条件は `basic_tsf_framework` 研究後 → **付与時点で xg 部隊が未解放** → 不正な師団テンプレートになりクラッシュ
- 教訓：`division_template` を付与する時は、**そのテンプレが使う全 subunit が、付与条件のテックで解放済み**であること。未解放の部隊を含めてはいけない
- 修正：未解放部隊を使うテンプレは、その部隊の解放テック後に付与する別ブロックへ分離（フラグで冪等）
- ⚠️ 続報（2026-06-06 第2のクラッシュ）：**regiments(前線)だけでなく support(支援中隊)も同じ**。engineer/maintenance_company/field_hospital/recon/signal_company/logistics_company/motorized などバニラ部隊は研究で解放されるため、序盤に付与する division_template に入れると `Invalid subunit` ＋ `Unknown effect-type: support` でクラッシュ。**安全策：on_actionsで全国に配る師団テンプレは support を入れず、確実に解放済みの自前部隊(MVLV_tsf_battalion等)だけにする**。補助中隊はプレイヤーが手動で足す

### 🔴🔴 MODアセット流用時、gfx/models を「丸ごと」コピーすると本体を上書きしてクラッシュ
- やらかし：戦術機3Dモデル欠落を直すため、元MOD(MuvluvJP)の gfx/models を丸ごと(1405ファイル)コピー → 戦術機モデルは入ったが、同梱の geo_*(MD本体の歩兵/銃モデル)183個・generic_tank_medium(HOI4標準中戦車)8個が**本体ファイルを上書き** → 各国が歩兵・中戦車を配備する2002年8月で本体ユニットがクラッシュ
- さらに BETA・squad_frame の欠落アニメを参照する定義(_geo_animations.asset等)も紛れ込んでいた
- 症状：3Dモデルコピー後に「7月は越えるが8月で落ちる」。画像を直しても同じ8月で落ち続けた（画像は無関係だった）
- **教訓**：MODのアセットを流用する時は、必要なサブディレクトリ(gfx/models/units/tsf 等)だけをコピーする。gfx/models 丸ごとは厳禁
- 検証法：コピーした各ファイルの相対パスが HOI4本体/MD本体に同名で存在するか(=上書き)をチェック。存在したら本体を壊している
- 解決：gfx/models を全削除し、戦術機が実際に使うディレクトリ(units/tsf配下=223ファイル)だけ再コピー。戦術機の.mesh/.anim/texture/animation定義は全て units/tsf 配下にあった
- 補足：OneDriveフォルダのrmtreeは読み取り専用属性でPermissionError → PowerShellで`attrib -R /S /D`後に`Remove-Item -Recurse -Force`

### ⭐⭐ クラッシュ調査は「まずクラッシュレポートを見る」（鉄則・最優先）
- **やらかし反省**：2002年クラッシュで、ユーザーの言葉だけを頼りに装備定義ファイルの検証を何度も繰り返す回り道をした。crash dumpを最初に見ていれば一発で「PHYSFS＝アセット読込失敗」と分かり、3Dモデル欠落に最短到達できた
- **必ず最初にこの順で見る**：
  1. `Documents/Paradox Interactive/Hearts of Iron IV/crashes/` の最新フォルダ → `exception.txt`（スタックトレース）と `meta.yml`（日時・MOD構成）
  2. `logs/error.log`（末尾。"Invalid subunit"等の致命的エラー）
  3. `logs/game.log`（末尾。クラッシュ直前に何が実行されたか）
- **スタックトレースの読み方**：
  - `PHYSFS_swapULE64` 系（シンボル無しでも）→ ファイル/アセットのバイナリ読込。.mesh/.dds/.anim欠落、テクスチャ参照切れ、セーブ破損を疑う（＝文法エラーではない）
  - autosave中でなくゲーム進行中に落ちる＋同一スタックの再現性→特定アセットの読込失敗が濃厚
- 定義ファイルの突き合わせ検証は「レポートで当たりを付けた後」にやる。闇雲な全数検証から始めない

### 🔴🔴 戦術機の3Dモデル(.mesh)欠落 → 配備時にPHYSFSクラッシュ（2002年問題の真因）
- 症状：第1世代重戦術機を研究→生産→配備したあたり(2002年)で EXCEPTION_ACCESS_VIOLATION。crash dumpのスタックは全て `PHYSFS_swapULE64`（＝ファイル/アセットのバイナリ読込）。autosaveでなくゲーム進行中に落ちる
- 真因：**gfx/models フォルダが丸ごと存在せず、戦術機の3Dモデル(.mesh)が32個全部欠落**していた。entity定義(gfx/entities/tsf*.gfx, units_tsf*.asset)は存在するのに実体(.mesh)が無い
- 仕組み：sub_unit(MVLV_tsf_battalion等)が `sprite = tsf` で 3Dモデル `tsf_entity`→`generic_tsf_mesh`→generic_tsf.mesh を使う。部隊がマップ/戦闘画面で3D表示された瞬間、無い.meshを読みに行って落ちる
- 「第1世代重で出た」理由：日本主力の瑞鶴(Type82)が最初に量産・配備された戦術機だから。軽は未配備だっただけで、放置すれば全戦術機で同じく落ちる
- **重要な教訓**：定義ファイル(equipment/module/technology)がいくら完全整合でも、3Dモデル実体が無ければ落ちる。クラッシュ調査では定義だけでなく gfx/models の.mesh実在、texture(.dds)、anim(.anim)まで確認する
- 解決：元MOD「MuvluvJP_1.18_Test」(Steam workshop 3372337928)から gfx/models を丸ごとコピー(433MB, .mesh318+.dds828+.anim198)。entity定義(tsf*.gfx)が元MODと完全一致だったので、modelsコピーだけで全参照が解決
- 切り分けのコツ：crash dumpが `PHYSFS`系スタックなら「文法エラー」でなく「ファイル/アセット読込失敗」を疑う。.mesh/.dds/.anim の欠落、テクスチャ参照切れ等

### 🟢 framework前提・機体装備に「未来技術」を混ぜない（年代遅延の原因）
- 症状：第1〜2世代の戦術機が、本来の年代(1995/2005)でなく2010〜2015年まで研究・配備できない
- 原因2つ：
  1. **framework の dependencies に、その世代より新しい技術**が混ざっていた（例：第2世代軽(2005)の前提に add_sensor_3/deta_link_3(2015)）→ 2015年まで素体を研究できない
  2. **機体の default_modules に素体年代より新しいモジュール**（例：第2世代重(2005)機に armor_composite(2010)）→ 2010年まで配備できない
- 修正：
  - 前提から未来技術を削除（同年代以前の技術だけ残す）
  - 装備は同年代相応に置換：armor_composite(2010)→armor_heavy / add_sensor_3(2015)→add_sensor_2 / add_thruster_3(2015)→add_thruster_2 / OS_XM3 等は除去
- 検証法：各 framework/機体について「前提・default_modules の各技術の start_year ≤ その世代(素体)の year」を確認。超えていたら年代遅延バグ

### 🟢 AIの研究優先度を「研究枠の多い国だけ」上げる
- `ai_will_do` は乗算。modifier で国別条件を足せば国ごとに変えられる
  ```
  ai_will_do = {
      factor = 1
      modifier = { date > 2004.1.1 factor = 60 }                           # 全国: 年代到達で60
      modifier = { num_research_slots > 5 date > 2004.1.1 factor = 1.5 }    # 研究枠6以上: ×1.5 = 90
  }
  ```
- 判定は **`num_research_slots > N`**（現在の研究スロット数）。MDは**GDP（gdp_total/gdp_per_capita）で研究枠が増減**するので、これで「発展した大国だけ優先度UP」になる
- ⚠️ 失敗例：当初 `has_idea = super_power` を使ったが、MDの super_power は**研究スロットと無関係**（超大国フラグ＝faction権・配列管理）で、しかも**開始時はどの国も持たない**（フォーカスで動的付与）。研究枠判定には使えない
- `num_research_slots` はMD内で使用例ゼロだったが HOI4 標準trigger。ゲーム内で効くか要確認（効かなければ MD変数 `research_slot` を check_variable で判定する手もある）
- 特定系統（スサノオ等）を除外したい時は、その技術だけ modifier を足さない

### 🟢 完成品のみ生産可・素体は生産不可にする（MD方式）/ 特務素体のarchetype問題
- **素体を生産不可に**：派生素体（chassis_1_light〜chassis_4 等）に `is_buildable = no` を追加。これでMDの戦車/戦闘機と同じく「素体は作れず、完成品(variant)だけ生産可能」になる
  - MDの例：`heavy_tank_chassis`(is_buildable=no) → `heavy_tank_chassis_0`(variant,生産可)
  - variant側は is_buildable 未指定でも生産可能（親のnoを継承しない）。共通機は yes 明示済み
  - 副次効果：AIが素体でなく完成品(固有機・共通機)を生産するようになる
- **特務機(武御雷・瑞鶴)の画像が出ない問題**：原因は archetype の作りミス
  - 正しいarchetype `MVLV_TSF_chassis` は `is_archetype = yes`＋module_slots を持つ本体
  - だが `MVLV_TSF_specialForces_chassis` は **is_archetype 無し・archetype=MVLV_TSF_chassis の“子variant”**になっていた
  - 武御雷の `archetype = MVLV_TSF_specialForces_chassis`（=子variant）を指すと、**個別picture(画像)が反映されない**
  - 修正：specialForces_chassis を正しいarchetype化（`MVLV_TSF_chassis`の中身を丸ごとコピーしpicture名だけ変更＝is_archetype=yes・module_slots・stats・type/group_by/interface_category を揃える）
  - 教訓：variantの `archetype = X` の X は必ず **is_archetype=yes を持つ本体**を指すこと。子variantを指すと画像解決が壊れる

### 🔴 固有武装の検証は「ベース素体」でなく「その機体の親素体」で行う（autosaveクラッシュ実例 2026-06-05）
- 症状：ゲーム開始後しばらくして**オートセーブ書き込み時にクラッシュ**（exception.txt が `PHYSFS_writeULE64` / EXCEPTION_ACCESS_VIOLATION）。起動・パースは通る
- 原因：**`chassis_1_heavy` 系（撃震・瑞鶴の4型）には shoulder スロットが無い**のに、固有武装で shoulder にモジュールを割り当てていた。存在しないスロットへの default_modules 割り当て → serialize 不能 → autosave で落ちる
- 落とし穴：武装追加時の検証を**ベース素体 `MVLV_TSF_chassis`（任意6枠フル）の許可カテゴリだけ**で行っていた。実際に使えるスロットは **その variant の parent 素体の inherit チェーン**で決まり、素体ごとに違う
  - chassis_1_heavy / specialForces_chassis_1_heavy：shoulder **無し**（head/leftBackArm/arm/waist/leg のみ）
  - chassis_0 系：head のみ
  - その他の chassis_1_light〜4：任意6枠フル
- 正しい検証：parent をたどって「自分宣言スロット ∪ 親の有効スロット」を再帰計算し、default_modules の各スロットがそこに含まれるかを確認してから書き込む
- 切り分け：autosave時クラッシュ＋直前に default_modules を触った → まずスロット不整合を疑う（`Invalid subunit` や PHYSFS_write 系）
- 注意：クラッシュしたセーブは壊れている可能性。修正後は**新規ゲームで開始**して、最初のautosave（ゲーム内2月頭）を超えられるか確認する

### 🔴 autosaveクラッシュの真因：module_slots に「親素体に無いスロット」を inherit で宣言（2026-06-05 実例）
- 症状：新規ゲームで進行 → オートセーブ書き込み時にクラッシュ（exception.txt `PHYSFS_writeULE64` / EXCEPTION_ACCESS_VIOLATION、error.log `Invalid subunit.: none` in autosave_temp.hoi4）
- 真因：**撃震・瑞鶴（素体 chassis_1_heavy 系）の variant の module_slots に `MVLV_TSF_shoulder_slot = inherit` が残っていた**。だが chassis_1_heavy 系には shoulder スロットが無い → 親に無いスロットを inherit しようとして装備がランタイムで壊れる → その装備を持つ部隊の subunit が none → autosave で serialize 失敗してクラッシュ
- 重要：**default_modules だけ素体整合させても不十分**。`module_slots` 自体も「その variant の親素体に実在するスロットだけ」にしなければならない（default_modules から肩を消しても、module_slots に肩=inherit が残っていれば壊れる）
- パースは通る（起動・ロードは成功）。壊れるのは装備構築〜autosave のランタイム。だから error.log のロード時セクションには出ず、ゲーム内日付つきの `Invalid subunit` で出る

### ⚠️ 戦術機のスロットは13個（右背中スロットは“存在する”。前回の「無い」は誤判定だった）
- ベース素体 `MVLV_TSF_chassis` の module_slots は **13スロット**
- 基本6：armor / OS / engine / headUnit / right_hand / left_hand
- 任意7：head / shoulder / leftBackArm / **rigtBackArm（右背中）** / arm / waist / leg
- `MVLV_TSF_rigtBackArm_slot = MVLV_TSF_leftBackArm_slot` というエイリアス定義で、左背中と同じカテゴリ（剣/追加突撃砲/背中スラスター/背中補給）が入る
- ⚠️ ただし**派生素体ごとに任意枠は異なる**：`chassis_1_heavy`・`specialForces_chassis_1_heavy`（撃震・瑞鶴）は **shoulder が無い**。`chassis_0` 系は head のみ。それ以外（chassis_1_light〜4）は任意7枠フル
- 各スロットに入れられるカテゴリ：
  - head：センサー / 追加装甲（ブレードアーマー等）
  - shoulder：スラスター / センサー / 大型ミサイル / 追加装甲
  - leftBackArm / rigtBackArm：剣（長刀） / 追加突撃砲 / 背中スラスター / ドロップタンク
  - arm：近接（チェーンソード=モーターブレード / 短刀） / センサー / 追加装甲
  - waist：スラスター / 追加装甲
  - leg：追加装甲 / 補給
- ⚠️ カテゴリ厳守：チェーンソード/短刀は **arm のみ**、長刀は **left_hand/leftBackArm/rigtBackArm のみ**、大型ミサイルは **shoulder のみ**
- 安全策：**module_slots と default_modules の両方**を、その variant の親素体チェーンで再帰計算した「実在スロット集合」に対して検証してから書き込む（親をたどって own_slots ∪ 親の eff_slots を計算する）

### 🟢 AIに戦術機を研究させる頻度の上げ方（年代ゲート付き）
- 課題：元MODは第2・第3世代 framework の `ai_will_do` が **base factor 0**（前提装備が揃うまでAIがほぼ研究しない）。AIの戦術機が貧弱・世代更新しない一因
- 対策①：framework の `ai_will_do` を年代条件付き factor に
  ```
  ai_will_do = {
      factor = 1                                  # 年代前は標準（＝未来世代を先取りしない）
      modifier = { date > 2004.1.1 factor = 3 }   # その世代の年代に達したら優先
      modifier = { has_tech=... date > 2004.1.1 factor = 5 }  # 前提装備も揃えば最優先(計15)
  }
  ```
  - 世代の開始年：第1=1995 / 第2=2005 / 第3=2015 / 第4=2035。`date > (年-1).1.1` でゲート
  - factor は**乗算**。base 0 だと何を掛けても0なので、優先させたいなら base を 1 以上にする
- 対策②：研究速度ボーナスidea（カテゴリ研究速度）を on_actions で全国付与
  ```
  # common/ideas/: hidden_ideas = { MVLV_tsf_research_boost = { research_bonus = { MVLV_tsf_tech = 0.15 } } }
  # on_startup: every_country = { add_ideas = MVLV_tsf_research_boost }
  # on_weekly : every_country = { if = { limit = { NOT = { has_idea = ... } } add_ideas = ... } }  # 既存セーブ冪等
  ```
  - カテゴリ別研究速度は idea の `research_bonus` で（focus/continuous_focus の modifier では `Unknown modifier` になる→このファイル冒頭の項を参照）
- 「①選ばれやすく＋②速く」の合わせ技。年代ゲートで未来技術の先取りは防げる

## 🟢 国家統合（軸がバラバラ）でも固有機体を継承させる方法
- 機体解放を TAG 名指し（`USA = {...}`）だけにすると、統合で別の国が軸になったとき**吸収された国の機体が宙に浮く**
- 解決：`every_country` + `any_owned_state = { is_core_of = <母国TAG> }` で「その機体の母国の元領土を持つ国」に解放
  ```
  every_country = { if = { limit = {
      has_tech = MVLV_research_tsf_3_maneuver_framework
      any_owned_state = { is_core_of = FRA }
      NOT = { has_tech = tsf_variant_fra_3m }
  } set_technology = { tsf_variant_fra_3m = 1 } } }
  ```
- 利点：州ID(province/state番号)不要。`is_core_of` は元の中核州判定なので、併合・領土編入どの統合方法でも、軸がどこでも継承できる
- 平常時の自国は「自国中核州を所有」なのでこの式だけで解放される（即時性が欲しければ TAG 名指しの on_daily も併用＝冪等で無害）
- 負荷：`every_country`×グループ数×`any_owned_state` は重めなので **on_weekly** に置く（統合は稀なので週1で十分）

### 教訓
- 「デザイナーが開かない」→ module_slots（全inherit）漏れを疑う
- 「絵が出ない」→ picture が `_medium` を指していない／gfxに該当spriteが無いを疑う
- 「開始時に全機使える」→ on_startup/on_weekly で即付与していないか疑う
- common/*.txt は **BOM無し** で保存（BOM有だと "Unexpected token" でツリー全消滅）。loc yml は BOM有

---

## 🟢 デバッグ方法

### autosave クラッシュの切り分け手順
1. **MD Beta 単独で起動** → 我々の MOD が原因か確認
2. **段階的にファイルを `.bak` にリネーム** → 二分探索で犯人特定
3. クラッシュレポート確認：
   - `crashes/hoi4_*/exception.txt` でスタックトレース
   - `crashes/hoi4_*/logs/error.log` で具体的なエラー
   - `crashes/hoi4_*/meta.yml` で `IsOldSave`（古いセーブのロードかどうか）と MOD リスト
   - `crashes/hoi4_*/dlc_load.json` で実際に有効だった MOD ID

### 良いログの読み方
- `IsOldSave: false` = 古いセーブを開いた crash ではない
- `persistent.cpp:66` = セーブ書き込み処理（autosave 含む）
- `triggerimplementation.cpp:3140` = ai_strategy 内の trigger 評価（has_tech 等が無効な参照だとここに出る）

---

## 🔴🔴🔴 equipment ファイルを `duplicate_archetypes = {` で囲むと、その素体を使う機体の生産解放でクラッシュ（2026-06-07 真因・最重要）

### 症状
- `research all` 後に時間を進めると EXCEPTION_ACCESS_VIOLATION（C0000005）
- スタックは全て `PHYSFS_swapULE64`（シンボル無し）、深いネストで `(+3331456)` と `(+3332817)` が**交互に繰り返す＝再帰の暴走**
- 「第1世代重戦術機（瑞鶴 zuikaku）を研究完了するとクラッシュ」と特定できるが、瑞鶴の定義そのものは完全に正常に見える
- error.log には致命的エラー無し（TSF系は "script_enum に無い" の無害な警告のみ）

### 真因
- 素体定義ファイル `MVLV_TSF_specialForces_chassis.txt`（武御雷ツリー素体）と `MVLV_TSF_support_chassis.txt`（攻撃機ツリー素体）が、
  ファイル先頭で **`duplicate_archetypes = { ... }`** で全体を囲んでいた
- 正しい素体ファイル `MVLV_TSF_chassis.txt` は **`equipments = { ... }`** で囲んでいる（これは落ちない）
- `duplicate_archetypes` で定義した archetype/variant を、**別ファイルの variant が実際に生産解放(enable_equipments)して frame 生成すると、HOI4 内部の親子参照解決が再帰的に破綻**してクラッシュする
- 瑞鶴(zuikaku)は `specialForces_chassis` を実際に enable する唯一の機体だった（武御雷は enable 0回＝生成されないので巻き添えにならず無実に見えた）→ 瑞鶴だけが落ちた

### 修正
- `duplicate_archetypes = {` を **`equipments = {`** に置換（specialForces_chassis / support_chassis の2ファイル）
- これだけで解決。中身（archetype, module_slots, default_modules, 数値）は一切変えなくてよい

### 切り分けで効いた決定打
- 「素体ファイルの先頭バイト」を比較した：
  - chassis.txt = `\n\nequipments = {` （正常）
  - specialForces_chassis.txt = `duplicate_archetypes = {` （異常）
- 内容(行集合)が完全同型なのに片方だけ落ちる → **囲みブロックの種類**を疑え

### 教訓・注意
- ⚠️ **静的解析で何も見つからない時は「ファイルを囲む最上位キーワード」を確認する**。素体・装備は必ず `equipments = { }` で囲む。`duplicate_archetypes` は使わない
- my パーサ（`\n\t<name> = {` で中の素体を拾う正規表現）は囲みが何であろうと中身を拾えてしまうので、囲みの異常を見逃す。**先頭バイト/先頭行を直接見ること**
- スタックに同じ2アドレスが交互に並ぶ＝**無限再帰/深い再帰**。文法エラーやアセット欠落(.mesh)とは別系統。「素体の親子/複製の定義」を疑う
- 比較対象を選ぶ時は「**実際に enable_equipments で生産解放されているか**」を必ず確認する。enable 0回の機体（武御雷）は frame 生成されず、落ちないからといって無実とは限らない（＝比較対象として無効）
