/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import type { Metadata } from 'next';
import { baseOpenGraph, SiteBreadcrumb, SiteFooter, SiteHeader } from '../seo';
import { buildRanking, RANKING_META, type RankingKind } from './ranking-data';

const title = 'ランキング';
const description = 'B.LEAGUE（B.PREMIER・B.ONE）でプレーする選手の出身高校・出身大学のランキングです。';

export const metadata: Metadata = {
  title,
  description,
  alternates: { canonical: '/rankings' },
  openGraph: { ...baseOpenGraph, title, description, url: '/rankings' },
};

const KINDS: readonly RankingKind[] = ['high-school', 'university'];

export default function RankingsIndexPage() {
  return (
    <main className="jbaListB-page">
      <SiteHeader active="rankings" />

      <SiteBreadcrumb crumbs={[{ label: 'ランキング' }]} />

      <div className="jbaListB-main">
        <div>
          <p className="jbaListB-eyebrow">Ranking</p>
          <h1 className="jbaListB-h1">ランキング</h1>
        </div>

        <p className="jbaListB-lede">{description}</p>

        <div className="jbaListB-table">
          {KINDS.map((kind) => {
            const { label, path } = RANKING_META[kind];
            const top = buildRanking(kind).slice(0, 3);
            return (
              <a href={path} key={kind} className="jbaListB-row jbaListB-rankIndexGrid">
                <div className="jbaListB-rowName">B.LEAGUE選手の出身{label}ランキング</div>
                <div className="jbaListB-rowMuted">
                  {top.map((row) => `${row.rank}位 ${row.name}（${row.active}人）`).join('・')}
                </div>
              </a>
            );
          })}
        </div>
      </div>

      <SiteFooter />
    </main>
  );
}
