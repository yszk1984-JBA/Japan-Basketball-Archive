import type { Metadata } from 'next';
import './globals.css';
import './site-b.css';
import { defaultOgImage } from './seo';
import { adsenseClientId, siteUrl } from './site-url';

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: {
    default: 'Rosterline｜日本バスケ経歴アーカイブ',
    template: '%s | Rosterline',
  },
  description: '日本バスケットボールの人物と所属を、出典とともに記録するアーカイブ。',
  // iconsはmetadataで指定しない。vinextがアイコンのlinkタグに内部キー（/players/p000419:13vaz3c など）を
  // data属性として出力し、GooglebotがそれをURLとして拾って404が大量に記録されたため（2026-11-02）。
  // ファビコンは下の<head>内に直接書く。
  openGraph: {
    siteName: 'Rosterline',
    locale: 'ja_JP',
    type: 'website',
    images: [defaultOgImage],
  },
  // Xでのリンク表示を大きな画像のカードにする。@rosterline_jp は公式Xアカウント。
  twitter: {
    card: 'summary_large_image',
    site: '@rosterline_jp',
    images: [defaultOgImage.url],
  },
};

const googleAnalyticsId = 'G-9QYZ1747RN';

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="ja">
      <head>
        <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
        <script async src={`https://www.googletagmanager.com/gtag/js?id=${googleAnalyticsId}`} />
        <script
          dangerouslySetInnerHTML={{
            __html: `
              window.dataLayer = window.dataLayer || [];
              function gtag(){dataLayer.push(arguments);}
              gtag('js', new Date());
              gtag('config', '${googleAnalyticsId}');
            `,
          }}
        />
        {/* Google AdSense（サイトの所有確認と広告配信）。自動広告はAdSense管理画面でオフにし、広告枠は個別に配置する。 */}
        <script
          async
          src={`https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${adsenseClientId}`}
          crossOrigin="anonymous"
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
