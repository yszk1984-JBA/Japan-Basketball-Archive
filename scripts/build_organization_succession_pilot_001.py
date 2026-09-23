#!/usr/bin/env python3
"""Build Organization Succession Pilot 001.

Per Yuichi's decision (2026-09-23) on
docs/ORGANIZATION_SUCCESSION_PROPOSAL_V0.1.md:
- スキーマ拡張の方針: Option A（付随リンクファイルを追加、中心4エンティティは不変）
- 承継とみなす範囲: 名称変更のみ（運営権異動は対象外）
- 公開サイトでの見せ方: 今回は保留

This pilot creates CANDIDATE data for organization_successions using the
2 (of 3) known cases where BOTH the pre- and post-rename Organization IDs
already exist as registered candidates:

1. 湘南ユナイテッドBC (ORG000163) -> ウォルガ湘南 (ORG000050)
2. 東芝ブレイブサンダース (ORG000164) -> 川崎ブレイブサンダース (ORG000122)

The third known case, サンロッカーズ渋谷 -> 東京サンロッカーズ
(ORG000114), is NOT included here: サンロッカーズ渋谷 (the pre-rename
name) was never registered as its own Organization, because no Career
so far has needed to reference it under that name (田中大貴's Master
Career already uses the post-rename ORG000114). A succession link needs
a predecessor_organization_id to point to, so this is left as an open
question for Yuichi rather than guessed at (see pilot README).
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "organization_succession_pilot_001"

SOURCES = [
    {
        "source_id": "OSS0001",
        "title": "2026-27シーズンよりクラブ名称変更のお知らせ",
        "publisher": "B3リーグ 湘南ユナイテッドBC公式サイト",
        "url": "https://shonan-united.com/news/20260523-01/",
        "accessed_at": "2026-09-23",
    },
    {
        "source_id": "OSS0002",
        "title": "川崎ブレイブサンダース",
        "publisher": "Wikipedia日本語版",
        "url": "https://ja.wikipedia.org/wiki/川崎ブレイブサンダース",
        "accessed_at": "2026-09-23",
    },
]

SUCCESSIONS = [
    {
        "succession_id": "OSC0001",
        "predecessor_organization_id": "ORG000163",
        "predecessor_name": "湘南ユナイテッドBC",
        "successor_organization_id": "ORG000050",
        "successor_name": "ウォルガ湘南",
        "effective_date": "2026",
        "effective_date_precision": "season",
        "reason": "NAME_CHANGE",
        "source_id": "OSS0001",
        "source_locator": "本文 > 「このたび、湘南ユナイテッドBCは、2026-27シーズンよりクラブ名称を「ウォルガ湘南」へ変更いたします」",
        "assessment": "SUPPORTED",
    },
    {
        "succession_id": "OSC0002",
        "predecessor_organization_id": "ORG000164",
        "predecessor_name": "東芝ブレイブサンダース",
        "successor_organization_id": "ORG000122",
        "successor_name": "川崎ブレイブサンダース",
        "effective_date": "2016-07-01",
        "effective_date_precision": "day",
        "reason": "NAME_CHANGE",
        "source_id": "OSS0002",
        "source_locator": "沿革 > 「2016年7月1日、正式クラブ名を『東芝川崎ブレイブサンダース』、リーグでのチーム呼称を『川崎ブレイブサンダース』に変更した」",
        "assessment": "SUPPORTED",
    },
]


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    write_csv(BASE / "source_references.csv", SOURCES, ["source_id", "title", "publisher", "url", "accessed_at"])
    write_csv(BASE / "organization_succession_candidates.csv", SUCCESSIONS, [
        "succession_id", "predecessor_organization_id", "predecessor_name",
        "successor_organization_id", "successor_name", "effective_date",
        "effective_date_precision", "reason", "source_id", "source_locator", "assessment",
    ])
    print(f"Wrote organization_succession_pilot_001: {len(SUCCESSIONS)} successions, {len(SOURCES)} sources")


if __name__ == "__main__":
    main()
