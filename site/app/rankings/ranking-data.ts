import { CLUB_COLORS } from '../club-colors';
import { organizationCategory } from '../organization-category';
import {
  getOrganizationById,
  getPrimaryCareer,
  masterApprovals,
  masterPublication,
  organizationSlugFor,
  players,
} from '../public-data';

// 出身校ランキングの集計。
// - 対象はMaster Dataの選手と、Master承認済みのCareerだけ（Candidateは含めない）。
// - 「現役」は、現在（直近）の所属が現行のB.PREMIER・B.ONEの51クラブ（club-colors.ts）である選手。
// - 学校の区分（高校・大学）は組織名からの自動判定（organization-category.ts）を使う。
// - 改称・統合した学校は資料に書かれた当時の名称で数え、現在の名称（Masterの付随データ）を併記する。
//   組織データ上で別の組織として登録されていれば別々に数える。
export type RankingKind = 'high-school' | 'university' | 'premier-high-school';

export type RankingRow = {
  readonly rank: number;
  readonly organizationId: string;
  readonly slug: string | undefined;
  readonly name: string;
  // 改称・統合した学校の現在の名称（例：「現：仙台大学附属明成高等学校」）。
  readonly currentNameNote?: string;
  // 現在B.PREMIER・B.ONEのクラブに所属している出身者の数（並び順の基準）。
  readonly active: number;
  // 本サイトに登録されている出身者の延べ人数（引退者・B3以下・海外などを含む）。
  readonly total: number;
  // 現役の出身者（選手名・選手ページ・現所属クラブ）。リーグ別ランキングで学校ごとに並べる。
  readonly activePlayers: readonly { readonly name: string; readonly slug: string; readonly club: string }[];
};

export const RANKING_META: Record<
  RankingKind,
  {
    readonly category: 'hs' | 'univ';
    readonly label: string;
    readonly path: string;
    // 指定があれば、そのリーグのクラブに今所属している選手だけを「現役」として数える。
    readonly league?: 'PREMIER' | 'B.ONE';
  }
> = {
  'high-school': { category: 'hs', label: '高校', path: '/rankings/high-school' },
  university: { category: 'univ', label: '大学', path: '/rankings/university' },
  'premier-high-school': { category: 'hs', label: '高校', path: '/rankings/premier-high-school', league: 'PREMIER' },
};

function isActiveTopLeaguePlayer(player: (typeof players)[number], league?: 'PREMIER' | 'B.ONE'): boolean {
  const organizationId = getPrimaryCareer(player)?.organizationId;
  const club = organizationId ? CLUB_COLORS[organizationId] : undefined;
  return Boolean(club && (!league || club.league === league));
}

function currentNameNote(organizationId: string): string | undefined {
  const current = getOrganizationById(organizationId)?.currentName;
  return current ? `${current.label}：${current.currentName}` : undefined;
}

export function buildRanking(kind: RankingKind): RankingRow[] {
  const { category, league } = RANKING_META[kind];
  const byOrganization = new Map<string, { name: string; total: Set<string>; active: Set<string> }>();
  const playerById = new Map(players.map((player) => [player.id, player]));

  for (const player of players) {
    if (player.dataStatus !== 'master') continue;
    const active = isActiveTopLeaguePlayer(player, league);
    for (const career of player.careers) {
      if (career.status !== 'master' || !career.organizationId || !career.organization) continue;
      if (organizationCategory(career.organization) !== category) continue;
      const entry = byOrganization.get(career.organizationId) ?? {
        name: career.organization,
        total: new Set<string>(),
        active: new Set<string>(),
      };
      entry.total.add(player.id);
      if (active) entry.active.add(player.id);
      byOrganization.set(career.organizationId, entry);
    }
  }

  const sorted = [...byOrganization.entries()]
    .map(([organizationId, entry]) => ({
      organizationId,
      slug: organizationSlugFor(organizationId),
      name: entry.name,
      currentNameNote: currentNameNote(organizationId),
      active: entry.active.size,
      total: entry.total.size,
      activePlayers: [...entry.active]
        .map((id) => playerById.get(id))
        .filter((player): player is (typeof players)[number] => Boolean(player))
        .map((player) => ({ name: player.name, slug: player.slug, club: getPrimaryCareer(player)?.organization ?? '' }))
        .sort((left, right) => left.club.localeCompare(right.club, 'ja') || left.name.localeCompare(right.name, 'ja')),
    }))
    .filter((row) => row.active > 0)
    .sort(
      (left, right) =>
        right.active - left.active || right.total - left.total || left.name.localeCompare(right.name, 'ja'),
    );

  // 現役人数が同じ学校は同順位（1, 2, 2, 4…）にする。
  let previousActive = -1;
  let previousRank = 0;
  return sorted.map((row, index) => {
    const rank = row.active === previousActive ? previousRank : index + 1;
    previousActive = row.active;
    previousRank = rank;
    return { ...row, rank };
  });
}

// 集計に使ったMaster Dataの最終承認日。
export function rankingAsOf(): string {
  const dates = Object.values(masterApprovals as Record<string, { approvedAt: string }>).map(
    (approval) => approval.approvedAt,
  );
  return dates.reduce((latest, date) => (date > latest ? date : latest), masterPublication.approvedAt);
}

export function activeTopLeaguePlayerCount(league?: 'PREMIER' | 'B.ONE'): number {
  return players.filter((player) => player.dataStatus === 'master' && isActiveTopLeaguePlayer(player, league)).length;
}
