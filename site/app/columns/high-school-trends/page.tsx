/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import { ColumnLayout, columnMetadata } from '../ColumnLayout';
import { OrgLink } from '../OrgLink';

const SLUG = 'high-school-trends';
export const metadata = columnMetadata(SLUG);

const TOP_SCHOOLS = [
  { rank: 1, name: '福岡大学附属大濠高等学校', count: 30 },
  { rank: 2, name: '洛南高等学校', count: 23 },
  { rank: 3, name: '福岡第一高等学校', count: 21 },
  { rank: 4, name: '北陸高等学校', count: 15 },
  { rank: 5, name: '中部大学第一高等学校', count: 11 },
  { rank: 5, name: '東海大学付属諏訪高等学校', count: 11 },
];

export default function Page() {
  return (
    <ColumnLayout
      slug={SLUG}
      related={[
        { label: 'B.LEAGUE選手の出身高校ランキング', href: '/rankings/high-school' },
        { label: 'B.PREMIER選手の出身高校ランキング', href: '/rankings/premier-high-school' },
        { label: 'B.ONE選手の出身高校ランキング', href: '/rankings/bone-high-school' },
        { label: '高校→大学の進学ルート', href: '/rankings/high-school-to-university' },
        { label: '同じ高校出身の選手が多いB.LEAGUEクラブ', href: '/rankings/club-high-school-alumni' },
      ]}
    >
      <section>
        <p>
          B.PREMIERとB.ONEでプレーする選手は、どの高校から来ているのでしょうか。Rosterlineに登録済みで、現在この2リーグのクラブに所属している選手498人の出身高校を集計すると、<strong>179校</strong>にのぼりました。
        </p>
        <p>
          一方で、上位の数校に出身者が集まっている様子もはっきり見えます。この記事では、出身者の多い高校に共通する傾向を、データから3つ取り上げます。
        </p>
      </section>

      <section>
        <h2>傾向1：上位校への集中と、広い裾野</h2>
        <p>出身者の多い高校の上位5位（6校）だけで、B.PREMIER・B.ONEの現役選手の約2割（111人）を占めています。</p>
        <table className="jbaListB-articleTable">
          <thead>
            <tr>
              <th>順位</th>
              <th>高校</th>
              <th style={{ textAlign: 'right' }}>現役選手</th>
            </tr>
          </thead>
          <tbody>
            {TOP_SCHOOLS.map((school) => (
              <tr key={school.name}>
                <td>{school.rank}</td>
                <td>
                  <OrgLink name={school.name} />
                </td>
                <td className="num">{school.count}人</td>
              </tr>
            ))}
          </tbody>
        </table>
        <p>
          上位15校まで広げると約36%（180人）です。裏を返せば、<strong>残りの6割以上は、出身者が数人以下の160校以上から来ている</strong>
          ことになります。トップリーグへの道は、一部の高校だけに開かれているわけではありません。
        </p>
        <p>
          地域で見ると、福岡県の2校（福岡大学附属大濠・福岡第一）で51人、京都府の2校（洛南・東山）で31人と、特定の地域に出身者が集まっている点も目を引きます。
        </p>
      </section>

      <section>
        <h2>傾向2：出身者が多くのクラブに散らばっている</h2>
        <p>出身者が多い高校ほど、同じクラブに固まるのではなく、多くのクラブに分かれてプレーしています。</p>
        <ul>
          <li>
            <OrgLink name="福岡大学附属大濠高等学校" />：30人が<strong>23クラブ</strong>に所属
          </li>
          <li>
            <OrgLink name="福岡第一高等学校" />：21人が17クラブ
          </li>
          <li>
            <OrgLink name="洛南高等学校" />：23人が14クラブ
          </li>
        </ul>
        <p>
          例外的に、同じクラブに同じ高校の出身者がまとまるケースもあります。
          <OrgLink name="宇都宮ブレックス" />
          には洛南高校の出身者が5人所属しており、登録データの中では最多の組み合わせです（詳しくは「
          <a href="/rankings/club-high-school-alumni">同じ高校出身の選手が多いB.LEAGUEクラブ</a>」）。
        </p>
      </section>

      <section>
        <h2>傾向3：高校ごとに「進学先のパターン」がある</h2>
        <p>出身者の多い高校は、大学の進学先にもそれぞれの特徴があります。</p>
        <ul>
          <li>
            <strong>
              <OrgLink name="福岡大学附属大濠高等学校" />
            </strong>
            ：登録済みの出身者30人のうち10人が筑波大学へ。高校と大学の組み合わせとしては、登録データの中で最も多いルートです。
          </li>
          <li>
            <strong>
              <OrgLink name="福岡第一高等学校" />
            </strong>
            ：東海大学（8人）、日本体育大学（5人）、専修大学（4人）、日本経済大学（4人）と進学先が分かれています。大学の在籍記録がない出身者も7人います。
          </li>
          <li>
            <strong>
              <OrgLink name="東海大学付属諏訪高等学校" />
            </strong>
            ：11人のうち5人が東海大学へ。付属校から系列大学へ進むルートです。
          </li>
          <li>
            <strong>
              <OrgLink name="中部大学第一高等学校" />
            </strong>
            ：13人のうち4人が大東文化大学へ進んでいます。
          </li>
        </ul>
        <p>
          高校での経験に加えて、「どの大学を経てプロに進むか」という道筋まで含めて、選手のキャリアが形づくられている様子がうかがえます（詳しくは「
          <a href="/rankings/high-school-to-university">高校→大学の進学ルート</a>」）。
        </p>
      </section>

      <section>
        <h2>B.PREMIERとB.ONEで違いはあるか</h2>
        <p>リーグ別に見ると、順位が少し入れ替わります。</p>
        <ul>
          <li>B.PREMIER：1位 福岡大学附属大濠（17人）、2位 洛南（16人）、3位 福岡第一（10人）</li>
          <li>B.ONE：1位 福岡大学附属大濠（13人）、2位 福岡第一（11人）、3位 北陸（8人）</li>
        </ul>
        <p>洛南高校の出身者はB.PREMIERに16人、B.ONEに7人と、B.PREMIERに多いのが特徴です。</p>
      </section>

      <section>
        <h2>まとめ</h2>
        <ul>
          <li>トップリーグの選手は179校から来ており、上位6校で約2割、残りの6割以上は出身者が少数の高校から来ている</li>
          <li>出身者の多い高校ほど、多くのクラブに散らばっている</li>
          <li>高校ごとに、大学への進学先にパターンがある</li>
        </ul>
        <p>
          高校ごとの出身選手は、<a href="/rankings/high-school">出身高校ランキング</a>
          や各高校のページで一覧できます。気になる高校の卒業生が、今どのクラブでプレーしているかをたどってみてください。
        </p>
      </section>
    </ColumnLayout>
  );
}
