import { organizationCategory } from '../organization-category';
import { getOrganizationById, organizationSlugFor, players } from '../public-data';

// 高校→大学の進学ルート（組み合わせ）の集計。
// - 対象はMaster Dataの選手と、Master承認済みのCareerだけ（Candidateは含めない）。
// - 高校・大学の区分は組織名からの自動判定（organization-category.ts）。
// - 1人の選手に高校・大学が複数ある場合（転校など）は、その組み合わせをすべて1回ずつ数える。
// - 在籍の前後関係（高校の後に大学）は資料で確認していない。「高校と大学の両方の在籍記録がある」組み合わせとして数える。
// - 改称・統合した学校は資料に書かれた当時の名称で数える（出身校ランキングと同じ扱い）。

export const ROUTE_PATH = '/rankings/high-school-to-university';
export const ROUTE_TITLE = 'B.LEAGUE選手の「高校→大学」進学ルートランキング';
// 掲載する最少人数（1人だけの組み合わせは件数が多く、ランキングとしての意味が薄いため一覧に載せない）。
export const ROUTE_MIN_PLAYERS = 2;

export type RouteSchool = { readonly id: string; readonly name: string; readonly slug: string | undefined; readonly currentNameNote?: string };
export type RoutePlayer = { readonly id: string; readonly name: string; readonly slug: string };
export type RouteRow = {
  readonly rank: number;
  readonly highSchool: RouteSchool;
  readonly university: RouteSchool;
  readonly players: readonly RoutePlayer[];
};

function school(id: string, name: string): RouteSchool {
  const current = getOrganizationById(id)?.currentName;
  return {
    id,
    name,
    slug: organizationSlugFor(id),
    ...(current ? { currentNameNote: `${current.label}：${current.currentName}` } : {}),
  };
}

function schoolsOf(player: (typeof players)[number], category: 'hs' | 'univ'): RouteSchool[] {
  const seen = new Map<string, RouteSchool>();
  for (const career of player.careers) {
    if (career.status !== 'master' || !career.organizationId || !career.organization) continue;
    if (organizationCategory(career.organization) !== category) continue;
    if (!seen.has(career.organizationId)) seen.set(career.organizationId, school(career.organizationId, career.organization));
  }
  return [...seen.values()];
}

type Aggregate = {
  readonly pairs: Map<string, { highSchool: RouteSchool; university: RouteSchool; players: RoutePlayer[] }>;
  readonly playersWithRoute: number;
};

let cache: Aggregate | undefined;

function aggregate(): Aggregate {
  if (cache) return cache;
  const pairs: Aggregate['pairs'] = new Map();
  let playersWithRoute = 0;
  for (const player of players) {
    if (player.dataStatus !== 'master') continue;
    const highSchools = schoolsOf(player, 'hs');
    const universities = schoolsOf(player, 'univ');
    if (!highSchools.length || !universities.length) continue;
    playersWithRoute += 1;
    for (const highSchool of highSchools) {
      for (const university of universities) {
        const key = `${highSchool.id}>${university.id}`;
        const entry = pairs.get(key) ?? { highSchool, university, players: [] };
        entry.players.push({ id: player.id, name: player.name, slug: player.slug });
        pairs.set(key, entry);
      }
    }
  }
  cache = { pairs, playersWithRoute };
  return cache;
}

export function buildRouteRanking(): RouteRow[] {
  const sorted = [...aggregate().pairs.values()]
    .filter((entry) => entry.players.length >= ROUTE_MIN_PLAYERS)
    .sort(
      (left, right) =>
        right.players.length - left.players.length ||
        left.highSchool.name.localeCompare(right.highSchool.name, 'ja') ||
        left.university.name.localeCompare(right.university.name, 'ja'),
    );
  // 人数が同じ組み合わせは同順位（1, 2, 2, 4…）にする。
  let previousCount = -1;
  let previousRank = 0;
  return sorted.map((entry, index) => {
    const rank = entry.players.length === previousCount ? previousRank : index + 1;
    previousCount = entry.players.length;
    previousRank = rank;
    return { rank, highSchool: entry.highSchool, university: entry.university, players: entry.players };
  });
}

// 高校と大学の両方の在籍記録がある選手の数（集計の母集団）。
export function routePopulation(): number {
  return aggregate().playersWithRoute;
}

export type Spread = { readonly school: RouteSchool; readonly destinations: number; readonly players: number };

// 注目ポイント：進学先（または出身高校）の数が多い学校。母集団が小さい学校を除くため、選手minPlayers人以上の学校に限る。
export function mostSpread(from: 'hs' | 'univ', minPlayers = 5): Spread | undefined {
  const bySchool = new Map<string, { school: RouteSchool; others: Set<string>; players: Set<string> }>();
  for (const entry of aggregate().pairs.values()) {
    const own = from === 'hs' ? entry.highSchool : entry.university;
    const other = from === 'hs' ? entry.university : entry.highSchool;
    const item = bySchool.get(own.id) ?? { school: own, others: new Set<string>(), players: new Set<string>() };
    item.others.add(other.id);
    for (const player of entry.players) item.players.add(player.id);
    bySchool.set(own.id, item);
  }
  return [...bySchool.values()]
    .filter((item) => item.players.size >= minPlayers)
    .map((item) => ({ school: item.school, destinations: item.others.size, players: item.players.size }))
    .sort((left, right) => right.destinations - left.destinations || right.players - left.players)[0];
}
