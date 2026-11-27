// 記事末尾の「参考資料」（外部の出典）。リーグの公式資料と報道を、発行元・日付つきで並べる。
export function References({ items }: { items: readonly { label: string; publisher: string; date: string; href: string }[] }) {
  return (
    <section>
      <h2>参考資料</h2>
      <ul style={{ fontSize: 13 }}>
        {items.map((item) => (
          <li key={item.href}>
            <a href={item.href} target="_blank" rel="noreferrer">
              {item.label}
            </a>
            （{item.publisher}、{item.date}）
          </li>
        ))}
      </ul>
    </section>
  );
}
