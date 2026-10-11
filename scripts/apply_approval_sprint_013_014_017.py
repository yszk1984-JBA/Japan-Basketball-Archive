#!/usr/bin/env python3
"""Apply Yuichi's explicit Approval Sprint 013 / 014 / 017 decision to MASTER.

Scope: school Careers of existing MASTER persons (batch_032 wave_05 / wave_06,
batch_033 wave_06). Approval records:
data/verified/approval_sprint_0{13,14,17}/master_approval.md.
Excluded: all HOLD issues, and (Yuichi: 「外す」) 濱田貴流馬's 近畿大学 Career
C002762 with its evidence.
"""

from __future__ import annotations

import csv
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "data/master"
APPROVED_AT = "2026-10-11"
TRACKED = ["README.md", "person_review.csv", "career_review.csv", "organization_review.csv",
           "evidence_review.csv", "source_review.csv", "hold_review.csv", "validation_report.md"]
SPRINTS = [
    # sprint, approval id, packet commit, verified commit, expected new orgs, label
    ("013", "APP-AS013-20261011-01", "cca4f9c", "03cc094", 5, "B.PREMIER選手18名の出身校（クラブ公式サイト、batch_032 wave_05）"),
    ("014", "APP-AS014-20261011-01", "89a7e60", "28291b5", 1, "B.PREMIER選手15名の出身高校（batch_032 wave_06）"),
    ("017", "APP-AS017-20261011-01", "97664f0", "db58da1", 11, "B.ONE選手20名の出身校（batch_033 wave_06、濱田貴流馬の近畿大学を除く）"),
]
EXCLUDED_CAREERS = {"C002762"}
CAREER_H = ["career_id", "person_id", "organization_id", "role", "start", "end"]
SOURCE_H = ["source_id", "title", "publisher", "url", "accessed_at"]
EVIDENCE_H = ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id",
              "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"]
APPROVAL_H = ["approval_id", "batch", "verified_commit", "approved_scope", "excluded_scope", "approved_by",
              "approved_at", "approval_reference"]
VERBATIM = ["Approval Sprint 013・014・017の承認する", "HOLDは対象外", "`外す`"]


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as h:
        return list(csv.DictReader(h))


def write(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=headers, lineterminator="\n")
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
    people = {r["person_id"] for r in read(MASTER / "person.csv")}
    m_orgs = {r["organization_id"] for r in read(MASTER / "organization.csv")}
    all_c, all_o, all_s, all_e, approvals, labels = [], [], [], [], [], []
    for s, aid, pkt, ver, new_orgs, label in SPRINTS:
        packet = ROOT / f"data/verified/approval_sprint_{s}"
        paths = [str((packet / n).relative_to(ROOT)) for n in TRACKED]
        if subprocess.run(["git", "diff", "--quiet", pkt, "--", *paths], cwd=ROOT).returncode:
            raise SystemExit(f"Approval Sprint {s} packet differs from the reviewed commit {pkt}")
        text = (packet / "master_approval.md").read_text(encoding="utf-8")
        for v in (aid, pkt, ver, "承認者：Yuichi", *VERBATIM):
            if v not in text:
                raise SystemExit(f"Approval Sprint {s} approval record is incomplete ({v})")
        careers = [{k: r[k] for k in CAREER_H} for r in read(packet / "career_review.csv")
                   if r["career_id"] not in EXCLUDED_CAREERS]
        evidence = [{k: r[k] for k in EVIDENCE_H} for r in read(packet / "evidence_review.csv")
                    if r["entity_id"] not in EXCLUDED_CAREERS]
        if any(e["assessment"] != "SUPPORTED" for e in evidence):
            raise SystemExit(f"{s}: non-SUPPORTED evidence")
        if any(c["person_id"] not in people for c in careers):
            raise SystemExit(f"{s}: person not in MASTER")
        cids = {c["career_id"] for c in careers}
        if any(e["entity_id"] not in cids for e in evidence) or any(not any(e["entity_id"] == c for e in evidence) for c in cids):
            raise SystemExit(f"{s}: evidence/career mismatch")
        used_src = {e["source_id"] for e in evidence}
        sources = [{k: r[k] for k in SOURCE_H} for r in read(packet / "source_review.csv") if r["source_id"] in used_src]
        if {x["source_id"] for x in sources} != used_src:
            raise SystemExit(f"{s}: missing source")
        used_org = {c["organization_id"] for c in careers}
        orgs = [{"organization_id": r["organization_id"], "name": r["name"]} for r in read(packet / "organization_review.csv")
                if r["organization_id"] in used_org]
        if {o["organization_id"] for o in orgs} != used_org:
            raise SystemExit(f"{s}: missing organization")
        n_new = sum(o["organization_id"] not in m_orgs for o in orgs)
        if n_new != new_orgs:
            raise SystemExit(f"{s}: expected {new_orgs} new organizations, got {n_new}")
        holds = len(read(packet / "hold_review.csv"))
        excluded = f"{holds} HOLD issues" + ("; career C002762 (濱田貴流馬 近畿大学) and its 2 evidence records" if s == "017" else "")
        approvals.append({"approval_id": aid, "batch": f"Approval Sprint {s}", "verified_commit": ver,
                          "approved_scope": f"{len({c['person_id'] for c in careers})} existing persons, {len(careers)} school careers, "
                                            f"{len(evidence)} supported evidence, {len(orgs)} referenced organizations ({n_new} new)",
                          "excluded_scope": excluded, "approved_by": "Yuichi", "approved_at": APPROVED_AT,
                          "approval_reference": f"data/verified/approval_sprint_{s}/master_approval.md"})
        labels.append(f"- `{aid}`：Approval Sprint {s}（{label}、Career {len(careers)}件）")
        all_c += careers; all_o += orgs; all_s += sources; all_e += evidence
        print(s, len(careers), "careers", len(evidence), "evidence", len(orgs), "orgs", n_new, "new")

    counts = {
        "orgs": merge(MASTER / "organization.csv", all_o, ["organization_id", "name"], "organization_id"),
        "careers": merge(MASTER / "career.csv", all_c, CAREER_H, "career_id"),
        "sources": merge(MASTER / "source.csv", all_s, SOURCE_H, "source_id"),
        "evidence": merge(MASTER / "evidence.csv", all_e, EVIDENCE_H, "record_id"),
        "approvals": merge(MASTER / "approval_records.csv", approvals, APPROVAL_H, "approval_id"),
    }
    report_path = MASTER / "master_build_report.md"
    rep = report_path.read_text(encoding="utf-8")
    anchor = "\n\n## MASTER件数"
    rep = rep.replace(anchor, "\n" + "\n".join(labels) + anchor, 1)
    rep = re.sub(r"作成日：\S+", f"作成日：{APPROVED_AT}", rep, count=1)
    for k, lab in (("orgs", "Organization"), ("careers", "Career"), ("sources", "Source"), ("evidence", "Evidence"), ("approvals", "Approval")):
        rep = re.sub(rf"- {lab}：\d+件", f"- {lab}：{counts[k]}件", rep)
    report_path.write_text(rep, encoding="utf-8")
    print("applied:", counts)


if __name__ == "__main__":
    main()
