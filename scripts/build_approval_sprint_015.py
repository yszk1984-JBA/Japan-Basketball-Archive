#!/usr/bin/env python3
"""Build the Human Approval packet for Approval Sprint 015 (渡邊・田臥・富永 overseas).

Scope: batch_007 wave_12 VERIFIED -- 11 new Careers for MASTER persons P000103,
P000105, P000106, the Organizations they reference (8 not yet in MASTER), and
period corrections for 2 existing MASTER school Careers. Tier proposal per
person: Tier 2 when a MASTER value is corrected, otherwise Tier 1. Never
writes data/master and never records an approval.
"""

from __future__ import annotations

import csv
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V = ROOT / "data/verified/batch_007_wave_12"
OUT = ROOT / "data/verified/approval_sprint_015"
VERIFIED_COMMIT = "188db92"
CREATED_AT = "2026-10-08"


def read(p: Path) -> list[dict[str, str]]:
    with p.open(encoding="utf-8-sig", newline="") as h:
        return list(csv.DictReader(h))


def write(name: str, rows: list[dict[str, str]], headers: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / name).open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=headers, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    files = [str(p.relative_to(ROOT)) for p in sorted(V.glob("*")) if p.is_file()]
    if subprocess.run(["git", "diff", "--quiet", VERIFIED_COMMIT, "--", *files], cwd=ROOT).returncode:
        raise SystemExit("VERIFIED snapshot changed")
    m_people = {r["person_id"]: r["name"] for r in read(ROOT / "data/master/person.csv")}
    m_orgs = {r["organization_id"]: r["name"] for r in read(ROOT / "data/master/organization.csv")}
    m_careers = {r["career_id"]: r for r in read(ROOT / "data/master/career.csv")}
    careers = read(V / "career_verified.csv")
    orgs = {r["organization_id"]: r["name"] for r in read(V / "organization_verified.csv")}
    evidence = read(V / "evidence_records.csv") + read(V / "master_correction_evidence.csv")
    corrections = read(V / "master_corrections.csv")
    sources = read(V / "source_references.csv")
    src_all = {r["source_id"]: r for r in read(ROOT / "data/candidate/batch_007/wave_12/source_references.csv")}
    for e in evidence:
        if e["source_id"] not in {s["source_id"] for s in sources}:
            sources.append(src_all[e["source_id"]])
    issues = read(V / "issue_dispositions.csv")

    errors = []
    if any(c["person_id"] not in m_people for c in careers):
        errors.append("MasterにないPerson")
    if {c["career_id"] for c in careers} & set(m_careers):
        errors.append("既存Master Career IDと重複")
    for c in corrections:
        m = m_careers.get(c["career_id"])
        if not m or (m["start"], m["end"]) != (c["old_start"], c["old_end"]):
            errors.append(f"{c['career_id']}: 訂正前の値がMasterと不一致")
    for oid, name in orgs.items():
        if oid in m_orgs and m_orgs[oid] != name:
            errors.append(f"{oid}: Master名と不一致")
    if any(e["assessment"] != "SUPPORTED" for e in evidence):
        errors.append("SUPPORTEDでないEvidence")

    corr_people = {c["person_id"] for c in corrections}
    person_review = [{"person_id": p, "name": m_people[p], "tier_proposal": "Tier 2" if p in corr_people else "Tier 1",
                      "tier_reasons": "既存Masterの値（学校の在学期間）を訂正する案を含む" if p in corr_people else "Careerの追加のみ（NBA公式の記録）",
                      "added_careers": str(sum(c["person_id"] == p for c in careers)),
                      "corrections": str(sum(c["person_id"] == p for c in corrections)), "verified_commit": VERIFIED_COMMIT}
                     for p in sorted({c["person_id"] for c in careers})]
    career_review = [{**c, "name": m_people[c["person_id"]], "organization_name": orgs[c["organization_id"]],
                      "evidence_count": str(sum(e["entity_id"] == c["career_id"] for e in evidence))} for c in careers]
    org_review = [{"organization_id": o, "name": n, "status": "Master既存" if o in m_orgs else "新規（Master未登録）"} for o, n in orgs.items()]
    write("person_review.csv", person_review, list(person_review[0].keys()))
    write("career_review.csv", career_review, ["career_id", "person_id", "name", "organization_id", "organization_name", "role", "start", "end", "evidence_count"])
    write("organization_review.csv", org_review, ["organization_id", "name", "status"])
    write("master_correction_review.csv", corrections, list(corrections[0].keys()))
    write("evidence_review.csv", evidence, list(evidence[0].keys()))
    write("source_review.csv", sources, ["source_id", "title", "publisher", "url", "accessed_at"])
    write("hold_review.csv", issues, list(issues[0].keys()))
    (OUT / "validation_report.md").write_text("\n".join([
        "# Approval Sprint 015 検証レポート", "", f"作成日：{CREATED_AT}", "",
        f"- 検証：{'PASS' if not errors else 'FAIL'}", f"- エラー：{len(errors)}件",
        f"- 対象人物：{len(person_review)}名（Tier 1案：{sum(p['tier_proposal'] == 'Tier 1' for p in person_review)}名、Tier 2案：{sum(p['tier_proposal'] == 'Tier 2' for p in person_review)}名）", f"- 追加Career：{len(careers)}件", f"- Masterの期間訂正：{len(corrections)}件",
        f"- Organization：{len(org_review)}件（Master未登録{sum(o['status'] != 'Master既存' for o in org_review)}件）",
        f"- Evidence：{len(evidence)}件", f"- HOLD Issue：{len(issues)}件", "", "## エラー", "",
        *([f"- {e}" for e in errors] or ["- なし"])]) + "\n", encoding="utf-8")
    if errors:
        raise SystemExit(errors)
    rows = "\n".join(f"| {m_people[c['person_id']]} | {c['career_id']} | {orgs[c['organization_id']]}{'（新規）' if c['organization_id'] not in m_orgs else ''} | {c['start']}〜{c['end']} |" for c in careers)
    corr = "\n".join(f"| {m_people[c['person_id']]} | {c['career_id']} | {c['organization_name']} | 未記録 | {c['new_start']}〜{c['new_end']} |" for c in corrections)
    tiers = "\n".join(f"- {p['name']}：{p['tier_proposal']}（{p['tier_reasons']}）" for p in person_review)
    (OUT / "README.md").write_text(f"""# Approval Sprint 015

作成日：{CREATED_AT}

状態：HUMAN APPROVAL待ち。MASTER未反映・公開未実施。

## 対象

渡邊雄太（P000103）・田臥勇太（P000105）・富永啓生（P000106）の海外経歴（batch_007 wave_12、Yuichiの指示 2026-10-08「3人まとめて進めましょう」）。VERIFIED snapshot commit：`{VERIFIED_COMMIT}`。

### 追加するCareer

| 選手 | Career | Organization | 期間 |
| --- | --- | --- | --- |
{rows}

### Masterの期間の訂正（`master_correction_review.csv`）

| 選手 | Career | 学校 | 現在 | 訂正後 |
| --- | --- | --- | --- | --- |
{corr}

## Tier判定案

{tiers}

## 判断範囲

`evidence_review.csv`のSUPPORTED Evidenceに対応するCareer・Organizationと、`master_correction_review.csv`の期間訂正2件。`hold_review.csv`の{len(issues)}件（渡邊の2023-24の2クラブ在籍とGリーグ出場、田臥のABA・ブレックス期、マッドアンツの改称）は対象外。

この資料の作成はHuman Approvalではない。Yuichiが対象版・範囲・Tierを明示して承認した後に限り、Masterへ反映できる。
""", encoding="utf-8")
    print("Approval Sprint 015 packet:", len(careers), "careers,", len(corrections), "corrections,", len(evidence), "evidence")


if __name__ == "__main__":
    main()
