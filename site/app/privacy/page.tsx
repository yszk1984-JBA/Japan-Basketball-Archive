/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import type { Metadata } from 'next';
import { baseOpenGraph, breadcrumbJsonLd, JsonLd, SiteBreadcrumb, SiteFooter, SiteHeader, siteUrl } from '../seo';
import { correctionFormUrl } from '../site-url';

const title = 'プライバシーポリシー';
const description =
  'Rosterlineにおける、アクセス解析（Google Analytics）、広告配信（Google AdSense）とCookieの利用、お問い合わせフォームで受け取る情報の取り扱いについて説明します。';
// 本文を変更したら更新する（sitemap.tsのPRIVACY_UPDATED_ATも合わせる）。
const UPDATED_AT = '2026年11月2日';

export const metadata: Metadata = {
  title,
  description,
  alternates: { canonical: '/privacy' },
  openGraph: { ...baseOpenGraph, title, description, url: '/privacy' },
};

const external = { target: '_blank', rel: 'noopener noreferrer' } as const;

export default function PrivacyPage() {
  return (
    <main className="jbaListB-page">
      <JsonLd
        data={{
          '@context': 'https://schema.org',
          '@graph': [
            { '@type': 'WebPage', name: title, url: `${siteUrl}/privacy` },
            breadcrumbJsonLd([
              { name: 'ホーム', path: '/' },
              { name: title, path: '/privacy' },
            ]),
          ],
        }}
      />
      <SiteHeader />

      <SiteBreadcrumb crumbs={[{ label: title }]} />

      <div className="jbaListB-main">
        <div>
          <p className="jbaListB-eyebrow">Privacy</p>
          <h1 className="jbaListB-h1">{title}</h1>
        </div>

        <section className="jbaListB-section jbaListB-about">
          <p>
            Rosterline（以下「本サイト」）は、個人が運営する日本バスケットボールの経歴アーカイブです。本サイトをご利用いただく際の、情報の取り扱いについて以下のとおり定めます。
          </p>
        </section>

        <section className="jbaListB-section jbaListB-about">
          <div className="jbaListB-sectionHead">
            <h2>広告の配信について</h2>
          </div>
          <ul>
            <li>本サイトは、第三者配信の広告サービス「Google AdSense」を利用しています。</li>
            <li>
              Googleなどの第三者配信事業者は、Cookieを使用して、本サイトや他のサイトへの過去のアクセス情報に基づいて広告を配信します。
            </li>
            <li>
              Googleが広告Cookieを使用することにより、Googleやそのパートナーは、本サイトや他のサイトへのアクセス情報に基づいて、適切な広告を表示できます。
            </li>
            <li>
              パーソナライズ広告は、Googleの
              <a href="https://www.google.com/settings/ads" {...external}>
                広告設定
              </a>
              で無効にできます。また、
              <a href="https://www.aboutads.info/choices/" {...external}>
                www.aboutads.info
              </a>
              にアクセスすると、パーソナライズ広告に使われる第三者配信事業者のCookieを無効にできます。
            </li>
            <li>
              Googleによる情報の取り扱いについては、
              <a href="https://policies.google.com/technologies/ads?hl=ja" {...external}>
                Googleの広告に関するポリシー
              </a>
              をご覧ください。
            </li>
            <li>広告は、掲載データとは区別して表示します。広告主が、掲載するデータの内容や選手・学校の表示順に関与することはありません。</li>
          </ul>
        </section>

        <section className="jbaListB-section jbaListB-about">
          <div className="jbaListB-sectionHead">
            <h2>アクセス解析について</h2>
          </div>
          <ul>
            <li>
              本サイトは、利用状況を把握してサイトを改善するために、Googleのアクセス解析ツール「Google Analytics」を利用しています。
            </li>
            <li>Google AnalyticsはCookieを使用してデータを収集します。このデータは匿名で収集され、個人を特定するものではありません。</li>
            <li>
              Cookieはブラウザの設定で無効にできます。また、
              <a href="https://tools.google.com/dlpage/gaoptout?hl=ja" {...external}>
                Google Analyticsオプトアウト アドオン
              </a>
              を使うと、Google Analyticsによるデータ収集を止められます。詳しくは
              <a href="https://policies.google.com/technologies/partner-sites?hl=ja" {...external}>
                Googleのポリシーと規約
              </a>
              をご覧ください。
            </li>
          </ul>
        </section>

        <section className="jbaListB-section jbaListB-about">
          <div className="jbaListB-sectionHead">
            <h2>お問い合わせ・訂正依頼で受け取る情報</h2>
          </div>
          <ul>
            <li>
              <a href={correctionFormUrl} {...external}>
                訂正・削除依頼フォーム
              </a>
              （Googleフォーム）でご記入いただいた内容は、掲載内容の確認・訂正と、ご返信のためだけに使います。
            </li>
            <li>法令に基づく場合を除き、ご本人の同意なく第三者に提供することはありません。</li>
          </ul>
        </section>

        <section className="jbaListB-section jbaListB-about">
          <div className="jbaListB-sectionHead">
            <h2>免責事項</h2>
          </div>
          <ul>
            <li>
              掲載情報は公開資料に基づいて出典とともに記録していますが、その正確性・完全性を保証するものではありません。誤りにお気づきの場合は、
              <a href="/about#corrections">訂正・削除のご依頼</a>からお知らせください。
            </li>
            <li>本サイトからリンクしている外部サイトの内容について、本サイトは責任を負いません。</li>
          </ul>
        </section>

        <section className="jbaListB-section jbaListB-about">
          <div className="jbaListB-sectionHead">
            <h2>改定</h2>
          </div>
          <p>本ポリシーの内容は、必要に応じて変更することがあります。変更後の内容は、このページに掲載した時点から適用します。</p>
          <p>最終更新日：{UPDATED_AT}</p>
        </section>
      </div>

      <SiteFooter />
    </main>
  );
}
