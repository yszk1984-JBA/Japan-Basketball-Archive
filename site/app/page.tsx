/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import { ArrowRight, Database, School, ShieldCheck } from 'lucide-react';
import type { Metadata } from 'next';
import { getHomepagePlayers, players, sources } from './public-data';

export const metadata: Metadata = {
  alternates: { canonical: '/' },
};

export default function Home() {
  const homepagePlayers = getHomepagePlayers();
  const organizationCount = new Set(
    players.flatMap((player) => player.careers.map((career) => career.organization).filter(Boolean)),
  ).size;

  return (
    <main>
      <header className="site-header">
        <a href="/" className="brand" aria-label="Japan Basketball Archive ホーム">
          <span className="brand-mark">J</span><span>Japan Basketball Archive</span>
        </a>
        <span className="prototype-label">Archive preview</span>
      </header>
      <section className="hero">
        <div><p className="eyebrow">日本バスケットボールの記録</p><h1>選手と所属を、<br />出典からたどる。</h1><p className="lead">承認済みMaster Dataと、公開画面の検証に使う確認中データを区別して掲載しています。</p></div>
        <div className="hero-ball" aria-hidden="true"><span /></div>
      </section>
      <section className="stats" aria-label="プロトタイプの収録状況">
        <div><strong>{players.length}</strong><span>人物</span></div><div><strong>{organizationCount}</strong><span>掲載組織</span></div><div><strong>{sources.length}</strong><span>参照資料</span></div><div><strong>複数</strong><span>対象年度</span></div>
      </section>
      <section className="content-section">
        <div className="section-heading"><div><p className="eyebrow">Featured players</p><h2>注目選手</h2></div><a href="/organizations/fukuoka-daiichi" className="text-link">福岡第一高校のページを見る <ArrowRight size={17} /></a></div>
        <div className="player-grid">{homepagePlayers.map((player, index) => <a href={`/players/${player.slug}`} className="player-card" key={player.id}><span className="card-index">{String(index + 1).padStart(2, '0')}</span><div><p className="card-meta">{player.cardContext}</p><h3>{player.name}</h3><p className={player.dataStatus === 'master' ? 'card-status master' : 'card-status'}>{player.dataStatus === 'master' ? 'Master · 承認済み' : '候補データ · 正式承認前'}</p></div><ArrowRight size={20} /></a>)}</div>
      </section>
      <section className="principles"><div><Database size={22} /><h3>つながる記録</h3><p>人物、学校、経歴をIDで結びます。</p></div><div><ShieldCheck size={22} /><h3>出典を表示</h3><p>掲載した事実から確認元へ移動できます。</p></div><div><School size={22} /><h3>育成経路</h3><p>学校やクラブを時系列でたどる設計です。</p></div></section>
      <footer><span>Japan Basketball Archive</span><span>Data under review · 2026</span></footer>
    </main>
  );
}
