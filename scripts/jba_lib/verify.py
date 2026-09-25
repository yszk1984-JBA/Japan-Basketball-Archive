"""Generic CANDIDATE -> VERIFIED promotion, shared by many batch/wave pairs.

Mirrors the hand-written build_batch_006_wave_02_verified.py /
validate_batch_006_wave_02_verified.py exactly (same field selection,
same held-field handling, same issue disposition), but parameterized
so a single driver script can process many waves without copy-pasting
a near-identical script per wave. This module never writes to
data/master/*.csv or data/verified/approval_sprint_*/ -- it only ever
produces VERIFIED candidates, which are not yet Human Approval or
Master data (Governance v1.0: RAW -> CANDIDATE -> QA -> VERIFIED ->
HUMAN APPROVAL -> MASTER, no stage skipped).
"""

from __future__ import annotations

import csv
import subprocess
from collections import defaultdict
from pathlib import Path


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _write(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _unique(rows: list[dict[str, str]], key: str, fields: list[str]) -> list[dict[str, str]]:
    found: dict[str, dict[str, str]] = {}
    for row in rows:
        compact = {field: row[field] for field in [key, *fields]}
        if row[key] in found and found[row[key]] != compact:
            raise SystemExit(f"conflicting duplicate {row[key]}")
        found[row[key]] = compact
    return list(found.values())


def unchanged_since_review(root: Path, wave_dir: Path, source_commit: str) -> None:
    paths = [str(path.relative_to(root)) for path in sorted(wave_dir.glob("*.csv"))]
    result = subprocess.run(
        ["git", "diff", "--quiet", source_commit, "--", *paths],
        cwd=root,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(f"{wave_dir}: candidate snapshot changed after QA (commit {source_commit})")


def build_verified(root: Path, wave_dir: Path, output_dir: Path, source_commit: str,
                    created_at: str, label: str) -> dict[str, int]:
    """Promote one CANDIDATE wave's READY-decision fields to VERIFIED.

    Returns a dict of counts for the caller to report/aggregate.
    """
    unchanged_since_review(root, wave_dir, source_commit)

    decisions = _read(wave_dir / "qa_decisions.csv")
    ready = [row for row in decisions if row["decision"] == "READY_FOR_VERIFIED_REVIEW"]
    holds = [row for row in decisions if row["decision"] == "HOLD_CANDIDATE"]
    issues = _read(wave_dir / "issues.csv")

    eligible: dict[tuple[str, str], set[str]] = defaultdict(set)
    held_rows: list[dict[str, str]] = []
    for row in ready:
        target = (row["entity_type"], row["entity_id"])
        eligible[target].update(filter(None, row["eligible_fields"].split("|")))
        if row["held_fields"]:
            held_rows.append({
                "decision_id": row["decision_id"],
                "entity_type": row["entity_type"],
                "entity_id": row["entity_id"],
                "held_fields": row["held_fields"],
                "reason": "READY判断内の未確認項目としてVERIFIEDから除外",
            })
    for row in holds:
        held_fields = "|".join(dict.fromkeys(filter(None, [
            *row["eligible_fields"].split("|"), *row["held_fields"].split("|"),
        ])))
        held_rows.append({
            "decision_id": row["decision_id"],
            "entity_type": row["entity_type"],
            "entity_id": row["entity_id"],
            "held_fields": held_fields,
            "reason": "HOLD_CANDIDATE判断のためEntity全体をVERIFIEDから除外",
        })

    persons = _unique(_read(wave_dir / "person_candidates.csv"), "person_id", ["name"])
    organizations = _unique(_read(wave_dir / "organization_candidates.csv"), "organization_id", ["name"])
    careers = _unique(
        _read(wave_dir / "career_candidates.csv"), "career_id",
        ["person_id", "organization_id", "role", "start", "end"],
    )
    sources = _unique(
        _read(wave_dir / "source_references.csv"), "source_id",
        ["title", "publisher", "url", "accessed_at"],
    )
    evidence = _read(wave_dir / "evidence_records.csv")

    verified_evidence = [
        row for row in evidence
        if row["assessment"] == "SUPPORTED"
        and row["field_name"] in eligible[(row["entity_type"], row["entity_id"])]
    ]
    used_source_ids = {row["source_id"] for row in verified_evidence}
    verified_sources = [row for row in sources if row["source_id"] in used_source_ids]
    verified_persons = [row for row in persons if "name" in eligible[("Person", row["person_id"])]]
    verified_careers: list[dict[str, str]] = []
    for row in careers:
        allowed = eligible[("Career", row["career_id"])]
        if "organization_id" not in allowed:
            continue
        verified_careers.append({
            "career_id": row["career_id"],
            "person_id": row["person_id"],
            "organization_id": row["organization_id"],
            "role": row["role"] if "role" in allowed else "",
            "start": row["start"] if "start" in allowed else "",
            "end": row["end"] if "end" in allowed else "",
        })
    # Organizations: some batches (006-era) carry an explicit per-Organization
    # QA decision; later batches (007+, jba_lib era) do not -- an Organization
    # candidate there is implicitly confirmed by being referenced from a
    # READY Career (its name was itself part of that Career's SUPPORTED
    # evidence). So an Organization is eligible if EITHER it has its own
    # explicit "name" decision, OR it is referenced by a Career that made it
    # into verified_careers.
    used_org_ids = {row["organization_id"] for row in verified_careers}
    verified_organizations = [
        row for row in organizations
        if "name" in eligible[("Organization", row["organization_id"])]
        or row["organization_id"] in used_org_ids
    ]

    issue_dispositions = [{
        "issue_id": row["issue_id"],
        "person_id": row["person_id"],
        "related_id": row["related_id"],
        "issue_type": row["issue_type"],
        "status": "HOLD",
        "description": row["description"],
        "disposition": "VERIFIEDへ含めず、追加の公式資料が得られるまで保留",
    } for row in issues]

    _write(output_dir / "person_verified.csv", ["person_id", "name"], verified_persons)
    _write(output_dir / "organization_verified.csv", ["organization_id", "name"], verified_organizations)
    _write(output_dir / "career_verified.csv",
           ["career_id", "person_id", "organization_id", "role", "start", "end"], verified_careers)
    _write(output_dir / "source_references.csv",
           ["source_id", "title", "publisher", "url", "accessed_at"], verified_sources)
    _write(output_dir / "evidence_records.csv", [
        "record_id", "entity_type", "entity_id", "field_name", "candidate_value",
        "source_id", "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note",
    ], verified_evidence)
    _write(output_dir / "held_fields.csv",
           ["decision_id", "entity_type", "entity_id", "held_fields", "reason"], held_rows)
    _write(output_dir / "issue_dispositions.csv", [
        "issue_id", "person_id", "related_id", "issue_type", "status", "description", "disposition",
    ], issue_dispositions)

    counts = {
        "ready": len(ready), "holds": len(holds),
        "persons": len(verified_persons), "organizations": len(verified_organizations),
        "careers": len(verified_careers), "sources": len(verified_sources),
        "evidence": len(verified_evidence), "held": len(held_rows), "issues": len(issue_dispositions),
    }

    scope = f"""# {label} VERIFIED候補 作成範囲

作成日：{created_at}

{label}のQA判断から、READY {counts['ready']}件の`eligible_fields`だけをVERIFIED候補へ抽出した。

- CANDIDATE・QA基準commit：`{source_commit}`
- 対象：`{wave_dir.relative_to(root)}/qa_decisions.csv`のREADY {counts['ready']}件
- 除外：PARTIAL Evidence、`held_fields`、全HOLD Issue
- HUMAN APPROVAL：含まない
- Master承認・反映：含まない
- 公開サイト反映：含まない
"""
    (output_dir / "verification_scope.md").write_text(scope, encoding="utf-8")

    report = f"""# {label} VERIFIED生成レポート

作成日：{created_at}

## 結果

- CANDIDATEスナップショット：commit `{source_commit}`から変更なし
- READY Decision：{counts['ready']}件
- HOLD Decision：{counts['holds']}件
- Person：{counts['persons']}件
- Career：{counts['careers']}件
- Organization：{counts['organizations']}件
- Source：{counts['sources']}件
- 採用Evidence：{counts['evidence']}件
- HOLD記録：{counts['held']}件
- HOLD Issue：{counts['issues']}件
- HUMAN APPROVAL・Master：未実施
- 公開サイト：未変更

VERIFIEDは公式SourceとQAを通過した確認済み候補であり、Human ApprovalまたはMasterを意味しない。
"""
    (output_dir / "verification_report.md").write_text(report, encoding="utf-8")

    readme = f"""# {label} VERIFIED

作成日：{created_at}

状態：VERIFIED候補、HUMAN APPROVAL・MASTER未実施

{label}のREADY {counts['ready']}判断について、`eligible_fields`に一致するSUPPORTED Evidenceだけを抽出した。PARTIAL Evidence、`held_fields`、{counts['issues']}件のHOLD Issueは除外・分離している。

このディレクトリは確認済み候補であり、正式なMaster Dataでも公開承認済みデータでもない。

## ファイル

- `person_verified.csv`：{counts['persons']}人
- `organization_verified.csv`：{counts['organizations']}組織
- `career_verified.csv`：{counts['careers']}件
- `source_references.csv`：採用Evidenceが参照する公式Source
- `evidence_records.csv`：eligible_fieldsに一致したSUPPORTED Evidence
- `held_fields.csv`：VERIFIEDへ含めなかった判断・項目
- `issue_dispositions.csv`：{counts['issues']}件のHOLD
- `verification_scope.md`：対象範囲と除外事項
- `verification_report.md`：生成結果
- `validation_report.md`：構造検証結果
"""
    (output_dir / "README.md").write_text(readme, encoding="utf-8")

    return counts


def validate_verified(root: Path, output_dir: Path, wave_dir: Path, label: str, created_at: str) -> list[str]:
    errors: list[str] = []
    persons = _read(output_dir / "person_verified.csv")
    organizations = _read(output_dir / "organization_verified.csv")
    careers = _read(output_dir / "career_verified.csv")
    sources = _read(output_dir / "source_references.csv")
    evidence = _read(output_dir / "evidence_records.csv")
    held = _read(output_dir / "held_fields.csv")
    issues = _read(output_dir / "issue_dispositions.csv")
    decisions = _read(wave_dir / "qa_decisions.csv")
    ready = [row for row in decisions if row["decision"] == "READY_FOR_VERIFIED_REVIEW"]

    eligible: dict[tuple[str, str], set[str]] = {}
    for row in ready:
        target = (row["entity_type"], row["entity_id"])
        eligible.setdefault(target, set()).update(filter(None, row["eligible_fields"].split("|")))

    person_ids = {row["person_id"] for row in persons}
    organization_ids = {row["organization_id"] for row in organizations}
    source_ids = {row["source_id"] for row in sources}
    career_ids = {row["career_id"] for row in careers}
    master_person_ids = {row["person_id"] for row in _read(root / "data" / "master" / "person.csv")}
    if person_ids & master_person_ids:
        errors.append("Masterに存在するPersonが新規VERIFIEDへ混入")

    for row in careers:
        if row["person_id"] not in person_ids:
            errors.append(f"{row['career_id']}: unknown person")
        if row["organization_id"] not in organization_ids:
            errors.append(f"{row['career_id']}: unknown organization")
        allowed = eligible.get(("Career", row["career_id"]), set())
        for field in ["organization_id", "role", "start", "end"]:
            if row[field] and field not in allowed:
                errors.append(f"{row['career_id']}: held {field} was populated")

    for row in evidence:
        if row["assessment"] != "SUPPORTED":
            errors.append(f"{row['record_id']}: non-supported evidence")
        if row["source_id"] not in source_ids:
            errors.append(f"{row['record_id']}: unknown source")
        if row["field_name"] not in eligible.get((row["entity_type"], row["entity_id"]), set()):
            errors.append(f"{row['record_id']}: field outside eligible scope")
        if row["entity_type"] == "Career" and row["entity_id"] not in career_ids:
            errors.append(f"{row['record_id']}: evidence refers to excluded career")

    if any(row["status"] != "HOLD" for row in issues):
        errors.append("issue disposition contains a non-HOLD status")
    if any(not row["held_fields"] for row in held):
        errors.append("held_fields contains a blank field list")

    report = [
        f"# {label} VERIFIED検証レポート", "", f"作成日：{created_at}", "",
        "## 結果", "", f"- 検証：{'PASS' if not errors else 'FAIL'}",
        f"- エラー：{len(errors)}件", f"- Person：{len(persons)}件",
        f"- Career：{len(careers)}件", f"- Organization：{len(organizations)}件",
        f"- Source：{len(sources)}件", f"- Evidence：{len(evidence)}件",
        f"- HOLD記録：{len(held)}件", f"- HOLD Issue：{len(issues)}件",
        "- HUMAN APPROVAL・Master：未実施", "", "## エラー", "",
    ]
    report.extend(f"- {error}" for error in errors)
    if not errors:
        report.append("- なし")
    (output_dir / "validation_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return errors
