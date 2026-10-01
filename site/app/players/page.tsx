/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import type { Metadata } from 'next';
import { getPrimaryCareer, masterApprovals, masterPublication, players } from '../public-data';
import { baseOpenGraph, breadcrumbJsonLd, JsonLd, SiteBreadcrumb, SiteFooter, SiteHeader, siteUrl } from '../seo';
import { organizationCategory, ORGANIZATION_CATEGORY_ORDER } from '../organization-category';
import { PlayersListView, type PlayerRow } from './PlayersListView';

// 「YYYY年M月D日」形式の生年月日を、文字列比較でそのまま年齢順に並べられる
// 「YYYY-MM-DD」形式に変換する。形式外の値（未確認等）はnullを返し、並び替え対象から除外する。
function parseBirthDate(value: string | undefined): string | null {
  const match = value?.match(/^(\d{4})年(\d{1,2})月(\d{1,2})日$/);
  if (!match) return null;
  const [, year, month, day] = match;
  return `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
}

// Masterデータの承認日（新着順の並び替えに使用）。経歴追加の承認（enrichmentApprovalIds）も
// 含めた最新日を採用する。Candidateデータは承認日を持たないためnull（並び替え時は末尾）。
function latestApprovedAt(player: (typeof players)[number]): string | null {
  if (player.dataStatus !== 'master') return null;
  const approvals = masterApprovals as Record<string, { approvedAt: string }>;
  const ids = [player.approvalId, ...(player.enrichmentApprovalIds ?? [])].filter((id): id is string => Boolean(id));
  const dates = ids.map((id) => approvals[id]?.approvedAt).filter((date): date is string => Boolean(date));
  if (dates.length === 0) return masterPublication.approvedAt;
  return dates.reduce((latest, date) => (date > latest ? date : latest));
}

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
    birthDate: parseBirthDate(player.facts.find((fact) => fact.label === '生年月日')?.value),
    approvedAt: latestApprovedAt(player),
    careerCount: player.careers.length,
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
