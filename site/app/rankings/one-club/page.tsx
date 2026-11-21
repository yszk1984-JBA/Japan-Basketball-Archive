/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import type { Metadata } from 'next';
import { baseOpenGraph, breadcrumbJsonLd, JsonLd, SiteBreadcrumb, SiteFooter, SiteHeader, siteUrl } from '../../seo';
import { ShareButtons } from '../../ShareButtons';
import { rankingAsOf } from '../ranking-data';
import { buildOneClubRanking, ONE_CLUB_PATH, ONE_CLUB_TITLE, oneClubPlayerCount } from '../one-club-data';

const description =
  '2016-17シーズンのB.LEAGUE開幕から現在まで、同じクラブでプレーを続けている選手を、クラブ別に掲載しています。本サイトに登録済みの選手から抽出し、各選手の経歴は出典つきで確認できます。';

export const metadata: Metadata = {
  title: ONE_CLUB_TITLE,
  description,
  alternates: { canonical: ONE_CLUB_PATH },
  openGraph: { ...baseOpenGraph, title: ONE_CLUB_TITLE, description, url: ONE_CLUB_PATH },
};

function formatDate(isoDate: string): string {
  const [year, month, day] = isoDate.slice(0, 10).split('-');
  return `${year}年${Number(month)}月${Number(day)}日`;
}

export default function OneClubRankingPage() {
  const rows = buildOneClubRanking();
  const total = oneClubPlayerCount();
  const leaders = rows.filter((row) => row.rank === 1);
  const seasons = new Date(rankingAsOf()).getFullYear() - 2016 + (new Date(rankingAsOf()).getMonth() >= 8 ? 1 : 0);
  const lead = leaders.length
    ? `最も多いのは${leaders.map((row) => row.clubName).join('・')}の${leaders[0].players.length}人です。`
    : '';
  const shareText = leaders.length
    ? `${ONE_CLUB_TITLE}は${total}人｜最多は${leaders.map((row) => row.clubName).join('・')}（${leaders[0].players.length}人）`
    : ONE_CLUB_TITLE;

  return (
    <main className="jbaListB-page">
      <JsonLd
        data={{
          '@context': 'https://schema.org',
          '@graph': [
            breadcrumbJsonLd([
              { name: 'ホーム', path: '/' },
              { name: 'ランキング', path: '/rankings' },
              { name: ONE_CLUB_TITLE, path: ONE_CLUB_PATH },
            ]),
            {
              '@type': 'ItemList',
              name: ONE_CLUB_TITLE,
              numberOfItems: total,
              itemListElement: rows
                .flatMap((row) => row.players)
                .map((player, index) => ({
                  '@type': 'ListItem',
                  position: index + 1,
                  name: player.name,
                  url: `${siteUrl}/players/${player.slug}`,
                })),
            },
          ],
        }}
      />
      <SiteHeader active="rankings" />

      <SiteBreadcrumb crumbs={[{ label: 'ランキング', href: '/rankings' }, { label: '開幕から同じクラブ一筋' }]} />

      <div className="jbaListB-main">
        <div>
          <p className="jbaListB-eyebrow">Ranking</p>
          <h1 className="jbaListB-h1">{ONE_CLUB_TITLE}</h1>
        </div>

        <div>
          <p className="jbaListB-lede">
            2016-17シーズンのB.LEAGUE開幕から現在まで、{seasons}シーズン続けて同じクラブに所属している選手は、本サイトに登録済みの選手のうち{total}人です。{lead}
          </p>
          <ShareButtons url={`${siteUrl}${ONE_CLUB_PATH}`} text={shareText} hashtags={['Bリーグ']} />
          <p className="jbaListB-rankOther">
            <a href="/rankings">ほかのランキングを見る →</a>
          </p>
        </div>

        <div className="jbaListB-table">
          <div className="jbaListB-tableHead jbaListB-routeGrid">
            <div>順位</div>
            <div>クラブ</div>
            <div className="jbaListB-rankNum">人数</div>
            <div>選手</div>
          </div>
          {rows.map((row) => (
            <div key={row.clubId} className="jbaListB-row jbaListB-routeGrid">
              <div className="jbaListB-rankPos">{row.rank}</div>
              <div className="jbaListB-routeName">
                {row.clubSlug ? <a href={`/organizations/${row.clubSlug}`}>{row.clubName}</a> : row.clubName}
              </div>
              <div className="jbaListB-rankNum">
                <strong>{row.players.length}</strong>人
              </div>
              <div className="jbaListB-routePlayers">
                {row.players.map((player, index) => (
                  <span key={player.id}>
                    {index > 0 ? '、' : ''}
                    <a href={`/players/${player.slug}`}>{player.name}</a>
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className="jbaListB-rankNotes">
          <p>集計の前提（{formatDate(rankingAsOf())}時点の登録データ）</p>
          <ul>
            <li>本サイトに登録済み（確認済みのデータ）の選手だけを数えています。登録されていない選手は含まれないため、実際の人数より少ない場合があります。</li>
            <li>2016-17シーズン（B.LEAGUE開幕）から所属が続いていて、所属の終了が記録されていない選手が対象です。</li>
            <li>この期間に、期限付き移籍を含めて別のクラブへの所属が記録されている選手は含めていません。</li>
            <li>本サイトのクラブ所属の記録は、主にB.LEAGUE公式の所属履歴（2016-17シーズン以降）にもとづいています。B.LEAGUE開幕より前の在籍年数は含みません。</li>
            <li>改称したクラブは、現在の名称で掲載しています。</li>
          </ul>
        </div>
      </div>

      <SiteFooter />
    </main>
  );
}
