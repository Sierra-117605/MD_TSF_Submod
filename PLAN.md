# PLAN.md — MD_TSF_Submod 当初の意図

## プロジェクト概要

**MD_TSF_Submod** は Hearts of Iron IV の MOD「Millennium Dawn: A Beta Test Mod」（以下 MD Beta）に Muv-Luv の戦術機（戦術歩行戦闘機 / Tactical Surface Fighter）を追加する個人用 submod。

## 目的

- MD Beta の現代戦シミュレーションに Muv-Luv の戦術機を組み込み、独自の戦闘体験を楽しむ
- **個人利用のみ、公開はしない**（Muv-Luv 素材は MuvluvJP MOD 由来）

## 想定するゲーム体験

- 主要国（USA, RUS, JAP, CHI, GER, FRA, ENG, IND など）が独自の戦術機を研究・生産
- 日本帝国軍の 77式撃震 / 94式不知火 / TYPE-00武御雷、米国の F-5 / F-22、ロシアの MiG-21 / Su-37、中国の J-10 など、Muv-Luv 正典の機体を再現
- MD Beta の通常兵科（歩兵・戦車）と並行して戦術機師団を運用可能

## 素材ソース

- **MuvluvJP_1.18_Test** (Workshop ID: 3372337928) — オリジナルの戦術機 MOD。テクスチャ、3D エンティティ、モジュール定義、テクツリーを流用
- **MuvluvJP** (Workshop ID: 3244449823) — 別バリアント
- Muv-Luv 関連 MOD 群（参考用）

## 元 MOD からの主な改造方針

1. **start_year を +30 年シフト**（1970年代 → 2000年代）して MD の時代設定に合わせる
2. **BETA 関連の battalion/装備は削除**（MD は対人戦想定のため、対 BETA 用は不要）
3. **テクツリーを MD のタイムラインに整合**
4. **localisation を日本語化、ファイル名衝突を回避するため `MVLV_` prefix を付ける**
5. **MD Beta の装備デザイナー UI と統合**

## 大きな改造の歴史

### Plan A: AI 自動配備対応
- AI が装備デザイナーを使わなくても戦術機を生産・配備できるようにするため、chassis variant ごとに `default_modules` を設定
- → **過剰な実装で autosave クラッシュ等を誘発。後で撤回**

### Plan C: 国別命名 variant
- 各国の戦術機に Muv-Luv 正典の固有名称を付ける（F-22, 不知火, 武御雷 等）
- 国限定の派生 equipment + テク（`allow_branch`）として実装
- 当初ハイフン使用 `USA_TSF_F-22` で構文エラー → 識別子はアンダースコアに修正

## ユーザーについて

- HOI4 MOD 開発知識・コーディング知識は**ない**
- AI（Claude）に作業を依頼してドキュメント / コード / Paradox スクリプトを書いてもらう前提
- 専門用語は平易な言葉で説明されることを希望
