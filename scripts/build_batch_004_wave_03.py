#!/usr/bin/env python3
"""Build Batch 004 Wave 3 candidate files without touching VERIFIED or MASTER."""

from __future__ import annotations

import csv
from pathlib import Path


OUT = Path("data/candidate/batch_004/wave_03")
CHECKED = "2026-09-20"


def write(name: str, headers: list[str], rows: list[list[str]]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(headers)
        writer.writerows(rows)


def main() -> None:
    write("person_candidates.csv", ["person_id", "name"], [
        ["P000068", "重冨 周希"],
        ["P000069", "重冨 友希"],
        ["P000014", "キエキエ トピー アリ"],
        ["P000070", "遥 天翼"],
    ])
    write("organization_candidates.csv", ["organization_id", "name"], [
        ["ORG000010", "福岡第一高等学校"], ["ORG000015", "東海大学"],
        ["ORG000018", "専修大学"], ["ORG000040", "ライジングゼファー福岡"],
        ["ORG000050", "ウォルガ湘南"], ["ORG000052", "新潟アルビレックスBB"],
        ["ORG000054", "名古屋ダイヤモンドドルフィンズ"], ["ORG000067", "熊本ヴォルターズ"],
        ["ORG000090", "横浜エクセレンス"], ["ORG000100", "山口パッツファイブ"],
        ["ORG000101", "鹿児島レブナイズ"], ["ORG000102", "東京サンレーヴス"],
        ["ORG000103", "茨城ロボッツ"], ["ORG000104", "三菱電機ダイヤモンドドルフィンズ"],
    ])
    careers = [
        ["C000232", "P000068", "ORG000010", "Player", "", ""],
        ["C000233", "P000068", "ORG000018", "Player", "2017", ""],
        ["C000234", "P000068", "ORG000040", "Player", "2021", "2024"],
        ["C000235", "P000068", "ORG000050", "Player", "2026", ""],
        ["C000236", "P000069", "ORG000010", "Player", "", ""],
        ["C000237", "P000069", "ORG000018", "Player", "2017", ""],
        ["C000238", "P000069", "ORG000040", "Player", "2021", "2023"],
        ["C000239", "P000069", "ORG000100", "Player", "2022", "2026"],
        ["C000240", "P000014", "ORG000101", "Player", "2021", "2021"],
        ["C000241", "P000014", "ORG000090", "Player", "2024", "2025"],
        ["C000242", "P000070", "ORG000010", "Player", "", ""],
        ["C000243", "P000070", "ORG000015", "Player", "", ""],
        ["C000244", "P000070", "ORG000104", "Player", "2011", "2013"],
        ["C000245", "P000070", "ORG000054", "Player", "2013", "2014"],
        ["C000246", "P000070", "ORG000067", "Player", "2014", "2016"],
        ["C000247", "P000070", "ORG000052", "Player", "2016", "2018"],
        ["C000248", "P000070", "ORG000040", "Player", "2018", "2019"],
        ["C000249", "P000070", "ORG000102", "Player", "2019", "2020"],
        ["C000250", "P000070", "ORG000103", "Player", "2020", "2022"],
        ["C000251", "P000070", "ORG000103", "Head Coach", "2022", "2025"],
        ["C000252", "P000070", "ORG000067", "Assistant Coach", "2025", ""],
    ]
    write("career_candidates.csv", ["career_id", "person_id", "organization_id", "role", "start", "end"], careers)
    write("source_references.csv", ["source_id", "title", "publisher", "url", "accessed_at"], [
        ["B4W3S0001", "専大スポーツ第559号 2017年度期待のニューパワー", "専修大学", "https://www.senshu-u.ac.jp/albums/abm.php?d=2115&f=abm00003946.pdf&n=2017%E5%B9%B44%E6%9C%88%E5%8F%B7%EF%BC%88%E7%AC%AC559%E5%8F%B7%EF%BC%8911%E9%9D%A2.pdf", CHECKED],
        ["B4W3S0002", "重冨周希 B.LEAGUE公式選手プロフィール", "B.LEAGUE", "https://www.bleague.jp/roster_detail/?PlayerID=5100000076", CHECKED],
        ["B4W3S0003", "重冨友希 B.LEAGUE公式選手プロフィール", "B.LEAGUE", "https://www.bleague.jp/roster_detail/?PlayerID=40173", CHECKED],
        ["B4W3S0004", "重冨友希選手 2025-26シーズン契約合意（継続）", "山口パッツファイブ", "https://patsfive.com/shigetomi2526/", CHECKED],
        ["B4W3S0005", "キエキエ・トピー・アリ B.LEAGUE公式選手プロフィール", "B.LEAGUE", "https://www.bleague.jp/roster_detail/?PlayerID=36413", CHECKED],
        ["B4W3S0006", "キエキエ・トピー・アリ選手 2024-25シーズン契約合意", "横浜エクセレンス", "https://yokohama-ex.jp/team/pages/id=21831", CHECKED],
        ["B4W3S0007", "キエキエ・トピー・アリ選手 契約満了", "横浜エクセレンス", "https://yokohama-ex.jp/team/pages/id=22085", CHECKED],
        ["B4W3S0008", "遥天翼 B.LEAGUE公式選手プロフィール", "B.LEAGUE", "https://www.bleague.jp/roster_detail/?PlayerID=8642", CHECKED],
        ["B4W3S0009", "遥天翼氏 2025-26シーズン契約（新規）", "熊本ヴォルターズ", "https://www.volters.jp/news/detail/id=16536", CHECKED],
    ])

    e = []
    def ev(i, typ, entity, field, value, source, locator, summary, assessment="SUPPORTED", note=""):
        e.append([f"B4W3E{i:04d}", typ, entity, field, value, source, locator, summary, assessment, CHECKED, note])

    ev(1,"Person","P000068","name","重冨 周希","B4W3S0002","基本情報 > 選手名","B.LEAGUE公式の氏名")
    ev(2,"Person","P000068","name_en","Shuki Shigetomi","B4W3S0002","基本情報 > 英語表記","B.LEAGUE公式の英語表記")
    ev(3,"Person","P000068","birth_date","1998-06-09","B4W3S0002","基本情報 > 生年月日","生年月日を掲載")
    ev(4,"Person","P000068","height_cm","174","B4W3S0002","基本情報 > 身長","登録身長")
    ev(5,"Person","P000068","weight_kg","74","B4W3S0002","基本情報 > 体重","登録体重")
    ev(6,"Career","C000232","organization_id","ORG000010","B4W3S0001","PDF 11面 > バスケットボール部 > 重冨周希","出身高校を福岡第一高と掲載")
    ev(7,"Career","C000232","role","Player","B4W3S0001","PDF 11面 > 2017年度入部選手","バスケットボール部の入部者として掲載","PARTIAL","高校での役割を直接示す資料ではない")
    ev(8,"Career","C000233","organization_id","ORG000018","B4W3S0001","PDF 11面 > バスケットボール部","専修大学2017年度入部者として掲載")
    ev(9,"Career","C000233","role","Player","B4W3S0001","PDF 11面 > バスケットボール部","選手として入部者欄に掲載")
    ev(10,"Career","C000233","entry_year","2017","B4W3S0001","PDF見出し > 2017年度","2017年度入部")
    ev(11,"Career","C000234","organization_id","ORG000040","B4W3S0002","クラブ所属履歴","2021-22から2023-24福岡")
    ev(12,"Career","C000234","role","Player","B4W3S0002","選手プロフィール","B.LEAGUE選手として掲載")
    ev(13,"Career","C000234","seasons","2021-22|2022-23|2023-24","B4W3S0002","クラブ所属履歴","福岡所属シーズン")
    ev(14,"Career","C000234","competition_participation","2023-24 B2 53試合","B4W3S0002","シーズン成績","B2公式戦出場")
    ev(15,"Career","C000235","organization_id","ORG000050","B4W3S0002","クラブ所属履歴 > 2026-27湘南","ウォルガ湘南所属")
    ev(16,"Career","C000235","role","Player","B4W3S0002","2026-27選手プロフィール","登録選手として掲載")
    ev(17,"Person","P000069","name","重冨 友希","B4W3S0003","基本情報 > 選手名","B.LEAGUE公式の氏名")
    ev(18,"Person","P000069","name_en","Yuuki Shigetomi","B4W3S0003","基本情報 > 英語表記","B.LEAGUE公式の英語表記")
    ev(19,"Person","P000069","birth_date","1998-06-09","B4W3S0003","基本情報 > 生年月日","生年月日を掲載")
    ev(20,"Person","P000069","height_cm","174","B4W3S0003","基本情報 > 身長","登録身長")
    ev(21,"Person","P000069","weight_kg","75","B4W3S0003","基本情報 > 体重","登録体重")
    ev(22,"Career","C000236","organization_id","ORG000010","B4W3S0001","PDF 11面 > バスケットボール部 > 重冨友希","出身高校を福岡第一高と掲載")
    ev(23,"Career","C000236","role","Player","B4W3S0001","PDF 11面 > 2017年度入部選手","バスケットボール部の入部者として掲載","PARTIAL","高校での役割を直接示す資料ではない")
    ev(24,"Career","C000237","organization_id","ORG000018","B4W3S0001","PDF 11面 > バスケットボール部","専修大学2017年度入部者として掲載")
    ev(25,"Career","C000237","role","Player","B4W3S0001","PDF 11面 > バスケットボール部","選手として入部者欄に掲載")
    ev(26,"Career","C000237","entry_year","2017","B4W3S0001","PDF見出し > 2017年度","2017年度入部")
    ev(27,"Career","C000238","organization_id","ORG000040","B4W3S0004","プレイ歴","2021-22福岡、2022-23途中まで福岡")
    ev(28,"Career","C000238","role","Player","B4W3S0004","契約選手プロフィール","選手として掲載")
    ev(29,"Career","C000239","organization_id","ORG000100","B4W3S0004","プレイ歴","2022-23期限付き移籍、2023-25山口")
    ev(30,"Career","C000239","role","Player","B4W3S0004","契約合意発表","山口との選手契約")
    ev(31,"Career","C000239","contract_season","2025-26","B4W3S0004","発表見出し・本文","2025-26継続契約")
    ev(32,"Person","P000014","name","キエキエ トピー アリ","B4W3S0005","基本情報 > 選手名","中黒を除いた既存Person表記に対応")
    ev(33,"Person","P000014","name_en","Topy Ali Kiekie","B4W3S0005","基本情報 > 英語表記","B.LEAGUE公式の英語表記")
    ev(34,"Person","P000014","birth_date","2003-03-23","B4W3S0005","基本情報 > 生年月日","生年月日を掲載")
    ev(35,"Career","C000240","organization_id","ORG000101","B4W3S0006","経歴 > 2021.01-03鹿児島","高校在学中の鹿児島所属")
    ev(36,"Career","C000240","role","Player","B4W3S0005","2020-21鹿児島シーズン成績","B3公式戦18試合出場")
    ev(37,"Career","C000240","competition_participation","2020-21 B3 18試合369分24秒","B4W3S0005","シーズン成績","鹿児島での公式戦出場")
    ev(38,"Career","C000241","organization_id","ORG000090","B4W3S0006","契約合意本文","横浜EXとの契約")
    ev(39,"Career","C000241","role","Player","B4W3S0006","契約選手プロフィール","選手契約の対象")
    ev(40,"Career","C000241","contract_season","2024-25","B4W3S0006","発表見出し","2024-25契約")
    ev(41,"Career","C000241","competition_participation","2024-25 B3RS 4試合・B3PO 3試合","B4W3S0005","シーズン成績","横浜EXで公式戦出場")
    ev(42,"Career","C000241","contract_end_notice","2025-05-22","B4W3S0007","契約満了本文","自由交渉選手リスト公示日")
    ev(43,"Person","P000070","name","遥 天翼","B4W3S0008","基本情報 > 選手名","B.LEAGUE公式の氏名")
    ev(44,"Person","P000070","name_en","Tenyoku You","B4W3S0008","基本情報 > 英語表記","B.LEAGUE公式の英語表記")
    ev(45,"Person","P000070","birth_date","1988-10-06","B4W3S0008","基本情報 > 生年月日","生年月日を掲載")
    ev(46,"Person","P000070","birthplace_country","中国","B4W3S0009","プロフィール > 出身地","中華人民共和国出身、日本国籍と記載")
    ev(47,"Person","P000070","nationality","日本","B4W3S0009","プロフィール > 出身地","日本国籍と明記")
    ev(48,"Career","C000242","organization_id","ORG000010","B4W3S0009","経歴 > 福岡第一高校","高校経歴を掲載")
    ev(49,"Career","C000242","role","Player","B4W3S0009","経歴一覧","学校経歴のみで高校部の役割は直接記載なし","PARTIAL","高校バスケ部Playerの直接資料ではない")
    ev(50,"Career","C000243","organization_id","ORG000015","B4W3S0009","経歴 > 東海大学","大学経歴を掲載")
    ev(51,"Career","C000243","role","Player","B4W3S0009","プロ選手経歴前の大学欄","競技者経歴として掲載","PARTIAL","大学ロスターでの直接確認ではない")
    history = [
        (52,"C000244","ORG000104","2011-13 三菱電機ダイヤモンドドルフィンズ"),
        (54,"C000245","ORG000054","2013-14 三菱電機ダイヤモンドドルフィンズ名古屋"),
        (56,"C000246","ORG000067","2014-16 熊本ヴォルターズ"),
        (58,"C000247","ORG000052","2016-18 新潟アルビレックスBB"),
        (60,"C000248","ORG000040","2018-19 ライジングゼファー福岡"),
        (62,"C000249","ORG000102","2019-20 東京サンレーヴス"),
        (64,"C000250","ORG000103","2020-22 茨城ロボッツ"),
    ]
    for n,cid,oid,label in history:
        ev(n,"Career",cid,"organization_id",oid,"B4W3S0009",f"経歴 > {label}",label)
        ev(n+1,"Career",cid,"role","Player","B4W3S0009",f"選手経歴 > {label}","プロ選手経歴として掲載")
    ev(66,"Career","C000251","organization_id","ORG000103","B4W3S0009","経歴 > 2022-25 茨城U15","茨城ロボッツU15所属")
    ev(67,"Career","C000251","role","Head Coach","B4W3S0009","経歴 > U15ヘッドコーチ","2022-25 U15ヘッドコーチ")
    ev(68,"Career","C000252","organization_id","ORG000067","B4W3S0009","経歴 > 2025- 熊本","熊本ヴォルターズ所属")
    ev(69,"Career","C000252","role","Assistant Coach","B4W3S0009","発表見出し・経歴","2025-26アシスタントコーチ就任")
    for n,oid,name,src in [
        (70,"ORG000010","福岡第一高等学校","B4W3S0001"),(71,"ORG000015","東海大学","B4W3S0009"),
        (72,"ORG000018","専修大学","B4W3S0001"),(73,"ORG000040","ライジングゼファー福岡","B4W3S0002"),
        (74,"ORG000050","ウォルガ湘南","B4W3S0002"),(75,"ORG000052","新潟アルビレックスBB","B4W3S0009"),
        (76,"ORG000054","名古屋ダイヤモンドドルフィンズ","B4W3S0009"),(77,"ORG000067","熊本ヴォルターズ","B4W3S0009"),
        (78,"ORG000090","横浜エクセレンス","B4W3S0006"),(79,"ORG000100","山口パッツファイブ","B4W3S0004"),
        (80,"ORG000101","鹿児島レブナイズ","B4W3S0006"),(81,"ORG000102","東京サンレーヴス","B4W3S0009"),
        (82,"ORG000103","茨城ロボッツ","B4W3S0009"),(83,"ORG000104","三菱電機ダイヤモンドドルフィンズ","B4W3S0009"),
    ]:
        ev(n,"Organization",oid,"name",name,src,"資料内の組織名・経歴欄","公式資料の組織表記")
    write("evidence_records.csv", ["record_id","entity_type","entity_id","field_name","candidate_value","source_id","source_locator","evidence_summary","assessment","checked_at","issue_note"], e)

    write("issues.csv", ["issue_id","person_id","related_id","issue_type","status","description","next_check"], [
        ["B4W3I0001","P000068","C000232","HIGH_SCHOOL_ROLE_AND_PERIOD","HOLD","専修大学公式は福岡第一高出身を示すが、高校部での役割と期間は直接示さない","高校大会公式ロスターを確認"],
        ["B4W3I0002","P000068","C000233","UNIVERSITY_END","HOLD","2017年度入部は確認したが終了時期は未確認","卒業・退部等の公式資料を確認"],
        ["B4W3I0003","P000068","C000235","CLUB_HISTORY_GAP","HOLD","B.LEAGUEプロフィールに2024-25・2025-26湘南の履歴が表示されず、2026-27のみ確認","クラブ公式の年度別契約発表を確認"],
        ["B4W3I0004","P000069","C000236","HIGH_SCHOOL_ROLE_AND_PERIOD","HOLD","専修大学公式は福岡第一高出身を示すが、高校部での役割と期間は直接示さない","高校大会公式ロスターを確認"],
        ["B4W3I0005","P000069","C000237","UNIVERSITY_END","HOLD","2017年度入部は確認したが終了時期は未確認","卒業・退部等の公式資料を確認"],
        ["B4W3I0006","P000069","C000239","TRANSFER_BOUNDARY","HOLD","2022-23途中の期限付き移籍日は未確認","福岡・山口の移籍発表日を確認"],
        ["B4W3I0007","P000014","C000240","DATE_PRECISION","HOLD","経歴は2021.01-03とするが各日付は未確認","鹿児島公式の契約・満了発表を確認"],
        ["B4W3I0008","P000014","C000241","POST_2025_AFFILIATION","HOLD","2025年契約満了後の所属は未確認","現行リーグ・クラブ公式を確認"],
        ["B4W3I0009","P000070","C000242","HIGH_SCHOOL_ROLE_AND_PERIOD","HOLD","熊本公式経歴は学校名のみで高校部の役割と期間は直接示さない","高校大会公式資料を確認"],
        ["B4W3I0010","P000070","C000243","UNIVERSITY_ROLE_AND_PERIOD","HOLD","熊本公式経歴は大学名のみで大学部の役割と期間は直接示さない","大学大会公式資料を確認"],
        ["B4W3I0011","P000070","P000070","CLUB_SUCCESSION","HOLD","三菱電機ダイヤモンドドルフィンズと名古屋ダイヤモンドドルフィンズの組織承継関係は未整理","OrganizationAlias・継承ルールで別途整理"],
    ])

    decisions = []
    def dec(i, typ, eid, eligible, held, reason):
        decisions.append([f"B4W3D{i:04d}",typ,eid,"READY_FOR_VERIFIED_REVIEW",eligible,held,reason,CHECKED])
    dec(1,"Person","P000068","name|name_en|birth_date|height_cm|weight_kg","","B.LEAGUE公式で確認")
    dec(2,"Person","P000069","name|name_en|birth_date|height_cm|weight_kg","","B.LEAGUE公式で確認")
    dec(3,"Person","P000014","name|name_en|birth_date","","既存VERIFIEDとB.LEAGUE公式を再確認")
    dec(4,"Person","P000070","name|name_en|birth_date|birthplace_country|nationality","","B.LEAGUE・クラブ公式で確認")
    for i,(cid,eligible,held,reason) in enumerate([
        ("C000232","organization_id","role|start|end","出身高校のみ確認"),("C000233","organization_id|role|entry_year","end","専修大学公式入部資料"),
        ("C000234","organization_id|role|seasons|competition_participation","exact_start|exact_end","B.LEAGUE公式"),("C000235","organization_id|role","2024-25|2025-26|exact_start|end","B.LEAGUE公式の2026-27表示"),
        ("C000236","organization_id","role|start|end","出身高校のみ確認"),("C000237","organization_id|role|entry_year","end","専修大学公式入部資料"),
        ("C000238","organization_id|role","exact_start|exact_end","山口公式プレイ歴"),("C000239","organization_id|role|contract_season","transfer_date|end","山口公式契約発表"),
        ("C000240","organization_id|role|competition_participation","exact_start|exact_end","B.LEAGUE・横浜EX公式"),("C000241","organization_id|role|contract_season|competition_participation|contract_end_notice","exact_start|exact_end","横浜EX・B.LEAGUE公式"),
        ("C000242","organization_id","role|start|end","熊本公式経歴"),("C000243","organization_id","role|start|end","熊本公式経歴"),
        ("C000244","organization_id|role","exact_dates","熊本公式経歴"),("C000245","organization_id|role","exact_dates","熊本公式経歴"),
        ("C000246","organization_id|role","exact_dates","熊本公式経歴"),("C000247","organization_id|role","exact_dates","熊本公式経歴"),
        ("C000248","organization_id|role","exact_dates","熊本公式経歴"),("C000249","organization_id|role","exact_dates","熊本公式経歴"),
        ("C000250","organization_id|role","exact_dates","熊本公式経歴"),("C000251","organization_id|role","exact_dates","熊本公式経歴"),
        ("C000252","organization_id|role","end","熊本公式加入発表"),
    ], start=5): dec(i,"Career",cid,eligible,held,reason)
    for j,oid in enumerate(["ORG000010","ORG000015","ORG000018","ORG000040","ORG000050","ORG000052","ORG000054","ORG000067","ORG000090","ORG000100","ORG000101","ORG000102","ORG000103","ORG000104"], start=26):
        dec(j,"Organization",oid,"name","","公式資料内表記を確認")
    write("qa_decisions.csv", ["decision_id","entity_type","entity_id","decision","eligible_fields","held_fields","reason","reviewed_at"], decisions)


if __name__ == "__main__":
    main()
