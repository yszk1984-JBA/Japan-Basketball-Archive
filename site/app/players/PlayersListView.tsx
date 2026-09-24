'use client';
/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */

import { useMemo, useState } from 'react';
import { ORGANIZATION_CATEGORY_META, ORGANIZATION_CATEGORY_ORDER, type OrganizationCategory } from '../organization-category';

export type PlayerRow = {
  readonly id: string;
  readonly slug: string;
  readonly name: string;
  readonly org: string | null;
  readonly category: OrganizationCategory | null;
  readonly status: 'master' | 'candidate';
  readonly sources: number;
};

type StatusFilter = 'all' | 'master' | 'candidate';
type CategoryFilter = 'all' | OrganizationCategory;

const STATUS_OPTIONS: { key: StatusFilter; label: string }[] = [
  { key: 'all', label: 'すべて' },
  { key: 'master', label: 'Master' },
  { key: 'candidate', label: 'Candidate' },
];

const CATEGORY_OPTIONS: { key: CategoryFilter; label: string }[] = [
  { key: 'all', label: 'すべて' },
  ...ORGANIZATION_CATEGORY_ORDER.map((key) => ({ key, label: ORGANIZATION_CATEGORY_META[key].label })),
];

export function PlayersListView({ rows, totalCount }: { rows: readonly PlayerRow[]; totalCount: number }) {
  const [statusFilter, setStatusFilter] = useState<StatusFilter>('all');
  const [categoryFilter, setCategoryFilter] = useState<CategoryFilter>('all');

  const filtered = useMemo(
    () =>
      rows.filter(
        (row) =>
          (statusFilter === 'all' || row.status === statusFilter) &&
          (categoryFilter === 'all' || row.category === categoryFilter),
      ),
    [rows, statusFilter, categoryFilter],
  );

  return (
    <>
      <p className="jbaListB-lede">
        {filtered.length} / {totalCount}人を表示中。データステータス・所属カテゴリーで絞り込めます。
      </p>

      <div className="jbaListB-filterCard">
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
            ※ カテゴリーは組織名から自動判定した表示用の分類です。Master／Candidateデータのスキーマ自体は変更していません。
          </p>
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
          <div className="jbaListB-empty">条件に一致する選手がいません。</div>
        ) : (
          filtered.map((row) => {
            const categoryMeta = row.category ? ORGANIZATION_CATEGORY_META[row.category] : null;
            return (
              <a href={`/players/${row.slug}`} key={row.id} className="jbaListB-row jbaListB-playersGrid">
                <div className="jbaListB-rowName">{row.name}</div>
                <div className="jbaListB-rowMuted">{row.org ?? '所属未確認'}</div>
                <div>
                  {categoryMeta ? (
                    <span className="jbaListB-pill" style={{ background: categoryMeta.bg, color: categoryMeta.color }}>
                      {categoryMeta.label}
                    </span>
                  ) : (
                    <span className="jbaListB-rowMuted">—</span>
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
