#!/usr/bin/env python3
"""Apply Yuichi's explicit Approval Sprint 018 decision to MASTER.

Scope: 八村塁(P000104, new), 馬場雄大(P000107)・比江島慎(P000084)(both existing
MASTER persons, Career additions only) from batch_007 wave_13 VERIFIED. The
packet must be unchanged since its review commit, and master_approval.md must
hold Yuichi's approval text. New Person, Careers, referenced Organizations,
SUPPORTED Evidence and Sources are added; nothing already in MASTER is
changed. HOLD issues / held fields are not applied.
"""

from __future__ import annotations

import csv
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "data/verified/approval_sprint_018"
MASTER = ROOT / "data/master"
PACKET_COMMIT = "014da83"
VERIFIED_COMMIT = "cc7fbc1"
APPROVAL_ID = "APP-AS018-20261008-01"
APPROVED_AT = "2026-10-08"
TRACKED = ["README.md", "person_review.csv", "career_review.csv", "organization_review.csv",
           "evidence_review.csv", "source_review.csv", "hold_review.csv", "held_fields_review.csv",
           "validation_report.md"]
EVIDENCE_HEADERS = ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id",
                    "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"]


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as h:
        return list(csv.DictReader(h))


def write(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=headers, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def merge(path: Path, incoming: list[dict[str, str]], headers: list[str], key: str) -> list[dict[str, str]]:
    merged = {r[key]: r for r in read(path)}
    for r in incoming:
        r = {h: r[h] for h in headers}
        if r[key] in merged and merged[r[key]] != r:
            raise SystemExit(f"MASTER conflict: {key}={r[key]}")
        merged[r[key]] = r
    rows = [merged[k] for k in sorted(merged)]
    write(path, headers, rows)
    return rows


def verify() -> None:
    paths = [str((PACKET / n).relative_to(ROOT)) for n in TRACKED]
    if subprocess.run(["git", "diff", "--quiet", PACKET_COMMIT, "--", *paths], cwd=ROOT).returncode:
        raise SystemExit("Approval Sprint 018 packet differs from the reviewed commit")
    text = (PACKET / "master_approval.md").read_text(encoding="utf-8")
    for v in (APPROVAL_ID, PACKET_COMMIT, VERIFIED_COMMIT, "承認者：Yuichi", "Masterに承認します"):
        if v not in text:
            raise SystemExit("Approval Sprint 018 approval record is incomplete")


def main() -> None:
    verify()
    persons_in_packet = read(PACKET / "person_review.csv")
    careers = [{k: r[k] for k in ["career_id", "person_id", "organization_id", "role", "start", "end"]}
               for r in read(PACKET / "career_review.csv")]
    orgs = [{"organization_id": r["organization_id"], "name": r["name"]} for r in read(PACKET / "organization_review.csv")]
    sources = [{k: r[k] for k in ["source_id", "title", "publisher", "url", "accessed_at"]} for r in read(PACKET / "source_review.csv")]
    evidence = [{k: r[k] for k in EVIDENCE_HEADERS} for r in read(PACKET / "evidence_review.csv")]
    if any(e["assessment"] != "SUPPORTED" for e in evidence):
        raise SystemExit("non-SUPPORTED evidence in packet")

    existing_people = {r["person_id"] for r in read(MASTER / "person.csv")}
    new_persons = [{"person_id": r["person_id"], "name": r["name"]} for r in persons_in_packet
                   if r["person_id"] not in existing_people]
    if any(r["person_id"] in existing_people for r in new_persons):
        raise SystemExit("unexpected: person already in MASTER")

    counts = {
        "people": len(merge(MASTER / "person.csv", new_persons, ["person_id", "name"], "person_id")) if new_persons else len(read(MASTER / "person.csv")),
        "orgs": len(merge(MASTER / "organization.csv", orgs, ["organization_id", "name"], "organization_id")),
        "careers": len(merge(MASTER / "career.csv", careers, ["career_id", "person_id", "organization_id", "role", "start", "end"], "career_id")),
        "sources": len(merge(MASTER / "source.csv", sources, ["source_id", "title", "publisher", "url", "accessed_at"], "source_id")),
        "evidence": len(merge(MASTER / "evidence.csv", evidence, EVIDENCE_HEADERS, "record_id")),
    }
    holds = len(read(PACKET / "hold_review.csv"))
    held = len(read(PACKET / "held_fields_review.csv"))
    counts["approvals"] = len(merge(MASTER / "approval_records.csv", [{
        "approval_id": APPROVAL_ID, "batch": "Approval Sprint 018", "verified_commit": VERIFIED_COMMIT,
        "approved_scope": f"{len(new_persons)} new person (八村塁 P000104), 2 existing persons (馬場雄大 P000107, 比江島慎 P000084) with career additions, "
                           f"{len(careers)} careers, {len(evidence)} supported evidence, {len(orgs)} referenced organizations (Tier 2)",
        "excluded_scope": f"{holds} HOLD issues, {held} held fields", "approved_by": "Yuichi", "approved_at": APPROVED_AT,
        "approval_reference": "data/verified/approval_sprint_018/master_approval.md",
    }], ["approval_id", "batch", "verified_commit", "approved_scope", "excluded_scope", "approved_by", "approved_at", "approval_reference"], "approval_id"))

    report_path = MASTER / "master_build_report.md"
    rep = report_path.read_text(encoding="utf-8")
    rep = rep.replace("作成日：2026-10-04", f"作成日：{APPROVED_AT}")
    rep = rep.replace(
        "- `APP-AS012-20261004-01`：Approval Sprint 012（B.PREMIER選手6名の現所属Careerの期間訂正）",
        "- `APP-AS012-20261004-01`：Approval Sprint 012（B.PREMIER選手6名の現所属Careerの期間訂正）\n"
        f"- `{APPROVAL_ID}`：Approval Sprint 018（八村塁の新規登録、馬場雄大・比江島慎の海外Career追加、海外公式資料、Tier 2）")
    rep = re.sub(r"- Person：\d+件", f"- Person：{counts['people']}件", rep)
    rep = re.sub(r"- Organization：\d+件", f"- Organization：{counts['orgs']}件", rep)
    rep = re.sub(r"- Career：\d+件", f"- Career：{counts['careers']}件", rep)
    rep = re.sub(r"- Source：\d+件", f"- Source：{counts['sources']}件", rep)
    rep = re.sub(r"- Evidence：\d+件", f"- Evidence：{counts['evidence']}件", rep)
    rep = re.sub(r"- Approval：\d+件", f"- Approval：{counts['approvals']}件", rep)
    report_path.write_text(rep, encoding="utf-8")
    print(f"Approval Sprint 018 applied: +{len(new_persons)} persons, +{len(careers)} careers -> {counts}")


if __name__ == "__main__":
    main()
