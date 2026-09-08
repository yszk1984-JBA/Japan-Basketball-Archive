import { ArrowRight, Database, School, ShieldCheck } from 'lucide-react';
import { players, sources } from './prototype-data';

export default function Home() {
  return (
    <main>
      <header className="site-header">
        <a href="/" className="brand" aria-label="Japan Basketball Archive ホーム">
          <span className="brand-mark">J</span><span>Japan Basketball Archive</span>
        </a>
        <span className="prototype-label">Prototype v0.01</span>
      </header>
      <section className="hero">
        <div><p className="eyebrow">日本バスケットボールの記録</p><h1>選手と所属を、<br />出典からたどる。</h1><p className="lead">福岡第一高校の2020年度データを使った公開プロトタイプです。掲載内容は確認中で、正式なMaster Dataではありません。</p></div>
        <div className="hero-ball" aria-hidden="true"><span /></div>
      </section>
      <section className="stats" aria-label="プロトタイプの収録状況">
        <div><strong>{players.length}</strong><span>人物</span></div><div><strong>1</strong><span>組織</span></div><div><strong>{sources.length}</strong><span>参照資料</span></div><div><strong>2020</strong><span>対象年度</span></div>
      </section>
      <section className="content-section">
        <div className="section-heading"><div><p className="eyebrow">Pilot organization</p><h2>福岡第一高等学校</h2></div><a href="/organizations/fukuoka-daiichi" className="text-link">学校ページを見る <ArrowRight size={17} /></a></div>
        <div className="player-grid">{players.map((player, index) => <a href={`/players/${player.slug}`} className="player-card" key={player.id}><span className="card-index">0{index + 1}</span><div><p className="card-meta">No. {player.jerseyNumber}</p><h3>{player.name}</h3><p>{player.position}</p></div><ArrowRight size={20} /></a>)}</div>
      </section>
      <section className="principles"><div><Database size={22} /><h3>つながる記録</h3><p>人物、学校、経歴をIDで結びます。</p></div><div><ShieldCheck size={22} /><h3>出典を表示</h3><p>掲載した事実から確認元へ移動できます。</p></div><div><School size={22} /><h3>育成経路</h3><p>学校やクラブを時系列でたどる設計です。</p></div></section>
      <footer><span>Japan Basketball Archive</span><span>Data under review · 2026</span></footer>
    </main>
  );
}
