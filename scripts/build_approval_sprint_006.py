#!/usr/bin/env python3
"""Build the consolidated Human Approval packet for Batch 008〜018
(強豪校水平展開シリーズ、学校1〜11、22 waves、82名) VERIFIED candidates.

This generalizes build_approval_sprint_005.py (single-wave) to loop over
every wave promoted by build_verified_batches_008_018.py and produce ONE
consolidated review packet, per Yuichi's own instruction to proceed
"全batch一括で進める" (all batches together) using the traditional
(Tier-less) approval method ("従来方式で進める"), matching Approval
Sprints 001-005.

This step ONLY builds the review packet. It never writes to
data/master/*.csv and never records a Human Approval decision -- the
approval_request.md below contains a DRAFT/SUGGESTED confirmation text
only, which Yuichi must review and restate in his own words. AI must
never fabricate or pre-fill his approval.
"""

from __future__ import annotations

import csv
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "verified" / "approval_sprint_006"
VERIFIED_COMMIT = "8dd71b9"
CREATED_AT = "2026-09-25"

# (batch, wave, school label) -- mirrors build_verified_batches_008_018.py's
# MANIFEST (commit column dropped; not needed here since all waves share
# the same VERIFIED_COMMIT once promoted).
MANIFEST = [
    ("008", "wave_01", "福岡大学附属大濠高等学校（学校1/11）"),
    ("008", "wave_02", "福岡大学附属大濠高等学校（学校1/11）"),
    ("008", "wave_03", "福岡大学附属大濠高等学校（学校1/11）"),
    ("008", "wave_04", "福岡大学附属大濠高等学校（学校1/11）"),
    ("009", "wave_01", "仙台大学附属明成高等学校（学校2/11）"),
    ("010", "wave_01", "洛南高等学校（学校3/11）"),
    ("010", "wave_02", "洛南高等学校（学校3/11）"),
    ("010", "wave_03", "洛南高等学校（学校3/11）"),
    ("010", "wave_04", "洛南高等学校（学校3/11）"),
    ("011", "wave_01", "開志国際高等学校（学校4/11）"),
    ("012", "wave_01", "延岡学園高等学校（学校5/11）"),
    ("013", "wave_01", "東山高等学校（学校6/11）"),
    ("013", "wave_02", "東山高等学校（学校6/11）"),
    ("014", "wave_01", "北陸高等学校（学校7/11）"),
    ("014", "wave_02", "北陸高等学校（学校7/11）"),
    ("014", "wave_03", "北陸高等学校（学校7/11）"),
    ("014", "wave_04", "北陸高等学校（学校7/11）"),
    ("015", "wave_01", "藤枝明誠高等学校（学校8/11）"),
    ("015", "wave_02", "藤枝明誠高等学校（学校8/11）"),
    ("017", "wave_01", "土浦日本大学高等学校（学校10/11）"),
    ("017", "wave_02", "土浦日本大学高等学校（学校10/11）"),
    ("018", "wave_01", "八王子学園八王子高等学校（学校11/11）"),
]


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write(name: str, headers: list[str], rows: list[dict[str, str]]) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with (OUTPUT / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def wave_label(batch: str, wave: str, school: str) -> str:
    wave_num = wave.replace("wave_", "").lstrip("0") or wave
    return f"Batch {int(batch)} Wave {wave_num} ({school})"


def unchanged_since_verified() -> None:
    paths: list[str] = []
    for batch, wave, _school in MANIFEST:
        wave_dir = ROOT / "data" / "verified" / f"batch_{batch}_{wave}"
        paths.extend(str(path.relative_to(ROOT)) for path in sorted(wave_dir.glob("*")) if path.is_file())
    result = subprocess.run(
        ["git", "diff", "--quiet", VERIFIED_COMMIT, "--", *paths],
        cwd=ROOT,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit("Batch 008-018 VERIFIED snapshot changed after promotion")


def main() -> None:
    unchanged_since_verified()

    all_people: list[dict[str, str]] = []
    all_careers: list[dict[str, str]] = []
    all_organizations: list[dict[str, str]] = []  # raw, pre-dedup
    all_evidence: list[dict[str, str]] = []
    all_sources: list[dict[str, str]] = []
    all_issues: list[dict[str, str]] = []
    all_held_fields: list[dict[str, str]] = []

    # person_id / career_id -> the wave label they came from (for review tagging)
    label_by_person: dict[str, str] = {}
    label_by_career: dict[str, str] = {}
    labels_by_org: dict[str, list[str]] = {}

    for batch, wave, school in MANIFEST:
        source = ROOT / "data" / "verified" / f"batch_{batch}_{wave}"
        label = wave_label(batch, wave, school)

        people = read(source / "person_verified.csv")
        careers = read(source / "career_verified.csv")
        organizations = read(source / "organization_verified.csv")
        evidence = read(source / "evidence_records.csv")
        sources = read(source / "source_references.csv")
        issues = read(source / "issue_dispositions.csv")
        held_fields = read(source / "held_fields.csv")

        for row in people:
            label_by_person[row["person_id"]] = label
        for row in careers:
            label_by_career[row["career_id"]] = label
        for row in organizations:
            labels_by_org.setdefault(row["organization_id"], [])
            if label not in labels_by_org[row["organization_id"]]:
                labels_by_org[row["organization_id"]].append(label)

        all_people.extend(people)
        all_careers.extend(careers)
        all_organizations.extend(organizations)
        all_evidence.extend(evidence)
        all_sources.extend(sources)
        all_issues.extend(issues)
        all_held_fields.extend(held_fields)

    person_by_id = {row["person_id"]: row for row in all_people}
    # Dedup organizations by organization_id (the same existing organization
    # is legitimately referenced -- via Career -- from many different waves;
    # GLOBAL sequential Organization IDs mean these are the SAME row, not
    # separate candidates. First-seen name/fields are kept.)
    organization_by_id: dict[str, dict[str, str]] = {}
    for row in all_organizations:
        organization_by_id.setdefault(row["organization_id"], row)

    master_person_ids = {row["person_id"] for row in read(ROOT / "data" / "master" / "person.csv")}

    person_review: list[dict[str, str]] = []
    for person in all_people:
        pid = person["person_id"]
        related_careers = [row for row in all_careers if row["person_id"] == pid]
        related_ids = {row["career_id"] for row in related_careers}
        related_evidence = [
            row for row in all_evidence
            if row["entity_id"] == pid or row["entity_id"] in related_ids
        ]
        related_holds = [row for row in all_issues if pid in row["person_id"].split("|")]
        person_review.append({
            "person_id": pid,
            "name": person["name"],
            "verified_batch": label_by_person[pid],
            "verified_commit": VERIFIED_COMMIT,
            "career_count": str(len(related_careers)),
            "evidence_count": str(len(related_evidence)),
            "hold_issue_count": str(len(related_holds)),
            "priority_reason": "強豪校水平展開シリーズ（学校1〜11）：出身校を起点とするCareer",
        })

    career_review: list[dict[str, str]] = []
    for career in all_careers:
        cid = career["career_id"]
        career_evidence = [row for row in all_evidence if row["entity_id"] == cid]
        career_review.append({
            "verified_batch": label_by_career[cid],
            "person_id": career["person_id"],
            "name": person_by_id[career["person_id"]]["name"],
            **career,
            "organization_name": organization_by_id[career["organization_id"]]["name"],
            "evidence_count": str(len(career_evidence)),
            "source_ids": "|".join(dict.fromkeys(row["source_id"] for row in career_evidence)),
        })

    hold_review: list[dict[str, str]] = []
    for row in all_issues:
        # Some issues are shared across several persons at once (a single
        # group-level HOLD, e.g. "4名とも入学・卒業年月が未確認") and record
        # person_id as a "|"-joined list rather than one ID. Resolve each
        # referenced person's name individually rather than assuming a
        # single ID.
        person_ids = row["person_id"].split("|")
        names = "、".join(person_by_id[pid]["name"] for pid in person_ids)
        batches = "|".join(dict.fromkeys(
            label_by_person[pid] for pid in person_ids if pid in label_by_person
        ))
        hold_review.append({
            "verified_batch": batches,
            "issue_id": row["issue_id"],
            "person_id": row["person_id"],
            "name": names,
            "related_id": row["related_id"],
            "issue_type": row["issue_type"],
            "description": row["description"],
            "disposition": row["disposition"],
        })

    organization_review = [
        {"verified_batches": "|".join(labels_by_org[oid]), **row}
        for oid, row in organization_by_id.items()
    ]

    # Evidence / source / held-fields keep a per-row batch tag based on the
    # wave they were read from (recovered by re-walking the manifest, since
    # these rows have no person_id/career_id of their own to key off of).
    evidence_review: list[dict[str, str]] = []
    source_review: list[dict[str, str]] = []
    held_fields_review: list[dict[str, str]] = []
    for batch, wave, school in MANIFEST:
        source = ROOT / "data" / "verified" / f"batch_{batch}_{wave}"
        label = wave_label(batch, wave, school)
        for row in read(source / "evidence_records.csv"):
            evidence_review.append({"verified_batch": label, **row})
        for row in read(source / "source_references.csv"):
            source_review.append({"verified_batch": label, **row})
        for row in read(source / "held_fields.csv"):
            held_fields_review.append({"verified_batch": label, **row})

    write(
        "person_review.csv",
        ["person_id", "name", "verified_batch", "verified_commit", "career_count", "evidence_count", "hold_issue_count", "priority_reason"],
        person_review,
    )
    write(
        "career_review.csv",
        ["verified_batch", "person_id", "name", "career_id", "organization_id", "role", "start", "end", "organization_name", "evidence_count", "source_ids"],
        career_review,
    )
    write("organization_review.csv", ["verified_batches", "organization_id", "name"], organization_review)
    write(
        "evidence_review.csv",
        ["verified_batch", "record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id", "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"],
        evidence_review,
    )
    write("source_review.csv", ["verified_batch", "source_id", "title", "publisher", "url", "accessed_at"], source_review)
    write("hold_review.csv", ["verified_batch", "issue_id", "person_id", "name", "related_id", "issue_type", "description", "disposition"], hold_review)
    write("held_fields_review.csv", ["verified_batch", "decision_id", "entity_type", "entity_id", "held_fields", "reason"], held_fields_review)

    errors: list[str] = []
    expected = {
        "people": (len(all_people), 82),
        "careers": (len(all_careers), 242),
        "organizations (raw, pre-dedup)": (len(all_organizations), 166),
        "organizations (unique)": (len(organization_review), len(organization_by_id)),
        "evidence": (len(evidence_review), 514),
        "sources": (len(source_review), 109),
        "issues": (len(hold_review), 108),
        "held fields": (len(held_fields_review), 241),
    }
    for label, (actual, wanted) in expected.items():
        if actual != wanted:
            errors.append(f"{label}: expected {wanted}, got {actual}")
    if {row["person_id"] for row in all_people} & master_person_ids:
        errors.append("既存Master Personが混入")
    if len(all_people) != len({row["person_id"] for row in all_people}):
        errors.append("Person IDの重複あり")
    source_ids = {row["source_id"] for row in all_sources}
    held_keys = {
        (row["entity_type"], row["entity_id"], field)
        for row in all_held_fields for field in row["held_fields"].split("|")
    }
    for row in evidence_review:
        if row["assessment"] != "SUPPORTED":
            errors.append(f"{row['record_id']}: SUPPORTEDではない")
        if row["source_id"] not in source_ids:
            errors.append(f"{row['record_id']}: Source参照が不足")
        if (row["entity_type"], row["entity_id"], row["field_name"]) in held_keys:
            errors.append(f"{row['record_id']}: HOLD項目が承認候補へ混入")

    validation = [
        "# Approval Sprint 006 検証レポート", "", f"作成日：{CREATED_AT}", "",
        "## 結果", "", f"- 検証：{'PASS' if not errors else 'FAIL'}",
        f"- エラー：{len(errors)}件", f"- Person：{len(person_review)}件",
        f"- Career：{len(career_review)}件",
        f"- Organization：{len(organization_review)}件（unique、参照元は{len(all_organizations)}件）",
        f"- Evidence：{len(evidence_review)}件", f"- Source：{len(source_review)}件",
        f"- HOLD Issue：{len(hold_review)}件", f"- HOLD判断・項目：{len(held_fields_review)}件",
        f"- 対象wave数：{len(MANIFEST)}",
        "", "## エラー", "",
    ]
    validation.extend(f"- {error}" for error in errors)
    if not errors:
        validation.append("- なし")
    (OUTPUT / "validation_report.md").write_text("\n".join(validation) + "\n", encoding="utf-8")
    if errors:
        raise SystemExit("Approval Sprint 006 validation failed")

    # Per-school subtotal table (82人を1表に並べるより見通しが良いため)。
    school_stats: dict[str, dict[str, int]] = {}
    school_order: list[str] = []
    for batch, wave, school in MANIFEST:
        if school not in school_stats:
            school_stats[school] = {"persons": 0, "careers": 0, "evidence": 0, "holds": 0}
            school_order.append(school)
        source = ROOT / "data" / "verified" / f"batch_{batch}_{wave}"
        school_stats[school]["persons"] += len(read(source / "person_verified.csv"))
        school_stats[school]["careers"] += len(read(source / "career_verified.csv"))
        school_stats[school]["evidence"] += len(read(source / "evidence_records.csv"))
        school_stats[school]["holds"] += len(read(source / "issue_dispositions.csv"))

    readme = f"""# Approval Sprint 006

作成日：{CREATED_AT}

状態：HUMAN APPROVAL待ち。MASTER未反映・公開未実施。

## 対象

強豪校水平展開シリーズ（学校1〜11、Batch 008〜018、22 wave）でVERIFIED候補となり、
まだMasterに含まれていない{len(person_review)}名を対象とする。対象校は以下の通り。

{chr(10).join(f"- {s}" for s in school_order)}

対象者の氏名一覧は `person_review.csv` を参照（本READMEには全{len(person_review)}名は列挙しない）。

## 対象版

- VERIFIED snapshot commit：`{VERIFIED_COMMIT}`

## 件数

- Person：{len(person_review)}件
- Career：{len(career_review)}件
- Organization参照（unique）：{len(organization_review)}件
- Evidence：{len(evidence_review)}件
- Source：{len(source_review)}件
- HOLD Issue：{len(hold_review)}件
- HOLD判断・項目：{len(held_fields_review)}件

## 判断範囲

`evidence_review.csv`のSUPPORTED Evidenceと、対応するPerson・Career・Organizationだけが承認候補。
`hold_review.csv`と`held_fields_review.csv`は対象外で、不明値を補わない。

この資料の作成はHuman Approvalではない。Yuichiが対象版と範囲を明示して承認した後に限り、Masterへ反映できる。
"""
    (OUTPUT / "README.md").write_text(readme, encoding="utf-8")

    summary_lines = [
        "# Approval Sprint 006 レビュー要約", "", f"作成日：{CREATED_AT}", "",
        "## 学校別内訳", "",
        "| 学校 | Person | Career | Evidence | HOLD |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for school in school_order:
        s = school_stats[school]
        summary_lines.append(f"| {school} | {s['persons']} | {s['careers']} | {s['evidence']} | {s['holds']} |")
    summary_lines.extend([
        "", f"| **合計** | **{len(person_review)}** | **{len(career_review)}** | **{len(evidence_review)}** | **{len(hold_review)}** |",
        "", "## 判断方法", "",
        f"- 承認候補：{len(person_review)}人・{len(career_review)} Career・{len(evidence_review)}件のSUPPORTED Evidence",
        f"- 承認対象外：{len(hold_review)}件のHOLD Issue、{len(held_fields_review)}件のHOLD判断・項目",
        "- HOLDは未確認の期間、表記差、未収録の所属歴等であり、承認してもMasterへ入らない",
        "- 契約、リーグ登録、公式戦出場は資料が裏付ける範囲だけを採用する",
        "- 組織（Organization）は既存Master組織・新規組織を問わず、Careerの根拠として参照された組織を`organization_review.csv`に一覧化している（同一組織が複数waveから参照される場合は1行に集約し、`verified_batches`列に参照元waveを列挙）",
        "", "## 詳細ファイル", "",
        "- `person_review.csv`：対象人物と件数（全82名）",
        "- `career_review.csv`：承認候補の所属・活動歴",
        "- `evidence_review.csv`：項目別の根拠",
        "- `source_review.csv`：出典URL",
        "- `hold_review.csv`：承認対象外の未解決事項",
        "- `held_fields_review.csv`：承認対象外の判断・項目",
    ])
    (OUTPUT / "review_summary.md").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    request = f"""# Human Approval確認文（ドラフト・未使用）

この確認文は、Yuichiが資料を確認した後に、Yuichi自身の言葉で使用するための「たたき台」である。
事前入力やAIによる代筆は行わない。AIはこの文面をそのまま承認発言として記録しない。

> 対象：Approval Sprint 006の{len(person_review)}名（学校1〜11、強豪校水平展開シリーズ）。対象版：VERIFIED snapshot `{VERIFIED_COMMIT}`。範囲：`evidence_review.csv`のSUPPORTED Evidenceに対応するPerson・Career・Organization。判断：対象範囲をMasterへ反映してよい。`hold_review.csv`の全{len(hold_review)}件と`held_fields_review.csv`の全{len(held_fields_review)}件は承認対象外。

Yuichiがこの資料を確認した上で、上記と異なる範囲・条件・除外を希望する場合は、その内容をそのままチャットで伝えてほしい。
"""
    (OUTPUT / "approval_request.md").write_text(request, encoding="utf-8")

    print(
        f"Approval Sprint 006: {len(person_review)} persons, {len(career_review)} careers, "
        f"{len(organization_review)} unique organizations, {len(evidence_review)} evidence, "
        f"{len(hold_review)} HOLD issues"
    )


if __name__ == "__main__":
    main()
