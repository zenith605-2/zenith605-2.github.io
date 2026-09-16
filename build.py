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
import shutil
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
    ('/check.html', '0.9'),
    ('/guides/', '0.8'),
    ('/guides/what-google-checks.html', '0.8'),
    ('/guides/daily-opens-data.html', '0.8'),
    ('/guides/why-testers-drop.html', '0.7'),
    ('/guides/production-form.html', '0.8'),
    ('/guides/google-group.html', '0.8'),
    ('/guides/country-availability.html', '0.8'),
    ('/guides/blocked-screens.html', '0.8'),
    ('/guides/closed-test-setup.html', '0.8'),
    ('/guides/troubleshooting.html', '0.8'),
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


def posts():
    """게시판 글.

    게시판 화면이 부르는 것과 같은 RPC 다 (assets/api.js posts()). 표를 직접
    읽으면 글쓴이 이름이 안 따라오고, 무엇보다 두 곳이 서로 다른 글 목록을
    보게 될 수 있다.
    """
    rows = _rpc('community_list', {})
    # 목록 RPC 는 본문을 300자에서 자른다 — 미리보기 두 줄에 쓰는 값이라 그렇다.
    # 그대로 구우면 페이지마다 첫 문단만 남아서, 검색에 걸리게 하려던 본문이
    # 통째로 빠진다. 글마다 한 번 더 부른다.
    return [_rpc('community_post', {'p_id': r['id']}) or r for r in rows]


def _rpc(name, body):
    req = urllib.request.Request(
        f'{SUPABASE_URL}/rest/v1/rpc/{name}',
        data=json.dumps(body).encode(),
        headers={
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
            'Content-Type': 'application/json',
        })
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())


# 게시판 글 중 둘은 웹 가이드와 같은 내용을 다룬다 — ⑤ 신청서, ⑥ 구글 그룹.
# 글을 구워 놓으면 그 둘이 같은 검색어를 놓고 우리 페이지끼리 경쟁한다.
# 가이드 쪽이 더 길고 언어판도 다섯이라, 그쪽을 정본으로 지목한다.
#
# 글은 그대로 둔다 — 게시판을 넘기다 읽는 사람에게는 이 길이가 맞다.
SAME_AS = {
    'b7aa6295': ('production-form', 'ko'),   # ⑤ 마지막 관문
    '57e82241': ('production-form', 'en'),   # ⑤ The last gate
    'e72b05ad': ('google-group', 'ko'),      # ⑥ 구글 그룹
    '6532aa58': ('google-group', 'en'),      # ⑥ Google Group
    '25b49497': ('blocked-screens', 'ko'),        # ⑦ 막히는 화면
    '1066dd26': ('blocked-screens', 'en'),        # ⑦ five screens
    '6907dbd1': ('why-testers-drop', 'ko'),       # ⑧ 왜 사라지나
    'c72632ae': ('why-testers-drop', 'en'),       # ⑧ why disappear
    'f62b52a2': ('country-availability', 'ko'),   # ⑨ 배포 국가
    '48ae70f7': ('country-availability', 'en'),   # ⑨ all countries
    '96c19d4b': ('what-google-checks', 'ko'),     # ⑩ 구글이 보는 것
    'a9e52539': ('what-google-checks', 'en'),     # ⑩ what Google checks
    '4abb2978': ('daily-opens-data', 'ko'),       # ⑪ 14일 내내
    'cf0dcf78': ('daily-opens-data', 'en'),       # ⑪ nobody opens
}


def same_as(row):
    """이 글의 정본이 따로 있으면 그 주소, 없으면 None."""
    hit = SAME_AS.get(row['id'][:8])
    if not hit:
        return None
    slug, lang = hit
    prefix = '' if lang == 'en' else '/' + lang
    return f'{prefix}/guides/{slug}.html'


# 주소는 /p/<id 앞 8자>.html 이다.
#
# 제목을 slug 로 쓰면 한국어·일본어 글은 URL 이 통째로 퍼센트 인코딩되고,
# 제목을 고치면 주소가 바뀌어 이미 나간 링크가 죽는다. 검색에서 slug 가 주는
# 이득은 제목·본문에 비하면 작아서, 안 변하는 쪽을 골랐다.
def post_path(row):
    return '/p/' + row['id'][:8] + '.html'


def linkify(escaped):
    """본문에 그냥 적힌 주소를 누를 수 있게 만든다.

    escape 를 거친 문자열만 넣는다 — 주소가 아닌 부분이 태그로 살아나면 안 된다.
    끝의 문장부호는 주소에서 뺀다 ("...html." 의 마침표까지 넣으면 404 다).
    게시판 화면(community.html linkify)과 같은 규칙이다.
    """
    def one(m):
        u = m.group(0)
        tail = ''
        while u and u[-1] in '.,;:)]':
            tail = u[-1] + tail
            u = u[:-1]
        return f'<a href="{u}" rel="noopener">{u}</a>{tail}'
    return re.sub(r'https?://[^\s<]+', one, escaped)


def post_body(content, images):
    """본문의 [imgN] 자리에 그 번호의 사진을 끼운다.

    앱(community_screen.dart _bodyWithImages)·웹(community.html
    bodyWithImages)과 같은 규칙이어야 한 글이 세 곳에서 다르게 보이지 않는다.
    """
    e = html.escape
    imgs = images or []
    text = content or ''
    used = set()
    out = []
    cursor = 0
    for m in re.finditer(r'\[img(\d+)\]', text):
        i = int(m.group(1)) - 1
        before = text[cursor:m.start()].strip()
        if before:
            out.append(f'<p class="desc pre">{linkify(e(before))}</p>')
        if 0 <= i < len(imgs):
            out.append(f'<img class="shot" src="{e(imgs[i])}" alt="">')
            used.add(i)
        cursor = m.end()
    rest = text[cursor:].strip()
    if rest:
        out.append(f'<p class="desc pre">{linkify(e(rest))}</p>')
    for i, u in enumerate(imgs):
        if i not in used:
            out.append(f'<img class="shot" src="{e(u)}" alt="">')
    return '\n  '.join(out)


def post_page(row):
    e = html.escape
    title = row.get('title') or ''
    content = row.get('content') or ''
    lang = (row.get('lang') or 'en').split('-')[0]
    imgs = row.get('images') or []
    author = row.get('author_name') or 'A developer'
    day = (row.get('created_at') or '')[:10]

    plain = re.sub(r'\[img\d+\]', ' ', content)
    plain = re.sub(r'\s+', ' ', plain).strip()
    desc = plain[:280]

    canon = same_as(row) or post_path(row)
    ld = {
        '@context': 'https://schema.org',
        '@type': 'DiscussionForumPosting',
        'headline': title,
        'datePublished': row.get('created_at'),
        'author': {'@type': 'Person', 'name': author},
        'url': SITE + post_path(row),
    }
    if desc:
        ld['articleBody'] = desc
    if imgs:
        ld['image'] = imgs[0]

    og_img = f'<meta property="og:image" content="{e(imgs[0])}">' if imgs else ''
    return f"""<!DOCTYPE html>
<html lang="{e(lang)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} | ACT Party</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}{canon}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
{og_img}
<link rel="stylesheet" href="/assets/app.css?v={CACHE_V}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>

<header class="top">
  <div class="wrap">
    <a class="brand" href="/"><span class="dot">ACT</span> ACT Party</a>
    <nav>
      <a href="/community.html">Board</a>
      <a href="/guides/">Guides</a>
      <a href="/board.html">App board</a>
    </nav>
  </div>
</header>

<article class="wrap narrow" style="padding-top:28px">
  <div class="card">
    <h1 class="app-name" style="font-size:22px;margin:0 0 6px">{e(title)}</h1>
    <p class="muted">{e(author)}{f' &middot; {e(day)}' if day else ''}</p>
  {post_body(content, imgs)}
  </div>

  <p style="margin:22px 0 0">
    <a href="/community.html#post={e(row['id'])}">Read replies on the board &rarr;</a>
  </p>
  <p style="margin:8px 0 0"><a href="/community.html">&larr; All posts</a></p>
</article>

<footer class="bot"><div class="wrap"><p>
  <a href="/">ACT Party</a> &middot; <a href="/guides/">Guides</a> &middot;
  <a href="/privacy.html">Privacy</a></p></div></footer>
</body>
</html>
"""


def prune_apps(live):
    """목록에서 빠진 앱의 페이지를 지운다.

    여기서 굽기만 하고 안 지웠더니 141개 폴더 중 29개가 이미 없는 앱이었다.
    사이트맵에는 안 올라가지만 예전에 색인된 주소라 사람이 눌러 들어올 수 있고,
    그 페이지는 "N명 모집 중"이라고 거짓말을 한다 (2026-09-15).

    한 번에 다 날리는 사고를 막는다: 목록을 못 받아 왔거나 절반 넘게 사라진
    것처럼 보이면 손대지 않고 넘어간다. 앱이 다시 목록에 들어오면 다음
    실행에서 페이지도 다시 생긴다.
    """
    root = os.path.join(BASE, 'a')
    if not os.path.isdir(root):
        return
    have = {d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d))}
    gone = have - live
    if len(live) < 20 or len(gone) > len(have) * 0.4:
        print(f'  ! 앱 목록이 이상하다 (현재 {len(live)}, 지울 것 {len(gone)}) '
              f'— 지우지 않고 넘어간다')
        return
    for d in sorted(gone):
        shutil.rmtree(os.path.join(root, d))
    if gone:
        print(f'  내려간 앱 페이지 {len(gone)}개 삭제')


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

    # 게시판 글. 앱 상세와 달리 글마다 내용이 다 달라서 읽히는 페이지 쪽
    # 사이트맵에 넣는다.
    rows = posts()
    os.makedirs(os.path.join(BASE, 'p'), exist_ok=True)
    for row in rows:
        with open(os.path.join(BASE, 'p', row['id'][:8] + '.html'), 'w',
                  encoding='utf-8', newline='') as f:
            f.write(post_page(row))
    # 정본이 가이드 쪽인 글은 사이트맵에 안 올린다 — 올려 두고 canonical 로
    # 다른 데를 가리키면 구글에 앞뒤가 안 맞는 말을 하는 셈이다.
    urls += [f'{SITE}{post_path(r)}' for r in rows if not same_as(r)]

    app_urls = []
    prune_apps({a['package_name'] for a in listed})
    for a in listed:
        pkg = a['package_name']
        d = os.path.join(BASE, 'a', pkg)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, 'index.html'), 'w', encoding='utf-8',
                  newline='') as f:
            f.write(page(a))
        app_urls.append(f'{SITE}/a/{pkg}/')

    # 사이트맵을 둘로 나눈다.
    #
    # 하나에 다 넣었더니 앱 상세 107개가 전체의 63% 를 차지했다. 서로 비슷하고
    # 얇은 페이지 뭉치라 구글이 뒤로 미루는데, 그 줄에 한국어 가이드·랜딩이
    # 같이 밀려 크롤링조차 안 됐다 (색인 10 / 미색인 80, 2026-09-13).
    #
    # 읽히길 바라는 페이지와 목록용 페이지를 갈라 두면 중요한 쪽이 먼저 처리된다.
    def write_sitemap(name, items):
        body = '\n'.join(f'  <url><loc>{u}</loc></url>' for u in items)
        with open(os.path.join(BASE, name), 'w', encoding='utf-8',
                  newline='') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                    f'{body}\n</urlset>\n')

    write_sitemap('sitemap-pages.xml', urls)
    write_sitemap('sitemap-apps.xml', app_urls)

    # 색인 파일 — 구글에는 이 하나만 제출하면 아래 둘을 같이 읽는다
    with open(os.path.join(BASE, 'sitemap.xml'), 'w', encoding='utf-8',
              newline='') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                f'  <sitemap><loc>{SITE}/sitemap-pages.xml</loc></sitemap>\n'
                f'  <sitemap><loc>{SITE}/sitemap-apps.xml</loc></sitemap>\n'
                '</sitemapindex>\n')
    urls = urls + app_urls

    with open(os.path.join(BASE, 'robots.txt'), 'w', encoding='utf-8',
              newline='') as f:
        f.write('User-agent: *\nAllow: /\n'
                'Disallow: /console.html\n'
                f'Sitemap: {SITE}/sitemap.xml\n')

    print(f'앱 페이지 {len(listed)}개, 글 페이지 {len(rows)}개, 사이트맵 {len(urls)}개 URL')


if __name__ == '__main__':
    sys.exit(main())
