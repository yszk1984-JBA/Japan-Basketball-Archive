import {
  getCurrentCareer,
  getOrganizationById,
  organizationDisplayName,
  players,
  type PublicPlayer,
} from '../public-data';
import { organizationCategory } from '../organization-category';
import { rankingAsOf } from './ranking-data';

// Master Dataだけから集計する追加ランキング（2026-11）。
// - 共通の型（ExtraRanking）にそろえ、ページ・一覧・サイトマップは EXTRA_RANKING_IDS を順に回して作る。
// - 「注目ポイント」はデータから自動で作る文章だけにし、推測や評価（「名門」「最強」など）は書かない。
// - 網羅していると誤解されないよう、どのページも「本サイトに登録済みの選手のみ」と明記する。

export type RankingLink = { readonly label: string; readonly href?: string };
export type ExtraRankingRow = {
  readonly key: string;
  readonly rank: number;
  readonly name: RankingLink;
  readonly sub?: RankingLink;
  readonly count: number;
  readonly unit: string;
  readonly items: readonly RankingLink[];
};
export type ExtraRanking = {
  readonly id: ExtraRankingId;
  readonly path: string;
  readonly title: string;
  readonly crumb: string;
  readonly description: string;
  readonly lede: string;
  readonly share: string;
  readonly headers: { readonly name: string; readonly count: string; readonly items: string };
  readonly points: readonly string[];
  readonly notes: readonly string[];
  readonly rows: readonly ExtraRankingRow[];
  readonly indexSummary: string;
};

export const EXTRA_RANKING_IDS = [
  'club-high-school-alumni',
  'high-school-to-pro',
  'generation',
  'oldest-active',
  'most-clubs',
] as const;
export type ExtraRankingId = (typeof EXTRA_RANKING_IDS)[number];

export const EXTRA_RANKING_PATHS: Record<ExtraRankingId, string> = {
  'club-high-school-alumni': '/rankings/club-high-school-alumni',
  'high-school-to-pro': '/rankings/high-school-to-pro',
  generation: '/rankings/generation',
  'oldest-active': '/rankings/oldest-active',
  'most-clubs': '/rankings/most-clubs',
};

const BLEAGUE_START_YEAR = 2016;
const COMMON_NOTE =
  '本サイトに登録済み（確認済みのデータ）の選手だけを数えています。登録されていない選手は含まれないため、実際の人数より少ない場合があります。';

type Career = PublicPlayer['careers'][number];

const masterPlayers = () => players.filter((player) => player.dataStatus === 'master');
const masterCareers = (player: PublicPlayer) => player.careers.filter((career) => career.status === 'master');
const categoryOf = (career: Career) => (career.organization ? organizationCategory(career.organization) : 'other');
const isClubCareer = (career: Career) => categoryOf(career) === 'club';

function orgLink(organizationId: string | undefined, fallback: string): RankingLink {
  const organization = organizationId ? getOrganizationById(organizationId) : undefined;
  return organization
    ? { label: organizationDisplayName(organization), href: `/organizations/${organization.slug}` }
    : { label: fallback };
}

function playerLink(player: PublicPlayer, suffix = ''): RankingLink {
  return { label: `${player.name}${suffix}`, href: `/players/${player.slug}` };
}

// 現在の所属クラブ（終了年のないクラブの経歴）。学校・クラブ以外（海外クラブ等の「その他」）は対象外。
function currentClub(player: PublicPlayer): Career | undefined {
  const career = getCurrentCareer(player);
  return career && career.status === 'master' && isClubCareer(career) ? career : undefined;
}

function birthDate(player: PublicPlayer): { year: number; month: number; day: number } | undefined {
  const value = player.facts.find((fact) => fact.label === '生年月日')?.value;
  const match = value?.match(/(\d{4})年(\d{1,2})月(\d{1,2})日/);
  return match ? { year: Number(match[1]), month: Number(match[2]), day: Number(match[3]) } : undefined;
}

// 学年（日本の学校年度：4月2日〜翌年4月1日生まれが同じ学年）。
function schoolYearOf(date: { year: number; month: number; day: number }): number {
  return date.month < 4 || (date.month === 4 && date.day === 1) ? date.year - 1 : date.year;
}

function ageOn(date: { year: number; month: number; day: number }, isoDate: string): number {
  const [year, month, day] = isoDate.slice(0, 10).split('-').map(Number);
  const hadBirthday = month > date.month || (month === date.month && day >= date.day);
  return year - date.year - (hadBirthday ? 0 : 1);
}

// 人数の多い順に並べ、同じ人数は同順位にする。
function withRanks<T extends { count: number }>(rows: T[]): (T & { rank: number })[] {
  let previousCount = Number.NaN;
  let previousRank = 0;
  return rows.map((row, index) => {
    const rank = row.count === previousCount ? previousRank : index + 1;
    previousCount = row.count;
    previousRank = rank;
    return { ...row, rank };
  });
}

const byName = (left: PublicPlayer, right: PublicPlayer) => left.name.localeCompare(right.name, 'ja');

// 1. 同じ高校出身の選手が多いクラブ（現在の所属）
function clubHighSchoolAlumni(): ExtraRanking {
  const groups = new Map<string, { club: Career; school: Career; players: PublicPlayer[] }>();
  for (const player of masterPlayers()) {
    const club = currentClub(player);
    if (!club?.organizationId) continue;
    const seen = new Set<string>();
    for (const school of masterCareers(player)) {
      if (categoryOf(school) !== 'hs' || !school.organizationId || seen.has(school.organizationId)) continue;
      seen.add(school.organizationId);
      const key = `${club.organizationId}|${school.organizationId}`;
      const group = groups.get(key) ?? { club, school, players: [] };
      group.players.push(player);
      groups.set(key, group);
    }
  }
  const rows = withRanks(
    [...groups.entries()]
      .filter(([, group]) => group.players.length >= 2)
      .map(([key, group]) => ({
        key,
        name: orgLink(group.club.organizationId, group.club.organization ?? ''),
        sub: orgLink(group.school.organizationId, group.school.organization ?? ''),
        count: group.players.length,
        unit: '人',
        items: [...group.players].sort(byName).map((player) => playerLink(player)),
      }))
      .sort((left, right) => right.count - left.count || left.name.label.localeCompare(right.name.label, 'ja')),
  );
  const top = rows[0];
  const schools = new Map<string, number>();
  for (const row of rows) schools.set(row.sub!.label, (schools.get(row.sub!.label) ?? 0) + 1);
  const topSchoolClubs = Math.max(0, ...schools.values());
  const topSchool = [...schools.entries()]
    .filter(([, count]) => count === topSchoolClubs)
    .map(([school]) => school)
    .join('・');
  const title = '同じ高校出身の選手が多いB.LEAGUEクラブ';
  return {
    id: 'club-high-school-alumni',
    path: EXTRA_RANKING_PATHS['club-high-school-alumni'],
    title,
    crumb: '同じ高校出身の選手が多いクラブ',
    description:
      '現在の所属クラブと出身高校の組み合わせで、同じ高校の出身者が2人以上いるクラブを人数の多い順に掲載しています。本サイトに登録済みの選手から集計し、各選手の経歴は出典つきで確認できます。',
    lede: top
      ? `同じ高校の出身者が今いっしょにプレーしている組み合わせは、登録済みの選手で${rows.length}組あります。最も多いのは${top.name.label}の${top.sub!.label}出身者で、${top.count}人です。`
      : '',
    share: top ? `${title}｜1位は${top.name.label}×${top.sub!.label}（${top.count}人）` : title,
    headers: { name: 'クラブ／出身高校', count: '人数', items: '選手' },
    points: [
      top ? `${top.name.label}には、${top.sub!.label}出身の選手が${top.count}人所属しています。` : '',
      topSchoolClubs >= 2
        ? `${topSchool}は、${topSchoolClubs}クラブで「同じ高校出身の選手が2人以上」の組み合わせに入っており、最も多くのクラブに出身者がまとまっています。`
        : '',
      `2人以上の組み合わせに入る選手は、のべ${rows.reduce((sum, row) => sum + row.count, 0)}人です。`,
    ].filter(Boolean),
    notes: [
      COMMON_NOTE,
      '現在の所属は、終了年が記録されていないクラブの所属です。',
      '出身高校は、本サイトに在籍記録のある高校です。複数の高校に在籍した選手は、それぞれの高校で数えています。',
    ],
    rows,
    indexSummary: rows
      .slice(0, 2)
      .map((row) => `${row.rank}位 ${row.name.label}×${row.sub!.label}（${row.count}人）`)
      .join('・'),
  };
}

// 2. 高校から大学を経ずにプロ入りした選手（出身高校別）
function highSchoolToPro(): ExtraRanking {
  type Entry = { player: PublicPlayer; school: Career; club: Career };
  const entries: Entry[] = [];
  for (const player of masterPlayers()) {
    const careers = masterCareers(player);
    // 大学・海外の学校（College等）の在籍記録がある選手は除く。
    // 「北海道文教大学附属高等学校」のように高校名に「大学」を含む付属校があるため、高校・中学は除いて判定する。
    const hasCollege = careers.some((career) => {
      const category = categoryOf(career);
      if (category === 'univ') return true;
      if (category === 'hs' || category === 'jhs') return false;
      return /College|University|カレッジ|ユニバーシティ/i.test(career.organization ?? '');
    });
    if (hasCollege) continue;
    const schools = careers.filter((career) => categoryOf(career) === 'hs' && career.endYear != null);
    if (!schools.length) continue;
    const lastSchool = schools.reduce((latest, career) => (career.endYear! > latest.endYear! ? career : latest));
    // U18・U15などのユースチームはトップチーム（プロ）の所属に数えない。
    const clubs = careers.filter(
      (career) => isClubCareer(career) && career.startYear != null && !/U\d{2}|ユース/.test(career.organization ?? ''),
    );
    if (!clubs.length) continue;
    const firstClub = clubs.reduce((first, career) => (career.startYear! < first.startYear! ? career : first));
    // 高校在籍の最終年までにB.LEAGUEクラブとの所属が始まっている（卒業と同時、または在学中）。
    if (firstClub.startYear! > lastSchool.endYear!) continue;
    entries.push({ player, school: lastSchool, club: firstClub });
  }
  const groups = new Map<string, Entry[]>();
  for (const entry of entries) {
    const key = entry.school.organizationId ?? entry.school.organization ?? '';
    groups.set(key, [...(groups.get(key) ?? []), entry]);
  }
  const rows = withRanks(
    [...groups.entries()]
      .map(([key, group]) => ({
        key,
        name: orgLink(group[0].school.organizationId, group[0].school.organization ?? ''),
        count: group.length,
        unit: '人',
        items: [...group]
          .sort((left, right) => right.club.startYear! - left.club.startYear! || byName(left.player, right.player))
          .map(({ player, club }) =>
            playerLink(player, `（${orgLink(club.organizationId, club.organization ?? '').label}・${club.startYear}年〜）`),
          ),
      }))
      .sort((left, right) => right.count - left.count || left.name.label.localeCompare(right.name.label, 'ja')),
  );
  const years = entries.map((entry) => entry.club.startYear!);
  const recent = years.filter((year) => year >= Math.max(...years) - 2).length;
  const title = '高校から大学を経ずにB.LEAGUE入りした選手';
  return {
    id: 'high-school-to-pro',
    path: EXTRA_RANKING_PATHS['high-school-to-pro'],
    title,
    crumb: '高校から直接B.LEAGUE入りした選手',
    description:
      '大学に進まず、高校在学中または卒業と同時にB.LEAGUEのクラブに所属した選手を、出身高校ごとに掲載しています。本サイトに登録済みの選手から抽出し、各選手の経歴は出典つきで確認できます。',
    lede: `高校から大学を経ずにB.LEAGUEのクラブに所属した選手は、本サイトに登録済みの選手のうち${entries.length}人です。出身高校ごとに、最初の所属クラブと所属開始年を掲載しています。`,
    share: `${title}｜登録済みデータで${entries.length}人`,
    headers: { name: '出身高校', count: '人数', items: '選手（最初の所属クラブ・開始年）' },
    points: [
      rows[0] && rows[0].count >= 2
        ? `最も多い出身高校は${rows.filter((row) => row.rank === 1).map((row) => row.name.label).join('と')}で、各${rows[0].count}人です。`
        : '',
      years.length ? `${entries.length}人のうち${recent}人は、${Math.max(...years) - 2}年以降に所属が始まった選手です。` : '',
      '高校在学中にトップチームに登録され、そのままプロ契約に進むケースも含みます（個々の契約形態は各選手の出典をご確認ください）。',
    ].filter(Boolean),
    notes: [
      COMMON_NOTE,
      '高校在籍の最終年（記録上の終了年）までに、B.LEAGUEのクラブとの所属が始まっている選手が対象です。',
      '大学（海外のCollege・Universityを含む）の在籍記録がある選手は含めていません。大学の在籍が本サイトに記録されていない可能性があるため、該当しない選手が含まれる場合があります。',
    ],
    rows,
    indexSummary: `${entries.length}人を出身高校別に掲載`,
  };
}

// 3. 現役選手が多い学年（世代）
function generation(): ExtraRanking {
  const groups = new Map<number, PublicPlayer[]>();
  let current = 0;
  for (const player of masterPlayers()) {
    if (!currentClub(player)) continue;
    current += 1;
    const date = birthDate(player);
    if (!date) continue;
    const year = schoolYearOf(date);
    groups.set(year, [...(groups.get(year) ?? []), player]);
  }
  const counted = [...groups.values()].reduce((sum, group) => sum + group.length, 0);
  const rows = withRanks(
    [...groups.entries()]
      .map(([year, group]) => ({
        key: String(year),
        name: { label: `${year}年度生まれ` },
        sub: { label: `${year + 19}年 高校卒業の学年` },
        count: group.length,
        unit: '人',
        items: [...group].sort(byName).map((player) => playerLink(player)),
      }))
      .sort((left, right) => right.count - left.count || Number(right.key) - Number(left.key)),
  );
  const top = rows.filter((row) => row.rank === 1);
  const title = 'B.LEAGUE現役選手が多い学年（世代）ランキング';
  const asOf = rankingAsOf();
  const medianYear = (() => {
    const years = [...groups.entries()].flatMap(([year, group]) => group.map(() => year)).sort((a, b) => a - b);
    return years[Math.floor(years.length / 2)];
  })();
  return {
    id: 'generation',
    path: EXTRA_RANKING_PATHS.generation,
    title,
    crumb: '現役選手が多い学年（世代）',
    description:
      'B.LEAGUEのクラブに現在所属する選手を、生年月日から学年（4月2日〜翌年4月1日生まれ）に分け、人数の多い順に掲載しています。本サイトに登録済みの選手から集計しています。',
    lede: top.length
      ? `B.LEAGUEのクラブに現在所属する登録選手${counted}人を学年別に数えると、最も多いのは${top.map((row) => row.name.label).join('・')}で${top[0].count}人です。`
      : '',
    share: top.length
      ? `${title}｜最多は${top.map((row) => row.name.label).join('・')}（${top[0].count}人）`
      : title,
    headers: { name: '学年', count: '人数', items: '選手' },
    points: [
      top.length ? `${top[0].name.label}は${top[0].sub!.label}で、${top[0].count}人が現在B.LEAGUEのクラブに所属しています。` : '',
      medianYear
        ? `学年の中央値は${medianYear}年度生まれ（現在${ageOn({ year: medianYear + 1, month: 4, day: 1 }, asOf)}〜${ageOn({ year: medianYear, month: 4, day: 2 }, asOf)}歳）です。`
        : '',
      current > counted ? `生年月日が登録されていない${current - counted}人は数えていません。` : '',
    ].filter(Boolean),
    notes: [
      COMMON_NOTE,
      '学年は日本の学校年度（4月2日〜翌年4月1日生まれ）で分けています。海外で教育を受けた選手も、生年月日から同じ方法で分けています。',
      '「高校卒業の学年」は、生年月日から計算した目安です。実際の卒業年とは異なる場合があります。',
      '現在の所属は、終了年が記録されていないB.LEAGUEのクラブの所属です。',
    ],
    rows,
    indexSummary: rows
      .slice(0, 3)
      .map((row) => `${row.rank}位 ${row.name.label}（${row.count}人）`)
      .join('・'),
  };
}

// 4. 現役最年長選手
const OLDEST_LIMIT = 20;
function oldestActive(): ExtraRanking {
  const asOf = rankingAsOf();
  const list = masterPlayers()
    .map((player) => ({ player, club: currentClub(player), date: birthDate(player) }))
    .filter((entry): entry is { player: PublicPlayer; club: Career; date: NonNullable<ReturnType<typeof birthDate>> } =>
      Boolean(entry.club && entry.date),
    )
    .sort(
      (left, right) =>
        left.date.year - right.date.year || left.date.month - right.date.month || left.date.day - right.date.day,
    );
  const cut = list[OLDEST_LIMIT - 1];
  const top = list.filter(
    (entry, index) =>
      index < OLDEST_LIMIT ||
      (cut && entry.date.year === cut.date.year && entry.date.month === cut.date.month && entry.date.day === cut.date.day),
  );
  const rows = top.map((entry, index) => ({
    key: entry.player.id,
    rank: index + 1,
    name: playerLink(entry.player),
    sub: { label: `${entry.date.year}年${entry.date.month}月${entry.date.day}日生まれ` },
    count: ageOn(entry.date, asOf),
    unit: '歳',
    items: [orgLink(entry.club.organizationId, entry.club.organization ?? '')],
  }));
  const first = rows[0];
  const clubCounts = new Map<string, number>();
  for (const row of rows) clubCounts.set(row.items[0].label, (clubCounts.get(row.items[0].label) ?? 0) + 1);
  const topClubCount = Math.max(0, ...clubCounts.values());
  const topClub = [...clubCounts.entries()]
    .filter(([, count]) => count === topClubCount)
    .map(([club]) => club)
    .join('・');
  const title = 'B.LEAGUE現役最年長選手ランキング';
  return {
    id: 'oldest-active',
    path: EXTRA_RANKING_PATHS['oldest-active'],
    title,
    crumb: '現役最年長選手',
    description: `B.LEAGUEのクラブに現在所属する選手を、生年月日の早い順に${OLDEST_LIMIT}人掲載しています。年齢と所属クラブも確認できます。本サイトに登録済みの選手から集計しています。`,
    lede: first
      ? `B.LEAGUEのクラブに現在所属する登録選手のうち、最年長は${first.name.label}（${first.items[0].label}）の${first.count}歳です。`
      : '',
    share: first ? `${title}｜最年長は${first.name.label}（${first.count}歳）` : title,
    headers: { name: '選手', count: '年齢', items: '現在の所属クラブ' },
    points: [
      rows.length ? `上位${rows.length}人は${rows[rows.length - 1].count}〜${first.count}歳です。` : '',
      `40歳以上でB.LEAGUEのクラブに所属している登録選手は${list.filter((entry) => ageOn(entry.date, asOf) >= 40).length}人です。`,
      topClubCount >= 2 && !topClub.includes('・') ? `上位${rows.length}人に最も多く入っているクラブは${topClub}で、各${topClubCount}人です。` : '',
    ].filter(Boolean),
    notes: [
      COMMON_NOTE,
      `年齢は、データの集計日（下記）時点で計算しています。`,
      '現在の所属は、終了年が記録されていないB.LEAGUEのクラブの所属です。生年月日が登録されていない選手は含まれません。',
    ],
    rows,
    indexSummary: rows
      .slice(0, 3)
      .map((row) => `${row.rank}位 ${row.name.label}（${row.count}歳）`)
      .join('・'),
  };
}

// 5. B.LEAGUE開幕以降に所属したクラブ数が多い選手
const MOST_CLUBS_MIN = 7;
function mostClubs(): ExtraRanking {
  const entries = masterPlayers().map((player) => {
    const clubs = masterCareers(player)
      .filter((career) => isClubCareer(career) && (career.endYear == null || career.endYear > BLEAGUE_START_YEAR))
      .sort((left, right) => (left.startYear ?? 9999) - (right.startYear ?? 9999));
    const unique: Career[] = [];
    for (const career of clubs) {
      const key = career.organizationId ?? career.organization;
      if (!unique.some((item) => (item.organizationId ?? item.organization) === key)) unique.push(career);
    }
    return { player, clubs: unique };
  });
  const listed = entries
    .filter((entry) => entry.clubs.length >= MOST_CLUBS_MIN)
    .sort((left, right) => right.clubs.length - left.clubs.length || byName(left.player, right.player));
  const rows = withRanks(
    listed.map((entry) => ({
      key: entry.player.id,
      name: playerLink(entry.player),
      count: entry.clubs.length,
      unit: 'クラブ',
      items: entry.clubs.map((career) => orgLink(career.organizationId, career.organization ?? '')),
    })),
  );
  const withClubs = entries.filter((entry) => entry.clubs.length > 0);
  const fivePlus = withClubs.filter((entry) => entry.clubs.length >= 5).length;
  const first = rows[0];
  const title = 'B.LEAGUE開幕以降に所属したクラブ数が多い選手';
  return {
    id: 'most-clubs',
    path: EXTRA_RANKING_PATHS['most-clubs'],
    title,
    crumb: '所属したクラブ数が多い選手',
    description: `2016-17シーズンのB.LEAGUE開幕以降に所属したクラブの数が${MOST_CLUBS_MIN}以上の選手を、多い順に掲載しています。所属したクラブも順に確認できます。本サイトに登録済みの選手から集計しています。`,
    lede: first
      ? `B.LEAGUE開幕以降に所属したクラブ数が最も多い登録選手は、${first.name.label}の${first.count}クラブです。${MOST_CLUBS_MIN}クラブ以上の選手は${rows.length}人います。`
      : '',
    share: first ? `${title}｜最多は${first.name.label}（${first.count}クラブ）` : title,
    headers: { name: '選手', count: 'クラブ数', items: '所属したクラブ（開始年順）' },
    points: [
      `クラブの所属記録がある登録選手${withClubs.length}人のうち、5クラブ以上に所属した選手は${fivePlus}人（${Math.round((fivePlus / withClubs.length) * 100)}%）です。`,
      first ? `最多の${first.name.label}は、${first.items[0].label}から${first.items[first.items.length - 1].label}まで${first.count}クラブに所属しています。` : '',
    ].filter(Boolean),
    notes: [
      COMMON_NOTE,
      '2016-17シーズン以降も続いていた所属と、それ以降に始まった所属を数えています（B.LEAGUE開幕より前に終わった所属は含みません）。',
      '期限付き移籍の所属先も1クラブとして数えています。同じクラブに複数回所属した場合は1クラブです。改称したクラブは1クラブとして扱っています。',
      'B.LEAGUE以外（海外リーグなど）のクラブは含みません。',
    ],
    rows,
    indexSummary: rows
      .slice(0, 2)
      .map((row) => `${row.rank}位 ${row.name.label}（${row.count}クラブ）`)
      .join('・'),
  };
}

const builders: Record<ExtraRankingId, () => ExtraRanking> = {
  'club-high-school-alumni': clubHighSchoolAlumni,
  'high-school-to-pro': highSchoolToPro,
  generation,
  'oldest-active': oldestActive,
  'most-clubs': mostClubs,
};
const cache = new Map<ExtraRankingId, ExtraRanking>();

export function buildExtraRanking(id: ExtraRankingId): ExtraRanking {
  const cached = cache.get(id);
  if (cached) return cached;
  const ranking = builders[id]();
  cache.set(id, ranking);
  return ranking;
}
