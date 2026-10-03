#!/usr/bin/env python3
"""Apply Yuichi's Approval Sprint 011 decision (河村勇輝 NBA update) to MASTER.

Adds 2 Careers, 2 Organizations, their SUPPORTED evidence and sources, and
applies 3 approved period corrections to existing MASTER Careers. Refuses to
run unless the packet is unchanged since review and master_approval.md holds
the approval text."""

from __future__ import annotations

import csv
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "data/verified/approval_sprint_011"
MASTER = ROOT / "data/master"
PACKET_COMMIT = "13a115e"
VERIFIED_COMMIT = "5b98773"
APPROVAL_ID = "APP-AS011-20261003-01"
TEXT = "3. Tier： 案どおりTier 2（丁寧確認）で確定する"
EV_H = ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id",
        "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"]


def read(p: Path) -> list[dict[str, str]]:
    with p.open(encoding="utf-8-sig", newline="") as h:
        return list(csv.DictReader(h))


def write(p: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    with p.open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=headers, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def merge(p: Path, incoming: list[dict[str, str]], headers: list[str], key: str) -> list[dict[str, str]]:
    rows = {r[key]: r for r in read(p)}
    for r in incoming:
        r = {h: r[h] for h in headers}
        if r[key] in rows and rows[r[key]] != r:
            raise SystemExit(f"MASTER conflict {key}={r[key]}")
        rows[r[key]] = r
    out = [rows[k] for k in sorted(rows)]
    write(p, headers, out)
    return out


def main() -> None:
    tracked = [str((PACKET / n).relative_to(ROOT)) for n in ("README.md", "person_review.csv", "career_review.csv", "organization_review.csv",
                                                              "master_correction_review.csv", "evidence_review.csv", "source_review.csv",
                                                              "hold_review.csv", "validation_report.md")]
    if subprocess.run(["git", "diff", "--quiet", PACKET_COMMIT, "--", *tracked], cwd=ROOT).returncode:
        raise SystemExit("packet differs from the reviewed version")
    text = (PACKET / "master_approval.md").read_text(encoding="utf-8")
    if any(v not in text for v in (APPROVAL_ID, PACKET_COMMIT, VERIFIED_COMMIT, "承認者：Yuichi", TEXT)):
        raise SystemExit("approval record incomplete")

    careers = read(PACKET / "career_review.csv")
    corrections = read(PACKET / "master_correction_review.csv")
    m_careers = read(MASTER / "career.csv")
    by_id = {c["career_id"]: c for c in m_careers}
    for c in corrections:
        m = by_id[c["career_id"]]
        if (m["start"], m["end"]) != (c["old_start"], c["old_end"]):
            raise SystemExit(f"{c['career_id']}: MASTER value is not the approved old value")
        m["start"], m["end"] = c["new_start"], c["new_end"]
    ch = ["career_id", "person_id", "organization_id", "role", "start", "end"]
    write(MASTER / "career.csv", ch, m_careers)
    counts = {
        "orgs": len(merge(MASTER / "organization.csv", read(PACKET / "organization_review.csv"), ["organization_id", "name"], "organization_id")),
        "careers": len(merge(MASTER / "career.csv", careers, ch, "career_id")),
        "sources": len(merge(MASTER / "source.csv", read(PACKET / "source_review.csv"), ["source_id", "title", "publisher", "url", "accessed_at"], "source_id")),
        "evidence": len(merge(MASTER / "evidence.csv", read(PACKET / "evidence_review.csv"), EV_H, "record_id")),
        "approvals": len(merge(MASTER / "approval_records.csv", [{
            "approval_id": APPROVAL_ID, "batch": "Approval Sprint 011", "verified_commit": VERIFIED_COMMIT,
            "approved_scope": "P000064: 2 careers added, 3 career period corrections, 2 organizations, 17 supported evidence (Tier 2)",
            "excluded_scope": "3 HOLD issues", "approved_by": "Yuichi", "approved_at": "2026-10-03",
            "approval_reference": "data/verified/approval_sprint_011/master_approval.md"}],
            ["approval_id", "batch", "verified_commit", "approved_scope", "excluded_scope", "approved_by", "approved_at", "approval_reference"], "approval_id")),
    }
    people = len(read(MASTER / "person.csv"))
    (MASTER / "corrections/2026-10-03_p000064_career_periods.md").write_text("""# Master訂正記録：河村勇輝（P000064）のCareer期間

作成日：2026-10-03
承認：Approval Sprint 011（`APP-AS011-20261003-01`、Yuichi、2026-10-03、Tier 2）

## 内容（`data/master/career.csv`の`start`・`end`）

| Career | クラブ | 訂正前 | 訂正後 | 根拠 |
| --- | --- | --- | --- | --- |
| C000221 | 三遠ネオフェニックス | 未記録 | 2019〜2020 | B.LEAGUE公式クラブ所属履歴「2019-20 三遠」 |
| C000222 | 横浜ビー・コルセアーズ | 未記録 | 2020〜2024 | B.LEAGUE公式クラブ所属履歴「2020-21〜2023-24 横浜BC」 |
| C000223 | メンフィス・グリズリーズ | 未記録 | 2024〜2025 | NBA公式通算成績（2024-25 MEM 22試合）・2024-25ロスター |

組織・役割は変更していない。根拠のEvidenceは`B4W7E0012`〜`B4W7E0017`。`data/candidate/`・`data/verified/`のスナップショットは変更しない。
""", encoding="utf-8")
    rep = (MASTER / "master_build_report.md").read_text(encoding="utf-8")
    import re
    rep = rep.replace("作成日：2026-10-01", "作成日：2026-10-03")
    rep = rep.replace("- `APP-AS010-20260930-01`：Approval Sprint 010（B.ONEロスター起点の横展開、batch_033、182名）",
                      "- `APP-AS010-20260930-01`：Approval Sprint 010（B.ONEロスター起点の横展開、batch_033、182名）\n- `APP-AS011-20261003-01`：Approval Sprint 011（河村勇輝のNBA経歴アップデート、batch_004 wave_07、Career 2件追加・期間訂正3件）")
    for k, label in (("orgs", "Organization"), ("careers", "Career"), ("sources", "Source"), ("evidence", "Evidence"), ("approvals", "Approval")):
        rep = re.sub(rf"- {label}：\d+件", f"- {label}：{counts[k]}件", rep)
    rep = re.sub(r"- Person：\d+件", f"- Person：{people}件", rep)
    rep = rep.replace("訂正：2026-10-01 重複Organizationの統合", "訂正：2026-10-03 河村勇輝のCareer期間（`corrections/2026-10-03_p000064_career_periods.md`）。2026-10-01 重複Organizationの統合")
    (MASTER / "master_build_report.md").write_text(rep, encoding="utf-8")
    print(counts)


if __name__ == "__main__":
    main()
