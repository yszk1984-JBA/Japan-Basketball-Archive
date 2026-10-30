import { RankingPage, rankingMetadata } from '../RankingPage';

export const metadata = rankingMetadata('premier-high-school');

export default function Page() {
  return <RankingPage kind="premier-high-school" />;
}
