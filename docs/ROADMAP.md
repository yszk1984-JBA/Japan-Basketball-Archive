# ROADMAP — Governance v1.0

日程は未設定。各段階の結果を確認して次の範囲を決める。

| 段階 | 内容 | 完了条件 |
| --- | --- | --- |
| 0：初期セットアップ | clone、ローカルプロジェクト登録、Governanceの7文書 | 差分・リンク・原則の整合性を確認し、commit・pushを確認 |
| 1：パイロット確認 | 福岡第一高校の既存Excelを確認 | 原本保全、シート・列・出典・不明点を整理し、v0.1への対応をYuichiと合意 |
| 2：候補と検証 | 合意した小規模範囲で取込と検証を実装 | CANDIDATE、QA記録、Python検証結果を作成。問題のあるデータを分離 |
| 3：人間の承認 | VERIFIEDをYuichiが確認 | 対象版・範囲の明示的承認を記録し、その範囲だけMASTERへ反映 |
| 4：サイト検討 | 公開範囲と表示方法を設計 | 出典表示、利用条件、公開対象、技術構成をYuichiと合意 |

現在は段階1のパイロット確認を進めている。公開画面を早期に検証するため、確認中の少数データを使うWebプロトタイプを並行して作成する。プロトタイプの表示データはVERIFIEDまたはMASTERを意味しない。data/raw、data/candidate、data/verified、data/master、scriptsは必要になる段階で作成する。

Person / Career / Organization / Sourceを超えるスキーマ拡張や大規模実装は、目的と影響を説明し、Yuichiと合意してから行う。
