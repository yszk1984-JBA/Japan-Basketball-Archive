#!/usr/bin/env python3
"""Build the Human Approval packet for Approval Sprint 021 (estimated high-school periods).

Scope: batch_036 wave_01 VERIFIED -- 415 period additions to existing MASTER
high-school Careers, estimated from the birth date (owner-approved exception
to "do not guess"; every value is marked 推定値). Tier proposal: Tier 2.
Never writes data/master and never records an approval.
"""

from __future__ import annotations

import csv
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V = ROOT / "data/verified/batch_036_wave_01"
OUT = ROOT / "data/verified/approval_sprint_021"
VERIFIED_COMMIT = "abc3d37"
CREATED_AT = "2026-10-25"


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
    master = {r["career_id"]: r for r in read(ROOT / "data/master/career.csv")}
    corr = read(V / "master_corrections.csv")
    evidence = read(V / "evidence_records.csv")
    sources = read(V / "source_references.csv")
    issues = read(V / "issues.csv")
    errors = []
    for c in corr:
        m = master.get(c["career_id"])
        if not m or (m["start"], m["end"]) != (c["old_start"], c["old_end"]):
            errors.append(f"{c['career_id']}: 訂正前の値がMasterと不一致")
    if any(e["assessment"] != "SUPPORTED" or not e["issue_note"].startswith("推定値") for e in evidence):
        errors.append("推定値の印のないEvidence")
    review = [{**c, "name": people[c["person_id"]], "tier_proposal": "Tier 2", "verified_commit": VERIFIED_COMMIT} for c in corr]
    write("master_correction_review.csv", review, ["career_id", "person_id", "name", "organization_name", "old_start", "old_end",
                                                   "new_start", "new_end", "reason", "tier_proposal", "verified_commit"])
    write("evidence_review.csv", evidence, list(evidence[0].keys()))
    write("source_review.csv", sources, ["source_id", "title", "publisher", "url", "accessed_at"])
    write("hold_review.csv", issues, list(issues[0].keys()))
    (OUT / "validation_report.md").write_text("\n".join([
        "# Approval Sprint 021 検証レポート", "", f"作成日：{CREATED_AT}", "",
        f"- 検証：{'PASS' if not errors else 'FAIL'}", f"- エラー：{len(errors)}件",
        f"- 高校期間の推定：{len(corr)}件（{len({c['person_id'] for c in corr})}名、全員Tier 2案）",
        f"- Evidence：{len(evidence)}件（すべて推定値の印つき）", f"- 対象外（HOLD）：{len(issues)}件", "", "## エラー", "",
        *([f"- {e}" for e in errors] or ["- なし"])]) + "\n", encoding="utf-8")
    if errors:
        raise SystemExit(errors)
    by_start = Counter(c["new_start"] for c in corr)
    dist = "、".join(f"{k}年入学 {v}名" for k, v in sorted(by_start.items()))
    sample = "\n".join(f"| {r['name']} | {r['organization_name']} | {r['reason'].split('生年月日 ')[1].split(' ')[0]} | {r['new_start']}〜{r['new_end']} |"
                       for r in review if r["name"].replace(" ", "") in {"比江島慎", "河村勇輝", "富永啓生", "篠山竜青", "原修太", "西田優大"})
    (OUT / "README.md").write_text(f"""# Approval Sprint 021

作成日：{CREATED_AT}

状態：HUMAN APPROVAL待ち。MASTER未反映・公開未実施。

## 対象

日本の高校の在学期間を、生年月日から推定して設定する（batch_036 wave_01、Yuichiの指示 2026-10-25）。VERIFIED snapshot commit：`{VERIFIED_COMMIT}`。

ガバナンスの「推測しない」に対するYuichi明示の例外。すべて推定値として印を付け、サイトでは「推定」と明記して表示する。

- 件数：{len(corr)}件（既存Masterの高校Careerの「期間なし」に開始年・終了年を入れる）
- ルール：Y年4月2日〜Y+1年4月1日生まれ → 高校 Y+16〜Y+19
- 入学年の分布：{dist}
- 一覧：`master_correction_review.csv`

### 例

| 選手 | 高校 | 生年月日 | 推定期間 |
| --- | --- | --- | --- |
{sample}

## 対象外（`hold_review.csv`）

{chr(10).join('- ' + i['description'] for i in issues)}

## 注意

浪人・留年・休学、留学生の途中入学、高校の転校などは生年月日だけでは分からないため、実際の在学期間と違う可能性がある。公式資料で期間が確認できた場合は、その値に置き換える。

## Tier判定案

全員Tier 2（丁寧確認）：資料で確認した値ではなく推定のため。

この資料の作成はHuman Approvalではない。Yuichiが対象版・範囲・Tierを明示して承認した後に限り、Masterへ反映できる。
""", encoding="utf-8")
    print("Approval Sprint 021 packet:", len(corr), "estimates")


if __name__ == "__main__":
    main()
