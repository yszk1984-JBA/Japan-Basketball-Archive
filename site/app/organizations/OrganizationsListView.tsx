'use client';
/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */

import { useMemo, useState } from 'react';
import { ORGANIZATION_CATEGORY_META, ORGANIZATION_CATEGORY_ORDER, type OrganizationCategory } from '../organization-category';

export type OrganizationRow = {
  readonly id: string;
  readonly slug: string;
  readonly name: string;
  // 改称・統合した学校の現在の名称の注記（例：「現：仙台大学附属明成高等学校」）。
  readonly currentNameNote?: string;
  readonly category: OrganizationCategory;
  readonly total: number;
  readonly master: number;
};

type CategoryFilter = 'all' | OrganizationCategory;
type SortKey = 'count' | 'name' | 'candidate' | 'category';

const CATEGORY_OPTIONS: { key: CategoryFilter; label: string }[] = [
  { key: 'all', label: 'すべて' },
  ...ORGANIZATION_CATEGORY_ORDER.map((key) => ({ key, label: ORGANIZATION_CATEGORY_META[key].label })),
];

const SORT_OPTIONS: { key: SortKey; label: string }[] = [
  { key: 'count', label: '在籍者数順' },
  { key: 'name', label: '五十音順' },
  { key: 'candidate', label: '確認中件数順' },
  { key: 'category', label: 'カテゴリー順' },
];

export function OrganizationsListView({ rows, totalCount }: { rows: readonly OrganizationRow[]; totalCount: number }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [categoryFilter, setCategoryFilter] = useState<CategoryFilter>('all');
  const [sortKey, setSortKey] = useState<SortKey>('count');

  const filtered = useMemo(() => {
    const query = searchQuery.trim().toLowerCase();
    const next = rows.filter(
      (row) =>
        (categoryFilter === 'all' || row.category === categoryFilter) &&
        (query === '' ||
          row.name.toLowerCase().includes(query) ||
          (row.currentNameNote ?? '').toLowerCase().includes(query)),
    );
    if (sortKey === 'count') return [...next].sort((left, right) => right.total - left.total);
    if (sortKey === 'candidate') {
      return [...next].sort((left, right) => (right.total - right.master) - (left.total - left.master));
    }
    if (sortKey === 'category') {
      return [...next].sort((left, right) => {
        const categoryDiff = ORGANIZATION_CATEGORY_ORDER.indexOf(left.category) - ORGANIZATION_CATEGORY_ORDER.indexOf(right.category);
        return categoryDiff !== 0 ? categoryDiff : left.name.localeCompare(right.name, 'ja');
      });
    }
    return [...next].sort((left, right) => left.name.localeCompare(right.name, 'ja'));
  }, [rows, categoryFilter, sortKey, searchQuery]);

  return (
    <>
      <p className="jbaListB-lede">
        {filtered.length} / {totalCount}件を表示中。名前検索・カテゴリーで絞り込み、並び替えができます。
      </p>

      <div className="jbaListB-filterCard">
        <div className="jbaListB-filterGroup">
          <div className="jbaListB-filterLabel">検索</div>
          <div className="jbaListB-searchWrap">
            <svg
              className="jbaListB-searchIcon"
              width="14"
              height="14"
              viewBox="0 0 24 24"
              fill="none"
              stroke="#8A97A3"
              strokeWidth="2.2"
              aria-hidden="true"
            >
              <circle cx="11" cy="11" r="7"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
            <input
              type="search"
              className="jbaListB-searchInput"
              placeholder="組織名で検索"
              aria-label="組織名で検索"
              value={searchQuery}
              onChange={(event) => setSearchQuery(event.target.value)}
            />
          </div>
        </div>
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
          <div className="jbaListB-empty">条件に一致する組織がありません。検索キーワードや絞り込みを変えてみてください。</div>
        ) : (
          filtered.map((row) => {
            const categoryMeta = ORGANIZATION_CATEGORY_META[row.category];
            return (
              <a href={`/organizations/${row.slug}`} key={row.id} className="jbaListB-row jbaListB-orgsGrid">
                <span className="jbaListB-dot" style={{ background: categoryMeta.color }} />
                <div>
                  <div className="jbaListB-rowName">{row.name}</div>
                  {row.currentNameNote ? <div className="jbaListB-rankCurrent">{row.currentNameNote}</div> : null}
                </div>
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
