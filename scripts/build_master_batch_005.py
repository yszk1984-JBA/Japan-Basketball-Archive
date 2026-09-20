#!/usr/bin/env python3
"""Apply the explicitly approved Batch 005 VERIFIED snapshot to MASTER."""

from __future__ import annotations

import csv
import subprocess
from pathlib import Path


VERIFIED = Path("data/verified/batch_005")
MASTER = Path("data/master")
VERIFIED_COMMIT = "7093141"
APPROVAL_ID = "APP-B005-20260921-01"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def ensure_approved_snapshot() -> None:
    tracked = [
        "person_verified.csv", "organization_verified.csv", "career_verified.csv",
        "source_references.csv", "evidence_records.csv", "held_fields.csv",
        "issue_dispositions.csv", "validation_report.md",
    ]
    result = subprocess.run(
        ["git", "diff", "--quiet", VERIFIED_COMMIT, "--", *[str(VERIFIED / name) for name in tracked]],
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit("Batch 005 VERIFIED snapshot differs from the approved commit")
    approval = (VERIFIED / "master_approval.md").read_text(encoding="utf-8")
    required = [APPROVAL_ID, VERIFIED_COMMIT, "> 承認します", "承認者：Yuichi"]
    if any(value not in approval for value in required):
        raise SystemExit("Master approval record is incomplete")


def merge(
    existing_path: Path,
    incoming: list[dict[str, str]],
    headers: list[str],
    key: str,
) -> list[dict[str, str]]:
    existing = read(existing_path) if existing_path.exists() else []
    found = {row[key]: row for row in existing}
    for row in incoming:
        identifier = row[key]
        if identifier in found and found[identifier] != row:
            raise SystemExit(f"MASTER conflict for {key}={identifier}")
        found[identifier] = row
    rows = [found[identifier] for identifier in sorted(found)]
    write(existing_path, headers, rows)
    return rows


def main() -> None:
    ensure_approved_snapshot()
    persons = merge(
        MASTER / "person.csv", read(VERIFIED / "person_verified.csv"),
        ["person_id", "name"], "person_id",
    )
    organizations = merge(
        MASTER / "organization.csv", read(VERIFIED / "organization_verified.csv"),
        ["organization_id", "name"], "organization_id",
    )
    careers = merge(
        MASTER / "career.csv", read(VERIFIED / "career_verified.csv"),
        ["career_id", "person_id", "organization_id", "role", "start", "end"], "career_id",
    )
    sources = merge(
        MASTER / "source.csv", read(VERIFIED / "source_references.csv"),
        ["source_id", "title", "publisher", "url", "accessed_at"], "source_id",
    )
    evidence = merge(
        MASTER / "evidence.csv", read(VERIFIED / "evidence_records.csv"),
        ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id", "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"],
        "record_id",
    )
    approval_rows = [{
        "approval_id": APPROVAL_ID,
        "batch": "Batch 005 Wave 1",
        "verified_commit": VERIFIED_COMMIT,
        "approved_scope": "B5W1D0001-B5W1D0026 eligible_fields",
        "excluded_scope": "held_fields 9件・HOLD Issue 9件",
        "approved_by": "Yuichi",
        "approved_at": "2026-09-21",
        "approval_reference": "data/verified/batch_005/master_approval.md",
    }]
    approvals = merge(
        MASTER / "approval_records.csv", approval_rows,
        ["approval_id", "batch", "verified_commit", "approved_scope", "excluded_scope", "approved_by", "approved_at", "approval_reference"],
        "approval_id",
    )

    report = f"""# MASTER反映レポート

作成日：2026-09-21

## 今回の反映

- Approval ID：`{APPROVAL_ID}`
- VERIFIED基準commit：`{VERIFIED_COMMIT}`
- Batch：Batch 005 Wave 1
- 範囲：全26 Decisionの`eligible_fields`
- 除外：9件の`held_fields`、9件のHOLD Issue

## MASTER件数

- Person：{len(persons)}件
- Organization：{len(organizations)}件
- Career：{len(careers)}件
- Source：{len(sources)}件
- Evidence：{len(evidence)}件
- Approval：{len(approvals)}件

公開サイトへの反映は行っていない。
"""
    (MASTER / "master_build_report.md").write_text(report, encoding="utf-8")

    readme = """# MASTER DATA

このディレクトリには、Yuichiが対象版と範囲を明示的に承認したデータだけを格納する。

## 現在の内容

- Batch 005 Wave 1
- Approval ID：`APP-B005-20260921-01`
- VERIFIED基準commit：`7093141`
- HOLD項目・HOLD Issue：含まない
- 公開サイト反映：未実施

## ファイル

- `person.csv`
- `organization.csv`
- `career.csv`
- `source.csv`
- `evidence.csv`
- `approval_records.csv`
- `master_build_report.md`
- `validation_report.md`

Masterへの追加・訂正は、CANDIDATEから同じGovernance工程を通し、承認済み範囲だけを反映する。
"""
    (MASTER / "README.md").write_text(readme, encoding="utf-8")


if __name__ == "__main__":
    main()
