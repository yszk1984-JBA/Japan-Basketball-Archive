/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import { organizations } from '../public-data';

// 記事本文から組織ページへリンクする（名称で探し、見つからなければ文字だけ表示する）。
export function OrgLink({ name, label }: { name: string; label?: string }) {
  const organization = organizations.find((item) => item.name === name);
  return organization ? <a href={`/organizations/${organization.slug}`}>{label ?? name}</a> : <>{label ?? name}</>;
}
