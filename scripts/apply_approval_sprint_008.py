#!/usr/bin/env python3
"""Apply Yuichi's explicit Approval Sprint 008 decision to MASTER.

Adds 264 past-club Careers (batch_031) for existing MASTER persons, the
Organizations they reference, their SUPPORTED evidence and sources, and
applies the approved ORG000222 name correction. Refuses to run unless the
packet is unchanged since its review commit and master_approval.md holds
Yuichi's approval text for this packet/VERIFIED commit."""

from __future__ import annotations

import csv
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "data/verified/approval_sprint_008"
MASTER = ROOT / "data/master"
PACKET_COMMIT = "2164a97"
VERIFIED_COMMIT = "f53dbd3"
APPROVAL_ID = "APP-AS008-20260929-01"
CORRECTION_RECORD = "data/master/corrections/2026-09-29_org000222_name.md"


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


def verify_approval() -> None:
    tracked = ["README.md", "approval_request.md", "person_review.csv", "career_review.csv", "organization_review.csv",
               "organization_correction_review.csv", "evidence_review.csv", "source_review.csv", "hold_review.csv", "validation_report.md"]
    if subprocess.run(["git", "diff", "--quiet", PACKET_COMMIT, "--", *[str((PACKET / n).relative_to(ROOT)) for n in tracked]], cwd=ROOT).returncode:
        raise SystemExit("Approval Sprint 008 differs from the approved review packet")
    text = (PACKET / "master_approval.md").read_text(encoding="utf-8")
    required = [APPROVAL_ID, PACKET_COMMIT, VERIFIED_COMMIT, "承認者：Yuichi",
                "Approval Sprint 008を、版 f53dbd3、Tierは案どおり（Tier 1 74名／Tier 2 34名）で、SUPPORTED Evidenceの範囲とORG000222の名称訂正をMasterに反映してよい。HOLDは対象外。"]
    if any(v not in text for v in required):
        raise SystemExit("Approval Sprint 008 approval record is incomplete")


def main() -> None:
    verify_approval()
    careers = [{k: r[k] for k in ["career_id", "person_id", "organization_id", "role", "start", "end"]} for r in read(PACKET / "career_review.csv")]
    orgs = [{"organization_id": r["organization_id"], "name": r["name"]} for r in read(PACKET / "organization_review.csv")]
    sources = {r["source_id"]: {k: r[k] for k in ["source_id", "title", "publisher", "url", "accessed_at"]} for r in read(PACKET / "source_review.csv")}
    evidence = [{k: r[k] for k in ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id",
                                   "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"]} for r in read(PACKET / "evidence_review.csv")]

    # 1) approved name correction (existing MASTER row)
    org_rows = read(MASTER / "organization.csv")
    for fix in read(PACKET / "organization_correction_review.csv"):
        row = next(r for r in org_rows if r["organization_id"] == fix["organization_id"])
        if row["name"] != fix["old_name"]:
            raise SystemExit(f"{fix['organization_id']}: MASTER name is not the approved old name")
        row["name"] = fix["new_name"]
    write(MASTER / "organization.csv", ["organization_id", "name"], org_rows)

    master_people = {r["person_id"] for r in read(MASTER / "person.csv")}
    if any(c["person_id"] not in master_people for c in careers):
        raise SystemExit("Career for a person not in MASTER")
    m_orgs = merge(MASTER / "organization.csv", orgs, ["organization_id", "name"], "organization_id")
    m_careers = merge(MASTER / "career.csv", careers, ["career_id", "person_id", "organization_id", "role", "start", "end"], "career_id")
    m_sources = merge(MASTER / "source.csv", list(sources.values()), ["source_id", "title", "publisher", "url", "accessed_at"], "source_id")
    m_evidence = merge(MASTER / "evidence.csv", evidence, ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id",
                                                           "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"], "record_id")
    m_people = read(MASTER / "person.csv")
    m_approvals = merge(MASTER / "approval_records.csv", [{
        "approval_id": APPROVAL_ID, "batch": "Approval Sprint 008", "verified_commit": VERIFIED_COMMIT,
        "approved_scope": "264 careers for 108 existing persons (Tier 1: 74, Tier 2: 34), 1056 supported evidence, 6 new organizations, ORG000222 name correction",
        "excluded_scope": "82 HOLD issues", "approved_by": "Yuichi", "approved_at": "2026-09-29",
        "approval_reference": "data/verified/approval_sprint_008/master_approval.md",
    }], ["approval_id", "batch", "verified_commit", "approved_scope", "excluded_scope", "approved_by", "approved_at", "approval_reference"], "approval_id")

    (ROOT / CORRECTION_RECORD).write_text("""# Master訂正記録：ORG000222の名称訂正

作成日：2026-09-29
承認：Approval Sprint 008（`APP-AS008-20260929-01`、Yuichi、2026-09-29）

## 内容

- `data/master/organization.csv`：`ORG000222`の`name`を「トライフォース岡山」→「トライフープ岡山」に訂正

## 経緯

batch_022（尽誠学園、2026-09-26）で、要約型Web取得ツールが返した英訳「Triforce Okayama」から「トライフォース岡山」と登録し、Approval Sprint 007でMasterへ反映された。2026-09-29の深掘り（batch_031）で、B.LEAGUE公式の選手一覧（出身校タグ）・公式順位表（TeamID=1639、2019-20〜2026-27）の表記がいずれも「トライフープ岡山」であることを確認した。

## 影響範囲

- ORG000222を参照するCareer（若狭功希・笠井康平ほか）のIDや値は変更していない（Organization名のみの訂正）
- `data/candidate/`・`data/verified/`の過去スナップショット（batch_022、Approval Sprint 007）は変更しない
""", encoding="utf-8")

    (MASTER / "master_build_report.md").write_text(f"""# MASTER反映レポート

作成日：2026-09-29

## 反映済み承認

- `APP-B005-20260921-01`：Batch 005 Wave 1
- `APP-AS001-20260921-01`〜`APP-AS007-20260926-01`：Approval Sprint 001〜007
- `{APPROVAL_ID}`：Approval Sprint 008（B.LEAGUE期の過去所属クラブ深掘り、batch_031、2段階承認の初回）、ORG000222名称訂正を含む

## MASTER件数

- Person：{len(m_people)}件
- Organization：{len(m_orgs)}件
- Career：{len(m_careers)}件
- Source：{len(m_sources)}件
- Evidence：{len(m_evidence)}件
- Approval：{len(m_approvals)}件

Approval Sprint 008の82件のHOLD Issueはmasterに含めていない。公開サイト反映は別工程で行う。
""", encoding="utf-8")
    print(f"MASTER updated: {len(m_people)} persons, {len(m_orgs)} orgs, {len(m_careers)} careers, {len(m_evidence)} evidence, {len(m_approvals)} approvals")


if __name__ == "__main__":
    main()
