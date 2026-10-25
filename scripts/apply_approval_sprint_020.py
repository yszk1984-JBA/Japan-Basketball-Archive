#!/usr/bin/env python3
"""Apply Yuichi's explicit Approval Sprint 020 decision to MASTER.

Scope: pre-B.LEAGUE / early overseas careers of national-team players
(batch_035 wave_01, VERIFIED 9687ee5): 24 Careers for 11 existing MASTER
persons and 8 new Organizations. Approval record:
data/verified/approval_sprint_020/master_approval.md. HOLD issues excluded.
"""

from __future__ import annotations

import csv
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "data/verified/approval_sprint_020"
MASTER = ROOT / "data/master"
PACKET_COMMIT = "1e1333a"
VERIFIED_COMMIT = "9687ee5"
APPROVAL_ID = "APP-AS020-20261025-01"
APPROVED_AT = "2026-10-25"
TRACKED = ["README.md", "person_review.csv", "career_review.csv", "organization_review.csv", "evidence_review.csv",
           "source_review.csv", "hold_review.csv", "held_fields_review.csv", "validation_report.md"]
CAREER_H = ["career_id", "person_id", "organization_id", "role", "start", "end"]
SOURCE_H = ["source_id", "title", "publisher", "url", "accessed_at"]
EVIDENCE_H = ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id",
              "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"]


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as h:
        return list(csv.DictReader(h))


def write(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=headers, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def merge(path: Path, incoming: list[dict[str, str]], headers: list[str], key: str) -> int:
    merged = {r[key]: r for r in read(path)}
    for r in incoming:
        r = {h: r[h] for h in headers}
        if r[key] in merged and merged[r[key]] != r:
            raise SystemExit(f"MASTER conflict: {key}={r[key]}")
        merged[r[key]] = r
    write(path, headers, [merged[k] for k in sorted(merged)])
    return len(merged)


def main() -> None:
    paths = [str((PACKET / n).relative_to(ROOT)) for n in TRACKED]
    if subprocess.run(["git", "diff", "--quiet", PACKET_COMMIT, "--", *paths], cwd=ROOT).returncode:
        raise SystemExit("Approval Sprint 020 packet differs from the reviewed commit")
    text = (PACKET / "master_approval.md").read_text(encoding="utf-8")
    for v in (APPROVAL_ID, PACKET_COMMIT, VERIFIED_COMMIT, "承認者：Yuichi", "上記の内容をすべて承諾します", "Tier 2を承諾します"):
        if v not in text:
            raise SystemExit(f"approval record is incomplete ({v})")
    master_people = {r["person_id"] for r in read(MASTER / "person.csv")}
    careers = [{k: r[k] for k in CAREER_H} for r in read(PACKET / "career_review.csv")]
    if any(c["person_id"] not in master_people for c in careers):
        raise SystemExit("person not in MASTER")
    orgs = [{"organization_id": r["organization_id"], "name": r["name"]} for r in read(PACKET / "organization_review.csv")]
    evidence = [{k: r[k] for k in EVIDENCE_H} for r in read(PACKET / "evidence_review.csv")]
    if any(e["assessment"] != "SUPPORTED" for e in evidence):
        raise SystemExit("non-SUPPORTED evidence")
    used = {e["source_id"] for e in evidence}
    sources = [{k: r[k] for k in SOURCE_H} for r in read(PACKET / "source_review.csv") if r["source_id"] in used]
    holds = len(read(PACKET / "hold_review.csv"))
    held = len(read(PACKET / "held_fields_review.csv"))
    counts = {
        "people": len(master_people),
        "orgs": merge(MASTER / "organization.csv", orgs, ["organization_id", "name"], "organization_id"),
        "careers": merge(MASTER / "career.csv", careers, CAREER_H, "career_id"),
        "sources": merge(MASTER / "source.csv", sources, SOURCE_H, "source_id"),
        "evidence": merge(MASTER / "evidence.csv", evidence, EVIDENCE_H, "record_id"),
    }
    counts["approvals"] = merge(MASTER / "approval_records.csv", [{
        "approval_id": APPROVAL_ID, "batch": "Approval Sprint 020", "verified_commit": VERIFIED_COMMIT,
        "approved_scope": f"pre-B.LEAGUE / early overseas careers of national-team players: {len({c['person_id'] for c in careers})} existing persons, "
                          f"{len(careers)} careers, {len(orgs)} referenced organizations (8 new), {len(evidence)} supported evidence "
                          f"(Japanese Wikipedia, non-official); Tier 2",
        "excluded_scope": f"{holds} HOLD issues; {held} held fields", "approved_by": "Yuichi", "approved_at": APPROVED_AT,
        "approval_reference": "data/verified/approval_sprint_020/master_approval.md",
    }], ["approval_id", "batch", "verified_commit", "approved_scope", "excluded_scope", "approved_by", "approved_at", "approval_reference"],
        "approval_id")
    report_path = MASTER / "master_build_report.md"
    rep = report_path.read_text(encoding="utf-8")
    rep = rep.replace("\n\n## MASTER件数", f"\n- `{APPROVAL_ID}`：Approval Sprint 020（日本代表経験者の開幕前・初期海外の経歴、batch_035 wave_01、Career 24件・新規Organization 8件、Wikipedia、Tier 2）\n\n## MASTER件数", 1)
    rep = re.sub(r"作成日：\S+", f"作成日：{APPROVED_AT}", rep, count=1)
    for k, lab in (("people", "Person"), ("orgs", "Organization"), ("careers", "Career"), ("sources", "Source"), ("evidence", "Evidence"), ("approvals", "Approval")):
        rep = re.sub(rf"- {lab}：\d+件", f"- {lab}：{counts[k]}件", rep)
    report_path.write_text(rep, encoding="utf-8")
    print("Approval Sprint 020 applied:", counts)


if __name__ == "__main__":
    main()
