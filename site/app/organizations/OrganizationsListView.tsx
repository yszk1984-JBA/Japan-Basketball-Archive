'use client';
/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */

import { useMemo, useState } from 'react';
import { ORGANIZATION_CATEGORY_META, ORGANIZATION_CATEGORY_ORDER, type OrganizationCategory } from '../organization-category';

export type OrganizationRow = {
  readonly id: string;
  readonly slug: string;
  readonly name: string;
  readonly category: OrganizationCategory;
  readonly total: number;
  readonly master: number;
};

type CategoryFilter = 'all' | OrganizationCategory;
type SortKey = 'count' | 'name';

const CATEGORY_OPTIONS: { key: CategoryFilter; label: string }[] = [
  { key: 'all', label: 'すべて' },
  ...ORGANIZATION_CATEGORY_ORDER.map((key) => ({ key, label: ORGANIZATION_CATEGORY_META[key].label })),
];

const SORT_OPTIONS: { key: SortKey; label: string }[] = [
  { key: 'count', label: '在籍者数順' },
  { key: 'name', label: '五十音順' },
];

export function OrganizationsListView({ rows, totalCount }: { rows: readonly OrganizationRow[]; totalCount: number }) {
  const [categoryFilter, setCategoryFilter] = useState<CategoryFilter>('all');
  const [sortKey, setSortKey] = useState<SortKey>('count');

  const filtered = useMemo(() => {
    const next = rows.filter((row) => categoryFilter === 'all' || row.category === categoryFilter);
    return [...next].sort((left, right) =>
      sortKey === 'count' ? right.total - left.total : left.name.localeCompare(right.name, 'ja'),
    );
  }, [rows, categoryFilter, sortKey]);

  return (
    <>
      <p className="jbaListB-lede">
        {filtered.length} / {totalCount}件を表示中。カテゴリー・在籍者数で絞り込み・並び替えができます。
      </p>

      <div className="jbaListB-filterCard">
        <div className="jbaListB-filterGroup">
          <div className="jbaListB-filterLabel">カテゴリー</div>
          <div className="jbaListB-chipRow">
            {CATEGORY_OPTIONS.map((option) => (
              <button
                key={option.key}
                type="button"
                className={`jbaListB-chip${categoryFilter === option.key ? ' jbaListB-chipActive' : ''}`}
                onClick={() => setCategoryFilter(option.key)}
              >
                {option.label}
              </button>
            ))}
          </div>
          <p className="jbaListB-hint">
            ※ カテゴリーは組織名から自動判定した表示用の分類です（例：「高等学校」を含む→高校）。組織データのスキーマ自体に種別列は追加していません。
          </p>
        </div>
        <div className="jbaListB-filterGroup">
          <div className="jbaListB-filterLabel">並び替え</div>
          <div className="jbaListB-chipRow">
            {SORT_OPTIONS.map((option) => (
              <button
                key={option.key}
                type="button"
                className={`jbaListB-chip${sortKey === option.key ? ' jbaListB-chipActive' : ''}`}
                onClick={() => setSortKey(option.key)}
              >
                {option.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="jbaListB-table">
        <div className="jbaListB-tableHead jbaListB-orgsGrid">
          <div></div>
          <div>組織名</div>
          <div>カテゴリー</div>
          <div>在籍者数</div>
        </div>
        {filtered.length === 0 ? (
          <div className="jbaListB-empty">条件に一致する組織がありません。</div>
        ) : (
          filtered.map((row) => {
            const categoryMeta = ORGANIZATION_CATEGORY_META[row.category];
            return (
              <a href={`/organizations/${row.slug}`} key={row.id} className="jbaListB-row jbaListB-orgsGrid">
                <span className="jbaListB-dot" style={{ background: categoryMeta.color }} />
                <div className="jbaListB-rowName">{row.name}</div>
                <div>
                  <span className="jbaListB-pill" style={{ background: categoryMeta.bg, color: categoryMeta.color }}>
                    {categoryMeta.label}
                  </span>
                </div>
                <div className="jbaListB-rowMuted">
                  {row.total}件{row.master > 0 ? ` ・うちMaster ${row.master}件` : ''}
                </div>
              </a>
            );
          })
        )}
      </div>
    </>
  );
}
