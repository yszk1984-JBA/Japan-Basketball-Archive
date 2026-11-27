/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import { AffiliateSlot } from '../../affiliate/AffiliateSlot';
import { GuideLayout, guideMetadata } from '../GuideLayout';

const SLUG = 'basketball-ball-size';
export const metadata = guideMetadata(SLUG);

// 数値はすべて出典（FIBA・日本バスケットボール協会）の規格・条文から。推測で補わない。
// 規格が改定されたら、表の数値と guide-data.ts の checkedAt / updatedAt を更新する。
const SIZE_SPECS = [
  { size: '7号', circumference: '750〜770mm', weight: '580〜620g', use: 'すべての男子の大会' },
  { size: '6号', circumference: '715〜730mm', weight: '510〜550g', use: 'すべての女子の大会' },
  { size: '5号', circumference: '685〜700mm', weight: '465〜495g', use: 'ミニバスケットボール' },
  { size: '軽量5号', circumference: '685〜700mm', weight: '360〜390g', use: 'ミニバスケットボール' },
] as const;

export default function Page() {
  return (
    <GuideLayout
      slug={SLUG}
      related={[
        { label: 'B.LEAGUE選手の出身高校ランキング', href: '/rankings/high-school' },
        { label: 'コラム：B.LEAGUE選手を多く輩出する高校の共通点', href: '/columns/high-school-trends' },
        { label: '選手一覧（出身校からたどる）', href: '/players' },
      ]}
      references={[
        {
          label: 'Official Basketball Rules 2024 – Basketball Equipment',
          publisher: 'FIBA（国際バスケットボール連盟）',
          date: '2024年10月1日発効',
          href: 'https://assets.fiba.basketball/image/upload/documents-corporate-fiba-official-rules-2024-official-basketball-rules-and-basketball-equipment.pdf',
        },
        {
          label: '2026 バスケットボール競技規則',
          publisher: '日本バスケットボール協会',
          date: '2026年4月1日施行',
          href: 'https://www.japanbasketball.jp/files/referee/rule/2026rule.pdf',
        },
        {
          label: '2026 ミニバスケットボール競技規則（ミニバスケットボールにおける適用規則の相違点）',
          publisher: '日本バスケットボール協会',
          date: '2026年4月1日施行',
          href: 'https://www.japanbasketball.jp/wp-content/uploads/2026rule_MiniBasketball_v1.pdf',
        },
        {
          label: '各種規程（バスケットボール施設・用器具について）',
          publisher: '日本バスケットボール協会',
          date: '2026年11月28日確認',
          href: 'https://www.japanbasketball.jp/jba/kitei/',
        },
        {
          label: 'バスケットボール施設・用器具規格（2021年4月1日改訂版）',
          publisher: '日本バスケットボール協会',
          date: '2021年4月1日',
          href: 'https://www.japanbasketball.jp/wp-content/uploads/Facility-equipment_20210401.pdf',
        },
        {
          label: 'FIBA 3x3 Official Game Basketball（製品情報）',
          publisher: 'Wilson（FIBA 3x3公式球のメーカー）',
          date: '2026年11月28日確認',
          href: 'https://www.wilson.com/en-us/products/fiba-3x3-official-game-basketball-wz10018',
        },
      ]}
    >
      <section>
        <p>
          バスケットボールのボールには5号・6号・7号などの「号数」があり、使う号数は競技規則で決まっています。結論から言うと、
          <strong>小学生（ミニバス）は男女とも5号、中学生以上は男子が7号、女子が6号</strong>
          です。この記事では、号数ごとの大きさと重さ、試合球と練習球の違い、屋内用と屋外用の違い、買うときに確かめたいポイントを、国際バスケットボール連盟（FIBA）と日本バスケットボール協会（JBA）の規則をもとにまとめます。
        </p>
      </section>

      <section>
        <h2>早見表：年代・男女別の号数</h2>
        <div className="jbaGuide-tableWrap">
          <table className="jbaGuide-table">
            <thead>
              <tr>
                <th scope="col">区分</th>
                <th scope="col">号数</th>
                <th scope="col">根拠</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>小学生（ミニバスケットボール、U12）男子・女子</td>
                <td>5号または軽量5号</td>
                <td>JBA「ミニバスケットボール競技規則」第3条</td>
              </tr>
              <tr>
                <td>中学生以上の男子（中学・高校・大学・一般）</td>
                <td>7号</td>
                <td>FIBA規格「すべての男子の大会では7号」</td>
              </tr>
              <tr>
                <td>中学生以上の女子（中学・高校・大学・一般）</td>
                <td>6号</td>
                <td>FIBA規格「すべての女子の大会では6号」</td>
              </tr>
              <tr>
                <td>3x3（3人制）</td>
                <td>3x3専用のボール</td>
                <td>6号の大きさで7号の重さ（メーカー公表の仕様）</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p style={{ fontSize: 13 }}>
          JBAの「バスケットボール競技規則」は、ボールの詳しい規格をFIBAの「Basketball Equipment」によるとしています。国内の大会も、この規格にもとづいて号数が決まります。
        </p>
      </section>

      <section>
        <h2>5号・6号・7号の違い：大きさと重さ</h2>
        <p>FIBAの2024年版の規格では、号数ごとの円周と重さの範囲が次のように決まっています。</p>
        <div className="jbaGuide-tableWrap">
          <table className="jbaGuide-table">
            <thead>
              <tr>
                <th scope="col">号数</th>
                <th scope="col">円周</th>
                <th scope="col">重さ</th>
                <th scope="col">使う大会</th>
              </tr>
            </thead>
            <tbody>
              {SIZE_SPECS.map((spec) => (
                <tr key={spec.size}>
                  <td>{spec.size}</td>
                  <td>{spec.circumference}</td>
                  <td>{spec.weight}</td>
                  <td>{spec.use}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <ul>
          <li>軽量5号は、大きさは5号と同じで、重さが約100g軽いボールです。</li>
          <li>規格の範囲で比べると、7号は5号より円周が5〜8cmほど大きく、重さは85〜155gほど重くなります。</li>
          <li>
            インターネット上では、以前の版の規格の数値（7号で円周749〜780mm、重さ567〜650gなど）が書かれていることがあります。最新の範囲は上の表のとおりです。
          </li>
          <li>規格では、ボールに号数と推奨空気圧（またはその範囲）を表示することになっています。</li>
        </ul>
      </section>

      <section>
        <h2>年齢・競技カテゴリー別の選び方</h2>
        <ul>
          <li>
            <strong>小学生（ミニバス）：</strong>JBAのミニバスケットボール競技規則で「5号または軽量5号」と決まっています。男女の区別はありません。ミニバスはリングの高さも2.60mと、一般の3.05mより低く決められています。
          </li>
          <li>
            <strong>中学生：</strong>中学校に上がると、男子は7号、女子は6号になります。男子は5号から一気に7号へ、女子は5号から6号へ切り替わるので、進学先のチームで使う号数を確かめてから買うと無駄がありません。
          </li>
          <li>
            <strong>高校生・大学生・一般：</strong>中学と同じく、男子は7号、女子は6号です。
          </li>
          <li>
            <strong>3x3：</strong>3x3（3人制）は専用のボールを使います。メーカーの公表では、6号と同じ大きさで、7号と同じ重さです。5人制のボールとは別物なので、3x3の大会に出るなら3x3用を選びます。
          </li>
        </ul>
      </section>

      <section>
        <h2>男子と女子で違うこと</h2>
        <p>
          FIBAの規格では「すべての男子の大会では7号、すべての女子の大会では6号を使う」と決められています。年代による区別はなく、中学生以上は大会のカテゴリー（男子・女子）で号数が決まります。ミニバス（小学生）だけは、男女とも5号（または軽量5号）です。
        </p>
      </section>

      <section>
        <h2>公式試合用と練習用の違い</h2>
        <ul>
          <li>
            <strong>試合で使うボールは大会が決めます。</strong>
            競技規則では、国内の大会の試合球は大会の主催者の考えで決めるとされています。試合に向けて練習するなら、出場する大会の要項で試合球（メーカー・品番）を確かめておくと安心です。
          </li>
          <li>
            <strong>検定球：</strong>JBAは「施設・用器具規格」にもとづいてボールを検定しています。対象は皮革製・合成皮革製・ゴム製のボールです。商品に「検定球」と表示されているのは、この検定を受けたボールです。
          </li>
          <li>
            <strong>表面の素材と大会のレベル：</strong>FIBAの規格では、最も高いレベルの大会（Level 1）で使うボールは、表面が天然皮革か人工皮革（合成皮革）でなければなりません。それ以外のレベル（Level 2）では、ゴム製の表面も認められています。
          </li>
          <li>
            「試合球」「練習球」は、規則上の区分ではなく商品の表示です。号数・検定球かどうか・表面の素材をあわせて確認しましょう。
          </li>
        </ul>
      </section>

      <section>
        <h2>屋内用と屋外用の違い</h2>
        <p>
          競技規則には「屋内用」「屋外用」という区分はありません。規則が決めているのは、号数ごとの大きさ・重さ・弾み方と、大会のレベルに応じた表面の素材です。
        </p>
        <p>
          屋内用・屋外用は、メーカーが商品ごとに示している「推奨使用環境」です。体育館で使うのか、屋外のコートや公園で使うのかを決めてから、商品の表示（推奨使用環境と表面の素材：天然皮革・人工皮革・ゴム）を確かめて選びます。屋外向けとされていないボールを屋外で使うと、表面が傷みやすくなる場合があります。
        </p>
      </section>

      <section>
        <h2>購入時に確かめたいポイント</h2>
        <ol>
          <li>
            <strong>号数：</strong>使う人の年代と、男子・女子で決まります（早見表を参照）。ボール本体と商品説明の両方に号数が書かれているかを確かめます。
          </li>
          <li>
            <strong>対象の表示：</strong>メーカーは「中学生以上男子」「小学生用」のように対象を表示していることが多いので、号数とあわせて確認します。
          </li>
          <li>
            <strong>検定球かどうか：</strong>チームの練習や大会を想定するなら、検定球の表示を確かめます。
          </li>
          <li>
            <strong>使う場所と素材：</strong>屋内か屋外か、推奨使用環境と表面の素材を確かめます。
          </li>
          <li>
            <strong>空気圧と空気入れ：</strong>ボールに表示された推奨空気圧に合わせます。目安として、規格では約1,800mmの高さから落としたときに、一般のボールは1,035〜1,085mm、ミニバスのボールは960〜1,160mmの高さまで弾む空気圧とされています（ボールの下の端で測った高さ）。空気入れ（ポンプ）と針が別売りの商品もあります。
          </li>
          <li>
            <strong>3x3用かどうか：</strong>3x3用のボールは5人制のボールと仕様が違います。
          </li>
        </ol>
        <AffiliateSlot slot="guide-shopping" pageType="guide" pageKey={SLUG} />
      </section>

      <section>
        <h2>ミニバスから中学・高校、そしてプロへ</h2>
        <p>
          5号のボールで始めたミニバスの選手たちが、中学・高校で7号・6号に持ち替え、その先のB.LEAGUEへ進んでいきます。Rosterlineでは、B.LEAGUE選手が
          <a href="/rankings/high-school">どの高校の出身か</a>
          をランキングにしているほか、
          <a href="/players">選手ごとの経歴</a>
          を、出典とともに高校・大学からたどれるようにしています。
        </p>
      </section>
    </GuideLayout>
  );
}
