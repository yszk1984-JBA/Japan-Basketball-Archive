import { masterPlayers, masterPublication, masterSources } from './master-data';
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
};

export type PublicOrganization = {
  readonly id: string;
  readonly slug: string;
  readonly name: string;
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
  .map(([id, name]) => ({ id, name, slug: canonicalOrganizationSlug(id) }))
  .sort((left, right) => left.name.localeCompare(right.name, 'ja'));

export function getOrganization(slug: string): PublicOrganization | undefined {
  const resolvedId = organizationSlugAliases[slug] ?? slug.toUpperCase();
  return organizations.find((organization) => organization.id === resolvedId);
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

export { masterPublication };
