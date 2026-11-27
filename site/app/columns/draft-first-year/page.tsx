/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import { ColumnLayout, columnMetadata } from '../ColumnLayout';
import { OrgLink } from '../OrgLink';
import { PlayerLink } from '../PlayerLink';
import { References } from '../References';

const SLUG = 'draft-first-year';
export const metadata = columnMetadata(SLUG);

// 2026-11-26時点の確認済みデータ（各選手の「B.LEAGUEドラフト」の記録）。
const PICKS = [
  { pick: '1巡目・全体1位', name: '山﨑 一渉', club: 'サンロッカーズ渋谷' },
  { pick: '1巡目・全体2位', name: '赤間 賢人', club: '茨城ロボッツ' },
  { pick: '1巡目・全体3位', name: '新井 楽人', club: '横浜ビー・コルセアーズ' },
  { pick: '1巡目・全体4位', name: '岩下 准平', club: '長崎ヴェルカ' },
  { pick: '1巡目・全体5位', name: '岩屋 頼', club: '秋田ノーザンハピネッツ' },
  { pick: '1巡目・全体6位', name: '松野 遥弥', club: '広島ドラゴンフライズ' },
  { pick: '2巡目・全体7位', name: '西部 秀馬', club: '京都ハンナリーズ' },
  { pick: '2巡目・全体8位', name: '田中 流嘉州', club: '滋賀レイクス' },
  { pick: '3巡目・全体9位', name: '堀田 尚秀', club: '秋田ノーザンハピネッツ' },
  { pick: '3巡目・全体10位', name: '泉 登翔', club: '富山グラウジーズ' },
  { pick: '3巡目・全体11位', name: '武富 楓太', club: '佐賀バルーナーズ' },
];

export default function Page() {
  return (
    <ColumnLayout
      slug={SLUG}
      related={[
        { label: '高校から大学を経ずにB.LEAGUE入りした選手', href: '/rankings/high-school-to-pro' },
        { label: 'コラム：高校から大学を経ずにプロへ', href: '/columns/high-school-to-pro' },
        { label: 'コラム：サラリーキャップ元年、選手はどう動いたか', href: '/columns/salary-cap-first-year-moves' },
      ]}
    >
      <section>
        <p>
          2026年1月29日、B.LEAGUEで初めてのドラフトが行われました。対象は、B.PREMIERのクラブに入る日本人の新人選手です。これまでは、選手が自分で行き先を選び、クラブと交渉して契約していました。ドラフトでは、指名したクラブが交渉の権利を持ちます。
        </p>
        <p>選手にとって、キャリアの入口はどう変わったのでしょうか。制度と登録データから整理します。</p>
      </section>

      <section>
        <h2>第1回ドラフトの結果：指名は11人</h2>
        <p>
          参加した23クラブのうち、実際に指名したのは一部のクラブにとどまり、指名は<strong>11人</strong>でした。
          <OrgLink name="宇都宮ブレックス" />
          、<OrgLink name="シーホース三河" />
          、<OrgLink name="名古屋ダイヤモンドドルフィンズ" />
          はドラフト自体に参加していません。
        </p>
        <table className="jbaListB-articleTable">
          <thead>
            <tr>
              <th>指名順</th>
              <th>選手</th>
              <th>指名したクラブ</th>
            </tr>
          </thead>
          <tbody>
            {PICKS.map((row) => (
              <tr key={row.name}>
                <td>{row.pick}</td>
                <td>
                  <PlayerLink name={row.name} />
                </td>
                <td>
                  <OrgLink name={row.club === 'サンロッカーズ渋谷' ? '東京サンロッカーズ' : row.club} label={row.club} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <p>
          このほか、自クラブのU18チームの選手とドラフトを経ずに契約できる「ユース優先交渉権」で、
          <PlayerLink name="阿部 真冴橙" />
          （仙台89ERS）、<PlayerLink name="西村 優真" />
          （レバンガ北海道）、<PlayerLink name="若野 瑛太" />
          （名古屋ダイヤモンドドルフィンズ）の3人がトップチームと契約しています。
        </p>
        <p>
          指名が少なかった理由について、島田慎二コミッショナーは、サラリーキャップのもとで若手に投資しにくいことや、新人の報酬が固定されていることを挙げています。
        </p>
      </section>

      <section>
        <h2>選手の立場から：選べない入口</h2>
        <ul>
          <li>
            <strong>行き先を選べない：</strong>
            指名されると、交渉できるのは指名したクラブだけです。2025年3月にリーグが発表した制度案では、指名を断るとそのシーズンはB.PREMIERのクラブと契約できない、とされていました。
          </li>
          <li>
            <strong>ドラフトを避ける動き：</strong>報道によると、対象となる選手のうち十数人が、ドラフトの前にプロ契約を結んで対象から外れました。
            <PlayerLink name="佐藤 涼成" />
            、<PlayerLink name="小澤 飛悠" />
            、<PlayerLink name="渡邉 伶音" />
            のように、大学を早めに離れてプロ入りした選手もいます。制度が、選手の進路の選び方そのものに影響しています。
          </li>
          <li>
            <strong>指名直後の期限付移籍：</strong>
            <PlayerLink name="岩下 准平" />
            は長崎ヴェルカに、<PlayerLink name="田中 流嘉州" />
            は滋賀レイクスに指名されましたが、2026-27シーズンは、育成契約選手制度によってお互いのクラブへ期限付移籍しています。指名されたクラブで、すぐにプレーできるとは限りません。
          </li>
        </ul>
      </section>

      <section>
        <h2>報酬：B.PREMIERとB.ONEで大きな差</h2>
        <p>
          ドラフトで入る新人の報酬は、指名の順位などで決まった固定の額です。報道によると、日本の大学からの3巡目以降の指名で、2年契約・1,000万円とされています。代理人からは、指名順に関係なく固定されている額は高すぎる、という意見も出ており、リーグは3巡目以降の報酬の見直しを検討しています。
        </p>
        <p>
          一方、2025年3月の制度案では、B.ONEやB.NEXTのクラブに入る新人の報酬は、上限460万円（出来高を除く）とされていました。同じ年に大学を卒業した選手でも、入るクラブの区分によって、報酬に2倍以上の差が生まれる可能性があります。
        </p>
      </section>

      <section>
        <h2>新しく生まれた保護</h2>
        <p>
          ドラフトは選手の選択肢を狭める一方で、新しい保護も用意しています。リーグのドラフト規程では、ドラフトに参加するクラブに、指名した選手の<strong>引退後3年間の雇用の保障</strong>
          などを求めています。また、契約期間は最長3年で、3年目に選手が契約を続けるかどうかを選べるオプション（プレーヤーオプション）を付けることもできます。
        </p>
        <p>キャリアの短いプロ選手にとって、引退後の生活を支える仕組みが制度として決まったことは、これまでにない変化です。</p>
      </section>

      <section>
        <h2>まとめ</h2>
        <ul>
          <li>第1回ドラフトの指名は11人。ユース優先交渉権での契約が3人</li>
          <li>指名されたら行き先を選べず、ドラフトを避けて早めにプロ入りする選手も出た</li>
          <li>指名直後に育成契約で別のクラブへ移る例もある</li>
          <li>B.PREMIERとB.ONEで新人の報酬に大きな差がある</li>
          <li>引退後3年間の雇用保障という、新しい保護も生まれた</li>
        </ul>
        <p>第2回のドラフトは2027年1月28日に予定されています。制度の見直しとあわせて、指名された選手たちのその後も、Rosterlineで記録していきます。</p>
      </section>

      <References
        items={[
          {
            label: '特定新人選手選択会議（ドラフト）規程',
            publisher: 'B.LEAGUE',
            date: '2025年8月制定',
            href: 'https://www.bleague.jp/files/user/about/pdf/r-50.pdf',
          },
          {
            label: 'B.LEAGUE ドラフト 概要発表会見 資料',
            publisher: 'B.LEAGUE',
            date: '2025年3月',
            href: 'https://bleague.jp/files/user/B.LEAGUE_DRAFT.pdf',
          },
          {
            label: '見えたバスケ界の“就職活動”が持つ厳しさ「?」が多かったBリーグ初ドラフトの内幕',
            publisher: 'スポーツナビ',
            date: '2026年1月',
            href: 'https://sports.yahoo.co.jp/column/detail/2026013000007-spnavi?p=1',
          },
          {
            label: 'バスケBプレミア新人報酬改定も ドラフトでの指名人数増狙い',
            publisher: '熊本日日新聞（共同通信）',
            date: '2026年8月',
            href: 'https://kumanichi.com/articles/2026468',
          },
          {
            label: '「NBA丸パクリではダメ」日本バスケ界最大手エージェントが語る新Bリーグ成功の鍵',
            publisher: '現代ビジネス',
            date: '2025年11月',
            href: 'https://gendai.media/articles/-/160142',
          },
        ]}
      />
    </ColumnLayout>
  );
}
