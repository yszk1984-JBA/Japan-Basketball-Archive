#!/usr/bin/env python3
"""Reusable pipeline for the weekly B.PREMIER check (and other small updates).

Yuichi (2026-11-03)「Bプレミアの選手の経歴が合っているかのチェックを定期的にしたい」→
毎週（月曜の夜）、現所属＋新加入・退団、違いがあれば承認用の資料まで作る。

One JSON spec per batch (data/raw/research/weekly_spec_<date>.json) describes the findings
that were confirmed in official sources. The pipeline keeps Governance v1.0:

  candidate SPEC                 -> data/candidate/batch_NNN/wave_01      (commit = CANDIDATE)
  verified  SPEC CANDIDATE_COMMIT -> data/verified/batch_NNN_wave_01      (commit = VERIFIED)
  packet    SPEC VERIFIED_COMMIT  -> data/verified/approval_sprint_NNN    (commit = review packet)
  apply     SPEC PACKET_COMMIT    -> data/master/*                        ONLY after Yuichi's approval

`apply` refuses to run unless data/verified/approval_sprint_NNN/master_approval.md exists and
quotes Yuichi's own words with the version, the scope and the Tier. The AI never writes or
infers that approval.

Spec keys: batch, sprint, date, prefix, title, tier, sources{key:{title,publisher,url}},
new_persons[{person_id,name,birth_date?,source,locator}], new_orgs[{organization_id,name}],
careers[{career_id,person_id,organization_id,start,end,source,locator,summary}],
corrections[{career_id,new_start,new_end,source,locator,reason}],
holds[{name,description,next_check}].
"""

from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "data/master"
CAREER_H = ["career_id", "person_id", "organization_id", "role", "start", "end"]
SOURCE_H = ["source_id", "title", "publisher", "url", "accessed_at"]
EVIDENCE_H = ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id",
              "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"]
CORR_H = ["career_id", "person_id", "organization_name", "old_start", "old_end", "new_start", "new_end", "reason"]
ISSUE_H = ["issue_id", "person_id", "related_id", "issue_type", "status", "description", "next_check"]


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as h:
        return list(csv.DictReader(h))


def write(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=headers, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def git_unchanged(commit: str, *paths: Path) -> bool:
    rel = [str(p.relative_to(ROOT)) for p in paths]
    return subprocess.run(["git", "diff", "--quiet", commit, "--", *rel], cwd=ROOT).returncode == 0 and \
        subprocess.run(["git", "cat-file", "-e", f"{commit}^{{commit}}"], cwd=ROOT).returncode == 0


def period(start: str, end: str) -> str:
    if not start and not end:
        return "期間なし"
    return f"{start}〜{end}"


class Spec:
    def __init__(self, path: str):
        self.path = Path(path) if Path(path).is_absolute() else ROOT / path
        self.d = json.loads(self.path.read_text(encoding="utf-8"))
        self.batch = self.d["batch"]
        self.sprint = self.d["sprint"]
        self.cand = ROOT / f"data/candidate/batch_{self.batch}/wave_01"
        self.ver = ROOT / f"data/verified/batch_{self.batch}_wave_01"
        self.packet = ROOT / f"data/verified/approval_sprint_{self.sprint}"


def candidate(spec: Spec) -> None:
    d, p, date = spec.d, spec.d["prefix"], spec.d["date"]
    master = {r["career_id"]: r for r in read(MASTER / "career.csv")}
    people = {r["person_id"]: r["name"] for r in read(MASTER / "person.csv")}
    orgs = {r["organization_id"]: r["name"] for r in read(MASTER / "organization.csv")}
    sources, evidence = {}, []

    def sid(key: str) -> str:
        if key not in sources:
            s = d["sources"][key]
            sources[key] = {"source_id": f"{p}S{len(sources) + 1:04d}", "title": s["title"], "publisher": s["publisher"],
                            "url": s["url"], "accessed_at": date}
        return sources[key]["source_id"]

    def ev(etype: str, eid: str, field: str, value: str, src: str, loc: str, summary: str) -> None:
        evidence.append({"record_id": f"{p}E{len(evidence) + 1:04d}", "entity_type": etype, "entity_id": eid, "field_name": field,
                         "candidate_value": value, "source_id": sid(src), "source_locator": loc, "evidence_summary": summary,
                         "assessment": "SUPPORTED", "checked_at": date, "issue_note": ""})

    errors = []
    for n in d.get("new_persons", []):
        if n["person_id"] in people:
            errors.append(f"{n['person_id']} は使用済み")
        ev("Person", n["person_id"], "name", n["name"], n["source"], n["locator"], "公式プロフィールで氏名を確認")
        if n.get("birth_date"):
            ev("Person", n["person_id"], "birth_date", n["birth_date"], n["source"], n["locator"], "公式プロフィールで生年月日を確認")
    for o in d.get("new_orgs", []):
        if o["organization_id"] in orgs:
            errors.append(f"{o['organization_id']} は使用済み")
    new_pids = {n["person_id"] for n in d.get("new_persons", [])}
    new_oids = {o["organization_id"] for o in d.get("new_orgs", [])}
    careers = []
    for c in d.get("careers", []):
        if c["career_id"] in master:
            errors.append(f"{c['career_id']} は使用済み")
        if c["person_id"] not in people and c["person_id"] not in new_pids:
            errors.append(f"{c['career_id']}: 不明なPerson")
        if c["organization_id"] not in orgs and c["organization_id"] not in new_oids:
            errors.append(f"{c['career_id']}: 不明なOrganization")
        careers.append({"career_id": c["career_id"], "person_id": c["person_id"], "organization_id": c["organization_id"],
                        "role": "Player", "start": c["start"], "end": c["end"]})
        ev("Career", c["career_id"], "organization_id", c["organization_id"], c["source"], c["locator"], c["summary"])
        ev("Career", c["career_id"], "role", "Player", c["source"], c["locator"], "選手としての所属")
        for f in ("start", "end"):
            if c[f]:
                ev("Career", c["career_id"], f, c[f], c["source"], c["locator"], c["summary"])
    corrections = []
    for c in d.get("corrections", []):
        m = master.get(c["career_id"])
        if not m:
            errors.append(f"{c['career_id']}: MasterにないCareer")
            continue
        corrections.append({"career_id": c["career_id"], "person_id": m["person_id"], "organization_name": orgs[m["organization_id"]],
                            "old_start": m["start"], "old_end": m["end"], "new_start": c["new_start"], "new_end": c["new_end"],
                            "reason": c["reason"]})
        for f in ("start", "end"):
            if m[f] != c[f"new_{f}"]:
                ev("Career", c["career_id"], f, c[f"new_{f}"], c["source"], c["locator"], c["reason"])
    if errors:
        raise SystemExit("; ".join(errors))
    issues = [{"issue_id": f"{p}I{i:04d}", "person_id": "", "related_id": "", "issue_type": "HOLD", "status": "HOLD",
               "description": f"{h['name']}：{h['description']}", "next_check": h.get("next_check", "")}
              for i, h in enumerate(d.get("holds", []), 1)]
    write(spec.cand / "person_candidates.csv", ["person_id", "name"], [{"person_id": n["person_id"], "name": n["name"]} for n in d.get("new_persons", [])])
    write(spec.cand / "organization_candidates.csv", ["organization_id", "name"], d.get("new_orgs", []))
    write(spec.cand / "career_candidates.csv", CAREER_H, careers)
    write(spec.cand / "master_corrections.csv", CORR_H, corrections)
    write(spec.cand / "source_references.csv", SOURCE_H, list(sources.values()))
    write(spec.cand / "evidence_records.csv", EVIDENCE_H, evidence)
    write(spec.cand / "issues.csv", ISSUE_H, issues)
    print(f"batch_{spec.batch} CANDIDATE: persons={len(new_pids)} orgs={len(new_oids)} careers={len(careers)} "
          f"corrections={len(corrections)} evidence={len(evidence)} holds={len(issues)}")


def verified(spec: Spec, commit: str) -> None:
    files = sorted(spec.cand.glob("*.csv"))
    if not git_unchanged(commit, *files):
        raise SystemExit("CANDIDATE changed after its commit (or bad commit)")
    errors = []
    people = {r["person_id"] for r in read(MASTER / "person.csv")}
    orgs = {r["organization_id"] for r in read(MASTER / "organization.csv")}
    master = {r["career_id"]: r for r in read(MASTER / "career.csv")}
    new_p = {r["person_id"] for r in read(spec.cand / "person_candidates.csv")}
    new_o = {r["organization_id"] for r in read(spec.cand / "organization_candidates.csv")}
    careers = read(spec.cand / "career_candidates.csv")
    new_c = {c["career_id"] for c in careers}
    ev = read(spec.cand / "evidence_records.csv")
    src = {r["source_id"] for r in read(spec.cand / "source_references.csv")}
    for c in read(spec.cand / "master_corrections.csv"):
        m = master.get(c["career_id"])
        if not m or (m["start"], m["end"]) != (c["old_start"], c["old_end"]):
            errors.append(f"{c['career_id']}: MASTERの値が訂正前と一致しない")
        for f in ("start", "end"):
            if c[f"old_{f}"] != c[f"new_{f}"] and not any(e["entity_id"] == c["career_id"] and e["field_name"] == f and e["candidate_value"] == c[f"new_{f}"] for e in ev):
                errors.append(f"{c['career_id']}: {f}の根拠なし")
    for c in careers:
        if c["person_id"] not in people | new_p or c["organization_id"] not in orgs | new_o or c["career_id"] in master:
            errors.append(f"{c['career_id']}: 不正なCareer")
        if not any(e["entity_id"] == c["career_id"] and e["field_name"] == "organization_id" for e in ev):
            errors.append(f"{c['career_id']}: 所属の根拠なし")
    for pid in new_p:
        if pid in people or not any(e["entity_id"] == pid and e["field_name"] == "name" for e in ev):
            errors.append(f"{pid}: 新規Personの不備")
    for e in ev:
        if e["assessment"] != "SUPPORTED" or e["source_id"] not in src:
            errors.append(f"{e['record_id']}: SUPPORTEDでない、または出典なし")
        if e["entity_type"] == "Person" and e["entity_id"] not in people | new_p:
            errors.append(f"{e['record_id']}: 不明なPerson")
        if e["entity_type"] == "Career" and e["entity_id"] not in master and e["entity_id"] not in new_c:
            errors.append(f"{e['record_id']}: 不明なCareer")
    spec.ver.mkdir(parents=True, exist_ok=True)
    for f in files:
        (spec.ver / f.name).write_bytes(f.read_bytes())
    (spec.ver / "validation_report.md").write_text(
        f"# Batch {spec.batch} Wave 1（{spec.d['title']}）VERIFIED検証レポート\n\n作成日：{spec.d['date']}\n\n- 基準commit：`{commit}`\n"
        f"- 検証：{'PASS' if not errors else 'FAIL'}\n- 新規Person：{len(new_p)}件、新規Organization：{len(new_o)}件、Career追加：{len(careers)}件、"
        f"期間訂正：{len(read(spec.cand / 'master_corrections.csv'))}件、Evidence：{len(ev)}件\n- HUMAN APPROVAL・Master：未実施\n\n## エラー\n\n"
        + ("\n".join(f"- {e}" for e in errors) if errors else "- なし") + "\n", encoding="utf-8")
    if errors:
        raise SystemExit("VERIFIED FAIL: " + "; ".join(errors))
    print(f"batch_{spec.batch} VERIFIED: PASS")


def packet(spec: Spec, commit: str) -> None:
    files = sorted(spec.ver.glob("*"))
    if not git_unchanged(commit, *files):
        raise SystemExit("VERIFIED changed after its commit (or bad commit)")
    d = spec.d
    tier = d["tier"]
    people = {r["person_id"]: r["name"] for r in read(MASTER / "person.csv")}
    orgs = {r["organization_id"]: r["name"] for r in read(MASTER / "organization.csv")}
    new_p = {r["person_id"]: r["name"] for r in read(spec.ver / "person_candidates.csv")}
    new_o = {r["organization_id"]: r["name"] for r in read(spec.ver / "organization_candidates.csv")}
    names, onames = people | new_p, orgs | new_o
    careers = read(spec.ver / "career_candidates.csv")
    corr = read(spec.ver / "master_corrections.csv")
    ev = read(spec.ver / "evidence_records.csv")
    holds = read(spec.ver / "issues.csv")
    pk = spec.packet
    write(pk / "person_review.csv", ["person_id", "name", "status", "tier_proposal", "added_careers", "corrections", "verified_commit"],
          [{"person_id": pid, "name": names[pid], "status": "新規Person" if pid in new_p else "Master既存", "tier_proposal": tier,
            "added_careers": sum(c["person_id"] == pid for c in careers), "corrections": sum(c["person_id"] == pid for c in corr),
            "verified_commit": commit}
           for pid in sorted({c["person_id"] for c in careers} | {c["person_id"] for c in corr} | set(new_p))])
    write(pk / "person_review_new_only.csv", ["person_id", "name"], [{"person_id": k, "name": v} for k, v in new_p.items()])
    write(pk / "career_review.csv", CAREER_H[:2] + ["name", "organization_id", "organization_name", "role", "start", "end"],
          [c | {"name": names[c["person_id"]], "organization_name": onames[c["organization_id"]]} for c in careers])
    write(pk / "organization_review.csv", ["organization_id", "name", "status"],
          [{"organization_id": k, "name": v, "status": "新規（Master未登録）"} for k, v in new_o.items()])
    write(pk / "master_correction_review.csv", CORR_H, corr)
    write(pk / "evidence_review.csv", EVIDENCE_H, ev)
    write(pk / "source_review.csv", SOURCE_H, read(spec.ver / "source_references.csv"))
    write(pk / "hold_review.csv", ISSUE_H, holds)
    lines = [f"# Approval Sprint {spec.sprint}", "", f"作成日：{d['date']}", "", "状態：HUMAN APPROVAL待ち。MASTER未反映・公開未実施。", "",
             "## 対象", "", f"{d['title']}（batch_{spec.batch} wave_01）。VERIFIED snapshot commit：`{commit}`。", ""]
    if new_p:
        lines += ["### 新しく登録する選手", "", "| Person | 氏名 | 生年月日 |", "| --- | --- | --- |"]
        for pid, n in new_p.items():
            bd = next((e["candidate_value"] for e in ev if e["entity_id"] == pid and e["field_name"] == "birth_date"), "")
            lines.append(f"| {pid} | {n} | {bd or '記載なし'} |")
        lines.append("")
    if careers:
        lines += ["### 追加するCareer", "", "| Career | 選手 | 所属 | 期間 |", "| --- | --- | --- | --- |"]
        lines += [f"| {c['career_id']} | {names[c['person_id']]} | {onames[c['organization_id']]} | {period(c['start'], c['end'])} |" for c in careers]
        lines.append("")
    if corr:
        lines += ["### Masterの期間の訂正", "", "| Career | 選手 | 所属 | 今 | 訂正後 | 理由 |", "| --- | --- | --- | --- | --- | --- |"]
        lines += [f"| {c['career_id']} | {names[c['person_id']]} | {c['organization_name']} | {period(c['old_start'], c['old_end'])} | "
                  f"{period(c['new_start'], c['new_end'])} | {c['reason']} |" for c in corr]
        lines.append("")
    if new_o:
        lines += ["### 新しく登録する組織", ""] + [f"- {k} {v}" for k, v in new_o.items()] + [""]
    lines += ["## 対象外（HOLD）", ""] + ([f"- {h['description']}" for h in holds] or ["- なし"]) + [""]
    lines += ["## Tier判定案", "", f"全員{tier}（{d.get('tier_reason', '')}）。", "",
              "## 承認対象Evidence", "", f"`evidence_review.csv`の全{len(ev)}件。", "",
              "この資料の作成はHuman Approvalではない。Yuichiが対象版・範囲・Tierを明示して承認した後に限り、Masterへ反映できる。", ""]
    (pk / "README.md").write_text("\n".join(lines), encoding="utf-8")
    (pk / "validation_report.md").write_text((spec.ver / "validation_report.md").read_text(encoding="utf-8"), encoding="utf-8")
    print(f"Approval Sprint {spec.sprint} packet: persons={len(new_p)} careers={len(careers)} corrections={len(corr)} evidence={len(ev)} holds={len(holds)}")


PACKET_FILES = ["README.md", "person_review.csv", "person_review_new_only.csv", "career_review.csv", "organization_review.csv",
                "master_correction_review.csv", "evidence_review.csv", "source_review.csv", "hold_review.csv", "validation_report.md"]


def merge(path: Path, incoming: list[dict[str, str]], headers: list[str], key: str) -> int:
    merged = {r[key]: r for r in read(path)}
    for r in incoming:
        r = {h: r[h] for h in headers}
        if r[key] in merged and merged[r[key]] != r:
            raise SystemExit(f"MASTER conflict: {key}={r[key]}")
        merged[r[key]] = r
    write(path, headers, [merged[k] for k in sorted(merged)])
    return len(merged)


def apply(spec: Spec, packet_commit: str, approval_id: str, verified_commit: str) -> None:
    pk = spec.packet
    if not git_unchanged(packet_commit, *[pk / n for n in PACKET_FILES]):
        raise SystemExit("packet differs from the reviewed commit")
    approval = pk / "master_approval.md"
    if not approval.exists():
        raise SystemExit("master_approval.md がない：Yuichiの承認（版・範囲・Tier）を本人の言葉で記録してから実行する")
    text = approval.read_text(encoding="utf-8")
    for v in (approval_id, packet_commit, verified_commit, "承認者：Yuichi", "## 承認の経緯（チャットでの実際のやり取り、原文）"):
        if v not in text:
            raise SystemExit(f"approval record is incomplete ({v})")
    approved_at = re.search(r"承認日：(\d{4}-\d{2}-\d{2})", text).group(1)
    new_p = read(pk / "person_review_new_only.csv")
    careers = [{k: r[k] for k in CAREER_H} for r in read(pk / "career_review.csv")]
    corr = read(pk / "master_correction_review.csv")
    ev = [{k: r[k] for k in EVIDENCE_H} for r in read(pk / "evidence_review.csv")]
    sources = read(pk / "source_review.csv")
    orgs = [{"organization_id": r["organization_id"], "name": r["name"]} for r in read(pk / "organization_review.csv")]
    rows = read(MASTER / "career.csv")
    by_id = {r["career_id"]: r for r in rows}
    for c in corr:
        m = by_id.get(c["career_id"])
        if not m or (m["start"], m["end"]) != (c["old_start"], c["old_end"]):
            raise SystemExit(f"{c['career_id']}: MASTER differs from the reviewed old value")
        m["start"], m["end"] = c["new_start"], c["new_end"]
    write(MASTER / "career.csv", CAREER_H, rows)
    counts = {
        "people": merge(MASTER / "person.csv", new_p, ["person_id", "name"], "person_id"),
        "orgs": merge(MASTER / "organization.csv", orgs, ["organization_id", "name"], "organization_id"),
        "careers": merge(MASTER / "career.csv", careers, CAREER_H, "career_id"),
        "sources": merge(MASTER / "source.csv", sources, SOURCE_H, "source_id"),
        "evidence": merge(MASTER / "evidence.csv", ev, EVIDENCE_H, "record_id"),
    }
    holds = len(read(pk / "hold_review.csv"))
    counts["approvals"] = merge(MASTER / "approval_records.csv", [{
        "approval_id": approval_id, "batch": f"Approval Sprint {spec.sprint}", "verified_commit": verified_commit,
        "approved_scope": f"{spec.d['title']}: {len(new_p)} new persons, {len(orgs)} new organizations, {len(careers)} careers, "
                          f"{len(corr)} master career period corrections, {len(ev)} supported evidence; {spec.d['tier']}",
        "excluded_scope": f"{holds} HOLD issues", "approved_by": "Yuichi", "approved_at": approved_at,
        "approval_reference": str(approval.relative_to(ROOT)),
    }], ["approval_id", "batch", "verified_commit", "approved_scope", "excluded_scope", "approved_by", "approved_at", "approval_reference"], "approval_id")
    new_ids = {p["person_id"] for p in new_p}
    write(pk / "career_review_enrichment_only.csv", ["person_id", "career_id"],
          [{"person_id": c["person_id"], "career_id": c["career_id"]} for c in careers if c["person_id"] not in new_ids] +
          [{"person_id": c["person_id"], "career_id": c["career_id"]} for c in corr])
    # Registers this approval for scripts/build_site_master_data.py (read from site_registration.json).
    (pk / "site_registration.json").write_text(json.dumps({"approval_id": approval_id, "new_persons": bool(new_p)}, ensure_ascii=False) + "\n", encoding="utf-8")
    report = MASTER / "master_build_report.md"
    rep = report.read_text(encoding="utf-8")
    rep = rep.replace("\n\n## MASTER件数", f"\n- `{approval_id}`：Approval Sprint {spec.sprint}（{spec.d['title']}、batch_{spec.batch} wave_01、"
                      f"新規{len(new_p)}名・Career追加{len(careers)}件・期間訂正{len(corr)}件・新規Organization {len(orgs)}件、{spec.d['tier']}）\n\n## MASTER件数", 1)
    rep = re.sub(r"作成日：\S+", f"作成日：{approved_at}", rep, count=1)
    for k, lab in (("people", "Person"), ("orgs", "Organization"), ("careers", "Career"), ("sources", "Source"), ("evidence", "Evidence"), ("approvals", "Approval")):
        rep = re.sub(rf"- {lab}：\d+件", f"- {lab}：{counts[k]}件", rep)
    report.write_text(rep, encoding="utf-8")
    print(f"Approval Sprint {spec.sprint} applied:", counts)


def main() -> None:
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    cmd, spec = sys.argv[1], Spec(sys.argv[2])
    if cmd == "candidate":
        candidate(spec)
    elif cmd == "verified":
        verified(spec, sys.argv[3])
    elif cmd == "packet":
        packet(spec, sys.argv[3])
    elif cmd == "apply":
        apply(spec, sys.argv[3], sys.argv[4], sys.argv[5])
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
