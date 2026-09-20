/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import { ArrowLeft, ArrowUpRight } from 'lucide-react';
import type { Metadata } from 'next';
import { getPlayer, getSources, players } from '../../prototype-data';

export function generateStaticParams() {
  return players.map((player) => ({ slug: player.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const player = getPlayer(slug);

  if (!player) return {};

  return {
    title: player.name,
    description: `${player.name}の所属・経歴を、確認できた出典とともに掲載しています。`,
    alternates: { canonical: `/players/${player.slug}` },
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
  if (!player) return <main className="detail-shell"><p>人物が見つかりません。</p></main>;

  const sourceIds = [...new Set([
    ...player.facts.flatMap((fact) => fact.sourceIds),
    ...player.careers.flatMap((career) => career.sourceIds),
    ...player.aliases.flatMap((alias) => alias.sourceIds),
  ])];
  const playerSources = getSources(sourceIds);

  return (
    <main className="detail-shell">
      <nav className="detail-nav"><a href="/"><ArrowLeft size={17} /> アーカイブへ戻る</a><span>Prototype · 候補データ</span></nav>
      <header className="person-header">
        <p className="eyebrow">Person · {player.id}</p>
        <h1>{player.name}</h1>
        <p className="candidate-status">候補データ · 出典あり · 正式承認前</p>
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
          {player.careers.map((career) => (
            <div key={`${career.period}-${career.organization ?? career.detail}`}>
              <span className="year">{career.period}</span>
              <span className={`timeline-dot ${career.status === 'hold' ? 'muted' : ''}`} />
              <div>
                {career.organization ? <strong>{career.organization}</strong> : <strong className="hold-label">確認中</strong>}
                <p>{career.detail}</p>
                <EvidenceLinks sourceIds={career.sourceIds} />
              </div>
            </div>
          ))}
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
        <p className="review-note">このページは公開表示を確認するためのプロトタイプです。掲載内容はGovernance v1.0のHuman approvalを受けたMaster Dataではありません。</p>
      </section>
    </main>
  );
}
