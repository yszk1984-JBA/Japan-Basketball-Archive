import { RankingPage, rankingMetadata } from '../RankingPage';

export const metadata = rankingMetadata('premier-university');

export default function Page() {
  return <RankingPage kind="premier-university" />;
}
