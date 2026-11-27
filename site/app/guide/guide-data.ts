// Rosterline Guide（用品・観戦・遠征の実用ガイド）の記事一覧。
// コラム（columns/、登録データを集計した解説記事）とは別のセクションとして扱う。
// 1本追加するたびに、ここに1件足して app/guide/<slug>/page.tsx を作る。
// 記事は公式情報・メーカー情報で確かめた事実だけで書き、使用経験やレビューを創作しない。
export type Guide = {
  readonly slug: string;
  readonly title: string;
  readonly description: string;
  readonly category: 'gear' | 'watching' | 'travel';
  readonly publishedAt: string;
  readonly updatedAt?: string;
  // 参照した規則・メーカー情報を最後に確認した日
  readonly checkedAt: string;
};

export const GUIDE_CATEGORY_LABELS: Readonly<Record<Guide['category'], string>> = {
  gear: '用品',
  watching: '観戦',
  travel: '遠征・宿泊',
};

export const GUIDES: readonly Guide[] = [
  {
    slug: 'basketball-ball-size',
    title: 'バスケットボールのサイズ（号数）の選び方｜ミニバス・中学生・高校生・一般向け',
    description:
      'ミニバスは5号、中学生以上は男子7号・女子6号。号数ごとの大きさと重さ、試合球と練習球の違い、屋内用と屋外用の違い、購入時に確かめたいポイントを、FIBA・日本バスケットボール協会の規則をもとにまとめました。',
    category: 'gear',
    publishedAt: '2026-11-28',
    checkedAt: '2026-11-28',
  },
];

export function getGuide(slug: string): Guide {
  const guide = GUIDES.find((item) => item.slug === slug);
  if (!guide) throw new Error(`Unknown guide: ${slug}`);
  return guide;
}

export const guidePath = (slug: string) => `/guide/${slug}`;
