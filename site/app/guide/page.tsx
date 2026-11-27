/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import type { Metadata } from 'next';
import { formatJaDate } from '../columns/ColumnLayout';
import { baseOpenGraph, breadcrumbJsonLd, JsonLd, SiteBreadcrumb, SiteFooter, SiteHeader } from '../seo';
import { GUIDE_CATEGORY_LABELS, guidePath, GUIDES } from './guide-data';

const title = 'ガイド';
const description =
  'バスケットボールの用品選び・観戦・遠征に役立つ実用ガイドです。競技規則やメーカーの公開情報など、確かめられる情報をもとにまとめています。';

export const metadata: Metadata = {
  title,
  description,
  alternates: { canonical: '/guide' },
  openGraph: { ...baseOpenGraph, title, description, url: '/guide' },
};

export default function GuideIndexPage() {
  const guides = [...GUIDES].sort((left, right) =>
    (right.updatedAt ?? right.publishedAt).localeCompare(left.updatedAt ?? left.publishedAt),
  );
  return (
    <main className="jbaListB-page">
      <JsonLd
        data={{
          '@context': 'https://schema.org',
          '@graph': [
            breadcrumbJsonLd([
              { name: 'ホーム', path: '/' },
              { name: title, path: '/guide' },
            ]),
          ],
        }}
      />
      <SiteHeader active="guide" />
      <SiteBreadcrumb crumbs={[{ label: title }]} />

      <div className="jbaListB-main">
        <div>
          <p className="jbaListB-eyebrow">Guide</p>
          <h1 className="jbaListB-h1">{title}</h1>
        </div>
        <p className="jbaListB-lede">{description}</p>
        <p className="jbaListB-lede" style={{ fontSize: 13 }}>
          選手の経歴データをもとにした解説記事は<a href="/columns">コラム</a>にまとめています。
        </p>

        <div className="jbaListB-table">
          {guides.map((guide) => (
            <a href={guidePath(guide.slug)} key={guide.slug} className="jbaListB-row jbaListB-rankIndexGrid">
              <div className="jbaListB-rowName">{guide.title}</div>
              <div className="jbaListB-rowMuted">
                {GUIDE_CATEGORY_LABELS[guide.category]}｜{formatJaDate(guide.updatedAt ?? guide.publishedAt)}更新｜
                {guide.description}
              </div>
            </a>
          ))}
        </div>
      </div>

      <SiteFooter />
    </main>
  );
}
