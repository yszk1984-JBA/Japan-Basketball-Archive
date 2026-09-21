import { masterPlayers, masterPublication, masterSources } from './master-data';
import {
  homepagePlacements,
  players as prototypePlayers,
  sources as prototypeSources,
} from './prototype-data';

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

const approvedIds = new Set<string>(masterPlayers.map((player) => player.id));

const candidatePlayers: PublicPlayer[] = prototypePlayers
  .filter((player) => !approvedIds.has(player.id))
  .map((player) => ({
    ...player,
    dataStatus: 'candidate',
    approvalId: null,
  }));

export const players: readonly PublicPlayer[] = [
  ...(masterPlayers as unknown as readonly PublicPlayer[]),
  ...candidatePlayers,
];

const masterSourceIds = new Set<string>(masterSources.map((source) => source.id));
export const sources: readonly PublicSource[] = [
  ...(masterSources as unknown as readonly PublicSource[]),
  ...prototypeSources
    .filter((source) => !masterSourceIds.has(source.id))
    .map((source) => ({ ...source, dataStatus: 'candidate' as const })),
];

const publicationPriority: Record<string, number> = {
  P000064: 100,
  P000028: 210,
  P000066: 220,
  P000073: 230,
  P000074: 240,
};

for (const placement of homepagePlacements) {
  publicationPriority[placement.playerId] ??= placement.priority + 100;
}

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

export { masterPublication };
