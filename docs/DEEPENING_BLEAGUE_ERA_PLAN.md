# 深掘り計画：B.LEAGUE期の過去所属クラブ（Master既存選手）

作成日：2026-09-29

状態：計画。Yuichiの指示（2026-09-29「深堀からお願いします」）を受けて作成。データの追加はまだ行っていない。

## 目的

Master登録済みの選手について、B.LEAGUE公式プロフィールの「クラブ所属履歴」（2016-17シーズン以降）に載っている**現所属より前のプロクラブ**をCareerとして追加する。各WaveでPRO_HISTORY_GAPS issueとして記録してきた内容を、正式な候補データにする。

## 対象

- Master 166名のうち、B.LEAGUE公式のPlayerIDがMasterのSourceから特定できる**155名**（一覧：`docs/DEEPENING_BLEAGUE_ERA_TARGETS.csv`）。
- PlayerIDがない11名（大学在学中の選手等）は対象外。
- P000082はPlayerIDが2つ（49711・51000138）記録されている。着手時に両方を確認し、公式サイト側の紐付けを判断する（人物同定の論点としてTier 2扱い）。
- B.LEAGUE開幕前（NBL・bjリーグ等）の経歴、在学期間は今回の対象外（別の深掘り）。

## 登録ルール

1. **出典**：B.LEAGUE公式の選手プロフィール（`roster_detail`）の「クラブ所属履歴」のみ。ブラウザで実ページから読み取る（要約型Web取得ツールは使わない）。
2. **Careerの単位**：同じクラブに連続して在籍した期間を1件とする。一度離れて戻った場合は別のCareerにする。
3. **期間の表し方**：既存の深掘り（batch_007 wave_08）と同じく、`start`＝最初のシーズンの開始年、`end`＝最後のシーズンの終了年（例：2016-17〜2020-21 → start 2016 / end 2021）。
4. **同一シーズンに2クラブ**（シーズン途中の移籍）：両方をCareerにし、どちらもそのシーズンの年を使う。移籍の時期・理由は記録しない。
5. **現所属のCareer**：既存のMaster Careerはそのまま。追加するのは現所属より前の在籍だけ。
6. **クラブ名**：所属履歴は略称（例：SR渋谷、千葉J、A東京）なので、B.LEAGUE公式のクラブ一覧・クラブページで正式名称を確認してから既存Organizationに対応付ける。対応付けできない略称はHOLDにする。
7. **改称**：栃木→宇都宮ブレックスのように同一クラブと確認済みのものは、batch_010の前例どおり同じOrganizationにする（ORG_NAME_HISTORY issue）。未確認の改称・同名別クラブはHOLD。
8. **空白のシーズン**：理由を推測しない（CAREER_TIMELINE_NOTEとして記録）。

## データの置き場所

`docs/HISTORICAL_CAREER_DEEPENING_LOG.md`の運用ルールどおり、深掘りWaveは**対象選手の元の登録Batch**に追加する（例：batch_019の選手はbatch_019/wave_03）。横断的な進捗は同ログに記録する。

## 承認

深掘りで追加したCareerは、CANDIDATE → QA → VERIFIED → Approval Sprint 008 → Masterの順で扱う。Approval Sprint 008から2段階承認（`docs/APPROVAL_TIERING_PROPOSAL_V0.1.md`）を試行する。改称・同名クラブ・PlayerIDの不整合を含む選手はTier 2になる。

## 進め方

1. B.LEAGUE公式のクラブ略称 → 正式名称の対応表を作る（2016-17以降の全クラブ）。
2. 155名の所属履歴をブラウザでまとめて読み取る。
3. 元Batchごとに深掘りWaveを生成し、検証スクリプトで確認する。
4. VERIFIED化とApproval Sprint 008の資料作成。

## 前提

手順1〜2はYuichiのMac上のブラウザ（Claudeのブラウザ）で行う。Macが接続されていないと着手できない。
