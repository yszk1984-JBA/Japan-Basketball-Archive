# 古野拓巳 追加調査レビュー

確認日：2026-09-19

## 確認結果

全日本大学バスケットボール連盟（JUBF）の公式資料から、次を確認した。

- 第17回日本男子学生選抜大会の選手プロフィールに「古野 拓巳」「SG」「180cm」「3年」「日本経済大」「福岡第一高」と掲載されている。
- 第18回大会の公式結果に「古野 拓巳」「九州」「No.10」「4年」と掲載されている。

このため、日本経済大学での選手Career `C000076`をCANDIDATEへ追加した。福岡第一高校については出身校関係だけを採用し、高校バスケットボール部での役割と期間はHOLDを維持した。

## 項目別の扱い

| Career | 採用候補 | HOLD |
| --- | --- | --- |
| 福岡第一高校 `C000210` | `organization_id` | `role`、`start`、`end` |
| 日本経済大学 `C000076` | `organization_id`、`role`、`grade`、`jersey_number`、`position`、`height_cm` | `start`、`end` |

大学3年・4年の記録から入学年や卒業年を逆算していない。JUBF資料は競技参加を示すが、学籍上の入学・卒業年月を直接証明しないためである。

## Source

- [第17回日本男子学生選抜バスケットボール大会 選手プロフィール](https://jubf.jp/news/download/nc/79/fc/4/url/6YG45oqc5aSn5LyaIOeUt%2BWtkOODoeODs%2BODkOODvOihqFwucGRm) — PDF 8ページ、九州選抜 No.1
- [第18回日本男子学生選抜バスケットボール大会 大会結果](https://jubf.jp/news/download/nc/107/fc/1/url/55S35a2QMTjlm57pgbjmipzlpKfkvJrjgIDlpKfkvJrntZDmnpwucGRm) — REBOUND TOP10、九州 No.10

## Governance上の扱い

この結果はCANDIDATEと項目別QAであり、VERIFIED、HUMAN APPROVAL、MASTERではない。原本Excel、データ設計v0.1、公開サイトの正式データは変更していない。
