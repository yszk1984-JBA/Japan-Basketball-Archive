/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import type { Metadata } from 'next';
import { getOrganizationPlayers, organizations } from '../public-data';
import { organizationCategory } from '../organization-category';
import { OrganizationsListView, type OrganizationRow } from './OrganizationsListView';
import { SiteBreadcrumb, SiteFooter, SiteHeader } from '../seo';

export const metadata: Metadata = {
  title: '組織一覧',
  description: '学校・大学・クラブ等、選手の所属先として登録済みの組織の一覧です。',
  alternates: { canonical: '/organizations' },
};

export default function OrganizationsIndexPage() {
  const rows: OrganizationRow[] = organizations.map((organization) => {
    const relatedPlayers = getOrganizationPlayers(organization.id);
    return {
      id: organization.id,
      slug: organization.slug,
      name: organization.name,
      category: organizationCategory(organization.name),
      total: relatedPlayers.length,
      master: relatedPlayers.filter((player) => player.dataStatus === 'master').length,
    };
  });

  return (
    <main className="jbaListB-page">
      <SiteHeader active="organizations" />

      <SiteBreadcrumb crumbs={[{ label: '組織一覧' }]} />

      <div className="jbaListB-main">
        <div>
          <p className="jbaListB-eyebrow">Organizations</p>
          <h1 className="jbaListB-h1">組織一覧</h1>
        </div>

        <OrganizationsListView rows={rows} totalCount={organizations.length} />
      </div>

      <SiteFooter />
    </main>
  );
}
