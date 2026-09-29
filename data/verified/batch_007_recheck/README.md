# Batch 007（全Wave統合）VERIFIED

作成日：2026-09-30

状態：VERIFIED候補、HUMAN APPROVAL・MASTER未実施

batch_007は後続Wave（04・04b・08・10・11）が前のWaveの人物・Careerに項目・判断を追加する構成のため、全Waveをまとめて1つのVERIFIEDにした（`scripts/build_verified_batch_032.py`の`build_batch_007_merged`）。

- CANDIDATE・QA基準commit：`fa5bb78`（全Wave変更なしを確認）
- 採用：最新の判断がREADYで、そのREADY判断（最後のHOLD・REJECT以降）が対象とし、かつSUPPORTED Evidenceがある項目
- 除外：REJECT_CANDIDATE・HOLD_CANDIDATEの人物・Career、値の食い違う項目（`held_fields.csv`）、全Issue
- Person 26件、Career 124件、Organization 70件、Evidence 486件、除外記録 33件、HOLD Issue 59件
- 検証：PASS（エラー0件）


VERIFIEDはHuman ApprovalまたはMasterを意味しない。
