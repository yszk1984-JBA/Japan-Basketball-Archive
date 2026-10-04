#!/usr/bin/env python3
"""Apply Approval Sprint 012 (period corrections for 6 B.PREMIER players) to MASTER."""

from __future__ import annotations

import csv
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "data/verified/approval_sprint_012"
MASTER = ROOT / "data/master"
PACKET_COMMIT, VERIFIED_COMMIT, APPROVAL_ID = "61ef573", "f5222d0", "APP-AS012-20261004-01"
TEXT = "対象の版（f5222d0）、範囲（期間の訂正6件）、Tier（Tier 2）を、承認します"
EV_H = ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id",
        "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"]


def read(p):
    with p.open(encoding="utf-8-sig", newline="") as h:
        return list(csv.DictReader(h))


def write(p, headers, rows):
    with p.open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=headers, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def merge(p, incoming, headers, key):
    rows = {r[key]: r for r in read(p)}
    for r in incoming:
        r = {h: r[h] for h in headers}
        if r[key] in rows and rows[r[key]] != r:
            raise SystemExit(f"conflict {r[key]}")
        rows[r[key]] = r
    out = [rows[k] for k in sorted(rows)]
    write(p, headers, out)
    return out


def main():
    tracked = [str((PACKET / n).relative_to(ROOT)) for n in ("README.md", "person_review.csv", "master_correction_review.csv",
                                                              "evidence_review.csv", "source_review.csv", "validation_report.md")]
    if subprocess.run(["git", "diff", "--quiet", PACKET_COMMIT, "--", *tracked], cwd=ROOT).returncode:
        raise SystemExit("packet changed after review")
    t = (PACKET / "master_approval.md").read_text(encoding="utf-8")
    if any(v not in t for v in (APPROVAL_ID, PACKET_COMMIT, VERIFIED_COMMIT, "承認者：Yuichi", TEXT)):
        raise SystemExit("approval record incomplete")
    careers = read(MASTER / "career.csv")
    by = {c["career_id"]: c for c in careers}
    corr = read(PACKET / "master_correction_review.csv")
    for c in corr:
        m = by[c["career_id"]]
        if (m["start"], m["end"]) != (c["old_start"], c["old_end"]):
            raise SystemExit(f"{c['career_id']}: MASTER differs from old value")
        m["start"], m["end"] = c["new_start"], c["new_end"]
    write(MASTER / "career.csv", ["career_id", "person_id", "organization_id", "role", "start", "end"], careers)
    src = merge(MASTER / "source.csv", read(PACKET / "source_review.csv"), ["source_id", "title", "publisher", "url", "accessed_at"], "source_id")
    ev = merge(MASTER / "evidence.csv", read(PACKET / "evidence_review.csv"), EV_H, "record_id")
    ap = merge(MASTER / "approval_records.csv", [{
        "approval_id": APPROVAL_ID, "batch": "Approval Sprint 012", "verified_commit": VERIFIED_COMMIT,
        "approved_scope": "6 career period corrections (B.PREMIER current clubs), 6 supported evidence (Tier 2)",
        "excluded_scope": "C000265, C000419 (pending decision)", "approved_by": "Yuichi", "approved_at": "2026-10-04",
        "approval_reference": "data/verified/approval_sprint_012/master_approval.md"}],
        ["approval_id", "batch", "verified_commit", "approved_scope", "excluded_scope", "approved_by", "approved_at", "approval_reference"], "approval_id")
    (MASTER / "corrections/2026-10-04_premier_current_club_periods.md").write_text(
        "# Master訂正記録：B.PREMIER選手6名の現所属Careerの期間\n\n作成日：2026-10-04\n承認：Approval Sprint 012（`APP-AS012-20261004-01`、Yuichi、2026-10-04、Tier 2）\n\n"
        "| Career | 訂正前 | 訂正後 | 根拠 |\n| --- | --- | --- | --- |\n" +
        "\n".join(f"| {c['career_id']}（{c['organization_name']}） | 未記録 | {c['new_start']}〜 | {c['reason']} |" for c in corr) +
        "\n\n組織・役割・終了年（空）は変更していない。根拠のEvidenceは`COR1E0001`〜`COR1E0006`。\n", encoding="utf-8")
    rep = (MASTER / "master_build_report.md").read_text(encoding="utf-8").replace("作成日：2026-10-03", "作成日：2026-10-04")
    rep = rep.replace("Career 2件追加・期間訂正3件）", "Career 2件追加・期間訂正3件）\n- `APP-AS012-20261004-01`：Approval Sprint 012（B.PREMIER選手6名の現所属Careerの期間訂正）")
    rep = re.sub(r"- Source：\d+件", f"- Source：{len(src)}件", rep)
    rep = re.sub(r"- Evidence：\d+件", f"- Evidence：{len(ev)}件", rep)
    rep = re.sub(r"- Approval：\d+件", f"- Approval：{len(ap)}件", rep)
    rep = rep.replace("訂正：2026-10-03 河村勇輝", "訂正：2026-10-04 B.PREMIER選手6名の現所属Career期間（`corrections/2026-10-04_premier_current_club_periods.md`）。2026-10-03 河村勇輝")
    (MASTER / "master_build_report.md").write_text(rep, encoding="utf-8")
    print(len(src), len(ev), len(ap))


if __name__ == "__main__":
    main()
