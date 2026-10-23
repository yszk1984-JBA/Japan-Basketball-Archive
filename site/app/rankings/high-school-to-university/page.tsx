/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import type { Metadata } from 'next';
import { baseOpenGraph, breadcrumbJsonLd, JsonLd, SiteBreadcrumb, SiteFooter, SiteHeader, siteUrl } from '../../seo';
import { ShareButtons } from '../../ShareButtons';
import { rankingAsOf } from '../ranking-data';
import {
  buildRouteRanking,
  mostSpread,
  ROUTE_MIN_PLAYERS,
  ROUTE_PATH,
  ROUTE_TITLE,
  routePopulation,
  type RouteRow,
  type RouteSchool,
} from '../route-data';

const description =
  'B.LEAGUE選手がどの高校からどの大学へ進んだのか、「高校→大学」の組み合わせを人数の多い順に掲載しています。本サイトに登録済みの選手から集計し、各選手の経歴は出典つきで確認できます。';

export const metadata: Metadata = {
  title: ROUTE_TITLE,
  description,
  alternates: { canonical: ROUTE_PATH },
  openGraph: { ...baseOpenGraph, title: ROUTE_TITLE, description, url: ROUTE_PATH },
};

function formatDate(isoDate: string): string {
  const [year, month, day] = isoDate.slice(0, 10).split('-');
  return `${year}年${Number(month)}月${Number(day)}日`;
}

function routeLabel(row: RouteRow): string {
  return `${row.highSchool.name}→${row.university.name}`;
}

function SchoolLink({ school }: { school: RouteSchool }) {
  return (
    <span>
      {school.slug ? <a href={`/organizations/${school.slug}`}>{school.name}</a> : school.name}
      {school.currentNameNote ? <span className="jbaListB-rankCurrent">（{school.currentNameNote}）</span> : null}
    </span>
  );
}

export default function RouteRankingPage() {
  const rows = buildRouteRanking();
  const population = routePopulation();
  const leaders = rows.filter((row) => row.rank === 1);
  const highSchoolSpread = mostSpread('hs');
  const universitySpread = mostSpread('univ');
  const lead = leaders.length
    ? `最も多いルートは${leaders.map(routeLabel).join('、')}の${leaders[0].players.length}人です。`
    : '';
  const shareText = leaders.length
    ? `${ROUTE_TITLE}｜1位は${leaders.map(routeLabel).join('・')}（${leaders[0].players.length}人）`
    : ROUTE_TITLE;

  return (
    <main className="jbaListB-page">
      <JsonLd
        data={{
          '@context': 'https://schema.org',
          '@graph': [
            breadcrumbJsonLd([
              { name: 'ホーム', path: '/' },
              { name: 'ランキング', path: '/rankings' },
              { name: ROUTE_TITLE, path: ROUTE_PATH },
            ]),
            {
              '@type': 'ItemList',
              name: ROUTE_TITLE,
              itemListOrder: 'https://schema.org/ItemListOrderDescending',
              numberOfItems: rows.length,
              itemListElement: rows.slice(0, 50).map((row, index) => ({
                '@type': 'ListItem',
                position: index + 1,
                name: routeLabel(row),
              })),
            },
          ],
        }}
      />
      <SiteHeader active="rankings" />

      <SiteBreadcrumb crumbs={[{ label: 'ランキング', href: '/rankings' }, { label: '高校→大学の進学ルート' }]} />

      <div className="jbaListB-main">
        <div>
          <p className="jbaListB-eyebrow">Ranking</p>
          <h1 className="jbaListB-h1">{ROUTE_TITLE}</h1>
        </div>

        <div>
          <p className="jbaListB-lede">
            本サイトに登録済みの選手のうち、高校と大学の両方の在籍記録がある{population}人について、「どの高校からどの大学へ」の組み合わせを数えました。{lead}
          </p>
          <ShareButtons url={`${siteUrl}${ROUTE_PATH}`} text={shareText} hashtags={['Bリーグ']} />
          <p className="jbaListB-rankOther">
            <a href="/rankings/high-school">出身高校ランキング →</a>　<a href="/rankings/university">出身大学ランキング →</a>
          </p>
        </div>

        {highSchoolSpread || universitySpread ? (
          <div className="jbaListB-routePoints">
            <p>注目ポイント</p>
            <ul>
              {highSchoolSpread ? (
                <li>
                  進学先が最も多い高校は<SchoolLink school={highSchoolSpread.school} />
                  で、登録選手{highSchoolSpread.players}人の進学先は{highSchoolSpread.destinations}大学に分かれています。
                </li>
              ) : null}
              {universitySpread ? (
                <li>
                  出身高校が最も多い大学は<SchoolLink school={universitySpread.school} />
                  で、登録選手{universitySpread.players}人が{universitySpread.destinations}校から進学しています。
                </li>
              ) : null}
            </ul>
          </div>
        ) : null}

        <div className="jbaListB-table">
          <div className="jbaListB-tableHead jbaListB-routeGrid">
            <div>順位</div>
            <div>高校 → 大学</div>
            <div className="jbaListB-rankNum">人数</div>
            <div>選手</div>
          </div>
          {rows.map((row) => (
            <div key={`${row.highSchool.id}>${row.university.id}`} className="jbaListB-row jbaListB-routeGrid">
              <div className="jbaListB-rankPos">{row.rank}</div>
              <div className="jbaListB-routeName">
                <SchoolLink school={row.highSchool} />
                <span className="jbaListB-routeArrow" aria-label="から">→</span>
                <SchoolLink school={row.university} />
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
            <li>現役・引退を問わず、高校と大学の両方の在籍記録がある選手が対象です。高校から直接プロや海外へ進んだ選手は含まれません。</li>
            <li>{ROUTE_MIN_PLAYERS}人以上の組み合わせだけを掲載しています。</li>
            <li>高校や大学が複数ある選手（転校など）は、それぞれの組み合わせで数えています。</li>
            <li>改称や統合をした学校は、資料に書かれた当時の名称で掲載しています。</li>
          </ul>
        </div>
      </div>

      <SiteFooter />
    </main>
  );
}
