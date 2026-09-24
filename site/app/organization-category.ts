// 組織カテゴリー（高校／大学／クラブ／海外／その他）の推定ロジック。
//
// 重要：これは「表示専用」のヒューリスティックであり、Master/Candidateの
// データスキーマ（organization_candidates.csv / data/master/organization.csv）
// には一切変更を加えていない。組織種別を表す列はデータ側に存在しないため、
// 組織名の文字列パターンから機械的に推定した「見た目上の分類」に過ぎない。
// is_official_publisher()（build_site_candidate_data.py）と同じ考え方：
// 既存データには手を入れず、表示層でだけカテゴリを推定する。
//
// 新しい組織が追加されたとき、この一覧に該当しない海外組織・クラブ名は
// 「その他」に分類される（誤分類ではなく、未登録なだけ）。実際の分類と
// ズレを見つけたら、下記のリストに追記して調整する。

export type OrganizationCategory = 'hs' | 'univ' | 'club' | 'overseas' | 'other';

export const ORGANIZATION_CATEGORY_META: Record<
  OrganizationCategory,
  { readonly label: string; readonly bg: string; readonly color: string }
> = {
  hs: { label: '高校', bg: '#E7F7F5', color: '#1E8577' },
  univ: { label: '大学', bg: '#F1ECFE', color: '#6941C6' },
  club: { label: 'クラブ', bg: '#FEF0E6', color: '#B45A1E' },
  overseas: { label: '海外', bg: '#E8F0FE', color: '#1D5FD6' },
  other: { label: 'その他', bg: '#EEF1F4', color: '#5B6B7A' },
};

export const ORGANIZATION_CATEGORY_ORDER: readonly OrganizationCategory[] = [
  'hs',
  'univ',
  'club',
  'overseas',
  'other',
];

// 組織名に含まれていれば「海外」と判定するマーカー。高校・大学の文字列
// マッチより先に評価する（例：「モントロス・クリスチャン高等学校」は
// 実在の米国の高校のため、「高等学校」判定より先に海外判定を優先する）。
const OVERSEAS_MARKERS: readonly string[] = [
  'School',
  'スクール',
  'College',
  'University',
  'モントロス・クリスチャン',
  'グリズリーズ',
  'レジェンズ',
  'シカゴ・ブルズ',
  'クリッパーズ',
  'ゴンザガ',
  'ネブラスカ',
  'ジョージア工科',
  'ステッソン',
  'オクラホマ州立',
  'ブルーフィールド',
  'ブリガムヤング',
  'ジョージ・ワシントン',
];

// 国内のB.LEAGUE／実業団等のバスケットボールクラブ名（表示分類のためだけの
// 一覧。公開情報＝チーム名の一覧であり、Master/Candidateデータそのものでは
// ない）。未登録のクラブ名は「その他」に分類される。
const KNOWN_CLUB_NAMES = new Set<string>([
  'ライジングゼファー福岡',
  '京都ハンナリーズ',
  '神戸ストークス',
  'アースフレンズ東京Z',
  '宇都宮ブレックス',
  '佐賀バルーナーズ',
  'ウォルガ湘南',
  '新潟アルビレックスBB',
  '名古屋ダイヤモンドドルフィンズ',
  '横浜ビー・コルセアーズ',
  '熊本ヴォルターズ',
  '横浜エクセレンス',
  '愛媛オレンジバイキングス',
  'レバンガ北海道',
  '三遠ネオフェニックス',
  '山口パッツファイブ',
  '鹿児島レブナイズ',
  '東京サンレーヴス',
  '茨城ロボッツ',
  '三菱電機ダイヤモンドドルフィンズ',
  '琉球ゴールデンキングス',
  '琉球ゴールデンキングスU18',
  'アルバルク東京',
  '広島ドラゴンフライズ',
  '東京八王子ビートレインズ',
  '東京サンロッカーズ',
  '立川ダイス',
  '徳島ガンバロウズ',
  '千葉ジェッツ',
  '川崎ブレイブサンダース',
  'シーホース三河',
  '仙台89ERS',
  '長崎ヴェルカ',
  '秋田ノーザンハピネッツ',
  '大阪エヴェッサ',
  '群馬クレインサンダーズ',
  'アルティーリ千葉',
  '富山グラウジーズ',
  '信州ブレイブウォリアーズ',
  '滋賀レイクス',
  '島根スサノオマジック',
  'バンビシャス奈良',
  'JR東日本秋田ペッカーズ',
  '岩手ビッグブルズ',
  'しながわシティバスケットボールクラブ',
  'ファイティングイーグルス名古屋',
  '山形ワイヴァンズ',
  '青森ワッツ',
  'さいたまブロンコス',
  '越谷アルファーズ',
  'ヴィアティン三重',
  '湘南ユナイテッドBC',
  '東芝ブレイブサンダース',
]);

export function organizationCategory(name: string): OrganizationCategory {
  if (OVERSEAS_MARKERS.some((marker) => name.includes(marker))) return 'overseas';
  if (name.endsWith('高等学校') || name.endsWith('高校')) return 'hs';
  if (name.includes('大学')) return 'univ';
  if (KNOWN_CLUB_NAMES.has(name)) return 'club';
  return 'other';
}
