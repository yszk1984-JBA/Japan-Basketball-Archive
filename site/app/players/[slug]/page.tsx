/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import { ArrowUpRight } from 'lucide-react';
import type { Metadata } from 'next';
import { notFound, permanentRedirect } from 'next/navigation';
import { getPlayer, getSources, masterApprovals, masterPublication, organizationSlugFor, players } from '../../public-data';
import { CareerGantt } from './CareerGantt';
import { baseOpenGraph, JsonLd, playerJsonLd, playerPageMeta, SiteBreadcrumb, SiteFooter, SiteHeader } from '../../seo';

export function generateStaticParams() {
  return players.map((player) => ({ slug: player.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const player = getPlayer(slug);

  if (!player) return {};

  const sourceCount = new Set([
    ...player.facts.flatMap((fact) => fact.sourceIds),
    ...player.careers.flatMap((career) => career.sourceIds),
    ...player.aliases.flatMap((alias) => alias.sourceIds),
  ]).size;
  const { title, description } = playerPageMeta(player, sourceCount);

  return {
    title,
    description,
    alternates: { canonical: `/players/${player.slug}` },
    openGraph: { ...baseOpenGraph, title, description, url: `/players/${player.slug}`, type: 'profile' },
  };
}

function EvidenceLinks({ sourceIds }: { sourceIds: readonly string[] }) {
  const evidence = getSources(sourceIds);
  if (!evidence.length) return null;
  return (
    <div className="jbaListB-evidenceLinks" aria-label="この項目の出典">
      {evidence.map((source) => (
        <a href={source.url} target="_blank" rel="noreferrer" key={source.id}>
          出典 {source.id} <ArrowUpRight size={12} />
        </a>
      ))}
    </div>
  );
}

export default async function PlayerPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const player = getPlayer(slug);
  if (!player) notFound();
  if (slug !== player.slug) permanentRedirect(`/players/${player.slug}`);

  const sourceIds = [...new Set([
    ...player.facts.flatMap((fact) => fact.sourceIds),
    ...player.careers.flatMap((career) => career.sourceIds),
    ...player.aliases.flatMap((alias) => alias.sourceIds),
  ])];
  const playerSources = getSources(sourceIds);

  return (
    <main className="jbaListB-page">
      <JsonLd data={playerJsonLd(player, organizationSlugFor)} />
      <SiteHeader active="players" />
      <SiteBreadcrumb crumbs={[{ label: '選手一覧', href: '/players' }, { label: player.name }]} />

      <div className="jbaListB-main">
        <header className="jbaListB-detailHeader">
          <p className="jbaListB-eyebrow">Person · {player.id}</p>
          <h1 className="jbaListB-detailTitle">{player.name}</h1>
          <div className="jbaListB-statusRow">
            <span className={`jbaListB-pill ${player.dataStatus === 'master' ? 'jbaListB-statusMaster' : 'jbaListB-statusCandidate'}`}>
              {player.dataStatus === 'master' ? `Master・承認済み・${player.approvalId}` : '候補データ・出典あり・正式承認前'}
            </span>
          </div>
        </header>

        <section className="jbaListB-section">
          <div className="jbaListB-sectionHead">
            <p className="jbaListB-eyebrow">Source-based facts</p>
            <h2>確認できた情報</h2>
          </div>
          <div className="jbaListB-factGrid">
            {player.facts.map((fact) => (
              <article className="jbaListB-factCard" key={`${fact.label}-${fact.context}`}>
                <span className="jbaListB-factLabel">{fact.label}</span>
                <strong className="jbaListB-factValue">{fact.value}</strong>
                <p className="jbaListB-factContext">{fact.context}</p>
                <EvidenceLinks sourceIds={fact.sourceIds} />
              </article>
            ))}
          </div>
        </section>

        {player.aliases.length > 0 && (
          <section className="jbaListB-section">
            <div className="jbaListB-sectionHead">
              <p className="jbaListB-eyebrow">Name history</p>
              <h2>登録名の履歴</h2>
            </div>
            <div className="jbaListB-factGrid">
              {player.aliases.map((alias) => (
                <article className="jbaListB-aliasCard" key={`${alias.period}-${alias.value}`}>
                  <span className="jbaListB-aliasMeta">{alias.period} · {alias.label}</span>
                  <strong className="jbaListB-aliasValue">{alias.value}</strong>
                  <p className="jbaListB-aliasNote">過去の氏名は上書きせず、時点別に表示しています。</p>
                  <EvidenceLinks sourceIds={alias.sourceIds} />
                </article>
              ))}
            </div>
          </section>
        )}

        <section className="jbaListB-section">
          <div className="jbaListB-sectionHead">
            <p className="jbaListB-eyebrow">Career snapshot</p>
            <h2>経歴</h2>
          </div>
          <CareerGantt careers={player.careers} />
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
                    <EvidenceLinks sourceIds={career.sourceIds} />
                  </div>
                </div>
              );
            })}
          </div>
          <p className="jbaListB-ganttUndated">クラブ名は現在の登録名で表示しています。改称前の名称（例：サンロッカーズ渋谷、西宮ストークス）は、在籍当時の表記と異なる場合があります。</p>
        </section>

        <section className="jbaListB-section">
          <div className="jbaListB-sectionHead">
            <p className="jbaListB-eyebrow">Sources</p>
            <h2>この人物に使用した資料</h2>
          </div>
          <div className="jbaListB-sourceList">
            {playerSources.map((source) => (
              <a href={source.url} target="_blank" rel="noreferrer" className="jbaListB-sourceRow" key={source.id}>
                <span className="jbaListB-sourceId">{source.id}</span>
                <div>
                  <strong className="jbaListB-sourceTitle">{source.title}</strong>
                  <p className="jbaListB-sourceMeta">{source.publisher} · {player.sourceLocations?.[source.id] ?? source.location} · 確認日 {source.accessedAt}</p>
                </div>
                <ArrowUpRight size={16} />
              </a>
            ))}
          </div>
          <p className={`jbaListB-reviewNote ${player.dataStatus === 'master' ? 'jbaListB-reviewNoteMaster' : ''}`}>
            {player.dataStatus === 'master'
              ? `このページはGovernance v1.0のHuman approvalを経たMaster Dataです。承認日 ${(masterApprovals as Record<string, { approvedAt: string }>)[player.approvalId ?? '']?.approvedAt ?? masterPublication.approvedAt}${(player.enrichmentApprovalIds ?? []).length > 0 ? `（経歴の追加承認 ${(player.enrichmentApprovalIds ?? []).map((id) => (masterApprovals as Record<string, { approvedAt: string }>)[id]?.approvedAt ?? id).join('、')}）` : ''}。未解決のHOLD項目は掲載していません。`
              : 'このページはCANDIDATE段階のデータです。出典を伴うREADY_FOR_VERIFIED_REVIEW判定の項目のみを表示していますが、Yuichiによる正式承認（Governance v1.0のVERIFIED・Human approvalを経たMaster化）前の情報です。'}
          </p>
        </section>
      </div>

      <SiteFooter />
    </main>
  );
}
