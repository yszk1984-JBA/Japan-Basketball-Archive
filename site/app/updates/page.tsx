/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import type { Metadata } from 'next';
import { masterApprovals, players } from '../public-data';
import { baseOpenGraph, breadcrumbJsonLd, JsonLd, SiteBreadcrumb, SiteFooter, SiteHeader } from '../seo';

// 更新履歴：Master Dataの承認（Approval Sprint）ごとに、新しく公開した選手と経歴を追加した選手の数を掲載する。
// 「継続的に確認・更新しているサイトであること」を利用者に見える形にするページ（AdSense審査対応、2026-11）。
const title = '更新履歴';
const description =
  'Rosterlineで確認を終えて公開したデータの更新履歴です。承認ごとに、新しく掲載した選手と、経歴を追加・更新した選手の数を掲載しています。';
const NAMES_LIMIT = 8;

export const metadata: Metadata = {
  title,
  description,
  alternates: { canonical: '/updates' },
  openGraph: { ...baseOpenGraph, title, description, url: '/updates' },
};

function formatDate(isoDate: string): string {
  const [year, month, day] = isoDate.slice(0, 10).split('-');
  return `${year}年${Number(month)}月${Number(day)}日`;
}

function sprintLabel(approvalId: string): string {
  const match = approvalId.match(/^APP-AS(\d+)/);
  return match ? `第${Number(match[1])}回の承認` : '承認';
}

export default function UpdatesPage() {
  const approvals = Object.values(masterApprovals as Record<string, { approvalId: string; approvedAt: string }>);
  const entries = approvals
    .map((approval) => {
      const added = players.filter((player) => player.dataStatus === 'master' && player.approvalId === approval.approvalId);
      const enriched = players.filter(
        (player) => player.dataStatus === 'master' && (player.enrichmentApprovalIds ?? []).includes(approval.approvalId),
      );
      return { ...approval, added, enriched };
    })
    .filter((entry) => entry.added.length || entry.enriched.length)
    .sort((left, right) => right.approvedAt.localeCompare(left.approvedAt) || right.approvalId.localeCompare(left.approvalId));
  const masterCount = players.filter((player) => player.dataStatus === 'master').length;

  return (
    <main className="jbaListB-page">
      <JsonLd
        data={{
          '@context': 'https://schema.org',
          '@graph': [
            breadcrumbJsonLd([
              { name: 'ホーム', path: '/' },
              { name: title, path: '/updates' },
            ]),
          ],
        }}
      />
      <SiteHeader />
      <SiteBreadcrumb crumbs={[{ label: title }]} />

      <div className="jbaListB-main">
        <div>
          <p className="jbaListB-eyebrow">Updates</p>
          <h1 className="jbaListB-h1">{title}</h1>
        </div>
        <p className="jbaListB-lede">
          確認を終えて公開したデータの履歴です。現在、確認済みの選手は{masterCount}人です。データを確認して公開するまでの手順は
          <a href="/about">このサイトについて</a>をご覧ください。
        </p>

        {entries.map((entry) => (
          <section className="jbaListB-section jbaListB-about" key={entry.approvalId}>
            <div className="jbaListB-sectionHead">
              <h2>
                {formatDate(entry.approvedAt)}　{sprintLabel(entry.approvalId)}
              </h2>
            </div>
            <ul>
              {entry.added.length ? (
                <li>
                  新しく掲載した選手：{entry.added.length}人（
                  {entry.added.slice(0, NAMES_LIMIT).map((player, index) => (
                    <span key={player.id}>
                      {index > 0 ? '、' : ''}
                      <a href={`/players/${player.slug}`}>{player.name}</a>
                    </span>
                  ))}
                  {entry.added.length > NAMES_LIMIT ? ' ほか' : ''}）
                </li>
              ) : null}
              {entry.enriched.length ? <li>経歴を追加・更新した選手：{entry.enriched.length}人</li> : null}
            </ul>
          </section>
        ))}
      </div>

      <SiteFooter />
    </main>
  );
}
