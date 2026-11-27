#!/usr/bin/env python3
"""Affiliate Engine の広告データ（site/app/affiliate/*.json）を検証する。

使い方（リポジトリのルートで）:
    python3 scripts/check_affiliate_data.py            # 今日（日本時間）で判定
    python3 scripts/check_affiliate_data.py --today 2026-12-31
    python3 scripts/check_affiliate_data.py --warn-days 14

終了コード:
    0: 問題なし（警告のみを含む）
    1: エラーあり（必須項目の欠落、参照切れ、不正な素材、表示中の案件の期限切れなど）

表示判定のルールは site/app/affiliate/select.ts と同じ。どちらかを変えたら、もう一方も合わせる。
GitHub Actions（.github/workflows/affiliate-check.yml）で毎日実行する。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "site" / "app" / "affiliate"
JST = timezone(timedelta(hours=9))

ASP_ALLOWED_HOSTS = {"a8": ["a8.net"], "rakuten": ["rakuten.co.jp", "r10s.jp"]}
PARTNERSHIP = {"pending", "approved", "rejected", "ended"}
PAGE_TYPES = {"archive", "ranking", "column", "guide"}
ALLOWED_TAGS = {"a", "img", "br", "span", "div", "p", "table", "tbody", "tr", "td", "strong", "b"}
ALLOWED_ATTRS = {"href", "src", "alt", "title", "width", "height", "border", "style", "target", "rel", "class"}
FORBIDDEN_STYLE = re.compile(r"url\s*\(|expression|javascript:|@import|behavior|-moz-binding", re.I)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ID_RE = {"program": re.compile(r"^AFF\d{6}$"), "link": re.compile(r"^LNK\d{6}$"), "placement": re.compile(r"^PLC\d{3,}$")}

errors: list[str] = []
warnings: list[str] = []


def load(name: str) -> list[dict]:
    path = DATA_DIR / name
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{name}: 読み込めません（{exc}）")
        return []
    if not isinstance(value, list):
        errors.append(f"{name}: 配列ではありません")
        return []
    return value


def allowed_url(value: str | None, asp: str) -> bool:
    if not value:
        return False
    try:
        url = urlparse(value)
    except ValueError:
        return False
    host = (url.hostname or "").lower()
    if url.scheme != "https" or not host:
        return False
    return any(host == h or host.endswith("." + h) for h in ASP_ALLOWED_HOSTS.get(asp, []))


def check_raw_html(html: str | None, asp: str) -> str | None:
    if not html or not html.strip():
        return "rawHtmlが空です"
    body = re.sub(r"<!--[\s\S]*?-->", "", html)
    tag_re = re.compile(r"<\/?([a-zA-Z][a-zA-Z0-9]*)\b((?:[^>\"']|\"[^\"]*\"|'[^']*')*)>")
    attr_re = re.compile(r"([^\s\"'=<>/]+)(?:\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|([^\s\"'=<>`]+)))?")
    rest, last, has_link = "", 0, False
    for match in tag_re.finditer(body):
        rest += body[last : match.start()]
        last = match.end()
        tag = match.group(1).lower()
        if tag not in ALLOWED_TAGS:
            return f"許可していないタグ: <{tag}>"
        if match.group(0).startswith("</"):
            continue
        for attr in attr_re.finditer(re.sub(r"/\s*$", "", match.group(2))):
            name = attr.group(1).lower()
            value = attr.group(2) or attr.group(3) or attr.group(4) or ""
            if name not in ALLOWED_ATTRS:
                return f"許可していない属性: {name}"
            if name in ("href", "src"):
                if not allowed_url(value.replace("&amp;", "&"), asp):
                    return f"許可していないURL: {value[:80]}"
                if tag == "a" and name == "href":
                    has_link = True
            if name == "style" and FORBIDDEN_STYLE.search(value):
                return "style属性に使えない指定があります"
            if name == "target" and value not in ("_blank", "_self"):
                return f"target属性の値: {value}"
    rest += body[last:]
    if "<" in rest or ">" in rest:
        return "タグとして解釈できない「<」「>」があります"
    if not has_link:
        return "広告リンク（<a href>）がありません"
    return None


def check_date(where: str, field: str, value) -> str | None:
    if value in (None, ""):
        return None
    if not isinstance(value, str) or not DATE_RE.match(value):
        errors.append(f"{where}: {field} は YYYY-MM-DD 形式にしてください（{value!r}）")
        return None
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--today", help="判定に使う日付（YYYY-MM-DD、日本時間）。省略時は今日")
    parser.add_argument("--warn-days", type=int, default=14, help="期限が近い案件を警告する日数（既定14日）")
    args = parser.parse_args()
    today = args.today or datetime.now(JST).date().isoformat()
    soon = (datetime.fromisoformat(today) + timedelta(days=args.warn_days)).date().isoformat()

    programs, links, placements = load("programs.json"), load("links.json"), load("placements.json")

    # --- Program ---
    program_by_id: dict[str, dict] = {}
    for item in programs:
        pid = item.get("id", "?")
        where = f"programs.json {pid}"
        if not ID_RE["program"].match(str(pid)):
            errors.append(f"{where}: id は AFF000001 形式にしてください")
        if pid in program_by_id:
            errors.append(f"{where}: id が重複しています")
        program_by_id[pid] = item
        for key in ("name", "asp", "partnershipStatus", "categories"):
            if not item.get(key):
                errors.append(f"{where}: {key} がありません")
        if item.get("asp") not in ASP_ALLOWED_HOSTS:
            errors.append(f"{where}: asp は {sorted(ASP_ALLOWED_HOSTS)} のいずれか")
        if item.get("partnershipStatus") not in PARTNERSHIP:
            errors.append(f"{where}: partnershipStatus は {sorted(PARTNERSHIP)} のいずれか")
        if not isinstance(item.get("enabled"), bool):
            errors.append(f"{where}: enabled は true / false")
        check_date(where, "validFrom", item.get("validFrom"))
        until = check_date(where, "validUntil", item.get("validUntil"))
        checked = check_date(where, "termsCheckedAt", item.get("termsCheckedAt"))
        active = item.get("enabled") is True and item.get("partnershipStatus") == "approved"
        if item.get("enabled") is True and item.get("partnershipStatus") != "approved":
            warnings.append(f"{where}: enabled ですが提携が approved ではないため表示されません")
        if active and until and until < today:
            errors.append(f"{where}: 表示中の案件の期限（{until}）が過ぎています。enabled を false にしてデプロイしてください")
        elif active and until and until <= soon:
            warnings.append(f"{where}: 期限（{until}）が{args.warn_days}日以内に切れます")
        if active and checked and checked < (datetime.fromisoformat(today) - timedelta(days=92)).date().isoformat():
            warnings.append(f"{where}: 報酬条件・掲載規約の確認日（{checked}）から3か月以上たっています")

    # --- Link ---
    link_ids: set[str] = set()
    for item in links:
        lid = item.get("id", "?")
        where = f"links.json {lid}"
        if not ID_RE["link"].match(str(lid)):
            errors.append(f"{where}: id は LNK000001 形式にしてください")
        if lid in link_ids:
            errors.append(f"{where}: id が重複しています")
        link_ids.add(lid)
        program = program_by_id.get(item.get("programId"))
        if not program:
            errors.append(f"{where}: programId（{item.get('programId')}）が programs.json にありません")
            continue
        asp = program.get("asp")
        mode = item.get("mode")
        if mode == "rawHtml":
            reason = check_raw_html(item.get("rawHtml"), asp)
            if reason:
                errors.append(f"{where}: rawHtml を表示できません（{reason}）")
        elif mode == "fields":
            if not allowed_url(item.get("href"), asp):
                errors.append(f"{where}: href が {asp} の許可ドメインの https URL ではありません")
            if item.get("impressionPixel") and not allowed_url(item.get("impressionPixel"), asp):
                errors.append(f"{where}: impressionPixel が {asp} の許可ドメインの https URL ではありません")
            if not (item.get("label") or "").strip():
                errors.append(f"{where}: label がありません")
        else:
            errors.append(f"{where}: mode は fields / rawHtml")
        if not item.get("categories"):
            errors.append(f"{where}: categories がありません")
        if not isinstance(item.get("enabled"), bool):
            errors.append(f"{where}: enabled は true / false")
        until = check_date(where, "validUntil", item.get("validUntil"))
        program_active = program.get("enabled") is True and program.get("partnershipStatus") == "approved"
        if program_active and item.get("enabled") is True and until:
            if until < today:
                errors.append(f"{where}: 表示中の素材の期限（{until}）が過ぎています。enabled を false にしてデプロイしてください")
            elif until <= soon:
                warnings.append(f"{where}: 期限（{until}）が{args.warn_days}日以内に切れます")

    # --- Placement ---
    placement_ids: set[str] = set()
    for item in placements:
        plid = item.get("id", "?")
        where = f"placements.json {plid}"
        if not ID_RE["placement"].match(str(plid)):
            errors.append(f"{where}: id は PLC001 形式にしてください")
        if plid in placement_ids:
            errors.append(f"{where}: id が重複しています")
        placement_ids.add(plid)
        if not item.get("slot"):
            errors.append(f"{where}: slot がありません")
        types = item.get("pageTypes") or []
        if not types or any(t not in PAGE_TYPES for t in types):
            errors.append(f"{where}: pageTypes は {sorted(PAGE_TYPES)} から選んでください")
        if "archive" in types:
            warnings.append(f"{where}: archive（選手・組織ページ）はv0.1では広告を置かない方針です")
        if not isinstance(item.get("maxItems"), int) or item.get("maxItems", 0) < 1 or item.get("maxItems", 0) > 3:
            errors.append(f"{where}: maxItems は 1〜3（過剰な広告表示を避けるため）")

    active_count = sum(
        1 for p in programs if p.get("enabled") is True and p.get("partnershipStatus") == "approved"
    )
    print(f"判定日：{today}（日本時間）")
    print(f"案件 {len(programs)} 件（表示対象 {active_count} 件）／素材 {len(links)} 件／表示ルール {len(placements)} 件")
    for message in warnings:
        print(f"WARNING: {message}")
    for message in errors:
        print(f"ERROR: {message}")
    if errors:
        print(f"エラー {len(errors)} 件")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
