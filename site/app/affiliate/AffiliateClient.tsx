'use client';

import { useEffect, useRef, type ReactNode } from 'react';
import { todayJst } from './select';

type Gtag = (...args: unknown[]) => void;

// GA4へ送るのは広告の識別子だけ（個人情報・入力内容・URLのクエリは送らない）。gtagが無ければ何もしない。
function sendEvent(name: 'affiliate_click' | 'affiliate_impression', item: HTMLElement, useBeacon: boolean) {
  try {
    const gtag = (window as unknown as { gtag?: Gtag }).gtag;
    gtag?.('event', name, {
      affiliate_id: item.dataset.affProgram,
      link_id: item.dataset.affLink,
      asp_name: item.dataset.affAsp,
      page_type: item.dataset.affPageType,
      placement_id: item.dataset.affPlacement,
      ...(useBeacon ? { transport_type: 'beacon' } : {}),
    });
  } catch {
    // 計測の失敗は広告リンクの動作に影響させない
  }
}

// data-aff-until（日本時間の最終表示日）を過ぎた要素を隠す。
// ページはビルド時に作られるため、期限切れの広告が次のデプロイまで残らないようにする閲覧時の安全策。
function hideExpired(root: HTMLElement): void {
  const today = todayJst();
  const targets = [root, ...Array.from(root.querySelectorAll<HTMLElement>('[data-aff-until]'))];
  for (const element of targets) {
    const until = element.dataset.affUntil;
    if (until && today > until) element.hidden = true;
  }
  const items = Array.from(root.querySelectorAll<HTMLElement>('[data-aff-item]'));
  if (items.length > 0 && items.every((item) => item.hidden)) root.hidden = true;
}

// 広告枠のラッパー。クリック・表示の計測と、期限切れの非表示を受け持つ。
// クリックは枠でまとめて受け取り（イベント委譲）、ASP発行コードの中身には手を加えない。
// 遷移を止めない（preventDefaultしない）ため、ASP側の計測にも影響しない。
export function AffiliateSlotClient({
  className,
  until,
  children,
}: {
  className: string;
  until: string | null;
  children: ReactNode;
}) {
  const ref = useRef<HTMLElement>(null);

  useEffect(() => {
    const root = ref.current;
    if (!root) return;
    hideExpired(root);
    if (root.hidden) return;

    const onClick = (event: MouseEvent) => {
      if (event.type === 'auxclick' && event.button !== 1) return;
      const target = event.target as Element | null;
      if (!target?.closest('a[href]')) return;
      const item = target.closest<HTMLElement>('[data-aff-item]');
      if (item && !item.hidden) sendEvent('affiliate_click', item, true);
    };
    root.addEventListener('click', onClick, true);
    root.addEventListener('auxclick', onClick, true);

    // 表示回数：各広告が画面に半分以上入ったときに、ページの表示ごとに1回だけ送る。
    const sent = new Set<Element>();
    const observer =
      typeof IntersectionObserver === 'undefined'
        ? null
        : new IntersectionObserver(
            (entries) => {
              for (const entry of entries) {
                if (!entry.isIntersecting || sent.has(entry.target)) continue;
                const item = entry.target as HTMLElement;
                if (item.hidden) continue;
                sent.add(item);
                sendEvent('affiliate_impression', item, false);
                observer?.unobserve(item);
              }
            },
            { threshold: 0.5 },
          );
    root.querySelectorAll('[data-aff-item]').forEach((item) => observer?.observe(item));

    return () => {
      root.removeEventListener('click', onClick, true);
      root.removeEventListener('auxclick', onClick, true);
      observer?.disconnect();
    };
  }, []);

  return (
    <aside ref={ref} className={className} aria-label="広告" data-aff-until={until ?? undefined}>
      {children}
    </aside>
  );
}

// 記事上部のPR表記。ページ内の広告がすべて期限切れになったら一緒に隠す。
export function AffiliateNoticeClient({ until, children }: { until: string | null; children: ReactNode }) {
  const ref = useRef<HTMLParagraphElement>(null);
  useEffect(() => {
    const element = ref.current;
    if (element && until && todayJst() > until) element.hidden = true;
  }, [until]);
  return (
    <p ref={ref} className="jbaAff-notice" data-aff-until={until ?? undefined}>
      {children}
    </p>
  );
}
