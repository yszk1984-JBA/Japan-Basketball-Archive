/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import { ArrowUpRight } from 'lucide-react';
import type { Metadata } from 'next';
import { notFound, permanentRedirect } from 'next/navigation';
import {
  getOrganization,
  getOrganizationPlayers,
  getOrganizationSourceIds,
  getSources,
  organizationDisplayName,
  organizationSlugAliases,
  organizations,
  type PublicOrganization,
  type PublicPlayer,
} from '../../public-data';
import {
  clubBreakdown,
  isSchoolOrganization,
  latestClubOf,
  organizationNames,
  schoolBreakdown,
  schoolsOf,
  type OrganizationCount,
} from '../../organization-relations';
import { baseOpenGraph, isOrganizationIndexable, JsonLd, organizationJsonLd, organizationKind, organizationPageMeta, SiteBreadcrumb, SiteFooter, SiteHeader } from '../../seo';

// この組織での在籍期間（複数回在籍した場合は並べる）。一覧の「現在の所属」ではなく、
// このページの組織との関係を示す。
function periodsAt(player: PublicPlayer, organizationId: string): string {
  const periods = player.careers
    .filter((career) => career.organizationId === organizationId)
    .map((career) => career.period);
  return periods.length > 0 ? `在籍 ${periods.join('、')}` : player.cardContext;
}

// 名簿の1行に添える関係情報。クラブページでは出身校、学校ページでは直近の所属クラブ。
function relationNote(player: PublicPlayer, organization: PublicOrganization, isSchool: boolean): string | null {
  if (isSchool) {
    const club = latestClubOf(player);
    return club && club.id !== organization.id ? `直近の所属：${organizationNames([club])}` : null;
  }
  const schools = schoolsOf(player).filter((school) => school.id !== organization.id);
  return schools.length > 0 ? `出身：${organizationNames(schools)}` : null;
}

// 「福岡第一高等学校（3人）、…」のような上位の要約（descriptionに使う）。
function topList(counts: readonly OrganizationCount[], limit = 3): string {
  return counts
    .slice(0, limit)
    .map(({ organization, count }) => `${organization.name}（${count}人）`)
    .join('、');
}

function pageHighlights(organization: PublicOrganization, relatedPlayers: readonly PublicPlayer[]): string | undefined {
  if (isSchoolOrganization(organization)) {
    const { clubs } = clubBreakdown(relatedPlayers);
    return clubs.length > 0 ? `主な所属クラブ：${topList(clubs)}` : undefined;
  }
  if (organizationKind(organization) !== 'club') return undefined;
  const { highSchools, universities } = schoolBreakdown(relatedPlayers, organization.id);
  const parts = [
    highSchools.length > 0 ? `主な出身高校：${topList(highSchools)}` : '',
    universities.length > 0 ? `主な出身大学：${topList(universities)}` : '',
  ].filter(Boolean);
  return parts.length > 0 ? parts.join('。') : undefined;
}

// 出身校・所属クラブの内訳（人数つきのリンク一覧）。
function BreakdownList({ title, counts }: { title: string; counts: readonly OrganizationCount[] }) {
  if (counts.length === 0) return null;
  return (
    <div className="jbaListB-breakdown">
      <h3 className="jbaListB-breakdownTitle">{title}</h3>
      <ul className="jbaListB-breakdownList">
        {counts.map(({ organization, count }) => (
          <li key={organization.id}>
            <a href={`/organizations/${organization.slug}`} className="jbaListB-breakdownItem">
              <span>{organizationDisplayName(organization)}</span>
              <span className="jbaListB-breakdownCount">{count}人</span>
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}

function formatYearMonth(value: string): string {
  const [year, month] = value.split('-');
  return month ? `${year}年${Number(month)}月` : `${year}年`;
}

export function generateStaticParams() {
  return [
    ...organizations.map((organization) => ({ slug: organization.slug })),
    ...Object.keys(organizationSlugAliases).map((slug) => ({ slug })),
  ];
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const organization = getOrganization(slug);

  if (!organization) return {};

  const relatedPlayers = getOrganizationPlayers(organization.id);
  const playerCount = relatedPlayers.length;
  const { title, description } = organizationPageMeta(organization, playerCount, pageHighlights(organization, relatedPlayers));

  return {
    title,
    description,
    alternates: { canonical: `/organizations/${organization.slug}` },
    ...(isOrganizationIndexable(playerCount) ? {} : { robots: { index: false, follow: true } }),
    openGraph: { ...baseOpenGraph, title, description, url: `/organizations/${organization.slug}` },
  };
}

export default async function OrganizationPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const organization = getOrganization(slug);
  if (!organization) notFound();
  if (slug !== organization.slug) permanentRedirect(`/organizations/${organization.slug}`);

  const relatedPlayers = getOrganizationPlayers(organization.id);
  const masterPlayers = relatedPlayers.filter((player) => player.dataStatus === 'master');
  const candidatePlayers = relatedPlayers.filter((player) => player.dataStatus === 'candidate');
  const organizationSources = getSources(getOrganizationSourceIds(organization.id));
  const isSchool = isSchoolOrganization(organization);
  const isClub = organizationKind(organization) === 'club';
  const schools = isClub ? schoolBreakdown(relatedPlayers, organization.id) : null;
  const clubs = isSchool ? clubBreakdown(relatedPlayers) : null;

  return (
    <main className="jbaListB-page">
      <JsonLd data={organizationJsonLd(organization)} />
      <SiteHeader active="organizations" />
      <SiteBreadcrumb crumbs={[{ label: '組織一覧', href: '/organizations' }, { label: organization.name }]} />

      <div className="jbaListB-main">
        <header className="jbaListB-detailHeader">
          <p className="jbaListB-eyebrow">Organization · {organization.id}</p>
          <h1 className="jbaListB-detailTitle">{organization.name}</h1>
          {organization.currentName ? (
            <p className="jbaListB-currentName">
              {organization.currentName.label}：<strong>{organization.currentName.currentName}</strong>
              （{formatYearMonth(organization.currentName.effectiveDate)}
              {organization.currentName.changeType === 'SCHOOL_MERGER' ? 'に統合により開校' : 'に改称'}。出典：
              <a href={organization.currentName.source.url} target="_blank" rel="noreferrer">
                {organization.currentName.source.publisher}
              </a>
              ）。このページでは、資料に書かれた当時の名称で掲載しています。
            </p>
          ) : null}
        </header>

        {schools && schools.playersWithSchool > 0 ? (
          <section className="jbaListB-section">
            <div className="jbaListB-sectionHeading">
              <div className="jbaListB-sectionHead">
                <p className="jbaListB-eyebrow">Schools</p>
                <h2>出身校</h2>
              </div>
              <span className="jbaListB-note">
                {relatedPlayers.length}人中{schools.playersWithSchool}人の出身校を収録
              </span>
            </div>
            <BreakdownList title="出身高校" counts={schools.highSchools} />
            <BreakdownList title="出身大学・その他の学校" counts={schools.universities} />
          </section>
        ) : null}

        {clubs && clubs.playersWithClub > 0 ? (
          <section className="jbaListB-section">
            <div className="jbaListB-sectionHeading">
              <div className="jbaListB-sectionHead">
                <p className="jbaListB-eyebrow">Clubs</p>
                <h2>直近の所属クラブ</h2>
              </div>
              <span className="jbaListB-note">
                {relatedPlayers.length}人中{clubs.playersWithClub}人の所属を収録
              </span>
            </div>
            <BreakdownList title="直近の所属クラブ" counts={clubs.clubs} />
          </section>
        ) : null}

        <section className="jbaListB-section">
          <div className="jbaListB-sectionHeading">
            <div className="jbaListB-sectionHead">
              <p className="jbaListB-eyebrow">Approved Master</p>
              <h2>承認済み人物</h2>
            </div>
            <span className="jbaListB-note">{masterPlayers.length} records</span>
          </div>
          <div className="jbaListB-rosterList">
            {masterPlayers.map((player) => (
              <a href={`/players/${player.slug}`} className="jbaListB-rosterRow" key={player.id}>
                <span className="jbaListB-rosterNumber">M</span>
                <div>
                  <strong className="jbaListB-rosterName">{player.name}</strong>
                  <p className="jbaListB-rosterMeta">{periodsAt(player, organization.id)} · {player.id} · Master</p>
                  {relationNote(player, organization, isSchool) ? (
                    <p className="jbaListB-rosterRelation">{relationNote(player, organization, isSchool)}</p>
                  ) : null}
                </div>
                <ArrowUpRight size={16} />
              </a>
            ))}
          </div>
        </section>

        <section className="jbaListB-section">
          <div className="jbaListB-sectionHeading">
            <div className="jbaListB-sectionHead">
              <p className="jbaListB-eyebrow">Candidate records</p>
              <h2>確認中の人物</h2>
            </div>
            <span className="jbaListB-note">{candidatePlayers.length} records</span>
          </div>
          <div className="jbaListB-rosterList">
            {candidatePlayers.map((player) => (
              <a href={`/players/${player.slug}`} className="jbaListB-rosterRow" key={player.id}>
                <span className="jbaListB-rosterNumber">{player.facts.find((fact) => fact.label === '背番号')?.value ?? '—'}</span>
                <div>
                  <strong className="jbaListB-rosterName">{player.name}</strong>
                  <p className="jbaListB-rosterMeta">{periodsAt(player, organization.id)} · {player.id}</p>
                  {relationNote(player, organization, isSchool) ? (
                    <p className="jbaListB-rosterRelation">{relationNote(player, organization, isSchool)}</p>
                  ) : null}
                </div>
                <ArrowUpRight size={16} />
              </a>
            ))}
          </div>
        </section>

        <section className="jbaListB-section">
          <div className="jbaListB-sectionHead">
            <p className="jbaListB-eyebrow">Sources</p>
            <h2>参照資料</h2>
          </div>
          <div className="jbaListB-sourceList">
            {organizationSources.map((source) => (
              <a href={source.url} target="_blank" rel="noreferrer" className="jbaListB-sourceRow" key={source.id}>
                <span className="jbaListB-sourceId">{source.id}</span>
                <div>
                  <strong className="jbaListB-sourceTitle">{source.title}</strong>
                  <p className="jbaListB-sourceMeta">{source.publisher} · {source.dataStatus === 'master' ? 'Master' : '候補'}</p>
                </div>
                <ArrowUpRight size={16} />
              </a>
            ))}
          </div>
          <p className="jbaListB-reviewNote">
            この一覧は{organization.name}とのCareerが収録済みの人物だけを表示します。全関係者を示す名簿ではありません。
            {isClub ? '出身校・人数は、本サイトに登録済みの経歴から集計したものです。' : null}
            {isSchool ? '直近の所属クラブは、本サイトに登録済みの経歴のうち最も新しい所属です。現在の所属と異なる場合があります。' : null}
          </p>
        </section>
      </div>

      <SiteFooter />
    </main>
  );
}
