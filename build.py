"""앱별 정적 페이지 + 사이트맵 생성기.

board.html / app.html 은 브라우저에서 데이터를 불러온다. 사람에게는 충분하지만
크롤러는 그 안을 못 본다. 검색 유입이 웹을 만드는 이유이므로, 앱마다 내용이
HTML 에 박힌 페이지를 따로 굽는다.

    python web/build.py

앱이 늘거나 설명이 바뀌면 다시 돌린다. 결과는 web/a/{package}/index.html.
"""
import html
import io
import json
import re
import os
import sys
import urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://actparty.app'

# 캐시 버전은 index.html 한 군데서만 관리한다. 여기 숫자를 따로 적어 두면
# 사이트를 올릴 때마다 이 파일만 옛 버전으로 남는다 (v74 로 26개 남아 있었다).
CACHE_V = re.search(r'app\.css\?v=(\d+)',
                    io.open('index.html', encoding='utf-8').read()).group(1)
ACT_STORE = ('https://play.google.com/store/apps/details'
             '?id=kr.testerparty.tester_party')

SUPABASE_URL = 'https://eedqzvckdxfcuoyycivu.supabase.co'
SUPABASE_KEY = 'sb_publishable_hF3_Mw-TybTPGxXPBx4M3Q_sPKe06UU'

STATIC_PAGES = [
    ('/', '1.0'),
    ('/board.html', '0.9'),
    ('/guides/', '0.8'),
    ('/guides/what-google-checks.html', '0.8'),
    ('/guides/daily-opens-data.html', '0.8'),
    ('/guides/why-testers-drop.html', '0.7'),
    ('/guides/production-form.html', '0.8'),
    ('/guides/google-group.html', '0.8'),
]


def public_apps():
    """anon 키로 부른다 — 로그인 없이 읽히는 게 이 설계의 전제다."""
    req = urllib.request.Request(
        f'{SUPABASE_URL}/rest/v1/rpc/public_apps',
        data=b'{}',
        headers={
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
            'Content-Type': 'application/json',
        })
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())


def page(a):
    e = html.escape
    name = a.get('name') or ''
    pkg = a.get('package_name') or ''
    dev = a.get('developer_name') or 'Developer'
    desc = a.get('description') or ''
    cur = a.get('current_testers') or 0
    need = a.get('needed_testers') or 12
    icon = a.get('icon_url') or ''
    karma = a.get('owner_karma') or 0
    done = a.get('owner_completed') or 0
    # 비공개 테스트 중인 앱은 스토어 페이지가 공개적으로 404 다.
    # 출시 표시가 된 앱만 링크를 건다 — 깨진 링크는 안 거는 것만 못하다.
    store = (f'https://play.google.com/store/apps/details?id={pkg}'
             if pkg and a.get('released_at') else '')

    # 검색 결과에 뜨는 한 줄. 설명이 없으면 상태로 대신한다.
    meta_desc = (f'{name} by {dev} is looking for closed testers on ACT Party. '
                 f'{cur} of {need} testers so far. '
                 + (desc if desc else ''))[:300]

    ld = {
        '@context': 'https://schema.org',
        '@type': 'SoftwareApplication',
        'name': name,
        'operatingSystem': 'Android',
        'applicationCategory': 'MobileApplication',
        'author': {'@type': 'Person', 'name': dev},
    }
    if desc:
        ld['description'] = desc
    if icon:
        ld['image'] = icon
    if store:
        ld['url'] = store

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(name)} — looking for closed testers | ACT Party</title>
<meta name="description" content="{e(meta_desc)}">
<link rel="canonical" href="{SITE}/a/{e(pkg)}/">
<meta property="og:title" content="{e(name)} — looking for closed testers">
<meta property="og:description" content="{e(meta_desc)}">
{f'<meta property="og:image" content="{e(icon)}">' if icon else ''}
<link rel="stylesheet" href="/assets/app.css?v={CACHE_V}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>

<header class="top">
  <div class="wrap">
    <a class="brand" href="/"><span class="dot">ACT</span> ACT Party</a>
    <nav>
      <a href="/board.html">App board</a>
      <a href="/guides/">Guides</a>
      <a href="/console.html">My apps</a>
    </nav>
  </div>
</header>

<div class="wrap narrow" style="padding-top:28px">
  <div class="card app-card" style="margin-bottom:16px">
    {f'<img class="app-icon" src="{e(icon)}" alt="">' if icon
      else f'<div class="app-icon ph">{e(name[:1].upper())}</div>'}
    <div style="min-width:0;flex:1">
      <h1 class="app-name" style="font-size:22px">{e(name)}</h1>
      <p class="muted">{e(dev)}</p>
      {f'<p class="desc">{e(desc)}</p>' if desc else ''}
      <div class="bar"><i style="width:{min(100, round(cur / max(need, 1) * 100))}%"></i></div>
      <p class="count"><b>{cur}</b> / {need} testers</p>
    </div>
  </div>

  <div class="card" style="margin-bottom:16px">
    <p style="margin:0 0 6px"><span class="muted">Package</span> {e(pkg) or '—'}</p>
    <p style="margin:0 0 6px"><span class="muted">Developer karma</span> {karma}</p>
    <p style="margin:0"><span class="muted">Finished trades</span> {done}</p>
  </div>

  <div class="card">
    <h2 style="font-size:17px;margin:0 0 8px">Test this app, get testers back</h2>
    <p class="muted" style="font-size:14px">
      {e(dev)} is trading closed tests on ACT Party. You test theirs, they test
      yours.</p>
    <p class="muted" style="font-size:14px;margin-top:10px">
      Daily opens are recorded automatically from Android usage stats — no
      screenshots, no forms to fill. That part needs the ACT Party app on your
      phone; without it your testing stays invisible to the other side.</p>
    <p class="row" style="margin-top:14px">
      <a class="btn" href="{ACT_STORE}" rel="noopener">Get ACT Party — free</a>
      <a class="btn ghost" href="/app.html?p={e(pkg)}">Open on the board</a>
      {f'<a class="btn ghost" href="{store}" rel="nofollow noopener">View on Play</a>' if store else ''}
    </p>
  </div>

  <p style="margin-top:22px"><a href="/board.html">← All apps looking for testers</a></p>
</div>

<footer class="bot"><div class="wrap"><p>
  <a href="/">ACT Party</a> · <a href="/guides/">Guides</a> ·
  <a href="/privacy.html">Privacy</a></p></div></footer>
</body>
</html>
"""


def main():
    apps = public_apps()
    listed = [a for a in apps if a.get('package_name')]
    urls = [f'{SITE}{p}' for p, _ in STATIC_PAGES]
    # 언어별 가이드 (i18n_build.py 가 만든다). 없으면 영어만 올라간다.
    i18n = os.path.join(BASE, 'i18n_pages.json')
    if os.path.exists(i18n):
        urls += [f'{SITE}{p}' for p in json.load(open(i18n, encoding='utf-8'))]
    # 검색어 랜딩 페이지 (landing_build.py 가 만든다)
    landing = os.path.join(BASE, 'landing_pages.json')
    if os.path.exists(landing):
        urls += [f'{SITE}{p}' for p in json.load(open(landing, encoding='utf-8'))]

    for a in listed:
        pkg = a['package_name']
        d = os.path.join(BASE, 'a', pkg)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, 'index.html'), 'w', encoding='utf-8',
                  newline='') as f:
            f.write(page(a))
        urls.append(f'{SITE}/a/{pkg}/')

    body = '\n'.join(
        f'  <url><loc>{u}</loc></url>' for u in urls)
    with open(os.path.join(BASE, 'sitemap.xml'), 'w', encoding='utf-8',
              newline='') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                f'{body}\n</urlset>\n')

    with open(os.path.join(BASE, 'robots.txt'), 'w', encoding='utf-8',
              newline='') as f:
        f.write('User-agent: *\nAllow: /\n'
                'Disallow: /console.html\n'
                f'Sitemap: {SITE}/sitemap.xml\n')

    print(f'앱 페이지 {len(listed)}개, 사이트맵 {len(urls)}개 URL')


if __name__ == '__main__':
    sys.exit(main())
