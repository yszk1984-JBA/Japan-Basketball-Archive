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
    slug: 'draft-first-year',
    title: 'B.LEAGUEドラフト元年：選べない入口と、新しい保護',
    description:
      '2026年1月に初めて行われたB.LEAGUEドラフトでは、指名は11人。指名されたら行き先を選べず、指名直後に別のクラブへ期限付移籍した選手もいます。一方で、引退後3年間の雇用保障という新しい保護も生まれました。制度と登録データから、選手の立場で整理します。',
    publishedAt: '2026-11-28',
    dataAsOf: '2026-11-26',
  },
  {
    slug: 'salary-cap-first-year-moves',
    title: 'サラリーキャップ元年、選手はどう動いたか：B.PREMIERへの移籍は約2割減',
    description:
      '2026-27シーズンから、B.PREMIERに上限8億円・下限5億円のサラリーキャップが導入されました。登録データで選手の移籍を集計すると、B.PREMIERのクラブへの移籍は約2割減り、B.ONEのクラブへの移籍が増えています。制度の狙いと、選手の立場から見た影響を整理します。',
    publishedAt: '2026-11-28',
    dataAsOf: '2026-11-26',
  },
  {
    slug: 'how-to-research-careers',
    title: 'B.LEAGUE選手の経歴の調べ方：情報源の使い分けと、つまずきやすいポイント',
    description:
      '500人以上の選手の経歴を出典つきで記録してきた経験から、B.LEAGUE公式サイト、クラブ公式サイト、JBA・大会の記録の使い分けと、学校やクラブの改称、表記ゆれなど、調べるときにつまずきやすいポイントをまとめました。',
    publishedAt: '2026-11-28',
    dataAsOf: '2026-11-26',
  },
  {
    slug: 'one-club',
    title: 'B.LEAGUE開幕から同じクラブ一筋：11シーズンを1つのクラブで過ごす17人',
    description:
      '移籍が当たり前のB.LEAGUEで、開幕から同じクラブに所属し続ける登録選手は17人。開幕シーズンから現役を続ける129人のうち13%です。クラブ別の内訳、開幕前からの在籍、ほかのクラブから来て根付いた選手を、確認済みデータから見ていきます。',
    publishedAt: '2026-11-28',
    dataAsOf: '2026-11-26',
  },
  {
    slug: 'high-school-to-pro',
    title: '高校から大学を経ずにプロへ：その道は増えているのか',
    description:
      '高校から大学に進まずにB.LEAGUEのクラブに所属した登録選手14人のうち12人は2022年以降。多くは高校在学中に所属が始まっています。それでも主流は大学経由であることも含めて、確認済みデータから読み解きます。',
    publishedAt: '2026-11-28',
    dataAsOf: '2026-11-26',
  },
  {
    slug: 'high-school-trends',
    title: 'B.LEAGUE選手を多く輩出する高校の共通点：登録データで見る3つの傾向',
    description:
      'B.PREMIER・B.ONEでプレーする選手498人の出身高校を集計すると179校。上位校への集中と広い裾野、福岡・京都に出身者が集まる理由（出身中学からの検証）、出身者が多くのクラブに散らばる傾向、高校ごとの進学先のパターンを、確認済みデータから読み解きます。',
    publishedAt: '2026-11-28',
    updatedAt: '2026-11-28',
    dataAsOf: '2026-11-26',
  },
];

export function getColumn(slug: string): Column {
  const column = COLUMNS.find((item) => item.slug === slug);
  if (!column) throw new Error(`Unknown column: ${slug}`);
  return column;
}

export const columnPath = (slug: string) => `/columns/${slug}`;
