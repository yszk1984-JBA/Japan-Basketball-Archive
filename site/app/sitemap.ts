import type { MetadataRoute } from 'next';
import { getOrganizationPlayers, organizations, players } from './public-data';
import { isOrganizationIndexable } from './seo';
import { siteUrl } from './site-url';

const baseUrl = siteUrl;

export default function sitemap(): MetadataRoute.Sitemap {
  const playerPages: MetadataRoute.Sitemap = players.map((player) => ({
    url: `${baseUrl}/players/${player.slug}`,
    lastModified: '2026-09-23',
    changeFrequency: 'weekly',
    priority: 0.7,
  }));

  // noindexの組織ページ（所属選手が少ないページ）はサイトマップに載せない。
  const organizationPages: MetadataRoute.Sitemap = organizations
    .filter((organization) => isOrganizationIndexable(getOrganizationPlayers(organization.id).length))
    .map((organization) => ({
      url: `${baseUrl}/organizations/${organization.slug}`,
      lastModified: '2026-09-23',
      changeFrequency: 'weekly',
      priority: 0.6,
    }));

  return [
    {
      url: baseUrl,
      lastModified: '2026-09-23',
      changeFrequency: 'weekly',
      priority: 1,
    },
    {
      url: `${baseUrl}/players`,
      lastModified: '2026-09-23',
      changeFrequency: 'weekly',
      priority: 0.8,
    },
    {
      url: `${baseUrl}/organizations`,
      lastModified: '2026-09-23',
      changeFrequency: 'weekly',
      priority: 0.8,
    },
    ...['/rankings', '/rankings/high-school', '/rankings/university', '/about'].map((path) => ({
      url: `${baseUrl}${path}`,
      lastModified: '2026-10-06',
      changeFrequency: 'weekly' as const,
      priority: 0.8,
    })),
    ...organizationPages,
    ...playerPages,
  ];
}
