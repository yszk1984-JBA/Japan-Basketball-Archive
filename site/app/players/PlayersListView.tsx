'use client';
/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */

import { useMemo, useState } from 'react';
import { ORGANIZATION_CATEGORY_META, ORGANIZATION_CATEGORY_ORDER, type OrganizationCategory } from '../organization-category';

export type PlayerRow = {
  readonly id: string;
  readonly slug: string;
  readonly name: string;
  readonly org: string | null;
  /** 現在（直近）の所属から推定した1件のカテゴリー。表示（所属欄の隣の主要バッジ用）に使う。 */
  readonly primaryCategory: OrganizationCategory | null;
  /** 経歴に登場した組織すべてから推定したカテゴリーの集合。絞り込みに使う（例：現役プロでも高校時代の経歴があれば「高校」に含める）。 */
  readonly categories: readonly OrganizationCategory[];
  readonly status: 'master' | 'candidate';
  readonly sources: number;
};

type StatusFilter = 'all' | 'master' | 'candidate';
type CategoryFilter = 'all' | OrganizationCategory;
type SortKey = 'default' | 'name' | 'sources';

const STATUS_OPTIONS: { key: StatusFilter; label: string }[] = [
  { key: 'all', label: 'すべて' },
  { key: 'master', label: 'Master' },
  { key: 'candidate', label: 'Candidate' },
];

const CATEGORY_OPTIONS: { key: CategoryFilter; label: string }[] = [
  { key: 'all', label: 'すべて' },
  ...ORGANIZATION_CATEGORY_ORDER.map((key) => ({ key, label: ORGANIZATION_CATEGORY_META[key].label })),
];

const SORT_OPTIONS: { key: SortKey; label: string }[] = [
  { key: 'default', label: '登録順' },
  { key: 'name', label: '五十音順' },
  { key: 'sources', label: '出典数順' },
];

export function PlayersListView({ rows, totalCount }: { rows: readonly PlayerRow[]; totalCount: number }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<StatusFilter>('all');
  const [categoryFilter, setCategoryFilter] = useState<CategoryFilter>('all');
  const [sortKey, setSortKey] = useState<SortKey>('default');

  const filtered = useMemo(() => {
    const query = searchQuery.trim().toLowerCase();
    const next = rows.filter(
      (row) =>
        (statusFilter === 'all' || row.status === statusFilter) &&
        (categoryFilter === 'all' || row.categories.includes(categoryFilter)) &&
        (query === '' || row.name.toLowerCase().includes(query)),
    );
    if (sortKey === 'name') return [...next].sort((left, right) => left.name.localeCompare(right.name, 'ja'));
    if (sortKey === 'sources') return [...next].sort((left, right) => right.sources - left.sources);
    return next;
  }, [rows, statusFilter, categoryFilter, searchQuery, sortKey]);

  return (
    <>
      <p className="jbaListB-lede">
        {filtered.length} / {totalCount}人を表示中。名前検索・データステータス・所属カテゴリーで絞り込み、並び替えができます。
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
              placeholder="選手名で検索"
              aria-label="選手名で検索"
              value={searchQuery}
              onChange={(event) => setSearchQuery(event.target.value)}
            />
          </div>
        </div>
        <div className="jbaListB-filterGroup">
          <div className="jbaListB-filterLabel">データステータス</div>
          <div className="jbaListB-chipRow">
            {STATUS_OPTIONS.map((option) => (
              <button
                key={option.key}
                type="button"
                className={`jbaListB-chip${statusFilter === option.key ? ' jbaListB-chipActive' : ''}`}
                onClick={() => setStatusFilter(option.key)}
              >
                {option.label}
              </button>
            ))}
          </div>
        </div>
        <div className="jbaListB-filterGroup">
          <div className="jbaListB-filterLabel">所属カテゴリー</div>
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
            ※ カテゴリーは組織名から自動判定した表示用の分類です。Master／Candidateデータのスキーマ自体は変更していません。経歴に登場したことがあるカテゴリーで絞り込むため、例えば「高校」を選ぶと、現在はプロ所属でも高校時代の経歴がある選手も表示されます。
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
        <div className="jbaListB-tableHead jbaListB-playersGrid">
          <div>氏名</div>
          <div>所属</div>
          <div>カテゴリー</div>
          <div>ステータス</div>
          <div>出典</div>
        </div>
        {filtered.length === 0 ? (
          <div className="jbaListB-empty">条件に一致する選手がいません。検索キーワードや絞り込みを変えてみてください。</div>
        ) : (
          filtered.map((row) => {
            return (
              <a href={`/players/${row.slug}`} key={row.id} className="jbaListB-row jbaListB-playersGrid">
                <div className="jbaListB-rowName">{row.name}</div>
                <div className="jbaListB-rowMuted">{row.org ?? '所属未確認'}</div>
                <div className="jbaListB-pillWrap">
                  {row.categories.length === 0 ? (
                    <span className="jbaListB-rowMuted">—</span>
                  ) : (
                    row.categories.map((category) => {
                      const categoryMeta = ORGANIZATION_CATEGORY_META[category];
                      return (
                        <span
                          key={category}
                          className="jbaListB-pill"
                          style={{ background: categoryMeta.bg, color: categoryMeta.color }}
                        >
                          {categoryMeta.label}
                        </span>
                      );
                    })
                  )}
                </div>
                <div>
                  <span
                    className={`jbaListB-pill ${row.status === 'master' ? 'jbaListB-statusMaster' : 'jbaListB-statusCandidate'}`}
                  >
                    {row.status === 'master' ? '承認済み' : '確認中'}
                  </span>
                </div>
                <div className="jbaListB-rowMuted">{row.sources}件</div>
              </a>
            );
          })
        )}
      </div>
    </>
  );
}
