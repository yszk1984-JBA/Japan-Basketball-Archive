#!/usr/bin/env python3
"""Validate a roster-based batch: 032 (+ batch_007/wave_11 re-check) or 033.

Run: validate_batch_032_roster.py [32|33]
"""

from __future__ import annotations

import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import read_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
B7 = ROOT / "data" / "candidate" / "batch_007"
CHECK_DATE = date(2026, 9, 30)
BATCH = int(sys.argv[1]) if len(sys.argv) > 1 else 32
BASE = ROOT / "data" / "candidate" / f"batch_{BATCH:03d}"
RECHECK = B7 / "wave_11" if BATCH == 32 else None
LATER = [ROOT / "data" / "candidate" / f"batch_{b:03d}" for b in (33,) if b > BATCH]


def main() -> int:
    errors: list[str] = []
    ours = [*sorted(BASE.glob("wave_*")), *([RECHECK] if RECHECK else [])]

    def is_ours(path: Path) -> bool:
        return any(w == path.parent for w in ours) or any(l in path.parents for l in LATER)

    other_people, other_careers, other_orgs = set(), {}, {}
    for r in read_csv(ROOT / "data/master/person.csv"):
        other_people.add(r["person_id"])
    for r in read_csv(ROOT / "data/master/career.csv"):
        other_careers[r["career_id"]] = r
    for r in read_csv(ROOT / "data/master/organization.csv"):
        other_orgs[r["organization_id"]] = r["name"]
    for path in (ROOT / "data" / "candidate").rglob("*.csv"):
        if is_ours(path):
            continue
        if path.name == "person_candidates.csv":
            other_people |= {r["person_id"] for r in read_csv(path)}
        elif path.name == "career_candidates.csv":
            for r in read_csv(path):
                other_careers.setdefault(r["career_id"], r)
        elif path.name == "organization_candidates.csv":
            for r in read_csv(path):
                other_orgs.setdefault(r["organization_id"], r["name"])

    b7_people, b7_careers, b7_decisions = set(), {}, {}
    for wave in sorted(B7.glob("wave_*")):
        if wave == RECHECK:
            continue
        b7_people |= {r["person_id"] for r in read_csv(wave / "person_candidates.csv")}
        for r in read_csv(wave / "career_candidates.csv"):
            b7_careers[r["career_id"]] = r
        for r in read_csv(wave / "qa_decisions.csv"):
            b7_decisions[r["entity_id"]] = r["decision"]

    new_org_names = {r["organization_id"]: r["name"] for r in read_csv(BASE / "new_organizations.csv")}
    ids = Counter()
    totals = Counter()
    lines = []
    all_new_careers: dict[str, dict] = {}
    rejected: set[str] = set()
    for wave in ours:
        persons = read_csv(wave / "person_candidates.csv")
        careers = read_csv(wave / "career_candidates.csv")
        orgs = {r["organization_id"]: r["name"] for r in read_csv(wave / "organization_candidates.csv")}
        sources = {r["source_id"] for r in read_csv(wave / "source_references.csv")}
        evidence = read_csv(wave / "evidence_records.csv")
        issues = read_csv(wave / "issues.csv")
        decisions = read_csv(wave / "qa_decisions.csv")
        recheck = wave == RECHECK
        name = "batch_007/wave_11" if recheck else f"batch_{BATCH:03d}/{wave.name}"

        for oid, oname in orgs.items():
            known = other_orgs.get(oid, new_org_names.get(oid))
            if known is None:
                errors.append(f"{name} {oid}: 未登録のOrganization")
            elif known != oname:
                errors.append(f"{name} {oid}: 名称不一致 {known!r} / {oname!r}")
        person_ids = set()
        for p in persons:
            ids["P" + p["person_id"]] += 1
            person_ids.add(p["person_id"])
            if p["person_id"] in other_people:
                errors.append(f"{p['person_id']}: 既存Person IDと重複")
        allowed_people = b7_people if recheck else person_ids
        career_ids = set()
        for c in careers:
            ids["C" + c["career_id"]] += 1
            career_ids.add(c["career_id"])
            all_new_careers[c["career_id"]] = c
            if c["career_id"] in other_careers:
                errors.append(f"{c['career_id']}: 既存Career IDと重複")
            if c["person_id"] not in allowed_people:
                errors.append(f"{c['career_id']}: Person参照が不正 {c['person_id']}")
            if c["organization_id"] not in orgs:
                errors.append(f"{c['career_id']}: Organization参照が不足")
            if c["start"] and (not c["start"].isdigit() or (c["end"] and (not c["end"].isdigit() or int(c["end"]) <= int(c["start"])))):
                errors.append(f"{c['career_id']}: start/endが不正 {c['start']}-{c['end']}")
            if c["end"] and not c["start"]:
                errors.append(f"{c['career_id']}: startなしでendあり")
        covered = Counter()
        for e in evidence:
            if e["source_id"] not in sources:
                errors.append(f"{e['record_id']}: Source参照が不足")
            ok = e["entity_id"] in career_ids or e["entity_id"] in person_ids or (recheck and e["entity_id"] in b7_careers)
            if not ok:
                errors.append(f"{e['record_id']}: 参照先が不明 {e['entity_id']}")
            if not e["source_locator"]:
                errors.append(f"{e['record_id']}: Source内位置が不足")
            covered[(e["entity_id"], e["field_name"])] += 1
        for p in persons:
            for field in ("name", "birth_date"):
                if covered[(p["person_id"], field)] < 1:
                    errors.append(f"{p['person_id']}: {field}の根拠なし")
        births = {e["entity_id"]: e["candidate_value"] for e in evidence if e["field_name"] == "birth_date"}
        for pid, b in births.items():
            y, m, d = map(int, b.split("-"))
            age = CHECK_DATE.year - y - ((CHECK_DATE.month, CHECK_DATE.day) < (m, d))
            if age < 18:
                errors.append(f"{pid}: 18歳未満（{age}歳）")
        for c in careers:
            if c["start"]:
                if covered[(c["career_id"], "organization_id")] < 2:
                    errors.append(f"{c['career_id']}: クラブのorganization_idの根拠が2件未満")
                if covered[(c["career_id"], "start")] < 1:
                    errors.append(f"{c['career_id']}: startの根拠なし")
                if c["end"] and covered[(c["career_id"], "end")] < 1:
                    errors.append(f"{c['career_id']}: endの根拠なし")
            elif covered[(c["career_id"], "organization_id")] < 1:
                errors.append(f"{c['career_id']}: 学校のorganization_idの根拠なし")
        decided = defaultdict(list)
        for d in decisions:
            decided[d["entity_id"]].append(d["decision"])
            if d["decision"] == "REJECT_CANDIDATE":
                rejected.add(d["entity_id"])
                if d["entity_id"] not in b7_careers:
                    errors.append(f"{d['decision_id']}: 取り下げ対象がbatch_007のCareerでない {d['entity_id']}")
            if d["decision"] not in {"READY_FOR_VERIFIED_REVIEW", "HOLD_CANDIDATE", "REJECT_CANDIDATE"}:
                errors.append(f"{d['decision_id']}: 判断値が不正")
        for eid in career_ids | person_ids:
            if decided.get(eid) != ["READY_FOR_VERIFIED_REVIEW"]:
                errors.append(f"{name} {eid}: 判断がない、または重複 {decided.get(eid)}")
        totals.update(persons=len(persons), careers=len(careers), evidence=len(evidence), issues=len(issues), sources=len(sources))
        lines.append(f"| {name} | {len(persons)} | {len(careers)} | {len(evidence)} | {len(sources)} | {len(issues)} |")

    for k, v in ids.items():
        if v > 1:
            errors.append(f"ID重複 {k[1:]}")
    # After the re-check, no person may hold two live Careers at the same club with the same start.
    live = [c for c in b7_careers.values() if c["career_id"] not in rejected and b7_decisions.get(c["career_id"]) != "REJECT_CANDIDATE"]
    live += list(all_new_careers.values())
    seen = Counter((c["person_id"], c["organization_id"], c["start"]) for c in live)
    for key, v in seen.items():
        if v > 1:
            errors.append(f"同じ人物・所属・開始年のCareerが{v}件 {key}")

    report = [
        ("# Batch 032（ロスター起点の横展開）・batch_007 wave_11（再確認）検証レポート" if RECHECK else
         f"# Batch {BATCH:03d}（ロスター起点の横展開）検証レポート"), "", "作成日：2026-09-30", "",
        f"- 検証：{'PASS' if not errors else 'FAIL'}", f"- エラー：{len(errors)}件",
        f"- Person：{totals['persons']}件（新規）", f"- Career：{totals['careers']}件", f"- Evidence：{totals['evidence']}件",
        f"- Source：{totals['sources']}件", f"- Issue：{totals['issues']}件",
        *([f"- 取り下げ（REJECT_CANDIDATE）：{len(rejected)}件（batch_007の期間未記録Career）"] if RECHECK else []),
        "- VERIFIED・Master・公開サイト：未変更", "",
        "| Wave | Person | Career | Evidence | Source | Issue |", "| --- | ---: | ---: | ---: | ---: | ---: |", *lines,
        "", "## エラー", "",
    ]
    report.extend(f"- {e}" for e in errors) if errors else report.append("- なし")
    (BASE / "validation_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report[:12]))
    for e in errors[:30]:
        print(" ", e)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
