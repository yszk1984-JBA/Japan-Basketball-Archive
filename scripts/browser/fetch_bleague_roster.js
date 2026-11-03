// B.LEAGUE公式の選手一覧（日本国籍・在籍中）を全クラブ分取得し、TSVの文字列を返す。
// 使い方：Claudeのブラウザで https://www.bleague.jp/roster/?tab=1&year=2026 を開き、
// このファイルの中身を javascript_tool でそのまま実行する。結果は window.__tsv にも入る。
// TAB：1=B.PREMIER、2=B.ONE、3=B.NEXT。YEAR：シーズン開始年。
// 返り値の各行：tab<TAB>TeamID<TAB>PlayerID<TAB>一覧上の氏名
// 保存先：data/raw/research/bleague_roster_premier_<取得日>.tsv（先頭に # のヘッダー2行。前回のファイルを参照）
const TAB = 1, YEAR = 2026;
const clubs = [...document.querySelectorAll('select[name=club] option')].filter(o => o.value).map(o => [o.value, o.textContent.trim()]);
const rows = [], counts = [];
for (const [id, abbr] of clubs) {
  const url = `/roster/?tab=${TAB}&year=${YEAR}&club=${id}&c=${encodeURIComponent('日本')}&e=${encodeURIComponent('在籍中')}&o=sort`;
  const html = await fetch(url).then(r => r.text());
  const doc = new DOMParser().parseFromString(html, 'text/html');
  const seen = new Set();
  for (const a of doc.querySelectorAll('a[href*="PlayerID="]')) {
    const pid = a.href.match(/PlayerID=(\d+)/)[1];
    if (seen.has(pid)) continue;
    seen.add(pid);
    rows.push([TAB, id, pid, a.textContent.trim().split('\n')[0].trim()].join('\t'));
  }
  counts.push(`${abbr}:${seen.size}`);
}
window.__tsv = rows.join('\n');
({ clubs: clubs.length, players: rows.length, counts: counts.join(' ') });
