/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import { ArrowRight, Database, School, ShieldCheck } from 'lucide-react';
import type { Metadata } from 'next';
import { getHomepagePlayers, players, sources, type PublicPlayer } from './public-data';
import { JsonLd, SiteFooter, SiteHeader, websiteJsonLd } from './seo';
import { ALL_STAR_2026 } from './all-star';
import { clubColor } from './club-colors';

export const metadata: Metadata = {
  alternates: { canonical: '/' },
};

// オールスター選手カードの「現在の所属」を選ぶ。経歴データは必ずしも年代順の末尾が
// 最新とは限らない（例：外国籍選手で出身大学の経歴が末尾に入っているケース）ため、
// 終了年が未確定（endYear: null）で開始年が確認できている経歴のうち、開始年が
// 最も新しいものを優先する。該当がなければ選手一覧と同じ「末尾の経歴」にフォールバックする。
function currentCareer(player: PublicPlayer) {
  const ongoing = player.careers.filter(
    (career): career is typeof career & { startYear: number } =>
      typeof career.startYear === 'number' && career.endYear === null,
  );
  if (ongoing.length > 0) {
    return ongoing.reduce((latest, career) => (career.startYear > latest.startYear ? career : latest));
  }
  return player.careers[player.careers.length - 1];
}

export default function Home() {
  const homepagePlayers = getHomepagePlayers();
  const organizationCount = new Set(
    players.flatMap((player) => player.careers.map((career) => career.organization).filter(Boolean)),
  ).size;

  const allStarPlayers = ALL_STAR_2026.entries
    .map((entry) => {
      const player = players.find((candidate) => candidate.id === entry.playerId);
      if (!player) return null;
      const career = currentCareer(player);
      return { entry, player, org: career?.organization ?? null, orgId: career?.organizationId };
    })
    .filter((row): row is NonNullable<typeof row> => row !== null);

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
              承認済みMaster Dataと、公開画面の検証に使う確認中データを区別して掲載しています。
            </p>
          </div>
          <div className="jbaListB-heroBadge" aria-hidden="true">JB</div>
        </section>

        <section className="jbaListB-stats" aria-label="収録状況">
          <div className="jbaListB-statItem">
            <span className="jbaListB-statValue">{players.length}</span>
            <span className="jbaListB-statLabel">人物</span>
          </div>
          <div className="jbaListB-statItem">
            <span className="jbaListB-statValue">{organizationCount}</span>
            <span className="jbaListB-statLabel">掲載組織</span>
          </div>
          <div className="jbaListB-statItem">
            <span className="jbaListB-statValue">{sources.length}</span>
            <span className="jbaListB-statLabel">参照資料</span>
          </div>
          <div className="jbaListB-statItem">
            <span className="jbaListB-statValue">複数</span>
            <span className="jbaListB-statLabel">対象年度</span>
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
          <div className="jbaListB-cardGrid">
            {homepagePlayers.map((player, index) => (
              <a href={`/players/${player.slug}`} className="jbaListB-playerCard" key={player.id}>
                <div>
                  <span className="jbaListB-cardIndex">{String(index + 1).padStart(2, '0')}</span>
                  <p className="jbaListB-cardMeta">{player.cardContext}</p>
                  <h3 className="jbaListB-cardName">{player.name}</h3>
                  <span className={`jbaListB-pill ${player.dataStatus === 'master' ? 'jbaListB-statusMaster' : 'jbaListB-statusCandidate'}`}>
                    {player.dataStatus === 'master' ? 'Master・承認済み' : '候補データ・正式承認前'}
                  </span>
                </div>
                <ArrowRight size={20} />
              </a>
            ))}
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
            <div className="jbaListB-cardGrid">
              {allStarPlayers.map(({ entry, player, org, orgId }, index) => (
                <a href={`/players/${player.slug}`} className="jbaListB-playerCard" key={player.id}>
                  <div>
                    <span className="jbaListB-cardIndex">{String(index + 1).padStart(2, '0')}</span>
                    <p className="jbaListB-cardMeta">
                      {entry.team}
                      {entry.captain ? '・キャプテン' : ''}
                    </p>
                    <h3 className="jbaListB-cardName">{player.name}</h3>
                    <span className="jbaListB-rowMuted">
                      {clubColor(orgId) ? (
                        <span className="jbaListB-clubDot" style={{ background: clubColor(orgId) }} aria-hidden="true" />
                      ) : null}
                      {org ?? '所属未確認'}
                    </span>
                  </div>
                  <ArrowRight size={20} />
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
