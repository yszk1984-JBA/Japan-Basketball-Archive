#!/usr/bin/env python3
"""Build the Human Approval packet for Approval Sprint 011 (河村勇輝 NBA update).

Scope: batch_004 wave_07 VERIFIED -- 2 new Careers (シカゴ・ブルズ,
ロサンゼルス・クリッパーズ) for MASTER person P000064, the 2 Organizations
they reference (not yet in MASTER), and period corrections for 3 existing
MASTER Careers. Tier proposal: Tier 2 (it changes existing MASTER values).
Never writes data/master and never records an approval.
"""

from __future__ import annotations

import csv
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V = ROOT / "data/verified/batch_004_wave_07"
OUT = ROOT / "data/verified/approval_sprint_011"
VERIFIED_COMMIT = "5b98773"
CREATED_AT = "2026-10-03"


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
    src_all = {r["source_id"]: r for r in read(ROOT / "data/candidate/batch_004/wave_07/source_references.csv")}
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

    person_review = [{"person_id": "P000064", "name": m_people["P000064"], "tier_proposal": "Tier 2",
                      "tier_reasons": "既存Masterの値（期間）を変更する訂正を含む／一部の項目（ブルズの契約解除日）は公式以外の記録のみ（issueとして保留、承認対象外）",
                      "added_careers": str(len(careers)), "corrections": str(len(corrections)), "verified_commit": VERIFIED_COMMIT}]
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
        "# Approval Sprint 011 検証レポート", "", f"作成日：{CREATED_AT}", "",
        f"- 検証：{'PASS' if not errors else 'FAIL'}", f"- エラー：{len(errors)}件",
        f"- 対象人物：1名（Tier 2案）", f"- 追加Career：{len(careers)}件", f"- Masterの期間訂正：{len(corrections)}件",
        f"- Organization：{len(org_review)}件（Master未登録{sum(o['status'] != 'Master既存' for o in org_review)}件）",
        f"- Evidence：{len(evidence)}件", f"- HOLD Issue：{len(issues)}件", "", "## エラー", "",
        *([f"- {e}" for e in errors] or ["- なし"])]) + "\n", encoding="utf-8")
    if errors:
        raise SystemExit(errors)
    rows = "\n".join(f"| {c['career_id']} | {orgs[c['organization_id']]} | {c['start']}〜{c['end']} |" for c in careers)
    corr = "\n".join(f"| {c['career_id']} | {c['organization_name']} | 未記録 | {c['new_start']}〜{c['new_end']} |" for c in corrections)
    (OUT / "README.md").write_text(f"""# Approval Sprint 011

作成日：{CREATED_AT}

状態：HUMAN APPROVAL待ち。MASTER未反映・公開未実施。

## 対象

河村勇輝（P000064）のNBA経歴アップデート（batch_004 wave_07、Yuichiの指示 2026-10-03）。VERIFIED snapshot commit：`{VERIFIED_COMMIT}`。

### 追加するCareer

| Career | クラブ | 期間 |
| --- | --- | --- |
{rows}

Organization：シカゴ・ブルズ（ORG000139）、ロサンゼルス・クリッパーズ（ORG000140）はMaster未登録のため、あわせて追加する。

### Masterの期間の訂正（`master_correction_review.csv`）

| Career | クラブ | 現在 | 訂正後 |
| --- | --- | --- | --- |
{corr}

## Tier判定案

Tier 2（丁寧確認）：既存Masterの値を変更する訂正を含むため。

## 判断範囲

`evidence_review.csv`のSUPPORTED Evidenceに対応するCareer・Organizationと、`master_correction_review.csv`の期間訂正3件。`hold_review.csv`の{len(issues)}件（ブルズの2回の契約と解除、クリッパーズのExhibit 10契約の行方、Gリーグ派遣）は対象外。

クリッパーズの契約はExhibit 10（無保証のキャンプ契約）で、開幕までに変わりうる。開幕後にNBA公式ロスターで再確認する。

この資料の作成はHuman Approvalではない。Yuichiが対象版・範囲・Tierを明示して承認した後に限り、Masterへ反映できる。
""", encoding="utf-8")
    print("Approval Sprint 011 packet:", len(careers), "careers,", len(corrections), "corrections,", len(evidence), "evidence")


if __name__ == "__main__":
    main()
