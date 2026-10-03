// 現行（2026-27シーズン）のB.PREMIER（26クラブ）・B.ONE（25クラブ）、計51クラブの
// メインカラーを、プレイヤーカードの「ワンポイント」バッジ用に保持する表示専用データ。
//
// 注意：
// - 対象はプロクラブ（B.PREMIER/B.ONE）のみ。高校・大学など他の組織には付与しない。
// - 色の多くは、各クラブの公式サイトが正式なHEXコード／RGB値を公開していないため、
//   Wikipedia等に記載されたチームカラーの色名（例：「ハピネッツピンク」）やロゴの見た目から
//   近似値として割り当てたものであり、各クラブの正式なブランドガイドラインの値とは異なる
//   場合がある。あくまで一覧性を高めるための装飾（アクセント）であり、公式表記として
//   扱わないこと。
// - Master/Candidateのデータスキーマ（Person/Career/Organization）には一切変更を加えていない。
export type ClubColorSourceType = 'wikipedia_infobox' | 'visual_estimate';

export type ClubColorEntry = {
  readonly color: string;
  readonly league: 'PREMIER' | 'B.ONE';
  readonly sourceType: ClubColorSourceType;
};

export const CLUB_COLORS: Readonly<Record<string, ClubColorEntry>> = {
  ORG000144: { color: '#1B1E2A', league: 'PREMIER', sourceType: 'wikipedia_infobox' },
  ORG000109: { color: '#E2001A', league: 'PREMIER', sourceType: 'wikipedia_infobox' },
  ORG000130: { color: '#0078BE', league: 'PREMIER', sourceType: 'wikipedia_infobox' },
  ORG000092: { color: '#1E9F46', league: 'PREMIER', sourceType: 'wikipedia_infobox' },
  ORG000097: { color: '#DA291C', league: 'PREMIER', sourceType: 'wikipedia_infobox' },
  ORG000042: { color: '#00A7DB', league: 'PREMIER', sourceType: 'wikipedia_infobox' },
  ORG000132: { color: '#FFD400', league: 'PREMIER', sourceType: 'wikipedia_infobox' },
  ORG000048: { color: '#0075C2', league: 'PREMIER', sourceType: 'wikipedia_infobox' },
  ORG000150: { color: '#C8102E', league: 'PREMIER', sourceType: 'visual_estimate' },
  ORG000118: { color: '#E6002D', league: 'PREMIER', sourceType: 'wikipedia_infobox' },
  ORG000054: { color: '#E4002B', league: 'PREMIER', sourceType: 'wikipedia_infobox' },
  ORG000142: { color: '#E4002B', league: 'PREMIER', sourceType: 'wikipedia_infobox' },
  ORG000047: { color: '#1D3461', league: 'PREMIER', sourceType: 'wikipedia_infobox' },
  ORG000149: { color: '#E3001B', league: 'PREMIER', sourceType: 'wikipedia_infobox' },
  ORG000155: { color: '#005BAC', league: 'PREMIER', sourceType: 'wikipedia_infobox' },
  ORG000122: { color: '#D7000F', league: 'PREMIER', sourceType: 'wikipedia_infobox' },
  ORG000110: { color: '#EB6101', league: 'PREMIER', sourceType: 'wikipedia_infobox' },
  ORG000114: { color: '#FFD400', league: 'PREMIER', sourceType: 'wikipedia_infobox' },
  ORG000055: { color: '#0C2340', league: 'PREMIER', sourceType: 'wikipedia_infobox' },
  ORG000153: { color: '#0070C0', league: 'PREMIER', sourceType: 'wikipedia_infobox' },
  ORG000106: { color: '#C9A227', league: 'PREMIER', sourceType: 'wikipedia_infobox' },
  ORG000043: { color: '#00A650', league: 'PREMIER', sourceType: 'wikipedia_infobox' },
  ORG000137: { color: '#E4007F', league: 'PREMIER', sourceType: 'wikipedia_infobox' },
  ORG000143: { color: '#D7000F', league: 'PREMIER', sourceType: 'visual_estimate' },
  ORG000103: { color: '#0086D1', league: 'PREMIER', sourceType: 'wikipedia_infobox' },
  ORG000135: { color: '#F7B500', league: 'PREMIER', sourceType: 'visual_estimate' },

  ORG000183: { color: '#C8102E', league: 'B.ONE', sourceType: 'wikipedia_infobox' },
  ORG000046: { color: '#0C1F3D', league: 'B.ONE', sourceType: 'wikipedia_infobox' },
  ORG000222: { color: '#0068B7', league: 'B.ONE', sourceType: 'wikipedia_infobox' },
  ORG000171: { color: '#E2231A', league: 'B.ONE', sourceType: 'wikipedia_infobox' },
  ORG000180: { color: '#1C3664', league: 'B.ONE', sourceType: 'visual_estimate' },
  ORG000227: { color: '#F39800', league: 'B.ONE', sourceType: 'wikipedia_infobox' },
  ORG000040: { color: '#0F4C91', league: 'B.ONE', sourceType: 'visual_estimate' },
  ORG000181: { color: '#C8102E', league: 'B.ONE', sourceType: 'visual_estimate' },
  ORG000226: { color: '#1A1A1A', league: 'B.ONE', sourceType: 'wikipedia_infobox' },
  ORG000173: { color: '#C8102E', league: 'B.ONE', sourceType: 'wikipedia_infobox' },
  ORG000116: { color: '#2E8B57', league: 'B.ONE', sourceType: 'visual_estimate' },
  ORG000091: { color: '#F39800', league: 'B.ONE', sourceType: 'wikipedia_infobox' },
  ORG000052: { color: '#F39800', league: 'B.ONE', sourceType: 'wikipedia_infobox' },
  ORG000223: { color: '#002855', league: 'B.ONE', sourceType: 'visual_estimate' },
  ORG000111: { color: '#F2A900', league: 'B.ONE', sourceType: 'visual_estimate' },
  ORG000090: { color: '#2E8540', league: 'B.ONE', sourceType: 'wikipedia_infobox' },
  ORG000067: { color: '#C8102E', league: 'B.ONE', sourceType: 'wikipedia_infobox' },
  ORG000200: { color: '#0095D9', league: 'B.ONE', sourceType: 'visual_estimate' },
  ORG000202: { color: '#8E3B8F', league: 'B.ONE', sourceType: 'wikipedia_infobox' },
  ORG000115: { color: '#F39800', league: 'B.ONE', sourceType: 'wikipedia_infobox' },
  ORG000190: { color: '#800020', league: 'B.ONE', sourceType: 'wikipedia_infobox' },
  ORG000205: { color: '#C8102E', league: 'B.ONE', sourceType: 'visual_estimate' },
  ORG000182: { color: '#0078BE', league: 'B.ONE', sourceType: 'wikipedia_infobox' },
  ORG000224: { color: '#1A1A1A', league: 'B.ONE', sourceType: 'wikipedia_infobox' },
  ORG000101: { color: '#1A1A1A', league: 'B.ONE', sourceType: 'wikipedia_infobox' },
};

export function clubColor(organizationId: string | undefined): string | undefined {
  if (!organizationId) return undefined;
  return CLUB_COLORS[organizationId]?.color;
}
