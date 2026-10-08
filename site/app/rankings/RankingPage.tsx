/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import type { Metadata } from 'next';
import { baseOpenGraph, breadcrumbJsonLd, JsonLd, SiteBreadcrumb, SiteFooter, SiteHeader, siteUrl } from '../seo';
import { activeTopLeaguePlayerCount, buildRanking, RANKING_META, rankingAsOf, type RankingKind } from './ranking-data';

function texts(kind: RankingKind) {
  const { label } = RANKING_META[kind];
  const title = `B.LEAGUE選手の出身${label}ランキング`;
  const description = `現在B.PREMIER・B.ONEでプレーする選手の出身${label}を、人数の多い順に掲載しています。本サイトに登録済みの選手から集計し、各選手の経歴は出典つきで確認できます。`;
  return { title, description };
}

export function rankingMetadata(kind: RankingKind): Metadata {
  const { title, description } = texts(kind);
  const { path } = RANKING_META[kind];
  return {
    title,
    description,
    alternates: { canonical: path },
    openGraph: { ...baseOpenGraph, title, description, url: path },
  };
}

function formatDate(isoDate: string): string {
  const [year, month, day] = isoDate.slice(0, 10).split('-');
  return `${year}年${Number(month)}月${Number(day)}日`;
}

export function RankingPage({ kind }: { kind: RankingKind }) {
  const { label, path } = RANKING_META[kind];
  const { title } = texts(kind);
  const rows = buildRanking(kind);
  const otherKind: RankingKind = kind === 'high-school' ? 'university' : 'high-school';
  const crumbs = [
    { name: 'ホーム', path: '/' },
    { name: 'ランキング', path: '/rankings' },
    { name: title, path },
  ];

  return (
    <main className="jbaListB-page">
      <JsonLd
        data={{
          '@context': 'https://schema.org',
          '@graph': [
            breadcrumbJsonLd(crumbs),
            {
              '@type': 'ItemList',
              name: title,
              itemListOrder: 'https://schema.org/ItemListOrderDescending',
              numberOfItems: rows.length,
              itemListElement: rows.slice(0, 50).map((row, index) => ({
                '@type': 'ListItem',
                position: index + 1,
                name: row.name,
                ...(row.slug ? { url: `${siteUrl}/organizations/${row.slug}` } : {}),
              })),
            },
          ],
        }}
      />
      <SiteHeader active="rankings" />

      <SiteBreadcrumb crumbs={[{ label: 'ランキング', href: '/rankings' }, { label: `出身${label}` }]} />

      <div className="jbaListB-main">
        <div>
          <p className="jbaListB-eyebrow">Ranking</p>
          <h1 className="jbaListB-h1">{title}</h1>
        </div>

        <div>
          <p className="jbaListB-lede">
            現在B.PREMIER・B.ONEのクラブに所属している選手（本サイトに登録済みの{activeTopLeaguePlayerCount()}
            人）が、どの{label}の出身かを数えました。{rows.length}校を、現役選手の多い順に掲載しています。
          </p>
          <p className="jbaListB-rankOther">
            <a href={RANKING_META[otherKind].path}>出身{RANKING_META[otherKind].label}ランキングを見る →</a>
          </p>
        </div>

        <div className="jbaListB-table">
          <div className="jbaListB-tableHead jbaListB-rankGrid">
            <div>順位</div>
            <div>{label}</div>
            <div className="jbaListB-rankNum">現役選手</div>
            <div className="jbaListB-rankNum">登録出身者</div>
          </div>
          {rows.map((row) => {
            const cells = (
              <>
                <div className="jbaListB-rankPos">{row.rank}</div>
                <div>
                  <div className="jbaListB-rowName">{row.name}</div>
                  {row.currentNameNote ? <div className="jbaListB-rankCurrent">{row.currentNameNote}</div> : null}
                </div>
                <div className="jbaListB-rankNum">
                  <strong>{row.active}</strong>人
                </div>
                <div className="jbaListB-rankNum jbaListB-rowMuted">{row.total}人</div>
              </>
            );
            return row.slug ? (
              <a href={`/organizations/${row.slug}`} key={row.organizationId} className="jbaListB-row jbaListB-rankGrid">
                {cells}
              </a>
            ) : (
              <div key={row.organizationId} className="jbaListB-row jbaListB-rankGrid">
                {cells}
              </div>
            );
          })}
        </div>

        <div className="jbaListB-rankNotes">
          <p>集計の前提（{formatDate(rankingAsOf())}時点の登録データ）</p>
          <ul>
            <li>本サイトに登録済み（確認済みのデータ）の選手だけを数えています。登録されていない選手は含まれないため、実際の人数より少ない場合があります。</li>
            <li>「現役選手」は、現在の所属が2026-27シーズンのB.PREMIER・B.ONEのクラブである選手です。</li>
            <li>「登録出身者」は、その{label}の在籍記録がある選手の人数で、引退した選手やB3・海外などでプレーする選手も含みます。</li>
            <li>改称や統合をした{label}は、資料に書かれた当時の名称で掲載し、現在の名称を書き添えています。</li>
          </ul>
        </div>
      </div>

      <SiteFooter />
    </main>
  );
}
