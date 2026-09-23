import type { MetadataRoute } from 'next';
import { organizations, players } from './public-data';

const baseUrl = 'https://japanbasketballarchive.com';

export default function sitemap(): MetadataRoute.Sitemap {
  const playerPages: MetadataRoute.Sitemap = players.map((player) => ({
    url: `${baseUrl}/players/${player.slug}`,
    lastModified: '2026-09-23',
    changeFrequency: 'weekly',
    priority: 0.7,
  }));

  const organizationPages: MetadataRoute.Sitemap = organizations.map((organization) => ({
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
    ...organizationPages,
    ...playerPages,
  ];
}
