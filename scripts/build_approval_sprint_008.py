#!/usr/bin/env python3
"""Build the Human Approval packet for Approval Sprint 008 (Batch 031).

First sprint under the two-tier approval rule adopted on 2026-09-29
(docs/APPROVAL_TIERING_PROPOSAL_V0.1.md). This script proposes a Tier per
person automatically (Tier 1 = simple check, Tier 2 = careful check) with
its reasons; Yuichi confirms the Tier and gives the approval himself. It
never writes data/master/*.csv and never records an approval.

Scope of the sprint:
- 264 VERIFIED Careers from batch_031 (past B.LEAGUE-era clubs of 108
  existing MASTER persons) plus the Organizations they reference.
- One Organization name correction already in MASTER: ORG000222
  「トライフォース岡山」→「トライフープ岡山」 (batch_031/org_corrections.csv).
"""

from __future__ import annotations

import csv
import subprocess
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data/verified/approval_sprint_008"
VERIFIED_COMMIT = "f53dbd3"
CREATED_AT = "2026-09-29"
TODAY = date(2026, 9, 29)
WAVES = ["wave_01", "wave_02", "wave_03", "wave_04"]
SPLIT_ORGS = {"ORG000102", "ORG000174", "ORG000163", "ORG000050"}  # same TeamID, separate Organizations


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as h:
        return list(csv.DictReader(h))


def write(name: str, headers: list[str], rows: list[dict[str, str]]) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with (OUTPUT / name).open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=headers, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def unchanged_since_verified() -> None:
    paths = []
    for wave in WAVES:
        d = ROOT / "data/verified" / f"batch_031_{wave}"
        paths += [str(p.relative_to(ROOT)) for p in sorted(d.glob("*")) if p.is_file()]
    paths.append("data/candidate/batch_031/org_corrections.csv")
    if subprocess.run(["git", "diff", "--quiet", VERIFIED_COMMIT, "--", *paths], cwd=ROOT).returncode:
        raise SystemExit("Batch 031 VERIFIED snapshot changed after promotion")


def main() -> None:
    unchanged_since_verified()
    master_people = {r["person_id"]: r["name"] for r in read(ROOT / "data/master/person.csv")}
    master_orgs = {r["organization_id"]: r["name"] for r in read(ROOT / "data/master/organization.csv")}
    birth = {e["entity_id"]: e["candidate_value"] for e in read(ROOT / "data/master/evidence.csv")
             if e["entity_type"] == "Person" and e["field_name"] in ("birth_date", "date_of_birth")}
    corrections = read(ROOT / "data/candidate/batch_031/org_corrections.csv")

    careers, orgs, evidence, sources, issues = [], {}, [], [], []
    wave_of = {}
    for wave in WAVES:
        d = ROOT / "data/verified" / f"batch_031_{wave}"
        label = f"Batch 31 Wave {int(wave[-2:])}"
        for r in read(d / "career_verified.csv"):
            careers.append(r)
            wave_of[r["career_id"]] = label
        for r in read(d / "organization_verified.csv"):
            orgs.setdefault(r["organization_id"], {**r, "verified_batches": []})["verified_batches"].append(label)
        evidence += [{"verified_batch": label, **r} for r in read(d / "evidence_records.csv")]
        sources += [{"verified_batch": label, **r} for r in read(d / "source_references.csv")]
        issues += [{"verified_batch": label, **r} for r in read(d / "issue_dispositions.csv")]

    by_person = defaultdict(list)
    for c in careers:
        by_person[c["person_id"]].append(c)
    issues_by_person = defaultdict(list)
    for i in issues:
        for pid in i["person_id"].split("|"):
            issues_by_person[pid].append(i)
    corrected = {c["organization_id"] for c in corrections}

    person_review = []
    tier_counts = defaultdict(int)
    for pid in sorted(by_person):
        reasons = []
        types = {i["issue_type"] for i in issues_by_person[pid]}
        if "NOT_ON_CURRENT_ROSTER" in types:
            reasons.append("2026-27の所属履歴がなく、現役B.LEAGUE選手と確認できない")
        if "ORG_NAME_HISTORY" in types:
            reasons.append("改称したクラブの同一性判断を含む（公式TeamIDが同一）")
        if "DUAL_PLAYER_ID" in types:
            reasons.append("公式サイト上でPlayerIDが2つに分かれている")
        cars = by_person[pid]
        if any(c["organization_id"] in corrected for c in cars):
            reasons.append("名称を訂正するOrganization（ORG000222）を参照")
        if any(c["organization_id"] in SPLIT_ORGS for c in cars):
            reasons.append("同一TeamIDで別Organizationとして登録済みのクラブ（東京サンレーヴス／しながわ、湘南）を参照")
        b = birth.get(pid, "")
        if b:
            y, m, d = map(int, b.split("-"))
            age = TODAY.year - y - ((TODAY.month, TODAY.day) < (m, d))
            if age < 18:
                reasons.append("18歳未満")
        tier = "Tier 2" if reasons else "Tier 1"
        tier_counts[tier] += 1
        person_review.append({
            "person_id": pid, "name": master_people[pid], "tier_proposal": tier,
            "tier_reasons": "／".join(reasons) or "現役B.LEAGUE選手・公式資料のみ・エスカレーション条件なし",
            "added_careers": str(len(cars)),
            "added_clubs": "、".join(f"{orgs[c['organization_id']]['name']}（{c['start']}〜{c['end']}）" for c in sorted(cars, key=lambda c: c["start"])),
            "other_notes": "／".join(sorted(t for t in types if t in ("MASTER_PERIOD_DIFFERENCE", "SAME_SEASON_TWO_CLUBS"))),
            "verified_commit": VERIFIED_COMMIT,
        })

    career_review = []
    for c in careers:
        ev = [e for e in evidence if e["entity_id"] == c["career_id"]]
        career_review.append({"verified_batch": wave_of[c["career_id"]], "name": master_people[c["person_id"]], **c,
                              "organization_name": orgs[c["organization_id"]]["name"], "evidence_count": str(len(ev)),
                              "source_ids": "|".join(dict.fromkeys(e["source_id"] for e in ev))})
    organization_review = [{"verified_batches": "|".join(dict.fromkeys(o["verified_batches"])),
                            "organization_id": oid, "name": o["name"],
                            "status": ("名称訂正（Master既存）" if oid in corrected else
                                       "Master既存" if oid in master_orgs else "新規")}
                           for oid, o in sorted(orgs.items())]
    correction_review = [{**c, "master_current_name": master_orgs.get(c["organization_id"], "")} for c in corrections]

    write("person_review.csv", ["person_id", "name", "tier_proposal", "tier_reasons", "added_careers", "added_clubs", "other_notes", "verified_commit"], person_review)
    write("career_review.csv", ["verified_batch", "name", "career_id", "person_id", "organization_id", "role", "start", "end", "organization_name", "evidence_count", "source_ids"], career_review)
    write("organization_review.csv", ["verified_batches", "organization_id", "name", "status"], organization_review)
    write("organization_correction_review.csv", ["organization_id", "old_name", "new_name", "reason", "master_current_name"], correction_review)
    write("evidence_review.csv", ["verified_batch", "record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id", "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"], evidence)
    write("source_review.csv", ["verified_batch", "source_id", "title", "publisher", "url", "accessed_at"], sources)
    write("hold_review.csv", ["verified_batch", "issue_id", "person_id", "related_id", "issue_type", "status", "description", "disposition"], issues)

    errors = []
    if len(careers) != 264:
        errors.append(f"careers: expected 264, got {len(careers)}")
    if len({c['career_id'] for c in careers}) != len(careers):
        errors.append("Career ID重複")
    master_career_ids = {r["career_id"] for r in read(ROOT / "data/master/career.csv")}
    if {c["career_id"] for c in careers} & master_career_ids:
        errors.append("既存Master Career IDと重複")
    if any(c["person_id"] not in master_people for c in careers):
        errors.append("MasterにないPerson")
    for e in evidence:
        if e["assessment"] != "SUPPORTED":
            errors.append(f"{e['record_id']}: SUPPORTEDではない")
    for c in corrections:
        if master_orgs.get(c["organization_id"]) != c["old_name"]:
            errors.append(f"{c['organization_id']}: 訂正前名称がMasterと不一致")
    for oid, o in orgs.items():
        if oid in master_orgs and master_orgs[oid] != o["name"] and oid not in corrected:
            errors.append(f"{oid}: Master名と不一致")
    (OUTPUT / "validation_report.md").write_text("\n".join([
        "# Approval Sprint 008 検証レポート", "", f"作成日：{CREATED_AT}", "",
        f"- 検証：{'PASS' if not errors else 'FAIL'}", f"- エラー：{len(errors)}件",
        f"- 対象人物：{len(person_review)}名（Tier 1案 {tier_counts['Tier 1']}名、Tier 2案 {tier_counts['Tier 2']}名）",
        f"- Career：{len(career_review)}件", f"- Organization：{len(organization_review)}件（うち新規{sum(o['status']=='新規' for o in organization_review)}件、名称訂正{len(correction_review)}件）",
        f"- Evidence：{len(evidence)}件", f"- Source：{len(sources)}件", f"- HOLD Issue：{len(issues)}件", "", "## エラー", "",
        *([f"- {e}" for e in errors] or ["- なし"])]) + "\n", encoding="utf-8")
    if errors:
        raise SystemExit("Approval Sprint 008 validation failed")

    t1 = [p for p in person_review if p["tier_proposal"] == "Tier 1"]
    t2 = [p for p in person_review if p["tier_proposal"] == "Tier 2"]
    new_orgs = [o for o in organization_review if o["status"] == "新規"]
    (OUTPUT / "README.md").write_text(f"""# Approval Sprint 008

作成日：{CREATED_AT}

状態：HUMAN APPROVAL待ち。MASTER未反映・公開未実施。**2段階承認（Tier）の初回試行。**

## 対象

B.LEAGUE期の過去所属クラブ深掘り（batch_031、4 wave）でVERIFIEDとなった、Master既存{len(person_review)}名の過去の所属Career {len(career_review)}件と、参照するOrganization。あわせて、Master既存Organizationの名称訂正1件（ORG000222）。

- VERIFIED snapshot commit：`{VERIFIED_COMMIT}`
- 新規Person：なし（全員Master登録済み）
- 新規Organization：{len(new_orgs)}件（{'、'.join(o['name'] for o in new_orgs)}）
- 名称訂正：ORG000222「トライフォース岡山」→「トライフープ岡山」（`organization_correction_review.csv`）

## Tier判定案（自動検証による案。確定はYuichi）

- Tier 1（簡易確認）案：{len(t1)}名
- Tier 2（丁寧確認）案：{len(t2)}名

判定案と理由は`person_review.csv`の`tier_proposal`・`tier_reasons`列。Tier 2の主な理由は、改称クラブの同一性判断、2026-27の所属履歴がないこと、PlayerIDの重複、名称訂正Organizationの参照。

### 確認の仕方

- Tier 1：出典が公式でURLが有効／所属と期間が根拠の資料位置と一致／人物同定に問題がない／掲載しない項目が含まれない、の4点
- Tier 2：上記に加え、全Evidenceを資料位置と1件ずつ照合

## 判断範囲

`evidence_review.csv`のSUPPORTED Evidenceに対応するCareer・Organizationと、`organization_correction_review.csv`の名称訂正が承認候補。`hold_review.csv`の{len(issues)}件は対象外（既存Masterの期間の差異30件もここに含まれ、Masterは変更しない）。

この資料の作成はHuman Approvalではない。Yuichiが対象版・範囲・Tierを明示して承認した後に限り、Masterへ反映できる。
""", encoding="utf-8")
    (OUTPUT / "approval_request.md").write_text(f"""# Human Approval確認文（ドラフト・未使用）

この確認文は、Yuichiが資料を確認した後に、Yuichi自身の言葉で使用するための「たたき台」である。AIによる代筆・事前入力はしない。

> 対象：Approval Sprint 008（batch_031、Master既存{len(person_review)}名の過去所属Career {len(career_review)}件）。対象版：VERIFIED snapshot `{VERIFIED_COMMIT}`。Tier：判定案どおり（Tier 1 {len(t1)}名／Tier 2 {len(t2)}名）で確定。範囲：SUPPORTED Evidenceに対応するCareer・Organization、およびORG000222の名称訂正。判断：対象範囲をMasterへ反映してよい。`hold_review.csv`の全{len(issues)}件は対象外。

Tierの変更、除外したい人物・Career、名称訂正の可否などがあれば、そのまま伝えてほしい。
""", encoding="utf-8")
    print(f"Approval Sprint 008: {len(person_review)} persons (T1 {len(t1)}, T2 {len(t2)}), {len(career_review)} careers, {len(organization_review)} orgs, {len(evidence)} evidence")


if __name__ == "__main__":
    main()
