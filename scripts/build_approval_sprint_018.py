#!/usr/bin/env python3
"""Build the Human Approval packet for Approval Sprint 018 (overseas careers).

Scope: data/verified/batch_007_wave_13 VERIFIED (八村塁・馬場雄大・比江島慎の
海外経歴、CANDIDATE/QA commit `0956d97`、VERIFIED commit `cc7fbc1`) --
1 new Person (八村塁 P000104) + 11 Careers (5 for P000104, 3 for P000107, 1
for P000084, all already READY/eligible in VERIFIED) + 8 Organizations
(4 new: ORG000493-496) + 12 Sources + 49 SUPPORTED Evidence.

Yuichi requested this addition in chat (2026-10-08, "八村塁追加して"). Claude
presented the VERIFIED scope, the HOLD exclusions and a Tier 2 proposal (氏名
の根拠がWikipediaのみで、出典優先順位5＝エスカレーション条件に該当するため)
in chat, and Yuichi replied "Masterに承認します". This script only builds the
review packet; it does not write data/master and does not record the
approval (see master_approval.md, written separately after this packet is
committed).
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V = ROOT / "data/verified/batch_007_wave_13"
OUT = ROOT / "data/verified/approval_sprint_018"
CANDIDATE_COMMIT = "0956d97"
VERIFIED_COMMIT = "cc7fbc1"
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
    m_people = {r["person_id"]: r["name"] for r in read(ROOT / "data/master/person.csv")}
    m_orgs = {r["organization_id"]: r["name"] for r in read(ROOT / "data/master/organization.csv")}
    m_careers = read(ROOT / "data/master/career.csv")

    persons = read(V / "person_verified.csv")
    careers = read(V / "career_verified.csv")
    orgs = read(V / "organization_verified.csv")
    sources = read(V / "source_references.csv")
    evidence = read(V / "evidence_records.csv")
    held = read(V / "held_fields.csv")
    issues = read(V / "issue_dispositions.csv")

    errors = []
    if any(r["person_id"] in m_people for r in persons):
        errors.append("Person already in MASTER")
    if {c["career_id"] for c in careers} & {c["career_id"] for c in m_careers}:
        errors.append("Career ID already in MASTER")
    if any(c["person_id"] not in m_people and c["person_id"] not in {r["person_id"] for r in persons} for c in careers):
        errors.append("Career references a Person not in this packet and not in MASTER")
    for o in orgs:
        if o["organization_id"] in m_orgs and m_orgs[o["organization_id"]] != o["name"]:
            errors.append(f"{o['organization_id']}: MASTER name differs")
    if any(e["assessment"] != "SUPPORTED" for e in evidence):
        errors.append("non-SUPPORTED evidence in VERIFIED snapshot")

    # Tier proposal: uniform Tier 2 for this wave. 八村塁(P000104)の氏名は出典
    # 優先順位5（Wikipedia）のみで確認され、エスカレーション条件（出典優先順
    # 位1〜2になく3以下だけ）に該当する。馬場雄大(P000107)・比江島慎(P000084)
    # の追加分はNBA/NBL公式のみだが、同一人物のCareerを含む本Waveは一体として
    # Yuichiに提示し、Tier 2（丁寧確認）で承認を受けた。
    tier_reason = {
        "P000104": "氏名の根拠がWikipediaのみ（出典優先順位5、エスカレーション条件に該当）。NBA公式はRui Hachimuraの英字表記のみ",
        "P000107": "本Waveの一体承認（P000104のエスカレーションに合わせてTier 2で確認）",
        "P000084": "本Waveの一体承認（P000104のエスカレーションに合わせてTier 2で確認）",
    }
    person_review = [{"person_id": r["person_id"], "name": r["name"], "tier_proposal": "Tier 2",
                       "tier_reasons": tier_reason.get(r["person_id"], ""),
                       "added_careers": str(sum(c["person_id"] == r["person_id"] for c in careers)),
                       "existing_in_master": "Yes" if r["person_id"] in m_people else "No (new)",
                       "verified_commit": VERIFIED_COMMIT} for r in persons]
    # P000107・P000084はVERIFIEDスナップショットには人物として現れない(既存MASTER)ため、
    # Career側から逆算して追加する。
    for pid in dict.fromkeys(c["person_id"] for c in careers if c["person_id"] not in {p["person_id"] for p in persons}):
        person_review.append({"person_id": pid, "name": m_people[pid], "tier_proposal": "Tier 2",
                               "tier_reasons": tier_reason.get(pid, ""),
                               "added_careers": str(sum(c["person_id"] == pid for c in careers)),
                               "existing_in_master": "Yes", "verified_commit": VERIFIED_COMMIT})

    new_person_names = {p["person_id"]: p["name"] for p in persons}
    org_name = {o["organization_id"]: o["name"] for o in orgs}
    career_review = [{**c, "person_name": m_people.get(c["person_id"]) or new_person_names[c["person_id"]],
                       "organization_name": org_name[c["organization_id"]],
                       "organization_status": "Master既存" if c["organization_id"] in m_orgs else "新規",
                       "held_fields": "|".join(h["held_fields"] for h in held if h["entity_id"] == c["career_id"]),
                       "evidence_count": str(sum(e["entity_id"] == c["career_id"] for e in evidence))} for c in careers]
    org_review = [{"organization_id": o["organization_id"], "name": o["name"],
                   "status": "Master既存" if o["organization_id"] in m_orgs else "新規（Master未登録）"} for o in orgs]

    write("person_review.csv", person_review, ["person_id", "name", "tier_proposal", "tier_reasons", "added_careers", "existing_in_master", "verified_commit"])
    write("career_review.csv", career_review, ["career_id", "person_id", "person_name", "organization_id", "organization_name",
                                               "organization_status", "role", "start", "end", "held_fields", "evidence_count"])
    write("organization_review.csv", org_review, ["organization_id", "name", "status"])
    write("evidence_review.csv", evidence, list(evidence[0].keys()))
    write("source_review.csv", sources, ["source_id", "title", "publisher", "url", "accessed_at"])
    write("hold_review.csv", issues, list(issues[0].keys()))
    write("held_fields_review.csv", held, list(held[0].keys()))

    new_orgs = [o for o in org_review if o["status"] != "Master既存"]
    (OUT / "validation_report.md").write_text("\n".join([
        "# Approval Sprint 018 検証レポート", "", f"作成日：{CREATED_AT}", "",
        f"- 検証：{'PASS' if not errors else 'FAIL'}", f"- エラー：{len(errors)}件",
        f"- 対象人物：{len(person_review)}名（新規1名：八村塁 P000104、既存2名：馬場雄大 P000107・比江島慎 P000084）",
        f"- 追加Career：{len(careers)}件", f"- Organization：{len(org_review)}件（Master未登録{len(new_orgs)}件）",
        f"- Source：{len(sources)}件", f"- Evidence：{len(evidence)}件",
        f"- Held fields（VERIFIEDから除外済み）：{len(held)}件", f"- HOLD Issue：{len(issues)}件",
        "- Tier提案：全員Tier 2（丁寧確認）", "", "## エラー", "", *([f"- {e}" for e in errors] or ["- なし"]),
    ]) + "\n", encoding="utf-8")
    if errors:
        raise SystemExit(errors)

    rows = "\n".join(f"| {r['person_name']} | {r['organization_name']}{'（新規）' if r['organization_status'] == '新規' else ''} | "
                     f"{(r['start'] + '〜' + r['end']) if r['start'] else '（期間未確認）'} |" for r in career_review)
    (OUT / "README.md").write_text(f"""# Approval Sprint 018

作成日：{CREATED_AT}

状態：HUMAN APPROVAL待ち。MASTER未反映・公開未実施。

## 対象

Yuichiからのチャットでの依頼（「八村塁追加して」2026-10-08）に対応。batch_007 wave_13
VERIFIED（八村塁・馬場雄大・比江島慎の海外経歴、CANDIDATE/QA commit `{CANDIDATE_COMMIT}`、
VERIFIED commit `{VERIFIED_COMMIT}`）のうち、READY判断に基づきVERIFIEDへ採用済みの範囲を
Master反映の対象として提示する。

- **八村塁（P000104）**：MASTERへの新規登録。明成高等学校・ゴンザガ大学・ワシントン・
  ウィザーズ・ロサンゼルス・レイカーズ・ロサンゼルス・クリッパーズの5 Career
- **馬場雄大（P000107、既存MASTER）**：テキサス・レジェンズ（Gリーグ）・メルボルン・
  ユナイテッド（NBL）の3 Career追加
- **比江島慎（P000084、既存MASTER）**：ブリスベン・ブレッツ（NBL）の1 Career追加

| 選手 | 組織 | 期間 |
| --- | --- | --- |
{rows}

新規Organization：{"、".join(o["name"] for o in new_orgs)}。

## Tier提案

全員Tier 2（丁寧確認）。八村塁の氏名はWikipediaのみで確認され（NBA公式はRui Hachimuraの
英字表記のみ）、`claude/approval-tiers.md`のエスカレーション条件（出典優先順位1〜2になく
3以下だけ）に該当するため。馬場雄大・比江島慎の追加分はNBA/NBL公式のみだが、同一Waveとして
一体で確認する。

## 承認対象外（本Sprintには含めない）

- `hold_review.csv`：5件のHOLD Issue（八村塁の氏名の出典、3件のSAME_SEASON_TWO_CLUBS、
  Gリーグのシーズン区分）
- `held_fields_review.csv`：2件（C002731の高校在籍期間、C002735のクリッパーズ在籍終了年）

この資料の作成はHuman Approvalではない。Yuichiが対象版・範囲・Tierを明示して承認した後に
限り、Masterへ反映できる。
""", encoding="utf-8")
    print(f"Approval Sprint 018 packet: {len(person_review)} persons, {len(careers)} careers, "
          f"{len(new_orgs)} new orgs, {len(evidence)} evidence, {len(issues)} hold issues")


if __name__ == "__main__":
    main()
