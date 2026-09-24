import type { Metadata } from 'next';
import './globals.css';
import './prototype-v002.css';
import './list-b.css';

export const metadata: Metadata = {
  metadataBase: new URL('https://japanbasketballarchive.com'),
  title: {
    default: 'Japan Basketball Archive',
    template: '%s | Japan Basketball Archive',
  },
  description: '日本バスケットボールの人物と所属を、出典とともに記録するアーカイブ。',
  icons: {
    icon: [{ url: '/favicon.svg', type: 'image/svg+xml' }],
    shortcut: '/favicon.svg',
  },
  openGraph: {
    siteName: 'Japan Basketball Archive',
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
