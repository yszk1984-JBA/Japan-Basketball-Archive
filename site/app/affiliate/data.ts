// 広告データ（JSON）の読み込み。JSONを編集してcommit・pushすると、次のデプロイで反映される。
import type { AffiliateData, AffiliateLink, AffiliatePlacement, AffiliateProgram } from './types';
import programs from './programs.json';
import links from './links.json';
import placements from './placements.json';

export const affiliateData: AffiliateData = {
  programs: programs as readonly AffiliateProgram[],
  links: links as readonly AffiliateLink[],
  placements: placements as readonly AffiliatePlacement[],
};
