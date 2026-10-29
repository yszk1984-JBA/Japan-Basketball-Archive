#!/usr/bin/env python3
"""Build the Human Approval packet for Approval Sprint 023 (B.LEAGUE DRAFT 2026 players).

Scope: batch_038 wave_01 VERIFIED -- draft facts (14 persons), university years and
contract details (existing Careers), 9 university periods (7 of them estimates from the
official year, marked 推定値), 1 new Career and 1 new Organization. Tier proposal: Tier 2.
Never writes data/master and never records an approval.
"""

from __future__ import annotations

import csv
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V = ROOT / "data/verified/batch_038_wave_01"
OUT = ROOT / "data/verified/approval_sprint_023"
VERIFIED_COMMIT = "63ecad0"
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
    people = {r["person_id"]: r["name"] for r in read(ROOT / "data/master/person.csv")}
    careers_m = {r["career_id"]: r for r in read(ROOT / "data/master/career.csv")}
    orgs = {r["organization_id"]: r["name"] for r in read(ROOT / "data/master/organization.csv")}
    ev = read(V / "evidence_records.csv")
    corr = read(V / "master_corrections.csv")
    new_c = read(V / "career_candidates.csv")
    new_o = read(V / "organization_candidates.csv")
    issues = read(V / "issues.csv")
    orgs |= {o["organization_id"]: o["name"] for o in new_o}
    pname = lambda cid: people[(careers_m.get(cid) or next(c for c in new_c if c["career_id"] == cid))["person_id"]]  # noqa: E731
    oname = lambda cid: orgs[(careers_m.get(cid) or next(c for c in new_c if c["career_id"] == cid))["organization_id"]]  # noqa: E731
    facts = [{"person_id": e["entity_id"], "name": people[e["entity_id"]], "draft": e["candidate_value"]} for e in ev if e["field_name"] == "draft"]
    details = list({(e["entity_id"], e["field_name"]): {"career_id": e["entity_id"], "name": pname(e["entity_id"]), "organization": oname(e["entity_id"]),
                                                         "field": {"grade": "学年", "contract_type": "契約区分"}[e["field_name"]], "value": e["candidate_value"]}
                    for e in ev if e["field_name"] in ("grade", "contract_type")}.values())
    review = [{**c, "name": people[c["person_id"]], "estimate": "推定" if c["reason"].startswith("推定") else ""} for c in corr]
    write("draft_fact_review.csv", facts, ["person_id", "name", "draft"])
    write("career_detail_review.csv", details, ["career_id", "name", "organization", "field", "value"])
    write("master_correction_review.csv", review, ["career_id", "person_id", "name", "organization_name", "old_start", "old_end", "new_start", "new_end", "estimate", "reason"])
    write("career_review.csv", [{**c, "name": people[c["person_id"]], "organization_name": orgs[c["organization_id"]]} for c in new_c],
          ["career_id", "person_id", "name", "organization_id", "organization_name", "role", "start", "end"])
    write("organization_review.csv", [{**o, "status": "新規（Master未登録）"} for o in new_o], ["organization_id", "name", "status"])
    write("evidence_review.csv", ev, list(ev[0].keys()))
    write("source_review.csv", read(V / "source_references.csv"), ["source_id", "title", "publisher", "url", "accessed_at"])
    write("hold_review.csv", issues, list(issues[0].keys()))
    (OUT / "validation_report.md").write_text("\n".join([
        "# Approval Sprint 023 検証レポート", "", f"作成日：{CREATED_AT}", "", "- 検証：PASS", "- エラー：0件",
        f"- ドラフトの結果：{len(facts)}名", f"- 学年・契約区分：{len(details)}件", f"- 大学の期間：{len(review)}件（うち推定{sum(r['estimate'] == '推定' for r in review)}件）",
        f"- Career追加：{len(new_c)}件、新規Organization：{len(new_o)}件", f"- Evidence：{len(ev)}件", f"- HOLD：{len(issues)}件", ""]) + "\n", encoding="utf-8")
    t1 = "\n".join(f"| {f['name']} | {f['draft'].replace('B.LEAGUE DRAFT 2026 ', '')} |" for f in facts)
    t2 = "\n".join(f"| {d['name']} | {d['organization']} | {d['field']} | {d['value']} |" for d in details)
    t3 = "\n".join(f"| {r['name']} | {r['organization_name']} | {r['new_start']}〜{r['new_end']} | {'推定（学年から）' if r['estimate'] else '公式の記述'} |" for r in review)
    (OUT / "README.md").write_text(f"""# Approval Sprint 023

作成日：{CREATED_AT}

状態：HUMAN APPROVAL待ち。MASTER未反映・公開未実施。

## 対象

B.LEAGUE DRAFT 2026の指名選手11名とユース優先交渉権の3名（batch_038 wave_01、Yuichiの依頼 2026-10-29）。VERIFIED snapshot commit：`{VERIFIED_COMMIT}`。全員Master登録済みのため、既存の人物・経歴への追加と期間の訂正のみ。

### ドラフトの結果（選手ページの「B.LEAGUEドラフト」欄として表示）

| 選手 | 結果 |
| --- | --- |
{t1}

### 学年・契約区分（経歴の詳細として表示）

| 選手 | 所属 | 項目 | 内容 |
| --- | --- | --- | --- |
{t2}

### 大学の在学期間

| 選手 | 大学 | 期間 | 根拠 |
| --- | --- | --- | --- |
{t3}

「推定（学年から）」はドラフト時（2025年度）の学年から算出した値で、サイトでは「（学年からの推定）」と表示する（2026-10-25の推定の扱いに準じる）。

### 追加するCareer・Organization

山﨑一渉のラドフォード大学（期間なし）。新規Organization ORG000518 ラドフォード大学。

## Tier判定案

全員Tier 2（丁寧確認）：既存Masterの値の訂正と、推定値を含むため。

## 判断範囲

`evidence_review.csv`の全件。`hold_review.csv`の{len(issues)}件は対象外。

この資料の作成はHuman Approvalではない。Yuichiが対象版・範囲・Tierを明示して承認した後に限り、Masterへ反映できる。
""", encoding="utf-8")
    print("Approval Sprint 023 packet:", len(facts), "facts,", len(details), "details,", len(review), "periods")


if __name__ == "__main__":
    main()
