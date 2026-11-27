// コラム（解説記事）の一覧。1本追加するたびに、ここに1件足して app/columns/<slug>/page.tsx を作る。
// 記事中の数字は、dataAsOf 時点の確認済み（Master）データから集計した値で固定している（記事は公開時点の記録）。
export type Column = {
  readonly slug: string;
  readonly title: string;
  readonly description: string;
  readonly publishedAt: string;
  readonly updatedAt?: string;
  readonly dataAsOf: string;
};

export const COLUMNS: readonly Column[] = [
  {
    slug: 'high-school-trends',
    title: 'B.LEAGUE選手を多く輩出する高校の共通点：登録データで見る3つの傾向',
    description:
      'B.PREMIER・B.ONEでプレーする選手498人の出身高校を集計すると179校。上位校への集中と広い裾野、出身者が多くのクラブに散らばる傾向、高校ごとの進学先のパターンを、確認済みデータから読み解きます。',
    publishedAt: '2026-11-28',
    dataAsOf: '2026-11-26',
  },
];

export function getColumn(slug: string): Column {
  const column = COLUMNS.find((item) => item.slug === slug);
  if (!column) throw new Error(`Unknown column: ${slug}`);
  return column;
}

export const columnPath = (slug: string) => `/columns/${slug}`;
