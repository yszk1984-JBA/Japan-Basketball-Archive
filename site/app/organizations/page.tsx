/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import { ArrowLeft, ArrowRight } from 'lucide-react';
import type { Metadata } from 'next';
import { getOrganizationPlayers, organizations } from '../public-data';

export const metadata: Metadata = {
  title: '組織一覧',
  description: '学校・大学・クラブ等、選手の所属先として登録済みの組織の一覧です。',
  alternates: { canonical: '/organizations' },
};

export default function OrganizationsIndexPage() {
  const rows = organizations.map((organization) => {
    const relatedPlayers = getOrganizationPlayers(organization.id);
    return {
      organization,
      total: relatedPlayers.length,
      master: relatedPlayers.filter((player) => player.dataStatus === 'master').length,
    };
  });

  return (
    <main className="detail-shell">
      <nav className="detail-nav"><a href="/"><ArrowLeft size={17} /> アーカイブへ戻る</a><span>Prototype · 確認中</span></nav>
      <header className="organization-header"><p className="eyebrow">Organizations</p><h1>組織一覧</h1><p>現在、選手のCareerとして参照されている組織は{organizations.length}件です。学校種別（高校・大学等）による分類は未対応です。</p></header>
      <section className="roster-section">
        <div className="roster-list">
          {rows.map(({ organization, total, master }) => (
            <a href={`/organizations/${organization.slug}`} key={organization.id}>
              <span className="number">{organization.id.replace('ORG', '')}</span>
              <div><strong>{organization.name}</strong><p>{total} records{master > 0 ? ` · うちMaster ${master}件` : ''}</p></div>
              <ArrowRight size={19} />
            </a>
          ))}
        </div>
      </section>
    </main>
  );
}
