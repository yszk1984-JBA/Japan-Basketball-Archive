#!/usr/bin/env python3
"""Build the Human Approval packet for Approval Sprint 017 (出身校, club sites).

Scope: batch_032 wave_05 VERIFIED -- 18 school Careers for 18 MASTER persons
and the 15 Organizations they reference (5 not yet in MASTER). No MASTER value
is changed. Tier proposal per person: Tier 1 when the school is read from a
出身校 field of the club's player page; Tier 2 when it is read from prose or
an abbreviation (open issue on that Career). Never writes data/master and
never records an approval.
"""

from __future__ import annotations

import csv
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V = ROOT / "data/verified/batch_033_wave_06"
OUT = ROOT / "data/verified/approval_sprint_017"
VERIFIED_COMMIT = "db58da1"
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
    m_careers = read(ROOT / "data/master/career.csv")
    careers = read(V / "career_verified.csv")
    orgs = {r["organization_id"]: r["name"] for r in read(V / "organization_verified.csv")}
    evidence = read(V / "evidence_records.csv")
    sources = read(V / "source_references.csv")
    issues = read(V / "issue_dispositions.csv")
    flagged = {i["related_id"] for i in issues}

    errors = []
    if any(c["person_id"] not in m_people for c in careers):
        errors.append("MasterにないPerson")
    if {c["career_id"] for c in careers} & {c["career_id"] for c in m_careers}:
        errors.append("既存Master Career IDと重複")
    have = {(c["person_id"], c["organization_id"]) for c in m_careers}
    if any((c["person_id"], c["organization_id"]) in have for c in careers):
        errors.append("同じ学校のCareerがMasterに既存")
    for oid, name in orgs.items():
        if oid in m_orgs and m_orgs[oid] != name:
            errors.append(f"{oid}: Master名と不一致")
        if oid not in m_orgs and name in m_orgs.values():
            errors.append(f"{oid}: 同名のOrganizationがMasterに既存")
    if any(e["assessment"] != "SUPPORTED" for e in evidence):
        errors.append("SUPPORTEDでないEvidence")

    flagged_people = {c["person_id"] for c in careers if c["career_id"] in flagged}
    person_review = []
    for pid in dict.fromkeys(c["person_id"] for c in careers):
        t2 = pid in flagged_people
        person_review.append({"person_id": pid, "name": m_people[pid], "tier_proposal": "Tier 2" if t2 else "Tier 1",
                              "tier_reasons": "同名校・紹介文の記述・部に所属せず・表記ゆれのいずれか（issueあり）" if t2 else "クラブ公式の出身校欄・経歴欄の表記どおり",
                              "added_careers": str(sum(c["person_id"] == pid for c in careers)), "verified_commit": VERIFIED_COMMIT})
    t1 = sum(p["tier_proposal"] == "Tier 1" for p in person_review)
    t2 = len(person_review) - t1
    career_review = [{**c, "name": m_people[c["person_id"]], "organization_name": orgs[c["organization_id"]],
                      "organization_status": "Master既存" if c["organization_id"] in m_orgs else "新規",
                      "evidence_count": str(sum(e["entity_id"] == c["career_id"] for e in evidence))} for c in careers]
    org_review = [{"organization_id": o, "name": n, "status": "Master既存" if o in m_orgs else "新規（Master未登録）"} for o, n in orgs.items()]
    write("person_review.csv", person_review, list(person_review[0].keys()))
    write("career_review.csv", career_review, ["career_id", "person_id", "name", "organization_id", "organization_name",
                                               "organization_status", "role", "start", "end", "evidence_count"])
    write("organization_review.csv", org_review, ["organization_id", "name", "status"])
    write("evidence_review.csv", evidence, list(evidence[0].keys()))
    write("source_review.csv", sources, ["source_id", "title", "publisher", "url", "accessed_at"])
    write("hold_review.csv", issues, list(issues[0].keys()))
    new_orgs = [o for o in org_review if o["status"] != "Master既存"]
    (OUT / "validation_report.md").write_text("\n".join([
        "# Approval Sprint 017 検証レポート", "", f"作成日：{CREATED_AT}", "",
        f"- 検証：{'PASS' if not errors else 'FAIL'}", f"- エラー：{len(errors)}件",
        f"- 対象人物：{len(person_review)}名（Tier 1案：{t1}名、Tier 2案：{t2}名）", f"- 追加Career：{len(careers)}件",
        f"- Organization：{len(org_review)}件（Master未登録{len(new_orgs)}件）",
        f"- Evidence：{len(evidence)}件", f"- HOLD Issue：{len(issues)}件", "- Masterの既存値の変更：なし", "", "## エラー", "",
        *([f"- {e}" for e in errors] or ["- なし"])]) + "\n", encoding="utf-8")
    if errors:
        raise SystemExit(errors)
    tier = {p["person_id"]: p["tier_proposal"] for p in person_review}
    rows = "\n".join(f"| {r['name']} | {r['organization_name']}{'（新規）' if r['organization_status'] == '新規' else ''} | "
                     f"{r['start'] + '〜' + r['end'] if r['start'] else '（期間なし）'} | {tier[r['person_id']]} |" for r in career_review)
    (OUT / "README.md").write_text(f"""# Approval Sprint 017

作成日：{CREATED_AT}

状態：HUMAN APPROVAL待ち。MASTER未反映・公開未実施。

## 対象

B.ONE在籍のMaster登録選手のうち、高校のCareerがなかった選手{len(person_review)}名に、クラブ公式の資料で確認した出身校（高校・大学）のCareerを追加する（batch_033 wave_06、Yuichiの指示 2026-10-08）。VERIFIED snapshot commit：`{VERIFIED_COMMIT}`。

| 選手 | 学校 | 期間 | Tier案 |
| --- | --- | --- | --- |
{rows}

新規Organization：{"、".join(o["name"] for o in new_orgs)}。

Masterの既存値は変更しない。Approval Sprint 013〜016とは独立。

## Tier判定案

- Tier 1（{t1}名）：クラブ公式の発表・選手ページの出身校欄・経歴欄の表記どおり
- Tier 2（{t2}名）：ダマ ムッサ（Maranatha High Schoolの同名校）、宮本龍世（紹介文の記述）、濱田貴流馬（近畿大学のバスケ部には所属せず）、松井啓十郎（モントローズ／モントロス・クリスチャンの表記ゆれ）

## 判断範囲

`evidence_review.csv`のSUPPORTED Evidenceに対応するCareerとOrganization。`hold_review.csv`の{len(issues)}件は対象外。

この資料の作成はHuman Approvalではない。Yuichiが対象版・範囲・Tierを明示して承認した後に限り、Masterへ反映できる。
""", encoding="utf-8")
    print("Approval Sprint 017 packet:", len(careers), "careers,", t1, "Tier1,", t2, "Tier2,", len(new_orgs), "new orgs")


if __name__ == "__main__":
    main()
