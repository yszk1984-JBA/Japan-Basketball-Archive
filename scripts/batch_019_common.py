#!/usr/bin/env python3
"""Shared builder for Batch 019 (強豪校横展開 第2弾 学校1/12：桐光学園高等学校).

Second round of the powerhouse-school expansion (see
docs/BATCH_019_PROPOSAL.md). Discovery started from B.LEAGUE's
"ワタシノB.LEAGUE" tag list for TagID=35:桐光学園高等学校 (9 current
alumni, no "もっと見る" button). 齋藤拓実 is already registered
(P000086, batch_007/wave_01) and is excluded, leaving 8 new persons,
split 4+4 into Wave 1 and Wave 2.

Profile values were read on 2026-09-26 from each B.LEAGUE roster_detail
page: 氏名・生年月日 from the profile header, 出身校（高）/出身校（大）
from the Q&A section, and the club history from 「クラブ所属履歴」.
The site now lists the 2026-27 season as the latest row.

Scope (unchanged from Batch 008): minimal path only (高校→大学→現所属
クラブ). Earlier pro clubs are logged as PRO_HISTORY_GAPS issues. When
a player returned to the current club after playing elsewhere, the
start year is the year of the return (existing policy, see batch_013).

桐光学園高等学校 reuses the existing Organization ORG000123 whose
registered name is 「桐光学園高校」 (batch_007/wave_01). The name is
kept as-is so the ID/name pair stays consistent across batches;
normalising it is a separate decision for Yuichi.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CHECKED_AT = "2026-09-26"
SCHOOL_ORG = ("ORG000123", "桐光学園高校")
SCHOOL_TAG_NAME = "桐光学園高等学校"

# Existing Organization IDs were matched against master + every
# candidate organization_candidates.csv. 神奈川大学 is new (ORG000210;
# highest existing ID was ORG000209 from batch_018).
ORG_NAMES = {
    "ORG000123": "桐光学園高校",
    "ORG000124": "明治大学",
    "ORG000030": "青山学院大学",
    "ORG000210": "神奈川大学",
    "ORG000018": "専修大学",
    "ORG000136": "早稲田大学",
    "ORG000180": "ファイティングイーグルス名古屋",
    "ORG000090": "横浜エクセレンス",
    "ORG000106": "琉球ゴールデンキングス",
    "ORG000190": "越谷アルファーズ",
    "ORG000055": "横浜ビー・コルセアーズ",
    "ORG000097": "三遠ネオフェニックス",
    "ORG000142": "大阪エヴェッサ",
    "ORG000149": "富山グラウジーズ",
}


def build(wave: int, players: list[dict], first_career_seq: int) -> None:
    prefix = f"B19W{wave}"
    base = ROOT / "data" / "candidate" / "batch_019" / f"wave_{wave:02d}"

    persons, careers, sources, evidence, decisions, issues = [], [], [], [], [], []
    org_ids: list[str] = []

    def add_org(org_id: str) -> None:
        if org_id not in org_ids:
            org_ids.append(org_id)

    sources.append({
        "source_id": f"{prefix}S0001",
        "title": f"ワタシノB.LEAGUE選手一覧 | {SCHOOL_TAG_NAME}",
        "publisher": "B.LEAGUE",
        "url": f"https://www.bleague.jp/mybleague_list/?TagID=35:{SCHOOL_TAG_NAME}",
        "accessed_at": CHECKED_AT,
    })

    seq = {"e": 0, "d": 0, "i": 0, "s": 1, "c": first_career_seq}

    def ev(entity_type, entity_id, field, value, source_id, locator, summary, note=""):
        seq["e"] += 1
        evidence.append({
            "record_id": f"{prefix}E{seq['e']:04d}", "entity_type": entity_type,
            "entity_id": entity_id, "field_name": field, "candidate_value": value,
            "source_id": source_id, "source_locator": locator,
            "evidence_summary": summary, "assessment": "SUPPORTED",
            "checked_at": CHECKED_AT, "issue_note": note,
        })

    def dec(entity_type, entity_id, eligible, held, reason):
        seq["d"] += 1
        decisions.append({
            "decision_id": f"{prefix}D{seq['d']:04d}", "entity_type": entity_type,
            "entity_id": entity_id, "decision": "READY_FOR_VERIFIED_REVIEW",
            "eligible_fields": eligible, "held_fields": held, "reason": reason,
            "reviewed_at": CHECKED_AT,
        })

    def issue(person_id, related_id, issue_type, description, next_check):
        seq["i"] += 1
        issue_id = f"{prefix}I{seq['i']:04d}"
        issues.append({
            "issue_id": issue_id, "person_id": person_id, "related_id": related_id,
            "issue_type": issue_type, "status": "HOLD",
            "description": description, "next_check": next_check,
        })
        return issue_id

    def next_career() -> str:
        cid = f"C{seq['c']:06d}"
        seq["c"] += 1
        return cid

    for p in players:
        pid, name, plain = p["person_id"], p["name"], p["name"].replace(" ", "")
        seq["s"] += 1
        sid = f"{prefix}S{seq['s']:04d}"
        sources.append({
            "source_id": sid, "title": f"{plain} 選手プロフィール", "publisher": "B.LEAGUE",
            "url": f"https://www.bleague.jp/roster_detail/?PlayerID={p['bleague_id']}",
            "accessed_at": CHECKED_AT,
        })
        persons.append({"person_id": pid, "name": name})
        ev("Person", pid, "name", name, sid, "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認")
        ev("Person", pid, "birth_date", p["birth_date"], sid, "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認")
        dec("Person", pid, "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")

        hs_cid, uni_cid, club_cid = next_career(), next_career(), next_career()
        for org in (SCHOOL_ORG[0], p["university"], p["club"]):
            add_org(org)
        careers.extend([
            {"career_id": hs_cid, "person_id": pid, "organization_id": SCHOOL_ORG[0], "role": "Player", "start": "", "end": ""},
            {"career_id": uni_cid, "person_id": pid, "organization_id": p["university"], "role": "Player", "start": "", "end": ""},
            {"career_id": club_cid, "person_id": pid, "organization_id": p["club"], "role": "Player", "start": p["club_start"], "end": ""},
        ])

        gap_issue_id = f"{prefix}I{seq['i'] + 3:04d}" if p.get("pro_gaps") else ""
        ev("Career", hs_cid, "organization_id", SCHOOL_ORG[0], sid,
           f"基本情報 > 出身校（高）：{SCHOOL_TAG_NAME}", "B.LEAGUE公式プロフィールで出身高校を確認")
        ev("Career", uni_cid, "organization_id", p["university"], sid,
           f"基本情報 > 出身校（大）：{ORG_NAMES[p['university']]}", "B.LEAGUE公式プロフィールで出身大学を確認")
        ev("Career", club_cid, "organization_id", p["club"], sid,
           f"クラブ所属履歴 > {p['club_locator']}", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認",
           note=(f"{p['pro_gaps']}は今回のWaveでは対象外。詳細はissue {gap_issue_id}を参照" if gap_issue_id else ""))
        ev("Career", club_cid, "start", p["club_start"], sid,
           f"クラブ所属履歴 > {p['club_locator']}", p["start_summary"])

        dec("Career", hs_cid, "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
        dec("Career", uni_cid, "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
        dec("Career", club_cid, "organization_id|role|start", "end",
            "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定"
            + ("。過去クラブ在籍はissueに記録" if gap_issue_id else ""))

        issue(pid, hs_cid, "HIGH_SCHOOL_PERIOD",
              f"{plain}の桐光学園高等学校在籍そのものはB.LEAGUE公式プロフィールで確認できたが、入学・卒業年月は資料に記載がなく未確認。",
              "高校公式・大会公式ロスターでの裏付けを確認")
        issue(pid, uni_cid, "UNIVERSITY_PERIOD",
              f"{plain}の{ORG_NAMES[p['university']]}在籍そのものはB.LEAGUE公式プロフィールで確認できたが、入学・卒業年月は資料に記載がなく未確認。",
              "全日本大学バスケットボール連盟（JUBF）の年度別ロスターでの裏付けを確認")
        if gap_issue_id:
            got = issue(pid, pid, "PRO_HISTORY_GAPS",
                        f"{plain}は現所属（{ORG_NAMES[p['club']]}、{p['club_locator_short']}）以前に{p['pro_gaps']}の在籍がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
                        "後続の深掘りWaveでクラブ別Careerを追加")
            assert got == gap_issue_id, (got, gap_issue_id)
        for extra in p.get("extra_issues", []):
            issue(pid, extra.get("related", pid), extra["type"], extra["description"], extra["next_check"])

    orgs = [{"organization_id": o, "name": ORG_NAMES[o]} for o in org_ids]

    write_csv(base / "person_candidates.csv", ["person_id", "name"], persons)
    write_csv(base / "organization_candidates.csv", ["organization_id", "name"], orgs)
    write_csv(base / "career_candidates.csv", ["career_id", "person_id", "organization_id", "role", "start", "end"], careers)
    write_csv(base / "source_references.csv", ["source_id", "title", "publisher", "url", "accessed_at"], sources)
    write_csv(base / "evidence_records.csv", [
        "record_id", "entity_type", "entity_id", "field_name", "candidate_value",
        "source_id", "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note",
    ], evidence)
    write_csv(base / "issues.csv", [
        "issue_id", "person_id", "related_id", "issue_type", "status", "description", "next_check",
    ], issues)
    write_csv(base / "qa_decisions.csv", [
        "decision_id", "entity_type", "entity_id", "decision",
        "eligible_fields", "held_fields", "reason", "reviewed_at",
    ], decisions)
    print(
        f"Wrote batch_019/wave_{wave:02d}: {len(persons)} persons, {len(orgs)} orgs, {len(careers)} careers, "
        f"{len(sources)} sources, {len(evidence)} evidence, {len(decisions)} decisions, {len(issues)} issues"
    )
