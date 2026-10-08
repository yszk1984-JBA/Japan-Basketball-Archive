import { NextResponse, type NextRequest } from 'next/server';
import { siteUrl } from './app/site-url';

// 旧ドメイン（japanbasketballarchive.com）へのアクセスをrosterline.jpへ301転送する。
// CloudflareのRedirect Ruleでも転送しているが、Googlebotには転送されず200が返るケースが
// 確認されたため（2026-10-08、Search ConsoleのURL検査）、アプリ側でも同じ転送を行う。
const LEGACY_HOSTS = new Set(['japanbasketballarchive.com', 'www.japanbasketballarchive.com']);

export function proxy(request: NextRequest) {
  const host = (request.headers.get('host') ?? new URL(request.url).host).toLowerCase().split(':')[0];
  if (!LEGACY_HOSTS.has(host)) return NextResponse.next();

  const { pathname, search } = new URL(request.url);
  return NextResponse.redirect(`${siteUrl}${pathname}${search}`, 301);
}
