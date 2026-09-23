#!/usr/bin/env python3
"""Validate Organization Succession Pilot 001 candidate structure."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import read_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "organization_succession_pilot_001"

ALLOWED_REASONS = {"NAME_CHANGE"}  # 2026-09-23時点でYuichiが合意した範囲：名称変更のみ
ALLOWED_PRECISION = {"day", "month", "year", "season"}


def main() -> int:
    errors: list[str] = []

    successions = read_csv(BASE / "organization_succession_candidates.csv")
    sources = read_csv(BASE / "source_references.csv")

    all_org_ids: set[str] = {row["organization_id"] for row in read_csv(ROOT / "data" / "master" / "organization.csv")}
    for f in sorted((ROOT / "data" / "candidate").glob("batch_*/wave_*/organization_candidates.csv")):
        for row in read_csv(f):
            all_org_ids.add(row["organization_id"])

    source_ids = {row["source_id"] for row in sources}

    if len({row["succession_id"] for row in successions}) != len(successions):
        errors.append("succession_idが重複")
    if len({row["source_id"] for row in sources}) != len(sources):
        errors.append("source_idが重複")

    for row in successions:
        if row["predecessor_organization_id"] not in all_org_ids:
            errors.append(f"{row['succession_id']}: predecessor_organization_id参照が不足（{row['predecessor_organization_id']}）")
        if row["successor_organization_id"] not in all_org_ids:
            errors.append(f"{row['succession_id']}: successor_organization_id参照が不足（{row['successor_organization_id']}）")
        if row["predecessor_organization_id"] == row["successor_organization_id"]:
            errors.append(f"{row['succession_id']}: predecessorとsuccessorが同一ID")
        if row["reason"] not in ALLOWED_REASONS:
            errors.append(f"{row['succession_id']}: reasonが対象範囲外（{row['reason']}、現状はNAME_CHANGEのみ許可）")
        if row["effective_date_precision"] not in ALLOWED_PRECISION:
            errors.append(f"{row['succession_id']}: effective_date_precisionが不正（{row['effective_date_precision']}）")
        if row["source_id"] not in source_ids:
            errors.append(f"{row['succession_id']}: source_id参照が不足")
        if row["assessment"] not in {"SUPPORTED", "PARTIAL"}:
            errors.append(f"{row['succession_id']}: assessmentが不正")
        if not row["source_locator"]:
            errors.append(f"{row['succession_id']}: source_locatorが不足")

    report = [
        "# Organization Succession Pilot 001 検証レポート", "", "作成日：2026-09-23", "",
        "## 結果", "", f"- 検証：{'PASS' if not errors else 'FAIL'}",
        f"- エラー：{len(errors)}件",
        f"- Succession候補：{len(successions)}件",
        f"- Source：{len(sources)}件",
        "- 中心スキーマ（Person/Organization/Career/Source）・Master・公開サイト：未変更",
        "- スキーマ採用・VERIFIED・HUMAN APPROVAL・MASTER反映：未実施（Yuichiの最終承認待ち）",
        "", "## エラー", "",
    ]
    report.extend(f"- {error}" for error in errors)
    if not errors:
        report.append("- なし")
    (BASE / "validation_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
