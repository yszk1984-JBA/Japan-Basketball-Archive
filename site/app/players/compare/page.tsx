/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import { ArrowLeft } from 'lucide-react';
import type { Metadata } from 'next';
import { getPlayer, organizationSlugFor, type PublicPlayer } from '../../public-data';
import { SiteBreadcrumb, SiteFooter, SiteHeader } from '../../seo';

export const metadata: Metadata = {
  title: '選手比較',
  description: '複数の選手の確認できた情報・経歴を並べて比較できます。',
  robots: { index: false },
};

// 選手詳細ページのfactsで実際に使われているラベル（organization-category.tsと同様、
// 表示専用の並び順であり、Master/Candidateデータのスキーマには手を入れていない）。
const FACT_LABELS = ['英字表記', '生年月日', '身長', '体重', 'ポジション'] as const;

const MAX_COMPARE = 4;

function parseSlugs(raw: string | string[] | undefined): string[] {
  const value = Array.isArray(raw) ? raw[0] : raw;
  if (!value) return [];
  return [...new Set(value.split(',').map((slug) => slug.trim()).filter(Boolean))].slice(0, MAX_COMPARE);
}

function compareColsClass(count: number): string {
  if (count === 3) return ' jbaListB-compareCols3';
  if (count >= 4) return ' jbaListB-compareCols4';
  return '';
}

export default async function ComparePlayersPage({
  searchParams,
}: {
  searchParams: Promise<{ slugs?: string | string[] }>;
}) {
  const { slugs: rawSlugs } = await searchParams;
  const requestedSlugs = parseSlugs(rawSlugs);
  const players = requestedSlugs
    .map((slug) => getPlayer(slug))
    .filter((player): player is PublicPlayer => Boolean(player));
  const missingCount = requestedSlugs.length - players.length;
  const colsClass = compareColsClass(players.length);

  return (
    <main className="jbaListB-page">
      <SiteHeader active="players" />
      <SiteBreadcrumb crumbs={[{ label: '選手一覧', href: '/players' }, { label: '選手比較' }]} />

      <div className="jbaListB-main">
        <div>
          <p className="jbaListB-eyebrow">Compare players</p>
          <h1 className="jbaListB-h1">選手比較</h1>
          <p className="jbaListB-lede">
            選手一覧のチェックボックスで2〜{MAX_COMPARE}人を選ぶと、確認できた情報と経歴を並べて比較できます。
          </p>
        </div>

        {players.length < 2 ? (
          <div className="jbaListB-filterCard">
            <p className="jbaListB-note">
              比較するには選手を2人以上選ぶ必要があります。
              {missingCount > 0 && '（指定された選手の一部が見つかりませんでした）'}
            </p>
            <a href="/players" className="jbaListB-textLink" style={{ marginTop: 12 }}>
              <ArrowLeft size={14} /> 選手一覧に戻って選び直す
            </a>
          </div>
        ) : (
          <>
            {missingCount > 0 && (
              <p className="jbaListB-note">※ 指定された選手のうち{missingCount}人が見つかりませんでした。</p>
            )}

            <section className="jbaListB-section">
              <div className="jbaListB-sectionHead">
                <p className="jbaListB-eyebrow">Source-based facts</p>
                <h2>確認できた情報</h2>
              </div>
              <div className="jbaListB-compareTable">
                <div className={`jbaListB-compareRow jbaListB-compareHead${colsClass}`}>
                  <div className="jbaListB-compareRowLabel" />
                  {players.map((player) => (
                    <div key={player.id} className="jbaListB-compareCol">
                      <a href={`/players/${player.slug}`} className="jbaListB-timelineOrg">{player.name}</a>
                      <span
                        className={`jbaListB-pill ${player.dataStatus === 'master' ? 'jbaListB-statusMaster' : 'jbaListB-statusCandidate'}`}
                      >
                        {player.dataStatus === 'master' ? '承認済み' : '確認中'}
                      </span>
                    </div>
                  ))}
                </div>
                {FACT_LABELS.map((label) => (
                  <div key={label} className={`jbaListB-compareRow${colsClass}`}>
                    <div className="jbaListB-compareRowLabel">{label}</div>
                    {players.map((player) => {
                      const fact = player.facts.find((item) => item.label === label);
                      return (
                        <div key={player.id} className="jbaListB-compareCol">
                          {fact?.value ?? '—'}
                        </div>
                      );
                    })}
                  </div>
                ))}
              </div>
            </section>

            <section className="jbaListB-section">
              <div className="jbaListB-sectionHead">
                <p className="jbaListB-eyebrow">Career snapshot</p>
                <h2>経歴</h2>
              </div>
              <div className={`jbaListB-compareCareers${colsClass}`}>
                {players.map((player) => (
                  <div key={player.id} className="jbaListB-compareCareerCol">
                    <h3 className="jbaListB-compareCareerName">{player.name}</h3>
                    <div className="jbaListB-timeline">
                      {player.careers.map((career) => {
                        const organizationSlug = organizationSlugFor(career.organizationId);
                        return (
                          <div className="jbaListB-timelineRow" key={`${career.period}-${career.organization ?? career.detail}`}>
                            <span className="jbaListB-timelineYear">{career.period}</span>
                            <div className="jbaListB-timelineDotCol">
                              <span className={`jbaListB-timelineDot ${career.status === 'hold' ? 'jbaListB-timelineDotMuted' : ''}`} />
                            </div>
                            <div className="jbaListB-timelineBody">
                              {career.organization ? (
                                organizationSlug ? (
                                  <a href={`/organizations/${organizationSlug}`} className="jbaListB-timelineOrg">{career.organization}</a>
                                ) : (
                                  <strong className="jbaListB-timelineOrg">{career.organization}</strong>
                                )
                              ) : (
                                <strong className="jbaListB-timelineHold">確認中</strong>
                              )}
                              <p className="jbaListB-timelineDetail">{career.detail}</p>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                ))}
              </div>
            </section>
          </>
        )}
      </div>

      <SiteFooter />
    </main>
  );
}
