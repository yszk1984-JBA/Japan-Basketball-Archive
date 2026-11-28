// Affiliate Engine の表示判定テスト。実行：cd site && node --test scripts/affiliate.test.mjs
// （Node 22.18以降はTypeScriptの型を取り除いて .ts を直接読み込める）
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { test } from 'node:test';
import { a8Destination, checkRawHtml, isAllowedUrl, latestUntil, selectPage, selectSlot, todayJst } from '../app/affiliate/select.ts';

const readJson = (name) => JSON.parse(readFileSync(new URL(`../app/affiliate/${name}`, import.meta.url), 'utf8'));
const real = { programs: readJson('programs.json'), links: readJson('links.json'), placements: readJson('placements.json') };

const TODAY = '2026-12-01';
const A8_HTML =
  '<a href="https://px.a8.net/svt/ejp?a8mat=TEST" rel="nofollow"><img border="0" width="300" height="250" alt="" src="https://www28.a8.net/svt/bgt?aid=TEST"></a><img border="0" width="1" height="1" src="https://www13.a8.net/0.gif?a8mat=TEST" alt="">';

const program = (overrides = {}) => ({
  id: 'AFF900001',
  name: 'テスト案件',
  asp: 'a8',
  partnershipStatus: 'approved',
  enabled: true,
  validFrom: null,
  validUntil: null,
  categories: ['ball'],
  ...overrides,
});
const fieldsLink = (overrides = {}) => ({
  id: 'LNK900001',
  programId: 'AFF900001',
  kind: 'text',
  mode: 'fields',
  href: 'https://px.a8.net/svt/ejp?a8mat=TEST',
  impressionPixel: 'https://www13.a8.net/0.gif?a8mat=TEST',
  label: 'ボールを探す',
  categories: ['ball'],
  enabled: true,
  validUntil: null,
  ...overrides,
});
const placement = (overrides = {}) => ({
  id: 'PLC900',
  slot: 'guide-shopping',
  pageTypes: ['guide'],
  pageKeys: ['basketball-ball-size'],
  categories: ['ball'],
  maxItems: 2,
  enabled: true,
  ...overrides,
});
const query = { slot: 'guide-shopping', pageType: 'guide', pageKey: 'basketball-ball-size', today: TODAY };
const data = (p = [program()], l = [fieldsLink()], pl = [placement()]) => ({ programs: p, links: l, placements: pl });

test('実データ：初期状態は全案件が無効で、どのパイロットページにも広告が出ない', () => {
  assert.ok(real.programs.length >= 4);
  for (const item of real.programs) assert.equal(item.enabled, false, `${item.id} は無効のはず`);
  for (const [pageType, pageKey] of [
    ['column', 'high-school-trends'],
    ['ranking', 'high-school'],
    ['guide', 'basketball-ball-size'],
  ]) {
    assert.deepEqual(selectPage(real, pageType, pageKey, TODAY), []);
  }
});

test('承認済み・有効・期限内・正式素材ありなら表示される', () => {
  const slot = selectSlot(data(), query);
  assert.ok(slot);
  assert.equal(slot.items.length, 1);
  assert.equal(slot.until, null);
});

test('未提携・否認・終了の案件は表示しない', () => {
  for (const status of ['pending', 'rejected', 'ended']) {
    assert.equal(selectSlot(data([program({ partnershipStatus: status })]), query), null, status);
  }
});

test('無効（enabled: false）の案件・素材・ルールは表示しない', () => {
  assert.equal(selectSlot(data([program({ enabled: false })]), query), null);
  assert.equal(selectSlot(data(undefined, [fieldsLink({ enabled: false })]), query), null);
  assert.equal(selectSlot(data(undefined, undefined, [placement({ enabled: false })]), query), null);
});

test('期限：最終日までは表示し、翌日から表示しない。開始日前も表示しない', () => {
  assert.ok(selectSlot(data([program({ validUntil: TODAY })]), query));
  assert.equal(selectSlot(data([program({ validUntil: '2026-11-30' })]), query), null);
  assert.equal(selectSlot(data(undefined, [fieldsLink({ validUntil: '2026-11-30' })]), query), null);
  assert.equal(selectSlot(data([program({ validFrom: '2026-12-02' })]), query), null);
  const slot = selectSlot(data([program({ validUntil: '2026-12-31' })], [fieldsLink({ validUntil: '2026-12-15' })]), query);
  assert.equal(slot.until, '2026-12-15');
});

test('正式素材が未登録・不正なら表示しない（推測でリンクを作らない）', () => {
  assert.equal(selectSlot(data(undefined, []), query), null);
  assert.equal(selectSlot(data(undefined, [fieldsLink({ href: '' })]), query), null);
  assert.equal(selectSlot(data(undefined, [fieldsLink({ href: 'http://px.a8.net/x' })]), query), null, 'httpは不可');
  assert.equal(selectSlot(data(undefined, [fieldsLink({ href: 'https://example.com/x' })]), query), null, '許可外ドメイン');
  assert.equal(selectSlot(data(undefined, [fieldsLink({ href: 'https://a8.net.evil.example/x' })]), query), null);
  assert.equal(selectSlot(data(undefined, [fieldsLink({ label: '' })]), query), null);
});

test('ページ・枠・カテゴリーが一致しなければ表示しない', () => {
  assert.equal(selectSlot(data(), { ...query, pageKey: 'other' }), null);
  assert.equal(selectSlot(data(), { ...query, pageType: 'archive' }), null);
  assert.equal(selectSlot(data(), { ...query, slot: 'column-end' }), null);
  assert.equal(selectSlot(data(undefined, [fieldsLink({ categories: ['travel'] })]), query), null);
});

test('maxItemsを超えない・同じ素材を重複表示しない', () => {
  const links = [fieldsLink(), fieldsLink(), fieldsLink({ id: 'LNK900002' }), fieldsLink({ id: 'LNK900003' })];
  const slot = selectSlot(data(undefined, links), query);
  assert.deepEqual(
    slot.items.map((item) => item.link.id),
    ['LNK900001', 'LNK900002'],
  );
});

test('rawHtml：A8.netの標準的な形の素材は通す（改変しない）', () => {
  assert.deepEqual(checkRawHtml(A8_HTML, 'a8'), { ok: true });
  const slot = selectSlot(data(undefined, [fieldsLink({ mode: 'rawHtml', kind: 'banner', rawHtml: A8_HTML, href: undefined })]), query);
  assert.equal(slot.items[0].link.rawHtml, A8_HTML);
});

test('rawHtml：楽天の標準的な形の素材は通す', () => {
  const html =
    '<a href="https://hb.afl.rakuten.co.jp/hgc/TEST/?pc=https%3A%2F%2Fwww.rakuten.co.jp%2F" target="_blank" rel="nofollow sponsored noopener" style="word-wrap:break-word;"><img src="https://hbb.afl.rakuten.co.jp/hgb/TEST/" border="0" style="margin:2px" alt="" title=""></a>';
  assert.deepEqual(checkRawHtml(html, 'rakuten'), { ok: true });
  assert.equal(checkRawHtml(html, 'a8').ok, false, 'ASPが違うドメインは不可');
});

test('rawHtml：script・iframe・イベント属性・javascript:・許可外ドメイン・style内のurl()は拒否', () => {
  const bad = [
    '<script src="https://px.a8.net/x.js"></script><a href="https://px.a8.net/x">x</a>',
    '<iframe src="https://px.a8.net/x"></iframe>',
    '<a href="https://px.a8.net/x" onclick="alert(1)">x</a>',
    '<a href="javascript:alert(1)">x</a>',
    '<a href="https://example.com/x">x</a>',
    '<a href="https://px.a8.net/x" style="background:url(https://example.com/t.gif)">x</a>',
    '<a href="https://px.a8.net/x"><svg onload="alert(1)"></svg></a>',
    '<img src="https://www13.a8.net/0.gif">',
    '<a href="https://px.a8.net/x">x</a><',
    '<style>a{}</style><a href="https://px.a8.net/x">x</a>',
    '<a href="https://px.a8.net/x" srcdoc="x">x</a>',
  ];
  for (const html of bad) assert.equal(checkRawHtml(html, 'a8').ok, false, html);
});

test('補助関数', () => {
  assert.equal(isAllowedUrl('https://www13.a8.net/0.gif', 'a8'), true);
  assert.equal(isAllowedUrl('https://a8.net', 'a8'), true);
  assert.equal(isAllowedUrl('https://xa8.net', 'a8'), false);
  assert.equal(latestUntil(['2026-12-01', '2026-12-31']), '2026-12-31');
  assert.equal(latestUntil(['2026-12-01', null]), null);
  assert.equal(todayJst(new Date('2026-11-30T15:30:00Z')), '2026-12-01', 'UTC 15:30は日本時間の翌日');
});

test('広告主が指定した飛び先（allowedDestinations）の範囲外は表示しない', () => {
  const allowed = { allowedDestinations: ['https://www.supersports.com/ja-jp/xebio/'] };
  const inside =
    'https://px.a8.net/svt/ejp?a8mat=TEST&a8ejpredirect=https%3A%2F%2Fwww.supersports.com%2Fja-jp%2Fxebio%2Fbasketball%2F';
  const outside = 'https://px.a8.net/svt/ejp?a8mat=TEST&a8ejpredirect=https%3A%2F%2Fexample.com%2F';
  assert.equal(a8Destination(inside), 'https://www.supersports.com/ja-jp/xebio/basketball/');
  assert.ok(selectSlot(data([program(allowed)], [fieldsLink({ href: inside })]), query));
  assert.equal(selectSlot(data([program(allowed)], [fieldsLink({ href: outside })]), query), null);
  const raw = `<a href="${outside.replace(/&/g, '&amp;')}">x</a>`;
  assert.equal(selectSlot(data([program(allowed)], [fieldsLink({ mode: 'rawHtml', rawHtml: raw })]), query), null);
  assert.ok(selectSlot(data([program(allowed)], [fieldsLink()]), query), '飛び先の指定が無い標準リンクは表示');
});
