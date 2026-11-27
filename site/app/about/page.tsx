/* oxlint-disable next/no-html-link-for-pages -- Hosted Vinext navigation requires full-page links for reliable route changes. */
import type { Metadata } from 'next';
import { players } from '../public-data';
import {
  baseOpenGraph,
  breadcrumbJsonLd,
  DISCLAIMER_EN,
  DISCLAIMER_JA,
  JsonLd,
  SiteBreadcrumb,
  SiteFooter,
  SiteHeader,
  siteUrl,
} from '../seo';
import { correctionFormUrl, xHandle } from '../site-url';

const title = 'このサイトについて';
const description =
  'Rosterlineは、日本バスケットボール選手の所属と経歴を出典とともに記録する、個人運営の非公式アーカイブです。掲載データの考え方、データを確認して公開するまでの手順、編集方針、運営者、訂正・削除のご依頼の方法を説明します。';

export const metadata: Metadata = {
  title,
  description,
  alternates: { canonical: '/about' },
  openGraph: { ...baseOpenGraph, title, description, url: '/about' },
};

export default function AboutPage() {
  const masterCount = players.filter((player) => player.dataStatus === 'master').length;

  return (
    <main className="jbaListB-page">
      <JsonLd
        data={{
          '@context': 'https://schema.org',
          '@graph': [
            {
              '@type': 'AboutPage',
              name: title,
              url: `${siteUrl}/about`,
              isPartOf: { '@type': 'WebSite', name: 'Rosterline', url: siteUrl },
            },
            breadcrumbJsonLd([
              { name: 'ホーム', path: '/' },
              { name: title, path: '/about' },
            ]),
          ],
        }}
      />
      <SiteHeader />

      <SiteBreadcrumb crumbs={[{ label: title }]} />

      <div className="jbaListB-main">
        <div>
          <p className="jbaListB-eyebrow">About</p>
          <h1 className="jbaListB-h1">{title}</h1>
        </div>

        <section className="jbaListB-section jbaListB-about">
          <div className="jbaListB-sectionHead">
            <h2>Rosterlineとは</h2>
          </div>
          <p>
            Rosterline（ロスターライン）は、日本のバスケットボール選手が、どの学校・大学・クラブに所属してきたかを、出典とともに記録するアーカイブです。選手ごとの経歴をたどったり、学校やクラブからその出身選手を探したりできます。
          </p>
        </section>

        <section className="jbaListB-section jbaListB-about">
          <div className="jbaListB-sectionHead">
            <h2>掲載データの考え方</h2>
          </div>
          <ul>
            <li>所属や経歴には、裏付けとなる出典（公式サイト・大会資料・専門媒体など）を記載しています。出典のない情報は推測で埋めません。</li>
            <li>
              確認を終えたデータ（現在{masterCount}人分）と、確認中のデータを分けて掲載しています。確認中のデータには、その旨を表示しています。
            </li>
            <li>掲載しているのは本サイトに登録済みの選手だけです。人数やランキングは、すべての選手を網羅したものではありません。</li>
            <li>選手の写真は掲載していません。</li>
          </ul>
        </section>

        <section className="jbaListB-section jbaListB-about">
          <div className="jbaListB-sectionHead">
            <h2>データができるまで</h2>
          </div>
          <p>掲載するデータは、次の手順で確認してから公開しています。</p>
          <ol>
            <li>
              <strong>収集：</strong>B.LEAGUE公式サイトの選手情報・所属履歴、クラブ公式サイト、大会の公式資料、専門媒体の記事などから、所属と経歴の記録を集めます。
            </li>
            <li>
              <strong>照合：</strong>同じ選手の記録を複数の資料で突き合わせ、名前の表記ゆれ、学校の改称・統合、クラブの改称などを整理します。
            </li>
            <li>
              <strong>確認：</strong>出典と内容が一致しているかを1件ずつ確認します。確認が終わるまでは「確認中」として掲載し、ランキングなどの集計には使いません。
            </li>
            <li>
              <strong>承認・公開：</strong>確認を終えたデータを運営者が承認し、確認済みのデータとして公開します。承認の記録は<a href="/updates">更新履歴</a>で確認できます。
            </li>
          </ol>
          <p>
            現在の所属は、B.LEAGUEのクラブに所属する選手を中心に、シーズン中も定期的に照合して更新しています。出典で確認できない情報は、推測で補いません。
          </p>
        </section>

        <section className="jbaListB-section jbaListB-about">
          <div className="jbaListB-sectionHead">
            <h2>編集方針</h2>
          </div>
          <ul>
            <li>選手の評価や優劣は書きません。所属・在籍の事実と、その集計だけを掲載します。</li>
            <li>ランキングや「注目ポイント」の文章は、確認済みのデータから集計した結果だけで書いています。「名門」「最強」のような評価の言葉は使いません。</li>
            <li>出典の言い回しをそのまま転載せず、所属先と期間などの事実だけを記録します。</li>
            <li>選手のプライバシーに配慮し、公開されている競技上の経歴以外（家族、住所など）は掲載しません。</li>
          </ul>
        </section>

        <section className="jbaListB-section jbaListB-about">
          <div className="jbaListB-sectionHead">
            <h2>運営と収益化の方針</h2>
          </div>
          <ul>
            <li>Rosterlineは個人が運営しています。サイトの運営費をまかなうため、一部のページに広告（アフィリエイト広告を含む）を掲載しています。</li>
            <li>
              広告は、選手の経歴などの掲載データとは分けて表示し、「PR」「広告」と明示します。選手・学校・クラブのページには広告を掲載していません。
            </li>
            <li>
              広告主は、掲載データの内容、ランキング、選手・学校の表示順、記事の内容に関与しません。選手・学校・クラブが特定の商品やサービスを推奨しているものではありません。
            </li>
            <li>
              <a href="/guide">ガイド</a>
              （用品・観戦の実用記事）は、競技規則やメーカーの公開情報など確かめられる情報をもとに書いています。実際に使っていない商品の使用感やレビューは書きません。
            </li>
            <li>
              詳しくは<a href="/privacy">プライバシーポリシー</a>をご覧ください。
            </li>
          </ul>
        </section>

        <section className="jbaListB-section jbaListB-about">
          <div className="jbaListB-sectionHead">
            <h2>運営者</h2>
          </div>
          <p>
            Rosterlineは、日本のバスケットボールを応援する個人が運営しています。選手の歩んできた道のりを、学校やクラブをまたいでたどれる場所をつくることを目的に、2026年から公開しています。
          </p>
          <p>
            お問い合わせは<a href="/contact">お問い合わせ</a>のページをご覧ください。更新のお知らせはX（
            <a href={`https://x.com/${xHandle}`} target="_blank" rel="noreferrer">
              @{xHandle}
            </a>
            ）でも発信しています。
          </p>
        </section>

        <section className="jbaListB-section jbaListB-about" id="corrections">
          <div className="jbaListB-sectionHead">
            <h2>訂正・削除のご依頼</h2>
          </div>
          <p>
            掲載内容の誤りのご指摘や、掲載の削除のご依頼は、下記のフォームから受け付けています。選手ご本人・ご家族・所属先の方に限らず、どなたからでもお送りいただけます。
          </p>
          <p>
            <a href={correctionFormUrl} target="_blank" rel="noreferrer" className="jbaListB-aboutButton">
              訂正・削除依頼フォームを開く
            </a>
          </p>
          <ul>
            <li>対象のページのURL（または選手名・学校名・クラブ名）と、どの項目をどう直すべきかをお書きください。</li>
            <li>訂正のご指摘には、根拠となる資料（公式サイト・大会資料など）のURLを添えていただけると、確認が早く進みます。</li>
            <li>選手ご本人またはご家族からの削除のご依頼には、原則として対応します。</li>
            <li>内容を確認したうえで、順次反映します。返信をご希望の場合は、フォームに連絡先をご記入ください。</li>
          </ul>
        </section>

        <section className="jbaListB-section jbaListB-about">
          <div className="jbaListB-sectionHead">
            <h2>非公式のアーカイブです</h2>
          </div>
          <p>{DISCLAIMER_JA}</p>
          <p className="jbaListB-aboutEn" lang="en">
            {DISCLAIMER_EN}
          </p>
        </section>
      </div>

      <SiteFooter />
    </main>
  );
}
