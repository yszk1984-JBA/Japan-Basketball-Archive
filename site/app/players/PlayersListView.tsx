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
  /** 「YYYY-MM-DD」形式の生年月日（文字列比較で年齢順に並べられる）。未確認の場合はnull。 */
  readonly birthDate: string | null;
  /** Masterデータの承認日（「YYYY-MM-DD」）。Candidateデータや承認日が特定できない場合はnull。 */
  readonly approvedAt: string | null;
  /** 経歴（Career）の登録件数。 */
  readonly careerCount: number;
};

type StatusFilter = 'all' | 'master' | 'candidate';
type CategoryFilter = 'all' | OrganizationCategory;
type SortKey = 'default' | 'name' | 'sources' | 'birthdate' | 'approvedAt' | 'careerCount';

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
  { key: 'birthdate', label: '生年月日順（若い順）' },
  { key: 'approvedAt', label: '承認日順（新着順）' },
  { key: 'careerCount', label: '経歴件数順' },
];

// null（未確認・未承認）は並び替え軸に関わらず常に末尾に送る比較関数。
function compareNullableDesc(left: string | null, right: string | null): number {
  if (left === null && right === null) return 0;
  if (left === null) return 1;
  if (right === null) return -1;
  return right.localeCompare(left);
}

const MAX_COMPARE = 4;

export function PlayersListView({ rows, totalCount }: { rows: readonly PlayerRow[]; totalCount: number }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<StatusFilter>('all');
  const [categoryFilter, setCategoryFilter] = useState<CategoryFilter>('all');
  const [sortKey, setSortKey] = useState<SortKey>('default');
  const [selected, setSelected] = useState<ReadonlySet<string>>(new Set());

  const toggleSelected = (slug: string) => {
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(slug)) {
        next.delete(slug);
      } else if (next.size < MAX_COMPARE) {
        next.add(slug);
      }
      return next;
    });
  };

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
    if (sortKey === 'birthdate') return [...next].sort((left, right) => compareNullableDesc(left.birthDate, right.birthDate));
    if (sortKey === 'approvedAt') return [...next].sort((left, right) => compareNullableDesc(left.approvedAt, right.approvedAt));
    if (sortKey === 'careerCount') return [...next].sort((left, right) => right.careerCount - left.careerCount);
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
          <p className="jbaListB-hint">
            ※ 生年月日・承認日が確認できていない選手（主にCandidateデータ）は、該当の並び替えでは一覧の末尾に表示されます。
          </p>
        </div>
      </div>

      {selected.size > 0 && (
        <div className="jbaListB-compareBar">
          <span className="jbaListB-compareBarText">
            {selected.size}人選択中{selected.size >= MAX_COMPARE ? `（最大${MAX_COMPARE}人まで）` : ''}
          </span>
          <div className="jbaListB-compareBarActions">
            <button type="button" className="jbaListB-compareBarClear" onClick={() => setSelected(new Set())}>
              選択を解除
            </button>
            {selected.size >= 2 ? (
              <a href={`/players/compare?slugs=${[...selected].join(',')}`} className="jbaListB-compareBarButton">
                比較する（{selected.size}人）
              </a>
            ) : (
              <span className="jbaListB-compareBarButton" aria-disabled="true">
                あと1人選んでください
              </span>
            )}
          </div>
        </div>
      )}

      <div className="jbaListB-table">
        <div className="jbaListB-tableHead jbaListB-playersGrid">
          <div />
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
            const isSelected = selected.has(row.slug);
            return (
              <div key={row.id} className="jbaListB-row jbaListB-playersGrid">
                <div className="jbaListB-rowHead">
                  <span className="jbaListB-checkboxCell">
                    <input
                      type="checkbox"
                      checked={isSelected}
                      disabled={!isSelected && selected.size >= MAX_COMPARE}
                      onChange={() => toggleSelected(row.slug)}
                      aria-label={`${row.name}を比較に追加`}
                    />
                  </span>
                  <a href={`/players/${row.slug}`} className="jbaListB-rowName">{row.name}</a>
                </div>
                <a href={`/players/${row.slug}`} style={{ display: 'contents' }}>
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
              </div>
            );
          })
        )}
      </div>

      <p className="jbaListB-hint">
        ※ 選手名の左のチェックボックスで2〜{MAX_COMPARE}人を選ぶと、経歴・確認できた情報を並べて比較できます。
      </p>
    </>
  );
}
