/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import type { Metadata } from 'next';
import { players } from '../public-data';
import {
  baseOpenGraph,
  breadcrumbJsonLd,
  DISCLAIMER_EN,
  DISCLAIMER_JA,
  JsonLd,
  SiteBreadcrumb,
  SiteFooter,
  SiteHeader,
  siteUrl,
} from '../seo';

const title = 'このサイトについて';
const description =
  'Rosterlineは、日本バスケットボール選手の所属と経歴を出典とともに記録する、個人運営の非公式アーカイブです。掲載データの考え方と、競技団体とは関係がないことを説明します。';

export const metadata: Metadata = {
  title,
  description,
  alternates: { canonical: '/about' },
  openGraph: { ...baseOpenGraph, title, description, url: '/about' },
};

export default function AboutPage() {
  const masterCount = players.filter((player) => player.dataStatus === 'master').length;

  return (
    <main className="jbaListB-page">
      <JsonLd
        data={{
          '@context': 'https://schema.org',
          '@graph': [
            {
              '@type': 'AboutPage',
              name: title,
              url: `${siteUrl}/about`,
              isPartOf: { '@type': 'WebSite', name: 'Rosterline', url: siteUrl },
            },
            breadcrumbJsonLd([
              { name: 'ホーム', path: '/' },
              { name: title, path: '/about' },
            ]),
          ],
        }}
      />
      <SiteHeader />

      <SiteBreadcrumb crumbs={[{ label: title }]} />

      <div className="jbaListB-main">
        <div>
          <p className="jbaListB-eyebrow">About</p>
          <h1 className="jbaListB-h1">{title}</h1>
        </div>

        <section className="jbaListB-section jbaListB-about">
          <div className="jbaListB-sectionHead">
            <h2>Rosterlineとは</h2>
          </div>
          <p>
            Rosterline（ロスターライン）は、日本のバスケットボール選手が、どの学校・大学・クラブに所属してきたかを、出典とともに記録するアーカイブです。選手ごとの経歴をたどったり、学校やクラブからその出身選手を探したりできます。
          </p>
        </section>

        <section className="jbaListB-section jbaListB-about">
          <div className="jbaListB-sectionHead">
            <h2>掲載データの考え方</h2>
          </div>
          <ul>
            <li>所属や経歴には、裏付けとなる出典（公式サイト・大会資料・専門媒体など）を記載しています。出典のない情報は推測で埋めません。</li>
            <li>
              確認を終えたデータ（現在{masterCount}人分）と、確認中のデータを分けて掲載しています。確認中のデータには、その旨を表示しています。
            </li>
            <li>掲載しているのは本サイトに登録済みの選手だけです。人数やランキングは、すべての選手を網羅したものではありません。</li>
            <li>選手の写真は掲載していません。</li>
          </ul>
        </section>

        <section className="jbaListB-section jbaListB-about">
          <div className="jbaListB-sectionHead">
            <h2>非公式のアーカイブです</h2>
          </div>
          <p>{DISCLAIMER_JA}</p>
          <p className="jbaListB-aboutEn" lang="en">
            {DISCLAIMER_EN}
          </p>
        </section>
      </div>

      <SiteFooter />
    </main>
  );
}
