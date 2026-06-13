# 戦術機 variant 実装設計書（全機種・確認用）

実装前の最終確認用。各機体＝「素体(chassis variant)」＋「default_modules」。
見た目(3Dモデル)は世代別汎用（専用は撃震/不知火/武御雷/MiG-21/J-10のみ）。

---

## モジュール世代対応
| 種別 | 第1世代 | 第2世代 | 第3世代 | 第4世代 |
|---|---|---|---|---|
| エンジン標準 | engine_1 | engine_2 | engine_3 | engine_4 |
| エンジン高機動 | engine_maneuver_1 | engine_maneuver_2 | engine_maneuver_3 | engine_maneuver_3 |
| エンジン巡航 | engine_cruise_1 | engine_cruise_2 | engine_cruise_3 | engine_cruise_3 |
| OS標準 | OS_1_normal | OS_2_normal | OS_3_normal | OS_4_normal |
| OS近接 | OS_1_close | OS_2_close | OS_3_close | OS_XM3_close |
| OS支援 | OS_1_support | OS_2_support | OS_3_support | OS_XM3_support |
| OS最新 | - | - | OS_XM3 | OS_XM3 |
| 頭部標準 | head_normal_1 | head_normal_2 | head_normal_3 | head_normal_3 |
| 頭部重 | head_heavy_1 | head_heavy_2 | head_heavy_3 | head_heavy_3 |
| 頭部空戦 | head_aerial_1 | head_aerial_2 | head_aerial_3 | head_aerial_3 |
| 突撃砲 | assault_cannon_1 | assault_cannon_2 | assault_cannon_3 | assault_cannon_3 |
| 支援突撃砲 | support_assault_cannon_1 | support_assault_cannon_2 | support_assault_cannon_3 | support_assault_cannon_3 |

その他：long_sword（長刀・攻撃）/ chain_sword（モーターブレード・防御）/ shield / reactive_shield /
add_blade_armor（ブレード装甲）/ add_thruster_1-3（スラスター）/ add_sensor_1-3（地形追随等）/
large_missile_1-2（長射程ミサイル）/ support_gun（重火力低機動）/ deta_link_1-3（データリンク）

---

## 型別 標準default_modules（Nは世代）
| スロット | 軽戦術機 | 重戦術機 | 高機動戦術機 | 特務戦術機 |
|---|---|---|---|---|
| armor_slot | armor_light | armor_heavy | armor_composite | armor_composite |
| engine_slot | engine_maneuver_N | engine_cruise_N | engine_maneuver_N | engine_maneuver_N |
| OS_slot | OS_N_close | OS_N_support | OS_XM3(3+)/OS_N_normal | OS_XM3 |
| headUnit_slot | head_normal_N | head_heavy_N | head_aerial_N | head_aerial_N |
| right_hand_slot | assault_cannon_N | assault_cannon_N | assault_cannon_N | assault_cannon_N |
| left_hand_slot | long_sword | shield | reactive_shield | long_sword |
| 追加(あれば) | shield | large_missile_N | long_sword + add_thruster_N | long_sword + add_blade_armor |

---

# 国別 全機種

## 🇺🇸 アメリカ（USA）
| 戦術機 | 素体 | 世代/年 | 型 | 固有モジュール（標準からの差分） |
|---|---|---|---|---|
| F-5 フリーダムファイター | chassis_1_light | 1 / 1995 | 軽 | 標準（廉価・軽量の祖） |
| F-16 ファイティングファルコン | chassis_2_light | 2 / 2005 | 軽 | +deta_link_2（Hi-Lo Mix・多用途） |
| F-14 トムキャット | chassis_2_heavy | 2 / 2005 | 重 | engine_cruise_2 + large_missile_2（フェニックス長射程） |
| F-15 イーグル | chassis_2_heavy | 2 / 2005 | 重 | +large_missile_2（制空） |
| F-15E ストライクイーグル | chassis_2_heavy | 2.5 / 2010 | 重 | right_hand=support_assault_cannon_2（攻撃強化） |
| F-18 ホーネット | chassis_2_maneuver | 2 / 2005 | 高機動 | 標準（艦載多任務） |
| F-18EF スーパーホーネット | chassis_2_maneuver | 2.5 / 2010 | 高機動 | +add_thruster_2（強化格闘） |
| F-22 ラプター | chassis_3_maneuver | 3 / 2015 | 高機動 | OS_XM3 + armor_composite（ステルス戦域支配） |
| F-35 ライトニング | chassis_3_light | 3 / 2015 | 軽 | armor_composite + OS_XM3 + add_blade_armor（Lo・近接ステルス） |
| YF-23 ブラックウィドウII | chassis_3_maneuver | 3 / 2015 | 高機動 | left_hand=long_sword + right_hand=support_assault_cannon_3（複合兵装） |

## 🇯🇵 日本（JAP）— 通常
| 戦術機 | 素体 | 世代/年 | 型 | 固有モジュール |
|---|---|---|---|---|
| 77式戦術歩行戦闘機 撃震 | chassis_1_heavy | 1 / 1995 | 重 | left_hand=long_sword（国産初・近接） |
| 89式戦術歩行戦闘機 陽炎 | chassis_2_heavy | 2 / 2005 | 重 | left_hand=long_sword（F-15J・近接改修） |
| 97式戦術歩行高等練習機 吹雪 | chassis_2_maneuver | 2-3 / 2010 | 高機動 | OS_XM3（練習機だが第3世代準拠） |
| 94式戦術歩行戦闘機 不知火 | chassis_3_heavy | 3 / 2015 | 重 | OS_XM3 + long_sword（世界初第3世代） |
| 94式 不知火・壱型丙 | chassis_3_heavy | 3 / 2015 | 重 | +support_assault_cannon_3（重武装・データリンク） |
| 04式 不知火・弐型 | chassis_3_maneuver | 3 / 2018 | 高機動 | OS_XM3 + add_thruster_3 + long_sword（XFJ高機動化） |
| 04式戦術歩行戦闘機(Type-04) | chassis_4 | 4 / 2035 | 重 | OS_XM3（次世代） |
| 10式戦術歩行戦闘機(Type-10) | chassis_4 | 4 / 2035 | 高機動 | OS_XM3 + add_thruster_3（次世代） |

## 🇯🇵 日本（JAP）— 特務（斯衛軍／specialForces_chassis）
| 戦術機 | 素体 | 世代/年 | 型 | 固有モジュール |
|---|---|---|---|---|
| 82式戦術歩行戦闘機 瑞鶴 | sF_chassis_1（軽量） | 1 / 1995 | 特務 | long_sword×2（**特務大隊の早期解放機**） |
| 試製98式戦術歩行戦闘機 武御雷 | sF_chassis_2_maneuver | 2 / 2005 | 特務 | OS_XM3 + add_blade_armor + long_sword×2 |
| 00式 武御雷 C型(黒) | sF_chassis_3_maneuver | 3 / 2015 | 特務 | XM3+ブレード装甲+long_sword×2 / 標準・一般衛士（出力比70） |
| 00式 武御雷 A型(白) | sF_chassis_3_maneuver | 3 / 2015 | 特務 | 同上 / 高機動・一般武家（出力比80） |
| 00式 武御雷 F型(赤/黄) | sF_chassis_3_maneuver | 3 / 2015 | 特務 | 同上 / 高機動・有力/譜代武家（出力比90） |
| 00式 武御雷 R型(紫/青) | sF_chassis_3_maneuver | 3 / 2015 | 特務 | 同上+生体認証 / 最高出力・将軍家/五摂家（出力比100） |

※R/A/F/Cは同素体・同モジュールで、stats（max_org・攻撃・装甲）とpriorityで出力差を表現（R>F>A>C）。色は呼称のみ（見た目は3Dモデル共通）。
※瑞鶴も同様にType-82 R/F/A/C型が存在（必要なら同方式で展開可能。現状は早期解放用に1機種）。

## 🇷🇺 ロシア（RUS）
| 戦術機 | 素体 | 世代/年 | 型 | 固有モジュール |
|---|---|---|---|---|
| MiG-21 バラライカ | chassis_1_light | 1 / 1995 | 軽 | 標準（密集戦） |
| Su-11 | chassis_1_light | 1 / 1995 | 軽 | 標準（初期迎撃） |
| MiG-23 チボラシュカ | chassis_2_light | 2 / 2005 | 軽 | engine_maneuver_2（可変翼格闘） |
| MiG-25 スピオトフォズ | chassis_2_heavy | 2 / 2005 | 重 | right_hand=support_gun（高速突撃・支援砲） |
| MiG-27 アリゲーター | chassis_2_light | 2 / 2005 | 軽 | right_hand=support_assault_cannon_2（対地） |
| MiG-29 ラーストチカ | chassis_2_light | 2 / 2005 | 軽 | left_hand=chain_sword（モーターブレード密集） |
| Su-27 ジュラーブリク | chassis_2_heavy | 2 / 2005 | 重 | left_hand=chain_sword + long_sword（ブレード多数近接） |
| MiG-31 フォックスハウンド | chassis_2_heavy | 2.5 / 2010 | 重 | +large_missile_2（超高速迎撃） |
| MiG-35 | chassis_3_maneuver | 3 / 2015 | 高機動 | +add_thruster_3（三次元ノズル） |
| Su-37 チェルミナートル | chassis_2_maneuver | 2.5 / 2010 | 高機動 | left_hand=chain_sword + add_thruster_2（推力偏向近接） |
| Su-47 ビェールクト | chassis_3_maneuver | 3 / 2015 | 高機動 | left_hand=chain_sword + add_thruster_3（究極近接機動） |
| Su-57 | chassis_4 | 4 / 2035 | 高機動 | OS_XM3 + armor_composite（ステルス） |

## 🇨🇳 中国（CHI）
| 戦術機 | 素体 | 世代/年 | 型 | 固有モジュール |
|---|---|---|---|---|
| 殲撃8型 J-8 | chassis_1_light | 1 / 1995 | 軽 | 標準（装甲ラウンドモニター） |
| 殲撃10型 J-10 | chassis_2_light | 2 / 2005 | 軽 | reactive_shield + long_sword（柳葉刀・F-16派生最高傑作） |
| 殲撃11型 J-11 | chassis_2_heavy | 2 / 2005 | 重 | 標準（Su-27派生・制空） |
| 殲撃10型 J-10X | chassis_3_light | 3 / 2015 | 軽 | engine_maneuver_3（近接高機動特化） |
| 殲撃20型 J-20 | chassis_3_maneuver | 3 / 2015 | 高機動 | OS_XM3 + armor_composite（ステルス） |

## 🇩🇪 ドイツ（GER）
| 戦術機 | 素体 | 世代/年 | 型 | 固有モジュール |
|---|---|---|---|---|
| EF-2000 タイフーン | chassis_3_heavy | 3 / 2015 | 重 | add_blade_armor + long_sword + OS_XM3（全身ブレード密集戦） |
| Me-101P フェンリル | chassis_4 | 4 / 2035 | 重 | OS_XM3（次世代） |

## 🇫🇷 フランス（FRA）
| 戦術機 | 素体 | 世代/年 | 型 | 固有モジュール |
|---|---|---|---|---|
| ミラージュ2000 | chassis_2_light | 2 / 2005 | 軽 | engine_cruise_2（軽量高出力・汎用） |
| ミラージュ2000 Mod | chassis_2_light | 2.5 / 2010 | 軽 | engine_cruise_2 + add_thruster_2（直進加速砲撃） |
| ラファール | chassis_3_maneuver | 3 / 2015 | 高機動 | OS_XM3 + add_blade_armor（多用途・タイフーン類似） |

## 🇬🇧 イギリス（ENG）
| 戦術機 | 素体 | 世代/年 | 型 | 固有モジュール |
|---|---|---|---|---|
| EF-2000 タイフーン | chassis_3_heavy | 3 / 2015 | 重 | add_blade_armor + long_sword + OS_XM3 |
| テンペスト | chassis_4 | 4 / 2035 | 高機動 | OS_XM3 + armor_composite（次世代ステルス） |

## 🇮🇹 イタリア（ITA）
| 戦術機 | 素体 | 世代/年 | 型 | 固有モジュール |
|---|---|---|---|---|
| EF-2000 タイフーン | chassis_3_heavy | 3 / 2015 | 重 | add_blade_armor + long_sword + OS_XM3 |

## 🇸🇪 スウェーデン（SWE）
| 戦術機 | 素体 | 世代/年 | 型 | 固有モジュール |
|---|---|---|---|---|
| JA-37 ビゲン | chassis_2_light | 2 / 2005 | 軽 | add_sensor_2（NOE匍匐飛行特化） |
| JAS-39 グリペン | chassis_3_light | 3 / 2015 | 軽 | add_sensor_3 + deta_link_3（地形追随・低コスト） |

## 🇮🇱 イスラエル（ISR）
| 戦術機 | 素体 | 世代/年 | 型 | 固有モジュール |
|---|---|---|---|---|
| クフィル | chassis_1_light | 1 / 1995 | 軽 | add_sensor_1（砂漠赤外線） |
| ラビ | chassis_2_light | 2 / 2005 | 軽 | reactive_shield（F-16独自改・J-10母体） |

---

## 攻撃機（参考・既存のasa/tsa系。variant化対象外）
| 機体 | 系統 |
|---|---|
| A-6J 海神 | asa（水陸両用強襲） |
| A-10J 凌鉄 | tsa（重火力対地・support_gun相当） |
| A-12 アヴェンジャー | （第3世代強襲・ステルス） |

---

## 実装方式（G）
1. 各機体を equipment variant 定義（archetype + parent素体 + 上記default_modules）
2. 各機体に研究サブテック（前提＝元世代framework＋使用モジュールのテック）
3. 国別hidden techで該当国のみ解放
4. priority高めで生産優先
5. loc（正式名）

**この設計でOKなら実装に入ります。修正点（型・素体・モジュール）があれば指摘してください。**
