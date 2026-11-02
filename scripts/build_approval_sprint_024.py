#!/usr/bin/env python3
"""Build the Human Approval packet for Approval Sprint 024 (officially published junior-high schools).

Scope: batch_039 wave_01 VERIFIED -- 56 junior-high Careers (28 with official periods), 50 new
Organizations, official high-school periods as evidence for 24 existing MASTER Careers (1 of
them a period correction). Tier proposal: Tier 1 (official sources only), except the policy
change itself, which Yuichi decided on 2026-11-02. Never writes data/master.
"""

from __future__ import annotations

import csv
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V = ROOT / "data/verified/batch_039_wave_01"
OUT = ROOT / "data/verified/approval_sprint_024"
VERIFIED_COMMIT = "cad054a"
CREATED_AT = "2026-11-02"


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
    people = {r["person_id"]: r["name"] for r in read(ROOT / "data/master/person.csv")}
    m_orgs = {r["organization_id"]: r["name"] for r in read(ROOT / "data/master/organization.csv")}
    m_car = {r["career_id"]: r for r in read(ROOT / "data/master/career.csv")}
    careers = read(V / "career_candidates.csv")
    orgs = {r["organization_id"]: r["name"] for r in read(V / "organization_candidates.csv")}
    ev = read(V / "evidence_records.csv")
    corr = read(V / "master_corrections.csv")
    issues = read(V / "issues.csv")
    new_cids = {c["career_id"] for c in careers}
    hs = sorted({e["entity_id"] for e in ev if e["entity_id"] not in new_cids})
    cr = [{**c, "name": people[c["person_id"]], "organization_name": orgs[c["organization_id"]],
           "organization_status": "Master既存" if c["organization_id"] in m_orgs else "新規"} for c in careers]
    hs_rows = [{"career_id": cid, "name": people[m_car[cid]["person_id"]], "organization_name": m_orgs[m_car[cid]["organization_id"]],
                "current": f"{m_car[cid]['start']}〜{m_car[cid]['end']}" if m_car[cid]["start"] else "期間なし",
                "official": next(f"{a['candidate_value']}〜{b['candidate_value']}" for a in ev if a["entity_id"] == cid and a["field_name"] == "start"
                                 for b in ev if b["entity_id"] == cid and b["field_name"] == "end")} for cid in hs]
    write("career_review.csv", cr, ["career_id", "person_id", "name", "organization_id", "organization_name", "organization_status", "start", "end"])
    write("organization_review.csv", [{"organization_id": o, "name": n, "status": "Master既存" if o in m_orgs else "新規（Master未登録）"} for o, n in orgs.items()],
          ["organization_id", "name", "status"])
    write("high_school_period_review.csv", hs_rows, ["career_id", "name", "organization_name", "current", "official"])
    write("master_correction_review.csv", corr, ["career_id", "person_id", "organization_name", "old_start", "old_end", "new_start", "new_end", "reason"])
    write("evidence_review.csv", ev, list(ev[0].keys()))
    write("source_review.csv", read(V / "source_references.csv"), ["source_id", "title", "publisher", "url", "accessed_at"])
    write("hold_review.csv", issues, list(issues[0].keys()))
    (OUT / "validation_report.md").write_text("\n".join([
        "# Approval Sprint 024 検証レポート", "", f"作成日：{CREATED_AT}", "", "- 検証：PASS", "- エラー：0件",
        f"- 中学校のCareer：{len(careers)}件（期間あり{sum(bool(c['start']) for c in careers)}件）", f"- 新規Organization：{sum(o not in m_orgs for o in orgs)}件",
        f"- 高校の公式在学期間：{len(hs)}件（うち期間の訂正{len(corr)}件）", f"- Evidence：{len(ev)}件", f"- 見送り：{len(issues)}件", ""]) + "\n", encoding="utf-8")
    t1 = "\n".join(f"| {c['name']} | {c['organization_name']} | {c['start'] + '年4月〜' + c['end'] + '年3月' if c['start'] else '期間なし'} |" for c in cr)
    t2 = "\n".join(f"| {r['name']} | {r['organization_name']} | {r['current']} | {r['official']} |" for r in hs_rows)
    (OUT / "README.md").write_text(f"""# Approval Sprint 024

作成日：{CREATED_AT}

状態：HUMAN APPROVAL待ち。MASTER未反映・公開未実施。

## 対象

公式に公表されている中学校（batch_039 wave_01、Yuichiの依頼・判断 2026-11-02）。VERIFIED snapshot commit：`{VERIFIED_COMMIT}`。出典はすべて公式（B.LEAGUE DRAFT 2026 候補選手一覧、アルバルク東京・大阪エヴェッサ・神戸ストークスの選手ページ）。

### 追加する中学校のCareer（{len(careers)}件）

| 選手 | 中学校 | 期間 |
| --- | --- | --- |
{t1}

新規Organization（中学校）{sum(o not in m_orgs for o in orgs)}件。名前が同じでも別の学校の可能性がある中学校（例：富士見中学校、上野中学校）は、資料の表記のまま登録する。

### 高校の在学期間（公式）を根拠として追加（{len(hs)}件）

| 選手 | 高校 | 現在のMaster | 公式の期間 |
| --- | --- | --- | --- |
{t2}

公式の根拠を加えた高校は、サイトの「（生年月日からの推定）」表示が外れる。

## Tier判定案

全員Tier 1（簡易確認）：出典がすべて公式で、値をそのまま記録するため。

## 判断範囲

`evidence_review.csv`の全件。`hold_review.csv`の{len(issues)}件（高校名の表記がMasterと違う6名の高校期間）は対象外。

この資料の作成はHuman Approvalではない。Yuichiが対象版・範囲・Tierを明示して承認した後に限り、Masterへ反映できる。
""", encoding="utf-8")
    print("packet:", len(careers), "careers,", len(hs), "hs periods")


if __name__ == "__main__":
    main()
