/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import type { Metadata } from 'next';
import { baseOpenGraph, breadcrumbJsonLd, JsonLd, SiteBreadcrumb, SiteFooter, SiteHeader } from '../seo';
import { formatJaDate } from './ColumnLayout';
import { columnPath, COLUMNS } from './columns-data';

const title = 'コラム';
const description =
  'Rosterlineの確認済みデータをもとに、B.LEAGUE選手の出身校・進路・所属の傾向を読み解く解説記事です。';

export const metadata: Metadata = {
  title,
  description,
  alternates: { canonical: '/columns' },
  openGraph: { ...baseOpenGraph, title, description, url: '/columns' },
};

export default function ColumnsPage() {
  const columns = [...COLUMNS].sort((left, right) => right.publishedAt.localeCompare(left.publishedAt));
  return (
    <main className="jbaListB-page">
      <JsonLd
        data={{
          '@context': 'https://schema.org',
          '@graph': [
            breadcrumbJsonLd([
              { name: 'ホーム', path: '/' },
              { name: title, path: '/columns' },
            ]),
          ],
        }}
      />
      <SiteHeader active="columns" />
      <SiteBreadcrumb crumbs={[{ label: title }]} />

      <div className="jbaListB-main">
        <div>
          <p className="jbaListB-eyebrow">Column</p>
          <h1 className="jbaListB-h1">{title}</h1>
        </div>
        <p className="jbaListB-lede">{description}</p>

        <div className="jbaListB-table">
          {columns.map((column) => (
            <a href={columnPath(column.slug)} key={column.slug} className="jbaListB-row jbaListB-rankIndexGrid">
              <div className="jbaListB-rowName">{column.title}</div>
              <div className="jbaListB-rowMuted">
                {formatJaDate(column.publishedAt)}｜{column.description}
              </div>
            </a>
          ))}
        </div>
      </div>

      <SiteFooter />
    </main>
  );
}
