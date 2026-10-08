import type { MetadataRoute } from 'next';
import {
  getOrganizationPlayers,
  latestApprovedAt,
  organizations,
  organizationUpdatedAt,
  players,
  siteDataUpdatedAt,
} from './public-data';
import { isOrganizationIndexable } from './seo';
import { siteUrl } from './site-url';

const baseUrl = siteUrl;

// /about の本文を最後に更新した日。本文を書き換えたら更新する。
const ABOUT_UPDATED_AT = '2026-10-06';

// lastmodは、各ページの内容の元になったMasterデータの承認日から決める（固定日付にしない）。
// Googleはlastmodが実際の更新と一致している場合だけ参考にするため、承認日のないページ
// （Candidateの選手）には付けない。changefreq・priorityはGoogleが使わないため出力しない。
export default function sitemap(): MetadataRoute.Sitemap {
  const dataUpdatedAt = siteDataUpdatedAt();

  const playerPages: MetadataRoute.Sitemap = players.map((player) => {
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
    ...['', '/players', '/organizations', '/rankings', '/rankings/high-school', '/rankings/university'].map(
      (path) => ({ url: `${baseUrl}${path}`, lastModified: dataUpdatedAt }),
    ),
    { url: `${baseUrl}/about`, lastModified: ABOUT_UPDATED_AT },
    ...organizationPages,
    ...playerPages,
  ];
}
