'use client';

import { useState } from 'react';
import { xHandle } from './site-url';

type Props = {
  // シェアするページの絶対URL（canonicalと同じもの）。
  readonly url: string;
  // シェア文言（Xの投稿本文。URLは別に付く）。
  readonly text: string;
  // Xのハッシュタグ（#なし）。
  readonly hashtags?: readonly string[];
};

declare global {
  interface Window {
    gtag?: (...args: unknown[]) => void;
  }
}

// どのSNSでシェアされたかをGA4のshareイベントとして記録する（gtagが無ければ何もしない）。
function trackShare(method: string, url: string) {
  try {
    window.gtag?.('event', 'share', { method, content_type: 'page', item_id: url });
  } catch {
    // 計測の失敗はシェア操作に影響させない
  }
}

async function copyText(value: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(value);
    return true;
  } catch {
    // Clipboard APIが使えない環境（非HTTPSや権限なし）では失敗を返す
    return false;
  }
}

// X・LINE・URLコピーのシェアボタン。外部スクリプトは読み込まず、共有用URLへのリンクだけで実装する。
export function ShareButtons({ url, text, hashtags = [] }: Props) {
  const [copyState, setCopyState] = useState<'idle' | 'copied' | 'failed'>('idle');

  const xParams = new URLSearchParams({ text, url });
  if (hashtags.length) xParams.set('hashtags', hashtags.join(','));
  if (xHandle) xParams.set('via', xHandle);
  const xUrl = `https://x.com/intent/post?${xParams.toString()}`;
  const lineUrl = `https://social-plugins.line.me/lineit/share?url=${encodeURIComponent(url)}`;

  return (
    <div className="jbaListB-share" aria-label="このページをシェア">
      <span className="jbaListB-shareLabel">シェア</span>
      <a
        className="jbaListB-shareButton"
        href={xUrl}
        target="_blank"
        rel="noopener noreferrer"
        onClick={() => trackShare('x', url)}
      >
        Xでポスト
      </a>
      <a
        className="jbaListB-shareButton"
        href={lineUrl}
        target="_blank"
        rel="noopener noreferrer"
        onClick={() => trackShare('line', url)}
      >
        LINEで送る
      </a>
      <button
        type="button"
        className="jbaListB-shareButton"
        onClick={async () => {
          const ok = await copyText(url);
          setCopyState(ok ? 'copied' : 'failed');
          if (ok) trackShare('copy_link', url);
          window.setTimeout(() => setCopyState('idle'), 2000);
        }}
      >
        {copyState === 'copied' ? 'コピーしました' : copyState === 'failed' ? 'コピーできませんでした' : 'URLをコピー'}
      </button>
    </div>
  );
}
