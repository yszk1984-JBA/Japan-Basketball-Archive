#!/usr/bin/env python3
"""Promote Batch 032 and the batch_007 re-check to VERIFIED.

- batch_032 wave_01..04: new persons; generic promotion (jba_lib.verify).
- batch_007: never promoted before. The 25 persons re-checked in wave_11
  (docs/ROSTER_EXPANSION_PLAN.md) have records spread over wave_01..09,
  04b and 11, so every batch_007 data wave is promoted, then Careers and
  Persons withdrawn by a LATER wave (REJECT_CANDIDATE in wave_10 / wave_11)
  are removed from the VERIFIED output and recorded in held_fields.csv.
  wave_11 has no person rows (its persons live in the earlier waves), so
  validate_verified's "unknown person" error is replaced by a check that the
  person is a batch_007 person that was not withdrawn.
Nothing is written to data/master/*.csv.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import jba_lib.verify as verify_mod  # noqa: E402
from jba_lib.verify import build_verified, validate_verified  # noqa: E402

_orig_read = verify_mod._read


def _read_normalized(path: Path) -> list[dict[str, str]]:
    """Some early batch_007 waves use the older issue layout
    (issue_id, category, scope, description). Map it to the current one
    when reading; the CANDIDATE files themselves are not changed."""
    rows = _orig_read(path)
    if path.name == "issues.csv" and rows and "category" in rows[0]:
        return [{"issue_id": r["issue_id"], "person_id": r["scope"].replace(",", "|"), "related_id": r["scope"],
                 "issue_type": r["category"], "status": "HOLD", "description": r["description"], "next_check": ""}
                for r in rows]
    return rows


verify_mod._read = _read_normalized

ROOT = Path(__file__).resolve().parents[1]
CREATED_AT = "2026-09-30"
SOURCE_COMMIT = "fa5bb78"
B32_WAVES = ["wave_01", "wave_02", "wave_03", "wave_04"]


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as h:
        return list(csv.DictReader(h))


def write(path: Path, rows: list[dict[str, str]], headers: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=headers, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def headers(path: Path) -> list[str]:
    with path.open(encoding="utf-8-sig") as h:
        return h.readline().strip().split(",")


def build_batch_007_merged() -> tuple[list[str], str]:
    """batch_007 as ONE VERIFIED set.

    batch_007's later waves (04, 04b, 08, 10, 11) add fields, Careers and
    decisions to Persons/Careers registered in earlier waves, and point to
    Sources and Organizations defined in other waves. So the waves are read
    together: a field is VERIFIED when some wave has a READY decision naming
    it and a SUPPORTED Evidence row for it; a Career value left blank in its
    row (dates added by a deepening wave) is taken from that Evidence. A
    field with conflicting Evidence values is held. The latest decision per
    entity wins (a later READY supersedes an earlier HOLD). Persons/Careers withdrawn
    by REJECT_CANDIDATE in any wave, and whole-entity HOLD_CANDIDATE
    decisions, are excluded. The CANDIDATE files must be unchanged since
    SOURCE_COMMIT.
    """
    b7 = ROOT / "data/candidate/batch_007"
    waves = sorted(p for p in b7.glob("wave_*") if p.is_dir())
    for w in waves:
        verify_mod.unchanged_since_review(ROOT, w, SOURCE_COMMIT)
    persons, orgs, careers, sources = {}, {}, {}, {}
    evidence, issues, decisions = [], [], []
    for w in waves:
        for r in read(w / "person_candidates.csv"):
            persons[r["person_id"]] = r
        for r in read(w / "organization_candidates.csv"):
            orgs.setdefault(r["organization_id"], r)
        for r in read(w / "career_candidates.csv"):
            careers.setdefault(r["career_id"], r)
        for r in read(w / "source_references.csv"):
            sources.setdefault(r["source_id"], r)
        evidence += read(w / "evidence_records.csv")
        issues += _read_normalized(w / "issues.csv")
        decisions += [{**d, "wave": w.name} for d in read(w / "qa_decisions.csv")]
    # Organizations referenced from batch_007 but registered in MASTER or
    # another batch (e.g. ORG000110 広島ドラゴンフライズ in wave_08).
    for r in read(ROOT / "data/master/organization.csv"):
        orgs.setdefault(r["organization_id"], r)
    for path in sorted((ROOT / "data/candidate").rglob("organization_candidates.csv")):
        for r in read(path):
            orgs.setdefault(r["organization_id"], r)
    # The latest decision per entity wins (waves are read in order, so
    # wave_04's READY for a Career held in wave_01 supersedes that HOLD).
    # Eligible fields are the union of READY decisions after the last
    # non-READY one.
    by_entity: dict[str, list[dict]] = {}
    for d in decisions:
        by_entity.setdefault(d["entity_id"], []).append(d)
    rejected, held_entities, eligible = {}, {}, {}
    for eid, ds in by_entity.items():
        last = ds[-1]
        if last["decision"] == "REJECT_CANDIDATE":
            rejected[eid] = last
            continue
        if last["decision"] == "HOLD_CANDIDATE":
            held_entities[eid] = last
            continue
        tail = []
        for d in reversed(ds):
            if d["decision"] != "READY_FOR_VERIFIED_REVIEW":
                break
            tail.append(d)
        eligible[eid] = {f for d in tail for f in filter(None, d["eligible_fields"].split("|"))}
    supported: dict[tuple[str, str], list[dict]] = {}
    for e in evidence:
        if e["assessment"] == "SUPPORTED":
            supported.setdefault((e["entity_id"], e["field_name"]), []).append(e)

    held_rows, v_persons, v_careers, v_evidence = [], [], [], []
    for pid, p in persons.items():
        if pid in rejected or pid in held_entities:
            held_rows.append({"decision_id": (rejected.get(pid) or held_entities[pid])["decision_id"], "entity_type": "Person",
                              "entity_id": pid, "held_fields": "all", "reason": "REJECT_CANDIDATE／HOLD_CANDIDATEのためVERIFIEDから除外"})
            continue
        if "name" in eligible.get(pid, set()):
            v_persons.append({"person_id": pid, "name": p["name"]})
            v_evidence += [e for f in eligible[pid] for e in supported.get((pid, f), [])]
    person_ids = {p["person_id"] for p in v_persons}
    for cid, c in careers.items():
        if cid in rejected or cid in held_entities or c["person_id"] not in person_ids:
            if cid in rejected or cid in held_entities:
                d = rejected.get(cid) or held_entities[cid]
                held_rows.append({"decision_id": d["decision_id"], "entity_type": "Career", "entity_id": cid, "held_fields": "all",
                                  "reason": f"{d['wave']}の{d['decision']}のためVERIFIEDから除外"})
            continue
        allowed = eligible.get(cid, set())
        if "organization_id" not in allowed or not supported.get((cid, "organization_id")):
            continue
        row = {"career_id": cid, "person_id": c["person_id"], "organization_id": c["organization_id"], "role": "", "start": "", "end": ""}
        if "role" in allowed:
            row["role"] = c["role"]
        for f in ("start", "end"):
            if f not in allowed:
                continue
            values = {e["candidate_value"] for e in supported.get((cid, f), [])}
            if c[f]:
                if values and values != {c[f]}:
                    held_rows.append({"decision_id": "", "entity_type": "Career", "entity_id": cid, "held_fields": f,
                                      "reason": f"Careerの値{c[f]}とEvidenceの値{sorted(values)}が異なるため除外"})
                    continue
                row[f] = c[f]
            elif len(values) == 1:
                row[f] = values.pop()
            elif values:
                held_rows.append({"decision_id": "", "entity_type": "Career", "entity_id": cid, "held_fields": f,
                                  "reason": f"Evidenceの値が複数（{sorted(values)}）のため除外"})
        v_careers.append(row)
        for f in ("organization_id", "role", "start", "end"):
            if row[f] or f == "organization_id":
                v_evidence += supported.get((cid, f), [])
    # de-duplicate evidence, keep order
    seen = set()
    v_evidence = [e for e in v_evidence if not (e["record_id"] in seen or seen.add(e["record_id"]))]
    used_sources = {e["source_id"] for e in v_evidence}
    used_orgs = {c["organization_id"] for c in v_careers}
    out = ROOT / "data/verified/batch_007_recheck"
    out.mkdir(parents=True, exist_ok=True)
    write(out / "person_verified.csv", v_persons, ["person_id", "name"])
    write(out / "organization_verified.csv", [{"organization_id": o, "name": orgs[o]["name"]} for o in sorted(used_orgs)], ["organization_id", "name"])
    write(out / "career_verified.csv", v_careers, ["career_id", "person_id", "organization_id", "role", "start", "end"])
    write(out / "source_references.csv", [sources[s] for s in sorted(used_sources) if s in sources],
          ["source_id", "title", "publisher", "url", "accessed_at"])
    write(out / "evidence_records.csv", v_evidence, ["record_id", "entity_type", "entity_id", "field_name", "candidate_value",
                                                     "source_id", "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"])
    write(out / "held_fields.csv", held_rows, ["decision_id", "entity_type", "entity_id", "held_fields", "reason"])
    write(out / "issue_dispositions.csv", [{**{k: i[k] for k in ("issue_id", "person_id", "related_id", "issue_type", "description")},
                                            "status": "HOLD", "disposition": "VERIFIEDへ含めず、追加の公式資料が得られるまで保留"} for i in issues],
          ["issue_id", "person_id", "related_id", "issue_type", "status", "description", "disposition"])

    errors = []
    career_ids = {c["career_id"] for c in v_careers}
    for c in v_careers:
        if c["organization_id"] not in orgs:
            errors.append(f"{c['career_id']}: unknown organization")
        if c["start"] and c["end"] and int(c["end"]) < int(c["start"]):
            errors.append(f"{c['career_id']}: end < start")
    for e in v_evidence:
        if e["source_id"] not in sources:
            errors.append(f"{e['record_id']}: unknown source")
        if e["entity_id"] not in career_ids and e["entity_id"] not in person_ids:
            errors.append(f"{e['record_id']}: evidence refers to excluded entity")
    master_people = {r["person_id"] for r in read(ROOT / "data/master/person.csv")}
    if person_ids & master_people:
        errors.append("Masterに存在するPersonが混入")
    (out / "README.md").write_text(f"""# Batch 007（全Wave統合）VERIFIED

作成日：{CREATED_AT}

状態：VERIFIED候補、HUMAN APPROVAL・MASTER未実施

batch_007は後続Wave（04・04b・08・10・11）が前のWaveの人物・Careerに項目・判断を追加する構成のため、全Waveをまとめて1つのVERIFIEDにした（`scripts/build_verified_batch_032.py`の`build_batch_007_merged`）。

- CANDIDATE・QA基準commit：`{SOURCE_COMMIT}`（全Wave変更なしを確認）
- 採用：最新の判断がREADYで、そのREADY判断（最後のHOLD・REJECT以降）が対象とし、かつSUPPORTED Evidenceがある項目
- 除外：REJECT_CANDIDATE・HOLD_CANDIDATEの人物・Career、値の食い違う項目（`held_fields.csv`）、全Issue
- Person {len(v_persons)}件、Career {len(v_careers)}件、Organization {len(used_orgs)}件、Evidence {len(v_evidence)}件、除外記録 {len(held_rows)}件、HOLD Issue {len(issues)}件
- 検証：{'PASS' if not errors else 'FAIL'}（エラー{len(errors)}件）

{chr(10).join(f"- {e}" for e in errors) if errors else ""}
VERIFIEDはHuman ApprovalまたはMasterを意味しない。
""", encoding="utf-8")
    line = f"| batch_007（全Wave統合） | {len(v_persons)} | {len(v_careers)} | {len(used_orgs)} | {len(v_evidence)} | {len(issues)} | {'PASS' if not errors else 'FAIL'} |"
    return errors, line


def main() -> int:
    lines = ["# Batch 032・batch_007（再確認）VERIFIED promotion — 生成レポート", "", f"作成日：{CREATED_AT}", "",
             f"CANDIDATE・QA基準commit：`{SOURCE_COMMIT}`", "",
             "| 対象 | Person | Career | Org | Evidence | HOLD Issue | 検証 |",
             "| --- | ---: | ---: | ---: | ---: | ---: | --- |"]
    total_errors = 0

    for wave in B32_WAVES:
        wave_dir = ROOT / "data/candidate/batch_032" / wave
        out = ROOT / "data/verified" / f"batch_032_{wave}"
        label = f"Batch 32 Wave {int(wave[-2:])} (B.PREMIERロスター起点の横展開)"
        c = build_verified(ROOT, wave_dir, out, SOURCE_COMMIT, CREATED_AT, label)
        errors = validate_verified(ROOT, out, wave_dir, label, CREATED_AT)
        total_errors += len(errors)
        lines.append(f"| batch_032/{wave} | {c['persons']} | {c['careers']} | {c['organizations']} | {c['evidence']} | {c['issues']} | {'PASS' if not errors else 'FAIL'} |")
        print(wave, c, "errors", errors[:3])

    b7_errors, b7_line = build_batch_007_merged()
    total_errors += len(b7_errors)
    lines.append(b7_line)
    print("batch_007 merged errors", b7_errors[:5])

    lines += ["", f"- エラー合計：{total_errors}件", "",
              "batch_007の八村塁（P000104）は2026-27のB.LEAGUEロスターにないため、Approval Sprint 009の対象外（VERIFIEDには含まれる）。",
              "HUMAN APPROVAL・Master・公開サイトへの反映はこの生成には含まれない。"]
    (ROOT / "data/verified/BATCH_032_VERIFIED_SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 1 if total_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
