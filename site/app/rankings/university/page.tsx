import { RankingPage, rankingMetadata } from '../RankingPage';

export const metadata = rankingMetadata('university');

export default function Page() {
  return <RankingPage kind="university" />;
}
