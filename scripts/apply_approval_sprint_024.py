#!/usr/bin/env python3
"""Apply Yuichi's explicit Approval Sprint 024 decision to MASTER.

Scope (officially published junior-high schools, batch_039 wave_01, VERIFIED cad054a):
56 new Careers, 50 new Organizations, official high-school period evidence for 24 Careers
(1 MASTER period correction). Approval record:
data/verified/approval_sprint_024/master_approval.md. HOLD issues excluded.
Also writes the site-build helper list career_review_enrichment_only.csv (derived, not part of the reviewed packet).
"""

from __future__ import annotations

import csv
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "data/verified/approval_sprint_024"
MASTER = ROOT / "data/master"
PACKET_COMMIT = "b5b47ad"
VERIFIED_COMMIT = "cad054a"
APPROVAL_ID = "APP-AS024-20261102-01"
APPROVED_AT = "2026-11-02"
TRACKED = ["README.md", "career_review.csv", "organization_review.csv", "master_correction_review.csv", "high_school_period_review.csv",
           "evidence_review.csv", "source_review.csv", "hold_review.csv", "validation_report.md"]
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
        raise SystemExit("Approval Sprint 024 packet differs from the reviewed commit")
    text = (PACKET / "master_approval.md").read_text(encoding="utf-8")
    for v in (APPROVAL_ID, PACKET_COMMIT, VERIFIED_COMMIT, "承認者：Yuichi", "VERIFIED `cad054a`（資料 `b5b47ad`）", "全部承認します", "Tier：案は全員Tier 1"):
        if v not in text:
            raise SystemExit(f"approval record is incomplete ({v})")

    master_people = {r["person_id"] for r in read(MASTER / "person.csv")}
    # The review table omits role; take the rows from the VERIFIED snapshot and check they match the review.
    verified = {r["career_id"]: {k: r[k] for k in CAREER_H} for r in read(ROOT / "data/verified/batch_039_wave_01/career_candidates.csv")}
    if subprocess.run(["git", "diff", "--quiet", VERIFIED_COMMIT, "--", "data/verified/batch_039_wave_01"], cwd=ROOT).returncode:
        raise SystemExit("VERIFIED snapshot differs from the approved commit")
    review = read(PACKET / "career_review.csv")
    careers = [verified[r["career_id"]] for r in review]
    for r, c in zip(review, careers):
        if (r["person_id"], r["organization_id"], r["start"], r["end"]) != (c["person_id"], c["organization_id"], c["start"], c["end"]) or c["role"] != "Player":
            raise SystemExit(f"{r['career_id']}: review differs from VERIFIED")
    evidence = [{k: r[k] for k in EVIDENCE_H} for r in read(PACKET / "evidence_review.csv")]
    if any(e["assessment"] != "SUPPORTED" for e in evidence):
        raise SystemExit("non-SUPPORTED evidence")
    used = {e["source_id"] for e in evidence}
    sources = [{k: r[k] for k in SOURCE_H} for r in read(PACKET / "source_review.csv") if r["source_id"] in used]
    corrections = read(PACKET / "master_correction_review.csv")
    orgs = [{"organization_id": r["organization_id"], "name": r["name"]} for r in read(PACKET / "organization_review.csv")
            if r["status"].startswith("新規")]
    if len(careers) != 56 or len(orgs) != 50 or len(corrections) != 1 or any(c["person_id"] not in master_people for c in careers):
        raise SystemExit("unexpected packet set")

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
        "people": len(master_people),
        "careers": merge(MASTER / "career.csv", careers, CAREER_H, "career_id"),
        "sources": merge(MASTER / "source.csv", sources, SOURCE_H, "source_id"),
        "evidence": merge(MASTER / "evidence.csv", evidence, EVIDENCE_H, "record_id"),
        "orgs": merge(MASTER / "organization.csv", orgs, ["organization_id", "name"], "organization_id"),
    }
    counts["approvals"] = merge(MASTER / "approval_records.csv", [{
        "approval_id": APPROVAL_ID, "batch": "Approval Sprint 024", "verified_commit": VERIFIED_COMMIT,
        "approved_scope": f"officially published junior-high schools: {len(careers)} careers (C002830-C002885), {len(orgs)} new organizations "
                          f"(ORG000519-ORG000568), official high-school periods for 24 careers incl. {len(corrections)} master period correction (C002825), "
                          f"{len(evidence)} supported evidence; Tier 1",
        "excluded_scope": f"{holds} HOLD issues (high-school name mismatch)", "approved_by": "Yuichi", "approved_at": APPROVED_AT,
        "approval_reference": "data/verified/approval_sprint_024/master_approval.md",
    }], ["approval_id", "batch", "verified_commit", "approved_scope", "excluded_scope", "approved_by", "approved_at", "approval_reference"],
        "approval_id")

    hs_ids = {r["career_id"] for r in read(PACKET / "high_school_period_review.csv")}
    enrich = [{"person_id": c["person_id"], "career_id": c["career_id"]} for c in careers] + \
             [{"person_id": by_id[i]["person_id"], "career_id": i} for i in sorted(hs_ids)]
    write(PACKET / "career_review_enrichment_only.csv", ["person_id", "career_id"], enrich)

    report_path = MASTER / "master_build_report.md"
    rep = report_path.read_text(encoding="utf-8")
    rep = rep.replace("\n\n## MASTER件数", f"\n- `{APPROVAL_ID}`：Approval Sprint 024（公式に公表されている中学校、batch_039 wave_01、Career追加56件・新規Organization 50件・高校の公式在学期間24件〈期間訂正1件〉、Tier 1）\n\n## MASTER件数", 1)
    rep = re.sub(r"作成日：\S+", f"作成日：{APPROVED_AT}", rep, count=1)
    for k, lab in (("people", "Person"), ("orgs", "Organization"), ("careers", "Career"), ("sources", "Source"), ("evidence", "Evidence"), ("approvals", "Approval")):
        rep = re.sub(rf"- {lab}：\d+件", f"- {lab}：{counts[k]}件", rep)
    report_path.write_text(rep, encoding="utf-8")
    print("Approval Sprint 024 applied:", counts)


if __name__ == "__main__":
    main()
