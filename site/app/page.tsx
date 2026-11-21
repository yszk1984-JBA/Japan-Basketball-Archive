/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import { ArrowRight, Database, School, ShieldCheck } from 'lucide-react';
import type { Metadata } from 'next';
import { getCurrentCareer, getHomepagePlayers, getOrganizationById, getOrganizationPlayers, getPrimaryCareer, organizations, organizationSlugFor, playerContext, players, sources } from './public-data';
import { TopSearch, type TopSearchEntry } from './TopSearch';
import { BrandMark, JsonLd, SiteFooter, SiteHeader, websiteJsonLd } from './seo';
import { ALL_STAR_2026 } from './all-star';
import { CLUB_COLORS, clubColor } from './club-colors';
import { buildRanking } from './rankings/ranking-data';
import { buildRouteRanking, ROUTE_PATH, ROUTE_TITLE } from './rankings/route-data';

export const metadata: Metadata = {
  alternates: { canonical: '/' },
};

export default function Home() {
  const homepagePlayers = getHomepagePlayers();
  const organizationCount = new Set(
    players.flatMap((player) => player.careers.map((career) => career.organization).filter(Boolean)),
  ).size;
  const careerCount = players.reduce((total, player) => total + player.careers.length, 0);

  const clubs = Object.entries(CLUB_COLORS)
    .map(([organizationId, meta]) => {
      const organization = getOrganizationById(organizationId);
      const slug = organizationSlugFor(organizationId);
      if (!organization || !slug) return null;
      return { organizationId, color: meta.color, league: meta.league, name: organization.name, slug };
    })
    .filter((club): club is NonNullable<typeof club> => club !== null);
  const premierClubs = clubs.filter((club) => club.league === 'PREMIER');
  const bOneClubs = clubs.filter((club) => club.league === 'B.ONE');

  // トップページ用のランキング・ティーザー（出身高校・出身大学・高校→大学ルート、各上位3件）。
  // 集計ロジック本体は/rankingsと同じbuildRanking/buildRouteRankingを再利用している。
  const topHighSchools = buildRanking('high-school')
    .slice(0, 3)
    .map((row) => `${row.rank}位 ${row.name}（${row.active}人）`)
    .join('・');
  const topUniversities = buildRanking('university')
    .slice(0, 3)
    .map((row) => `${row.rank}位 ${row.name}（${row.active}人）`)
    .join('・');
  const topRoutes = buildRouteRanking()
    .slice(0, 3)
    .map((row) => `${row.rank}位 ${row.highSchool.name}→${row.university.name}（${row.players.length}人）`)
    .join('・');

  const allStarPlayers = ALL_STAR_2026.entries
    .map((entry) => {
      const player = players.find((candidate) => candidate.id === entry.playerId);
      if (!player) return null;
      const career = getPrimaryCareer(player);
      return { entry, player, orgId: career?.organizationId };
    })
    .filter((row): row is NonNullable<typeof row> => row !== null);

  // トップページの検索候補（選手・組織）。サーバー側で作り、検索ボックスに渡す。
  const searchEntries: TopSearchEntry[] = [
    ...players.map((player) => ({
      kind: 'player' as const,
      name: player.name,
      href: `/players/${player.slug}`,
      meta: getPrimaryCareer(player)?.organization ?? '',
      // 英字表記（JBA公式メンバー表などの英語表記）が確認できている選手は、ローマ字検索にも対応させる。
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
      <JsonLd data={websiteJsonLd()} />
      <SiteHeader />

      <div className="jbaListB-main">
        <section className="jbaListB-hero">
          <div>
            <p className="jbaListB-eyebrow">日本バスケットボールの記録</p>
            <h1 className="jbaListB-heroTitle">選手と所属を、出典からたどる。</h1>
            <p className="jbaListB-heroLead">
              すべての経歴に出典つき。承認済みのデータと確認中のデータを区別して表示しています。
            </p>
            <TopSearch entries={searchEntries} />
          </div>
          <BrandMark size={108} className="jbaListB-heroBadge" />
        </section>

        <section className="jbaListB-stats" aria-label="収録状況">
          <div className="jbaListB-statItem">
            <span className="jbaListB-statValue">{players.length.toLocaleString('ja-JP')}</span>
            <span className="jbaListB-statLabel">人物</span>
          </div>
          <div className="jbaListB-statItem">
            <span className="jbaListB-statValue">{organizationCount.toLocaleString('ja-JP')}</span>
            <span className="jbaListB-statLabel">掲載組織</span>
          </div>
          <div className="jbaListB-statItem">
            <span className="jbaListB-statValue">{sources.length.toLocaleString('ja-JP')}</span>
            <span className="jbaListB-statLabel">参照資料</span>
          </div>
          <div className="jbaListB-statItem">
            <span className="jbaListB-statValue">{careerCount.toLocaleString('ja-JP')}</span>
            <span className="jbaListB-statLabel">経歴</span>
          </div>
        </section>

        <section className="jbaListB-featuredSection">
          <div className="jbaListB-sectionHeading">
            <div>
              <p className="jbaListB-eyebrow">Featured players</p>
              <h2 className="jbaListB-sectionTitle">注目選手</h2>
            </div>
            <div className="jbaListB-sectionLinks">
              <a href="/players" className="jbaListB-textLink">選手一覧を見る <ArrowRight size={16} /></a>
              <a href="/organizations" className="jbaListB-textLink">組織一覧を見る <ArrowRight size={16} /></a>
            </div>
          </div>
          <div className="jbaListB-spotlightGrid">
            {homepagePlayers.map((player, index) => {
              const orgId = getCurrentCareer(player)?.organizationId ?? getPrimaryCareer(player)?.organizationId;
              return (
                <a href={`/players/${player.slug}`} className="jbaListB-spotlightCard" key={player.id}>
                  <span className="jbaListB-spotlightIndex">{String(index + 1).padStart(2, '0')}</span>
                  <span className="jbaListB-spotlightBody">
                    <span className="jbaListB-spotlightName">{player.name}</span>
                    <p className="jbaListB-spotlightMeta">
                      {clubColor(orgId) ? (
                        <span className="jbaListB-clubDot" style={{ background: clubColor(orgId) }} aria-hidden="true" />
                      ) : null}
                      {playerContext(player)}
                    </p>
                  </span>
                </a>
              );
            })}
          </div>
        </section>

        <section className="jbaListB-featuredSection">
          <div className="jbaListB-sectionHeading">
            <div>
              <p className="jbaListB-eyebrow">Browse by club</p>
              <h2 className="jbaListB-sectionTitle">クラブで探す</h2>
            </div>
            <div className="jbaListB-sectionLinks">
              <a href="/organizations" className="jbaListB-textLink">組織一覧を見る <ArrowRight size={16} /></a>
            </div>
          </div>
          <p className="jbaListB-lede">選手名が分からなくても、所属クラブから経歴をたどれます。B.LEAGUE全{clubs.length}クラブを掲載。</p>
          <div className="jbaListB-clubGroup">
            <p className="jbaListB-clubGroupLabel">B.PREMIER（{premierClubs.length}クラブ）</p>
            <div className="jbaListB-clubGrid">
              {premierClubs.map((club) => (
                <a href={`/organizations/${club.slug}`} className="jbaListB-clubCard" key={club.organizationId}>
                  <span className="jbaListB-clubCardDot" style={{ background: club.color }} aria-hidden="true" />
                  <span className="jbaListB-clubCardName">{club.name}</span>
                </a>
              ))}
            </div>
          </div>
          <div className="jbaListB-clubGroup">
            <p className="jbaListB-clubGroupLabel">B.ONE（{bOneClubs.length}クラブ）</p>
            <div className="jbaListB-clubGrid">
              {bOneClubs.map((club) => (
                <a href={`/organizations/${club.slug}`} className="jbaListB-clubCard" key={club.organizationId}>
                  <span className="jbaListB-clubCardDot" style={{ background: club.color }} aria-hidden="true" />
                  <span className="jbaListB-clubCardName">{club.name}</span>
                </a>
              ))}
            </div>
          </div>
        </section>

        <section className="jbaListB-featuredSection">
          <div className="jbaListB-sectionHeading">
            <div>
              <p className="jbaListB-eyebrow">Ranking</p>
              <h2 className="jbaListB-sectionTitle">ランキングで探す</h2>
            </div>
            <div className="jbaListB-sectionLinks">
              <a href="/rankings" className="jbaListB-textLink">ランキング一覧を見る <ArrowRight size={16} /></a>
            </div>
          </div>
          <p className="jbaListB-lede">出身校や進学ルートなど、切り口別のランキングからも選手を探せます。</p>
          <div className="jbaListB-table">
            <a href="/rankings/high-school" className="jbaListB-row jbaListB-rankIndexGrid">
              <div className="jbaListB-rowName">B.LEAGUE選手の出身高校ランキング</div>
              <div className="jbaListB-rowMuted">{topHighSchools}</div>
            </a>
            <a href="/rankings/university" className="jbaListB-row jbaListB-rankIndexGrid">
              <div className="jbaListB-rowName">B.LEAGUE選手の出身大学ランキング</div>
              <div className="jbaListB-rowMuted">{topUniversities}</div>
            </a>
            <a href={ROUTE_PATH} className="jbaListB-row jbaListB-rankIndexGrid">
              <div className="jbaListB-rowName">{ROUTE_TITLE}</div>
              <div className="jbaListB-rowMuted">{topRoutes}</div>
            </a>
          </div>
        </section>

        {allStarPlayers.length > 0 && (
          <section className="jbaListB-featuredSection">
            <div className="jbaListB-sectionHeading">
              <div>
                <p className="jbaListB-eyebrow">{ALL_STAR_2026.label}</p>
                <h2 className="jbaListB-sectionTitle">オールスター出場選手</h2>
              </div>
            </div>
            <p className="jbaListB-lede">
              {ALL_STAR_2026.period}・{ALL_STAR_2026.venue}開催。出場選手のうち当サイトに掲載済みの{allStarPlayers.length}
              人を掲載しています（出典：
              <a
                href={ALL_STAR_2026.sourceUrl}
                target="_blank"
                rel="noopener noreferrer"
                style={{ color: '#1D5FD6', fontWeight: 700, textDecoration: 'none' }}
              >
                {ALL_STAR_2026.sourceLabel}
              </a>
              ）。
            </p>
            <div className="jbaListB-spotlightGrid">
              {allStarPlayers.map(({ entry, player, orgId }, index) => (
                <a href={`/players/${player.slug}`} className="jbaListB-spotlightCard" key={player.id}>
                  <span className="jbaListB-spotlightIndex">{String(index + 1).padStart(2, '0')}</span>
                  <span className="jbaListB-spotlightBody">
                    <span className="jbaListB-spotlightName">{player.name}</span>
                    <p className="jbaListB-spotlightMeta">
                      {clubColor(orgId) ? (
                        <span className="jbaListB-clubDot" style={{ background: clubColor(orgId) }} aria-hidden="true" />
                      ) : null}
                      {entry.team}
                      {entry.captain ? '・キャプテン' : ''}
                    </p>
                  </span>
                </a>
              ))}
            </div>
          </section>
        )}

        <section className="jbaListB-principles">
          <div className="jbaListB-principleCard">
            <Database size={20} />
            <h3 className="jbaListB-principleTitle">つながる記録</h3>
            <p className="jbaListB-principleText">人物、学校、経歴をIDで結びます。</p>
          </div>
          <div className="jbaListB-principleCard">
            <ShieldCheck size={20} />
            <h3 className="jbaListB-principleTitle">出典を表示</h3>
            <p className="jbaListB-principleText">掲載した事実から確認元へ移動できます。</p>
          </div>
          <div className="jbaListB-principleCard">
            <School size={20} />
            <h3 className="jbaListB-principleTitle">育成経路</h3>
            <p className="jbaListB-principleText">学校やクラブを時系列でたどる設計です。</p>
          </div>
        </section>
      </div>

      <SiteFooter />
    </main>
  );
}
