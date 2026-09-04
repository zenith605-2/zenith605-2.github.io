"""검색어를 정면으로 받는 랜딩 페이지를 다섯 언어 URL 로 굽는다.

가이드는 "이미 막힌 사람"이 읽는 글이다. 그 앞 단계 — 콘솔에서 12명 조건을
처음 보고 검색창에 그대로 치는 사람 — 을 받는 페이지가 없었다. 검색어 하나에
페이지 하나, 언어마다 URL 하나.

    python web/landing_build.py     (그다음 python web/build.py 로 사이트맵)

결과: web/<slug>.html (영어), web/<lang>/<slug>.html, web/landing_pages.json
"""
import html
import io
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://actparty.app'
LANGS = ['en', 'ko', 'ja', 'zh-Hans', 'zh-Hant']
CACHE_V = __import__('re').search(r'app\.css\?v=(\d+)',
                                  io.open(os.path.join(BASE, 'index.html'), encoding='utf-8').read()).group(1)
LANG_NAME = {'en': 'English', 'ko': '한국어', 'ja': '日本語',
             'zh-Hans': '简体中文', 'zh-Hant': '繁體中文'}
STORE = 'https://play.google.com/store/apps/details?id=kr.testerparty.tester_party'


def url_of(slug, lang):
    return f'{SITE}/{slug}.html' if lang == 'en' else f'{SITE}/{lang}/{slug}.html'


def path_of(slug, lang):
    return f'/{slug}.html' if lang == 'en' else f'/{lang}/{slug}.html'


def alt_links(slug):
    out = [f'<link rel="alternate" hreflang="{l}" href="{url_of(slug, l)}">' for l in LANGS]
    out.append(f'<link rel="alternate" hreflang="x-default" href="{url_of(slug, "en")}">')
    return '\n'.join(out)


def lang_bar(slug, current):
    items = []
    for l in LANGS:
        if l == current:
            items.append(f'<b>{LANG_NAME[l]}</b>')
        else:
            items.append(f'<a href="{path_of(slug, l)}" hreflang="{l}">{LANG_NAME[l]}</a>')
    return ('<p class="muted" style="font-size:12.5px;margin:0 0 18px">'
            + ' · '.join(items) + '</p>')


def guide(lang, name):
    """가이드 링크 — 같은 언어판으로."""
    return f'/guides/{name}.html' if lang == 'en' else f'/{lang}/guides/{name}.html'


def render(slug, lang, p):
    e = html.escape
    # FAQ 구조화 데이터 — 질문형 검색에 그대로 걸린다
    faq = {
        '@context': 'https://schema.org', '@type': 'FAQPage',
        'mainEntity': [{'@type': 'Question', 'name': q,
                        'acceptedAnswer': {'@type': 'Answer', 'text': a}}
                       for q, a in p['faq']],
    }
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(p['title'])}</title>
<meta name="description" content="{e(p['desc'], quote=True)}">
<link rel="canonical" href="{url_of(slug, lang)}">
{alt_links(slug)}
<meta property="og:title" content="{e(p['title'], quote=True)}">
<meta property="og:description" content="{e(p['desc'], quote=True)}">
<meta property="og:url" content="{url_of(slug, lang)}">
<meta property="og:type" content="article">
<link rel="stylesheet" href="/assets/app.css?v={CACHE_V}">
<script type="application/ld+json">{json.dumps(faq, ensure_ascii=False)}</script>
<style>
  #doc h2 {{ margin-top: 30px }}
  #doc .steps li {{ margin-bottom: 10px; line-height: 1.65 }}
  #doc .faq dt {{ font-weight: 700; margin-top: 16px }}
  #doc .faq dd {{ margin: 4px 0 0; line-height: 1.65 }}
</style>
</head>
<body>

<header class="top">
  <div class="wrap">
    <a class="brand" href="/"><span class="dot">ACT</span> ACT Party</a>
    <nav>
      <a href="/launched.html" data-t="nav_launched">Launched</a>
      <a href="/parties.html" data-t="nav_party">Parties</a>
      <a href="/community.html" data-t="nav_board">Board</a>
      <a href="/how.html" data-t="nav_how">What is ACT Party?</a>
      <span id="authSlot"></span>
      <span id="langSlot"></span>
    </nav>
  </div>
</header>

<article class="doc wrap narrow" id="doc" style="padding-top:30px">
{lang_bar(slug, lang)}
<h1 style="font-size:28px;margin:0 0 8px">{p['h1']}</h1>
<p class="muted" style="margin:0 0 24px">{p['sub']}</p>
{p['body']}
<h2>{e(p['faq_h'])}</h2>
<dl class="faq">
{''.join(f'<dt>{e(q)}</dt><dd>{e(a)}</dd>' for q, a in p['faq'])}
</dl>
<div class="note" style="margin:26px 0">{p['cta']}</div>
</article>

<footer class="bot"><div class="wrap"><p>
  <a href="{guide(lang, 'index').replace('index.html', '')}" data-t="nav_guides">Guides</a> ·
  <a href="/" data-t="nav_board_home">App board</a></p></div></footer>

<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script type="module">
import {{ mountAuth }} from '/assets/api.js?v={CACHE_V}';
import {{ t, applyDom, langPicker, wireLangPicker }} from '/assets/i18n.js?v={CACHE_V}';
document.getElementById('langSlot').innerHTML = langPicker();
applyDom();
wireLangPicker();
mountAuth('authSlot', t);
</script>
</body>
</html>
'''


# ---------------------------------------------------------------------------
# 페이지 1 — "구글 플레이 테스터 12명"
# 검색: google play 12 testers / closed testing 12 testers / 테스터 12명 / 12人のテスター
# ---------------------------------------------------------------------------
def p_12(lang):
    g = lambda n: guide(lang, n)
    return {
        'ko': dict(
            title='구글 플레이 테스터 12명, 어떻게 구하나 — 비공개 테스트 14일 통과법 | ACT Party',
            desc='새 개발자 계정은 테스터 12명이 14일 동안 비공개 테스트에 참여해야 출시할 수 있습니다. 구글이 알려주지 않는 테스터 구하는 법과, 개발자끼리 무료로 교환하는 방법.',
            h1='구글 플레이 테스터 12명, 어디서 구하나',
            sub='새 개발자 계정이 처음 만나는 벽 — 그리고 그 벽을 넘는 세 가지 길',
            body=f'''
<p>2023년 11월부터 새로 만든 개인 개발자 계정은 앱을 바로 출시할 수 없습니다.
먼저 <b>테스터 12명이 비공개 테스트에 옵트인하고 14일을 채워야</b> 프로덕션 신청
버튼이 열립니다. 콘솔에는 조건만 적혀 있고, 그 12명을 어디서 구하는지는 한 줄도
없습니다.</p>

<h2>구글이 실제로 세는 것</h2>
<p>테스터가 앱을 매일 열었는지가 아니라, <b>옵트인 상태가 14일 이어졌는지</b>를
봅니다. 끝난 테스트 44건을 실측했을 때 테스터는 평균 14일 중 8.5일만 앱을
열었고, 그래도 심사는 통과했습니다. 자세한 숫자는
<a href="{g('what-google-checks')}">구글이 실제로 보는 것</a>과
<a href="{g('daily-opens-data')}">14일 내내 앱을 여는 사람은 없어요</a>에
있습니다.</p>

<h2>테스터를 구하는 세 가지 길</h2>
<ol class="steps">
  <li><b>지인 12명</b> — 가장 빠르지만 대부분 3~4명에서 멈춥니다. 14일 동안
  옵트인을 유지해 달라는 부탁이 생각보다 큽니다.</li>
  <li><b>유료 테스터 서비스</b> — 건당 2~5만 원. 옵트인 유지는 되지만 실제로
  앱을 쓰는 사람은 아닙니다.</li>
  <li><b>개발자끼리 교환</b> — 같은 벽에 막힌 개발자가 매주 수천 명 생깁니다.
  서로 앱을 테스트해 주면 둘 다 12명을 채웁니다. 무료이고, 상대도 개발자라
  피드백이 남습니다.</li>
</ol>

<h2>교환이 잘 안 되는 이유와 해결</h2>
<p>레딧이나 디스코드에서 "내 앱 테스트해 주면 네 것도 해줄게"를 올리는 게 보통의
방법인데, 상대가 정말 매일 여는지 알 수 없고, 14일 뒤에 조용히 사라지는 사람이
많습니다. <b>ACT Party</b>는 이 교환을 앱이 대신 관리합니다. 상대 앱을 열면 그날
인증이 자동으로 기록되고, 서로의 진행이 보드에 보입니다. 아무도 서로를 믿을
필요가 없습니다.</p>

<h2>시작 순서</h2>
<ol class="steps">
  <li>Play Console에서 비공개 테스트 트랙을 만들고 <a href="{g('google-group')}">구글 그룹을 연결</a>합니다. 여기서 절반이 막힙니다.</li>
  <li>트랙에 버전(AAB)을 올려 검토를 통과시킵니다. 이게 없으면 옵트인 링크가 안 열립니다.</li>
  <li>ACT Party에 앱을 등록하고, 보드에서 다른 개발자 앱을 골라 테스트를 시작합니다.</li>
  <li>14일 뒤 프로덕션 신청 — <a href="{g('production-form')}">설문 9문항</a>은 미리 읽어 두세요.</li>
</ol>''',
            faq_h='자주 묻는 질문',
            faq=[
                ('테스터가 14일 동안 매일 앱을 열어야 하나요?',
                 '아닙니다. 구글은 옵트인 상태가 14일 이어졌는지를 봅니다. 실측 44건에서 테스터는 평균 8.5일만 열었고 심사는 통과했습니다.'),
                ('12명 중 한 명이 중간에 나가면 처음부터 다시인가요?',
                 '아닙니다. 남은 사람의 기간은 그대로 쌓이고, 새 테스터가 들어오면 그 사람만 14일을 채우면 됩니다.'),
                ('테스터에게 돈을 줘도 되나요?',
                 '구글 정책상 금지는 아니지만, 유료 테스터는 실제 사용자와 다르다는 점을 프로덕션 신청 설문에서 설명해야 합니다. 개발자 교환은 이 문제가 없습니다.'),
                ('ACT Party는 유료인가요?',
                 '무료입니다. 개발자끼리 서로 테스트하는 구조라 비용이 없습니다.'),
            ],
            cta=f'<b>ACT Party</b>에는 지금 테스터를 찾는 앱이 항상 20~40개 올라와 있습니다. 내 앱을 등록하고 하나 골라 시작하면 됩니다. <a href="/">보드 보기</a> · <a href="{STORE}">앱 받기</a>',
        ),
        'en': dict(
            title='How to get 12 testers for Google Play closed testing (the 14-day rule) | ACT Party',
            desc='New Google Play developer accounts need 12 testers opted in for 14 days before they can publish. Where those testers actually come from, and how developers trade tests for free.',
            h1='Where to find 12 testers for Google Play',
            sub='The first wall a new developer account hits — and three ways over it',
            body=f'''
<p>Since November 2023 a new personal developer account cannot publish straight
away. First, <b>12 testers have to opt into a closed test and stay for 14 days</b>;
only then does the production button unlock. The console states the rule and
says nothing about where those 12 people come from.</p>

<h2>What Google actually counts</h2>
<p>Not whether testers open the app every day, but whether their <b>opt-in lasted
14 days</b>. Across 44 finished tests, testers opened the app on 8.5 of 14 days on
average and the reviews still passed. The numbers are in
<a href="{g('what-google-checks')}">What Google actually checks</a> and
<a href="{g('daily-opens-data')}">Nobody opens your app all 14 days</a>.</p>

<h2>Three ways to find testers</h2>
<ol class="steps">
  <li><b>Friends and family</b> — fastest, and usually stops at three or four.
  Asking someone to stay opted in for two weeks is a bigger favour than it sounds.</li>
  <li><b>Paid tester services</b> — roughly $20–50 per run. The opt-ins hold, but
  nobody actually uses the app.</li>
  <li><b>Trading with other developers</b> — thousands of developers hit this same
  wall every week. Test each other's apps and both of you reach 12. Free, and
  since the other side is a developer, you get real feedback.</li>
</ol>

<h2>Why trades fall apart, and the fix</h2>
<p>The usual way is a Reddit or Discord post: "test mine and I'll test yours".
You can't tell whether the other person really opens your app, and many quietly
vanish after a few days. <b>ACT Party</b> runs the trade for you: opening the
other app records that day's check-in automatically, and both sides' progress is
visible on the board. Nobody has to trust anybody.</p>

<h2>In order</h2>
<ol class="steps">
  <li>Create a closed testing track in Play Console and <a href="{g('google-group')}">connect a Google Group</a>. Half of all problems start here.</li>
  <li>Upload a build (AAB) to that track and get it through review. Without a published build the opt-in link opens nothing.</li>
  <li>Register the app on ACT Party, pick another developer's app from the board, and start.</li>
  <li>After 14 days, apply for production — read <a href="{g('production-form')}">the 9 questions</a> first.</li>
</ol>''',
            faq_h='Questions people ask',
            faq=[
                ('Do testers have to open the app every day for 14 days?',
                 'No. Google counts whether the opt-in lasted 14 days. In 44 measured tests testers opened the app on 8.5 days on average and the review passed.'),
                ('If one of the 12 drops out, does the clock restart?',
                 'No. The remaining testers keep their days; a replacement only needs to complete their own 14.'),
                ('Can I pay testers?',
                 "Google doesn't forbid it, but the production form asks how your testers' usage differs from real users, and paid opt-ins are hard to explain. Trading with developers avoids the question."),
                ('Is ACT Party free?',
                 'Yes. Developers test each other, so there is nothing to charge for.'),
            ],
            cta=f'<b>ACT Party</b> usually has 20–40 apps looking for testers at any moment. Register yours, pick one, and start. <a href="/">See the board</a> · <a href="{STORE}">Get the app</a>',
        ),
        'ja': dict(
            title='Google Play のテスター12人をどう集めるか — 非公開テスト14日の通過法 | ACT Party',
            desc='新しいデベロッパーアカウントは、テスター12人が14日間非公開テストに参加しないと公開できません。Googleが教えてくれないテスターの集め方と、開発者同士で無料で交換する方法。',
            h1='Google Play のテスター12人はどこで集めるか',
            sub='新しいアカウントが最初にぶつかる壁と、越える三つの道',
            body=f'''
<p>2023年11月以降、新しく作った個人デベロッパーアカウントはすぐには公開できません。
まず<b>テスター12人が非公開テストにオプトインして14日間続ける</b>必要があり、
それまで製品版の申請ボタンは開きません。コンソールには条件だけが書かれていて、
その12人をどこで集めるかは一行もありません。</p>

<h2>Googleが実際に数えているもの</h2>
<p>テスターが毎日アプリを開いたかではなく、<b>オプトインが14日続いたか</b>です。
完了したテスト44件を実測すると、テスターは14日のうち平均8.5日しか開いておらず、
それでも審査は通りました。詳しい数字は
<a href="{g('what-google-checks')}">Googleが実際に見ているもの</a>と
<a href="{g('daily-opens-data')}">14日間ずっと開く人はいません</a>にあります。</p>

<h2>テスターを集める三つの道</h2>
<ol class="steps">
  <li><b>知人12人</b> — 一番速いが、たいてい3〜4人で止まります。14日間オプトインを
  維持してもらう頼みは、思うより重いものです。</li>
  <li><b>有料テスターサービス</b> — 1回2〜5千円ほど。オプトインは維持されますが、
  実際にアプリを使う人ではありません。</li>
  <li><b>開発者同士の交換</b> — 同じ壁にぶつかる開発者が毎週数千人います。
  互いのアプリをテストすれば、両方が12人に届きます。無料で、相手も開発者なので
  フィードバックが残ります。</li>
</ol>

<h2>交換がうまくいかない理由と解決</h2>
<p>RedditやDiscordに「私のをテストしてくれたらあなたのも」と書くのが普通の方法ですが、
相手が本当に毎日開いているか分からず、数日で静かに消える人も多い。
<b>ACT Party</b>はこの交換をアプリが代わりに管理します。相手のアプリを開くとその日の
チェックインが自動で記録され、双方の進み具合がボードに見えます。誰も相手を
信じる必要がありません。</p>

<h2>進める順番</h2>
<ol class="steps">
  <li>Play Console で非公開テストトラックを作り、<a href="{g('google-group')}">Googleグループを連携</a>します。問題の半分はここで起きます。</li>
  <li>トラックにビルド（AAB）を上げて審査を通します。公開済みのビルドがないとオプトインリンクは開きません。</li>
  <li>ACT Party にアプリを登録し、ボードから他の開発者のアプリを選んでテストを始めます。</li>
  <li>14日後に製品版を申請 — <a href="{g('production-form')}">9つの設問</a>は先に読んでおいてください。</li>
</ol>''',
            faq_h='よくある質問',
            faq=[
                ('テスターは14日間毎日アプリを開く必要がありますか？',
                 'いいえ。Googleはオプトインが14日続いたかを見ます。実測44件でテスターは平均8.5日しか開いておらず、審査は通りました。'),
                ('12人のうち1人が途中で抜けたら最初からですか？',
                 'いいえ。残った人の日数はそのまま積み上がり、新しいテスターはその人だけが14日を満たせばいいのです。'),
                ('テスターにお金を払ってもいいですか？',
                 'Googleの規約上禁止ではありませんが、製品版申請の設問で「テスターの使い方が実際のユーザーとどう違うか」を説明する必要があります。開発者同士の交換にはこの問題がありません。'),
                ('ACT Party は有料ですか？',
                 '無料です。開発者同士で互いにテストする仕組みなので費用がかかりません。'),
            ],
            cta=f'<b>ACT Party</b> には今テスターを探しているアプリが常に20〜40個あります。自分のアプリを登録し、一つ選んで始めるだけです。<a href="/">ボードを見る</a> · <a href="{STORE}">アプリを入手</a>',
        ),
        'zh-Hans': dict(
            title='Google Play 的 12 名测试者从哪里来 — 通过 14 天封闭测试 | ACT Party',
            desc='新的开发者账号必须有 12 名测试者加入封闭测试并保持 14 天才能发布。Google 没有告诉你怎么找到他们；这里是找测试者的方法，以及开发者之间免费互测的方式。',
            h1='Google Play 的 12 名测试者去哪里找',
            sub='新账号遇到的第一道墙，以及翻过去的三条路',
            body=f'''
<p>自 2023 年 11 月起，新建的个人开发者账号不能直接发布应用。必须先有
<b>12 名测试者加入封闭测试并保持 14 天</b>，正式版申请按钮才会打开。
控制台里只写了条件，关于这 12 个人从哪里来，一个字都没有。</p>

<h2>Google 真正在数的是什么</h2>
<p>不是测试者是否每天打开应用，而是<b>加入状态是否持续了 14 天</b>。
对 44 次已完成的测试实测，测试者平均只在 14 天里打开了 8.5 天，审核照样通过。
详细数字见<a href="{g('what-google-checks')}">Google 实际检查什么</a>和
<a href="{g('daily-opens-data')}">没有人会连开 14 天</a>。</p>

<h2>找测试者的三条路</h2>
<ol class="steps">
  <li><b>找 12 个熟人</b> — 最快，但通常停在三四个人。请人保持加入状态两周，
  是个比想象中大的人情。</li>
  <li><b>付费测试服务</b> — 每次约 20～50 美元。加入状态能保住，但没人真的用你的应用。</li>
  <li><b>开发者之间互测</b> — 每周都有几千个开发者撞上同一道墙。互相测试对方的应用，
  两边都凑够 12 人。免费，而且对方也是开发者，会留下真实反馈。</li>
</ol>

<h2>互测为什么容易散，怎么解决</h2>
<p>通常的做法是在 Reddit 或 Discord 发帖："测我的，我也测你的"。但你不知道对方是否
真的每天打开，很多人几天后就悄悄消失。<b>ACT Party</b> 替你管理这件事：打开对方的
应用，当天的打卡自动记录，双方进度都在看板上可见。谁也不需要相信谁。</p>

<h2>按顺序做</h2>
<ol class="steps">
  <li>在 Play Console 建立封闭测试轨道，并<a href="{g('google-group')}">连接 Google 群组</a>。一半的问题都出在这一步。</li>
  <li>把版本（AAB）上传到该轨道并通过审核。没有已发布的版本，加入链接打不开。</li>
  <li>在 ACT Party 登记你的应用，从看板挑一个别人的应用开始测试。</li>
  <li>14 天后申请正式版 — 先读一读<a href="{g('production-form')}">那 9 个问题</a>。</li>
</ol>''',
            faq_h='常见问题',
            faq=[
                ('测试者必须连续 14 天每天打开应用吗？',
                 '不必。Google 看的是加入状态是否持续 14 天。实测 44 次中测试者平均只打开 8.5 天，审核通过。'),
                ('12 人里有人中途退出，要从头再来吗？',
                 '不用。留下的人天数照常累计，新补的测试者只需自己满 14 天。'),
                ('可以付钱给测试者吗？',
                 'Google 政策不禁止，但正式版申请表会问你测试者的使用方式与真实用户有何不同，付费加入很难解释。开发者互测没有这个问题。'),
                ('ACT Party 收费吗？',
                 '免费。开发者之间互相测试，没有需要收费的地方。'),
            ],
            cta=f'<b>ACT Party</b> 看板上随时有 20～40 个应用在找测试者。登记你的应用，挑一个开始就行。<a href="/">查看看板</a> · <a href="{STORE}">获取应用</a>',
        ),
        'zh-Hant': dict(
            title='Google Play 的 12 名測試者從哪裡來 — 通過 14 天封閉測試 | ACT Party',
            desc='新的開發者帳號必須有 12 名測試者加入封閉測試並保持 14 天才能發布。Google 沒有告訴你怎麼找到他們；這裡是找測試者的方法，以及開發者之間免費互測的方式。',
            h1='Google Play 的 12 名測試者去哪裡找',
            sub='新帳號遇到的第一道牆，以及翻過去的三條路',
            body=f'''
<p>自 2023 年 11 月起，新建的個人開發者帳號不能直接發布應用程式。必須先有
<b>12 名測試者加入封閉測試並保持 14 天</b>，正式版申請按鈕才會打開。
主控台裡只寫了條件，關於這 12 個人從哪裡來，一個字都沒有。</p>

<h2>Google 真正在數的是什麼</h2>
<p>不是測試者是否每天打開應用程式，而是<b>加入狀態是否持續了 14 天</b>。
對 44 次已完成的測試實測，測試者平均只在 14 天裡打開了 8.5 天，審核照樣通過。
詳細數字見<a href="{g('what-google-checks')}">Google 實際檢查什麼</a>和
<a href="{g('daily-opens-data')}">沒有人會連開 14 天</a>。</p>

<h2>找測試者的三條路</h2>
<ol class="steps">
  <li><b>找 12 個熟人</b> — 最快，但通常停在三四個人。請人保持加入狀態兩週，
  是個比想像中大的人情。</li>
  <li><b>付費測試服務</b> — 每次約 20～50 美元。加入狀態能保住，但沒人真的用你的應用程式。</li>
  <li><b>開發者之間互測</b> — 每週都有幾千個開發者撞上同一道牆。互相測試對方的應用程式，
  兩邊都湊夠 12 人。免費，而且對方也是開發者，會留下真實回饋。</li>
</ol>

<h2>互測為什麼容易散，怎麼解決</h2>
<p>通常的做法是在 Reddit 或 Discord 發文：「測我的，我也測你的」。但你不知道對方是否
真的每天打開，很多人幾天後就悄悄消失。<b>ACT Party</b> 替你管理這件事：打開對方的
應用程式，當天的打卡自動記錄，雙方進度都在看板上可見。誰也不需要相信誰。</p>

<h2>按順序做</h2>
<ol class="steps">
  <li>在 Play Console 建立封閉測試群組，並<a href="{g('google-group')}">連接 Google 群組</a>。一半的問題都出在這一步。</li>
  <li>把版本（AAB）上傳並通過審查。沒有已發布的版本，加入連結打不開。</li>
  <li>在 ACT Party 登記你的應用程式，從看板挑一個別人的應用程式開始測試。</li>
  <li>14 天後申請正式版 — 先讀一讀<a href="{g('production-form')}">那 9 個問題</a>。</li>
</ol>''',
            faq_h='常見問題',
            faq=[
                ('測試者必須連續 14 天每天打開應用程式嗎？',
                 '不必。Google 看的是加入狀態是否持續 14 天。實測 44 次中測試者平均只打開 8.5 天，審核通過。'),
                ('12 人裡有人中途退出，要從頭再來嗎？',
                 '不用。留下的人天數照常累計，新補的測試者只需自己滿 14 天。'),
                ('可以付錢給測試者嗎？',
                 'Google 政策不禁止，但正式版申請表會問你測試者的使用方式與真實使用者有何不同，付費加入很難解釋。開發者互測沒有這個問題。'),
                ('ACT Party 收費嗎？',
                 '免費。開發者之間互相測試，沒有需要收費的地方。'),
            ],
            cta=f'<b>ACT Party</b> 看板上隨時有 20～40 個應用程式在找測試者。登記你的應用程式，挑一個開始就行。<a href="/">查看看板</a> · <a href="{STORE}">取得應用程式</a>',
        ),
    }[lang]


from landing_14days import p_14days   # noqa: E402  (모듈 로드 뒤 import — 순환 방지)
from landing_find import p_find       # noqa: E402

PAGES = {
    'google-play-12-testers': p_12,
    'closed-testing-14-days': p_14days,
    'find-android-app-testers': p_find,
}


def main():
    written = []
    for slug, fn in PAGES.items():
        for lang in LANGS:
            p = fn(lang)
            out = os.path.join(BASE, *([] if lang == 'en' else [lang]), f'{slug}.html')
            os.makedirs(os.path.dirname(out), exist_ok=True)
            io.open(out, 'w', encoding='utf-8', newline='').write(render(slug, lang, p))
            written.append(path_of(slug, lang))
    io.open(os.path.join(BASE, 'landing_pages.json'), 'w', encoding='utf-8').write(
        json.dumps(written, ensure_ascii=False, indent=1))
    print(f'랜딩 {len(written)}개 생성')


if __name__ == '__main__':
    sys.exit(main())
