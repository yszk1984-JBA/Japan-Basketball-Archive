/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import { ArrowLeft, ArrowRight, ArrowUpRight } from 'lucide-react';
import type { Metadata } from 'next';
import { players, sources } from '../../public-data';

export const metadata: Metadata = {
  title: '福岡第一高等学校',
  description: '福岡第一高等学校男子バスケットボール部に関する、出典付き候補データの一覧です。',
  alternates: { canonical: '/organizations/fukuoka-daiichi' },
};

export default function OrganizationPage() {
  const relatedPlayers = players.filter((player) =>
    player.careers.some((career) => career.organization === '福岡第一高等学校'),
  );
  const masterPlayers = relatedPlayers.filter((player) => player.dataStatus === 'master');
  const candidatePlayers = relatedPlayers.filter((player) => player.dataStatus === 'candidate');

  return (
    <main className="detail-shell">
      <nav className="detail-nav"><a href="/"><ArrowLeft size={17} /> アーカイブへ戻る</a><span>Prototype · 確認中</span></nav>
      <header className="organization-header"><p className="eyebrow">Organization · ORG000010</p><h1>福岡第一高等学校</h1><p>福岡県福岡市 · High School</p></header>
      <section className="roster-section"><div className="section-heading"><div><p className="eyebrow">Approved Master</p><h2>承認済み人物</h2></div><span>{masterPlayers.length} records</span></div><div className="roster-list">{masterPlayers.map((player) => <a href={`/players/${player.slug}`} key={player.id}><span className="number">M</span><div><strong>{player.name}</strong><p>{player.cardContext} · {player.id} · Master</p></div><ArrowRight size={19} /></a>)}</div></section>
      <section className="roster-section"><div className="section-heading"><div><p className="eyebrow">Candidate records</p><h2>確認中の人物</h2></div><span>{candidatePlayers.length} records</span></div><div className="roster-list">{candidatePlayers.map((player) => <a href={`/players/${player.slug}`} key={player.id}><span className="number">{player.facts.find((fact) => fact.label === '背番号')?.value ?? '—'}</span><div><strong>{player.name}</strong><p>{player.cardContext} · {player.id}</p></div><ArrowRight size={19} /></a>)}</div></section>
      <section className="source-section"><p className="eyebrow">Sources</p><h2>参照資料</h2><div className="source-list">{sources.map((source) => <a href={source.url} target="_blank" rel="noreferrer" key={source.id}><span>{source.id}</span><div><strong>{source.title}</strong><p>{source.publisher} · {source.dataStatus === 'master' ? 'Master' : '候補'}</p></div><ArrowUpRight size={18} /></a>)}</div><p className="review-note">この一覧は福岡第一高校とのCareerが収録済みの人物だけを表示します。全関係者を示す名簿ではありません。</p></section>
    </main>
  );
}
