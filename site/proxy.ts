import { NextResponse, type NextRequest } from 'next/server';
import { siteUrl } from './app/site-url';

// 旧ドメイン（japanbasketballarchive.com）へのアクセスをrosterline.jpへ301転送する。
// CloudflareのRedirect Ruleでも転送しているが、Googlebotには転送されず200が返るケースが
// 確認されたため（2026-10-08、Search ConsoleのURL検査）、アプリ側でも同じ転送を行う。
const LEGACY_HOSTS = new Set(['japanbasketballarchive.com', 'www.japanbasketballarchive.com']);

// vinextが出力する内部キー（例：/players/p000419:13vaz3c、/organizations/org000010:1r0gtlh:0）を
// GooglebotがURLとして拾い、404として大量に記録していた（2026-11-02、Search Consoleの404が250件）。
// 「:」以降を取り除いた本来のページへ301転送する。
const INTERNAL_KEY_PATH = /^\/(players|organizations)\/([a-z0-9-]+):[a-z0-9]+(?::\d+)?\/?$/i;

export function proxy(request: NextRequest) {
  const url = new URL(request.url);
  const host = (request.headers.get('host') ?? url.host).toLowerCase().split(':')[0];
  if (LEGACY_HOSTS.has(host)) {
    return NextResponse.redirect(`${siteUrl}${url.pathname}${url.search}`, 301);
  }

  let pathname = url.pathname;
  try {
    pathname = decodeURIComponent(pathname);
  } catch {
    // 不正なエンコードはそのまま扱う
  }
  const internalKey = INTERNAL_KEY_PATH.exec(pathname);
  if (internalKey) {
    return NextResponse.redirect(`${siteUrl}/${internalKey[1]}/${internalKey[2].toLowerCase()}`, 301);
  }

  return NextResponse.next();
}
