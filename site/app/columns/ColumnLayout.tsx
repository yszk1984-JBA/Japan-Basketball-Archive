/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import type { Metadata } from 'next';
import type { ReactNode } from 'react';
import { baseOpenGraph, breadcrumbJsonLd, JsonLd, SiteBreadcrumb, SiteFooter, SiteHeader, siteUrl } from '../seo';
import { ShareButtons } from '../ShareButtons';
import { columnPath, getColumn } from './columns-data';

export function columnMetadata(slug: string): Metadata {
  const column = getColumn(slug);
  const path = columnPath(slug);
  return {
    title: column.title,
    description: column.description,
    alternates: { canonical: path },
    openGraph: { ...baseOpenGraph, title: column.title, description: column.description, url: path, type: 'article' },
  };
}

export function formatJaDate(isoDate: string): string {
  const [year, month, day] = isoDate.slice(0, 10).split('-');
  return `${year}年${Number(month)}月${Number(day)}日`;
}

export function ColumnLayout({
  slug,
  children,
  related,
}: {
  slug: string;
  children: ReactNode;
  related: readonly { label: string; href: string }[];
}) {
  const column = getColumn(slug);
  const path = columnPath(slug);
  return (
    <main className="jbaListB-page">
      <JsonLd
        data={{
          '@context': 'https://schema.org',
          '@graph': [
            breadcrumbJsonLd([
              { name: 'ホーム', path: '/' },
              { name: 'コラム', path: '/columns' },
              { name: column.title, path },
            ]),
            {
              '@type': 'Article',
              headline: column.title,
              description: column.description,
              datePublished: column.publishedAt,
              dateModified: column.updatedAt ?? column.publishedAt,
              url: `${siteUrl}${path}`,
              author: { '@type': 'Organization', name: 'Rosterline', url: siteUrl },
              publisher: { '@type': 'Organization', name: 'Rosterline', url: siteUrl },
            },
          ],
        }}
      />
      <SiteHeader active="columns" />
      <SiteBreadcrumb crumbs={[{ label: 'コラム', href: '/columns' }, { label: column.title }]} />

      <div className="jbaListB-main">
        <div>
          <p className="jbaListB-eyebrow">Column</p>
          <h1 className="jbaListB-h1">{column.title}</h1>
          <p className="jbaListB-articleMeta">
            公開：{formatJaDate(column.publishedAt)}
            {column.updatedAt ? `（更新：${formatJaDate(column.updatedAt)}）` : ''}　｜　集計：{formatJaDate(column.dataAsOf)}
            時点の登録データ　｜　文：Rosterline運営者
          </p>
          <ShareButtons url={`${siteUrl}${path}`} text={column.title} hashtags={['Bリーグ']} />
        </div>

        <article className="jbaListB-about jbaListB-article" style={{ display: 'grid', gap: 18 }}>
          {children}
        </article>

        <div className="jbaListB-rankNotes">
          <p>集計の前提</p>
          <ul>
            <li>本サイトに登録済み（確認済みのデータ）の選手だけを数えています。登録されていない選手は含まれません。</li>
            <li>数字は{formatJaDate(column.dataAsOf)}時点の登録データです。最新の人数は各ランキング・各ページでご確認ください。</li>
            <li>学校・クラブの名称は、選手が在籍していた当時の名称です。</li>
          </ul>
        </div>

        <div className="jbaListB-routePoints">
          <p>この記事で使ったデータ</p>
          <ul>
            {related.map((link) => (
              <li key={link.href}>
                <a href={link.href}>{link.label}</a>
              </li>
            ))}
            <li>
              <a href="/columns">ほかのコラムを読む</a>
            </li>
          </ul>
        </div>
      </div>

      <SiteFooter />
    </main>
  );
}
