# TODO.md — MD_TSF_Submod 作業状況

最終更新: 2026-06-13

---

## ✅ 直近の完了作業（2026-06-10〜13）

### 機体・素体まわり

- [x] **月虹（試02式戦術歩行戦闘機 F-15SEJ）新設**
  - 日本第3世代重戦術機、jap_3hで解放、画像=F-15SE.dds（後にACTVと議論しF-15SE確定）
  - 両スプライト（GFX_MVLV_pic + _medium）整備

- [x] **不知火の再配置**：3世代高機動 → **2世代高機動**へ移動
  - 第2世代高機動の空白を埋めた
  - 性能を世代相応に下方修正（-15%）

- [x] **不知火・壱型丙を3世代支援戦術機化**
  - archetype = support_chassis、parent = support_chassis_3_maneuver（pool統一）
  - 表示名「不知火・壱型丙（支援型）」

- [x] **04式を高機動 → 重戦術機に変更**（archetype変更、性能調整）

- [x] **武御雷C/A/F/R の差別化（原作出力比準拠）**
  - C=100/A=75/F=50/R=25（量産→希少フラッグシップ）
  - C型(黒)が標準量産、R型(青紫)が将軍家専用

- [x] **瑞鶴C/A/F/R も同じ差別化**（C=100/A=75/F=50/R=25）

- [x] **試製武御雷 TYPE-98X 表示名修正**
  - abbreviation を "TYPE-00" → "TYPE-98X" に
  - loc 3ヶ所重複解消

- [x] **全固有機 priority=100、汎用機 priority=10**に統一（90点差で確実に固有機優先）

### 素体まわり

- [x] **全12種の子素体を is_buildable=yes** に（プレイヤー自由設計可能）

- [x] **default_modules 全部空に**（プレイヤーが自由にモジュール選択）

- [x] **支援素体のサブカテゴリ（light/heavy/maneuver）廃止**（案C）
  - 12素体 → 6素体（archetype + _0 + 世代別1/2/3/4）

- [x] **特務素体のサブカテゴリも整理**（高機動系列のみ残す）

- [x] **支援素体は軽戦術機frameworkで解放**するよう統一

### 研究システム

- [x] **モジュール&素体→固有機体の並列化**（重要）
  - framework の dependencies からモジュール前提削除（10件）
  - variant 配布条件に前提モジュール条件をAND追加（108件）
  - 順序不問で両方研究すれば固有機体配布

- [x] **AI研究優先度設定**
  - 前提モジュール・素体framework → factor=90
  - 非前提モジュール → factor=40

- [x] **2000年以前のテック38個を on_startup で全国に付与**
  - 基礎研究・1世代モジュール・1世代framework
  - debug_pack、A-6/A-10/A-10C/A-12（未移植機）は除外

### F-47

- [x] **F-47を重戦術機化**（archetype = MVLV_TSF_chassis → chassis_heavy）
  - 重戦術機師団・F-47師団に組み込み可能に
  - ゲーム内表記が「戦術機」→「重戦術機」に

- [x] **F-47テンプレ解放の流れ変更**
  - 旧：framework研究 → 即テンプレ付与
  - 新：framework → 武装研究 → systems研究 → テンプレ付与

- [x] **F-47アイコン Type-00UN.dds 設定**（picture追加 + 両スプライト登録）

### 凄ノ皇（XG）

- [x] **スサノオ大隊 priority 2500 → 5000**（凄ノ皇師団アイコンを XG 専有に）
- [x] **xg_equipment 工場割り当て 10個**（同archetype統一）

### 師団テンプレ

- [x] **9師団テンプレの自動補完処理**（AIのみ・月次・has_template チェック）
  - 軽/重/高機動/混成/支援/特務/特務突撃/凄ノ皇/F-47
  - AIが削除・改名しても元の名前で復活
  - プレイヤーは編成自由（補完されない）

### 配布制御

- [x] **ZOM（ゾンビ）/ ALN（エイリアン）を戦術機から完全除外**
  - on_startup + on_monthly の全配布78件に NOT={tag=ZOM} NOT={tag=ALN} 追加

- [x] **日本での汎用機強制取り消し**（固有機被り対策）
  - F-4/F-15/F-16/F-18/F-15E/Su-34/ADF-01/support_3l を日本から取り消し
  - 残す：F-5（1世代軽）、F-35（3世代軽）、その他支援機

- [x] **第2世代汎用機配布のスワップ修正**
  - 2軽→F-16、2高機動→F-18、2重→F-15（正しい組み合わせに）

### 生産・工場

- [x] **工場割り当てを全archetype 10個に統一**
  - chassis (親), chassis_light/heavy/maneuver, support_chassis, specialForces_chassis, xg_equipment

- [x] **AI工場建設優先度（軍需400/民需150/造船所50）**
  - 戦術機保有国（basic_framework研究済み）に適用

### 画像・UI

- [x] **F-47機体画像追加**（GFX_MVLV_pic_f-47_equipment_ishkur + medium）

- [x] **J-20画像 Lunatic Lunarian版に差し替え**

### loc・互換性

- [x] **MD本体キーとの衝突470件削除**（TSF Submodが MD本体loc を上書きしていた問題）
  - MVLV_TSF_equipment（336件）、designer（85件）、replace/系（49件）

- [x] **古い `+JP: Modern Day mod` の非互換問題解明**（HOI4 1.17対応で MD 2.0.0と衝突）

- [x] **完全攻略ガイド GUIDE.md 作成**（14章＋付録）

- [x] **GitHubリポジトリ作成・初回push**
  - https://github.com/Sierra-117605/MD_TSF_Submod

---

## ⚠️ 既知の問題・要確認事項

- [ ] **既存セーブで素体（chassis_X_Y）が出るか**：is_buildable変更がセーブで反映されるか実機確認
- [ ] **AI重戦術機師団訓練**：補完処理で重師団テンプレ付与後、実際に訓練されるか1ヶ月以上プレイで確認
- [ ] **凄ノ皇師団アイコン**：priority=5000で XG専有になったか実機確認
- [ ] **F-47重戦術機表記**：ゲーム内で「重戦術機」と表示されるか
- [ ] **モジュール&素体→固有機体の流れ**：AIが新システムで固有機体に辿り着くか実プレイで確認

---

## 📋 未着手のアイデア

### 機体追加（保留中）
- [ ] **攻撃機型TSF**（A-6 海神 / A-10 凌鉄 / A-10C / A-12 アヴェンジャー）
  - 当時「カブり多いのでやめる」判断
  - 新archetype（chassis_attacker）か chassis_heavy統合かで再検討可

- [ ] その他未移植機体（F-4 Phantom米軍版、F-14Ex、F-18HMRV/AX、F-5派生、Starker Wind 等）

### システム拡張
- [ ] **第4世代特務固有機体**新設（現在T00Cは素体のみ解放）
  - 候補：武御雷の後継・新型機

- [ ] **F-47師団テンプレの自動最適化**（F-47機体が解放されたら自動的にF-47師団編成に切替）

- [ ] **AI戦略：戦術機師団を機甲化師団と同列の優先度に**
  - ai_strategy で生産・訓練の優先度を armor と同等に
  - 全機能の実装・検証完了後に着手

### UI・演出
- [ ] **戦術機師団アイコンの差別化**（軽/重/高機動を視覚的に区別）
- [ ] **凄ノ皇・F-47の専用師団アイコン**
- [ ] **武御雷 C/A/F/R の各型アイコン**

---

## 🗂️ プロジェクト構造

```
C:\dev\MD_TSF_Submod\          ← Gitリポジトリ（開発・ドキュメント）
├ GUIDE.md                     ← 完全攻略ガイド
├ KNOWLEDGE.md                 ← ハマりポイント・学び
├ TODO.md                      ← このファイル
├ SPEC.md                      ← 仕様メモ
├ PLAN.md                      ← 元々の計画
├ STATS_COMPARISON.md          ← 性能比較表
├ VARIANT_DESIGN.md            ← 機体設計メモ
├ MACHINE_LOADOUTS.md          ← 機体装備メモ
├ scripts/                     ← 開発用スクリプト
├ common/, gfx/, interface/, localisation/  ← MOD本体
└ descriptor.mod

C:\Users\tkmuh\OneDrive\ドキュメント\Paradox Interactive\Hearts of Iron IV\mod\MD_TSF_Submod\
                              ← HOI4が実際に読むMOD本体
                              ← 開発後にここを更新、dev側に同期してcommit
```

---

## 📝 メモ

- **開発フロー**：MOD本体（OneDrive側）で編集 → dev側に同期 → git commit & push
- **HOI4起動前**：必ずHOI4を完全終了してから編集
- **テスト**：archetype変更・装備削除等は新規ゲーム必須（既存セーブクラッシュ要因）
- **MD Beta 2.0.0**：HOI4 1.18.3.0と組み合わせ。1.19系は未対応
- **ゾンビモード**：MD内蔵で完結（Doomsday MOD不要）
- **古い +JP MOD**：HOI4 1.17対応で MD 2.0.0と非互換、必ず無効化
