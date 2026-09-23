/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import { ArrowLeft, ArrowUpRight } from 'lucide-react';
import type { Metadata } from 'next';
import { notFound, permanentRedirect } from 'next/navigation';
import { getPlayer, getSources, masterPublication, organizationSlugFor, players } from '../../public-data';
import { baseOpenGraph, careerOrganizationNames, JsonLd, playerJsonLd, SiteLinks } from '../../seo';

export function generateStaticParams() {
  return players.map((player) => ({ slug: player.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const player = getPlayer(slug);

  if (!player) return {};

  const organizationNames = careerOrganizationNames(player);
  const organizationsLabel = organizationNames.join('・');
  const title = organizationNames.length ? `${player.name}の経歴・所属（${organizationsLabel}）` : `${player.name}の経歴・所属`;
  const englishName = player.facts.find((fact) => fact.label === '英字表記')?.value;
  const sourceCount = new Set([
    ...player.facts.flatMap((fact) => fact.sourceIds),
    ...player.careers.flatMap((career) => career.sourceIds),
    ...player.aliases.flatMap((alias) => alias.sourceIds),
  ]).size;
  const description = [
    `${player.name}${englishName ? `（${englishName}）` : ''}の所属・経歴。`,
    organizationNames.length ? `${organizationsLabel}などの所属記録を、` : '',
    `出典${sourceCount > 0 ? `${sourceCount}件` : ''}とともに掲載しています。`,
    player.dataStatus === 'master' ? '' : '（正式承認前の候補データ）',
  ].join('');

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
    <div className="evidence-links" aria-label="この項目の出典">
      {evidence.map((source) => (
        <a href={source.url} target="_blank" rel="noreferrer" key={source.id}>
          出典 {source.id} <ArrowUpRight size={13} />
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
    <main className="detail-shell">
      <JsonLd data={playerJsonLd(player, organizationSlugFor)} />
      <nav className="detail-nav"><a href="/"><ArrowLeft size={17} /> アーカイブへ戻る</a><SiteLinks /><span>{player.dataStatus === 'master' ? 'Master Data' : '候補データ'}</span></nav>
      <header className="person-header">
        <p className="eyebrow">Person · {player.id}</p>
        <h1>{player.name}</h1>
        <p className={`candidate-status ${player.dataStatus === 'master' ? 'master-status' : ''}`}>{player.dataStatus === 'master' ? `Master · 承認済み · ${player.approvalId}` : '候補データ · 出典あり · 正式承認前'}</p>
      </header>

      <section className="fact-section">
        <p className="eyebrow">Source-based facts</p>
        <h2>確認できた情報</h2>
        <div className="fact-grid">
          {player.facts.map((fact) => (
            <article key={`${fact.label}-${fact.context}`}>
              <span>{fact.label}</span><strong>{fact.value}</strong><p>{fact.context}</p>
              <EvidenceLinks sourceIds={fact.sourceIds} />
            </article>
          ))}
        </div>
      </section>

      {player.aliases.length > 0 && (
        <section className="alias-section">
          <p className="eyebrow">Name history</p><h2>登録名の履歴</h2>
          {player.aliases.map((alias) => (
            <article className="alias-card" key={`${alias.period}-${alias.value}`}>
              <span>{alias.period} · {alias.label}</span><strong>{alias.value}</strong>
              <p>過去の氏名は上書きせず、時点別に表示しています。</p>
              <EvidenceLinks sourceIds={alias.sourceIds} />
            </article>
          ))}
        </section>
      )}

      <section className="timeline-section">
        <p className="eyebrow">Career snapshot</p><h2>経歴</h2>
        <div className="timeline">
          {player.careers.map((career) => {
            const organizationSlug = organizationSlugFor(career.organizationId);
            return (
              <div key={`${career.period}-${career.organization ?? career.detail}`}>
                <span className="year">{career.period}</span>
                <span className={`timeline-dot ${career.status === 'hold' ? 'muted' : ''}`} />
                <div>
                  {career.organization ? (
                    organizationSlug ? (
                      <a href={`/organizations/${organizationSlug}`}><strong>{career.organization}</strong></a>
                    ) : (
                      <strong>{career.organization}</strong>
                    )
                  ) : (
                    <strong className="hold-label">確認中</strong>
                  )}
                  <p>{career.detail}</p>
                  <EvidenceLinks sourceIds={career.sourceIds} />
                </div>
              </div>
            );
          })}
        </div>
      </section>

      <section className="source-section">
        <p className="eyebrow">Sources</p><h2>この人物に使用した資料</h2>
        <div className="source-list">
          {playerSources.map((source) => (
            <a href={source.url} target="_blank" rel="noreferrer" key={source.id}>
              <span>{source.id}</span><div><strong>{source.title}</strong><p>{source.publisher} · {source.location} · 確認日 {source.accessedAt}</p></div><ArrowUpRight size={18} />
            </a>
          ))}
        </div>
        <p className={`review-note ${player.dataStatus === 'master' ? 'master-note' : ''}`}>{player.dataStatus === 'master' ? `このページはGovernance v1.0のHuman approvalを経たMaster Dataです。承認日 ${masterPublication.approvedAt}。未解決のHOLD項目は掲載していません。` : 'このページはCANDIDATE段階のデータです。出典を伴うREADY_FOR_VERIFIED_REVIEW判定の項目のみを表示していますが、Yuichiによる正式承認（Governance v1.0のVERIFIED・Human approvalを経たMaster化）前の情報です。'}</p>
      </section>
    </main>
  );
}
