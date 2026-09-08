import Link from 'next/link';
import { ArrowLeft, ArrowUpRight } from 'lucide-react';
import { getPlayer, getSources, players } from '../../prototype-data';

export function generateStaticParams() { return players.map((player) => ({ slug: player.slug })); }

export default async function PlayerPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const player = getPlayer(slug);
  if (!player) return <main className="detail-shell"><p>人物が見つかりません。</p></main>;
  const playerSources = getSources(player.sourceIds);
  return (
    <main className="detail-shell">
      <nav className="detail-nav"><Link href="/"><ArrowLeft size={17} /> アーカイブへ戻る</Link><span>Prototype · 確認中</span></nav>
      <header className="person-header"><p className="eyebrow">Person · {player.id}</p><h1>{player.name}</h1><p className="reading">{player.reading}</p><div className="person-facts"><div><span>役割</span><strong>{player.role}</strong></div><div><span>背番号</span><strong>{player.jerseyNumber}</strong></div><div><span>ポジション</span><strong>{player.position}</strong></div></div></header>
      <section className="timeline-section"><p className="eyebrow">Career snapshot</p><h2>確認中の経歴</h2><div className="timeline"><div><span className="year">2020年度</span><span className="timeline-dot" /><div><Link href="/organizations/fukuoka-daiichi">福岡第一高等学校</Link><p>ウインターカップ2020 登録選手</p></div></div><div><span className="year">卒業後</span><span className="timeline-dot muted" /><div><strong>{player.nextStep}</strong><p>進路記事の記載。入学・在籍は別資料で確認中</p></div></div></div></section>
      <section className="source-section"><p className="eyebrow">Sources</p><h2>参照資料</h2><div className="source-list">{playerSources.map((source) => <a href={source.url} target="_blank" rel="noreferrer" key={source.id}><span>{source.id}</span><div><strong>{source.title}</strong><p>{source.publisher}</p></div><ArrowUpRight size={18} /></a>)}</div><p className="review-note">このページは公開表示を確認するためのプロトタイプです。掲載内容はGovernance v1.0のHuman approvalを受けたMaster Dataではありません。</p></section>
    </main>
  );
}
