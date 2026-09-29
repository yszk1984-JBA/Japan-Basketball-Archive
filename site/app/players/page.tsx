/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import type { Metadata } from 'next';
import { getPrimaryCareer, players } from '../public-data';
import { baseOpenGraph, breadcrumbJsonLd, JsonLd, SiteBreadcrumb, SiteFooter, SiteHeader, siteUrl } from '../seo';
import { organizationCategory, ORGANIZATION_CATEGORY_ORDER } from '../organization-category';
import { PlayersListView, type PlayerRow } from './PlayersListView';

const title = `選手一覧（${players.length}人）`;
const description = `日本バスケットボール選手${players.length}人の所属・経歴を、出典とともに掲載しています。高校・大学・プロの所属記録をたどれます。`;

export const metadata: Metadata = {
  title,
  description,
  alternates: { canonical: '/players' },
  openGraph: { ...baseOpenGraph, title, description, url: '/players' },
};

// 表示用の行データをサーバー側で作る。カテゴリーは組織名からの表示専用の
// 推定であり（organization-category.ts参照）、Master/Candidateのデータ
// スキーマそのものには手を入れていない。
//
// categoriesは経歴に登場した組織すべてから推定する（現在の所属だけでなく、
// 高校→大学→クラブのような経歴全体を対象にする）。これにより「高校」で
// 絞り込んだときに、現在はプロ所属の選手も含めた出身校ベースの一覧になる。
function toRow(player: (typeof players)[number]): PlayerRow {
  const primary = getPrimaryCareer(player);
  const categories = [
    ...new Set(
      player.careers
        .filter((career) => career.organization)
        .map((career) => organizationCategory(career.organization as string)),
    ),
  ].sort((left, right) => ORGANIZATION_CATEGORY_ORDER.indexOf(left) - ORGANIZATION_CATEGORY_ORDER.indexOf(right));

  return {
    id: player.id,
    slug: player.slug,
    name: player.name,
    org: primary?.organization ?? null,
    primaryCategory: primary?.organization ? organizationCategory(primary.organization) : null,
    categories,
    status: player.dataStatus,
    sources: new Set(player.careers.flatMap((career) => career.sourceIds)).size,
  };
}

export default function PlayersIndexPage() {
  const rows = players.map(toRow);

  return (
    <main className="jbaListB-page">
      <JsonLd
        data={{
          '@context': 'https://schema.org',
          '@graph': [
            {
              '@type': 'CollectionPage',
              name: title,
              url: `${siteUrl}/players`,
              description,
            },
            breadcrumbJsonLd([
              { name: 'ホーム', path: '/' },
              { name: '選手一覧', path: '/players' },
            ]),
          ],
        }}
      />

      <SiteHeader active="players" />

      <SiteBreadcrumb crumbs={[{ label: '選手一覧' }]} />

      <div className="jbaListB-main">
        <div>
          <p className="jbaListB-eyebrow">Players</p>
          <h1 className="jbaListB-h1">選手一覧</h1>
        </div>

        <PlayersListView rows={rows} totalCount={players.length} />

        <p className="jbaListB-note">
          ※ このページはCANDIDATE段階を含むデータを掲載しています。Yuichiによる正式承認（Governance
          v1.0のVERIFIED・Human approvalを経たMaster化）前の情報が含まれます。
        </p>
      </div>

      <SiteFooter />
    </main>
  );
}
