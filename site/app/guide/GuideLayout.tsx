/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import type { Metadata } from 'next';
import type { ReactNode } from 'react';
import { AffiliateNotice } from '../affiliate/AffiliateSlot';
import { formatJaDate } from '../columns/ColumnLayout';
import { References } from '../columns/References';
import { baseOpenGraph, breadcrumbJsonLd, JsonLd, SiteBreadcrumb, SiteFooter, SiteHeader, siteUrl } from '../seo';
import { ShareButtons } from '../ShareButtons';
import { GUIDE_CATEGORY_LABELS, getGuide, guidePath } from './guide-data';

export function guideMetadata(slug: string): Metadata {
  const guide = getGuide(slug);
  const path = guidePath(slug);
  return {
    title: guide.title,
    description: guide.description,
    alternates: { canonical: path },
    openGraph: { ...baseOpenGraph, title: guide.title, description: guide.description, url: path, type: 'article' },
  };
}

type Reference = { label: string; publisher: string; date: string; href: string };

// Guide記事の共通レイアウト。コラム（ColumnLayout）とは見出し・パンくず・一覧を分ける。
// 広告がある記事だけ、記事上部にPR表記（AffiliateNotice）が出る。広告枠は記事本文の中に各記事で置く。
export function GuideLayout({
  slug,
  children,
  references,
  related,
}: {
  slug: string;
  children: ReactNode;
  references: readonly Reference[];
  related: readonly { label: string; href: string }[];
}) {
  const guide = getGuide(slug);
  const path = guidePath(slug);
  const updated = guide.updatedAt ?? guide.publishedAt;
  return (
    <main className="jbaListB-page">
      <JsonLd
        data={{
          '@context': 'https://schema.org',
          '@graph': [
            breadcrumbJsonLd([
              { name: 'ホーム', path: '/' },
              { name: 'ガイド', path: '/guide' },
              { name: guide.title, path },
            ]),
            {
              '@type': 'Article',
              headline: guide.title,
              description: guide.description,
              datePublished: guide.publishedAt,
              dateModified: updated,
              url: `${siteUrl}${path}`,
              author: { '@type': 'Organization', name: 'Rosterline', url: siteUrl },
              publisher: { '@type': 'Organization', name: 'Rosterline', url: siteUrl },
            },
          ],
        }}
      />
      <SiteHeader active="guide" />
      <SiteBreadcrumb crumbs={[{ label: 'ガイド', href: '/guide' }, { label: guide.title }]} />

      <div className="jbaListB-main">
        <div>
          <p className="jbaListB-eyebrow">Guide｜{GUIDE_CATEGORY_LABELS[guide.category]}</p>
          <h1 className="jbaListB-h1">{guide.title}</h1>
          <p className="jbaListB-articleMeta">
            公開：{formatJaDate(guide.publishedAt)}　｜　最終更新：{formatJaDate(updated)}　｜　規則・メーカー情報の確認：
            {formatJaDate(guide.checkedAt)}　｜　文：Rosterline運営者
          </p>
          <ShareButtons url={`${siteUrl}${path}`} text={guide.title} hashtags={['バスケ']} />
        </div>

        <AffiliateNotice pageType="guide" pageKey={slug} />

        <article className="jbaListB-about jbaListB-article" style={{ display: 'grid', gap: 18 }}>
          {children}
          <References items={references} />
        </article>

        <div className="jbaListB-rankNotes">
          <p>この記事について</p>
          <ul>
            <li>競技規則・メーカーの公開情報をもとに、{formatJaDate(guide.checkedAt)}時点で確認できた内容を書いています。規則は改定されることがあるため、最新の内容は出典でご確認ください。</li>
            <li>出場する大会で使うボールは、大会の要項で指定されることがあります。迷ったときは、所属チームの指導者や大会の主催者に確認してください。</li>
            <li>特定の商品の使用感やおすすめの順位は掲載していません。</li>
          </ul>
        </div>

        <div className="jbaListB-routePoints">
          <p>あわせて読む</p>
          <ul>
            {related.map((link) => (
              <li key={link.href}>
                <a href={link.href}>{link.label}</a>
              </li>
            ))}
            <li>
              <a href="/guide">ほかのガイドを読む</a>
            </li>
          </ul>
        </div>
      </div>

      <SiteFooter />
    </main>
  );
}
