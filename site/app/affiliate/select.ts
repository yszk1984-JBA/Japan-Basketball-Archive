// 表示判定（純粋関数のみ。JSONの読み込みやReactには依存しない）。
// テスト：site/scripts/affiliate.test.mjs（node --test）。同じ規則を scripts/check_affiliate_data.py でも検証する。
import type {
  AffiliateData,
  AffiliateLink,
  AffiliatePlacement,
  AffiliateProgram,
  AspName,
  PageType,
  SelectedItem,
  SelectedSlot,
} from './types';

// ASPごとに、広告リンク・画像の読み込みを許可するドメイン（このドメインか、そのサブドメイン）。
// ASPの正式な素材がここにないドメインを使う場合は、素材を確認したうえでこの一覧を変更する（コードレビューを通す）。
export const ASP_ALLOWED_HOSTS: Readonly<Record<AspName, readonly string[]>> = {
  a8: ['a8.net'],
  rakuten: ['rakuten.co.jp', 'r10s.jp'],
};

// rawHtmlで許可するタグと属性。script・iframe・style要素・イベント属性（onclick等）は許可しない。
const ALLOWED_TAGS = new Set(['a', 'img', 'br', 'span', 'div', 'p', 'table', 'tbody', 'tr', 'td', 'strong', 'b']);
const ALLOWED_ATTRS = new Set(['href', 'src', 'alt', 'title', 'width', 'height', 'border', 'style', 'target', 'rel', 'class']);
const URL_ATTRS = new Set(['href', 'src']);
const FORBIDDEN_STYLE = /url\s*\(|expression|javascript:|@import|behavior|-moz-binding/i;

// 日本時間の今日（YYYY-MM-DD）。期限は日本時間の日付で判定する。
export function todayJst(now: Date = new Date()): string {
  return new Date(now.getTime() + 9 * 60 * 60 * 1000).toISOString().slice(0, 10);
}

function isIsoDate(value: unknown): value is string {
  return typeof value === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(value);
}

// 期間内か（validFrom・validUntil とも当日を含む）。
export function isWithinPeriod(today: string, validFrom?: string | null, validUntil?: string | null): boolean {
  if (validFrom && (!isIsoDate(validFrom) || today < validFrom)) return false;
  if (validUntil && (!isIsoDate(validUntil) || today > validUntil)) return false;
  return true;
}

export function isAllowedUrl(value: string | null | undefined, asp: AspName): boolean {
  if (!value) return false;
  let url: URL;
  try {
    url = new URL(value);
  } catch {
    return false;
  }
  if (url.protocol !== 'https:') return false;
  const host = url.hostname.toLowerCase();
  return ASP_ALLOWED_HOSTS[asp].some((allowed) => host === allowed || host.endsWith(`.${allowed}`));
}

export type HtmlCheck = { readonly ok: true } | { readonly ok: false; readonly reason: string };

// ASP発行コード（rawHtml）が、許可したタグ・属性・ドメインだけでできているかを確認する。
// コードは書き換えない。条件を満たさない素材は表示しない（ビルド前の検証スクリプトでも止める）。
export function checkRawHtml(html: string | null | undefined, asp: AspName): HtmlCheck {
  if (!html || !html.trim()) return { ok: false, reason: 'rawHtmlが空です' };
  const body = html.replace(/<!--[\s\S]*?-->/g, '');
  const tagPattern = /<\/?([a-zA-Z][a-zA-Z0-9]*)\b((?:[^>"']|"[^"]*"|'[^']*')*)>/g;
  let rest = '';
  let last = 0;
  let match: RegExpExecArray | null;
  let hasLink = false;
  while ((match = tagPattern.exec(body))) {
    rest += body.slice(last, match.index);
    last = match.index + match[0].length;
    const tag = match[1].toLowerCase();
    if (!ALLOWED_TAGS.has(tag)) return { ok: false, reason: `許可していないタグ: <${tag}>` };
    if (match[0].startsWith('</')) continue;
    const attrPattern = /([^\s"'=<>/]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+)))?/g;
    let attr: RegExpExecArray | null;
    const attrText = match[2].replace(/\/\s*$/, '');
    while ((attr = attrPattern.exec(attrText))) {
      const name = attr[1].toLowerCase();
      const value = attr[2] ?? attr[3] ?? attr[4] ?? '';
      if (!ALLOWED_ATTRS.has(name)) return { ok: false, reason: `許可していない属性: ${name}` };
      if (URL_ATTRS.has(name)) {
        const decoded = value.replace(/&amp;/g, '&');
        if (!isAllowedUrl(decoded, asp)) return { ok: false, reason: `許可していないURL: ${value.slice(0, 80)}` };
        if (tag === 'a' && name === 'href') hasLink = true;
      }
      if (name === 'style' && FORBIDDEN_STYLE.test(value)) return { ok: false, reason: 'style属性に使えない指定があります' };
      if (name === 'target' && !['_blank', '_self'].includes(value)) return { ok: false, reason: `target属性の値: ${value}` };
    }
  }
  rest += body.slice(last);
  if (rest.includes('<') || rest.includes('>')) return { ok: false, reason: 'タグとして解釈できない「<」「>」があります' };
  if (!hasLink) return { ok: false, reason: '広告リンク（<a href>）がありません' };
  return { ok: true };
}

// 素材が表示できる状態か（ASPの許可ドメイン・必須項目）。
export function checkLinkMaterial(link: AffiliateLink, asp: AspName): HtmlCheck {
  if (link.mode === 'rawHtml') return checkRawHtml(link.rawHtml, asp);
  if (!isAllowedUrl(link.href, asp)) return { ok: false, reason: 'hrefがASPの許可ドメインのhttps URLではありません' };
  if (link.impressionPixel && !isAllowedUrl(link.impressionPixel, asp))
    return { ok: false, reason: 'impressionPixelがASPの許可ドメインのhttps URLではありません' };
  if (!link.label || !link.label.trim()) return { ok: false, reason: 'labelがありません' };
  return { ok: true };
}

function earlier(left: string | null, right: string | null | undefined): string | null {
  const r = right && isIsoDate(right) ? right : null;
  if (!left) return r;
  if (!r) return left;
  return left < r ? left : r;
}

// 複数の期限のうち一番遅いもの。期限なし（null）が1つでもあれば null（＝期限なし）。
export function latestUntil(values: readonly (string | null)[]): string | null {
  if (values.length === 0 || values.some((value) => value === null)) return null;
  return [...(values as string[])].sort().at(-1) ?? null;
}

function programIsActive(program: AffiliateProgram | undefined, today: string): program is AffiliateProgram {
  return Boolean(
    program &&
      program.partnershipStatus === 'approved' &&
      program.enabled === true &&
      isWithinPeriod(today, program.validFrom, program.validUntil),
  );
}

function placementMatches(placement: AffiliatePlacement, slot: string, pageType: PageType, pageKey: string): boolean {
  if (!placement.enabled || placement.slot !== slot || !placement.pageTypes.includes(pageType)) return false;
  return !placement.pageKeys || placement.pageKeys.length === 0 || placement.pageKeys.includes(pageKey);
}

export type SlotQuery = { readonly slot: string; readonly pageType: PageType; readonly pageKey: string; readonly today: string };

// ある枠に表示する素材を決める。該当なしなら null（枠ごと描画しない）。
export function selectSlot(data: AffiliateData, query: SlotQuery): SelectedSlot | null {
  const placement = data.placements.find((item) => placementMatches(item, query.slot, query.pageType, query.pageKey));
  if (!placement) return null;
  const programs = new Map(data.programs.map((program) => [program.id, program]));
  const items: SelectedItem[] = [];
  const seen = new Set<string>();
  for (const link of data.links) {
    if (items.length >= Math.max(0, placement.maxItems)) break;
    if (seen.has(link.id)) continue;
    const program = programs.get(link.programId);
    if (!programIsActive(program, query.today)) continue;
    if (!link.enabled || !isWithinPeriod(query.today, null, link.validUntil)) continue;
    if (!link.categories.some((category) => placement.categories.includes(category))) continue;
    if (!checkLinkMaterial(link, program.asp).ok) continue;
    seen.add(link.id);
    items.push({ program, link, until: earlier(earlier(null, program.validUntil), link.validUntil) });
  }
  if (items.length === 0) return null;
  return { placement, items, until: latestUntil(items.map((item) => item.until)) };
}

// ページ内の全枠をまとめて判定する（記事上部のPR表記を出すかどうかに使う）。
export function selectPage(data: AffiliateData, pageType: PageType, pageKey: string, today: string): SelectedSlot[] {
  const slots = [...new Set(data.placements.map((placement) => placement.slot))];
  return slots
    .map((slot) => selectSlot(data, { slot, pageType, pageKey, today }))
    .filter((slot): slot is SelectedSlot => slot !== null);
}
