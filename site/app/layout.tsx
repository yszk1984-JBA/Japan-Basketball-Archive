import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = { title: 'Japan Basketball Archive', description: '日本バスケットボールの人物と所属を、出典とともに記録するアーカイブ。' };

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="ja"><body>{children}</body></html>;
}
