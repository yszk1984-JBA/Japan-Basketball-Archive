/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import type { Metadata } from 'next';
import { baseOpenGraph, breadcrumbJsonLd, JsonLd, SiteBreadcrumb, SiteFooter, SiteHeader, siteUrl } from '../seo';
import { ShareButtons } from '../ShareButtons';
import { rankingAsOf } from './ranking-data';
import {
  buildExtraRanking,
  EXTRA_RANKING_IDS,
  type ExtraRankingId,
  type RankingLink,
} from './extra-rankings';

export function extraRankingMetadata(id: ExtraRankingId): Metadata {
  const { title, description, path } = buildExtraRanking(id);
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

function LinkText({ link }: { link: RankingLink }) {
  return link.href ? <a href={link.href}>{link.label}</a> : <>{link.label}</>;
}

export function ExtraRankingPage({ id }: { id: ExtraRankingId }) {
  const ranking = buildExtraRanking(id);
  const related = EXTRA_RANKING_IDS.filter((other) => other !== id).map((other) => buildExtraRanking(other));

  return (
    <main className="jbaListB-page">
      <JsonLd
        data={{
          '@context': 'https://schema.org',
          '@graph': [
            breadcrumbJsonLd([
              { name: 'ホーム', path: '/' },
              { name: 'ランキング', path: '/rankings' },
              { name: ranking.title, path: ranking.path },
            ]),
            {
              '@type': 'ItemList',
              name: ranking.title,
              numberOfItems: ranking.rows.length,
              itemListElement: ranking.rows.map((row, index) => ({
                '@type': 'ListItem',
                position: index + 1,
                name: row.sub ? `${row.name.label}（${row.sub.label}）` : row.name.label,
                ...(row.name.href ? { url: `${siteUrl}${row.name.href}` } : {}),
              })),
            },
          ],
        }}
      />
      <SiteHeader active="rankings" />

      <SiteBreadcrumb crumbs={[{ label: 'ランキング', href: '/rankings' }, { label: ranking.crumb }]} />

      <div className="jbaListB-main">
        <div>
          <p className="jbaListB-eyebrow">Ranking</p>
          <h1 className="jbaListB-h1">{ranking.title}</h1>
        </div>

        <div>
          <p className="jbaListB-lede">{ranking.lede}</p>
          <ShareButtons url={`${siteUrl}${ranking.path}`} text={ranking.share} hashtags={['Bリーグ']} />
          <p className="jbaListB-rankOther">
            <a href="/rankings">ほかのランキングを見る →</a>
          </p>
        </div>

        {ranking.points.length ? (
          <div className="jbaListB-routePoints">
            <p>注目ポイント</p>
            <ul>
              {ranking.points.map((point) => (
                <li key={point}>{point}</li>
              ))}
            </ul>
          </div>
        ) : null}

        <div className="jbaListB-table">
          <div className="jbaListB-tableHead jbaListB-routeGrid">
            <div>順位</div>
            <div>{ranking.headers.name}</div>
            <div className="jbaListB-rankNum">{ranking.headers.count}</div>
            <div>{ranking.headers.items}</div>
          </div>
          {ranking.rows.map((row) => (
            <div key={row.key} className="jbaListB-row jbaListB-routeGrid">
              <div className="jbaListB-rankPos">{row.rank}</div>
              <div className="jbaListB-routeName">
                <LinkText link={row.name} />
                {row.sub ? (
                  <span className="jbaListB-rowMuted" style={{ display: 'block', fontWeight: 400 }}>
                    <LinkText link={row.sub} />
                  </span>
                ) : null}
              </div>
              <div className="jbaListB-rankNum">
                <strong>{row.count}</strong>
                {row.unit}
              </div>
              <div className="jbaListB-routePlayers">
                {row.items.map((item, index) => (
                  <span key={`${item.label}-${index}`}>
                    {index > 0 ? '、' : ''}
                    <LinkText link={item} />
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className="jbaListB-rankNotes">
          <p>集計の前提（{formatDate(rankingAsOf())}時点の登録データ）</p>
          <ul>
            {ranking.notes.map((note) => (
              <li key={note}>{note}</li>
            ))}
          </ul>
        </div>

        <div className="jbaListB-routePoints">
          <p>関連するランキング</p>
          <ul>
            {related.map((other) => (
              <li key={other.id}>
                <a href={other.path}>{other.title}</a>
              </li>
            ))}
            <li>
              <a href="/rankings/high-school">B.LEAGUE選手の出身高校ランキング</a>
            </li>
            <li>
              <a href="/rankings/university">B.LEAGUE選手の出身大学ランキング</a>
            </li>
          </ul>
        </div>
      </div>

      <SiteFooter />
    </main>
  );
}
