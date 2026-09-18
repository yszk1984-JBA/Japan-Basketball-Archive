# 福岡第一高校パイロットExcel 初回監査

確認日：2026-09-18  
対象：`Japan_Basketball_Archive_Phase2_WinterCup2020_FullStats_v0.22.xlsx`  
対象SHA-256：`609ce5d321aa6bd865c040277225b7ea69eb8861028178cfc004e1fde48b3765`

## この監査の位置づけ

Governance v1.0に基づき、対象Excelを読み取り専用で確認した。原本の変更、候補データへの取込、データ設計の拡張、VERIFIED判定、Master確定は行っていない。

Excel内の`Confirmed`、`Fixed`、`Full Team`等は原本に記載されたラベルまたは計算結果であり、Governance v1.0上のVERIFIED、HUMAN APPROVAL、MASTERを意味しない。

## 原本の状態

| 項目 | 確認結果 |
| --- | --- |
| ファイル形式 | Excel Workbook（`.xlsx`） |
| ファイルサイズ | 196,241 bytes |
| シート数 | 21 |
| 数式 | `Phase2Validation`に28セル |
| コメント | 0セル |
| 外部ハイパーリンク | セルのハイパーリンク設定は0件。URLはSource等の通常セルに記録 |
| 原本変更 | なし |

## シートの整理

### データ設計v0.1の中心

| シート | データ行数 | 主な内容 | v0.1との関係 |
| --- | ---: | --- | --- |
| Person | 55 | 人物ID、氏名、生年月日、身体情報等 | Personに対応 |
| Career | 203 | 人物と組織の関係、役割、期間等 | Careerに対応 |
| Organization | 84 | 学校、クラブ、大学等 | Organizationに対応 |
| Source | 64 | 資料名、発行元、URL、確認日等 | Sourceに対応 |
| Evidence | 41 | 対象ID・対象項目と出典の対応 | v0.1が求める項目別の根拠記録候補 |
| Season | 14 | 年度・シーズン | 補助データ。v0.1中心4表の外側 |

上記件数には入力例が含まれる。たとえばPerson、Career、Organization、Sourceの先頭には`Example`のサンプル行があるため、件数をそのまま実在データ件数として扱わない。

### 大会・試合の試験データ

| シート | データ行数 | 主な内容 | 扱い |
| --- | ---: | --- | --- |
| Competition | 1 | 大会 | 将来候補 |
| CompetitionTeam | 5 | 大会ごとの参加チーム | 将来候補 |
| CompetitionRoster | 15 | 大会ロスター | 将来候補 |
| Game | 4 | 試合 | 将来候補 |
| PlayerGameStats | 60 | 4試合×15人の個人成績 | 将来候補 |
| Phase2Validation | 4試合分の数式ほか | 得点一致・接続確認 | QA補助。中心データではない |

`Phase2Validation`の保存済み計算結果では、4試合ともチーム得点と選手得点合計が一致し、各試合15行になっている。ただし、今回は数式を再計算しておらず、この一致だけで史実の正しさやVERIFIEDを判定しない。

### 設計検討・テスト用シート

`README`、`Phase1_Review`、`OrganizationAlias`、`DataDictionary`、`SchoolCrossTest`、`JuniorHighTrace`、`YouthPathTest`、`ElementaryMiniBasket`、`MiniBasketCareerTest`がある。これらには設計判断やテスト結果が含まれるが、Governance v1.0採用後の正式なスキーマ決定またはMaster承認記録とは扱わない。

## 列の対応

### Person

v0.1の必須候補である`person_id`と`name`は、Excelでは`person_id`と`full_name_ja`を中心に表現できる。姓、名、英語名、旧名、生年月日、出生地、身体情報、ポジション、国籍等の追加列がある。

Person行には`source_id`がない。根拠はEvidenceで別管理する設計と見られるが、PersonのEvidenceは25件で、そのうち1件は存在しない人物IDを参照している。現在存在するPerson 55行のうち、Personを対象にしたEvidenceがあるのは24人物であり、全人物・全項目を追跡できる状態ではない。

### Career

v0.1の`career_id`、`person_id`、`organization_id`、`role`、`start`、`end`は、Excelの`career_id`、`person_id`、`organization_id`、`role`、`start_year`、`end_year`に対応できる。

`season_id`、`category`、`position`、`jersey_number`、`career_status`、`confidence`等の追加列がある。さらに`registration_type`、`date_precision`、`inferred_flag`、`contract_owner_org_id`、`movement_type`が追加されているが、これらはデータ設計v0.1には未採用である。今回の監査では拡張案としても確定しない。

203行のうち、開始年が空欄の行は79件、終了年が空欄の行は64件ある。空欄を現在所属や特定年に自動変換してはならない。

### Organization

v0.1の`organization_id`と`name`は、Excelの`organization_id`と`organization_name_ja`に対応できる。英語名、種別、親組織、所在地、設立年、活動状況、公式URL等の追加列がある。

各行に`source_id`はあるが、1件の出典が行内の全項目を裏付けるとは限らない。Organizationを対象にしたEvidenceは0件であり、項目別の根拠位置は不足している。

### Source

v0.1の`source_id`、`title`、`publisher`、`url`、`accessed_at`は、Excelの`source_id`、`title`、`publisher`、`url`、`accessed_date`に対応できる。64行すべてにタイトル、発行元、URL、確認日、信頼性ラベルがある。公開日は39件が空欄であるが、不明値として保持できる。

資料内の具体的なページ、表、段落等の位置はSource単体では十分に表現されず、Evidenceの`evidence_statement`や備考に混在している。再現可能な確認には、位置情報の記録方法を取込前に決める必要がある。

## 確認できた不整合と注意点

### 1. 存在しない人物IDへの参照

Careerの2行とEvidenceの1行が`P000027`を参照しているが、Personに`P000027`が存在しない。

- `C000027`：福岡第一高校、2021年終了
- `C000045`：2021年開始の留学候補、留学先組織は未特定
- `EV000027`：原文上は「ウッズジェリオ 翔」に関する根拠

同名人物を推測してPersonを自動作成せず、CANDIDATE段階で人物候補と表記を確認する必要がある。

初回の候補整理は[PILOT_CANDIDATE_P000027](PILOT_CANDIDATE_P000027.md)に記録した。

### 2. Excelテーブル範囲から外れたデータ

CareerのExcelテーブルは`A4:N104`だが、入力は213行目まであり、後半データがテーブル範囲外にある。また追加列`O:S`もテーブル外である。

Gameはテーブル`A:N`に対して追加列`O:R`、PlayerGameStatsはテーブル`A:Y`に対して追加列`Z:AB`がある。Excelのテーブル機能を前提に抽出すると、行または列を取りこぼす危険がある。

### 3. 出典URLの確認

パス内に`%3D`を含む10件は、2026-09-18の確認で公開ページへ到達し、タイトルも一致した。この表記だけを理由に修正しない。`SRC000023`はHTTPからHTTPSへ転送されるが、今回の取得環境では転送先が502となり本文を確認できなかったため、ブラウザまたはアーカイブでの再確認候補とする。詳細は[PILOT_SOURCE_URL_REVIEW](PILOT_SOURCE_URL_REVIEW.md)に記録した。

同一URLを使うSourceが1組ある。複数の事実に同じ資料を使うこと自体は問題ではないが、Sourceを分ける必要があるか、同一Sourceへ統合するかは取込設計時の判断事項である。

### 4. 項目別出典が不足

CareerとOrganizationには行単位の`source_id`がある一方、SCHEMA v0.1は「どの項目を資料のどの位置が裏付けるか」を求めている。Evidenceは41件あるが、全行・全項目を覆っていない。特にOrganizationの項目別Evidenceはない。

### 5. 原本内ラベルとGovernance段階が異なる

Careerでは原本上`Confirmed`が181件、`Likely`が19件、入力例が3件ある。Organization、試合、成績にも`Confirmed`がある。これらは既存Excelの確度ラベルであり、Governance v1.0のQAまたはVERIFIEDへ自動対応させない。

## データ設計v0.1への対応案

現時点では次の小さい範囲が安全である。

1. Person、Organization、Career、Sourceの4表だけを取込候補の対象とする。
2. Evidenceは中心表にせず、項目と出典位置を結ぶ付随記録の候補として整理する。
3. Season、大会、試合、成績、組織別名等は将来候補として保留する。
4. Excelの`Confirmed`等を新しい処理段階へ変換せず、すべてCANDIDATEから開始する。
5. `P000027`、`SRC000023`、項目別出典不足を解決してからQAへ進める。
6. Personの氏名分割、Organizationの追加属性、Careerの追加列は、値を捨てずに候補として保管する方法を別途検討する。v0.1の正式拡張はYuichiとの合意後に行う。

## 次の受入条件

次工程を「取込設計の準備完了」とする条件は次のとおり。

- `P000027`の人物候補と表記を原資料で確認し、未解決なら保留理由を記録する。
- 取込対象を中心4表に限定するか、追加列の保存方法をYuichiと合意する。
- 項目別の出典位置を記録する最小形式を決める。
- 入力例を実データから除外する規則を決める。
- 原本のハッシュとファイル名をRAW参照として保持する。

これらが終わるまでは、データ取込、Schema拡張、VERIFIED化、Master反映を行わない。
