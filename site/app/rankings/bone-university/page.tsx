import { RankingPage, rankingMetadata } from '../RankingPage';

export const metadata = rankingMetadata('bone-university');

export default function Page() {
  return <RankingPage kind="bone-university" />;
}
