#!/usr/bin/env python3
"""Build Batch 032: roster-based expansion, B.PREMIER 2026-27 (CANDIDATE).

Yuichi (2026-09-29): 「クラブのロスター起点に選手を追加します」, with the
choices B.PREMIERの148名から / 高校・大学＋B.LEAGUE期の全所属 /
未承認25名は最新情報で確認し直して同じSprintに含める / 帰化選手も含める.
Plan: docs/ROSTER_EXPANSION_PLAN.md.

Inputs (read in the browser on 2026-09-29, stored verbatim):
- data/raw/research/bleague_roster_premier_2026-09-29.tsv: the official
  player list (/roster/?year=2026&club=<TeamID>&c=日本&e=在籍中) for the 26
  B.PREMIER clubs. 「日本」 is B.LEAGUE's own nationality filter and includes
  naturalised players.
- data/raw/research/bleague_profiles_roster_2026-09-29.txt: for every
  roster player not yet in MASTER, the profile values (name, 生年月日,
  出身校（高）, 出身校（大）, 出身地, クラブ所属履歴).
- standings / abbreviation files shared with batch_031.

Outputs:
- data/candidate/batch_032/wave_NN: new persons (P000239 onwards).
- data/candidate/batch_007/wave_11: re-check of the 25 batch_007 persons that
  were never approved and are on a 2026-27 roster (per-origin rule of
  docs/HISTORICAL_CAREER_DEEPENING_LOG.md). Undated or out-of-date club
  Careers are withdrawn (REJECT_CANDIDATE) and replaced by dated Careers from
  the official history; school Careers are kept.

Rules:
- Persons under 18 on the check date are not registered (Yuichi,
  2026-09-29, 2段階承認の条件). A profile page with no values is not
  registered either; both are listed in the README.
- Schools: one Career per school printed in 出身校（高）/（大）, split on
  「、」/「, 」. 「(在学中)」 and 「(現・…)」 are notes, not part of the name. A
  name containing 「?」 (a character the site could not render) is not
  registered and is logged. 付属/附属 spellings are treated as the same
  school. 東海大学付属第四高等学校 is the former name of
  東海大学付属札幌高等学校 (stated on the profile) and is registered as one
  Organization, like renamed clubs.
- Clubs: exactly the batch_031 rules (scripts/jba_lib/bleague_history.py).
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.bleague_history import (  # noqa: E402
    RAW, ROOT, Resolver, all_organizations, parse_history, read, season_label, stints,
)
from jba_lib.csv_io import write_csv  # noqa: E402

CHECKED_AT = "2026-09-30"
CHECK_DATE = date(2026, 9, 30)
CURRENT_SEASON = 2026
WAVE_SIZE = 40
FIRST_PERSON = 239
FIRST_CAREER = 1033
FIRST_ORG = 229
ROSTER_FILE = RAW / "bleague_roster_premier_2026-09-29.tsv"
PROFILE_FILE = RAW / "bleague_profiles_roster_2026-09-29.txt"
OUT = ROOT / "data" / "candidate" / "batch_032"
RECHECK_OUT = ROOT / "data" / "candidate" / "batch_007" / "wave_11"

# TeamIDs that are not yet an Organization -> (org_id, name). Filled from the
# unresolved list the first run prints; names are the latest spelling on the
# official standings (older spellings go to ORG_NAME_HISTORY issues).
NEW_TEAMS: dict[str, str] = {
    "751": "アイシン アレイオンズ",
}
# School spellings that name the same school (key -> canonical spelling).
# Former names (the profile itself says 「現・…」 or both spellings appear):
# one Organization, logged as ORG_NAME_HISTORY.
RENAMED_SCHOOLS = {
    "東海大学付属第四高等学校": "東海大学付属札幌高等学校",
    "東海大学付属第三高等学校": "東海大学付属諏訪高等学校",
}
# Different spellings of an already registered school (no rename involved).
SPELLING_ALIASES = {
    "桐光学園高等学校": "桐光学園高校",
    "私立延岡学園高等学校": "延岡学園高等学校",
    "学校法人土浦日本大学学園土浦日本大学高等学校": "土浦日本大学高等学校",
}
SCHOOL_ALIASES = {**RENAMED_SCHOOLS, **SPELLING_ALIASES}
# Two Organizations already registered for the same university under
# different glyphs (白鷗/白鴎). Unifying them is Yuichi's call; until then a
# person who already has one of them is not given the other.
EQUIVALENT_ORGS = {"ORG000093": "ORG000208", "ORG000208": "ORG000093"}
# Entries printed in a school field that are not schools (a club team).
NON_SCHOOL_ENTRIES = {"Tokyo Samurai"}

CAREER_HEADERS = ["career_id", "person_id", "organization_id", "role", "start", "end"]
SOURCE_HEADERS = ["source_id", "title", "publisher", "url", "accessed_at"]
EVIDENCE_HEADERS = ["record_id", "entity_type", "entity_id", "field_name", "candidate_value",
                    "source_id", "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"]
ISSUE_HEADERS = ["issue_id", "person_id", "related_id", "issue_type", "status", "description", "next_check"]
DECISION_HEADERS = ["decision_id", "entity_type", "entity_id", "decision",
                    "eligible_fields", "held_fields", "reason", "reviewed_at"]


def school_key(name: str) -> str:
    return name.replace(" ", "").replace("　", "").replace("付属", "附属")


def split_schools(text: str) -> list[dict[str, str]]:
    """「A(現・B)、C(在学中)」 -> [{printed, name, note}, ...]."""
    text = (text or "").strip()
    if text in ("", "-"):
        return []
    out = []
    for part in re.split(r"、|, | / ", text):
        part = part.strip()
        if not part:
            continue
        note = ""
        m = re.search(r"\(現・([^)]*)\)", part)
        if m:
            note = f"現・{m.group(1)}"
            part = part.replace(m.group(0), "").strip()
        if "(在学中)" in part:
            note = "在学中"
            part = part.replace("(在学中)", "").strip()
        out.append({"printed": part, "note": note})
    return out


def parse_birth(text: str) -> str:
    m = re.search(r"(\d{4})年(\d{1,2})月(\d{1,2})日", text or "")
    return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}" if m else ""


def age_on(birth: str, on: date) -> int:
    y, m, d = map(int, birth.split("-"))
    return on.year - y - ((on.month, on.day) < (m, d))


def load_profiles() -> list[dict[str, str]]:
    keys = ["pid", "kind", "club", "abbr", "rname", "title", "birth", "hs", "uni", "home", "hist"]
    rows = []
    for line in PROFILE_FILE.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        rows.append(dict(zip(keys, line.split("|"))))
    return rows


class Writer:
    """Per-wave record collector with batch-style IDs (e.g. B32W1E0001)."""

    def __init__(self, prefix: str):
        self.prefix = prefix
        self.seq = defaultdict(int)
        self.persons, self.careers, self.sources = [], [], []
        self.evidence, self.issues, self.decisions = [], [], []
        self.orgs: dict[str, str] = {}
        self.source_ids: dict[tuple, str] = {}

    def next_id(self, kind: str) -> str:
        self.seq[kind] += 1
        return f"{self.prefix}{kind}{self.seq[kind]:04d}"

    def source(self, key: tuple, title: str, url: str) -> str:
        if key not in self.source_ids:
            sid = self.next_id("S")
            self.source_ids[key] = sid
            self.sources.append({"source_id": sid, "title": title, "publisher": "B.LEAGUE", "url": url,
                                 "accessed_at": CHECKED_AT})
        return self.source_ids[key]

    def ev(self, etype, eid, field, value, sid, locator, summary, note=""):
        self.evidence.append({
            "record_id": self.next_id("E"), "entity_type": etype, "entity_id": eid, "field_name": field,
            "candidate_value": value, "source_id": sid, "source_locator": locator,
            "evidence_summary": summary, "assessment": "SUPPORTED", "checked_at": CHECKED_AT, "issue_note": note,
        })

    def issue(self, pid, related, itype, text, next_check):
        self.issues.append({"issue_id": self.next_id("I"), "person_id": pid, "related_id": related,
                            "issue_type": itype, "status": "HOLD", "description": text, "next_check": next_check})

    def decide(self, etype, eid, decision, eligible, held, reason):
        self.decisions.append({"decision_id": self.next_id("D"), "entity_type": etype, "entity_id": eid,
                               "decision": decision, "eligible_fields": eligible, "held_fields": held,
                               "reason": reason, "reviewed_at": CHECKED_AT})

    def write(self, base: Path) -> None:
        write_csv(base / "person_candidates.csv", ["person_id", "name"], self.persons)
        write_csv(base / "organization_candidates.csv", ["organization_id", "name"],
                  [{"organization_id": k, "name": v} for k, v in sorted(self.orgs.items())])
        write_csv(base / "career_candidates.csv", CAREER_HEADERS, self.careers)
        write_csv(base / "source_references.csv", SOURCE_HEADERS, self.sources)
        write_csv(base / "evidence_records.csv", EVIDENCE_HEADERS, self.evidence)
        write_csv(base / "issues.csv", ISSUE_HEADERS, self.issues)
        write_csv(base / "qa_decisions.csv", DECISION_HEADERS, self.decisions)


def main() -> None:
    orgs = all_organizations(exclude=("batch_032", "wave_11"))
    profiles = load_profiles()
    roster = [dict(zip(["club", "abbr", "pid", "name"], line.split("\t")))
              for line in ROSTER_FILE.read_text(encoding="utf-8").splitlines()
              if line and not line.startswith("#")]
    roster_club = {r["pid"]: r for r in roster}

    # ---- Targets ---------------------------------------------------------
    master_names = {r["name"].replace(" ", ""): r["person_id"] for r in read(ROOT / "data/master/person.csv")}
    known_names = set(master_names)
    for path in (ROOT / "data" / "candidate").rglob("person_candidates.csv"):
        if "batch_032" in path.parts or "wave_11" in path.parts:
            continue
        known_names |= {r["name"].replace(" ", "") for r in read(path)}

    excluded, new_targets, recheck = [], [], []
    for p in profiles:
        birth = parse_birth(p["birth"])
        if not birth:
            excluded.append((p, "プロフィールに生年月日・出身校などの値がない（ページはあるが空欄）"))
            continue
        p["birth_iso"] = birth
        p["age"] = age_on(birth, CHECK_DATE)
        if p["age"] < 18:
            excluded.append((p, f"{CHECKED_AT}時点で{p['age']}歳（18歳未満は当面対象外）"))
            continue
        if p["kind"] == "pending":
            recheck.append(p)
        elif p["title"].replace(" ", "") in master_names:
            excluded.append((p, f"同名の人物がMasterに登録済み（{master_names[p['title'].replace(' ', '')]}、MasterのSourceにこのPlayerIDがないため機械照合で拾えなかった。同一人物かは要確認）"))
        elif p["title"].replace(" ", "") in known_names or p["rname"].replace(" ", "") in known_names:
            excluded.append((p, "同名の人物が候補に登録済み（重複の可能性、要確認）"))
        else:
            new_targets.append(p)

    # ---- Organizations: new clubs, then schools -------------------------
    next_org = FIRST_ORG
    new_orgs: dict[str, str] = {}

    def add_org(name: str) -> str:
        nonlocal next_org
        oid = f"ORG{next_org:06d}"
        next_org += 1
        orgs[oid] = name
        new_orgs[oid] = name
        return oid

    extra_teams = {tid: add_org(name) for tid, name in NEW_TEAMS.items()}
    resolver = Resolver(orgs, extra_teams)

    by_key = defaultdict(set)
    for oid, name in orgs.items():
        by_key[school_key(name)].add(oid)
    printed_variants = defaultdict(list)
    for p in new_targets + recheck:
        for field in ("hs", "uni"):
            for s in split_schools(p[field]):
                if "?" in s["printed"] or s["printed"] in NON_SCHOOL_ENTRIES:
                    continue
                canon = SCHOOL_ALIASES.get(s["printed"], s["printed"])
                printed_variants[school_key(canon)].append(canon)
    school_org: dict[str, str] = {}
    for key, variants in printed_variants.items():
        found = by_key.get(key, set())
        if len(found) > 1:
            raise SystemExit(f"ambiguous existing organization for {key}: {sorted(found)}")
        if found:
            school_org[key] = next(iter(found))
        else:
            name = next((v for v in variants if "附属" in v), variants[0])
            school_org[key] = add_org(name)

    unresolved_teams = set()
    for p in new_targets + recheck:
        for y, ab in parse_history(p["hist"]):
            r = resolver.resolve(y, ab)
            if r is None or r["org"] is None:
                unresolved_teams.add((y, ab, r["tid"] if r else "?", r["season_name"] if r else ""))
    if unresolved_teams:
        for u in sorted(unresolved_teams):
            print("UNRESOLVED", u)
        raise SystemExit("add the TeamIDs above to NEW_TEAMS")

    career_seq = FIRST_CAREER

    def next_career() -> str:
        nonlocal career_seq
        cid = f"C{career_seq:06d}"
        career_seq += 1
        return cid

    def register_schools(w: Writer, pid: str, plain: str, p: dict, sid: str, existing: dict[str, dict] | None):
        """Add school Careers. existing: org_id -> existing candidate Career (recheck only)."""
        for field, label, itype, check in (
            ("hs", "出身校（高）", "HIGH_SCHOOL_PERIOD", "高校公式・大会公式ロスターでの裏付けを確認"),
            ("uni", "出身校（大）", "UNIVERSITY_PERIOD", "大学・連盟の年度別ロスターでの裏付けを確認"),
        ):
            schools = split_schools(p[field])
            if field == "hs" and not schools and existing is None:
                w.issue(pid, pid, "SCHOOL_NOT_LISTED",
                        f"{plain}のB.LEAGUE公式プロフィールでは出身校（高）が「{p[field] or '空欄'}」で、高校名を確認できない。高校のCareerは登録していない。",
                        "クラブ公式プロフィール・報道で出身校を確認")
            for s in schools:
                if "?" in s["printed"]:
                    w.issue(pid, pid, "SCHOOL_NAME_UNREADABLE",
                            f"{plain}の{label}は公式サイト上「{s['printed']}」と表示され、一部の文字が読めない。Careerは登録していない。",
                            "クラブ公式プロフィール・大学公式で正しい名称を確認")
                    continue
                if s["printed"] in NON_SCHOOL_ENTRIES:
                    w.issue(pid, pid, "NON_SCHOOL_ENTRY",
                            f"{plain}の{label}欄には「{p[field]}」とあり、「{s['printed']}」は学校ではなくクラブチームとみられる。学校のCareerとしては登録していない。",
                            "所属チームとしての在籍時期を確認")
                    continue
                canon = SCHOOL_ALIASES.get(s["printed"], s["printed"])
                oid = school_org[school_key(canon)]
                if existing is not None and (oid in existing or EQUIVALENT_ORGS.get(oid) in existing):
                    continue
                cid = next_career()
                w.careers.append({"career_id": cid, "person_id": pid, "organization_id": oid, "role": "Player",
                                  "start": "", "end": ""})
                w.orgs[oid] = orgs[oid]
                note = ""
                if s["note"] == "在学中":
                    note = "プロフィール上は「(在学中)」の表記"
                elif s["note"]:
                    note = f"プロフィール上の表記は「{s['printed']}({s['note']})」"
                w.ev("Career", cid, "organization_id", oid, sid, f"基本情報 > {label}：{p[field]}",
                     f"B.LEAGUE公式プロフィールで{label}を確認", note)
                w.decide("Career", cid, "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end",
                         "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
                w.issue(pid, cid, itype,
                        f"{plain}の{orgs[oid]}在籍はB.LEAGUE公式プロフィールで確認できたが、入学・卒業年は資料に記載がなく未確認。",
                        check)
                if s["printed"] in SPELLING_ALIASES:
                    pass
                elif canon != s["printed"] or s["note"].startswith("現・"):
                    w.issue(pid, cid, "ORG_NAME_HISTORY",
                            f"{plain}のプロフィールの{label}は「{s['printed']}」" + (f"（{s['note']}）" if s["note"].startswith("現・") else "")
                            + f"。登録Organizationは「{orgs[oid]}」。改称前後の名称を1つのOrganizationとして扱った。",
                            "Organization名称の時系列表現（改称履歴）のスキーマ整備を検討")
                if s["note"] == "在学中":
                    w.issue(pid, cid, "ENROLLED_STUDENT",
                            f"{plain}のプロフィールでは{orgs[oid]}に「在学中」と表記されている（{CHECKED_AT}時点{p['age']}歳）。",
                            "在籍状況をクラブ公式発表で確認（丁寧確認の対象）")

    def club_rows(w: Writer, pid: str, plain: str, p: dict, prof_sid: str):
        rows = parse_history(p["hist"])
        per_season = defaultdict(list)
        resolved = []
        for y, ab in rows:
            per_season[y].append(ab)
            resolved.append((y, ab, resolver.resolve(y, ab)))
        for y, abs_ in sorted(per_season.items()):
            if len(abs_) > 1:
                w.issue(pid, pid, "SAME_SEASON_TWO_CLUBS",
                        f"{plain}の所属履歴には{season_label(y)}に「{'」「'.join(abs_)}」の{len(abs_)}行がある（シーズン途中の移籍とみられる）。該当するCareerに同じ年を用いた。移籍時期・理由は記録しない。",
                        "クラブ公式の加入・退団発表で時期を確認")
        if rows and min(y for y, _ in rows) == 2016:
            w.issue(pid, pid, "PRE_BLEAGUE_HISTORY",
                    f"{plain}の公式所属履歴はB.LEAGUE開幕の2016-17シーズンから始まる。開幕前（NBL・bjリーグ等）の在籍は公式所属履歴の対象外のため未確認で、記録していない。",
                    "深掘りでNBL・bjリーグ等の当時の公式資料・クラブ公式発表を確認")
        if not any(y == CURRENT_SEASON for y, _ in rows):
            w.issue(pid, pid, "CURRENT_SEASON_NOT_IN_HISTORY",
                    f"{plain}は2026-27の公式選手一覧（{p['abbr']}）に載っているが、所属履歴に2026-27の行がない。現所属のCareerは登録していない。",
                    "クラブ公式の契約発表で確認")
        return stints(resolved)

    def add_club_career(w: Writer, pid: str, org: str, items: list, prof_sid: str) -> str:
        s, last = items[0][0], items[-1][0]
        e = "" if last >= CURRENT_SEASON else str(last + 1)
        cid = next_career()
        w.careers.append({"career_id": cid, "person_id": pid, "organization_id": org, "role": "Player",
                          "start": str(s), "end": e})
        w.orgs[org] = orgs[org]
        rows_txt = f"「{season_label(items[0][0])} {items[0][1]}」" + (
            f"〜「{season_label(items[-1][0])} {items[-1][1]}」" if len(items) > 1 else "")
        w.ev("Career", cid, "organization_id", org, prof_sid, f"クラブ所属履歴 > {rows_txt}",
             "B.LEAGUE公式の所属履歴で在籍を確認（略称表記）")
        r0 = items[0][2]
        div = {"1": "B1", "2": "B2", "3": "B3"}[r0["tab"]] if r0["std_season"] < 2026 else f"tab={r0['tab']}"
        std_sid = w.source(("standings", r0["std_season"], r0["tab"]),
                           f"B.LEAGUE 順位表 {season_label(r0['std_season'])}（{div}）",
                           f"https://www.bleague.jp/standings/?year={r0['std_season']}&tab={r0['tab']}")
        w.ev("Career", cid, "organization_id", org, std_sid,
             f"順位表 > クラブ「{r0['season_name']}」（略称「{r0['std_abbr']}」、club_detail TeamID={r0['tid']}）",
             "公式順位表で略称とクラブ名・TeamIDの対応を確認")
        w.ev("Career", cid, "start", str(s), prof_sid, f"クラブ所属履歴 > 「{season_label(s)} {items[0][1]}」",
             f"所属履歴の最初のシーズン{season_label(s)}の開始年")
        if e:
            w.ev("Career", cid, "end", e, prof_sid, f"クラブ所属履歴 > 「{season_label(last)} {items[-1][1]}」",
                 f"所属履歴の最後のシーズン{season_label(last)}の終了年")
        w.decide("Career", cid, "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start" + ("|end" if e else ""),
                 "" if e else "end",
                 "B.LEAGUE公式の所属履歴と公式順位表で確認" + ("" if e else "。2026-27在籍中のため終了年なし"))
        names_used = sorted({it[2]["season_name"] for it in items if it[2]["season_name"]})
        if any(n.replace(" ", "") != orgs[org].replace(" ", "") for n in names_used):
            w.issue(w.current_pid, cid, "ORG_NAME_HISTORY",
                    f"{cid}の在籍期間中の公式順位表上のクラブ名は「{'」「'.join(names_used)}」で、登録Organization名「{orgs[org]}」と異なる。B.LEAGUE公式のTeamID（{r0['tid']}）が同一のため、Yuichiの判断（2026-09-29、栃木→宇都宮ブレックスと同じ扱い）により同一Organizationとして登録した。",
                    "Organization名称の時系列表現（改称履歴）のスキーマ整備を検討")
        if last >= CURRENT_SEASON:
            rc = roster_club.get(w.current_bid)
            if rc:
                roster_sid = w.source(("roster", rc["club"]), f"B.LEAGUE 選手一覧 2026-27（{rc['abbr']}、日本、在籍中）",
                                      f"https://www.bleague.jp/roster/?year=2026&club={rc['club']}&c=日本&e=在籍中&o=sort")
                w.ev("Career", cid, "organization_id", org, roster_sid, f"選手一覧 > {rc['abbr']} > {rc['name']}",
                     "2026-27シーズンの公式選手一覧で現所属を確認")
        return cid

    # ---- New persons (batch_032) ----------------------------------------
    person_seq = FIRST_PERSON
    waves = [new_targets[i:i + WAVE_SIZE] for i in range(0, len(new_targets), WAVE_SIZE)]
    report = []
    for wave_no, chunk in enumerate(waves, 1):
        w = Writer(f"B32W{wave_no}")
        for p in chunk:
            pid = f"P{person_seq:06d}"
            person_seq += 1
            p["person_id"] = pid
            name = p["rname"]
            plain = name.replace(" ", "")
            w.current_pid, w.current_bid = pid, p["pid"]
            prof_sid = w.source(("profile", p["pid"]), f"{plain} 選手プロフィール",
                                f"https://www.bleague.jp/roster_detail/?PlayerID={p['pid']}")
            w.persons.append({"person_id": pid, "name": name})
            w.ev("Person", pid, "name", name, prof_sid, "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認")
            w.ev("Person", pid, "birth_date", p["birth_iso"], prof_sid, f"基本情報 > 生年月日：{p['birth'].split('｜')[0]}",
                 "B.LEAGUE公式プロフィールで生年月日を確認")
            w.decide("Person", pid, "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
            register_schools(w, pid, plain, p, prof_sid, None)
            for org, items in club_rows(w, pid, plain, p, prof_sid):
                add_club_career(w, pid, org, items, prof_sid)
        w.write(OUT / f"wave_{wave_no:02d}")
        report.append((f"batch_032/wave_{wave_no:02d}", len(w.persons), len(w.careers), len(w.evidence), len(w.issues)))

    # ---- Re-check of unapproved batch_007 persons -----------------------
    old_people, old_careers, old_dec = {}, defaultdict(list), {}
    old_sources_pid = {}
    for wdir in sorted((ROOT / "data/candidate/batch_007").glob("wave_*")):
        if wdir.name == "wave_11":
            continue
        for r in read(wdir / "person_candidates.csv"):
            old_people[r["person_id"]] = r["name"]
        for r in read(wdir / "career_candidates.csv"):
            old_careers[r["person_id"]].append(r)
        for r in read(wdir / "qa_decisions.csv"):
            old_dec[r["entity_id"]] = r["decision"]
        for r in read(wdir / "source_references.csv"):
            m = re.search(r"PlayerID=(\d+)|/player/(\d+)/", r["url"] + " " + r["publisher"])
            if m:
                old_sources_pid.setdefault(m.group(1) or m.group(2), set())
    pid_by_bid = {}
    for wdir in sorted((ROOT / "data/candidate/batch_007").glob("wave_*")):
        if wdir.name == "wave_11":
            continue
        srcs = {r["source_id"]: r for r in read(wdir / "source_references.csv")}
        for r in read(wdir / "evidence_records.csv"):
            s = srcs.get(r["source_id"])
            if not s:
                continue
            m = re.search(r"PlayerID=(\d+)|/player/(\d+)/", s["url"] + " " + s["publisher"])
            if not m:
                continue
            bid = m.group(1) or m.group(2)
            person = r["entity_id"] if r["entity_type"] == "Person" else next(
                (c["person_id"] for cs in old_careers.values() for c in cs if c["career_id"] == r["entity_id"]), None)
            if person and old_dec.get(person) != "REJECT_CANDIDATE":
                pid_by_bid.setdefault(bid, person)

    w = Writer("B7W11")
    for p in recheck:
        bid = p["pid"]
        pid = pid_by_bid.get(bid)
        if not pid:
            raise SystemExit(f"no batch_007 person for PlayerID {bid} ({p['title']})")
        plain = old_people[pid].replace(" ", "")
        w.current_pid, w.current_bid = pid, bid
        prof_sid = w.source(("profile", bid), f"{plain} 選手プロフィール（再確認）",
                            f"https://www.bleague.jp/roster_detail/?PlayerID={bid}")
        mine = [c for c in old_careers[pid] if old_dec.get(c["career_id"]) != "REJECT_CANDIDATE"]
        by_org = {c["organization_id"]: c for c in mine}
        # Schools: keep existing ones, add schools the profile lists that are missing.
        register_schools(w, pid, plain, p, prof_sid, by_org)
        for field, label in (("hs", "出身校（高）"), ("uni", "出身校（大）")):
            listed = {school_org[school_key(SCHOOL_ALIASES.get(s["printed"], s["printed"]))]
                      for s in split_schools(p[field]) if "?" not in s["printed"] and s["printed"] not in NON_SCHOOL_ENTRIES}
            for c in mine:
                if not c["start"] and (c["organization_id"] in listed or EQUIVALENT_ORGS.get(c["organization_id"]) in listed):
                    w.ev("Career", c["career_id"], "organization_id", c["organization_id"], prof_sid,
                         f"基本情報 > {label}：{p[field]}", f"最新のB.LEAGUE公式プロフィールでも{label}を確認（再確認）")
        # Clubs.
        club_stints = club_rows(w, pid, plain, p, prof_sid)
        latest = {}
        for i, (org, _) in enumerate(club_stints):
            latest[org] = i
        school_orgs = by_org_schools(p, school_org)
        used = set()
        for i, (org, items) in enumerate(club_stints):
            s, last = items[0][0], items[-1][0]
            e = "" if last >= CURRENT_SEASON else str(last + 1)
            match = None
            for c in mine:
                if c["organization_id"] != org or c["career_id"] in used:
                    continue
                if not c["start"] and not c["end"]:
                    # batch_007 registered only the then-current club, without
                    # dates: it corresponds to the latest stay at that club.
                    if i == latest[org]:
                        match = c
                        break
                    continue
                lo = int(c["start"]) if c["start"] else -1
                hi = int(c["end"]) if c["end"] else 9999
                if lo <= last + 1 and hi >= s:
                    match = c
                    break
            if match and match["start"] == str(s) and match["end"] == e:
                used.add(match["career_id"])
                continue
            new_cid = add_club_career(w, pid, org, items, prof_sid)
            if match:
                used.add(match["career_id"])
                w.decide("Career", match["career_id"], "REJECT_CANDIDATE", "", "",
                         f"最新のB.LEAGUE公式所属履歴（{CHECKED_AT}）から期間付きのCareer {new_cid}（{season_label(s)}〜{season_label(last)}）を作成したため、期間が未記録または異なる旧Career（start={match['start'] or '空'}・end={match['end'] or '空'}）を取り下げ")
        club_orgs = club_like_orgs(resolver)
        for c in mine:
            if c["career_id"] in used or c["organization_id"] in school_orgs or EQUIVALENT_ORGS.get(c["organization_id"]) in school_orgs:
                continue
            if c["organization_id"] in club_orgs and not c["start"] and not c["end"]:
                w.issue(pid, c["career_id"], "CANDIDATE_NOT_IN_HISTORY",
                        f"{plain}の候補Career {c['career_id']}（{orgs[c['organization_id']]}、期間未記録）は、最新のB.LEAGUE公式所属履歴に該当する行がない。取り下げはせず、確認待ちとした。",
                        "クラブ公式発表で在籍の有無・時期を確認")
                w.decide("Career", c["career_id"], "HOLD_CANDIDATE", "", "organization_id|role|start|end",
                         "最新の公式所属履歴に該当行がないため保留")
    w.persons = []
    w.write(RECHECK_OUT)
    report.append(("batch_007/wave_11", len(recheck), len(w.careers), len(w.evidence), len(w.issues)))

    for r in report:
        print("%s: persons=%d careers=%d evidence=%d issues=%d" % r)
    print("new organizations:", len(new_orgs))
    for oid, name in new_orgs.items():
        print("  ", oid, name)
    print("excluded:", len(excluded))
    for p, why in excluded:
        print("  ", p["pid"], p["rname"], p["abbr"], why)
    print(f"next free: Person P{person_seq:06d}, Career C{career_seq:06d}, Organization ORG{next_org:06d}")
    write_summary(new_targets, recheck, excluded, new_orgs, pid_by_bid)


def by_org_schools(p: dict, school_org: dict[str, str]) -> set[str]:
    out = set()
    for field in ("hs", "uni"):
        for s in split_schools(p[field]):
            if "?" not in s["printed"] and s["printed"] not in NON_SCHOOL_ENTRIES:
                out.add(school_org[school_key(SCHOOL_ALIASES.get(s["printed"], s["printed"]))])
    return out


def club_like_orgs(resolver: Resolver) -> set[str]:
    """Organizations that are B.LEAGUE clubs (appear on any standings page)."""
    out = set(resolver.fixed.values())
    for r in resolver.standings:
        for n in resolver.team_names[r["team_id"]]:
            out |= resolver.name_to_org.get(n.replace(" ", ""), set())
    return out


def write_summary(new_targets, recheck, excluded, new_orgs, pid_by_bid) -> None:
    from jba_lib.csv_io import write_csv as wc
    wc(OUT / "targets.csv", ["person_id", "bleague_player_id", "name", "club_abbr", "birth_date", "wave"],
       [{"person_id": p["person_id"], "bleague_player_id": p["pid"], "name": p["rname"], "club_abbr": p["abbr"],
         "birth_date": p["birth_iso"], "wave": f"wave_{i // WAVE_SIZE + 1:02d}"} for i, p in enumerate(new_targets)])
    wc(OUT / "recheck_targets.csv", ["person_id", "bleague_player_id", "name", "club_abbr"],
       [{"person_id": pid_by_bid[p["pid"]], "bleague_player_id": p["pid"], "name": p["rname"], "club_abbr": p["abbr"]}
        for p in recheck])
    wc(OUT / "excluded.csv", ["bleague_player_id", "name", "club_abbr", "reason"],
       [{"bleague_player_id": p["pid"], "name": p["rname"], "club_abbr": p["abbr"], "reason": why} for p, why in excluded])
    wc(OUT / "new_organizations.csv", ["organization_id", "name"],
       [{"organization_id": k, "name": v} for k, v in new_orgs.items()])


if __name__ == "__main__":
    main()
