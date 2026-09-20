import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = { title: 'Japan Basketball Archive', description: '日本バスケットボールの人物と所属を、出典とともに記録するアーカイブ。' };

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
