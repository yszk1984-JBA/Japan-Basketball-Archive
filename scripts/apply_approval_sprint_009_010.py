#!/usr/bin/env python3
"""Apply Yuichi's explicit Approval Sprint 009 and 010 decisions to MASTER.

Sprint 009 (batch_032 + batch_007 re-check, 168 persons) is applied first,
then Sprint 010 (batch_033, 182 persons), because 010 references
Organizations created in 009. Each packet must be unchanged since its review
commit, and master_approval.md must hold Yuichi's approval text for that
packet / VERIFIED commit. New persons, their Careers, the referenced
Organizations, SUPPORTED Evidence and Sources are added; nothing already in
MASTER is changed. HOLD issues are not applied.
"""

from __future__ import annotations

import csv
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "data/master"
APPROVAL_TEXT = """Sprint 009は 6d497b2、Sprint 010は a506070 です。
Tierの確定： 判定案どおり（009はTier 1が106名・Tier 2が62名、010はTier 1が131名・Tier 2が51名）
範囲： SUPPORTED Evidenceの範囲をMasterに反映してよいこと。HOLDは対象外であること。"""
SPRINTS = [
    {"no": "009", "packet": ROOT / "data/verified/approval_sprint_009", "packet_commit": "a8427f8",
     "verified_commit": "6d497b2", "approval_id": "APP-AS009-20260930-01", "tiers": (106, 62)},
    {"no": "010", "packet": ROOT / "data/verified/approval_sprint_010", "packet_commit": "39e8233",
     "verified_commit": "a506070", "approval_id": "APP-AS010-20260930-01", "tiers": (131, 51)},
]
TRACKED = ["README.md", "approval_request.md", "person_review.csv", "career_review.csv", "organization_review.csv",
           "evidence_review.csv", "source_review.csv", "hold_review.csv", "validation_report.md"]
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
        if r[key] in merged and merged[r[key]] != r:
            raise SystemExit(f"MASTER conflict: {key}={r[key]}")
        merged[r[key]] = r
    rows = [merged[k] for k in sorted(merged)]
    write(path, headers, rows)
    return rows


def verify(s: dict) -> None:
    paths = [str((s["packet"] / n).relative_to(ROOT)) for n in TRACKED]
    if subprocess.run(["git", "diff", "--quiet", s["packet_commit"], "--", *paths], cwd=ROOT).returncode:
        raise SystemExit(f"Approval Sprint {s['no']} differs from the reviewed packet")
    text = (s["packet"] / "master_approval.md").read_text(encoding="utf-8")
    for v in (s["approval_id"], s["packet_commit"], s["verified_commit"], "承認者：Yuichi", APPROVAL_TEXT):
        if v not in text:
            raise SystemExit(f"Approval Sprint {s['no']} approval record is incomplete")
    tiers = [r["tier_proposal"] for r in read(s["packet"] / "person_review.csv")]
    if (tiers.count("Tier 1"), tiers.count("Tier 2")) != s["tiers"]:
        raise SystemExit(f"Approval Sprint {s['no']}: Tier counts differ from the approved ones")


def apply(s: dict) -> dict[str, int]:
    verify(s)
    p = s["packet"]
    persons = [{"person_id": r["person_id"], "name": r["name"]} for r in read(p / "person_review.csv")]
    careers = [{k: r[k] for k in ["career_id", "person_id", "organization_id", "role", "start", "end"]} for r in read(p / "career_review.csv")]
    orgs = [{"organization_id": r["organization_id"], "name": r["name"]} for r in read(p / "organization_review.csv")]
    sources = [{k: r[k] for k in ["source_id", "title", "publisher", "url", "accessed_at"]} for r in read(p / "source_review.csv")]
    evidence = [{k: r[k] for k in EVIDENCE_HEADERS} for r in read(p / "evidence_review.csv")]
    if any(e["assessment"] != "SUPPORTED" for e in evidence):
        raise SystemExit("non-SUPPORTED evidence in packet")
    existing_people = {r["person_id"] for r in read(MASTER / "person.csv")}
    if any(r["person_id"] in existing_people for r in persons):
        raise SystemExit(f"Sprint {s['no']}: person already in MASTER")
    counts = {
        "people": len(merge(MASTER / "person.csv", persons, ["person_id", "name"], "person_id")),
        "orgs": len(merge(MASTER / "organization.csv", orgs, ["organization_id", "name"], "organization_id")),
        "careers": len(merge(MASTER / "career.csv", careers, ["career_id", "person_id", "organization_id", "role", "start", "end"], "career_id")),
        "sources": len(merge(MASTER / "source.csv", sources, ["source_id", "title", "publisher", "url", "accessed_at"], "source_id")),
        "evidence": len(merge(MASTER / "evidence.csv", evidence, EVIDENCE_HEADERS, "record_id")),
    }
    holds = len(read(p / "hold_review.csv"))
    t1, t2 = s["tiers"]
    counts["approvals"] = len(merge(MASTER / "approval_records.csv", [{
        "approval_id": s["approval_id"], "batch": f"Approval Sprint {s['no']}", "verified_commit": s["verified_commit"],
        "approved_scope": f"{len(persons)} persons (Tier 1: {t1}, Tier 2: {t2}), {len(careers)} careers, {len(evidence)} supported evidence, {len(orgs)} referenced organizations",
        "excluded_scope": f"{holds} HOLD issues", "approved_by": "Yuichi", "approved_at": "2026-09-30",
        "approval_reference": f"data/verified/approval_sprint_{s['no']}/master_approval.md",
    }], ["approval_id", "batch", "verified_commit", "approved_scope", "excluded_scope", "approved_by", "approved_at", "approval_reference"], "approval_id"))
    print(f"Sprint {s['no']} applied: +{len(persons)} persons, +{len(careers)} careers -> {counts}")
    return counts


def main() -> None:
    counts = {}
    for s in SPRINTS:
        counts = apply(s)
    (MASTER / "master_build_report.md").write_text(f"""# MASTER反映レポート

作成日：2026-09-30

## 反映済み承認

- `APP-B005-20260921-01`：Batch 005 Wave 1
- `APP-AS001-20260921-01`〜`APP-AS008-20260929-01`：Approval Sprint 001〜008
- `APP-AS009-20260930-01`：Approval Sprint 009（B.PREMIERロスター起点の横展開、batch_032＋batch_007再確認、168名）
- `APP-AS010-20260930-01`：Approval Sprint 010（B.ONEロスター起点の横展開、batch_033、182名）

## MASTER件数

- Person：{counts['people']}件
- Organization：{counts['orgs']}件
- Career：{counts['careers']}件
- Source：{counts['sources']}件
- Evidence：{counts['evidence']}件
- Approval：{counts['approvals']}件

Approval Sprint 009・010のHOLD Issueはmasterに含めていない。公開サイト反映は別工程で行う。
""", encoding="utf-8")


if __name__ == "__main__":
    main()
