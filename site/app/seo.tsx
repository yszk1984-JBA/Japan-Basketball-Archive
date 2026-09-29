/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import { Fragment } from 'react';
import type { PublicOrganization, PublicPlayer } from './public-data';

export const siteUrl = 'https://japanbasketballarchive.com';

// ページ側でopenGraphを指定するとlayoutの値が丸ごと置き換わるため、共通項目をここから展開する。
export const baseOpenGraph = { siteName: 'Rosterline', locale: 'ja_JP', type: 'website' } as const;

// サイト共通ヘッダー（B案）。全ページで同一の見た目・ナビゲーションにするため、
// /players, /organizations で先行実装していたヘッダーをここに集約する。
export function SiteHeader({ active }: { active?: 'players' | 'organizations' }) {
  return (
    <header className="jbaListB-header">
      <a href="/" className="jbaListB-brand">
        <span className="jbaListB-brandMark">R</span>
        <span className="jbaListB-brandName">Rosterline</span>
      </a>
      <nav className="jbaListB-nav">
        <a href="/players" aria-current={active === 'players' ? 'page' : undefined}>選手</a>
        <a href="/organizations" aria-current={active === 'organizations' ? 'page' : undefined}>組織</a>
      </nav>
    </header>
  );
}

type BreadcrumbItem = { label: string; href?: string };

// サイト共通パンくず（B案）。最後の要素はリンクなし（現在ページ）として扱う。
export function SiteBreadcrumb({ crumbs }: { crumbs: readonly BreadcrumbItem[] }) {
  return (
    <div className="jbaListB-breadcrumb">
      <a href="/">TOP</a>
      {crumbs.map((crumb) => (
        <Fragment key={crumb.label}>
          {' ／ '}
          {crumb.href ? <a href={crumb.href}>{crumb.label}</a> : <span>{crumb.label}</span>}
        </Fragment>
      ))}
    </div>
  );
}

// サイト共通フッター（B案）。
export function SiteFooter() {
  return (
    <footer className="jbaListB-footer">
      <div className="jbaListB-footerInner">
        <div>
          <div className="jbaListB-footerTitle">Rosterline</div>
          <div>日本バスケットボールの人物と所属を、出典とともに記録するアーカイブです。</div>
        </div>
        <div className="jbaListB-footerLinks">
          <a href="/players">選手一覧</a>
          <a href="/organizations">組織一覧</a>
        </div>
      </div>
    </footer>
  );
}

// JSON-LD（構造化データ）を<script type="application/ld+json">として出力する。
// `<`をエスケープして、データ内の文字列がscriptタグを閉じないようにする。
export function JsonLd({ data }: { data: object }) {
  return (
    <script
      type="application/ld+json"
      // oxlint-disable-next-line react/no-danger -- JSON-LD must be emitted as raw JSON text.
      dangerouslySetInnerHTML={{ __html: JSON.stringify(data).replace(/</g, '\\u003c') }}
    />
  );
}

// 経歴に登場する組織名を、登録順・重複なしで最大limit件返す。
// 期間未確認のCareerが多いため、時系列を断定する「→」ではなく「・」で並べる。
export function careerOrganizationNames(player: PublicPlayer, limit = 3): string[] {
  const names: string[] = [];
  for (const career of player.careers) {
    if (career.organization && !names.includes(career.organization)) names.push(career.organization);
  }
  return names.slice(0, limit);
}

type Crumb = { name: string; path: string };

export function breadcrumbJsonLd(crumbs: readonly Crumb[]) {
  return {
    '@type': 'BreadcrumbList',
    itemListElement: crumbs.map((crumb, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      name: crumb.name,
      item: `${siteUrl}${crumb.path}`,
    })),
  };
}

// 選手ページのJSON-LD。
// Governance v1.0に従い、Person（事実の主張）はMaster Dataの人物だけに出力する。
// 候補データの人物はパンくずのみ。生年月日は検索上の効果が小さいため構造化データには含めない。
export function playerJsonLd(
  player: PublicPlayer,
  organizationSlugFor: (organizationId: string | undefined) => string | undefined,
) {
  const url = `${siteUrl}/players/${player.slug}`;
  const graph: object[] = [
    breadcrumbJsonLd([
      { name: 'ホーム', path: '/' },
      { name: '選手一覧', path: '/players' },
      { name: player.name, path: `/players/${player.slug}` },
    ]),
  ];

  if (player.dataStatus === 'master') {
    const englishName = player.facts.find((fact) => fact.label === '英字表記')?.value;
    const seen = new Set<string>();
    const affiliations = player.careers.flatMap((career) => {
      if (!career.organization || career.status !== 'master') return [];
      const key = career.organizationId ?? career.organization;
      if (seen.has(key)) return [];
      seen.add(key);
      const slug = organizationSlugFor(career.organizationId);
      return [{
        '@type': 'Organization',
        name: career.organization,
        ...(slug ? { url: `${siteUrl}/organizations/${slug}` } : {}),
      }];
    });

    graph.unshift({
      '@type': 'Person',
      '@id': `${url}#person`,
      name: player.name,
      ...(englishName ? { alternateName: englishName } : {}),
      url,
      ...(affiliations.length ? { affiliation: affiliations } : {}),
    });
  }

  return { '@context': 'https://schema.org', '@graph': graph };
}

export function organizationJsonLd(organization: PublicOrganization) {
  const path = `/organizations/${organization.slug}`;
  return {
    '@context': 'https://schema.org',
    '@graph': [
      { '@type': 'Organization', '@id': `${siteUrl}${path}#organization`, name: organization.name, url: `${siteUrl}${path}` },
      breadcrumbJsonLd([
        { name: 'ホーム', path: '/' },
        { name: '組織一覧', path: '/organizations' },
        { name: organization.name, path },
      ]),
    ],
  };
}
