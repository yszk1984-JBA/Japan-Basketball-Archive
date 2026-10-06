#!/usr/bin/env python3
"""Validate Organization Current Names 001 candidate structure."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import read_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "organization_current_names_001"

ALLOWED_CHANGE_TYPES = {"NAME_CHANGE", "SCHOOL_MERGER"}
ALLOWED_PRECISION = {"day", "month", "year"}


def main() -> int:
    errors: list[str] = []
    rows = read_csv(BASE / "current_name_candidates.csv")
    sources = read_csv(BASE / "source_references.csv")
    master_orgs = {row["organization_id"]: row["name"] for row in read_csv(ROOT / "data" / "master" / "organization.csv")}
    source_ids = {row["source_id"] for row in sources}

    if len({row["current_name_id"] for row in rows}) != len(rows):
        errors.append("current_name_idが重複")
    if len({row["organization_id"] for row in rows}) != len(rows):
        errors.append("同じorganization_idに複数の候補がある")
    if len(source_ids) != len(sources):
        errors.append("source_idが重複")

    for row in rows:
        rid = row["current_name_id"]
        org_id = row["organization_id"]
        if org_id not in master_orgs:
            errors.append(f"{rid}: organization_idがMasterに存在しない（{org_id}）")
        elif master_orgs[org_id] != row["recorded_name"]:
            errors.append(f"{rid}: recorded_nameがMasterの名称と一致しない（{row['recorded_name']} / {master_orgs[org_id]}）")
        if row["current_name"] == row["recorded_name"] or not row["current_name"]:
            errors.append(f"{rid}: current_nameが空、または登録名と同じ")
        if row["current_name"] in master_orgs.values():
            errors.append(f"{rid}: current_nameが別のOrganizationとして既に登録されている（統合の検討が必要）")
        if row["change_type"] not in ALLOWED_CHANGE_TYPES:
            errors.append(f"{rid}: change_typeが不正（{row['change_type']}）")
        if row["effective_date_precision"] not in ALLOWED_PRECISION:
            errors.append(f"{rid}: effective_date_precisionが不正")
        if row["source_id"] not in source_ids:
            errors.append(f"{rid}: source_id参照が不足")
        if not row["source_locator"]:
            errors.append(f"{rid}: source_locatorが不足")
        if row["assessment"] not in {"SUPPORTED", "PARTIAL"}:
            errors.append(f"{rid}: assessmentが不正")

    report = [
        "# Organization Current Names 001 検証レポート", "", "作成日：2026-10-06", "",
        "## 結果", "", f"- 検証：{'PASS' if not errors else 'FAIL'}",
        f"- エラー：{len(errors)}件",
        f"- 現在名の候補：{len(rows)}件",
        f"- Source：{len(sources)}件",
        "- 中心スキーマ（Person/Organization/Career/Source）・Master・公開サイト：未変更",
        "- VERIFIED・HUMAN APPROVAL・MASTER反映・公開表示：未実施（Yuichiの承認待ち）",
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
