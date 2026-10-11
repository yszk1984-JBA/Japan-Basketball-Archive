// 組織ページで使う「選手を介した組織どうしの関係」。
// クラブページ：所属選手の出身校（高校・大学）と、その内訳。
// 学校ページ：在籍した選手の進路（直近の所属クラブ）と、その内訳。
// どちらも登録済みの経歴（Career）から機械的に集計するだけで、新しい事実は作らない。
import {
  getOrganizationById,
  getOrganizationPlayers,
  getPrimaryCareer,
  organizationDisplayName,
  type PublicOrganization,
  type PublicPlayer,
} from './public-data';
import { organizationKind, type OrganizationKind } from './seo';

const SCHOOL_KINDS: ReadonlySet<OrganizationKind> = new Set(['highSchool', 'university', 'school']);

export function isSchoolOrganization(organization: PublicOrganization): boolean {
  return SCHOOL_KINDS.has(organizationKind(organization));
}

// 選手の出身校（学校として判定できる組織）。経歴の並び順（時系列）を保ち、同じ学校は1回だけ。
export function schoolsOf(player: PublicPlayer): PublicOrganization[] {
  const seen = new Set<string>();
  const schools: PublicOrganization[] = [];
  for (const career of player.careers) {
    if (!career.organizationId || seen.has(career.organizationId)) continue;
    const organization = getOrganizationById(career.organizationId);
    if (organization && isSchoolOrganization(organization)) {
      seen.add(organization.id);
      schools.push(organization);
    }
  }
  return schools;
}

// 選手の直近の所属（学校以外）。選手ページのtitle・ランキングと同じgetPrimaryCareerの判定を使う
// （期間未確認のクラブは「開始年が未確認の現在の所属」とみなす、データ生成時の方針に合わせる）。
// 直近の経歴が学校のとき（候補人物など）は、学校以外の最後の経歴を使う。
export function latestClubOf(player: PublicPlayer): PublicOrganization | undefined {
  const primary = getPrimaryCareer(player);
  const primaryOrganization = primary?.organizationId ? getOrganizationById(primary.organizationId) : undefined;
  if (primaryOrganization && !isSchoolOrganization(primaryOrganization)) return primaryOrganization;
  for (const career of [...player.careers].reverse()) {
    const organization = career.organizationId ? getOrganizationById(career.organizationId) : undefined;
    if (organization && !isSchoolOrganization(organization)) return organization;
  }
  return undefined;
}

export type OrganizationCount = { readonly organization: PublicOrganization; readonly count: number };

function countOrganizations(lists: readonly PublicOrganization[][]): OrganizationCount[] {
  const counts = new Map<string, OrganizationCount>();
  for (const list of lists) {
    for (const organization of list) {
      const previous = counts.get(organization.id);
      counts.set(organization.id, { organization, count: (previous?.count ?? 0) + 1 });
    }
  }
  return [...counts.values()].sort(
    (left, right) => right.count - left.count || left.organization.name.localeCompare(right.organization.name, 'ja'),
  );
}

// クラブの所属選手の出身校を、高校と大学（その他の学校を含む）に分けて人数の多い順に並べる。
export function schoolBreakdown(players: readonly PublicPlayer[], excludeId: string) {
  const perPlayer = players.map((player) => schoolsOf(player).filter((school) => school.id !== excludeId));
  const all = countOrganizations(perPlayer);
  return {
    highSchools: all.filter(({ organization }) => organizationKind(organization) === 'highSchool'),
    universities: all.filter(({ organization }) => organizationKind(organization) !== 'highSchool'),
    playersWithSchool: perPlayer.filter((list) => list.length > 0).length,
  };
}

// 学校に在籍した選手の、直近の所属クラブを人数の多い順に並べる。
export function clubBreakdown(players: readonly PublicPlayer[]) {
  const perPlayer = players.map((player) => {
    const club = latestClubOf(player);
    return club ? [club] : [];
  });
  return { clubs: countOrganizations(perPlayer), playersWithClub: perPlayer.filter((list) => list.length > 0).length };
}

// 「福岡第一高等学校、日本体育大学」のような表示用の文字列。
export function organizationNames(organizations: readonly PublicOrganization[]): string {
  return organizations.map((organization) => organizationDisplayName(organization)).join('、');
}

// 同じ学校に在籍記録のある他の選手（選手ページの「同じ出身校の選手」に使う）。
// 並び順：承認済み（Master）を先に、その中で世代の近い順。世代は、この学校での在籍開始年が双方に
// あればその差、無ければ生年の差で比べる（高校の在籍年は未確認のことが多いため）。どちらも分からない
// 選手は後ろ、最後に名前順。
function birthYearOf(player: PublicPlayer): number | null {
  const value = player.facts.find((fact) => fact.label === '生年月日')?.value;
  const match = value?.match(/(\d{4})年/);
  return match ? Number(match[1]) : null;
}

export function schoolmatesOf(player: PublicPlayer, school: PublicOrganization) {
  const startAt = (target: PublicPlayer) =>
    target.careers.find((career) => career.organizationId === school.id && career.startYear != null)?.startYear ?? null;
  const ownStart = startAt(player);
  const ownBirth = birthYearOf(player);
  const distance = (target: PublicPlayer) => {
    const start = startAt(target);
    if (ownStart != null && start != null) return Math.abs(start - ownStart);
    const birth = birthYearOf(target);
    if (ownBirth != null && birth != null) return Math.abs(birth - ownBirth);
    return Number.POSITIVE_INFINITY;
  };
  return getOrganizationPlayers(school.id)
    .filter((other) => other.id !== player.id)
    .sort(
      (left, right) =>
        Number(right.dataStatus === 'master') - Number(left.dataStatus === 'master') ||
        distance(left) - distance(right) ||
        left.name.localeCompare(right.name, 'ja'),
    );
}
