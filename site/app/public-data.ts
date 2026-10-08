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
  // この現在名を承認した日（サイトマップのlastmodに使う）。
  readonly approvedAt: string;
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

// トップページ「注目選手」の選定方針（2026-10-08、Yuichiと検討の上「ハイブリッド方式」で決定）。
// 固定枠：海外（NBA等）経歴の出典が確認できている、知名度の高い選手を常に先頭に表示。
// 自動枠：固定枠以外のMaster人物から、承認日が新しい順に残り枠を自動で埋める（データが
// 増えるほど新着選手が自然に反映され、手動メンテナンスの手間を抑える）。
// あくまで編集上のスポットライトであり、実力・知名度の順位付けを意図したものではない
// （MONETIZATION_DRAFTの「ランキングで非掲載者の存在を否定しない」方針と同じ考え方）。
const FEATURED_PLAYER_IDS: readonly string[] = [
  'P000064', // 河村勇輝（ロサンゼルス・クリッパーズ）
  'P000103', // 渡邊雄太（千葉ジェッツ、NBA経歴あり）
  'P000105', // 田臥勇太（宇都宮ブレックス、日本人初のNBA選手）
  'P000106', // 富永啓生（レバンガ北海道）
  'P000107', // 馬場雄大（長崎、NBA経歴あり）
  'P000084', // 比江島慎（宇都宮ブレックス、日本代表）
];

const HOMEPAGE_FEATURED_COUNT = 20;

export function getHomepagePlayers() {
  const featuredIds = new Set(FEATURED_PLAYER_IDS);
  const fixed = FEATURED_PLAYER_IDS.map((id) => players.find((player) => player.id === id)).filter(
    (player): player is PublicPlayer => player !== undefined,
  );

  const remainingSlots = Math.max(HOMEPAGE_FEATURED_COUNT - fixed.length, 0);
  // 承認日の新しい順（latestApprovedAtは本ファイル下部で定義、サイトマップのlastmod計算と共通。候補データはnullのため対象外）。
  const autoFilled = players
    .filter((player) => player.dataStatus === 'master' && !featuredIds.has(player.id))
    .sort((left, right) => (latestApprovedAt(right) ?? '').localeCompare(latestApprovedAt(left) ?? ''))
    .slice(0, remainingSlots);

  return [...fixed, ...autoFilled];
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

// Masterデータの承認日（新着順の並び替え・サイトマップのlastmodに使用）。経歴追加の承認
// （enrichmentApprovalIds）も含めた最新日を採用する。Candidateデータは承認日を持たないためnull。
export function latestApprovedAt(player: PublicPlayer): string | null {
  if (player.dataStatus !== 'master') return null;
  const approvals = masterApprovals as Record<string, { approvedAt: string }>;
  const ids = [player.approvalId, ...(player.enrichmentApprovalIds ?? [])].filter((id): id is string => Boolean(id));
  const dates = ids.map((id) => approvals[id]?.approvedAt).filter((date): date is string => Boolean(date));
  if (dates.length === 0) return masterPublication.approvedAt;
  return dates.reduce((latest, date) => (date > latest ? date : latest));
}

// 組織ページの最終更新日：所属するMaster選手の承認日と、現在名の承認日のうち最新のもの。
export function organizationUpdatedAt(organization: PublicOrganization): string | null {
  const dates = getOrganizationPlayers(organization.id)
    .map((player) => latestApprovedAt(player))
    .filter((date): date is string => Boolean(date));
  if (organization.currentName) dates.push(organization.currentName.approvedAt);
  return dates.length ? dates.reduce((latest, date) => (date > latest ? date : latest)) : null;
}

// サイト全体のデータの最終更新日（一覧・ランキング・トップページのlastmodに使用）。
export function siteDataUpdatedAt(): string {
  const dates = players.map((player) => latestApprovedAt(player)).filter((date): date is string => Boolean(date));
  for (const organization of organizations) {
    if (organization.currentName) dates.push(organization.currentName.approvedAt);
  }
  return dates.reduce((latest, date) => (date > latest ? date : latest), masterPublication.approvedAt);
}

