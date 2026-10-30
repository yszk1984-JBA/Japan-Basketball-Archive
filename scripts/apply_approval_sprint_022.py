#!/usr/bin/env python3
"""Apply Yuichi's explicit Approval Sprint 022 decision to MASTER.

Scope (post-opening roster update, batch_034 wave_01, VERIFIED 5a9b188):
4 MASTER period corrections, 4 new Careers, 2 new Persons. Approval record:
data/verified/approval_sprint_022/master_approval.md. HOLD issues excluded.
Also writes the site-build helper lists person_review_new_only.csv and
career_review_enrichment_only.csv (derived, not part of the reviewed packet).
"""

from __future__ import annotations

import csv
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "data/verified/approval_sprint_022"
MASTER = ROOT / "data/master"
PACKET_COMMIT = "38f6002"
VERIFIED_COMMIT = "6e29821"
APPROVAL_ID = "APP-AS022-20261030-01"
APPROVED_AT = "2026-10-30"
TRACKED = ["README.md", "person_review.csv", "career_review.csv", "organization_review.csv", "master_correction_review.csv",
           "evidence_review.csv", "source_review.csv", "hold_review.csv", "held_fields_review.csv", "validation_report.md"]
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
        raise SystemExit("Approval Sprint 022 packet differs from the reviewed commit")
    text = (PACKET / "master_approval.md").read_text(encoding="utf-8")
    for v in (APPROVAL_ID, PACKET_COMMIT, VERIFIED_COMMIT, "承認者：Yuichi", "対象の版：VERIFIED `6e29821`、資料 `38f6002`", "Tier案：全員Tier 2"):
        if v not in text:
            raise SystemExit(f"approval record is incomplete ({v})")

    people = read(PACKET / "person_review.csv")
    master_people = {r["person_id"] for r in read(MASTER / "person.csv")}
    new_persons = [{"person_id": r["person_id"], "name": r["name"]} for r in people if r["status"] == "新規Person"]
    if any(p["person_id"] in master_people for p in new_persons) or len(new_persons) != 2:
        raise SystemExit("unexpected new-person set")
    careers = [{k: r[k] for k in CAREER_H} for r in read(PACKET / "career_review.csv")]
    evidence = [{k: r[k] for k in EVIDENCE_H} for r in read(PACKET / "evidence_review.csv")]
    if any(e["assessment"] != "SUPPORTED" for e in evidence):
        raise SystemExit("non-SUPPORTED evidence")
    used = {e["source_id"] for e in evidence}
    sources = [{k: r[k] for k in SOURCE_H} for r in read(PACKET / "source_review.csv") if r["source_id"] in used]
    corrections = read(PACKET / "master_correction_review.csv")
    orgs = [{"organization_id": r["organization_id"], "name": r["name"]} for r in read(PACKET / "organization_review.csv")
            if r["status"] != "Master既存"]

    rows = read(MASTER / "career.csv")
    by_id = {r["career_id"]: r for r in rows}
    for c in corrections:
        m = by_id.get(c["career_id"])
        if not m or (m["start"], m["end"]) != (c["old_start"], c["old_end"]) or m["person_id"] != c["person_id"]:
            raise SystemExit(f"{c['career_id']}: MASTER differs from the reviewed old value")
        m["start"], m["end"] = c["new_start"], c["new_end"]
    write(MASTER / "career.csv", CAREER_H, rows)

    holds = len(read(PACKET / "hold_review.csv"))
    counts = {
        "people": merge(MASTER / "person.csv", new_persons, ["person_id", "name"], "person_id"),
        "careers": merge(MASTER / "career.csv", careers, CAREER_H, "career_id"),
        "sources": merge(MASTER / "source.csv", sources, SOURCE_H, "source_id"),
        "evidence": merge(MASTER / "evidence.csv", evidence, EVIDENCE_H, "record_id"),
        "orgs": merge(MASTER / "organization.csv", orgs, ["organization_id", "name"], "organization_id"),
    }
    counts["approvals"] = merge(MASTER / "approval_records.csv", [{
        "approval_id": APPROVAL_ID, "batch": "Approval Sprint 022", "verified_commit": VERIFIED_COMMIT,
        "approved_scope": f"2026-10-29 update: {len(new_persons)} new persons (P000566, P000567), {len(careers)} careers, {len(orgs)} new organizations, "
                          f"{len(corrections)} master career period corrections (C001371, C002686, C000129), "
                          f"{len(evidence)} supported evidence; Tier 2",
        "excluded_scope": f"{holds} HOLD issues; held fields", "approved_by": "Yuichi", "approved_at": APPROVED_AT,
        "approval_reference": "data/verified/approval_sprint_022/master_approval.md",
    }], ["approval_id", "batch", "verified_commit", "approved_scope", "excluded_scope", "approved_by", "approved_at", "approval_reference"],
        "approval_id")

    new_ids = {p["person_id"] for p in new_persons}
    write(PACKET / "person_review_new_only.csv", list(people[0].keys()), [r for r in people if r["person_id"] in new_ids])
    enrich = [{"person_id": c["person_id"], "career_id": c["career_id"]} for c in careers if c["person_id"] not in new_ids] + \
             [{"person_id": c["person_id"], "career_id": c["career_id"]} for c in corrections]
    write(PACKET / "career_review_enrichment_only.csv", ["person_id", "career_id"], enrich)

    report_path = MASTER / "master_build_report.md"
    rep = report_path.read_text(encoding="utf-8")
    rep = rep.replace("\n\n## MASTER件数", f"\n- `{APPROVAL_ID}`：Approval Sprint 022（2026-10-29の更新、batch_037 wave_01、期間訂正3件・Career追加23件・新規2名・新規Organization 2件、Tier 2）\n\n## MASTER件数", 1)
    rep = re.sub(r"作成日：\S+", f"作成日：{APPROVED_AT}", rep, count=1)
    for k, lab in (("people", "Person"), ("orgs", "Organization"), ("careers", "Career"), ("sources", "Source"), ("evidence", "Evidence"), ("approvals", "Approval")):
        rep = re.sub(rf"- {lab}：\d+件", f"- {lab}：{counts[k]}件", rep)
    report_path.write_text(rep, encoding="utf-8")
    print("Approval Sprint 022 applied:", counts)


if __name__ == "__main__":
    main()
