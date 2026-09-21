import type { MetadataRoute } from 'next';
import { players } from './public-data';

const baseUrl = 'https://japanbasketballarchive.com';

export default function sitemap(): MetadataRoute.Sitemap {
  const playerPages: MetadataRoute.Sitemap = players.map((player) => ({
    url: `${baseUrl}/players/${player.slug}`,
    lastModified: '2026-09-21',
    changeFrequency: 'weekly',
    priority: 0.7,
  }));

  return [
    {
      url: baseUrl,
      lastModified: '2026-09-21',
      changeFrequency: 'weekly',
      priority: 1,
    },
    {
      url: `${baseUrl}/organizations/fukuoka-daiichi`,
      lastModified: '2026-09-21',
      changeFrequency: 'weekly',
      priority: 0.8,
    },
    ...playerPages,
  ];
}
