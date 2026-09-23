#!/usr/bin/env python3
"""Generate the public Site CANDIDATE data module from READY CSV rows.

Mirrors build_site_master_data.py's output shape (PublicPlayer / PublicSource)
but reads every data/candidate/**/ wave directory instead of data/master, and
only surfaces entities individually marked READY_FOR_VERIFIED_REVIEW in that
entity's MOST RECENT qa_decisions.csv row. A HOLD_CANDIDATE Career is dropped
entirely; a field outside a READY entity's eligible_fields is never surfaced,
even if evidence for it exists (that evidence belongs to a field still on
HOLD). A Person with no READY Career at all is dropped (nothing safe to show).

Waves are grouped by BATCH (their parent directory), not read in isolation:
an Enrichment Wave (深掘りWave) adds no new Person/Organization/Career rows of
its own for existing entities, but supplies new evidence_records.csv and
qa_decisions.csv rows that reference Career/Organization IDs defined in an
EARLIER wave of the same batch. So within a batch, person/organization/career
rows, evidence rows and source rows are all merged across every wave before
building the public output; when more than one qa_decisions row exists for
the same (entity_type, entity_id) across waves, the row with the latest
reviewed_at (ties broken by wave directory name, i.e. the later wave) wins
in full — an Enrichment Wave's decision rows are written as a complete
restatement of eligible/held fields, not a delta, so "latest wins" is safe.

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
    batches: dict[Path, list[Path]] = defaultdict(list)
    for wave_dir in wave_dirs:
        batches[wave_dir.parent].append(wave_dir)

    public_people = []
    public_sources: dict[str, dict[str, str]] = {}

    for batch_dir, batch_wave_dirs in sorted(batches.items()):
        batch_wave_dirs = sorted(batch_wave_dirs)  # wave_01 < wave_02 < ... so later wave sorts last

        people: dict[str, dict[str, str]] = {}
        careers_by_person: dict[str, list[dict[str, str]]] = defaultdict(list)
        source_by_id: dict[str, dict[str, str]] = {}
        evidence_by_entity: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
        source_locators: dict[str, list[str]] = defaultdict(list)
        # (entity_type, entity_id) -> (reviewed_at, wave_dir_name, decision_row); later wave / later
        # reviewed_at wins outright, since an Enrichment Wave's decision row is a full restatement.
        decision_by_entity: dict[tuple[str, str], tuple[str, str, dict[str, str]]] = {}

        for wave_dir in batch_wave_dirs:
            person_path = wave_dir / "person_candidates.csv"
            if not person_path.exists():
                continue

            for row in read_csv(person_path):
                people.setdefault(row["person_id"], row)
            for row in read_csv(wave_dir / "organization_candidates.csv"):
                organizations.setdefault(row["organization_id"], row["name"])
            for row in read_csv(wave_dir / "career_candidates.csv"):
                careers_by_person[row["person_id"]].append(row)
            for row in read_csv(wave_dir / "source_references.csv"):
                source_by_id.setdefault(row["source_id"], row)
            for row in read_csv(wave_dir / "evidence_records.csv"):
                evidence_by_entity[(row["entity_type"], row["entity_id"])].append(row)
                source_locators[row["source_id"]].append(row["source_locator"])
            for row in read_csv(wave_dir / "qa_decisions.csv"):
                key = (row["entity_type"], row["entity_id"])
                candidate = (row.get("reviewed_at", ""), wave_dir.name, row)
                existing = decision_by_entity.get(key)
                if existing is None or candidate[:2] >= existing[:2]:
                    decision_by_entity[key] = candidate

        decisions_final = {key: value[2] for key, value in decision_by_entity.items()}

        for person_id, person in people.items():
            if person_id in master_person_ids:
                continue

            person_decision = decisions_final.get(("Person", person_id))
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
                career_decision = decisions_final.get(("Career", career["career_id"]))
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

                # start/end may now come from either the career's own row (as originally
                # recorded) or be confirmed later by an Enrichment Wave's evidence; prefer
                # the career row's own values, falling back to eligible evidence values.
                start = career["start"]
                end = career["end"]
                if not start and "start" in career_eligible:
                    start_values = unique([row["candidate_value"] for row in career_evidence if row["field_name"] == "start"])
                    start = start_values[0] if start_values else ""
                if not end and "end" in career_eligible:
                    end_values = unique([row["candidate_value"] for row in career_evidence if row["field_name"] == "end"])
                    end = end_values[0] if end_values else ""

                org_name = organizations.get(career["organization_id"], career["organization_id"])
                career_source_ids = unique([
                    row["source_id"] for row in career_evidence if row["field_name"] in career_eligible
                ])
                used_source_ids.update(career_source_ids)
                public_careers.append({
                    "id": career["career_id"],
                    "period": period(start, end),
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
