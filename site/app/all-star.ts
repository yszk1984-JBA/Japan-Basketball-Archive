// りそなグループ B.LEAGUE ALL-STAR GAME 2026（2026年1月16日〜18日・長崎県HAPPINESS ARENA、
// 2025-26シーズン）出場選手のうち、当サイトに掲載済みの選手を、トップページの特集表示用に
// 保持する表示専用データ。
//
// 注意：
// - 出典：goal.com「B-League All-Star 2026 players」
//   https://www.goal.com/jp/%E3%83%8B%E3%83%A5%E3%83%BC%E3%82%B9/b-league-all-star-2026-players/blt6f0cfaf502862228
//   （B.LEAGUE公式発表に基づく報道記事。team表記は記事に合わせて「B.BLACK」「B.WHITE」とした）。
// - 出場選手26名のうち、外国籍選手6名（アイザック・フォトゥ、クリストファー・スミス、
//   セバスチャン・サイズ、ジョシュ・ホーキンソン、ザック・オーガスト、ヴィック・ロー）は
//   当サイトの収録対象（日本人選手の高校・大学からプロへの経歴を中心に掲載）に含まれて
//   いないため、今回のリストから除外している。
// - これは選手の経歴（Career）に「オールスター出場」という事実を追加するものではなく、
//   トップページ表示専用のキュレーションである。Master/Candidateのデータスキーマ
//   （Person/Career/Organization）には一切変更を加えていない。
export type AllStarTeam = 'B.BLACK' | 'B.WHITE';

export type AllStarEntry = {
  readonly playerId: string;
  readonly team: AllStarTeam;
  readonly captain?: true;
};

export const ALL_STAR_2026: {
  readonly label: string;
  readonly period: string;
  readonly venue: string;
  readonly sourceLabel: string;
  readonly sourceUrl: string;
  readonly entries: readonly AllStarEntry[];
} = {
  label: 'りそなグループ B.LEAGUE ALL-STAR GAME 2026',
  period: '2026年1月16日〜18日',
  venue: '長崎県 HAPPINESS ARENA',
  sourceLabel: 'goal.com',
  sourceUrl:
    'https://www.goal.com/jp/%E3%83%8B%E3%83%A5%E3%83%BC%E3%82%B9/b-league-all-star-2026-players/blt6f0cfaf502862228',
  entries: [
    { playerId: 'P000084', team: 'B.BLACK', captain: true }, // 比江島慎
    { playerId: 'P000176', team: 'B.BLACK' }, // 篠山竜青
    { playerId: 'P000311', team: 'B.BLACK' }, // 吉井裕鷹
    { playerId: 'P000106', team: 'B.BLACK' }, // 富永啓生
    { playerId: 'P000097', team: 'B.BLACK' }, // 辻直人
    { playerId: 'P000373', team: 'B.BLACK' }, // 黒川虎徹
    { playerId: 'P000098', team: 'B.BLACK' }, // 安藤誓哉
    { playerId: 'P000357', team: 'B.BLACK' }, // 今村佳太
    { playerId: 'P000096', team: 'B.BLACK' }, // 竹内譲次
    { playerId: 'P000289', team: 'B.BLACK' }, // ギャビン・エドワーズ

    { playerId: 'P000083', team: 'B.WHITE', captain: true }, // 富樫勇樹
    { playerId: 'P000088', team: 'B.WHITE' }, // 岸本隆一
    { playerId: 'P000103', team: 'B.WHITE' }, // 渡邊雄太
    { playerId: 'P000089', team: 'B.WHITE' }, // 西田優大
    { playerId: 'P000158', team: 'B.WHITE' }, // 瀬川琉久
    { playerId: 'P000087', team: 'B.WHITE' }, // 田中大貴
    { playerId: 'P000161', team: 'B.WHITE' }, // 岡田侑大
    { playerId: 'P000090', team: 'B.WHITE' }, // 金丸晃輔
    { playerId: 'P000107', team: 'B.WHITE' }, // 馬場雄大
    { playerId: 'P000277', team: 'B.WHITE' }, // 川真田紘也
  ],
};
