import { masterApprovals, masterOrganizationCurrentNames, masterPlayers, masterPublication, masterSources } from './master-data';
import { candidatePlayers, candidateSources } from './candidate-data';

export type DataStatus = 'master' | 'candidate';

export type PublicSource = {
  readonly id: string;
  readonly title: string;
  readonly publisher: string;
  readonly url: string;
  readonly location: string;
  readonly accessedAt: string;
  readonly dataStatus: DataStatus;
};

export type PublicPlayer = {
  readonly id: string;
  readonly slug: string;
  readonly name: string;
  readonly cardContext: string;
  readonly dataStatus: DataStatus;
  readonly approvalId: string | null;
  // 人物を最初に登録した承認とは別に、経歴を追加した承認（例：深掘りのApproval Sprint 008）。
  readonly enrichmentApprovalIds?: readonly string[];
  readonly facts: readonly {
    readonly label: string;
    readonly value: string;
    readonly context: string;
    readonly sourceIds: readonly string[];
  }[];
  readonly careers: readonly {
    readonly period: string;
    readonly organization: string | null;
    readonly organizationId?: string;
    // 年の数値（Master人物のみ。候補人物のデータには無い）。年表（ガントチャート）表示に使う。
    readonly startYear?: number | null;
    readonly endYear?: number | null;
    readonly detail: string;
    readonly status: string;
    readonly sourceIds: readonly string[];
  }[];
  readonly aliases: readonly {
    readonly period: string;
    readonly label: string;
    readonly value: string;
    readonly sourceIds: readonly string[];
  }[];
  // 人物ごとの出典内位置（共有される出典、例：順位表で他の選手の位置まで並ばないように）。Master人物のみ。
  readonly sourceLocations?: Readonly<Record<string, string>>;
};

export type OrganizationCurrentName = {
  readonly currentName: string;
  // 「現」（改称）または「統合後」（統合による新設校）。
  readonly label: string;
  readonly effectiveDate: string;
  readonly changeType: string;
  readonly source: { readonly title: string; readonly publisher: string; readonly url: string };
};

export type PublicOrganization = {
  readonly id: string;
  readonly slug: string;
  // 資料に書かれた当時の名称（Masterのorganization.csv）。
  readonly name: string;
  // 改称・統合した学校の現在の名称（Masterの付随データ。該当しない組織はundefined）。
  readonly currentName?: OrganizationCurrentName;
};

export const players: readonly PublicPlayer[] = [
  ...(masterPlayers as unknown as readonly PublicPlayer[]),
  ...(candidatePlayers as unknown as readonly PublicPlayer[]),
];

const masterSourceIds = new Set<string>(masterSources.map((source) => source.id));
export const sources: readonly PublicSource[] = [
  ...(masterSources as unknown as readonly PublicSource[]),
  ...(candidateSources as unknown as readonly PublicSource[]).filter((source) => !masterSourceIds.has(source.id)),
];

const publicationPriority: Record<string, number> = {
  P000064: 100,
  P000028: 210,
  P000066: 220,
  P000073: 230,
  P000074: 240,
};

export function getHomepagePlayers() {
  const originalOrder = new Map(players.map((player, index) => [player.id, index]));
  return [...players].sort((left, right) => {
    const leftPriority = publicationPriority[left.id];
    const rightPriority = publicationPriority[right.id];
    if (leftPriority !== undefined && rightPriority !== undefined) return leftPriority - rightPriority;
    if (leftPriority !== undefined) return -1;
    if (rightPriority !== undefined) return 1;
    return (originalOrder.get(left.id) ?? 0) - (originalOrder.get(right.id) ?? 0);
  });
}

export function getPlayer(slug: string) {
  return players.find((player) => player.slug === slug || player.id.toLowerCase() === slug);
}

export function getSources(ids: readonly string[]) {
  return sources.filter((source) => ids.includes(source.id));
}

// 既存の手作り組織ページのURLを維持するための別名。新規追加時は基本的に不要
// （organization_idを小文字にしたスラッグが自動で割り当てられる）。
export const organizationSlugAliases: Record<string, string> = {
  'fukuoka-daiichi': 'ORG000010',
  // Merged into the kept ID (data/master/corrections/2026-10-01_org_merge_hakuoh_tomita.md)
  org000208: 'ORG000093',
  org000436: 'ORG000266',
};

function canonicalOrganizationSlug(organizationId: string): string {
  return organizationId.toLowerCase();
}

const organizationNamesById = new Map<string, string>();
for (const player of players) {
  for (const career of player.careers) {
    if (career.organizationId && career.organization && !organizationNamesById.has(career.organizationId)) {
      organizationNamesById.set(career.organizationId, career.organization);
    }
  }
}

export const organizations: readonly PublicOrganization[] = [...organizationNamesById.entries()]
  .map(([id, name]) => {
    const currentName = (masterOrganizationCurrentNames as Record<string, OrganizationCurrentName>)[id];
    return { id, name, slug: canonicalOrganizationSlug(id), ...(currentName ? { currentName } : {}) };
  })
  .sort((left, right) => left.name.localeCompare(right.name, 'ja'));

export function getOrganization(slug: string): PublicOrganization | undefined {
  const resolvedId = organizationSlugAliases[slug] ?? slug.toUpperCase();
  return organizations.find((organization) => organization.id === resolvedId);
}

// 「明成高等学校（現：仙台大学附属明成高等学校）」のように、当時の名称に現在の名称を書き添えた表示名。
export function organizationDisplayName(organization: PublicOrganization): string {
  const current = organization.currentName;
  return current ? `${organization.name}（${current.label}：${current.currentName}）` : organization.name;
}

export function getOrganizationById(organizationId: string): PublicOrganization | undefined {
  return organizations.find((organization) => organization.id === organizationId);
}

export function organizationSlugFor(organizationId: string | undefined): string | undefined {
  if (!organizationId) return undefined;
  return organizations.find((organization) => organization.id === organizationId)?.slug;
}

export function getOrganizationPlayers(organizationId: string) {
  return players.filter((player) =>
    player.careers.some((career) => career.organizationId === organizationId),
  );
}

export function getOrganizationSourceIds(organizationId: string): string[] {
  return [
    ...new Set(
      getOrganizationPlayers(organizationId).flatMap((player) =>
        player.careers
          .filter((career) => career.organizationId === organizationId)
          .flatMap((career) => career.sourceIds),
      ),
    ),
  ];
}


// 選手一覧・組織カテゴリー表示のために「現在（または直近）の所属」を1件選ぶ。
// Master人物は生成済みの並び順の最後の1件、候補人物はbuild_site_candidate_data.pyと
// 同じ並び替えロジック（(期間未確認かどうか, period文字列)の昇順で並べて最後の1件）で、
// cardContextの表示と矛盾しない組織を選ぶ。
export function getPrimaryCareer(player: PublicPlayer) {
  if (player.careers.length === 0) return undefined;
  // Master人物の経歴はbuild_site_master_data.pyが時系列順（学校→クラブの開始年順）に
  // 並べ、cardContextも最後の1件から作っているため、同じく最後の1件を使う。
  if (player.dataStatus === 'master') return player.careers[player.careers.length - 1];
  const sorted = [...player.careers].sort((left, right) => {
    const leftUnknown = left.period === '期間未確認' ? 1 : 0;
    const rightUnknown = right.period === '期間未確認' ? 1 : 0;
    if (leftUnknown !== rightUnknown) return leftUnknown - rightUnknown;
    return left.period < right.period ? -1 : left.period > right.period ? 1 : 0;
  });
  return sorted[sorted.length - 1];
}

export { masterApprovals, masterPublication };
