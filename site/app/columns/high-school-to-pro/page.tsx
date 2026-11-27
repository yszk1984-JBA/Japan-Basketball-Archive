/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import { ColumnLayout, columnMetadata } from '../ColumnLayout';
import { OrgLink } from '../OrgLink';
import { PlayerLink } from '../PlayerLink';

const SLUG = 'high-school-to-pro';
export const metadata = columnMetadata(SLUG);

// 2026-11-26時点の確認済みデータ（/rankings/high-school-to-pro と同じ抽出条件）。開始年の新しい順。
const PLAYERS = [
  { name: '西村 優真', school: '北海道文教大学附属高等学校', club: 'レバンガ北海道', year: 2025, inSchool: true },
  { name: '内山 晴輝', school: '鳥取城北高等学校', club: 'トライフープ岡山', year: 2025, inSchool: false },
  { name: '瀬川 琉久', school: '東山高等学校', club: '千葉ジェッツ', year: 2024, inSchool: true },
  { name: '佐取 龍之介', school: '豊見城高等学校', club: '琉球ゴールデンキングス', year: 2024, inSchool: true },
  { name: '崎濱 秀斗', school: '福岡第一高等学校', club: '琉球ゴールデンキングス', year: 2024, inSchool: false },
  { name: '若野 瑛太', school: '至学館高等学校', club: '名古屋ダイヤモンドドルフィンズ', year: 2023, inSchool: true },
  { name: '阿部 真冴橙', school: '宮城県利府高等学校', club: '仙台89ERS', year: 2023, inSchool: true },
  { name: '大森 康瑛', school: '麻布高等学校', club: '東京サンロッカーズ', year: 2023, inSchool: true },
  { name: '今西 優斗', school: '至学館高等学校', club: '名古屋ダイヤモンドドルフィンズ', year: 2022, inSchool: true },
  { name: '内藤 耀悠', school: '北海道文教大学附属高等学校', club: 'レバンガ北海道', year: 2022, inSchool: true },
  { name: '平良 宗龍', school: '開志国際高等学校', club: '琉球ゴールデンキングス', year: 2022, inSchool: true },
  { name: '湧川 颯斗', school: '福岡大学附属大濠高等学校', club: '滋賀レイクス', year: 2022, inSchool: true },
  { name: '山田 安斗夢', school: '鹿児島市立鹿児島商業高等学校', club: '鹿児島レブナイズ', year: 2016, inSchool: false },
  { name: '小野寺 祥太', school: '岩手県立盛岡南高等学校', club: '岩手ビッグブルズ', year: 2013, inSchool: false },
];

export default function Page() {
  return (
    <ColumnLayout
      slug={SLUG}
      related={[
        { label: '高校から大学を経ずにB.LEAGUE入りした選手', href: '/rankings/high-school-to-pro' },
        { label: 'B.LEAGUE現役選手が多い学年（世代）ランキング', href: '/rankings/generation' },
        { label: '高校→大学の進学ルート', href: '/rankings/high-school-to-university' },
      ]}
    >
      <section>
        <p>
          日本のバスケットボール選手の多くは、高校から大学に進み、大学を経てB.LEAGUEのクラブに入ります。一方で最近は、大学に進まず、高校からそのままクラブに所属する選手の名前を目にすることが増えました。
        </p>
        <p>
          本当に増えているのでしょうか。Rosterlineに登録済みの選手から、高校から大学を経ずにB.LEAGUEのクラブに所属した選手を抜き出すと、<strong>14人</strong>でした。この14人の記録から、その変化を見ていきます。
        </p>
      </section>

      <section>
        <h2>14人の顔ぶれ</h2>
        <table className="jbaListB-articleTable">
          <thead>
            <tr>
              <th>選手</th>
              <th>出身高校</th>
              <th>最初の所属クラブ</th>
              <th style={{ textAlign: 'right' }}>開始年</th>
            </tr>
          </thead>
          <tbody>
            {PLAYERS.map((player) => (
              <tr key={player.name}>
                <td>
                  <PlayerLink name={player.name} />
                </td>
                <td>
                  <OrgLink name={player.school} label={player.school.replace('高等学校', '高')} />
                </td>
                <td>
                  <OrgLink name={player.club} />
                </td>
                <td className="num">
                  {player.year}年{player.inSchool ? '＊' : ''}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <p style={{ fontSize: 12, color: '#5B6B7A' }}>＊高校に在籍している期間に、クラブとの所属が始まっている選手。</p>
      </section>

      <section>
        <h2>変化1：14人のうち12人が2022年以降</h2>
        <p>
          所属が始まった年で並べると、変化ははっきりしています。2022年以前は2013年と2016年に1人ずつだけでしたが、<strong>2022年に4人、2023年に3人、2024年に3人、2025年に2人</strong>と、ここ数年に集中しています。
        </p>
        <p>
          生まれた年で見ても、2022年以降の12人は全員が2004〜2007年生まれです。高校から直接プロに進む道は、この数年で新しく広がってきた道だと言えます。
        </p>
      </section>

      <section>
        <h2>変化2：多くは「高校在学中」に始まっている</h2>
        <p>
          さらに目を引くのは、所属が始まったタイミングです。14人のうち<strong>10人は、高校に在籍している期間にクラブとの所属が始まっています</strong>
          。しかも、その10人は全員が2022年以降の選手です。
        </p>
        <p>
          以前の2人（
          <PlayerLink name="小野寺 祥太" />、<PlayerLink name="山田 安斗夢" />
          ）は、高校の卒業と同じ年にクラブに入っています。「卒業してからプロへ」だった道が、「在学中からプロのクラブへ」という形に変わってきている様子がうかがえます。
        </p>
        <p style={{ fontSize: 12, color: '#5B6B7A' }}>
          ※本サイトでは、クラブとの所属の形（プロ契約、育成のための登録など）は区別していません。詳しくは各選手のページの出典をご確認ください。
        </p>
      </section>

      <section>
        <h2>変化3：特定のクラブに集まっている</h2>
        <p>最初の所属クラブを見ると、いくつかのクラブに偏りがあります。</p>
        <ul>
          <li>
            <OrgLink name="琉球ゴールデンキングス" />
            ：3人（平良宗龍、佐取龍之介、崎濱秀斗）
          </li>
          <li>
            <OrgLink name="名古屋ダイヤモンドドルフィンズ" />
            ：2人（今西優斗、若野瑛太。2人とも至学館高校）
          </li>
          <li>
            <OrgLink name="レバンガ北海道" />
            ：2人（内藤耀悠、西村優真。2人とも北海道文教大学附属高校）
          </li>
        </ul>
        <p>
          同じ高校から同じクラブへ、という組み合わせが2つあるのも特徴です。高校とクラブの間に、継続的なつながりがあることを示しているのかもしれません。
        </p>
      </section>

      <section>
        <h2>その後：早くから移籍も経験</h2>
        <p>
          2022年以降にプロの道へ進んだ12人のうち、
          <PlayerLink name="今西 優斗" />
          （立川ダイスへ）、
          <PlayerLink name="平良 宗龍" />
          （岩手ビッグブルズへ）、
          <PlayerLink name="湧川 颯斗" />
          （三遠ネオフェニックスへ）、
          <PlayerLink name="大森 康瑛" />
          （山形ワイヴァンズへ）の4人は、すでに別のクラブに移っています。大学の4年間を過ごす年齢で、複数のクラブを経験している選手もいることになります。
        </p>
      </section>

      <section>
        <h2>それでも主流は大学経由</h2>
        <p>
          ただし、高校から直接プロに進む選手が多数派になったわけではありません。2024〜2025年に初めてB.LEAGUEのクラブに所属した登録選手95人のうち、<strong>79人（83%）には大学の在籍記録があります</strong>。大学を経てプロに進む道は、今も中心的な道のままです。
        </p>
        <p style={{ fontSize: 12, color: '#5B6B7A' }}>
          ※大学の在籍記録がない選手には、海外出身の選手や、大学の記録がまだ本サイトに登録されていない選手も含まれます。
        </p>
      </section>

      <section>
        <h2>まとめ</h2>
        <ul>
          <li>高校から大学を経ずにB.LEAGUEのクラブに所属した登録選手14人のうち、12人は2022年以降</li>
          <li>そのうち10人は、高校に在籍している期間にクラブとの所属が始まっている</li>
          <li>琉球、名古屋D、北海道の3クラブに7人が集まり、同じ高校から同じクラブへの組み合わせもある</li>
          <li>それでも、新しくクラブに入る選手の8割以上は大学を経ている</li>
        </ul>
        <p>
          14人それぞれの経歴は、<a href="/rankings/high-school-to-pro">高校から大学を経ずにB.LEAGUE入りした選手</a>
          の一覧から各選手のページでたどれます。
        </p>
      </section>
    </ColumnLayout>
  );
}
