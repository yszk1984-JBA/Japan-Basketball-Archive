#!/usr/bin/env python3
"""Generate the public Site CANDIDATE data module from READY CSV rows.

Mirrors build_site_master_data.py's output shape (PublicPlayer / PublicSource)
but reads every data/candidate/**/ wave directory instead of data/master, and
only surfaces entities individually marked READY_FOR_VERIFIED_REVIEW in that
wave's qa_decisions.csv. A HOLD_CANDIDATE Career is dropped entirely; a field
outside a READY entity's eligible_fields is never surfaced, even if evidence
for it exists (that evidence belongs to a field still on HOLD). A Person with
no READY Career at all is dropped (nothing safe to show).

This is CANDIDATE data: sourced, but not yet through VERIFIED or Human
approval. It must never be confused with data/master/*.
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "site" / "app" / "candidate-data.ts"

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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
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


def eligible_set(row: dict[str, str] | None) -> set[str]:
    if not row or not row.get("eligible_fields"):
        return set()
    return set(row["eligible_fields"].split("|"))


def main() -> None:
    master_person_ids = {row["person_id"] for row in read_csv(ROOT / "data" / "master" / "person.csv")}
    organizations: dict[str, str] = {
        row["organization_id"]: row["name"] for row in read_csv(ROOT / "data" / "master" / "organization.csv")
    }

    wave_dirs = sorted({p.parent for p in (ROOT / "data" / "candidate").rglob("qa_decisions.csv")})

    public_people = []
    public_sources: dict[str, dict[str, str]] = {}

    for wave_dir in wave_dirs:
        person_path = wave_dir / "person_candidates.csv"
        if not person_path.exists():
            continue

        people = read_csv(person_path)
        orgs = read_csv(wave_dir / "organization_candidates.csv")
        careers = read_csv(wave_dir / "career_candidates.csv")
        sources = read_csv(wave_dir / "source_references.csv")
        evidence = read_csv(wave_dir / "evidence_records.csv")
        decisions = read_csv(wave_dir / "qa_decisions.csv")

        for row in orgs:
            organizations.setdefault(row["organization_id"], row["name"])

        decision_by_entity = {(row["entity_type"], row["entity_id"]): row for row in decisions}

        evidence_by_entity: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
        source_locators: dict[str, list[str]] = defaultdict(list)
        for row in evidence:
            evidence_by_entity[(row["entity_type"], row["entity_id"])].append(row)
            source_locators[row["source_id"]].append(row["source_locator"])

        careers_by_person: dict[str, list[dict[str, str]]] = defaultdict(list)
        for row in careers:
            careers_by_person[row["person_id"]].append(row)

        source_by_id = {row["source_id"]: row for row in sources}

        for person in people:
            person_id = person["person_id"]
            if person_id in master_person_ids:
                continue

            person_decision = decision_by_entity.get(("Person", person_id))
            if not person_decision or person_decision["decision"] != "READY_FOR_VERIFIED_REVIEW":
                continue
            person_eligible = eligible_set(person_decision)

            person_evidence = evidence_by_entity[("Person", person_id)]
            facts = []
            for field_name, label in FACT_LABELS.items():
                if field_name not in person_eligible:
                    continue
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

            used_source_ids: set[str] = set()
            for fact in facts:
                used_source_ids.update(fact["sourceIds"])

            public_careers = []
            for career in careers_by_person.get(person_id, []):
                career_decision = decision_by_entity.get(("Career", career["career_id"]))
                if not career_decision or career_decision["decision"] != "READY_FOR_VERIFIED_REVIEW":
                    continue
                career_eligible = eligible_set(career_decision)
                career_evidence = evidence_by_entity[("Career", career["career_id"])]

                details = []
                if "role" in career_eligible and career["role"]:
                    details.append("選手" if career["role"] == "Player" else career["role"])
                for field_name, label in CAREER_LABELS.items():
                    if field_name not in career_eligible:
                        continue
                    values = unique([
                        row["candidate_value"] for row in career_evidence if row["field_name"] == field_name
                    ])
                    if values:
                        details.append(f"{label}：{' / '.join(values)}")

                org_name = organizations.get(career["organization_id"], career["organization_id"])
                career_source_ids = unique([
                    row["source_id"] for row in career_evidence if row["field_name"] in career_eligible
                ])
                used_source_ids.update(career_source_ids)
                public_careers.append({
                    "id": career["career_id"],
                    "period": period(career["start"], career["end"]),
                    "organization": org_name,
                    "organizationId": career["organization_id"],
                    "detail": " · ".join(details) or "所属を公式資料で確認",
                    "status": "candidate",
                    "sourceIds": career_source_ids,
                })

            if not public_careers:
                continue

            latest = sorted(
                public_careers,
                key=lambda row: (row["period"] == "期間未確認", row["period"]),
            )[-1]
            public_people.append({
                "id": person_id,
                "slug": person_id.lower(),
                "name": person["name"],
                "cardContext": f"{latest['period']} · {latest['organization']}",
                "dataStatus": "candidate",
                "approvalId": None,
                "facts": facts,
                "careers": public_careers,
                "aliases": [],
            })

            for source_id in used_source_ids:
                if source_id in public_sources:
                    continue
                source = source_by_id.get(source_id)
                if not source:
                    continue
                locators = unique(source_locators[source_id])
                public_sources[source_id] = {
                    "id": source_id,
                    "title": source["title"],
                    "publisher": source["publisher"],
                    "url": source["url"],
                    "location": " / ".join(locators),
                    "accessedAt": source["accessed_at"],
                    "dataStatus": "candidate",
                }

    header = "// Generated by scripts/build_site_candidate_data.py. Do not edit directly.\n"
    body = (
        f"export const candidateSources = {json.dumps(list(public_sources.values()), ensure_ascii=False, indent=2)} as const;\n\n"
        f"export const candidatePlayers = {json.dumps(public_people, ensure_ascii=False, indent=2)} as const;\n"
    )
    OUTPUT.write_text(header + body, encoding="utf-8")
    print(f"Generated {OUTPUT.relative_to(ROOT)}: {len(public_people)} players, {len(public_sources)} sources")


if __name__ == "__main__":
    main()
