#!/usr/bin/env python3
"""Build the Human Approval packet for Approval Sprint 022 (2026-10-29 update).

Scope: batch_034 wave_01 VERIFIED -- 4 MASTER period corrections, 4 new Careers
(1 for an existing person, 3 for 2 new persons) and the 2 new Persons.
Tier proposal: Tier 2 for every person (MASTER corrections or new persons).
Never writes data/master and never records an approval.
"""

from __future__ import annotations

import csv
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V = ROOT / "data/verified/batch_037_wave_01"
OUT = ROOT / "data/verified/approval_sprint_022"
VERIFIED_COMMIT = "6e29821"
CREATED_AT = "2026-10-29"


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
    v_orgs = {r["organization_id"]: r["name"] for r in read(V / "organization_verified.csv")}
    new_orgs = {o: n for o, n in v_orgs.items() if o not in m_orgs}
    m_orgs = m_orgs | v_orgs
    m_careers = {r["career_id"]: r for r in read(ROOT / "data/master/career.csv")}
    persons = read(V / "person_verified.csv")
    names = {p["person_id"]: p["name"] for p in persons} | m_people
    careers = read(V / "career_verified.csv")
    corrections = read(V / "master_corrections.csv")
    evidence = read(V / "evidence_records.csv") + read(V / "master_correction_evidence.csv")
    sources = read(V / "source_references.csv")
    issues = read(V / "issue_dispositions.csv")
    held = read(V / "held_fields.csv")

    errors = []
    if {p["person_id"] for p in persons} & set(m_people):
        errors.append("新規PersonがMasterと重複")
    if {c["career_id"] for c in careers} & set(m_careers):
        errors.append("Career IDがMasterと重複")
    for c in careers:
        if c["person_id"] not in names:
            errors.append(f"{c['career_id']}: 不明なPerson")
        if c["organization_id"] not in m_orgs:
            errors.append(f"{c['career_id']}: 不明なOrganization")
    for c in corrections:
        m = m_careers.get(c["career_id"])
        if not m or (m["start"], m["end"]) != (c["old_start"], c["old_end"]):
            errors.append(f"{c['career_id']}: 訂正前の値がMasterと不一致")
    if any(e["assessment"] != "SUPPORTED" for e in evidence):
        errors.append("SUPPORTEDでないEvidence")
    if any(e["source_id"] not in {s["source_id"] for s in sources} for e in evidence):
        errors.append("Source参照が不足")

    involved = list(dict.fromkeys([c["person_id"] for c in corrections] + [c["person_id"] for c in careers]))
    person_review = []
    for pid in involved:
        new = pid not in m_people
        person_review.append({
            "person_id": pid, "name": names[pid], "status": "新規Person" if new else "Master既存",
            "tier_proposal": "Tier 2",
            "tier_reasons": "新規Person" if new else ("既存Masterの値（期間）を変更する訂正を含む" if any(c["person_id"] == pid for c in corrections) else "公式以外の出典（Wikipedia）を含む、または追加のみ"),
            "added_careers": str(sum(c["person_id"] == pid for c in careers)),
            "corrections": str(sum(c["person_id"] == pid for c in corrections)), "verified_commit": VERIFIED_COMMIT})
    career_review = [{**c, "name": names[c["person_id"]], "organization_name": m_orgs[c["organization_id"]],
                      "evidence_count": str(sum(e["entity_id"] == c["career_id"] for e in evidence))} for c in careers]
    org_review = [{"organization_id": o, "name": m_orgs[o], "status": "新規（Master未登録）" if o in new_orgs else "Master既存"}
                  for o in dict.fromkeys(c["organization_id"] for c in careers)]
    write("person_review.csv", person_review, list(person_review[0].keys()))
    write("career_review.csv", career_review, ["career_id", "person_id", "name", "organization_id", "organization_name", "role", "start", "end", "evidence_count"])
    write("organization_review.csv", org_review, ["organization_id", "name", "status"])
    write("master_correction_review.csv", corrections, list(corrections[0].keys()))
    write("evidence_review.csv", evidence, list(evidence[0].keys()))
    write("source_review.csv", sources, ["source_id", "title", "publisher", "url", "accessed_at"])
    write("hold_review.csv", issues, list(issues[0].keys()))
    write("held_fields_review.csv", held, list(held[0].keys()))
    (OUT / "validation_report.md").write_text("\n".join([
        "# Approval Sprint 022 検証レポート", "", f"作成日：{CREATED_AT}", "",
        f"- 検証：{'PASS' if not errors else 'FAIL'}", f"- エラー：{len(errors)}件",
        f"- 対象人物：{len(person_review)}名（新規{len(persons)}名、全員Tier 2案）", f"- 追加Career：{len(careers)}件",
        f"- Masterの期間訂正：{len(corrections)}件", f"- Organization：{len(org_review)}件（Master未登録{len(new_orgs)}件）",
        f"- Evidence：{len(evidence)}件", f"- HOLD Issue：{len(issues)}件", "", "## エラー", "",
        *([f"- {e}" for e in errors] or ["- なし"])]) + "\n", encoding="utf-8")
    if errors:
        raise SystemExit(errors)
    period = lambda s, e: f"{s}〜{e}"  # noqa: E731
    corr = "\n".join(f"| {c['career_id']} | {names[c['person_id']]} | {c['organization_name']} | {period(c['old_start'], c['old_end']) if (c['old_start'] or c['old_end']) else '期間なし'} | {period(c['new_start'], c['new_end'])} |" for c in corrections)
    add = "\n".join(f"| {c['career_id']} | {names[c['person_id']]} | {m_orgs[c['organization_id']]} | {period(c['start'], c['end']) if c['start'] else '期間なし（学校）'} |" for c in careers)
    (OUT / "README.md").write_text(f"""# Approval Sprint 022

作成日：{CREATED_AT}

状態：HUMAN APPROVAL待ち。MASTER未反映・公開未実施。

## 対象

2026-10-29の更新（batch_037 wave_01）。VERIFIED snapshot commit：`{VERIFIED_COMMIT}`。原文：`data/raw/research/update_2026-10-29.md`。

### Masterの期間の訂正（`master_correction_review.csv`）

| Career | 選手 | クラブ | 現在 | 訂正後 |
| --- | --- | --- | --- | --- |
{corr}

### 追加するCareer（`career_review.csv`）

| Career | 選手 | 所属 | 期間 |
| --- | --- | --- | --- |
{add}

新規Person：岡本飛竜（P000566、1993-04-20生）、ファイパプ月瑠（P000567、1987-06-22生）。新規Organization：{"、".join(f"{o}（{n}）" for o, n in new_orgs.items())}。

## Tier判定案

全員Tier 2（丁寧確認）：Masterの値の訂正、新規Person、または公式以外の出典（Wikipedia・報道）を含むため。

## 判断範囲

`evidence_review.csv`のSUPPORTED Evidenceに対応するPerson・Career・Organizationと、期間訂正{len(corrections)}件。`hold_review.csv`の{len(issues)}件と`held_fields_review.csv`は対象外。

この資料の作成はHuman Approvalではない。Yuichiが対象版・範囲・Tierを明示して承認した後に限り、Masterへ反映できる。
""", encoding="utf-8")
    print("Approval Sprint 022 packet:", len(persons), "new persons,", len(careers), "careers,", len(corrections), "corrections,", len(evidence), "evidence")


if __name__ == "__main__":
    main()
