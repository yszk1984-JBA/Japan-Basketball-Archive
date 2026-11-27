// 共通の広告枠（Affiliate Component）と、記事上部のPR表記。
// ページ側は <AffiliateSlot slot=... pageType=... pageKey=... /> を置くだけ。表示する素材は placements.json で決める。
// 表示できる素材が1件もなければ、見出し・PR表記を含めて何も描画しない。
import { AffiliateNoticeClient, AffiliateSlotClient } from './AffiliateClient';
import { affiliateData } from './data';
import { latestUntil, selectPage, selectSlot, todayJst } from './select';
import type { AffiliateData, PageType, SelectedItem } from './types';

export const AFFILIATE_NOTICE_TEXT =
  '本ページにはアフィリエイト広告が含まれています。掲載リンクを通じて商品・サービスを購入した場合、当サイトが報酬を受け取ることがあります。';

type SlotProps = {
  readonly slot: string;
  readonly pageType: PageType;
  readonly pageKey: string;
  // テスト用。通常は省略（JSONのデータとビルド時点の日本時間の日付を使う）
  readonly data?: AffiliateData;
  readonly today?: string;
};

function ItemBody({ item }: { item: SelectedItem }) {
  const { link, program } = item;
  if (link.mode === 'rawHtml') {
    // ASP発行コードを無加工で出力する（checkRawHtmlで許可したタグ・属性・ドメインだけのものに限る）。
    return <div className="jbaAff-raw" dangerouslySetInnerHTML={{ __html: link.rawHtml ?? '' }} />;
  }
  return (
    <>
      <a className="jbaAff-button" href={link.href} target="_blank" rel="sponsored noopener">
        <span className="jbaAff-buttonLabel">{link.label}</span>
        <span className="jbaAff-buttonShop">{program.name}</span>
      </a>
      {link.impressionPixel ? (
        // ASPの計測用画像（1×1）。ASPのURLをそのまま読み込むため、画像最適化（next/image）は通さない
        // oxlint-disable-next-line next/no-img-element
        <img className="jbaAff-pixel" src={link.impressionPixel} width={1} height={1} alt="" loading="eager" />
      ) : null}
    </>
  );
}

export function AffiliateSlot({ slot, pageType, pageKey, data = affiliateData, today = todayJst() }: SlotProps) {
  const selected = selectSlot(data, { slot, pageType, pageKey, today });
  if (!selected) return null;
  const { placement, items } = selected;
  const disclosures = [...new Set(items.map((item) => item.program.requiredDisclosure).filter((text): text is string => Boolean(text)))];

  return (
    <AffiliateSlotClient className="jbaAff-slot" until={selected.until}>
      <div className="jbaAff-head">
        <span className="jbaAff-badge">PR</span>
        <span>広告（アフィリエイト）</span>
      </div>
      {placement.heading ? <p className="jbaAff-heading">{placement.heading}</p> : null}
      <ul className="jbaAff-items">
        {items.map((item) => (
          <li
            key={item.link.id}
            className="jbaAff-item"
            data-aff-item=""
            data-aff-program={item.program.id}
            data-aff-link={item.link.id}
            data-aff-asp={item.program.asp}
            data-aff-page-type={pageType}
            data-aff-placement={placement.id}
            data-aff-until={item.until ?? undefined}
          >
            <ItemBody item={item} />
          </li>
        ))}
      </ul>
      {disclosures.map((text) => (
        <p key={text} className="jbaAff-note">
          {text}
        </p>
      ))}
      <p className="jbaAff-note">
        リンク先のショップで購入・予約されると、運営者に報酬が支払われることがあります。商品の仕様・価格・在庫はリンク先でご確認ください。広告主は本サイトの記事・データの内容に関与していません。
      </p>
    </AffiliateSlotClient>
  );
}

// 記事上部のPR表記。そのページに表示される広告が1件以上あるときだけ出す。
export function AffiliateNotice({
  pageType,
  pageKey,
  data = affiliateData,
  today = todayJst(),
}: Omit<SlotProps, 'slot'>) {
  const slots = selectPage(data, pageType, pageKey, today);
  if (slots.length === 0) return null;
  return (
    <AffiliateNoticeClient until={latestUntil(slots.map((slot) => slot.until))}>
      <span className="jbaAff-badge">PR</span>
      {AFFILIATE_NOTICE_TEXT}
    </AffiliateNoticeClient>
  );
}
