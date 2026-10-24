#!/usr/bin/env python3
"""Build the Human Approval packet for Approval Sprint 020 (national-team players,
pre-B.LEAGUE careers).

Scope: batch_035 wave_01 VERIFIED -- 24 Careers for 11 MASTER persons and the 8
new Organizations they reference. All values come from Japanese Wikipedia
(non-official), so the Tier proposal is Tier 2 for everyone.
Never writes data/master and never records an approval.
"""

from __future__ import annotations

import csv
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V = ROOT / "data/verified/batch_035_wave_01"
OUT = ROOT / "data/verified/approval_sprint_020"
VERIFIED_COMMIT = "9687ee5"
CREATED_AT = "2026-10-24"


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
    careers = read(V / "career_verified.csv")
    orgs = {r["organization_id"]: r["name"] for r in read(V / "organization_verified.csv")}
    evidence = read(V / "evidence_records.csv")
    sources = read(V / "source_references.csv")
    issues = read(V / "issue_dispositions.csv")
    held = read(V / "held_fields.csv")
    errors = []
    if any(c["person_id"] not in m_people for c in careers):
        errors.append("MasterにないPerson")
    if {c["career_id"] for c in careers} & m_careers:
        errors.append("Career IDがMasterと重複")
    for o, n in orgs.items():
        if o in m_orgs and m_orgs[o] != n:
            errors.append(f"{o}: Master名と不一致")
    if any(e["assessment"] != "SUPPORTED" for e in evidence):
        errors.append("SUPPORTEDでないEvidence")
    held_ids = {h["entity_id"] for h in held}
    person_review = [{"person_id": p, "name": m_people[p], "tier_proposal": "Tier 2",
                      "tier_reasons": "公式以外の出典（Wikipedia日本語版）のみ",
                      "added_careers": str(sum(c["person_id"] == p for c in careers)), "verified_commit": VERIFIED_COMMIT}
                     for p in dict.fromkeys(c["person_id"] for c in careers)]
    career_review = [{**c, "name": m_people[c["person_id"]], "organization_name": orgs[c["organization_id"]],
                      "organization_status": "Master既存" if c["organization_id"] in m_orgs else "新規",
                      "period_held": "保留" if c["career_id"] in held_ids and not c["start"] else "",
                      "evidence_count": str(sum(e["entity_id"] == c["career_id"] for e in evidence))} for c in careers]
    org_review = [{"organization_id": o, "name": n, "status": "Master既存" if o in m_orgs else "新規（Master未登録）"} for o, n in orgs.items()]
    write("person_review.csv", person_review, list(person_review[0].keys()))
    write("career_review.csv", career_review, ["career_id", "person_id", "name", "organization_id", "organization_name", "organization_status",
                                               "role", "start", "end", "period_held", "evidence_count"])
    write("organization_review.csv", org_review, ["organization_id", "name", "status"])
    write("evidence_review.csv", evidence, list(evidence[0].keys()))
    write("source_review.csv", sources, ["source_id", "title", "publisher", "url", "accessed_at"])
    write("hold_review.csv", issues, list(issues[0].keys()))
    write("held_fields_review.csv", held, list(held[0].keys()))
    new = [o for o in org_review if o["status"] != "Master既存"]
    (OUT / "validation_report.md").write_text("\n".join([
        "# Approval Sprint 020 検証レポート", "", f"作成日：{CREATED_AT}", "",
        f"- 検証：{'PASS' if not errors else 'FAIL'}", f"- エラー：{len(errors)}件",
        f"- 対象人物：{len(person_review)}名（すべてMaster既存、全員Tier 2案）", f"- 追加Career：{len(careers)}件",
        f"- Organization：{len(org_review)}件（Master未登録{len(new)}件）", f"- Evidence：{len(evidence)}件",
        f"- HOLD Issue：{len(issues)}件", f"- 保留項目（held fields）：{len(held)}件", "", "## エラー", "",
        *([f"- {e}" for e in errors] or ["- なし"])]) + "\n", encoding="utf-8")
    if errors:
        raise SystemExit(errors)
    rows = "\n".join(f"| {c['career_id']} | {c['name']} | {c['organization_name']}{'（新規）' if c['organization_status'] == '新規' else ''} | "
                     f"{(c['start'] + '〜' + c['end']) if c['start'] else '期間保留'} |" for c in career_review)
    (OUT / "README.md").write_text(f"""# Approval Sprint 020

作成日：{CREATED_AT}

状態：HUMAN APPROVAL待ち。MASTER未反映・公開未実施。

## 対象

日本代表経験者の開幕前・初期海外の経歴（batch_035 wave_01、Yuichiの指示 2026-10-24）。VERIFIED snapshot commit：`{VERIFIED_COMMIT}`。

出典はすべてWikipedia日本語版の基本情報欄（公式以外、記事の版番号を記録）。Yuichiの判断「公式系＋Wikipedia等（Tier 2）」による。

### 追加するCareer（`career_review.csv`）

| Career | 選手 | 所属 | 期間 |
| --- | --- | --- | --- |
{rows}

新規Organization {len(new)}件：{'、'.join(o['name'] for o in new)}。

B.LEAGUEに続くクラブは、現在の登録名のOrganizationに開幕前の部分（〜2016）を別のCareerとして追加する。既存のB.LEAGUE期のCareerは変更しない。

## Tier判定案

全員Tier 2（丁寧確認）：出典が公式以外（Wikipedia）のみのため。

## 判断範囲

`evidence_review.csv`のSUPPORTED Evidenceに対応するCareer・Organization。`hold_review.csv`の{len(issues)}件と`held_fields_review.csv`の{len(held)}件（期間が分からない3件、学校の在学期間）は対象外。

この資料の作成はHuman Approvalではない。Yuichiが対象版・範囲・Tierを明示して承認した後に限り、Masterへ反映できる。
""", encoding="utf-8")
    print("Approval Sprint 020 packet:", len(careers), "careers,", len(new), "new orgs,", len(evidence), "evidence")


if __name__ == "__main__":
    main()
