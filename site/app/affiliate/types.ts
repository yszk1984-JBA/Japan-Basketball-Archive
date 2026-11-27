// Affiliate Engine v0.1 の型。データ本体は同じフォルダのJSON（programs / links / placements）。
// 広告データはバスケットボールのデータ（data/、master-data.ts）とは分けて持つ。Governance（RAW→MASTER）の対象外。
// 運用手順は docs/AFFILIATE_ENGINE.md を参照。

export type AspName = 'a8' | 'rakuten';

// 広告を置くページの種類。GA4で「Archive／Ranking／Column／Guide」別にクリック率を比べるための区分にもなる。
// v0.1では archive（選手・組織ページ）には広告を置かない。
export type PageType = 'archive' | 'ranking' | 'column' | 'guide';

// 案件（Affiliate Master）。ASPとの提携単位。
export type AffiliateProgram = {
  readonly id: string; // AFF000001 形式。変更しない
  readonly name: string;
  readonly asp: AspName;
  readonly aspProgramId?: string; // ASP側のID（記録用。表示しない）
  // ASPの管理画面で運営者が確認した提携状況。approved 以外は表示しない。
  readonly partnershipStatus: 'pending' | 'approved' | 'rejected' | 'ended';
  readonly enabled: boolean; // 運営者の表示スイッチ（Enable / Disable）
  readonly validFrom?: string | null; // YYYY-MM-DD（日本時間）。この日から表示
  readonly validUntil?: string | null; // YYYY-MM-DD（日本時間）。この日まで表示。null は期限なし
  readonly termsCheckedAt?: string | null; // 報酬条件・掲載規約を最後に確認した日
  readonly reward?: { readonly rate?: string; readonly epc?: string; readonly approvalRate?: string; readonly note?: string };
  readonly categories: readonly string[];
  readonly restrictions?: readonly string[]; // 掲載規約上の制約メモ
  // ASP・広告主から指定された表記がある場合に、広告枠に表示する文言
  readonly requiredDisclosure?: string | null;
  readonly notes?: string;
};

// 正式な広告素材（Link Manager）。ASPが発行したものをそのまま登録する。推測で作らない。
export type AffiliateLink = {
  readonly id: string; // LNK000001 形式
  readonly programId: string;
  readonly kind: 'text' | 'banner' | 'product';
  // fields: ASPがリンクURLと計測用画像を分けて使うことを認めている素材（文言を変更できるテキスト素材など）
  // rawHtml: ASP発行のコードを無加工で出力する素材（バナー・商品リンクなど）
  readonly mode: 'fields' | 'rawHtml';
  readonly href?: string; // mode: fields。ASP発行のURL（コピペ）
  readonly impressionPixel?: string | null; // mode: fields。ASP発行の計測用画像URL（ある場合のみ）
  readonly label?: string; // mode: fields。ASPが文言の変更を認めている素材だけ
  readonly rawHtml?: string; // mode: rawHtml。ASP発行コード全文（コピペ、改変しない）
  readonly categories: readonly string[];
  readonly enabled: boolean;
  readonly validUntil?: string | null;
  readonly issuedAt?: string | null; // 運営者がASPから素材を取得した日
  readonly notes?: string;
};

// 表示ルール（Placement Rules）。ページ側は「枠（slot）」を置くだけで、何を出すかはここで決める。
export type AffiliatePlacement = {
  readonly id: string; // PLC001 形式
  readonly slot: string;
  readonly pageTypes: readonly PageType[];
  readonly pageKeys?: readonly string[]; // 指定したページだけに出す（パイロット用）。省略時は pageTypes の全ページ
  readonly categories: readonly string[];
  readonly maxItems: number;
  readonly enabled: boolean;
  readonly heading?: string;
};

export type AffiliateData = {
  readonly programs: readonly AffiliateProgram[];
  readonly links: readonly AffiliateLink[];
  readonly placements: readonly AffiliatePlacement[];
};

// 広告枠に表示する1件分。
export type SelectedItem = {
  readonly program: AffiliateProgram;
  readonly link: AffiliateLink;
  // 表示期限（Program と Link の早い方）。null は期限なし。期限切れの非表示処理に使う
  readonly until: string | null;
};

export type SelectedSlot = {
  readonly placement: AffiliatePlacement;
  readonly items: readonly SelectedItem[];
  readonly until: string | null; // 枠内で一番遅い期限（全件が切れたら枠ごと消す）。期限なしが1件でもあれば null
};
