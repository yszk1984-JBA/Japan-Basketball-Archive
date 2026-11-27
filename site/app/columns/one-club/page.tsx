/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import { ColumnLayout, columnMetadata } from '../ColumnLayout';
import { OrgLink } from '../OrgLink';
import { PlayerLink } from '../PlayerLink';

const SLUG = 'one-club';
export const metadata = columnMetadata(SLUG);

// 2026-11-26時点の確認済みデータ（/rankings/one-club と同じ抽出条件）。
const CLUBS = [
  { club: '宇都宮ブレックス', players: ['田臥勇太', '竹内 公輔', '遠藤 祐亮', '渡邉 裕規'] },
  { club: '千葉ジェッツ', players: ['富樫勇樹', '原 修太'] },
  { club: '川崎ブレイブサンダース', players: ['篠山 竜青', '長谷川 技'] },
  { club: '名古屋ダイヤモンドドルフィンズ', players: ['張本 天傑', '中東 泰斗'] },
  { club: 'アルバルク東京', players: ['ザック・バランスキー'] },
  { club: '秋田ノーザンハピネッツ', players: ['中山 拓哉'] },
  { club: '神戸ストークス', players: ['道原 紀晃'] },
  { club: '大阪エヴェッサ', players: ['合田 怜'] },
  { club: '東京サンロッカーズ', players: ['ベンドラメ 礼生'] },
  { club: '東京八王子ビートレインズ', players: ['大金 広弥'] },
  { club: '富山グラウジーズ', players: ['水戸健史'] },
];

function Players({ names }: { names: readonly string[] }) {
  return (
    <>
      {names.map((name, index) => (
        <span key={name}>
          {index > 0 ? '、' : ''}
          <PlayerLink name={name} />
        </span>
      ))}
    </>
  );
}

export default function Page() {
  return (
    <ColumnLayout
      slug={SLUG}
      related={[
        { label: 'B.LEAGUE開幕から同じクラブ一筋の選手', href: '/rankings/one-club' },
        { label: 'B.LEAGUE開幕以降に所属したクラブ数が多い選手', href: '/rankings/most-clubs' },
        { label: 'B.LEAGUE現役最年長選手ランキング', href: '/rankings/oldest-active' },
      ]}
    >
      <section>
        <p>
          B.LEAGUEでは、移籍は珍しいことではありません。Rosterlineの登録データでは、開幕以降に5つ以上のクラブに所属した選手が全体の約2割にのぼり、最も多い選手は11クラブを経験しています（「
          <a href="/rankings/most-clubs">所属したクラブ数が多い選手</a>」）。
        </p>
        <p>
          その一方で、2016-17シーズンの開幕から今季まで、<strong>11シーズン続けて同じクラブに所属している選手</strong>
          もいます。登録データの中では17人です。この17人の記録から、「一筋」の選手の姿を見ていきます。
        </p>
      </section>

      <section>
        <h2>開幕から現役を続ける選手の13%</h2>
        <p>
          開幕シーズン（2016-17）にB.LEAGUEのクラブに所属していて、今も現役を続けている登録選手は129人います。そのうち、ずっと同じクラブにいるのが17人、
          <strong>約13%</strong>です。残りの9割近くは、この11シーズンのどこかでクラブを移っています。
        </p>
      </section>

      <section>
        <h2>クラブ別：宇都宮ブレックスが4人</h2>
        <table className="jbaListB-articleTable">
          <thead>
            <tr>
              <th>クラブ</th>
              <th style={{ textAlign: 'right' }}>人数</th>
              <th>選手</th>
            </tr>
          </thead>
          <tbody>
            {CLUBS.map((row) => (
              <tr key={row.club}>
                <td>
                  <OrgLink name={row.club} />
                </td>
                <td className="num">{row.players.length}人</td>
                <td>
                  <Players names={row.players} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <p>
          17人は11のクラブに分かれています。最も多いのは
          <OrgLink name="宇都宮ブレックス" />
          の4人で、千葉ジェッツ、川崎ブレイブサンダース、名古屋ダイヤモンドドルフィンズが2人ずつで続きます。複数の「一筋」選手がいるのは、この4クラブだけです。
        </p>
      </section>

      <section>
        <h2>開幕より前から同じクラブにいる選手</h2>
        <p>17人の中には、B.LEAGUEが始まる前から、すでに同じクラブでプレーしていた選手もいます。</p>
        <ul>
          <li>
            <PlayerLink name="水戸健史" />
            （富山グラウジーズ）：2008年から在籍
          </li>
          <li>
            <PlayerLink name="篠山 竜青" />
            （川崎ブレイブサンダース）：2011年から在籍
          </li>
          <li>
            <PlayerLink name="遠藤 祐亮" />
            （宇都宮ブレックス）：2012年から在籍
          </li>
          <li>
            <PlayerLink name="富樫勇樹" />、<PlayerLink name="原 修太" />
            （千葉ジェッツ）：2015年から在籍
          </li>
        </ul>
        <p>
          記録の上では、<PlayerLink name="水戸健史" />
          は2008年から同じクラブに所属しており、17人の中で最も長く1つのクラブに在籍しています。
        </p>
      </section>

      <section>
        <h2>ほかのクラブから来て、根付いた選手</h2>
        <p>「一筋」といっても、全員がプロのキャリアを同じクラブで始めたわけではありません。別のクラブを経験したあと、開幕の前後に移ったクラブにそのまま根付いた選手もいます。</p>
        <ul>
          <li>
            <PlayerLink name="竹内 公輔" />
            ：シーホース三河、アルバルク東京、広島ドラゴンフライズを経て、2016年から宇都宮ブレックス
          </li>
          <li>
            <PlayerLink name="張本 天傑" />
            ：アルバルク東京を経て、2016年から名古屋ダイヤモンドドルフィンズ
          </li>
          <li>
            <PlayerLink name="富樫勇樹" />
            ：秋田ノーザンハピネッツを経て、2015年から千葉ジェッツ
          </li>
        </ul>
        <p>
          一方で、17人のうち9人は、そのクラブ以外の所属（海外を含む）が本サイトには記録されていません。
        </p>
      </section>

      <section>
        <h2>32歳から41歳のベテランたち</h2>
        <p>
          生年月日が登録されている16人は、1985年から1994年の生まれで、現在32〜41歳です。最年長は1985年1月生まれの
          <PlayerLink name="竹内 公輔" />
          （41歳）、最年少は1994年7月生まれの
          <PlayerLink name="中山 拓哉" />
          （32歳）です。開幕から11シーズンという条件のため当然ではありますが、いずれもリーグの歩みとともにキャリアを重ねてきた選手たちです。
        </p>
      </section>

      <section>
        <h2>まとめ</h2>
        <ul>
          <li>開幕から11シーズン、同じクラブに所属し続ける登録選手は17人。開幕から現役を続ける129人の約13%</li>
          <li>宇都宮ブレックスが4人で最も多く、複数の「一筋」選手がいるのは4クラブだけ</li>
          <li>開幕前から同じクラブにいる選手もいれば、ほかのクラブから移って根付いた選手もいる</li>
        </ul>
        <p>
          最新の一覧は「<a href="/rankings/one-club">B.LEAGUE開幕から同じクラブ一筋の選手</a>」で確認できます。
        </p>
      </section>
    </ColumnLayout>
  );
}
