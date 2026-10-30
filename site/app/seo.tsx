/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import { Fragment } from 'react';
import { isSchoolName, organizationCategory } from './organization-category';
import { getPrimaryCareer, organizationDisplayName, type PublicOrganization, type PublicPlayer } from './public-data';
import { siteUrl } from './site-url';

export { siteUrl };

// ページ側でopenGraphを指定するとlayoutの値が丸ごと置き換わるため、共通項目をここから展開する。
// 共通のシェア画像（1200×630、public/og-default.png）。ページ固有の画像を作るまでは全ページでこれを使う。
export const defaultOgImage = { url: '/og-default.png', width: 1200, height: 630, alt: 'Rosterline｜選手と所属を、出典からたどる。' };
export const baseOpenGraph = {
  siteName: 'Rosterline',
  locale: 'ja_JP',
  type: 'website' as const,
  images: [defaultOgImage],
};

// サイト共通ヘッダー（B案）。全ページで同一の見た目・ナビゲーションにするため、
// /players, /organizations で先行実装していたヘッダーをここに集約する。
// Rosterlineのロゴマーク（public/favicon.svgと同じ図柄）。Rと、経歴の年表（点の並び。右端の橙は現在の所属）。
export function BrandMark({ size, className }: { size: number; className?: string }) {
  return (
    <svg viewBox="0 0 64 64" width={size} height={size} className={className} aria-hidden="true" focusable="false">
      <rect width="64" height="64" rx="14" fill="#1D5FD6" />
      <path
        d="M23 41V13h10.5a7.5 7.5 0 0 1 0 15H23M32 28l9 13"
        fill="none"
        stroke="#FFFFFF"
        strokeWidth="6"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path d="M14 52h36" stroke="#FFFFFF" strokeOpacity="0.45" strokeWidth="2.5" strokeLinecap="round" />
      <circle cx="18" cy="52" r="3.2" fill="#FFFFFF" />
      <circle cx="32" cy="52" r="3.2" fill="#FFFFFF" />
      <circle cx="46" cy="52" r="4" fill="#F5A524" />
    </svg>
  );
}

export function SiteHeader({ active }: { active?: 'players' | 'organizations' | 'rankings' }) {
  return (
    <header className="jbaListB-header">
      <a href="/" className="jbaListB-brand">
        <BrandMark size={28} className="jbaListB-brandMark" />
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
          <a href="/rankings/high-school-to-university">高校→大学の進学ルート</a>
          <a href="/about">このサイトについて</a>
          <a href="/about#corrections">訂正・削除のご依頼</a>
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
  return isSchoolName(organization.name) ? 'school' : 'unknown';
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
// highlights：「主な出身高校：〇〇（3人）、…」のような、ページ固有の要約（descriptionの末尾に付ける）。
export function organizationPageMeta(organization: PublicOrganization, playerCount: number, highlights?: string) {
  const kind = organizationKind(organization);
  const group = kind === 'club' ? 'club' : kind === 'unknown' ? 'unknown' : 'school';
  const name = organizationDisplayName(organization);
  const titles = {
    school: `${name}出身のバスケ選手一覧（${playerCount}人）`,
    club: `${name}の所属選手と出身校一覧（${playerCount}人）`,
    unknown: `${name}の在籍選手一覧（${playerCount}人）`,
  };
  const descriptions = {
    school: `${organization.name}に在籍記録のある選手${playerCount}人の進路（大学・クラブ）と経歴を、出典とともに掲載しています。`,
    club: `${organization.name}に所属記録のある選手${playerCount}人の出身校・経歴を、出典とともに掲載しています。`,
    unknown: `${organization.name}に在籍記録のある選手${playerCount}人の経歴を、出典とともに掲載しています。`,
  };
  const summary = highlights ? `${highlights}。` : '';
  return { title: titles[group], description: `${descriptions[group]}${summary}掲載は本サイトに登録済みの選手のみです。` };
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

// 選手ページのtitle・description。
// titleは出身校がある選手は「選手名の経歴・出身校｜〇〇高→〇〇大→現所属」のように進路を並べる
// （「〇〇 出身校」「〇〇 高校」のような検索意図に合わせるため。2026-10-30、Yuichi依頼）。
// 出身校を2校までに絞るのは、SERP表示でのtitle切れを避けるため（直近2校＝高校・大学を想定）。
// 出身校の記録が無い選手（海外出身で学校記録が未確認等）は、従来どおり現在（直近）の所属のみで表示する。
// 「現所属」と断定しないのは、引退した選手や、所属の終了を確認できていない選手がいるため。
export function playerPageMeta(player: PublicPlayer, sourceCount: number) {
  const latest = getPrimaryCareer(player)?.organization ?? undefined;
  const schoolCareers: { name: string; startYear: number | null | undefined }[] = [];
  for (const career of player.careers) {
    const name = career.organization;
    if (!name || name === latest || schoolCareers.some((school) => school.name === name)) continue;
    if (isSchoolName(name)) schoolCareers.push({ name, startYear: career.startYear });
  }
  // career配列の並び順は必ずしも年代順ではない（承認スプリントごとに後から追記されるため）。
  // また、大学の在籍期間は高校よりも未確認（startYearがnull）のことが多く、開始年だけで
  // 並べ替えると「大学→高校」のように逆順になってしまう。そのため、まず学校の種別
  // （高校相当→大学相当）で並べ、同じ種別どうしは開始年（未確認の場合は元の並び順）で
  // 並べ替える。種別は名称のパターンからの表示専用の推定であり、Master/Candidateの
  // データ自体を変更するものではない（organization-category.tsと同じ考え方）。
  // 「大阪学院大学高等学校」のように、高校の正式名称自体に「大学」の文字列を含む
  // 付属校があるため、中学・高校の判定を大学判定より先に見る。中学と高校も混在する
  // 選手がいるため、別レベルとして分ける（例：富樫勇樹の新発田市立本丸中学校→モントロス・
  // クリスチャン高等学校）。
  const schoolSortLevel = (name: string): number => {
    if (/中学校|中学/.test(name)) return 0;
    if (/高等学校|高校/.test(name)) return 1;
    if (/大学|University|College|カレッジ/.test(name)) return 2;
    return 1.5;
  };
  schoolCareers.sort((a, b) => {
    const levelDiff = schoolSortLevel(a.name) - schoolSortLevel(b.name);
    if (levelDiff !== 0) return levelDiff;
    if (a.startYear != null && b.startYear != null && a.startYear !== b.startYear) {
      return a.startYear - b.startYear;
    }
    return 0;
  });
  const schools = schoolCareers.map((school) => school.name);
  const englishName = player.facts.find((fact) => fact.label === '英字表記')?.value;
  // 英語表記の学校名が混じる留学経験者等は2校だと長くなりすぎるため、
  // タイトルが目安（55文字）を超える場合は直近1校（プロに近い方）に絞って短くする。
  // 正確なピクセル幅ではなく簡易な目安（検索結果での表示崩れをできるだけ避けるための安全策）。
  const MAX_TITLE_LENGTH = 55;
  const buildPathway = (schoolCount: number) => {
    const pathwaySchools = schools.slice(-schoolCount);
    const pathway = [...pathwaySchools, latest].filter((name): name is string => Boolean(name));
    return { pathwaySchools, pathway };
  };
  let { pathwaySchools, pathway } = buildPathway(2);
  if (
    pathwaySchools.length > 1 &&
    `${player.name}の経歴・出身校｜${pathway.join('→')}`.length > MAX_TITLE_LENGTH
  ) {
    ({ pathwaySchools, pathway } = buildPathway(1));
  }
  const title =
    pathwaySchools.length > 0
      ? `${player.name}の経歴・出身校｜${pathway.join('→')}`
      : latest
        ? `${player.name}（${latest}）の経歴・所属`
        : `${player.name}の経歴・所属`;
  const description = [
    `${player.name}${englishName ? `（${englishName}）` : ''}の経歴・所属。`,
    latest ? `直近の所属は${latest}。` : '',
    schools.length ? `出身校は${schools.slice(0, 3).join('・')}。` : '',
    `所属記録を出典${sourceCount > 0 ? `${sourceCount}件` : ''}とともに掲載しています。`,
    player.dataStatus === 'master' ? '' : '（正式承認前の候補データ）',
  ].join('');
  return { title, description };
}

// トップページのJSON-LD（SEO_SPEC_V1.0：WebSite。検索機能が未実装のためpotentialActionは付けない）。
export function websiteJsonLd() {
  return {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    '@id': `${siteUrl}/#website`,
    name: 'Rosterline',
    alternateName: 'Rosterline｜日本バスケ経歴アーカイブ',
    url: `${siteUrl}/`,
    inLanguage: 'ja',
  };
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
