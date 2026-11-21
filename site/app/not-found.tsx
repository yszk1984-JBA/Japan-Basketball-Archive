/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import { ArrowRight } from 'lucide-react';
import { getPrimaryCareer, getOrganizationPlayers, organizations, players } from './public-data';
import { TopSearch, type TopSearchEntry } from './TopSearch';
import { SiteFooter, SiteHeader } from './seo';

// Next.js/vinextのApp Router規約に従い、存在しないURL（削除済みの選手ID、リンク切れなど）に
// アクセスしたときに表示される。これまでヘッダー・フッターのない無地の英語ページ
// （「404 / This page could not be found.」）だったため、サイトのデザインに合わせて
// 日本語化し、トップ・選手一覧・組織一覧への導線とサイト内検索を追加する。
export default function NotFound() {
  // トップページと同じ検索候補（選手・組織）。英字表記での検索にも対応。
  const searchEntries: TopSearchEntry[] = [
    ...players.map((player) => ({
      kind: 'player' as const,
      name: player.name,
      href: `/players/${player.slug}`,
      meta: getPrimaryCareer(player)?.organization ?? '',
      altName: player.facts.find((fact) => fact.label === '英字表記')?.value,
    })),
    ...organizations
      .map((organization) => ({ organization, count: getOrganizationPlayers(organization.id).length }))
      .filter(({ count }) => count > 0)
      .map(({ organization, count }) => ({
        kind: 'organization' as const,
        name: organization.name,
        href: `/organizations/${organization.slug}`,
        meta: `在籍記録 ${count}人`,
      })),
  ];

  return (
    <main className="jbaListB-page">
      <SiteHeader />

      <div className="jbaListB-main">
        <section className="jbaListB-section jbaListB-notFound">
          <div>
            <p className="jbaListB-eyebrow">404 Not Found</p>
            <h1 className="jbaListB-h1">このページは見つかりませんでした。</h1>
            <p className="jbaListB-lede">
              URLが変更・削除されたか、リンク切れの可能性があります。下の検索、またはサイト内のリンクからお探しください。
            </p>
          </div>

          <TopSearch entries={searchEntries} />

          <div className="jbaListB-sectionLinks">
            <a href="/" className="jbaListB-textLink">トップへ戻る <ArrowRight size={16} /></a>
            <a href="/players" className="jbaListB-textLink">選手一覧を見る <ArrowRight size={16} /></a>
            <a href="/organizations" className="jbaListB-textLink">組織一覧を見る <ArrowRight size={16} /></a>
          </div>
        </section>
      </div>

      <SiteFooter />
    </main>
  );
}
