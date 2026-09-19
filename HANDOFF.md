# HANDOFF.md — 次回セッション引き継ぎ

最終更新: 2026-09-19（MD 2.0 正式版・HOI4 1.19 対応の修正を実施 / 実機確認待ち）

---

## 2026-09-19 [Claude Code → 本人] MD 2.0 正式版対応: 実機確認待ち

- ステータス: 修正実施済み / **本人のHOI4起動確認待ち**
- 関連: TODO.md「MD 2.0 正式版・HOI4 1.19 対応」、KNOWLEDGE.md 末尾3セクション

### 状況
6月中旬から作業が止まっていた。その間に HOI4 が 1.19.3.0 に、MD が正式版 2.0.0 になった。
MD正式版（workshop 2777392649）とMD Beta 2.0.0 は中身がほぼ同一で、サブMOD側の作り直しは不要と判明。

### やったこと
1. descriptor.mod を 1.19 + MD正式版の依存に変更
2. MDの古いコピーになっていた2ファイル（countrytechtreeview.gui / continuous_focus/generic.txt）を
   MD 2.0のファイルを土台にして作り直し、TSF部分だけ移植
3. MD本体を上書きしていた loc 18件・スプライト4件を削除

### 本人にお願いしたいこと
1. エクスプローラで OneDrive 側のMODフォルダを「このデバイス上で常に保持する」に設定
   （875ファイル中633ファイルがクラウドのみで、このままだとHOI4が読めない）
2. dev側 → OneDrive側へのコピー（OneDrive起動後）
3. ランチャーで MD正式版 + 本サブMOD を有効化して新規ゲーム
4. `logs/error.log` に MVLV / TSF 関連のエラーが出ていないか確認

### 判断してほしいこと
- 不要ファイル3件（スサノオ大隊の重複定義になっている .tmp 残骸を含む）を削除してよいか

---

## 🚀 次の会話を始めるときのプロンプト

新しいClaude Codeセッションで、最初に以下をそのまま貼り付けてください：

```
MD_TSF_Submodの開発を続ける。
まず C:\dev\MD_TSF_Submod\HANDOFF.md を読んで現状を把握して。
そのあと C:\dev\MD_TSF_Submod\TODO.md と KNOWLEDGE.md も確認して。

前回までで「高機動戦術機にSPモジュール枠が出ない」問題は解決済み（sp_slot 3個で実機確認OK）。
今は次の3つのタスクが残っている：
1. 凄ノ皇師団アイコンを XG 専有に（priority=5000では効かなかった）
2. AI戦略：戦術機師団を機甲化師団と同列の優先度に
3. 攻撃機型TSF（A-6/A-10/A-10C/A-12）の機体variant追加（素体は既に追加済み）

優先度1から着手したい。
```

---

## ✅ 前回までに解決済み（2026-06-14 実機確認）

| 項目 | 結果 |
|---|---|
| 高機動戦術機のSP枠表示（sp_slot継承修正・3個） | ✅ OK |
| 既存セーブで子素体（chassis_X_Y）が出現 | ✅ 出た |
| 重戦術機表記 | ✅ 出た |
| モジュール&素体→固有機体の解放フロー | ✅ 問題なし |

### 反映済みの sp_slot 修正サマリー
- `MVLV_TSF_0_chassis_categories.txt` の light_0 / heavy_0 / maneuver_0 に `sp_slot_1〜3 = inherit` 追加
- 全7ファイルから `sp_slot_4/5/6` 行を削除（合計約305行）
- 結果：archetype → chassis_X_0 → chassis_X_Y → variant の継承チェーンで SP枠3個が確実に降りる

---

## 🎯 次のタスク（優先度順・ユーザー確定）

### 1. 凄ノ皇師団アイコンを XG 専有にする（最優先）

#### 現状
- priority=5000（HANDOFF.md 旧版で「これでXG専有のはず」と書いていた）→ **実機で効かなかった**
- 凄ノ皇師団に汎用戦術機アイコンが表示される

#### 検討アプローチ
- `unique_unit_icon` を凄ノ皇師団テンプレ（XG師団テンプレ）に直接指定する
- もしくは専用sprite を定義 → division_template が参照
- ユーザー要望：**アイコン差別化はスサノオだけ**（軽/重/高機動の区別は現状維持）

#### 着手前に確認したいこと
- HOI4 が師団アイコンを決定する仕組み（priority のみ参照か、unique_unit_icon 等の上位機構があるか）
- スサノオ大隊（MVLV_xg_battalion）の現在のアイコン定義はどこにあるか
- 凄ノ皇師団テンプレのファイル位置と現在の sprite/icon 設定

### 2. AI戦略：戦術機師団を機甲化師団と同列の優先度に

#### 内容
- ai_strategy で戦術機師団（tsf_battalion系）の生産・訓練優先度を armor と同等に
- 既存 `common/ai_strategy/` 内の戦術機関連ファイルを修正
- 既存テンプレ補完処理（has_template チェック）との整合に注意

#### 既存資産
- `common/ai_strategy/tsf_generic_strategy.txt` 等の vanilla 形式ファイルあり
- KNOWLEDGE.md 参照：`ai_strategy_plans/` ではなく `ai_strategy/` に置くこと（autosaveクラッシュの教訓）

### 3. 攻撃機型TSF（A-6/A-10/A-10C/A-12）の機体variant追加

#### 現状
- **素体は既に追加済み**（chassis_attacker または chassis_heavy 流用）
- 機体variant が無いので AI が運用できない（素体だけでは固有機解放のフローに乗らない）

#### やること
- 各機の variant 定義（archetype / parent / picture / default_modules / 配布条件）
- 機体画像（dds + GFX sprite）の整備
- 配布制御（on_actions に米国向け enable_equipments 追加）
- 表示名（loc：A-6 海神 / A-10 凌鉄 / A-10C / A-12 アヴェンジャー）

---

## 📁 開発ディレクトリ二重構造

```
C:\dev\MD_TSF_Submod\           ← Gitリポジトリ（ドキュメント中心）
├ GUIDE.md (2708行)              完全攻略ガイド
├ TODO.md                        作業状況
├ KNOWLEDGE.md                   ハマりポイント
├ SPEC.md / PLAN.md              仕様・計画
├ HANDOFF.md                     このファイル
├ common/, gfx/, interface/, localisation/  MOD本体（同期用ミラー）
└ descriptor.mod

C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod\
                                ← HOI4が実際に読むMOD本体
                                ← 編集はこちら → dev側に同期 → git commit
```

**重要**: HOI4が読むのはOneDrive側。実機テスト前にOneDrive側が最新であることを確認すること。

---

## 🎮 環境

| 項目 | バージョン |
|---|---|
| HOI4 | **1.19.3.0**（2026-09-19時点） |
| MD | **正式版 2.0.0**（workshop 2777392649）。Beta 2.0.0 と中身はほぼ同一 |
| Visual Aid Mod | 任意 |
| JP翻訳MOD（旧 +JP） | **無効化必須**（HOI4 1.17対応で非互換） |
| Doomsday MOD | **不要**（MD内蔵） |

---

## ⏳ 未確認のまま残るもの

- [ ] **AI重戦術機師団訓練**：has_template補完後の訓練動作（1ヶ月以上プレイで確認）
- [ ] **F-47重戦術機表記**：ゲーム内で「重戦術機」と表示されるか（プレイヤー側未確認）
- [ ] **F-47機体としての挙動**：F-47は「めっちゃ強い重戦術機」の立ち位置で固定。テンプレ自動最適化等は不要

---

## 📋 ユーザー特性メモ

- **コード・プログラミングの知識ゼロ**
- 日本語でやり取り、専門用語は平易に説明
- HOI4 + Muv-Luv の融合MODを作りたい
- **AIが戦術機をちゃんと使ってくれること**が最優先設計目標
- 重大な変更前は確認を求める（破壊的操作には特に注意）
- 簡潔な応答を好む。長い解説より「何が変わったか」を端的に

---

## 🗂️ GitHubリポジトリ

URL: https://github.com/Sierra-117605/MD_TSF_Submod

push流れ：
1. OneDrive側でMOD編集
2. dev側にミラー同期
3. `git add` → `git commit` → `git push`

---

## 🔁 開発時の鉄則（KNOWLEDGE.mdより抜粋）

1. **archetype変更・装備削除は新規ゲーム必須**（既存セーブクラッシュ）
2. **HOI4完全終了してから編集**（ファイルロック・キャッシュ問題）
3. **JP翻訳MODは無効化**（HOI4 1.17時代の遺物）
4. **on_actions変更後はキャッシュクリア相当で新規ゲーム推奨**
5. **継承チェーンは parent → archetype 全段確認**（sp_slot問題の教訓）
6. **equipment ファイルは `equipments = { }` で囲む**（`duplicate_archetypes` は再帰クラッシュ要因）
7. **ai_strategy は `ai_strategy/` フォルダに**（`ai_strategy_plans/` は MD Beta 拡張形式必須でautosaveクラッシュ）
