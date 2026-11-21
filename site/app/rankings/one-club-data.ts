import { getOrganizationById, getPrimaryCareer, organizationSlugFor, players } from '../public-data';
import { organizationKind } from '../seo';

// 「B.LEAGUE開幕から同じクラブ一筋」の選手の抽出。
// - 対象はMaster Dataの選手と、Master承認済みのCareerだけ（Candidateは含めない）。
// - 条件：直近の所属がクラブで、所属の開始が2016年（2016-17シーズン、B.LEAGUE開幕）以前、
//   終了年が記録されていない（現在も所属）。かつ、2016年より後に終わる別クラブの所属
//   （期限付き移籍を含む）が記録されていないこと。
// - 本サイトのクラブ所属の記録は、主にB.LEAGUE公式の所属履歴（2016-17以降）による。
//   それ以前の所属は網羅していないため、「B.LEAGUE開幕から」に限った表現にする（「生え抜き」とは書かない）。
// - 改称したクラブ（公式TeamIDが同じ）は1つの組織として扱う（データ側の方針どおり）。

export const ONE_CLUB_PATH = '/rankings/one-club';
export const ONE_CLUB_TITLE = 'B.LEAGUE開幕から同じクラブ一筋の選手';
export const BLEAGUE_START_YEAR = 2016;

export type OneClubPlayer = { readonly id: string; readonly name: string; readonly slug: string };
export type OneClubRow = {
  readonly rank: number;
  readonly clubId: string;
  readonly clubName: string;
  readonly clubSlug: string | undefined;
  readonly players: readonly OneClubPlayer[];
};

function isClub(organizationId: string | undefined): boolean {
  const organization = organizationId ? getOrganizationById(organizationId) : undefined;
  return Boolean(organization && organizationKind(organization) === 'club');
}

let cache: OneClubRow[] | undefined;

export function buildOneClubRanking(): OneClubRow[] {
  if (cache) return cache;
  const byClub = new Map<string, { name: string; players: OneClubPlayer[] }>();
  for (const player of players) {
    if (player.dataStatus !== 'master') continue;
    const primary = getPrimaryCareer(player);
    if (!primary?.organizationId || !primary.organization || primary.status !== 'master') continue;
    if (primary.endYear != null || primary.startYear == null || primary.startYear > BLEAGUE_START_YEAR) continue;
    if (!isClub(primary.organizationId)) continue;
    const movedDuringBleague = player.careers.some(
      (career) =>
        career.organizationId !== primary.organizationId &&
        isClub(career.organizationId) &&
        (career.endYear == null || career.endYear > BLEAGUE_START_YEAR),
    );
    if (movedDuringBleague) continue;
    const entry = byClub.get(primary.organizationId) ?? { name: primary.organization, players: [] };
    entry.players.push({ id: player.id, name: player.name, slug: player.slug });
    byClub.set(primary.organizationId, entry);
  }
  const sorted = [...byClub.entries()]
    .map(([clubId, entry]) => ({
      clubId,
      clubName: entry.name,
      clubSlug: organizationSlugFor(clubId),
      players: [...entry.players].sort((left, right) => left.name.localeCompare(right.name, 'ja')),
    }))
    .sort(
      (left, right) =>
        right.players.length - left.players.length || left.clubName.localeCompare(right.clubName, 'ja'),
    );
  let previousCount = -1;
  let previousRank = 0;
  cache = sorted.map((row, index) => {
    const rank = row.players.length === previousCount ? previousRank : index + 1;
    previousCount = row.players.length;
    previousRank = rank;
    return { ...row, rank };
  });
  return cache;
}

export function oneClubPlayerCount(): number {
  return buildOneClubRanking().reduce((sum, row) => sum + row.players.length, 0);
}
