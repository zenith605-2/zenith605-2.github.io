"""검색어 하나 = 페이지 하나 (2026-11-27 사용자 "검색 단어 영어 한글로 선정부터 해", "이미지도 넣고
읽기 싫게 만들어 놨니"). 글은 세 줄 + 그림 + 표/단계, 끝에 앱 보드로 보낸다.

검색어는 구글 자동완성으로 골랐다(같은 날). 숫자는 ACT DB·출처가 있는 것만 쓴다.
build.py 가 write_all() 을 부른다.
"""
import html
import os

SITE = 'https://actparty.app'
E = html.escape

KO_BOARD, EN_BOARD = '/ko/test-pumasi.html', '/android-closed-testing.html'

PAGES = [
    # ── 한국어 ──
    dict(path='/ko/google-closed-test-12-testers.html', lang='ko', alt='/12-testers-14-days-free.html',
         title='구글 비공개 테스트 12명, 무료로 채우는 법 | ACT Party',
         desc='구글 플레이 새 개인 계정은 비공개 테스트 테스터 12명이 14일 필요합니다. 지인·대행·품앗이를 비교하고 무료로 채우는 법.',
         h1='구글 비공개 테스트 12명', img='ko_01_board',
         lines=['새 개인 개발자 계정은 테스터 12명이 비공개 테스트에 14일 참여해야 출시할 수 있어요.',
                '지인은 대개 몇 명에서 멈추고, 대행은 돈이 들어요.',
                '같은 처지의 개발자끼리 서로 테스트해 주면 무료로 채워요.'],
         table=(['방법', '비용', '14일 유지', '피드백'],
                [['지인', '무료', '부탁해야 함', '적음'],
                 ['대행', '유료', '됨', '형식적'],
                 ['품앗이 (ACT)', '무료', '서로 기록이 보임', '개발자 의견']])),
    dict(path='/ko/closed-test-14-days.html', lang='ko', alt='/closed-testing-requirements.html',
         title='비공개 테스트 14일, 매일 열어야 하나요? | ACT Party',
         desc='구글 플레이 비공개 테스트 14일 조건: 구글이 보는 건 옵트인이 14일 이어졌는지입니다. 끝난 테스트 기록으로 본 실제 14일.',
         h1='비공개 테스트 14일', img='ko_03_calendar',
         lines=['구글이 보는 건 테스터 12명의 옵트인이 14일 이어졌는지예요.',
                '중간에 테스트에서 나간 사람은 12명에서 빠져요. 몇 명 더 모으세요.',
                'ACT는 서로 앱을 연 날이 달력에 자동으로 쌓여서 14일이 어디까지 왔는지 보여요.'],
         steps=['1일차: 12명 이상 옵트인 · 설치', '1~14일: 옵트인 유지 (나간 사람은 빠짐)',
                '14일 뒤: 플레이 콘솔에서 프로덕션 신청 버튼이 열림'],
         more=[('/ko/guides/what-google-checks.html', '구글이 실제로 보는 것'),
               ('/ko/guides/daily-opens-data.html', '14일 동안 실제로 연 날 기록')]),
    dict(path='/ko/closed-tester-recruit.html', lang='ko', alt='/find-android-app-testers.html',
         title='비공개 테스터 모집 — 내 앱 올리고 테스터 받기 | ACT Party',
         desc='안드로이드 앱 비공개 테스터 모집: ACT Party에 앱을 올리면 테스터를 찾는 다른 개발자가 신청하고, 서로 테스트해 12명을 채웁니다.',
         h1='비공개 테스터 모집', img='ko_02_setup',
         lines=['모집 글을 따로 쓰지 않아도 돼요. 앱을 올리면 보드에 바로 떠요.',
                '다른 개발자가 신청하면 수락하고, 서로의 앱을 테스트해요.',
                '그룹 가입 → 옵트인 → 설치 3단계를 앱이 순서대로 안내해요.'],
         steps=['ACT Party 설치 · 내 앱 등록 (그룹·옵트인 링크)', '보드에서 신청을 받거나 직접 신청',
                '서로 설치 → 매일 연 날이 자동 기록']),
    dict(path='/ko/closed-test-agency.html', lang='ko', alt='/closed-testing-service.html',
         title='비공개 테스트 대행 vs 품앗이 — 비교 | ACT Party',
         desc='구글 플레이 비공개 테스트 대행과 개발자 품앗이를 비용·테스터·피드백으로 비교합니다. ACT Party는 무료 품앗이 앱입니다.',
         h1='비공개 테스트 대행 대신 품앗이', img='ko_05_free',
         lines=['대행은 돈을 내고 12명을 받는 방식이에요.',
                '품앗이는 내가 다른 개발자 앱을 테스트하고 그만큼 돌려받아요.',
                'ACT Party는 모든 기능이 무료이고, 크레딧·포인트 구매가 없어요.'],
         table=(['', '대행', '품앗이 (ACT)'],
                [['비용', '유료', '무료'], ['테스터', '모르는 사람', '같은 처지의 개발자'],
                 ['기록', '업체가 보고', '서로 연 날이 자동 기록'], ['내가 할 일', '없음', '상대 앱 테스트']])),
    dict(path='/ko/closed-test-rejected.html', lang='ko', alt=None,
         title='비공개 테스트 거절 — "테스터가 앱에 참여하지 않았습니다" | ACT Party',
         desc='프로덕션 액세스 신청이 거절된 사례를 ACT 기록으로 정리했습니다. 12명을 채워도 14일을 다 채운 테스터가 적으면 거절된 사례가 있었습니다.',
         h1='비공개 테스트 거절 사례', img='ko_03_calendar',
         lines=['12명·14일을 채워도 프로덕션 신청이 거절될 수 있어요.',
                'ACT 기록이 있는 거절 사례는 12명 중 14일을 다 채운 사람이 5명이었어요.',
                '출시된 앱 250개 중 234개는 테스터가 하루 1분 이상 쓴 날이 15% 미만이었어요 (2026-11-17 기준).'],
         steps=['12명보다 몇 명 더 모으기', '14일 끝날 때까지 옵트인 유지 확인',
                '테스터 의견을 모아 신청 질문지에 쓰기'],
         more=[('/ko/guides/production-form.html', '프로덕션 신청 질문지')]),
    dict(path='/ko/closed-testing-how.html', lang='ko', alt='/guides/test-swap.html',
         title='구글 비공개 테스트 방법 — 링크 3개 확인부터 | ACT Party',
         desc='구글 플레이 비공개 테스트 방법: 그룹·옵트인·국가 링크 확인, 내부 테스트는 12명에 안 들어감, 14일 유지.',
         h1='구글 비공개 테스트 방법', img='ko_02_setup',
         lines=['다른 구글 계정으로 그룹·옵트인 링크·국가를 먼저 열어 보세요.',
                '내부 테스트 참여자는 12명에 들어가지 않아요. 비공개 테스트만 세요.',
                '14일 동안 옵트인이 이어지면 프로덕션 신청이 열려요.'],
         table=(['트랙', '12명·14일에 세나'], [['내부 테스트', '안 셈'], ['비공개 테스트', '셈'], ['공개 테스트', '안 셈']]),
         more=[('/ko/guides/google-group.html', '구글 그룹 공개 설정'),
               ('/ko/guides/country-availability.html', '국가 설정')]),
    dict(path='/ko/internal-vs-closed-test.html', lang='ko', alt='/closed-testing-vs-internal-testing.html',
         title='내부 테스트 비공개 테스트 차이 — 12명은 비공개 테스트만 셉니다 | ACT Party',
         desc='구글 플레이 내부 테스트와 비공개 테스트 차이: 새 개인 계정의 테스터 12명·14일 조건은 비공개 테스트 참여자만 셉니다. 트랙별 비교.',
         h1='내부 테스트 비공개 테스트 차이', img='ko_02_setup',
         lines=['테스터 12명·14일 조건은 비공개 테스트 참여자만 세요.',
                '내부 테스트 링크로 설치하고 매일 열어도 이 조건에는 들어가지 않아요.',
                '링크를 보내기 전에 플레이 콘솔에서 트랙 이름이 "비공개 테스트"인지 확인하세요.'],
         table=(['트랙', '12명·14일에 세나', '참여 방법'],
                [['내부 테스트', '안 셈', '개발자가 넣은 이메일 목록'],
                 ['비공개 테스트', '셈', '구글 그룹·이메일 목록 + 옵트인'],
                 ['공개 테스트', '안 셈', '누구나']]),
         more=[('/ko/closed-testing-how.html', '구글 비공개 테스트 방법')]),
    # ── English ──
    dict(path='/12-testers-14-days-free.html', lang='en', alt='/ko/google-closed-test-12-testers.html',
         title='12 testers for 14 days, free — Google Play closed testing | ACT Party',
         desc='New Google Play personal accounts need 12 closed testers for 14 days. Compare friends, paid services and developer swaps, and fill it for free.',
         h1='12 testers for 14 days, free', img='en_01_board',
         lines=['New personal developer accounts need 12 testers opted in to a closed test for 14 days.',
                'Friends usually stop at a few; paid services cost money.',
                'Developers in the same spot test each other\'s apps — free.'],
         table=(['Way', 'Cost', 'Stays 14 days', 'Feedback'],
                [['Friends', 'Free', 'If you keep asking', 'Little'], ['Paid service', 'Paid', 'Yes', 'Generic'],
                 ['Swap (ACT)', 'Free', 'Both sides see the record', 'From developers']])),
    dict(path='/closed-testing-requirements.html', lang='en', alt='/ko/closed-test-14-days.html',
         title='Google Play closed testing requirements — 12 testers, 14 days | ACT Party',
         desc='What Google Play asks of new personal developer accounts: a closed test with at least 12 opted-in testers for 14 days before production access.',
         h1='Closed testing requirements', img='en_03_calendar',
         lines=['At least 12 testers opted in to a closed test, for 14 days in a row.',
                'Internal and open testing do not count. Testers who leave early stop counting.',
                'Then you apply for production; the form asks about your testing.'],
         steps=['Day 1: 12+ testers opt in and install', 'Days 1–14: stay opted in',
                'After 14 days: apply for production in Play Console'],
         more=[('/guides/what-google-checks.html', 'What Google actually checks'),
               ('/guides/production-form.html', 'The production access form')]),
    dict(path='/closed-testing-vs-internal-testing.html', lang='en', alt='/ko/internal-vs-closed-test.html',
         title='Closed testing vs internal testing — which counts for the 12 testers | ACT Party',
         desc='Only closed testing counts toward Google Play\'s 12 testers for 14 days. Internal and open testing do not. A quick comparison.',
         h1='Closed vs internal testing', img='en_02_setup',
         lines=['Only closed testing counts toward the 12 testers × 14 days.',
                'An internal testing link can be installed and used daily — it still does not count.',
                'Check the track name in Play Console before you send a link.'],
         table=(['Track', 'Counts?', 'Who can join'],
                [['Internal testing', 'No', 'Your email list'], ['Closed testing', 'Yes', 'Google Group or email list + opt-in'],
                 ['Open testing', 'No', 'Anyone']])),
    dict(path='/closed-testing-community.html', lang='en', alt='/ko/closed-tester-recruit.html',
         title='Google Play closed testing community — test each other\'s apps | ACT Party',
         desc='A closed testing community for Android developers: list your app, accept requests, and test each other\'s apps until both reach 12 testers for 14 days.',
         h1='Closed testing community', img='en_04_today',
         lines=['List your app; other developers who need testers request it.',
                'Test theirs, they test yours — the days each side opened are recorded automatically.',
                'Open every app you test with one button. No screenshots.'],
         steps=['Install ACT Party and add your app', 'Accept requests or send your own',
                'Both sides install — daily opens recorded']),
    dict(path='/closed-testing-service.html', lang='en', alt='/ko/closed-test-agency.html',
         title='Closed testing service vs developer swap — comparison | ACT Party',
         desc='Paid Google Play closed testing services compared with free developer swaps on cost, testers and records.',
         h1='Closed testing service or swap?', img='en_05_free',
         lines=['A paid service sells you 12 testers.',
                'A swap means you test other developers\' apps and get the same back.',
                'ACT Party is free — no credits or points to buy.'],
         table=(['', 'Paid service', 'Swap (ACT)'],
                [['Cost', 'Paid', 'Free'], ['Testers', 'Strangers', 'Developers in the same spot'],
                 ['Record', 'Reported by the vendor', 'Daily opens, both sides'], ['Your part', 'None', 'Test their app']])),
]

T = {
    'ko': dict(board='테스터를 찾는 앱 보기', get='ACT Party 무료로 받기', guides='가이드', apps='앱 목록', home='ACT Party'),
    'en': dict(board='See apps looking for testers', get='Get ACT Party — free', guides='Guides', apps='All apps', home='ACT Party'),
}

STYLE = """<style>
  .kw h1 { font-size: 26px; margin: 0 0 12px; }
  .kw .lines { margin: 0 0 18px; padding-left: 18px; line-height: 1.7; font-size: 16px; }
  .kw .hero { display: block; width: 100%; max-width: 260px; margin: 8px auto 18px; border-radius: 16px; }
  .kw table { border-collapse: collapse; width: 100%; margin: 0 0 18px; font-size: 15px; }
  .kw th, .kw td { border-top: 1px solid var(--ink700, #1D242D); padding: 9px 6px; text-align: left; }
  .kw th { color: var(--ink300, #8A97A6); font-weight: 600; }
  .kw ol.flow { counter-reset: s; list-style: none; padding: 0; margin: 0 0 18px; }
  .kw ol.flow li { counter-increment: s; display: flex; gap: 10px; align-items: center; padding: 10px 0; border-top: 1px solid var(--ink700, #1D242D); }
  .kw ol.flow li::before { content: counter(s); flex: none; width: 26px; height: 26px; border-radius: 50%; background: var(--mint, #3DDC97); color: #05261A; font-weight: 800; display: inline-flex; align-items: center; justify-content: center; }
  .kw .cta { display: flex; gap: 10px; flex-wrap: wrap; margin: 6px 0 18px; }
</style>"""


def render(p):
    lang, t = p['lang'], T[p['lang']]
    board = KO_BOARD if lang == 'ko' else EN_BOARD
    guides = '/ko/guides/' if lang == 'ko' else '/guides/'
    alts = ''
    if p.get('alt'):
        other = 'en' if lang == 'ko' else 'ko'
        alts = (f'<link rel="alternate" hreflang="{lang}" href="{SITE}{p["path"]}">\n'
                f'<link rel="alternate" hreflang="{other}" href="{SITE}{p["alt"]}">\n')
    table = ''
    if p.get('table'):
        head, rows = p['table']
        table = ('<table><tr>' + ''.join(f'<th>{E(h)}</th>' for h in head) + '</tr>' +
                 ''.join('<tr>' + ''.join(f'<td>{E(c)}</td>' for c in r) + '</tr>' for r in rows) + '</table>')
    steps = ''
    if p.get('steps'):
        steps = '<ol class="flow">' + ''.join(f'<li>{E(s)}</li>' for s in p['steps']) + '</ol>'
    more = ''
    if p.get('more'):
        more = '<p class="muted">' + ' · '.join(f'<a href="{u}">{E(x)}</a>' for u, x in p['more']) + '</p>'
    img = f'/img/kw/{p["img"]}.jpg'
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(p['title'])}</title>
<meta name="description" content="{E(p['desc'])}">
<link rel="canonical" href="{SITE}{p['path']}">
{alts}<meta property="og:title" content="{E(p['h1'])} | ACT Party">
<meta property="og:description" content="{E(p['desc'])}">
<meta property="og:url" content="{SITE}{p['path']}">
<meta property="og:image" content="{SITE}{img}">
<meta property="og:type" content="article">
<link rel="stylesheet" href="/assets/app.css?v=126">
{STYLE}
</head>
<body>
<header class="top">
  <div class="wrap">
    <a class="brand" href="/"><span class="dot">ACT</span> ACT Party</a>
    <nav>
      <a href="{board}">{E(t['board'] if lang == 'en' else '앱 보드')}</a>
      <a href="{guides}">{E(t['guides'])}</a>
    </nav>
  </div>
</header>
<article class="kw wrap narrow" style="padding-top:24px">
  <h1>{E(p['h1'])}</h1>
  <ul class="lines">{''.join(f'<li>{E(x)}</li>' for x in p['lines'])}</ul>
  {table}{steps}
  <div class="cta">
    <a class="btn" href="{board}">{E(t['board'])}</a>
    <a class="btn ghost" href="https://play.google.com/store/apps/details?id=kr.testerparty.tester_party&amp;referrer=utm_source%3Dactparty_site%26utm_medium%3Dkw" rel="noopener">{E(t['get'])}</a>
  </div>
  <img class="hero" src="{img}" alt="{E(p['h1'])} — ACT Party" width="540" height="960" loading="lazy">
  {more}
</article>
<footer class="bot"><div class="wrap"><p>
  <a href="/">ACT Party</a> · <a href="{guides}">{E(t['guides'])}</a> · <a href="/a/">{E(t['apps'])}</a> ·
  <a href="/privacy.html">Privacy</a> · <a href="/terms.html">Terms</a></p></div></footer>
</body>
</html>
"""


def write_all(base):
    out = []
    for p in PAGES:
        fp = os.path.join(base, *p['path'].strip('/').split('/'))
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, 'w', encoding='utf-8', newline='') as f:
            f.write(render(p))
        out.append(p['path'])
    return out


def links(lang):
    """보드 페이지 아래에 거는 검색어 페이지 링크"""
    return [(p['path'], p['h1']) for p in PAGES if p['lang'] == lang]
