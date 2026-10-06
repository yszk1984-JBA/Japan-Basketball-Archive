import type { Metadata } from 'next';
import './globals.css';
import './site-b.css';
import { siteUrl } from './site-url';

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: {
    default: 'Rosterline｜日本バスケ経歴アーカイブ',
    template: '%s | Rosterline',
  },
  description: '日本バスケットボールの人物と所属を、出典とともに記録するアーカイブ。',
  icons: {
    icon: [{ url: '/favicon.svg', type: 'image/svg+xml' }],
    shortcut: '/favicon.svg',
  },
  openGraph: {
    siteName: 'Rosterline',
    locale: 'ja_JP',
    type: 'website',
  },
};

const googleAnalyticsId = 'G-9QYZ1747RN';

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="ja">
      <head>
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
      </head>
      <body>{children}</body>
    </html>
  );
}
