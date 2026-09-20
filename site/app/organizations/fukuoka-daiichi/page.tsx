/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import { ArrowLeft, ArrowRight, ArrowUpRight } from 'lucide-react';
import type { Metadata } from 'next';
import { players, sources } from '../../prototype-data';

export const metadata: Metadata = {
  title: '福岡第一高等学校',
  description: '福岡第一高等学校男子バスケットボール部に関する、出典付き候補データの一覧です。',
  alternates: { canonical: '/organizations/fukuoka-daiichi' },
};

export default function OrganizationPage() {
  return (
    <main className="detail-shell">
      <nav className="detail-nav"><a href="/"><ArrowLeft size={17} /> アーカイブへ戻る</a><span>Prototype · 確認中</span></nav>
      <header className="organization-header"><p className="eyebrow">Organization · ORG000010</p><h1>福岡第一高等学校</h1><p>福岡県福岡市 · High School</p></header>
      <section className="roster-section"><div className="section-heading"><div><p className="eyebrow">Pilot records</p><h2>掲載人物</h2></div><span>{players.length} records</span></div><div className="roster-list">{players.map((player) => <a href={`/players/${player.slug}`} key={player.id}><span className="number">{player.facts.find((fact) => fact.label === '背番号')?.value ?? '—'}</span><div><strong>{player.name}</strong><p>{player.cardContext} · {player.id}</p></div><ArrowRight size={19} /></a>)}</div></section>
      <section className="source-section"><p className="eyebrow">Sources</p><h2>参照資料</h2><div className="source-list">{sources.map((source) => <a href={source.url} target="_blank" rel="noreferrer" key={source.id}><span>{source.id}</span><div><strong>{source.title}</strong><p>{source.publisher}</p></div><ArrowUpRight size={18} /></a>)}</div><p className="review-note">対象人物は画面の接続確認用に{players.length}名を掲載しています。福岡第一高校の全関係者を示す一覧ではありません。</p></section>
    </main>
  );
}
