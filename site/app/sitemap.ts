import type { MetadataRoute } from 'next';
import {
  getOrganizationPlayers,
  latestApprovedAt,
  organizations,
  organizationUpdatedAt,
  players,
  siteDataUpdatedAt,
} from './public-data';
import { isOrganizationIndexable, isPlayerIndexable } from './seo';
import { siteUrl } from './site-url';
import { EXTRA_RANKING_PATHS } from './rankings/extra-rankings';
import { columnPath, COLUMNS } from './columns/columns-data';
import { guidePath, GUIDES } from './guide/guide-data';

const baseUrl = siteUrl;

// /about の本文を最後に更新した日。本文を書き換えたら更新する。
const ABOUT_UPDATED_AT = '2026-11-28';
// /privacy の本文を最後に更新した日。本文を書き換えたら更新する。
const PRIVACY_UPDATED_AT = '2026-11-28';

// lastmodは、各ページの内容の元になったMasterデータの承認日から決める（固定日付にしない）。
// Googleはlastmodが実際の更新と一致している場合だけ参考にするため、承認日のないページ
// （Candidateの選手）には付けない。changefreq・priorityはGoogleが使わないため出力しない。
export default function sitemap(): MetadataRoute.Sitemap {
  const dataUpdatedAt = siteDataUpdatedAt();

  const playerPages: MetadataRoute.Sitemap = players.filter(isPlayerIndexable).map((player) => {
    const updatedAt = latestApprovedAt(player);
    return { url: `${baseUrl}/players/${player.slug}`, ...(updatedAt ? { lastModified: updatedAt } : {}) };
  });

  // noindexの組織ページ（所属選手が少ないページ）はサイトマップに載せない。
  const organizationPages: MetadataRoute.Sitemap = organizations
    .filter((organization) => isOrganizationIndexable(getOrganizationPlayers(organization.id).length))
    .map((organization) => {
      const updatedAt = organizationUpdatedAt(organization);
      return {
        url: `${baseUrl}/organizations/${organization.slug}`,
        ...(updatedAt ? { lastModified: updatedAt } : {}),
      };
    });

  return [
    ...['', '/players', '/organizations', '/rankings', '/updates', '/contact', '/columns', ...COLUMNS.map((column) => columnPath(column.slug)), '/rankings/premier-high-school', '/rankings/premier-university', '/rankings/bone-high-school', '/rankings/bone-university', '/rankings/high-school', '/rankings/university', '/rankings/high-school-to-university', '/rankings/one-club', ...Object.values(EXTRA_RANKING_PATHS)].map(
      (path) => ({ url: `${baseUrl}${path}`, lastModified: dataUpdatedAt }),
    ),
    // Guide（実用ガイド）は承認済みデータとは無関係のため、記事ごとの更新日を使う。
    { url: `${baseUrl}/guide`, lastModified: GUIDES.map((guide) => guide.updatedAt ?? guide.publishedAt).sort().at(-1) },
    ...GUIDES.map((guide) => ({ url: `${baseUrl}${guidePath(guide.slug)}`, lastModified: guide.updatedAt ?? guide.publishedAt })),
    { url: `${baseUrl}/about`, lastModified: ABOUT_UPDATED_AT },
    { url: `${baseUrl}/privacy`, lastModified: PRIVACY_UPDATED_AT },
    ...organizationPages,
    ...playerPages,
  ];
}
