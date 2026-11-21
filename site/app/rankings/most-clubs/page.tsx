import { ExtraRankingPage, extraRankingMetadata } from '../ExtraRankingPage';

export const metadata = extraRankingMetadata('most-clubs');

export default function Page() {
  return <ExtraRankingPage id="most-clubs" />;
}
