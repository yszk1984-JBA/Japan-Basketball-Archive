/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import { ColumnLayout, columnMetadata } from '../ColumnLayout';
import { OrgLink } from '../OrgLink';
import { PlayerLink } from '../PlayerLink';
import { References } from '../References';

const SLUG = 'salary-cap-first-year-moves';
export const metadata = columnMetadata(SLUG);

// 2026-11-26時点の確認済みデータから集計（新人＝学校からの加入は除く）。
// クラブの区分は2026-27の区分（B.PREMIER／B.ONE）を過去のシーズンにも当てはめている。
const MOVES = [
  { year: '24-25', toPremier: 70, toOne: 67, down: 27, up: 21 },
  { year: '25-26', toPremier: 72, toOne: 77, down: 35, up: 24 },
  { year: '26-27', toPremier: 59, toOne: 92, down: 37, up: 15 },
];

export default function Page() {
  return (
    <ColumnLayout
      slug={SLUG}
      related={[
        { label: 'B.LEAGUE開幕以降に所属したクラブ数が多い選手', href: '/rankings/most-clubs' },
        { label: 'B.LEAGUE開幕から同じクラブ一筋の選手', href: '/rankings/one-club' },
        { label: '組織一覧（クラブ）', href: '/organizations' },
      ]}
    >
      <section>
        <p>
          2026-27シーズン、B.LEAGUEは大きく形を変えました。最上位のB.PREMIERには、クラブが選手に支払う報酬の総額に<strong>上限8億円・下限5億円</strong>
          のサラリーキャップが導入されています。
        </p>
        <p>
          この制度は、選手の動きにどう表れたのでしょうか。Rosterlineに登録済みの選手の移籍を集計し、制度の狙いとあわせて、選手の立場から整理します。
        </p>
      </section>

      <section>
        <h2>制度のポイント</h2>
        <ul>
          <li>B.PREMIERのクラブは、選手報酬の総額を5億〜8億円に収める。外国籍・帰化・アジア枠の選手も含めた全選手が対象。</li>
          <li>例外は「スター選手条項」だけで、1人に限り、実際の報酬にかかわらず1.5億円として計算できる。</li>
          <li>違反した場合は、原則として2シーズン後の降格、翌シーズンの15勝の減算、超過額の5倍の制裁金。</li>
          <li>
            リーグは狙いとして、戦力の均衡、クラブ経営の健全化、ビジネス人材への投資を挙げています。島田慎二コミッショナーは「地方のクラブにも優勝のチャンスがある」と語っています。
          </li>
        </ul>
        <p>
          2026年11月にリーグが公表した開幕時点の報酬総額では、
          <OrgLink name="アルティーリ千葉" />
          が上限を約2,100万円上回っていました（最終的な判定は、2027年9月に公表される確定額で行われます）。
        </p>
      </section>

      <section>
        <h2>データ：B.PREMIERへの移籍は約2割減</h2>
        <p>シーズンごとに、新しいクラブに移った選手の数を数えました（大学・高校からの新人は除く。PはB.PREMIER、ONEはB.ONEのクラブ）。</p>
        <table className="jbaListB-articleTable">
          <thead>
            <tr>
              <th>シーズン</th>
              <th style={{ textAlign: 'right' }}>PREMIERへ</th>
              <th style={{ textAlign: 'right' }}>ONEへ</th>
              <th style={{ textAlign: 'right' }}>P→ONE</th>
              <th style={{ textAlign: 'right' }}>ONE→P</th>
            </tr>
          </thead>
          <tbody>
            {MOVES.map((row) => (
              <tr key={row.year}>
                <td>{row.year}</td>
                <td className="num">{row.toPremier}人</td>
                <td className="num">{row.toOne}人</td>
                <td className="num">{row.down}人</td>
                <td className="num">{row.up}人</td>
              </tr>
            ))}
          </tbody>
        </table>
        <ul>
          <li>
            B.PREMIERのクラブへの移籍は、前のシーズンの72人から<strong>59人へ、約2割減</strong>りました。
          </li>
          <li>
            反対に、B.ONEのクラブへの移籍は77人から<strong>92人へ、約2割増</strong>えています。
          </li>
          <li>
            B.PREMIERのクラブからB.ONEのクラブへ移った選手（37人）は、逆の方向（15人）の<strong>約2.5倍</strong>
            。B.ONEからB.PREMIERへ上がった選手は、比べた中で最も少なくなりました。
          </li>
        </ul>
        <p>
          たとえば、
          <PlayerLink name="小野 龍猛" />
          （京都ハンナリーズ→バンビシャス奈良）、<PlayerLink name="鈴木 達也" />
          （大阪エヴェッサ→バンビシャス奈良）、<PlayerLink name="小寺 ハミルトンゲイリー" />
          （広島ドラゴンフライズ→香川ファイブアローズ）は、B.PREMIERのクラブからB.ONEのクラブへ移りました。一方で、
          <PlayerLink name="並里 成" />
          （ファイティングイーグルス名古屋→横浜ビー・コルセアーズ）、<PlayerLink name="松山 駿" />
          （越谷アルファーズ→川崎ブレイブサンダース）、<PlayerLink name="佐藤 巧" />
          （山形ワイヴァンズ→千葉ジェッツ）のように、B.ONEのクラブからB.PREMIERのクラブへ移った選手もいます。
        </p>
        <p>
          受け入れが多かったのは、
          <OrgLink name="アースフレンズ東京Z" />
          、<OrgLink name="さいたまブロンコス" />
          、<OrgLink name="金沢サムライズ" />
          （各8人）など、B.ONEのクラブでした。
        </p>
        <p style={{ fontSize: 12, color: '#5B6B7A' }}>
          ※クラブの区分は2026-27の区分（B.PREMIER／B.ONE）を、過去のシーズンにも当てはめています。過去のシーズンの「B.PREMIERのクラブ」は、当時のB1と同じではありません。また、シーズン途中の移籍や特別指定選手の加入は、これから増える可能性があります。
        </p>
      </section>

      <section>
        <h2>選手の立場から見ると</h2>
        <p>
          この動きだけで、原因がサラリーキャップだと言い切ることはできません。それでも、制度の向きとデータの向きは一致しています。報酬の総額に上限ができたことで、B.PREMIERのクラブは選手の入れ替えを絞り、その分の選手をB.ONEのクラブが受け止めている、という見方ができます。
        </p>
        <p>選手の立場から見ると、次の3つの変化があります。</p>
        <ul>
          <li>
            <strong>B.PREMIERの「席」が限られた：</strong>
            クラブが使える人件費の枠が決まったため、実績のある選手でも、B.PREMIERのクラブと条件が折り合わずに移籍するケースが生まれやすくなっています。
          </li>
          <li>
            <strong>上に行く道は移籍だけ：</strong>
            新しいB.LEAGUEでは、クラブの区分は競技の成績ではなく、売上や入場者数、アリーナなどの経営の基準で決まります。B.ONEのクラブで活躍しても、チームごと昇格することはありません。選手がB.PREMIERでプレーするには移籍が必要ですが、その移籍は今季、減っています。
          </li>
          <li>
            <strong>決まり方への不満：</strong>
            2026年には日本バスケットボール選手会が発足し、初代会長には
            <PlayerLink name="ベンドラメ 礼生" />
            が就きました。選手会は、サラリーキャップなどの制度が選手の意見を聞かずに決まったことを問題として挙げていると報じられています。
          </li>
        </ul>
        <p>
          一方で、リーグは「選手の報酬を抑えるための制度ではない」と説明し、上限の引き上げの可能性にも触れています。戦力が均衡すれば、どのクラブにいても優勝を狙えるという、選手にとっての利点もあります。制度は始まったばかりで、評価にはもう少し時間が必要です。
        </p>
      </section>

      <section>
        <h2>まとめ</h2>
        <ul>
          <li>B.PREMIERに上限8億円・下限5億円のサラリーキャップが導入された</li>
          <li>登録データでは、B.PREMIERのクラブへの移籍が約2割減り、B.ONEのクラブへの移籍が約2割増えた</li>
          <li>B.ONEからB.PREMIERへ上がる移籍は15人で、比べた中で最も少ない</li>
          <li>選手会は、制度づくりに選手の声を入れることを求めている</li>
        </ul>
        <p>Rosterlineでは、シーズン途中の移籍も記録していきます。シーズンが終わった時点で、もう一度この数字を見直す予定です。</p>
      </section>

      <References
        items={[
          {
            label: '2026年スタートの新リーグでサラリーキャップを導入、Bリーグチェアマン島田慎二の思い（前編）',
            publisher: 'B.LEAGUE公式サイト／BASKET COUNT',
            date: '2025年8月',
            href: 'https://www.bleague.jp/media_news/detail/id=535520',
          },
          {
            label: 'サラリーキャップの本当の目的（島田慎二）',
            publisher: 'note',
            date: '2026年6月',
            href: 'https://note.com/1105shimada/n/n16440d6fba9b',
          },
          {
            label: 'Bリーグが導入したサラリーキャップ制の是非',
            publisher: 'スポーツナビ',
            date: '2026年9月',
            href: 'https://sports.yahoo.co.jp/column/detail/2026091900001-spnavi',
          },
          {
            label: 'A千葉が報酬総額“8億円超え”も島田コミッショナー「いまペナルティの対象になるものではない」',
            publisher: 'バスケットボールキング',
            date: '2026年11月',
            href: 'https://basketballking.jp/news/japan/20261111/642432.html',
          },
        ]}
      />
    </ColumnLayout>
  );
}
