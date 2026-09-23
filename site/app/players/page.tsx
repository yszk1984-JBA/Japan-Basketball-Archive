/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import { ArrowLeft, ArrowRight } from 'lucide-react';
import type { Metadata } from 'next';
import { players } from '../public-data';
import { baseOpenGraph, breadcrumbJsonLd, JsonLd, SiteLinks, siteUrl } from '../seo';

const title = `選手一覧（${players.length}人）`;
const description = `日本バスケットボール選手${players.length}人の所属・経歴を、出典とともに掲載しています。高校・大学・プロの所属記録をたどれます。`;

export const metadata: Metadata = {
  title,
  description,
  alternates: { canonical: '/players' },
  openGraph: { ...baseOpenGraph, title, description, url: '/players' },
};

export default function PlayersIndexPage() {
  const masterPlayers = players.filter((player) => player.dataStatus === 'master');
  const candidatePlayers = players.filter((player) => player.dataStatus !== 'master');

  const sections = [
    { key: 'master', eyebrow: 'Approved Master', heading: '承認済み人物', rows: masterPlayers },
    { key: 'candidate', eyebrow: 'Candidate records', heading: '確認中の人物', rows: candidatePlayers },
  ].filter((section) => section.rows.length > 0);

  return (
    <main className="detail-shell">
      <JsonLd
        data={{
          '@context': 'https://schema.org',
          '@graph': [
            {
              '@type': 'CollectionPage',
              name: title,
              url: `${siteUrl}/players`,
              description,
            },
            breadcrumbJsonLd([
              { name: 'ホーム', path: '/' },
              { name: '選手一覧', path: '/players' },
            ]),
          ],
        }}
      />
      <nav className="detail-nav"><a href="/"><ArrowLeft size={17} /> アーカイブへ戻る</a><SiteLinks /><span>Prototype · 確認中</span></nav>
      <header className="organization-header">
        <p className="eyebrow">Players</p>
        <h1>選手一覧</h1>
        <p>現在、{players.length}人を掲載しています（承認済み{masterPlayers.length}人・確認中{candidatePlayers.length}人）。所属組織や年代による絞り込みは未対応です。</p>
      </header>
      {sections.map((section) => (
        <section className="roster-section" key={section.key}>
          <div className="section-heading"><div><p className="eyebrow">{section.eyebrow}</p><h2>{section.heading}</h2></div><span>{section.rows.length} records</span></div>
          <div className="roster-list">
            {section.rows.map((player) => (
              <a href={`/players/${player.slug}`} key={player.id}>
                <span className="number">{section.key === 'master' ? 'M' : '—'}</span>
                <div><strong>{player.name}</strong><p>{player.cardContext} · {player.id}</p></div>
                <ArrowRight size={19} />
              </a>
            ))}
          </div>
        </section>
      ))}
    </main>
  );
}
