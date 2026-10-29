#!/usr/bin/env python3
"""Apply Yuichi's explicit Approval Sprint 023 decision (B.LEAGUE DRAFT 2026 players) to MASTER:
draft facts, Career details (grade, contract_type), 9 university periods (7 estimates),
1 new Career and 1 new Organization. Record: data/verified/approval_sprint_023/master_approval.md."""

from __future__ import annotations

import csv
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "data/verified/approval_sprint_023"
MASTER = ROOT / "data/master"
PACKET_COMMIT = "3573693"
VERIFIED_COMMIT = "63ecad0"
APPROVAL_ID = "APP-AS023-20261029-01"
APPROVED_AT = "2026-10-29"
TRACKED = ["README.md", "draft_fact_review.csv", "career_detail_review.csv", "master_correction_review.csv", "career_review.csv",
           "organization_review.csv", "evidence_review.csv", "source_review.csv", "hold_review.csv", "validation_report.md"]
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
        raise SystemExit("packet differs from the reviewed commit")
    text = (PACKET / "master_approval.md").read_text(encoding="utf-8")
    for v in (APPROVAL_ID, PACKET_COMMIT, VERIFIED_COMMIT, "承認者：Yuichi", "対象の版は VERIFIED 63ecad0、資料 3573693 です。"):
        if v not in text:
            raise SystemExit(f"approval record is incomplete ({v})")
    ev = [{k: r[k] for k in EVIDENCE_H} for r in read(PACKET / "evidence_review.csv")]
    if any(e["assessment"] != "SUPPORTED" for e in ev):
        raise SystemExit("non-SUPPORTED evidence")
    used = {e["source_id"] for e in ev}
    sources = [{k: r[k] for k in SOURCE_H} for r in read(PACKET / "source_review.csv") if r["source_id"] in used]
    corr = read(PACKET / "master_correction_review.csv")
    rows = read(MASTER / "career.csv")
    by_id = {r["career_id"]: r for r in rows}
    for c in corr:
        m = by_id.get(c["career_id"])
        if not m or (m["start"], m["end"]) != (c["old_start"], c["old_end"]):
            raise SystemExit(f"{c['career_id']}: MASTER differs")
        m["start"], m["end"] = c["new_start"], c["new_end"]
    write(MASTER / "career.csv", CAREER_H, rows)
    careers = [{k: r[k] for k in CAREER_H} for r in read(PACKET / "career_review.csv")]
    orgs = [{"organization_id": r["organization_id"], "name": r["name"]} for r in read(PACKET / "organization_review.csv")]
    counts = {
        "people": len(read(MASTER / "person.csv")),
        "orgs": merge(MASTER / "organization.csv", orgs, ["organization_id", "name"], "organization_id"),
        "careers": merge(MASTER / "career.csv", careers, CAREER_H, "career_id"),
        "sources": merge(MASTER / "source.csv", sources, SOURCE_H, "source_id"),
        "evidence": merge(MASTER / "evidence.csv", ev, EVIDENCE_H, "record_id"),
    }
    counts["approvals"] = merge(MASTER / "approval_records.csv", [{
        "approval_id": APPROVAL_ID, "batch": "Approval Sprint 023", "verified_commit": VERIFIED_COMMIT,
        "approved_scope": f"B.LEAGUE DRAFT 2026 players: 14 draft facts, career details (grade, contract_type), {len(corr)} university periods "
                          f"(7 estimates from the official year), {len(careers)} career, {len(orgs)} new organization, {len(ev)} supported evidence; Tier 2",
        "excluded_scope": f"{len(read(PACKET / 'hold_review.csv'))} HOLD issues", "approved_by": "Yuichi", "approved_at": APPROVED_AT,
        "approval_reference": "data/verified/approval_sprint_023/master_approval.md",
    }], ["approval_id", "batch", "verified_commit", "approved_scope", "excluded_scope", "approved_by", "approved_at", "approval_reference"], "approval_id")
    write(PACKET / "career_review_enrichment_only.csv", ["person_id", "career_id"],
          [{"person_id": e["entity_id"], "career_id": ""} for e in ev if e["entity_type"] == "Person"]
          + [{"person_id": by_id[e["entity_id"]]["person_id"] if e["entity_id"] in by_id else careers[0]["person_id"], "career_id": e["entity_id"]}
             for e in ev if e["entity_type"] == "Career"])
    rp = MASTER / "master_build_report.md"
    rep = rp.read_text(encoding="utf-8")
    rep = rep.replace("\n\n## MASTER件数", f"\n- `{APPROVAL_ID}`：Approval Sprint 023（B.LEAGUE DRAFT 2026の指名選手、batch_038 wave_01、ドラフト結果・学年・契約区分・大学期間、Tier 2）\n\n## MASTER件数", 1)
    rep = re.sub(r"作成日：\S+", f"作成日：{APPROVED_AT}", rep, count=1)
    for k, lab in (("people", "Person"), ("orgs", "Organization"), ("careers", "Career"), ("sources", "Source"), ("evidence", "Evidence"), ("approvals", "Approval")):
        rep = re.sub(rf"- {lab}：\d+件", f"- {lab}：{counts[k]}件", rep)
    rp.write_text(rep, encoding="utf-8")
    print("Approval Sprint 023 applied:", counts)


if __name__ == "__main__":
    main()
