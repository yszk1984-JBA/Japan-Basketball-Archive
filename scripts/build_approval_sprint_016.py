#!/usr/bin/env python3
"""Build the Human Approval packet for Approval Sprint 016 (八村・馬場・比江島 overseas).

Scope: batch_007 wave_13 VERIFIED -- the person 八村塁 (P000104, not yet in
MASTER), 11 Careers for P000104 / P000107 / P000084 and the Organizations they
reference. No MASTER value is changed. Tier proposal: Tier 2 for 八村塁 (new
person; Japanese name from Wikipedia only), Tier 1 for the others (official
sources). Never writes data/master and never records an approval.
"""

from __future__ import annotations

import csv
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V = ROOT / "data/verified/batch_007_wave_13"
OUT = ROOT / "data/verified/approval_sprint_016"
VERIFIED_COMMIT = "cc7fbc1"
CREATED_AT = "2026-10-08"
NEW_PERSON = "P000104"


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
    m_careers = {r["career_id"] for r in read(ROOT / "data/master/career.csv")}
    persons = read(V / "person_verified.csv")
    careers = read(V / "career_verified.csv")
    orgs = {r["organization_id"]: r["name"] for r in read(V / "organization_verified.csv")}
    evidence = read(V / "evidence_records.csv")
    sources = read(V / "source_references.csv")
    issues = read(V / "issue_dispositions.csv")
    names = {**m_people, **{p["person_id"]: p["name"] for p in persons}}

    errors = []
    if [p["person_id"] for p in persons] != [NEW_PERSON] or NEW_PERSON in m_people:
        errors.append("人物候補が想定と異なる")
    if any(c["person_id"] not in names for c in careers):
        errors.append("人物が不明なCareer")
    if {c["career_id"] for c in careers} & m_careers:
        errors.append("既存Master Career IDと重複")
    for oid, name in orgs.items():
        if oid in m_orgs and m_orgs[oid] != name:
            errors.append(f"{oid}: Master名と不一致")
        if oid not in m_orgs and name in m_orgs.values():
            errors.append(f"{oid}: 同名のOrganizationがMasterに既存")
    if any(e["assessment"] != "SUPPORTED" for e in evidence):
        errors.append("SUPPORTEDでないEvidence")

    person_review = []
    for pid in dict.fromkeys(c["person_id"] for c in careers):
        new = pid == NEW_PERSON
        person_review.append({"person_id": pid, "name": names[pid], "tier_proposal": "Tier 2" if new else "Tier 1",
                              "tier_reasons": "Master未登録の人物の新規追加／日本語氏名の出典がWikipediaのみ" if new else "Careerの追加のみ（公式資料）",
                              "new_person": "yes" if new else "no", "added_careers": str(sum(c["person_id"] == pid for c in careers)),
                              "verified_commit": VERIFIED_COMMIT})
    t1 = sum(p["tier_proposal"] == "Tier 1" for p in person_review)
    t2 = len(person_review) - t1
    career_review = [{**c, "name": names[c["person_id"]], "organization_name": orgs[c["organization_id"]],
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
        "# Approval Sprint 016 検証レポート", "", f"作成日：{CREATED_AT}", "",
        f"- 検証：{'PASS' if not errors else 'FAIL'}", f"- エラー：{len(errors)}件",
        f"- 対象人物：{len(person_review)}名（うち新規1名。Tier 1案：{t1}名、Tier 2案：{t2}名）", f"- 追加Career：{len(careers)}件",
        f"- Organization：{len(org_review)}件（Master未登録{len(new_orgs)}件）",
        f"- Evidence：{len(evidence)}件", f"- HOLD Issue：{len(issues)}件", "- Masterの既存値の変更：なし", "", "## エラー", "",
        *([f"- {e}" for e in errors] or ["- なし"])]) + "\n", encoding="utf-8")
    if errors:
        raise SystemExit(errors)
    rows = "\n".join(f"| {r['name']} | {r['organization_name']}{'（新規）' if r['organization_status'] == '新規' else ''} | "
                     f"{r['start'] + '〜' + r['end'] if r['start'] else '（期間なし）'} |" for r in career_review)
    tiers = "\n".join(f"- {p['name']}：{p['tier_proposal']}（{p['tier_reasons']}）" for p in person_review)
    (OUT / "README.md").write_text(f"""# Approval Sprint 016

作成日：{CREATED_AT}

状態：HUMAN APPROVAL待ち。MASTER未反映・公開未実施。

## 対象

八村塁（P000104、Master未登録のため人物ごと追加）・馬場雄大（P000107）・比江島慎（P000084）の海外経歴（batch_007 wave_13、Yuichiの選択 2026-10-08「海外経歴の続き」）。VERIFIED snapshot commit：`{VERIFIED_COMMIT}`。

| 選手 | Organization | 期間 |
| --- | --- | --- |
{rows}

新規Organization：{"、".join(o["name"] for o in new_orgs)}。Masterの既存値は変更しない。

## Tier判定案

{tiers}

## 判断範囲

人物 八村塁（氏名・生年月日）と、`evidence_review.csv`のSUPPORTED Evidenceに対応するCareer・Organization。`hold_review.csv`の{len(issues)}件（八村の日本語氏名の公式出典、同シーズン2クラブ3件、馬場のGリーグの試合区分）は対象外。

この資料の作成はHuman Approvalではない。Yuichiが対象版・範囲・Tierを明示して承認した後に限り、Masterへ反映できる。
""", encoding="utf-8")
    print("Approval Sprint 016 packet:", len(careers), "careers,", t1, "Tier1,", t2, "Tier2,", len(new_orgs), "new orgs")


if __name__ == "__main__":
    main()
