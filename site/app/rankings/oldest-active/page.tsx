import { ExtraRankingPage, extraRankingMetadata } from '../ExtraRankingPage';

export const metadata = extraRankingMetadata('oldest-active');

export default function Page() {
  return <ExtraRankingPage id="oldest-active" />;
}
