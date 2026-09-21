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

    if not approvals:
        raise SystemExit("No Master approval record found")
    if any(row["assessment"] != "SUPPORTED" for row in evidence):
        raise SystemExit("Public data can contain only SUPPORTED Master evidence")

    evidence_by_entity: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    source_locators: dict[str, list[str]] = defaultdict(list)
    for row in evidence:
        evidence_by_entity[(row["entity_type"], row["entity_id"])].append(row)
        source_locators[row["source_id"]].append(row["source_locator"])

    careers_by_person: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in careers:
        careers_by_person[row["person_id"]].append(row)

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
        for career in careers_by_person[person_id]:
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
                "organizationId": career["organization_id"],
                "detail": " · ".join(details) or "所属を公式資料で確認",
                "status": "master",
                "sourceIds": unique([row["source_id"] for row in career_evidence]),
            })

        latest = sorted(
            public_careers,
            key=lambda row: (row["period"] == "期間未確認", row["period"]),
        )[-1]
        public_people.append({
            "id": person_id,
            "slug": person_id.lower(),
            "name": person["name"],
            "cardContext": f"{latest['period']} · {latest['organization']}",
            "dataStatus": "master",
            "approvalId": approvals[-1]["approval_id"],
            "facts": facts,
            "careers": public_careers,
            "aliases": [],
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

    approval = approvals[-1]
    header = "// Generated by scripts/build_site_master_data.py. Do not edit directly.\n"
    body = (
        f"export const masterPublication = {json.dumps({'approvalId': approval['approval_id'], 'approvedAt': approval['approved_at'], 'verifiedCommit': approval['verified_commit']}, ensure_ascii=False, indent=2)} as const;\n\n"
        f"export const masterSources = {json.dumps(public_sources, ensure_ascii=False, indent=2)} as const;\n\n"
        f"export const masterPlayers = {json.dumps(public_people, ensure_ascii=False, indent=2)} as const;\n"
    )
    OUTPUT.write_text(header + body, encoding="utf-8")
    print(f"Generated {OUTPUT.relative_to(ROOT)}: {len(public_people)} players, {len(public_sources)} sources")


if __name__ == "__main__":
    main()
