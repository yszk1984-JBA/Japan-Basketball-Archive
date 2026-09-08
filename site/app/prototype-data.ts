export const sources = [
  { id:'SRC000010', title:'福岡県代表 男子 福岡第一高等学校 — 選手名鑑 2020', publisher:'J SPORTS', url:'https://www.jsports.co.jp/basketball/wintercup/players_2020/m_fukuoka/' },
  { id:'SRC000012', title:'ウインターカップ2020出場選手の進路一覧 〜九州〜', publisher:'月刊バスケットボールWEB', url:'https://www.basketball-zine.com/article/detail/69646' },
  { id:'SRC000013', title:'福岡第一 vs 県立四日市工業 公式ボックススコア', publisher:'日本バスケットボール協会（JBA）', url:'https://wintercup2020.japanbasketball.jp/boxscore/?period=18&schedulekey=6898' },
] as const;

export const players = [
  { id:'P000010', slug:'shugo-toyama', name:'當山 修梧', reading:'Shugo Toyama', jerseyNumber:'1', position:'PG', role:'選手', nextStep:'専修大学', sourceIds:['SRC000010','SRC000012','SRC000013'] },
  { id:'P000011', slug:'ryuyu-sunakawa', name:'砂川 琉勇', reading:'Ryuyu Sunakawa', jerseyNumber:'23', position:'SG', role:'選手', nextStep:'明星大学', sourceIds:['SRC000010','SRC000012','SRC000013'] },
  { id:'P000012', slug:'john-lawrence-harper-jr', name:'ハーパー ジャン ローレンス ジュニア', reading:'John Lawrence Harper Jr.', jerseyNumber:'31', position:'PG', role:'選手', nextStep:'東海大学', sourceIds:['SRC000010','SRC000012','SRC000013'] },
] as const;

export function getPlayer(slug: string) { return players.find((player) => player.slug === slug); }
export function getSources(ids: readonly string[]) { return sources.filter((source) => ids.includes(source.id)); }
