"""랜딩 3 — "how to find android app testers".
검색: how to find testers for android app / android beta testers / 안드로이드 앱 테스터 구하기

가장 넓은 검색어. 유료·지인·레딧·교환을 나란히 놓고 비교한다. 우리 쪽으로
몰지 않고 각각의 값을 그대로 적는다 — 그래야 글이 살아남고, 그래야 믿는다.
"""


def p_find(lang):
    from landing_build import guide, STORE
    g = lambda n: guide(lang, n)
    return {
        'ko': dict(
            title='안드로이드 앱 테스터 구하는 법 — 지인·유료·레딧·교환 비교 | ACT Party',
            desc='비공개 테스트 테스터를 구하는 네 가지 방법을 비용·속도·유지율로 비교합니다. 지인 부탁, 유료 서비스, 레딧 모집글, 개발자 교환. 각각 어디서 막히는지와 실제 수치.',
            h1='안드로이드 앱 테스터, 어떻게 구하나',
            sub='네 가지 방법을 비용·속도·유지율로 놓고 비교',
            body=f'''
<p>새 개발자 계정으로 앱을 내려면 <b>테스터 12명이 14일</b> 동안 비공개 테스트에
붙어 있어야 합니다. 방법은 크게 넷입니다. 각각 어디까지 가고 어디서 막히는지
그대로 적습니다.</p>

<h2>1. 지인에게 부탁</h2>
<p>제일 먼저 하는 방법이고, 대부분 3~4명에서 멈춥니다. "링크 눌러서 깔고 2주만
지우지 말아 줘"가 생각보다 큰 부탁이고, 그 사람들은 앱을 열지 않습니다.
비용 0, 속도 빠름, 유지율 낮음. 12명을 채운 사람을 거의 못 봤습니다.</p>

<h2>2. 유료 테스터 서비스</h2>
<p>건당 2~5만 원. 옵트인은 확실히 유지되고 손이 안 갑니다. 대신 실제로 앱을 쓰는
사람이 아니라서 피드백이 없고, 프로덕션 신청 설문에서 "테스터의 사용 방식이
실제 사용자와 같은가"를 물을 때 답이 궁색해집니다. 급하고 예산이 있으면 이
방법입니다.</p>

<h2>3. 레딧·디스코드 모집글</h2>
<p>r/AndroidAppTesters 같은 곳에 "내 앱 테스트해 주면 네 것도 해줄게"를 올립니다.
하루에 수십 개가 올라오고, 답은 오는데 <b>지키는 사람이 적습니다.</b> 상대가 정말
매일 여는지 알 수 없고, 며칠 뒤 조용히 사라지는 경우가 흔합니다. 비용 0,
속도 보통, 유지율은 운입니다.</p>

<h2>4. 개발자끼리 교환 — 기록이 남는 방식</h2>
<p>3번과 같은 교환인데, 앱이 대신 관리합니다. 상대 앱을 열면 그날 인증이 자동으로
기록되고, 서로의 진행이 보드에 보입니다. 사라지는 사람은 바로 드러나고,
끝까지 한 사람은 완주 기록이 쌓입니다. 끝난 교환 44건 기준 테스터는 14일 중
평균 8.8일을 열었고 심사는 통과했습니다. 비용 0, 속도 보통, 유지율 확인 가능.</p>

<h2>한눈에</h2>
<ol class="steps">
  <li><b>지인</b> — 빠르지만 12명까지 안 감</li>
  <li><b>유료</b> — 확실하지만 돈이 들고 설문에서 설명해야 함</li>
  <li><b>레딧 모집</b> — 무료지만 상대를 믿어야 함</li>
  <li><b>기록되는 교환</b> — 무료이고 믿을 필요가 없음. 대신 내 시간을 내서 남의 앱도 열어야 함</li>
</ol>

<h2>어느 방법이든 먼저 할 것</h2>
<p>테스터가 들어올 문이 열려 있어야 합니다. 구글 그룹 공개 설정, 트랙에 올라간
버전, 옵트인 링크. 이 셋 중 하나라도 빠지면 어떤 방법으로 사람을 구해도 첫날에
막힙니다. <a href="{g('google-group')}">그룹 만들고 연결하기</a>부터 보세요.
12명을 채우는 것 자체가 궁금하면
<a href="/{'' if lang == 'en' else lang + '/'}google-play-12-testers.html">테스터 12명, 어디서 구하나</a>에
더 자세히 있습니다.</p>''',
            faq_h='자주 묻는 질문',
            faq=[
                ('테스터에게 돈을 주면 문제가 되나요?', '구글 정책 위반은 아닙니다. 다만 프로덕션 신청 설문이 테스터의 사용 방식이 실제 사용자와 어떻게 다른지 묻기 때문에, 유료 옵트인은 그 답을 쓰기 어렵습니다.'),
                ('테스터가 12명보다 많아도 되나요?', '됩니다. 오히려 13~14명이 안전합니다. 한 명이 중간에 빠져 11명이 되는 날은 세지 않습니다.'),
                ('테스터가 앱을 매일 열어야 하나요?', '구글은 옵트인 기간을 세지, 연 횟수를 세지 않습니다. 실측 48건에서 평균 8.8일만 열었고 통과했습니다.'),
                ('교환하면 나도 남의 앱을 14일 열어야 하나요?', '네. 그게 교환입니다. 상대가 내 앱을 여는 만큼 나도 엽니다. 하루 한 번, 몇 초면 됩니다.'),
            ],
            cta=f'<b>ACT Party</b> 보드에는 테스터를 찾는 앱이 항상 20~40개 있습니다. 내 앱을 등록하고 하나 골라 시작하면 됩니다. <a href="/">보드 보기</a> · <a href="{STORE}">앱 받기</a>',
        ),
        'en': dict(
            title='How to find testers for your Android app — friends, paid, Reddit, trading compared | ACT Party',
            desc="Four ways to get closed-test testers, compared on cost, speed and how many actually stay: friends, paid services, Reddit posts, developer trades. Where each one breaks, with real numbers.",
            h1='How to find testers for an Android app',
            sub='Four ways, compared on cost, speed and who actually stays',
            body=f'''
<p>A new developer account cannot publish until <b>12 testers stay in a closed
test for 14 days</b>. There are four ways to get them. Here is how far each one
goes and where it breaks.</p>

<h2>1. Friends and family</h2>
<p>Everyone starts here and most stop at three or four. "Tap this link, install
it and don't delete it for two weeks" is a bigger ask than it sounds, and those
people never open the app. Cost zero, fast, poor retention. Almost nobody
reaches 12 this way.</p>

<h2>2. Paid tester services</h2>
<p>Roughly $20–50 per run. Opt-ins hold and it takes no effort. But nobody
actually uses the app, so there is no feedback, and when the production form
asks whether your testers' usage matches real users, the honest answer is
awkward. If you are in a hurry and have the budget, this works.</p>

<h2>3. Reddit and Discord posts</h2>
<p>"Test mine and I'll test yours" on r/AndroidAppTesters and similar. Dozens of
posts a day, replies do come, but <b>few people follow through.</b> You cannot
tell whether the other side really opens your app, and many go quiet after a
few days. Cost zero, medium speed, retention is luck.</p>

<h2>4. Trading with a record</h2>
<p>The same trade as #3, but an app runs it. Opening the other developer's app
records that day's check-in automatically and both sides' progress sits on a
board. Whoever disappears is visible at once; whoever finishes builds a record.
Across 48 finished trades testers opened the app on 8.8 of 14 days and reviews
passed. Cost zero, medium speed, retention you can see.</p>

<h2>At a glance</h2>
<ol class="steps">
  <li><b>Friends</b> — fast, rarely reaches 12</li>
  <li><b>Paid</b> — reliable, costs money, has to be explained on the form</li>
  <li><b>Reddit</b> — free, requires trusting strangers</li>
  <li><b>Recorded trade</b> — free, no trust needed, but you open other apps too</li>
</ol>

<h2>Whichever you pick, do this first</h2>
<p>The door has to be open before anyone can walk in: a Google Group set to
public, a build published on the track, a working opt-in link. Miss one and every
tester you find gets stuck on day one. Start with
<a href="{g('google-group')}">creating and connecting the group</a>. For the
12-tester count itself, see
<a href="/{'' if lang == 'en' else lang + '/'}google-play-12-testers.html">Where to find 12 testers</a>.</p>''',
            faq_h='Questions people ask',
            faq=[
                ('Is paying testers against the rules?', "Not against Google policy. But the production form asks how your testers' usage differs from real users, and paid opt-ins are hard to explain there."),
                ('Can I have more than 12 testers?', 'Yes, and 13 or 14 is safer. A day when someone drops out and you are at 11 does not count.'),
                ('Do testers have to open the app every day?', 'Google counts opt-in time, not opens. In 44 measured trades testers opened the app on 8.5 days on average and passed.'),
                ('If I trade, do I have to open their app for 14 days too?', "Yes, that is the trade. You open theirs as much as they open yours — once a day, a few seconds."),
            ],
            cta=f'<b>ACT Party</b> usually has 20–40 apps looking for testers. Register yours, pick one, start. <a href="/">See the board</a> · <a href="{STORE}">Get the app</a>',
        ),
        'ja': dict(
            title='Androidアプリのテスターの集め方 — 知人・有料・Reddit・交換を比較 | ACT Party',
            desc='非公開テストのテスターを集める四つの方法を、費用・速さ・定着率で比較します。知人に頼む、有料サービス、Redditの募集、開発者同士の交換。それぞれどこで詰まるか、実際の数字つき。',
            h1='Androidアプリのテスターはどう集めるか',
            sub='四つの方法を費用・速さ・定着率で並べて比較',
            body=f'''
<p>新しいデベロッパーアカウントでアプリを出すには、<b>テスター12人が14日間</b>
非公開テストに残っている必要があります。方法は大きく四つ。それぞれどこまで
行けて、どこで詰まるかをそのまま書きます。</p>

<h2>1. 知人に頼む</h2>
<p>誰もが最初にやり、たいてい3〜4人で止まります。「リンクを押して入れて、2週間
消さないで」は思うより大きな頼みで、その人たちはアプリを開きません。
費用ゼロ、速い、定着は低い。この方法で12人に届いた人をほとんど見ません。</p>

<h2>2. 有料テスターサービス</h2>
<p>1回2〜5千円ほど。オプトインは確実に維持され、手間はかかりません。ただ実際に
アプリを使う人ではないのでフィードバックがなく、製品版申請の設問で「テスターの
使い方が実際のユーザーと同じか」を聞かれると答えに困ります。急いでいて予算が
あるならこの方法です。</p>

<h2>3. Reddit・Discordの募集</h2>
<p>r/AndroidAppTesters などに「私のをテストしてくれたらあなたのも」と書きます。
一日に数十件上がり、返事は来ますが<b>守る人が少ない</b>。相手が本当に毎日開いて
いるか分からず、数日で静かに消えることが多い。費用ゼロ、速さは普通、定着は運です。</p>

<h2>4. 記録が残る交換</h2>
<p>3と同じ交換ですが、アプリが代わりに管理します。相手のアプリを開くとその日の
チェックインが自動で記録され、双方の進み具合がボードに見えます。消える人は
すぐ分かり、最後までやった人には完走の記録が積み上がります。完了した交換48件で
テスターは14日のうち平均8.5日開き、審査は通りました。費用ゼロ、速さは普通、
定着は確認できます。</p>

<h2>ひと目で</h2>
<ol class="steps">
  <li><b>知人</b> — 速いが12人に届きにくい</li>
  <li><b>有料</b> — 確実だが費用がかかり、設問で説明が要る</li>
  <li><b>Reddit募集</b> — 無料だが相手を信じるしかない</li>
  <li><b>記録される交換</b> — 無料で信じる必要がない。代わりに自分も他人のアプリを開く</li>
</ol>

<h2>どの方法でも先にやること</h2>
<p>テスターが入る扉が開いていなければなりません。Googleグループの公開設定、
トラックに上がったビルド、開くオプトインリンク。この三つのどれかが欠けると、
どんな方法で集めても初日に詰まります。まず
<a href="{g('google-group')}">グループを作って連携する</a>から。12人を集めること
自体は
<a href="/{'' if lang == 'en' else lang + '/'}google-play-12-testers.html">テスター12人はどこで集めるか</a>に詳しくあります。</p>''',
            faq_h='よくある質問',
            faq=[
                ('テスターにお金を払うと問題になりますか？', 'Googleの規約違反ではありません。ただ製品版申請の設問がテスターの使い方と実際のユーザーの違いを聞くので、有料オプトインはそこで説明しにくい。'),
                ('テスターは12人より多くてもいいですか？', 'はい。むしろ13〜14人が安全です。誰かが途中で抜けて11人になった日は数えられません。'),
                ('テスターは毎日アプリを開く必要がありますか？', 'Googleはオプトイン期間を数え、開いた回数は数えません。実測44件で平均8.5日しか開かず、通過しました。'),
                ('交換すると自分も相手のアプリを14日開くのですか？', 'はい、それが交換です。相手が自分のアプリを開く分だけ自分も開きます。一日一回、数秒です。'),
            ],
            cta=f'<b>ACT Party</b> のボードにはテスターを探すアプリが常に20〜40個あります。自分のアプリを登録し、一つ選んで始めるだけです。<a href="/">ボードを見る</a> · <a href="{STORE}">アプリを入手</a>',
        ),
        'zh-Hans': dict(
            title='怎么给 Android 应用找测试者 — 熟人、付费、Reddit、互测对比 | ACT Party',
            desc='找封闭测试者的四种方式，按成本、速度、留存率对比：找熟人、付费服务、Reddit 发帖、开发者互测。每种在哪一步会断，附真实数据。',
            h1='Android 应用的测试者怎么找',
            sub='四种方式，按成本、速度和真正留下来的人数对比',
            body=f'''
<p>新开发者账号要发布应用，必须有 <b>12 名测试者在封闭测试里待满 14 天</b>。
方法大体四种。每种能走多远、在哪断掉，照实写。</p>

<h2>1. 找熟人</h2>
<p>所有人都从这里开始，大多停在三四个人。"点这个链接装上，两周别删"是个比想象中
大的人情，而且这些人不会打开应用。零成本、快、留存差。靠这个凑到 12 人的几乎没见过。</p>

<h2>2. 付费测试服务</h2>
<p>每次约 20～50 美元。加入状态稳，不费力。但没人真的用你的应用，没有反馈；
正式版申请表问"测试者的使用方式是否与真实用户一致"时，不好回答。急、有预算，可以用。</p>

<h2>3. Reddit、Discord 发帖</h2>
<p>在 r/AndroidAppTesters 之类的地方发"测我的，我也测你的"。每天几十条，回复是有的，
但<b>说到做到的少</b>。你不知道对方是否真的每天打开，很多人几天后就没声了。
零成本、速度一般、留存靠运气。</p>

<h2>4. 有记录的互测</h2>
<p>和第 3 种一样是互测，但由应用来管。打开对方的应用，当天打卡自动记录，双方进度都在看板上。
谁消失了一眼就看到，谁做完了有完成记录。44 次已完成的互测里，测试者平均在 14 天中打开 8.8 天，
审核通过。零成本、速度一般、留存看得见。</p>

<h2>一眼看完</h2>
<ol class="steps">
  <li><b>熟人</b> — 快，但很难到 12 人</li>
  <li><b>付费</b> — 稳，但花钱，申请表上要解释</li>
  <li><b>Reddit 发帖</b> — 免费，但得信陌生人</li>
  <li><b>有记录的互测</b> — 免费、不用信任，但你也得打开别人的应用</li>
</ol>

<h2>不管选哪种，先做这个</h2>
<p>门得先开着：Google 群组设为公开、轨道上有已发布的版本、加入链接能打开。
缺一个，无论怎么找来的人都会卡在第一天。先看
<a href="{g('google-group')}">建群并连接</a>。至于怎么凑够 12 人，
<a href="/{'' if lang == 'en' else lang + '/'}google-play-12-testers.html">12 名测试者去哪里找</a>写得更细。</p>''',
            faq_h='常见问题',
            faq=[
                ('付钱给测试者违规吗？', '不违反 Google 政策。但正式版申请表会问测试者的使用方式与真实用户有何不同，付费加入在那里很难解释。'),
                ('测试者可以超过 12 人吗？', '可以，13～14 人更稳。有人中途退出只剩 11 人的那天不计入。'),
                ('测试者必须每天打开应用吗？', 'Google 数的是加入时长，不是打开次数。实测 48 次平均只打开 8.8 天，都通过了。'),
                ('互测的话我也得打开对方的应用 14 天？', '是的，这就是互测。对方打开你的多少，你也打开对方的多少。一天一次，几秒钟。'),
            ],
            cta=f'<b>ACT Party</b> 看板上随时有 20～40 个应用在找测试者。登记你的应用，挑一个开始。<a href="/">查看看板</a> · <a href="{STORE}">获取应用</a>',
        ),
        'zh-Hant': dict(
            title='怎麼給 Android 應用程式找測試者 — 熟人、付費、Reddit、互測比較 | ACT Party',
            desc='找封閉測試者的四種方式，按成本、速度、留存率比較：找熟人、付費服務、Reddit 發文、開發者互測。每種在哪一步會斷，附真實數據。',
            h1='Android 應用程式的測試者怎麼找',
            sub='四種方式，按成本、速度和真正留下來的人數比較',
            body=f'''
<p>新開發者帳號要發布應用程式，必須有 <b>12 名測試者在封閉測試裡待滿 14 天</b>。
方法大體四種。每種能走多遠、在哪斷掉，照實寫。</p>

<h2>1. 找熟人</h2>
<p>所有人都從這裡開始，大多停在三四個人。「點這個連結裝上，兩週別刪」是個比想像中
大的人情，而且這些人不會打開應用程式。零成本、快、留存差。靠這個湊到 12 人的幾乎沒見過。</p>

<h2>2. 付費測試服務</h2>
<p>每次約 20～50 美元。加入狀態穩，不費力。但沒人真的用你的應用程式，沒有回饋；
正式版申請表問「測試者的使用方式是否與真實使用者一致」時，不好回答。急、有預算，可以用。</p>

<h2>3. Reddit、Discord 發文</h2>
<p>在 r/AndroidAppTesters 之類的地方發「測我的，我也測你的」。每天幾十條，回覆是有的，
但<b>說到做到的少</b>。你不知道對方是否真的每天打開，很多人幾天後就沒聲了。
零成本、速度一般、留存靠運氣。</p>

<h2>4. 有記錄的互測</h2>
<p>和第 3 種一樣是互測，但由應用程式來管。打開對方的應用程式，當天打卡自動記錄，雙方進度都在看板上。
誰消失了一眼就看到，誰做完了有完成記錄。44 次已完成的互測裡，測試者平均在 14 天中打開 8.8 天，
審核通過。零成本、速度一般、留存看得見。</p>

<h2>一眼看完</h2>
<ol class="steps">
  <li><b>熟人</b> — 快，但很難到 12 人</li>
  <li><b>付費</b> — 穩，但花錢，申請表上要解釋</li>
  <li><b>Reddit 發文</b> — 免費，但得信陌生人</li>
  <li><b>有記錄的互測</b> — 免費、不用信任，但你也得打開別人的應用程式</li>
</ol>

<h2>不管選哪種，先做這個</h2>
<p>門得先開著：Google 群組設為公開、測試群組上有已發布的版本、加入連結能打開。
缺一個，無論怎麼找來的人都會卡在第一天。先看
<a href="{g('google-group')}">建群並連接</a>。至於怎麼湊夠 12 人，
<a href="/{'' if lang == 'en' else lang + '/'}google-play-12-testers.html">12 名測試者去哪裡找</a>寫得更細。</p>''',
            faq_h='常見問題',
            faq=[
                ('付錢給測試者違規嗎？', '不違反 Google 政策。但正式版申請表會問測試者的使用方式與真實使用者有何不同，付費加入在那裡很難解釋。'),
                ('測試者可以超過 12 人嗎？', '可以，13～14 人更穩。有人中途退出只剩 11 人的那天不計入。'),
                ('測試者必須每天打開應用程式嗎？', 'Google 數的是加入時長，不是打開次數。實測 48 次平均只打開 8.8 天，都通過了。'),
                ('互測的話我也得打開對方的應用程式 14 天？', '是的，這就是互測。對方打開你的多少，你也打開對方的多少。一天一次，幾秒鐘。'),
            ],
            cta=f'<b>ACT Party</b> 看板上隨時有 20～40 個應用程式在找測試者。登記你的應用程式，挑一個開始。<a href="/">查看看板</a> · <a href="{STORE}">取得應用程式</a>',
        ),
    }[lang]
