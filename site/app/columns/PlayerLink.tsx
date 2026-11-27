/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import { players } from '../public-data';

// 記事本文から選手ページへリンクする（確認済みの選手を名前で探し、見つからなければ文字だけ表示する）。
export function PlayerLink({ name, label }: { name: string; label?: string }) {
  const player = players.find((item) => item.dataStatus === 'master' && item.name === name);
  return player ? <a href={`/players/${player.slug}`}>{label ?? name.replace(/ /g, '')}</a> : <>{label ?? name}</>;
}
