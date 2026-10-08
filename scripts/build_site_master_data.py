#!/usr/bin/env python3
"""Generate the public Site data module from approved MASTER CSV files."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "data" / "master"
OUTPUT = ROOT / "site" / "app" / "master-data.ts"
# Every Master approval that contributed persons, mapped to the person list
# that packet approved. Kept complete and explicit (never a "default to the
# last known sprint" fallback) because build_site_master_data.py uses this to
# stamp each PUBLIC player with the correct approval id and approval date --
# getting this wrong would misstate the Governance v1.0 audit trail on a
# public page.
APPROVAL_PACKETS = {
    "APP-B005-20260921-01": ROOT / "data" / "verified" / "batch_005" / "person_verified.csv",
    "APP-AS001-20260921-01": ROOT / "data" / "verified" / "approval_sprint_001" / "person_review.csv",
    "APP-AS002-20260921-01": ROOT / "data" / "verified" / "approval_sprint_002" / "person_review.csv",
    "APP-AS003-20260921-01": ROOT / "data" / "verified" / "approval_sprint_003" / "person_review.csv",
    "APP-AS004-20260922-01": ROOT / "data" / "verified" / "approval_sprint_004" / "person_review.csv",
    "APP-AS005-20260923-01": ROOT / "data" / "verified" / "approval_sprint_005" / "person_review.csv",
    "APP-AS006-20260925-01": ROOT / "data" / "verified" / "approval_sprint_006" / "person_review.csv",
    "APP-AS007-20260926-01": ROOT / "data" / "verified" / "approval_sprint_007" / "person_review.csv",
    "APP-AS009-20260930-01": ROOT / "data" / "verified" / "approval_sprint_009" / "person_review.csv",
    "APP-AS010-20260930-01": ROOT / "data" / "verified" / "approval_sprint_010" / "person_review.csv",
    "APP-AS018-20261008-01": ROOT / "data" / "verified" / "approval_sprint_018" / "person_review_new_only.csv",
}
# Approvals that only ADDED careers to persons already introduced by one of
# the packets above (no new persons). They are listed in masterApprovals and
# count toward the "last updated" stamp, but never re-stamp a person's own
# approval id (that stays the approval that introduced the person).
ENRICHMENT_APPROVALS = {
    "APP-AS008-20260929-01": ROOT / "data" / "verified" / "approval_sprint_008" / "career_review.csv",
    "APP-AS011-20261003-01": ROOT / "data" / "verified" / "approval_sprint_011" / "career_review.csv",
    "APP-AS018-20261008-01": ROOT / "data" / "verified" / "approval_sprint_018" / "career_review_enrichment_only.csv",
    "APP-AS015-20261008-01": ROOT / "data" / "verified" / "approval_sprint_015" / "career_review.csv",
}
EDUCATION_MARKERS = ("高等学校", "高校", "大学", "中学校", "中学", "小学校")

FACT_LABELS = {
    "name_en": "英字表記",
    "birth_date": "生年月日",
    "height_cm": "身長",
    "weight_kg": "体重",
    "position": "ポジション",
}

CAREER_LABELS = {
    "registration_type": "登録区分",
    "contract_type": "契約区分",
    "grade": "学年",
    "league_registration": "リーグ登録",
    "competition_participation": "公式戦記録",
    "activity_period": "活動期間",
    "activity_end": "活動終了",
    "activity_status": "活動状況",
    "contract_continuation": "契約継続",
    "activity_end_announcement": "活動終了発表",
    "free_agent_list_announcement": "自由交渉選手リスト発表",
}

# Preserve public URLs that were already published before a candidate became Master.
PUBLIC_SLUGS = {
    "P000010": "shugo-toyama",
    "P000064": "yuki-kawamura",
}


def read_csv(name: str) -> list[dict[str, str]]:
    with (MASTER / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(value for value in values if value))


def display_value(field_name: str, value: str) -> str:
    if field_name == "birth_date" and len(value) == 10:
        year, month, day = value.split("-")
        return f"{year}年{int(month)}月{int(day)}日"
    if field_name == "height_cm":
        return f"{value}cm"
    if field_name == "weight_kg":
        return f"{value}kg"
    return value


def period(start: str, end: str) -> str:
    if start and end and start == end:
        return f"{start}年"
    if start and end:
        return f"{start}–{end}年"
    if start:
        return f"{start}年〜"
    if end:
        return f"〜{end}年"
    return "期間未確認"


def main() -> None:
    people = read_csv("person.csv")
    organizations = {row["organization_id"]: row["name"] for row in read_csv("organization.csv")}
    careers = read_csv("career.csv")
    sources = read_csv("source.csv")
    evidence = read_csv("evidence.csv")
    approvals = read_csv("approval_records.csv")
    current_names = read_csv("organization_current_names.csv")
    current_name_sources = {row["source_id"]: row for row in read_csv("organization_current_name_sources.csv")}

    if not approvals:
        raise SystemExit("No Master approval record found")
    if any(row["assessment"] != "SUPPORTED" for row in evidence):
        raise SystemExit("Public data can contain only SUPPORTED Master evidence")

    approvals_by_id = {row["approval_id"]: row for row in approvals}
    for approval_id in APPROVAL_PACKETS:
        if approval_id not in approvals_by_id:
            raise SystemExit(f"Missing Master approval record: {approval_id}")
    enrichment_by_person: dict[str, list[str]] = defaultdict(list)
    for approval_id, packet in ENRICHMENT_APPROVALS.items():
        with packet.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                if approval_id not in enrichment_by_person[row["person_id"]]:
                    enrichment_by_person[row["person_id"]].append(approval_id)
    approval_by_person: dict[str, str] = {}
    for approval_id, packet in APPROVAL_PACKETS.items():
        with packet.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                person_id = row["person_id"]
                if person_id in approval_by_person:
                    raise SystemExit(f"Person appears in multiple approval packets: {person_id}")
                approval_by_person[person_id] = approval_id
    # Every Master person must resolve to a real approval -- silently
    # defaulting an unmapped person to some other sprint's approval id would
    # misstate who approved them and when.
    unmapped = [row["person_id"] for row in people if row["person_id"] not in approval_by_person]
    if unmapped:
        raise SystemExit(f"Person(s) with no matching approval packet: {', '.join(unmapped)}")

    evidence_by_entity: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    source_locators: dict[str, list[str]] = defaultdict(list)
    for row in evidence:
        evidence_by_entity[(row["entity_type"], row["entity_id"])].append(row)
        source_locators[row["source_id"]].append(row["source_locator"])

    careers_by_person: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in careers:
        careers_by_person[row["person_id"]].append(row)

    def career_order(rows: list[dict[str, str]]) -> list[dict[str, str]]:
        """Chronological display order. career.csv is ordered by career_id,
        so careers added later by a deepening wave (older clubs, higher IDs)
        would otherwise appear after the current club. Schools keep their
        original relative order and come first; clubs follow, dated ones by
        start year, undated ones last in original order (in MASTER an undated
        club is usually the current one whose start is not yet confirmed)."""
        def key(item: tuple[int, dict[str, str]]):
            index, row = item
            is_school = any(m in organizations[row["organization_id"]] for m in EDUCATION_MARKERS)
            if is_school:
                return (0, 0, index)
            return (1, int(row["start"]) if row["start"] else 9999, index)
        return [row for _, row in sorted(enumerate(rows), key=key)]

    public_people = []
    for person in people:
        person_id = person["person_id"]
        person_evidence = evidence_by_entity[("Person", person_id)]
        facts = []
        for field_name, label in FACT_LABELS.items():
            rows = [row for row in person_evidence if row["field_name"] == field_name]
            if not rows:
                continue
            values = unique([display_value(field_name, row["candidate_value"]) for row in rows])
            facts.append({
                "label": label,
                "value": " / ".join(values),
                "context": rows[0]["evidence_summary"],
                "sourceIds": unique([row["source_id"] for row in rows]),
            })

        public_careers = []
        for career in career_order(careers_by_person[person_id]):
            career_evidence = evidence_by_entity[("Career", career["career_id"])]
            details = []
            if career["role"]:
                details.append("選手" if career["role"] == "Player" else career["role"])
            for field_name, label in CAREER_LABELS.items():
                values = unique([
                    row["candidate_value"]
                    for row in career_evidence
                    if row["field_name"] == field_name
                ])
                if values:
                    details.append(f"{label}：{' / '.join(values)}")
            public_careers.append({
                "id": career["career_id"],
                "period": period(career["start"], career["end"]),
                "organization": organizations[career["organization_id"]],
                "startYear": int(career["start"][:4]) if career["start"] else None,
                "endYear": int(career["end"][:4]) if career["end"] else None,
                "organizationId": career["organization_id"],
                "detail": " · ".join(details) or "所属を公式資料で確認",
                "status": "master",
                "sourceIds": unique([row["source_id"] for row in career_evidence]),
            })

        latest = public_careers[-1]
        # Per-player locators: shared sources (e.g. one standings page used
        # for many players) otherwise show every other player's locators.
        player_locators: dict[str, list[str]] = defaultdict(list)
        for row in person_evidence:
            player_locators[row["source_id"]].append(row["source_locator"])
        for career in careers_by_person[person_id]:
            for row in evidence_by_entity[("Career", career["career_id"])]:
                player_locators[row["source_id"]].append(row["source_locator"])
        public_people.append({
            "id": person_id,
            "slug": PUBLIC_SLUGS.get(person_id, person_id.lower()),
            "name": person["name"],
            "cardContext": f"{latest['period']} · {latest['organization']}",
            "dataStatus": "master",
            "approvalId": approval_by_person[person_id],
            "enrichmentApprovalIds": enrichment_by_person.get(person_id, []),
            "facts": facts,
            "careers": public_careers,
            "aliases": [],
            "sourceLocations": {sid: " / ".join(unique(locs)) for sid, locs in player_locators.items()},
        })

    public_sources = []
    for source in sources:
        locators = unique(source_locators[source["source_id"]])
        public_sources.append({
            "id": source["source_id"],
            "title": source["title"],
            "publisher": source["publisher"],
            "url": source["url"],
            "location": " / ".join(locators),
            "accessedAt": source["accessed_at"],
            "dataStatus": "master",
        })

    # Per-approval record (id -> approvedAt/verifiedCommit), so each player's
    # own dataStatus text can cite the date THEY were actually approved on,
    # instead of one global date. masterPublication is kept as a single
    # "latest approval" convenience value for anything that just wants an
    # overall "last updated" stamp.
    approval_summaries = {
        row["approval_id"]: {
            "approvalId": row["approval_id"],
            "approvedAt": row["approved_at"],
            "verifiedCommit": row["verified_commit"],
        }
        for row in approvals
        if row["approval_id"] in APPROVAL_PACKETS or row["approval_id"] in ENRICHMENT_APPROVALS
    }
    for approval_id in ENRICHMENT_APPROVALS:
        if approval_id not in approval_summaries:
            raise SystemExit(f"Missing Master approval record: {approval_id}")
    latest_approval = max(
        approval_summaries.values(),
        key=lambda summary: summary["approvedAt"],
    )
    # 改称した学校の現在の名称（付随データ）。organization.csvの名称は当時のまま表示し、これを書き添える。
    approval_ids = {row["approval_id"] for row in approvals}
    approved_at_by_id = {row["approval_id"]: row["approved_at"] for row in approvals}
    organization_current_names = {}
    for row in current_names:
        if row["organization_id"] not in organizations:
            raise SystemExit(f"Unknown organization in organization_current_names.csv: {row['organization_id']}")
        if row["approval_id"] not in approval_ids:
            raise SystemExit(f"Missing approval for organization current name: {row['current_name_id']}")
        source = current_name_sources.get(row["source_id"])
        if source is None:
            raise SystemExit(f"Missing source for organization current name: {row['current_name_id']}")
        organization_current_names[row["organization_id"]] = {
            "currentName": row["current_name"],
            "label": row["display_label"],
            "effectiveDate": row["effective_date"],
            "changeType": row["change_type"],
            "approvedAt": approved_at_by_id[row["approval_id"]],
            "source": {"title": source["title"], "publisher": source["publisher"], "url": source["url"]},
        }

    header = "// Generated by scripts/build_site_master_data.py. Do not edit directly.\n"
    body = (
        f"export const masterPublication = {json.dumps(latest_approval, ensure_ascii=False, indent=2)} as const;\n\n"
        f"export const masterApprovals = {json.dumps(approval_summaries, ensure_ascii=False, indent=2)} as const;\n\n"
        f"export const masterSources = {json.dumps(public_sources, ensure_ascii=False, indent=2)} as const;\n\n"
        f"export const masterPlayers = {json.dumps(public_people, ensure_ascii=False, indent=2)} as const;\n\n"
        f"export const masterOrganizationCurrentNames = {json.dumps(organization_current_names, ensure_ascii=False, indent=2)} as const;\n"
    )
    OUTPUT.write_text(header + body, encoding="utf-8")
    print(f"Generated {OUTPUT.relative_to(ROOT)}: {len(public_people)} players, {len(public_sources)} sources")


if __name__ == "__main__":
    main()
