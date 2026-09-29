#!/usr/bin/env python3
"""Build the Human Approval packet for Approval Sprint 009.

Scope (docs/ROSTER_EXPANSION_PLAN.md):
- batch_032: 143 new persons from the 2026-27 B.PREMIER rosters.
- batch_007 (merged VERIFIED): the 25 persons re-checked in wave_11.
  八村塁 (P000104, not on a B.LEAGUE roster) is outside this sprint.
- Re-check of the 7 Tier 1 persons sampled at Approval Sprint 008
  (already in MASTER; listed for Yuichi's careful re-check, no data change).

Tier proposal is automatic (docs/APPROVAL_TIERING_PROPOSAL_V0.1.md); Yuichi
confirms Tier and gives the approval himself. This script never writes
data/master/*.csv and never records an approval.
"""

from __future__ import annotations

import csv
import subprocess
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data/verified/approval_sprint_009"
VERIFIED_COMMIT = "6d497b2"
CREATED_AT = "2026-09-30"
TODAY = date(2026, 9, 30)
B32 = [ROOT / "data/verified" / f"batch_032_wave_{i:02d}" for i in range(1, 5)]
B7 = ROOT / "data/verified/batch_007_recheck"
SAMPLED_AS008 = ["P000129", "P000155", "P000166", "P000192", "P000208", "P000214", "P000225"]
OFFICIAL_MARKERS = ("B.LEAGUE", "公式")
ESCALATE = {
    "ORG_NAME_HISTORY": "改称した組織（クラブ・学校）の同一性判断を含む",
    "ENROLLED_STUDENT": "高校「在学中」の表記があり在籍状況の確認が必要",
    "NON_SCHOOL_ENTRY": "出身校欄に学校以外（クラブチーム）の記載がある",
    "SCHOOL_NAME_UNREADABLE": "学校名の一部が読めず未登録の項目がある",
    "DATE_CONFLICT": "資料間で年の食い違いがある",
}


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as h:
        return list(csv.DictReader(h))


def write(name: str, headers: list[str], rows: list[dict[str, str]]) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with (OUTPUT / name).open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=headers, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    paths = [str(p.relative_to(ROOT)) for d in [*B32, B7] for p in sorted(d.glob("*")) if p.is_file()]
    if subprocess.run(["git", "diff", "--quiet", VERIFIED_COMMIT, "--", *paths], cwd=ROOT).returncode:
        raise SystemExit("VERIFIED snapshot changed after promotion")

    master_people = {r["person_id"]: r["name"] for r in read(ROOT / "data/master/person.csv")}
    master_orgs = {r["organization_id"]: r["name"] for r in read(ROOT / "data/master/organization.csv")}
    recheck_ids = {r["person_id"] for r in read(ROOT / "data/candidate/batch_032/recheck_targets.csv")}

    persons, careers, orgs, evidence, sources, issues = {}, [], {}, [], {}, []
    origin = {}
    for d in [*B32, B7]:
        label = "Batch 32 " + d.name[-7:].replace("wave_", "Wave ") if d in B32 else "Batch 7（再確認）"
        keep = (lambda pid: True) if d in B32 else (lambda pid: pid in recheck_ids)
        for r in read(d / "person_verified.csv"):
            if keep(r["person_id"]):
                persons[r["person_id"]] = r["name"]
                origin[r["person_id"]] = label
        cs = [c for c in read(d / "career_verified.csv") if keep(c["person_id"])]
        careers += [{**c, "verified_batch": label} for c in cs]
        cids = {c["career_id"] for c in cs}
        for r in read(d / "organization_verified.csv"):
            orgs.setdefault(r["organization_id"], r["name"])
        for s in read(d / "source_references.csv"):
            sources.setdefault(s["source_id"], {**s, "verified_batch": label})
        ev = [e for e in read(d / "evidence_records.csv") if e["entity_id"] in cids or (e["entity_type"] == "Person" and keep(e["entity_id"]))]
        evidence += [{**e, "verified_batch": label} for e in ev]
        for i in read(d / "issue_dispositions.csv"):
            if any(keep(p) and (p in persons or d in B32) for p in i["person_id"].split("|")):
                issues.append({**i, "verified_batch": label})
    used_orgs = {c["organization_id"] for c in careers}
    used_sources = {e["source_id"] for e in evidence}

    by_person = defaultdict(list)
    for c in careers:
        by_person[c["person_id"]].append(c)
    issues_by_person = defaultdict(list)
    for i in issues:
        for p in i["person_id"].replace(",", "|").split("|"):
            issues_by_person[p].append(i)
    ev_by_entity = defaultdict(list)
    for e in evidence:
        ev_by_entity[(e["entity_id"], e["field_name"])].append(e)
    birth = {e["entity_id"]: e["candidate_value"] for e in evidence if e["field_name"] in ("birth_date", "date_of_birth")}

    person_review, tiers = [], defaultdict(int)
    for pid in sorted(persons):
        reasons = []
        types = {i["issue_type"] for i in issues_by_person[pid]}
        reasons += [text for t, text in ESCALATE.items() if t in types]
        # Official-source check: every VERIFIED field must have at least one official Source.
        weak = []
        for c in by_person[pid]:
            for f in ("organization_id", "start", "end"):
                if not c[f] and f != "organization_id":
                    continue
                evs = ev_by_entity[(c["career_id"], f)]
                if evs and not any(any(m in sources[e["source_id"]]["publisher"] for m in OFFICIAL_MARKERS) for e in evs):
                    weak.append(f"{c['career_id']}.{f}")
        if weak:
            reasons.append("公式資料ではない出典だけで裏付けている項目がある（" + "、".join(weak[:4]) + ("ほか" if len(weak) > 4 else "") + "）")
        b = birth.get(pid, "")
        if b:
            y, m, d = map(int, b.split("-"))
            if TODAY.year - y - ((TODAY.month, TODAY.day) < (m, d)) < 18:
                reasons.append("18歳未満")
        tier = "Tier 2" if reasons else "Tier 1"
        tiers[tier] += 1
        cs = sorted(by_person[pid], key=lambda c: (c["start"] == "" and 0 or 1, c["start"]))
        person_review.append({
            "verified_batch": origin[pid], "person_id": pid, "name": persons[pid], "birth_date": b,
            "tier_proposal": tier,
            "tier_reasons": "／".join(reasons) or "現役B.LEAGUE選手・公式資料のみ・エスカレーション条件なし",
            "careers": str(len(cs)),
            "career_summary": "、".join(f"{orgs[c['organization_id']]}" + (f"（{c['start']}〜{c['end']}）" if c["start"] else "") for c in cs),
            "other_notes": "／".join(sorted(t for t in types if t not in ESCALATE and t not in ("HIGH_SCHOOL_PERIOD", "UNIVERSITY_PERIOD"))),
            "verified_commit": VERIFIED_COMMIT,
        })

    career_review = [{**c, "name": persons[c["person_id"]], "organization_name": orgs[c["organization_id"]],
                      "evidence_count": str(sum(len(ev_by_entity[(c["career_id"], f)]) for f in ("organization_id", "start", "end", "role"))),
                      "source_ids": "|".join(dict.fromkeys(e["source_id"] for f in ("organization_id", "start", "end") for e in ev_by_entity[(c["career_id"], f)]))}
                     for c in careers]
    organization_review = [{"organization_id": o, "name": orgs[o], "status": "Master既存" if o in master_orgs else "新規（Master未登録）"}
                           for o in sorted(used_orgs)]
    resample = []
    m_careers = read(ROOT / "data/master/career.csv")
    for pid in SAMPLED_AS008:
        cs = [c for c in m_careers if c["person_id"] == pid]
        resample.append({"person_id": pid, "name": master_people[pid], "master_careers": str(len(cs)),
                         "career_ids": "|".join(c["career_id"] for c in cs),
                         "check": "Tier 2の手順（全SUPPORTED Evidenceを資料位置と照合）で再確認。誤りがあれば件数と内容を記録",
                         "result": "", "errors_found": ""})

    write("person_review.csv", ["verified_batch", "person_id", "name", "birth_date", "tier_proposal", "tier_reasons", "careers", "career_summary", "other_notes", "verified_commit"], person_review)
    write("career_review.csv", ["verified_batch", "name", "career_id", "person_id", "organization_id", "role", "start", "end", "organization_name", "evidence_count", "source_ids"], career_review)
    write("organization_review.csv", ["organization_id", "name", "status"], organization_review)
    write("evidence_review.csv", ["verified_batch", "record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id", "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"], evidence)
    write("source_review.csv", ["verified_batch", "source_id", "title", "publisher", "url", "accessed_at"], [sources[s] for s in sorted(used_sources)])
    write("hold_review.csv", ["verified_batch", "issue_id", "person_id", "related_id", "issue_type", "status", "description", "disposition"], issues)
    write("as008_sample_recheck.csv", ["person_id", "name", "master_careers", "career_ids", "check", "result", "errors_found"], resample)

    errors = []
    if len(persons) != 143 + 25:
        errors.append(f"persons: expected 168, got {len(persons)}")
    if set(persons) & set(master_people):
        errors.append("Master既存のPersonが混入")
    if len({c["career_id"] for c in careers}) != len(careers):
        errors.append("Career ID重複")
    if {c["career_id"] for c in careers} & {c["career_id"] for c in m_careers}:
        errors.append("既存Master Career IDと重複")
    for e in evidence:
        if e["assessment"] != "SUPPORTED":
            errors.append(f"{e['record_id']}: SUPPORTEDではない")
        if e["source_id"] not in sources:
            errors.append(f"{e['record_id']}: Sourceなし")
    for o in used_orgs:
        if o in master_orgs and master_orgs[o] != orgs[o]:
            errors.append(f"{o}: Master名と不一致")
    for pid in persons:
        if ("name" not in {e["field_name"] for e in evidence if e["entity_id"] == pid}):
            errors.append(f"{pid}: 氏名の根拠なし")
    seen = defaultdict(int)
    for c in careers:
        seen[(c["person_id"], c["organization_id"], c["start"])] += 1
    errors += [f"同じ人物・所属・開始年のCareerが重複 {k}" for k, v in seen.items() if v > 1]

    new_orgs = [o for o in organization_review if o["status"] != "Master既存"]
    (OUTPUT / "validation_report.md").write_text("\n".join([
        "# Approval Sprint 009 検証レポート", "", f"作成日：{CREATED_AT}", "",
        f"- 検証：{'PASS' if not errors else 'FAIL'}", f"- エラー：{len(errors)}件",
        f"- 対象人物：{len(persons)}名（Tier 1案 {tiers['Tier 1']}名、Tier 2案 {tiers['Tier 2']}名）",
        f"- Career：{len(careers)}件", f"- Organization：{len(organization_review)}件（うちMaster未登録{len(new_orgs)}件）",
        f"- Evidence：{len(evidence)}件", f"- Source：{len(used_sources)}件", f"- HOLD Issue：{len(issues)}件", "", "## エラー", "",
        *([f"- {e}" for e in errors] or ["- なし"])]) + "\n", encoding="utf-8")
    if errors:
        for e in errors[:20]:
            print(e)
        raise SystemExit("Approval Sprint 009 validation failed")

    t2 = [p for p in person_review if p["tier_proposal"] == "Tier 2"]
    reason_count = defaultdict(int)
    for p in t2:
        for r in p["tier_reasons"].split("／"):
            reason_count[r.split("（")[0]] += 1
    reason_lines = "\n".join(f"- {r}：{n}名" for r, n in sorted(reason_count.items(), key=lambda x: -x[1]))
    (OUTPUT / "README.md").write_text(f"""# Approval Sprint 009

作成日：{CREATED_AT}

状態：HUMAN APPROVAL待ち。MASTER未反映・公開未実施。2段階承認（2回目）。

## 対象

B.PREMIER 2026-27のロスター起点の横展開（`docs/ROSTER_EXPANSION_PLAN.md`）。

- 新規人物 143名（batch_032、P000239〜P000381）
- 以前から候補登録のまま未承認だった25名（batch_007、最新の公式情報で再確認済み）
- 合計 **{len(persons)}名**、Career {len(careers)}件、SUPPORTED Evidence {len(evidence)}件
- VERIFIED snapshot commit：`{VERIFIED_COMMIT}`
- Organization：{len(organization_review)}件（うちMaster未登録{len(new_orgs)}件。多くは出身校）

## Tier判定案（自動検証による案。確定はYuichi）

- Tier 1（簡易確認）案：{tiers['Tier 1']}名
- Tier 2（丁寧確認）案：{tiers['Tier 2']}名

Tier 2の理由（重複あり）：

{reason_lines}

判定案と理由は`person_review.csv`の`tier_proposal`・`tier_reasons`列。

## 前回（Sprint 008）の抜き取り再確認

Sprint 008でTier 1として承認した74名から抽出した7名（seed 20260929）を、今回Tier 2の手順で再確認する（`as008_sample_recheck.csv`）。対象はMaster登録済みのデータで、この資料では値を変更しない。誤りが見つかった場合は既存Masterの訂正と同じ経路で扱い、誤りの割合が5%を超えたらTier 1の条件を見直す。

## 判断範囲

`evidence_review.csv`のSUPPORTED Evidenceに対応するPerson・Career・Organizationが承認候補。`hold_review.csv`の{len(issues)}件（学校の在籍期間未確認、改称の記録、開幕前の在籍未確認など）は対象外。

## 確認してほしい点

- 白鷗大学（ORG000093）と白鴎大学（ORG000208）がMasterで別Organizationになっている。今回の新規人物は公式表記どおり「白鴎大学」（ORG000208）に紐づけた。統合するかは別途判断
- 八村阿蓮（神戸）はMasterの同名人物（P000133）と同一人物とみられるため、今回は登録していない（`data/candidate/batch_032/excluded.csv`）
- 18歳未満の3名は登録していない

この資料の作成はHuman Approvalではない。Yuichiが対象版・範囲・Tierを明示して承認した後に限り、Masterへ反映できる。
""", encoding="utf-8")
    (OUTPUT / "approval_request.md").write_text(f"""# Human Approval確認文（ドラフト・未使用）

この確認文は、Yuichiが資料を確認した後に、Yuichi自身の言葉で使用するための「たたき台」である。AIによる代筆・事前入力はしない。

> 対象：Approval Sprint 009（batch_032の新規143名とbatch_007の再確認25名、計{len(persons)}名・Career {len(careers)}件）。対象版：VERIFIED snapshot `{VERIFIED_COMMIT}`。Tier：判定案どおり（Tier 1 {tiers['Tier 1']}名／Tier 2 {tiers['Tier 2']}名）で確定。範囲：SUPPORTED Evidenceに対応するPerson・Career・Organization。判断：対象範囲をMasterへ反映してよい。`hold_review.csv`の全{len(issues)}件は対象外。

Tierの変更、除外したい人物・Career、Sprint 008抜き取り7名の再確認結果があれば、あわせて伝えてほしい。
""", encoding="utf-8")
    print(f"Approval Sprint 009: {len(persons)} persons (T1 {tiers['Tier 1']}, T2 {tiers['Tier 2']}), {len(careers)} careers, "
          f"{len(organization_review)} orgs ({len(new_orgs)} not in Master), {len(evidence)} evidence, {len(issues)} holds")
    print(reason_lines)


if __name__ == "__main__":
    main()
