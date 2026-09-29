/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import { ArrowUpRight } from 'lucide-react';
import type { Metadata } from 'next';
import { notFound, permanentRedirect } from 'next/navigation';
import {
  getOrganization,
  getOrganizationPlayers,
  getOrganizationSourceIds,
  getSources,
  organizationSlugAliases,
  organizations,
  type PublicPlayer,
} from '../../public-data';
import { baseOpenGraph, JsonLd, organizationJsonLd, SiteBreadcrumb, SiteFooter, SiteHeader } from '../../seo';

// この組織での在籍期間（複数回在籍した場合は並べる）。一覧の「現在の所属」ではなく、
// このページの組織との関係を示す。
function periodsAt(player: PublicPlayer, organizationId: string): string {
  const periods = player.careers
    .filter((career) => career.organizationId === organizationId)
    .map((career) => career.period);
  return periods.length > 0 ? `在籍 ${periods.join('、')}` : player.cardContext;
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

  const playerCount = getOrganizationPlayers(organization.id).length;
  const title = `${organization.name}の選手一覧（${playerCount}人）`;
  const description = `${organization.name}に所属記録のある選手${playerCount}人の経歴・所属を、出典とともに掲載しています。`;

  return {
    title,
    description,
    alternates: { canonical: `/organizations/${organization.slug}` },
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

  return (
    <main className="jbaListB-page">
      <JsonLd data={organizationJsonLd(organization)} />
      <SiteHeader active="organizations" />
      <SiteBreadcrumb crumbs={[{ label: '組織一覧', href: '/organizations' }, { label: organization.name }]} />

      <div className="jbaListB-main">
        <header className="jbaListB-detailHeader">
          <p className="jbaListB-eyebrow">Organization · {organization.id}</p>
          <h1 className="jbaListB-detailTitle">{organization.name}</h1>
        </header>

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
          </p>
        </section>
      </div>

      <SiteFooter />
    </main>
  );
}
