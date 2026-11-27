/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import type { Metadata } from 'next';
import { baseOpenGraph, breadcrumbJsonLd, JsonLd, SiteBreadcrumb, SiteFooter, SiteHeader } from '../seo';
import { correctionFormUrl, xHandle } from '../site-url';

const title = 'お問い合わせ';
const description =
  'Rosterlineへのお問い合わせ方法です。掲載内容の訂正・削除のご依頼はフォームから、そのほかのご連絡はXのダイレクトメッセージで受け付けています。';

export const metadata: Metadata = {
  title,
  description,
  alternates: { canonical: '/contact' },
  openGraph: { ...baseOpenGraph, title, description, url: '/contact' },
};

export default function ContactPage() {
  return (
    <main className="jbaListB-page">
      <JsonLd
        data={{
          '@context': 'https://schema.org',
          '@graph': [
            breadcrumbJsonLd([
              { name: 'ホーム', path: '/' },
              { name: title, path: '/contact' },
            ]),
          ],
        }}
      />
      <SiteHeader />
      <SiteBreadcrumb crumbs={[{ label: title }]} />

      <div className="jbaListB-main">
        <div>
          <p className="jbaListB-eyebrow">Contact</p>
          <h1 className="jbaListB-h1">{title}</h1>
        </div>

        <section className="jbaListB-section jbaListB-about">
          <div className="jbaListB-sectionHead">
            <h2>掲載内容の訂正・削除のご依頼</h2>
          </div>
          <p>
            誤りのご指摘や、掲載の削除のご依頼は、下記のフォームからお送りください。選手ご本人・ご家族・所属先の方に限らず、どなたからでも受け付けています。
          </p>
          <p>
            <a href={correctionFormUrl} target="_blank" rel="noreferrer" className="jbaListB-aboutButton">
              訂正・削除依頼フォームを開く
            </a>
          </p>
          <p>
            記入していただきたい内容は、<a href="/about#corrections">このサイトについて</a>をご覧ください。
          </p>
        </section>

        <section className="jbaListB-section jbaListB-about">
          <div className="jbaListB-sectionHead">
            <h2>そのほかのお問い合わせ</h2>
          </div>
          <p>
            掲載してほしい選手・学校のご提案、データの使い方のご相談など、そのほかのご連絡は、Xのダイレクトメッセージ（
            <a href={`https://x.com/${xHandle}`} target="_blank" rel="noreferrer">
              @{xHandle}
            </a>
            ）で受け付けています。
          </p>
        </section>

        <section className="jbaListB-section jbaListB-about">
          <div className="jbaListB-sectionHead">
            <h2>お返事について</h2>
          </div>
          <ul>
            <li>個人で運営しているため、お返事までにお時間をいただく場合があります。</li>
            <li>訂正のご指摘は、出典で確認できたものから順に反映します。</li>
            <li>営業・宣伝を目的としたご連絡には、お返事できない場合があります。</li>
          </ul>
        </section>
      </div>

      <SiteFooter />
    </main>
  );
}
