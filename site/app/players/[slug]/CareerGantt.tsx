/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import { ORGANIZATION_CATEGORY_META, organizationCategory } from '../../organization-category';
import { organizationSlugFor, type PublicPlayer } from '../../public-data';

// 選手詳細ページの横軸年表（B案：ガントチャート風、所属区分で色分け）。
// 年が確認できたCareerだけを棒で描き、期間未確認のCareerは下に名前だけ並べる。
// 在籍中（終了年なし）の棒は、表示時点のシーズン終了年まで伸ばす。
// モバイル幅では非表示にし、下の縦の一覧で読む（site-b.css）。

type Career = PublicPlayer['careers'][number];

const CURRENT_SEASON_END = 2027; // 2026-27シーズン

export function CareerGantt({ careers }: { careers: PublicPlayer['careers'] }) {
  const dated = careers.filter((career): career is Career & { startYear: number } =>
    typeof career.startYear === 'number' && Boolean(career.organization),
  );
  if (dated.length < 2) return null;
  const undated = careers.filter((career) => typeof career.startYear !== 'number' && career.organization);

  const endOf = (career: Career & { startYear: number }) =>
    Math.max(career.endYear ?? CURRENT_SEASON_END, career.startYear + 1);
  const minYear = Math.min(...dated.map((career) => career.startYear));
  const maxYear = Math.max(...dated.map(endOf));
  const span = maxYear - minYear;
  const step = span > 14 ? 4 : span > 8 ? 2 : 1;
  const ticks: number[] = [];
  for (let year = minYear; year <= maxYear; year += step) ticks.push(year);

  return (
    <div className="jbaListB-gantt" aria-label="経歴の年表">
      <div className="jbaListB-ganttAxis">
        <span className="jbaListB-ganttLabelCol" />
        <div className="jbaListB-ganttTrack">
          {ticks.map((year) => (
            <span className="jbaListB-ganttTick" key={year} style={{ left: `${((year - minYear) / span) * 100}%` }}>
              {year}
            </span>
          ))}
        </div>
      </div>
      {dated.map((career, index) => {
        const meta = ORGANIZATION_CATEGORY_META[organizationCategory(career.organization ?? '')];
        const left = ((career.startYear - minYear) / span) * 100;
        const width = ((endOf(career) - career.startYear) / span) * 100;
        const slug = organizationSlugFor(career.organizationId);
        const label = career.organization ?? '';
        return (
          <div className="jbaListB-ganttRow" key={`${index}-${career.period}-${label}`}>
            <span className="jbaListB-ganttLabelCol">
              {slug ? <a href={`/organizations/${slug}`}>{label}</a> : label}
            </span>
            <div className="jbaListB-ganttTrack">
              <span
                className="jbaListB-ganttBar"
                title={`${label}（${career.period}）`}
                style={{ left: `${left}%`, width: `${width}%`, background: meta.color }}
              >
                {/* 短い棒は文字が切れるため期間表示を省き、ホバー（title）と下の一覧で読む */}
                {width >= 7 && (
                  <span className="jbaListB-ganttBarText">
                    {career.endYear ? `${career.startYear}–${String(career.endYear).slice(2)}` : `${career.startYear}〜`}
                  </span>
                )}
              </span>
            </div>
          </div>
        );
      })}
      <div className="jbaListB-ganttLegend">
        {(['hs', 'univ', 'club', 'overseas'] as const).map((category) => (
          <span key={category} className="jbaListB-ganttLegendItem">
            <span className="jbaListB-ganttLegendSwatch" style={{ background: ORGANIZATION_CATEGORY_META[category].color }} />
            {ORGANIZATION_CATEGORY_META[category].label}
          </span>
        ))}
        <span className="jbaListB-ganttLegendNote">終了年のない所属は2026-27シーズンまで表示</span>
      </div>
      {undated.length > 0 && (
        <p className="jbaListB-ganttUndated">期間未確認：{undated.map((career) => career.organization).join('、')}</p>
      )}
    </div>
  );
}
