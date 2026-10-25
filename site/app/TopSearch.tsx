'use client';
/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */

import { useMemo, useState } from 'react';

export type TopSearchEntry = {
  readonly kind: 'player' | 'organization';
  readonly name: string;
  readonly href: string;
  /** 候補の下に添える補足（選手は直近の所属、組織は在籍記録のある人数など）。 */
  readonly meta: string;
};

const MAX_RESULTS = 8;

// 検索用の正規化：空白（半角・全角）を除き、英字を小文字にする。
// 「富樫 勇樹」と「富樫勇樹」のように、登録名の空白の有無に関わらず一致させる。
export function normalizeSearchText(value: string): string {
  return value.replace(/[\s　]+/g, '').toLowerCase();
}

// トップページの検索ボックス。入力に合わせて選手・組織の候補を表示し、
// Enter（または「検索」）で選手一覧ページ（/players?q=…）の絞り込み結果に移動する。
export function TopSearch({ entries }: { entries: readonly TopSearchEntry[] }) {
  const [query, setQuery] = useState('');
  const normalized = normalizeSearchText(query);

  const results = useMemo(() => {
    if (normalized === '') return [];
    const scored = entries
      .map((entry) => {
        const name = normalizeSearchText(entry.name);
        const index = name.indexOf(normalized);
        return index < 0 ? null : { entry, rank: index === 0 ? 0 : 1 };
      })
      .filter((item): item is { entry: TopSearchEntry; rank: number } => item !== null);
    scored.sort((left, right) => left.rank - right.rank || (left.entry.kind === right.entry.kind ? 0 : left.entry.kind === 'player' ? -1 : 1));
    return scored.slice(0, MAX_RESULTS).map((item) => item.entry);
  }, [entries, normalized]);

  return (
    <form className="jbaListB-topSearch" action="/players" method="get" aria-label="サイト内検索">
      <label className="jbaListB-topSearchLabel" htmlFor="top-search-input">
        選手名・学校名・クラブ名で検索
      </label>
      <div className="jbaListB-topSearchRow">
        <div className="jbaListB-topSearchField">
          <svg className="jbaListB-topSearchIcon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" aria-hidden="true">
            <circle cx="11" cy="11" r="7"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <input
            id="top-search-input"
            type="search"
            name="q"
            className="jbaListB-topSearchInput"
            placeholder="例：比江島慎、洛南高等学校、宇都宮ブレックス"
            autoComplete="off"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            aria-controls="top-search-results"
          />
        </div>
        <button type="submit" className="jbaListB-topSearchButton">検索</button>
      </div>
      {normalized !== '' && (
        <ul className="jbaListB-topSearchResults" id="top-search-results">
          {results.length === 0 ? (
            <li className="jbaListB-topSearchEmpty">一致する選手・組織が見つかりません</li>
          ) : (
            results.map((entry) => (
              <li key={`${entry.kind}-${entry.href}`}>
                <a href={entry.href} className="jbaListB-topSearchResult">
                  <span className={`jbaListB-topSearchKind jbaListB-topSearchKind-${entry.kind}`}>
                    {entry.kind === 'player' ? '選手' : '組織'}
                  </span>
                  <span className="jbaListB-topSearchName">{entry.name}</span>
                  <span className="jbaListB-topSearchMeta">{entry.meta}</span>
                </a>
              </li>
            ))
          )}
        </ul>
      )}
    </form>
  );
}
