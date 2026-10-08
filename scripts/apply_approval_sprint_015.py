#!/usr/bin/env python3
"""Apply Yuichi's explicit Approval Sprint 015 decision to MASTER.

Scope: 渡邊雄太(P000103)・田臥勇太(P000105)・富永啓生(P000106)（全員既存MASTER
Person）のCareer追加11件（batch_007 wave_12, VERIFIED commit `188db92`）＋既存
Career 2件（C000354, C000363）の期間（start/end）訂正。承認記録は
data/verified/approval_sprint_015/master_approval.md。HOLD issue（5件）は対象外。
"""

from __future__ import annotations

import csv
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "data/verified/approval_sprint_015"
MASTER = ROOT / "data/master"
PACKET_COMMIT = "75a759c"
VERIFIED_COMMIT = "188db92"
APPROVAL_ID = "APP-AS015-20261008-01"
APPROVED_AT = "2026-10-08"
TRACKED = ["README.md", "person_review.csv", "career_review.csv", "organization_review.csv",
           "evidence_review.csv", "source_review.csv", "hold_review.csv",
           "master_correction_review.csv", "validation_report.md"]
EVIDENCE_HEADERS = ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id",
                    "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"]
CORRECTIONS = {"C000354": ("2014", "2018"), "C000363": ("2021", "2024")}


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


def apply_corrections(path: Path, headers: list[str]) -> list[dict[str, str]]:
    rows = read(path)
    found = set()
    for r in rows:
        if r["career_id"] in CORRECTIONS:
            start, end = CORRECTIONS[r["career_id"]]
            if r["start"] or r["end"]:
                raise SystemExit(f"{r['career_id']}: expected blank start/end before correction, found start={r['start']!r} end={r['end']!r}")
            r["start"], r["end"] = start, end
            found.add(r["career_id"])
    if found != set(CORRECTIONS):
        raise SystemExit(f"correction targets not found: {set(CORRECTIONS) - found}")
    write(path, headers, rows)
    return rows


def verify() -> None:
    paths = [str((PACKET / n).relative_to(ROOT)) for n in TRACKED]
    if subprocess.run(["git", "diff", "--quiet", PACKET_COMMIT, "--", *paths], cwd=ROOT).returncode:
        raise SystemExit("Approval Sprint 015 packet differs from the reviewed commit")
    text = (PACKET / "master_approval.md").read_text(encoding="utf-8")
    for v in (APPROVAL_ID, PACKET_COMMIT, VERIFIED_COMMIT, "承認者：Yuichi",
              "Approval Sprint 015（上記の渡邊・田臥・富永の内容）をこのままMasterへ承認"):
        if v not in text:
            raise SystemExit("Approval Sprint 015 approval record is incomplete")


def main() -> None:
    verify()
    careers = [{k: r[k] for k in ["career_id", "person_id", "organization_id", "role", "start", "end"]}
               for r in read(PACKET / "career_review.csv")]
    orgs = [{"organization_id": r["organization_id"], "name": r["name"]} for r in read(PACKET / "organization_review.csv")]
    sources = [{k: r[k] for k in ["source_id", "title", "publisher", "url", "accessed_at"]} for r in read(PACKET / "source_review.csv")]
    evidence = [{k: r[k] for k in EVIDENCE_HEADERS} for r in read(PACKET / "evidence_review.csv")]
    if any(e["assessment"] != "SUPPORTED" for e in evidence):
        raise SystemExit("non-SUPPORTED evidence in packet")

    existing_people = {r["person_id"] for r in read(MASTER / "person.csv")}
    for c in careers:
        if c["person_id"] not in existing_people:
            raise SystemExit(f"unexpected: {c['person_id']} not already in MASTER (this packet adds no new Person)")

    counts = {
        "people": len(read(MASTER / "person.csv")),
        "orgs": len(merge(MASTER / "organization.csv", orgs, ["organization_id", "name"], "organization_id")),
        "careers": len(merge(MASTER / "career.csv", careers, ["career_id", "person_id", "organization_id", "role", "start", "end"], "career_id")),
        "sources": len(merge(MASTER / "source.csv", sources, ["source_id", "title", "publisher", "url", "accessed_at"], "source_id")),
        "evidence": len(merge(MASTER / "evidence.csv", evidence, EVIDENCE_HEADERS, "record_id")),
    }
    apply_corrections(MASTER / "career.csv", ["career_id", "person_id", "organization_id", "role", "start", "end"])

    holds = len(read(PACKET / "hold_review.csv"))
    counts["approvals"] = len(merge(MASTER / "approval_records.csv", [{
        "approval_id": APPROVAL_ID, "batch": "Approval Sprint 015", "verified_commit": VERIFIED_COMMIT,
        "approved_scope": f"3 existing persons (渡邊雄太 P000103 Tier2, 田臥勇太 P000105 Tier1, 富永啓生 P000106 Tier2) with career additions, "
                           f"{len(careers)} careers, {len(evidence)} supported evidence, {len(orgs)} referenced organizations, "
                           f"2 master career period corrections (C000354, C000363)",
        "excluded_scope": f"{holds} HOLD issues", "approved_by": "Yuichi", "approved_at": APPROVED_AT,
        "approval_reference": "data/verified/approval_sprint_015/master_approval.md",
    }], ["approval_id", "batch", "verified_commit", "approved_scope", "excluded_scope", "approved_by", "approved_at", "approval_reference"], "approval_id"))

    report_path = MASTER / "master_build_report.md"
    rep = report_path.read_text(encoding="utf-8")
    rep = rep.replace(
        f"- `{'APP-AS018-20261008-01'}`：Approval Sprint 018（八村塁の新規登録、馬場雄大・比江島慎の海外Career追加、海外公式資料、Tier 2）",
        f"- `APP-AS018-20261008-01`：Approval Sprint 018（八村塁の新規登録、馬場雄大・比江島慎の海外Career追加、海外公式資料、Tier 2）\n"
        f"- `{APPROVAL_ID}`：Approval Sprint 015（渡邊雄太・田臥勇太・富永啓生の海外Career追加、"
        f"Master期間訂正2件、NBA公式・大学公式資料、Tier 1/2）")
    rep = re.sub(r"- Organization：\d+件", f"- Organization：{counts['orgs']}件", rep)
    rep = re.sub(r"- Career：\d+件", f"- Career：{counts['careers']}件", rep)
    rep = re.sub(r"- Source：\d+件", f"- Source：{counts['sources']}件", rep)
    rep = re.sub(r"- Evidence：\d+件", f"- Evidence：{counts['evidence']}件", rep)
    rep = re.sub(r"- Approval：\d+件", f"- Approval：{counts['approvals']}件", rep)
    report_path.write_text(rep, encoding="utf-8")
    print(f"Approval Sprint 015 applied: +{len(careers)} careers, +2 corrections -> {counts}")


if __name__ == "__main__":
    main()
