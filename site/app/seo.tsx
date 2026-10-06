/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import { Fragment } from 'react';
import { organizationCategory } from './organization-category';
import { organizationDisplayName, type PublicOrganization, type PublicPlayer } from './public-data';
import { siteUrl } from './site-url';

export { siteUrl };

// ページ側でopenGraphを指定するとlayoutの値が丸ごと置き換わるため、共通項目をここから展開する。
export const baseOpenGraph = { siteName: 'Rosterline', locale: 'ja_JP', type: 'website' } as const;

// サイト共通ヘッダー（B案）。全ページで同一の見た目・ナビゲーションにするため、
// /players, /organizations で先行実装していたヘッダーをここに集約する。
export function SiteHeader({ active }: { active?: 'players' | 'organizations' | 'rankings' }) {
  return (
    <header className="jbaListB-header">
      <a href="/" className="jbaListB-brand">
        <span className="jbaListB-brandMark">R</span>
        <span className="jbaListB-brandName">Rosterline</span>
      </a>
      <nav className="jbaListB-nav">
        <a href="/players" aria-current={active === 'players' ? 'page' : undefined}>選手</a>
        <a href="/organizations" aria-current={active === 'organizations' ? 'page' : undefined}>組織</a>
        <a href="/rankings" aria-current={active === 'rankings' ? 'page' : undefined}>ランキング</a>
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

// 非公式であることの注記（docs/BRAND_NAME_PROPOSAL_V0.1.mdの免責表記案）。フッターとAboutページで使う。
export const DISCLAIMER_JA =
  '本サイトは、公益財団法人日本バスケットボール協会（JBA）、B.LEAGUE、その他の競技団体とは関係のない、個人が運営する非公式アーカイブです。掲載情報は公開資料に基づいており、出典を各ページに記載しています。';
export const DISCLAIMER_EN =
  'This is an independent, unofficial archive and is not affiliated with the Japan Basketball Association (JBA), B.LEAGUE, or any other governing body.';

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
          <a href="/rankings/high-school">出身高校ランキング</a>
          <a href="/rankings/university">出身大学ランキング</a>
          <a href="/about">このサイトについて</a>
        </div>
      </div>
      <p className="jbaListB-footerDisclaimer">{DISCLAIMER_JA}</p>
    </footer>
  );
}

// 組織の種類（表示文言と構造化データの型に使う）。
// 学校の区分は組織名からの自動判定（organization-category.ts）。海外の学校は区分が「海外」「その他」に
// なるため、名前からも学校かどうかを見る。
export type OrganizationKind = 'highSchool' | 'university' | 'school' | 'club' | 'unknown';

export function organizationKind(organization: PublicOrganization): OrganizationKind {
  const category = organizationCategory(organization.name);
  if (category === 'hs') return 'highSchool';
  if (category === 'univ') return 'university';
  if (category === 'club') return 'club';
  const looksLikeSchool =
    /(大学|大$|高校|高等学校|中学校|学園|学院|専門学校|カレッジ|スクール|ユニバーシティ|アカデミー|College|University|School|Academy|Institute|Prep)/i.test(
      organization.name,
    );
  return looksLikeSchool ? 'school' : 'unknown';
}

// 組織ページをindexする最低人数（SEO_SPEC_V1.0「ページ品質ゲーティング」：所属選手3名以上）。
// 未満のページはnoindex（リンクはたどらせる）にし、サイトマップにも載せない。
export const ORGANIZATION_INDEX_MIN_PLAYERS = 3;

export function isOrganizationIndexable(playerCount: number): boolean {
  return playerCount >= ORGANIZATION_INDEX_MIN_PLAYERS;
}

// 組織ページのtitle・description。
// 学校は「〇〇高校 Bリーガー」「〇〇大学 出身 選手」のような検索に合わせて「出身」を使い、
// クラブ等は「所属選手」とする。網羅していると誤解されないよう「記録のある」「確認できた」と書き、
// 「歴代」「全員」などの表現は使わない。
export function organizationPageMeta(organization: PublicOrganization, playerCount: number) {
  const kind = organizationKind(organization);
  const group = kind === 'club' ? 'club' : kind === 'unknown' ? 'unknown' : 'school';
  const name = organizationDisplayName(organization);
  const titles = {
    school: `${name}出身のバスケ選手一覧（${playerCount}人）`,
    club: `${name}の所属選手一覧（${playerCount}人）`,
    unknown: `${name}の在籍選手一覧（${playerCount}人）`,
  };
  const descriptions = {
    school: `${organization.name}に在籍記録のある選手${playerCount}人の進路（大学・クラブ）と経歴を、出典とともに掲載しています。`,
    club: `${organization.name}に所属記録のある選手${playerCount}人の出身校・経歴を、出典とともに掲載しています。`,
    unknown: `${organization.name}に在籍記録のある選手${playerCount}人の経歴を、出典とともに掲載しています。`,
  };
  return { title: titles[group], description: `${descriptions[group]}掲載は本サイトに登録済みの選手のみです。` };
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

// 組織の種類に応じたschema.orgの型（SEO_SPEC_V1.0：学校はEducationalOrganization、クラブはSportsTeam）。
// 高校・大学はEducationalOrganizationの下位型（HighSchool・CollegeOrUniversity）を使う。
const ORGANIZATION_SCHEMA_TYPE: Record<OrganizationKind, string> = {
  highSchool: 'HighSchool',
  university: 'CollegeOrUniversity',
  school: 'EducationalOrganization',
  club: 'SportsTeam',
  unknown: 'Organization',
};

export function organizationJsonLd(organization: PublicOrganization) {
  const path = `/organizations/${organization.slug}`;
  const kind = organizationKind(organization);
  return {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': ORGANIZATION_SCHEMA_TYPE[kind],
        '@id': `${siteUrl}${path}#organization`,
        name: organization.name,
        ...(organization.currentName ? { alternateName: organization.currentName.currentName } : {}),
        url: `${siteUrl}${path}`,
        ...(kind === 'club' ? { sport: 'Basketball' } : {}),
      },
      breadcrumbJsonLd([
        { name: 'ホーム', path: '/' },
        { name: '組織一覧', path: '/organizations' },
        { name: organization.name, path },
      ]),
    ],
  };
}
