import { RankingPage, rankingMetadata } from '../RankingPage';

export const metadata = rankingMetadata('high-school');

export default function Page() {
  return <RankingPage kind="high-school" />;
}
