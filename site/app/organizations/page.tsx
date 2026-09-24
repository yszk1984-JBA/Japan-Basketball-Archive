/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import type { Metadata } from 'next';
import { getOrganizationPlayers, organizations } from '../public-data';
import { organizationCategory } from '../organization-category';
import { OrganizationsListView, type OrganizationRow } from './OrganizationsListView';

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
      <header className="jbaListB-header">
        <a href="/" className="jbaListB-brand">
          <span className="jbaListB-brandMark">JB</span>
          <span className="jbaListB-brandName">Japan Basketball Archive</span>
        </a>
        <nav className="jbaListB-nav">
          <a href="/players">選手</a>
          <a href="/organizations" aria-current="page">組織</a>
        </nav>
      </header>

      <div className="jbaListB-breadcrumb">
        <a href="/">TOP</a> ／ <span>組織一覧</span>
      </div>

      <div className="jbaListB-main">
        <div>
          <p className="jbaListB-eyebrow">Organizations</p>
          <h1 className="jbaListB-h1">組織一覧</h1>
        </div>

        <OrganizationsListView rows={rows} totalCount={organizations.length} />
      </div>

      <footer className="jbaListB-footer">
        <div className="jbaListB-footerInner">
          <div>
            <div className="jbaListB-footerTitle">Japan Basketball Archive</div>
            <div>日本バスケットボールの人物と所属を、出典とともに記録するアーカイブです。</div>
          </div>
          <div className="jbaListB-footerLinks">
            <a href="/players">選手一覧</a>
          </div>
        </div>
      </footer>
    </main>
  );
}
