#!/usr/bin/env python3
"""Validate the small Fukuoka Daiichi candidate batch.

Structural QA only. Passing does not mean VERIFIED or MASTER approval.
"""

from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path


REQUIRED_FILES = {
    "person_candidates.csv": ["person_id", "name"],
    "organization_candidates.csv": ["organization_id", "name"],
    "career_candidates.csv": [
        "career_id",
        "person_id",
        "organization_id",
        "role",
        "start",
        "end",
    ],
    "source_references.csv": [
        "source_id",
        "title",
        "publisher",
        "url",
        "accessed_at",
    ],
    "evidence_records.csv": [
        "record_id",
        "entity_type",
        "entity_id",
        "field_name",
        "candidate_value",
        "source_id",
        "source_locator",
        "evidence_summary",
        "assessment",
        "checked_at",
        "issue_note",
    ],
    "issues.csv": [
        "issue_id",
        "person_id",
        "related_id",
        "issue_type",
        "status",
        "description",
        "next_check",
    ],
}

ALLOWED_ASSESSMENTS = {"SUPPORTED", "PARTIAL", "CONFLICT", "UNVERIFIED"}
ALLOWED_ENTITY_TYPES = {"Person", "Career", "Organization"}


def read_csv(path: Path, expected_headers: list[str]) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != expected_headers:
            raise ValueError(
                f"{path.name}: headers differ: {reader.fieldnames!r}"
            )
        return list(reader)


def duplicates(values: list[str]) -> list[str]:
    return sorted(key for key, count in Counter(values).items() if key and count > 1)


def main() -> int:
    batch_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
        "data/candidate/pilot_batch_001"
    )
    errors: list[str] = []
    loaded: dict[str, list[dict[str, str]]] = {}

    for filename, headers in REQUIRED_FILES.items():
        path = batch_dir / filename
        if not path.exists():
            errors.append(f"missing file: {filename}")
            continue
        try:
            loaded[filename] = read_csv(path, headers)
        except ValueError as exc:
            errors.append(str(exc))

    if errors:
        return write_report(batch_dir, loaded, errors)

    persons = loaded["person_candidates.csv"]
    organizations = loaded["organization_candidates.csv"]
    careers = loaded["career_candidates.csv"]
    sources = loaded["source_references.csv"]
    evidence = loaded["evidence_records.csv"]
    issues = loaded["issues.csv"]

    key_specs = [
        ("Person", persons, "person_id"),
        ("Organization", organizations, "organization_id"),
        ("Career", careers, "career_id"),
        ("Source", sources, "source_id"),
        ("Evidence", evidence, "record_id"),
        ("Issue", issues, "issue_id"),
    ]
    for label, rows, key in key_specs:
        blank = [index + 2 for index, row in enumerate(rows) if not row[key].strip()]
        dup = duplicates([row[key].strip() for row in rows])
        if blank:
            errors.append(f"{label}: blank {key} at CSV rows {blank}")
        if dup:
            errors.append(f"{label}: duplicate {key}: {dup}")

    person_ids = {row["person_id"] for row in persons}
    organization_ids = {row["organization_id"] for row in organizations}
    career_ids = {row["career_id"] for row in careers}
    source_ids = {row["source_id"] for row in sources}

    for index, row in enumerate(persons, start=2):
        if not row["name"].strip():
            errors.append(f"Person row {index}: name is blank")

    for index, row in enumerate(organizations, start=2):
        if not row["name"].strip():
            errors.append(f"Organization row {index}: name is blank")

    for index, row in enumerate(careers, start=2):
        if row["person_id"] not in person_ids:
            errors.append(
                f"Career row {index}: missing person {row['person_id']}"
            )
        if row["organization_id"] not in organization_ids:
            errors.append(
                f"Career row {index}: missing organization {row['organization_id']}"
            )
        if not row["role"].strip():
            errors.append(f"Career row {index}: role is blank")
        if row["start"] and row["end"] and int(row["start"]) > int(row["end"]):
            errors.append(f"Career row {index}: start is after end")

    entity_ids = {
        "Person": person_ids,
        "Career": career_ids,
        "Organization": organization_ids,
    }
    for index, row in enumerate(evidence, start=2):
        entity_type = row["entity_type"]
        if entity_type not in ALLOWED_ENTITY_TYPES:
            errors.append(
                f"Evidence row {index}: invalid entity_type {entity_type}"
            )
        elif row["entity_id"] not in entity_ids[entity_type]:
            errors.append(
                f"Evidence row {index}: missing {entity_type} {row['entity_id']}"
            )
        if row["source_id"] not in source_ids:
            errors.append(
                f"Evidence row {index}: missing source {row['source_id']}"
            )
        if not row["field_name"].strip():
            errors.append(f"Evidence row {index}: field_name is blank")
        if not row["source_locator"].strip():
            errors.append(f"Evidence row {index}: source_locator is blank")
        if not row["evidence_summary"].strip():
            errors.append(f"Evidence row {index}: evidence_summary is blank")
        if row["assessment"] not in ALLOWED_ASSESSMENTS:
            errors.append(
                f"Evidence row {index}: invalid assessment {row['assessment']}"
            )
        if not row["checked_at"].strip():
            errors.append(f"Evidence row {index}: checked_at is blank")

    return write_report(batch_dir, loaded, errors)


def write_report(
    batch_dir: Path,
    loaded: dict[str, list[dict[str, str]]],
    errors: list[str],
) -> int:
    counts = {name: len(rows) for name, rows in loaded.items()}
    issue_rows = loaded.get("issues.csv", [])
    open_issues = sum(row.get("status") in {"OPEN", "HOLD"} for row in issue_rows)
    lines = [
        "# Pilot Batch 001 QA Report",
        "",
        "この検査は構造QAであり、史実の正しさ、VERIFIED、HUMAN APPROVAL、MASTERを意味しない。",
        "",
        "## 結果",
        "",
        f"- 構造検査：{'PASS' if not errors else 'FAIL'}",
        f"- エラー：{len(errors)}件",
        f"- 未解決事項：{open_issues}件",
        "",
        "## 件数",
        "",
    ]
    for filename in REQUIRED_FILES:
        lines.append(f"- `{filename}`：{counts.get(filename, 0)}行")
    lines.extend(["", "## エラー", ""])
    if errors:
        lines.extend(f"- {error}" for error in errors)
    else:
        lines.append("- なし")
    lines.extend(
        [
            "",
            "## 解釈",
            "",
            "PASSはID、参照、必須項目、assessment値の形式が今回の規則に合うことだけを示す。",
            "`issues.csv`のOPEN/HOLDは解決しておらず、人間確認なしに候補値を昇格させない。",
            "",
        ]
    )
    (batch_dir / "qa_report.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines[:8]))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
