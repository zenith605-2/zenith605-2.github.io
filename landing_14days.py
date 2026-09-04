"""랜딩 2 — "closed testing 14 days".
검색: google play closed testing 14 days / 비공개 테스트 14일 / 非公開テスト 14日

콘솔에서 "14일" 을 처음 본 사람이 치는 검색어. 12명 페이지가 '사람을 어디서
구하나' 라면, 이 페이지는 '그 14일 동안 실제로 무슨 일이 일어나나' 다.
"""


def p_14days(lang):
    from landing_build import guide, STORE   # 모듈 로드 뒤에 부르므로 순환 아님
    g = lambda n: guide(lang, n)
    return {
        'ko': dict(
            title='구글 플레이 비공개 테스트 14일 — 실제로 무슨 일이 일어나나 | ACT Party',
            desc='테스터 12명이 14일을 채워야 출시할 수 있습니다. 구글이 세는 것, 테스터가 실제로 앱을 여는 날수, 며칠째에 사람이 빠지는지, 14일 뒤 신청 요령까지. 끝난 테스트 44건 실측.',
            h1='비공개 테스트 14일, 실제로는 이렇게 흘러갑니다',
            sub='끝난 테스트 44건을 날짜별로 기록한 결과',
            body=f'''
<p>구글 플레이 콘솔은 새 개발자 계정에 <b>테스터 12명, 14일</b>을 요구합니다.
조건은 한 줄인데, 그 14일 동안 무엇을 해야 하고 무엇이 세어지는지는 어디에도
없습니다. 개발자끼리 테스트를 교환하는 보드에서 끝난 테스트 44건의 매일 기록을
모았습니다.</p>

<h2>구글이 세는 것은 "옵트인 기간"입니다</h2>
<p>테스터가 앱을 매일 열었는지가 아닙니다. 테스터가 <b>옵트인한 상태로 14일이
지났는지</b>입니다. 그래서 앱을 며칠 안 열어도 심사에는 영향이 없습니다.
반대로 옵트인을 취소하면 그 사람의 시계는 멈춥니다. 자세한 근거는
<a href="{g('what-google-checks')}">구글이 실제로 보는 것</a>에 있습니다.</p>

<h2>테스터는 14일 중 8.5일만 엽니다</h2>
<p>44건 평균입니다. 14일을 전부 연 테스터는 44명 중 2명뿐이었습니다.
빠지는 시점은 끝 무렵이 아니라 <b>2~3일째</b>입니다. 처음 호기심으로 두어 번
열고, 그다음 잊습니다. 숫자 전체는
<a href="{g('daily-opens-data')}">14일 내내 앱을 여는 사람은 없어요</a>에
있습니다.</p>

<h2>날짜별로 보면</h2>
<ol class="steps">
  <li><b>1일째</b> — 옵트인·설치. 여기서 절반이 막힙니다. 링크가 안 열리거나,
  그룹 가입이 안 되거나, 트랙에 버전이 없거나. <a href="{g('google-group')}">그룹 설정 가이드</a>를 먼저 보세요.</li>
  <li><b>2~3일째</b> — 이탈이 가장 많은 구간. 테스터가 앱을 열 이유가 없으면 여기서 사라집니다.</li>
  <li><b>4~13일째</b> — 조용한 구간. 옵트인만 유지되면 심사 요건은 채워집니다.</li>
  <li><b>14일째</b> — 프로덕션 신청 버튼이 열립니다. 바로 누르지 말고 <a href="{g('production-form')}">설문 9문항</a>을 먼저 읽으세요. 두 문항이 승인을 가릅니다.</li>
</ol>

<h2>중간에 사람이 빠지면</h2>
<p>처음부터 다시가 아닙니다. 남은 사람의 날짜는 그대로 쌓이고, 새로 들어온
테스터만 자기 14일을 채우면 됩니다. 다만 12명 아래로 떨어진 기간은 세지
않으므로, 13~14명을 두는 편이 안전합니다. 왜 빠지는지는
<a href="{g('why-testers-drop')}">테스터는 왜 사라지나</a>에 정리했습니다.</p>

<h2>14일을 짧게 느끼는 법</h2>
<p>테스터가 매일 앱을 여는 걸 사람이 확인하려면 스크린샷을 주고받아야 하고,
그게 14일이면 다들 지칩니다. <b>ACT Party</b>는 상대 앱을 열면 그날 인증이
자동으로 기록됩니다. 개발자는 누가 며칠 열었는지 보드에서 보고, 테스터는
아무것도 보고할 필요가 없습니다.</p>''',
            faq_h='자주 묻는 질문',
            faq=[
                ('14일은 언제부터 세나요?', '테스터마다 옵트인한 날부터 따로 셉니다. 12명이 같은 날 들어올 필요는 없지만, 12명이 동시에 옵트인 상태인 기간이 14일 있어야 합니다.'),
                ('테스터가 앱을 안 열면 심사에 떨어지나요?', '아닙니다. 구글은 옵트인 기간을 봅니다. 실측 44건에서 평균 8.5일만 열었고 통과했습니다. 다만 설문에서 테스터 참여도를 물으니 아예 안 여는 건 좋지 않습니다.'),
                ('14일이 지났는데 버튼이 안 열려요', '12명이 동시에 옵트인된 상태가 14일 연속이었는지 확인하세요. 중간에 한 명이라도 빠져 11명이 된 날은 세지 않습니다.'),
                ('내부 테스트로도 되나요?', '아닙니다. 비공개 테스트(Closed testing) 트랙이어야 합니다. 내부 테스트는 조건에 포함되지 않습니다.'),
            ],
            cta=f'<b>ACT Party</b>는 개발자끼리 앱을 교환해 테스트하고, 매일 열었는지를 대신 기록합니다. 무료입니다. <a href="/">보드 보기</a> · <a href="{STORE}">앱 받기</a>',
        ),
        'en': dict(
            title='Google Play closed testing: what the 14 days actually look like | ACT Party',
            desc='12 testers must stay opted in for 14 days before you can publish. What Google counts, how many days testers really open the app, when people drop out, and how to apply on day 14. From 44 finished tests.',
            h1='The 14 days of closed testing, as they really happen',
            sub='Daily records from 44 finished tests',
            body=f'''
<p>Google Play Console asks a new developer account for <b>12 testers, 14 days</b>.
One line of rules, and nothing about what to do during those days or what is
actually being counted. On a board where developers trade tests, we kept the
daily record of 44 finished runs.</p>

<h2>Google counts opt-in time, not opens</h2>
<p>The question is not whether a tester opened the app every day. It is whether
they <b>stayed opted in for 14 days</b>. Skipping days does not hurt the review;
leaving the test stops that person's clock. The evidence is in
<a href="{g('what-google-checks')}">What Google actually checks</a>.</p>

<h2>Testers open the app on 8.5 of 14 days</h2>
<p>That is the average across 44 runs. Only 2 of 44 testers opened it every
single day. The drop-off comes early — <b>day two or three</b> — not at the end.
People open it a couple of times out of curiosity and then forget. Full numbers:
<a href="{g('daily-opens-data')}">Nobody opens your app all 14 days</a>.</p>

<h2>Day by day</h2>
<ol class="steps">
  <li><b>Day 1</b> — opt-in and install. Half of all problems live here: a link
  that opens nothing, a group nobody can join, a track with no build. Read the
  <a href="{g('google-group')}">Google Group guide</a> first.</li>
  <li><b>Days 2–3</b> — the biggest drop-off. A tester with no reason to open the app disappears here.</li>
  <li><b>Days 4–13</b> — quiet. As long as opt-ins hold, the requirement is being met.</li>
  <li><b>Day 14</b> — the production button unlocks. Don't press it yet: read
  <a href="{g('production-form')}">the 9 questions</a>. Two of them decide the outcome.</li>
</ol>

<h2>If someone drops out</h2>
<p>You do not start over. The others keep their days; a replacement only has to
complete their own 14. But days when you are below 12 do not count, so 13 or 14
testers is the safe number. Why they leave is in
<a href="{g('why-testers-drop')}">Why testers disappear</a>.</p>

<h2>Making the 14 days feel short</h2>
<p>Checking by hand whether testers open the app means trading screenshots for
two weeks, and everyone tires of that. With <b>ACT Party</b> opening the other
app records that day's check-in automatically. The developer sees who opened
what on the board; the tester reports nothing.</p>''',
            faq_h='Questions people ask',
            faq=[
                ('When does the 14-day clock start?', "Per tester, from their opt-in. The 12 don't have to join on the same day, but there must be a 14-day stretch with 12 opted in at once."),
                ("Do I fail review if testers don't open the app?", 'No. Google counts opt-in time. In 44 measured runs testers averaged 8.5 open days and passed. The production form does ask about engagement, so zero opens is still a bad look.'),
                ("It's been 14 days and the button is still locked", 'Check that 12 were opted in simultaneously for 14 consecutive days. A day where one person left and you were at 11 does not count.'),
                ('Does internal testing count?', 'No. It has to be the Closed testing track. Internal testing is outside the requirement.'),
            ],
            cta=f'<b>ACT Party</b> lets developers trade tests and records the daily opens for you. Free. <a href="/">See the board</a> · <a href="{STORE}">Get the app</a>',
        ),
        'ja': dict(
            title='Google Play 非公開テストの14日間 — 実際に何が起きるか | ACT Party',
            desc='テスター12人が14日間オプトインを維持しないと公開できません。Googleが数えるもの、テスターが実際にアプリを開く日数、何日目に人が抜けるか、14日後の申請のコツ。完了テスト44件の実測。',
            h1='非公開テストの14日間、実際はこう流れます',
            sub='完了したテスト44件の日次記録',
            body=f'''
<p>Google Play Console は新しいデベロッパーアカウントに<b>テスター12人、14日間</b>を
求めます。条件は一行ですが、その14日間に何をすべきで何が数えられているかは
どこにも書かれていません。開発者同士がテストを交換するボードで、完了した
44件の毎日の記録を集めました。</p>

<h2>Googleが数えるのは「オプトイン期間」です</h2>
<p>テスターが毎日アプリを開いたかではなく、<b>オプトインしたまま14日が経ったか</b>
です。数日開かなくても審査には影響しません。逆にオプトインを外すとその人の
時計は止まります。根拠は
<a href="{g('what-google-checks')}">Googleが実際に見ているもの</a>にあります。</p>

<h2>テスターが開くのは14日のうち8.5日</h2>
<p>44件の平均です。14日すべて開いたテスターは44人中2人だけでした。抜けるのは
終盤ではなく<b>2〜3日目</b>。最初は好奇心で二、三回開き、そのあと忘れます。
数字の全体は
<a href="{g('daily-opens-data')}">14日間ずっと開く人はいません</a>にあります。</p>

<h2>日ごとに見ると</h2>
<ol class="steps">
  <li><b>1日目</b> — オプトインとインストール。問題の半分はここです。リンクが開かない、
  グループに参加できない、トラックにビルドがない。先に
  <a href="{g('google-group')}">Googleグループのガイド</a>を読んでください。</li>
  <li><b>2〜3日目</b> — 離脱が最も多い区間。開く理由のないテスターはここで消えます。</li>
  <li><b>4〜13日目</b> — 静かな区間。オプトインが維持されていれば要件は満たされています。</li>
  <li><b>14日目</b> — 製品版の申請ボタンが開きます。すぐ押さず、
  <a href="{g('production-form')}">9つの設問</a>を先に読んでください。二つの設問が結果を分けます。</li>
</ol>

<h2>途中で人が抜けたら</h2>
<p>最初からやり直しではありません。残った人の日数はそのまま積み上がり、新しい
テスターは自分の14日を満たせばいい。ただし12人を下回った日は数えないので、
13〜14人にしておく方が安全です。なぜ抜けるかは
<a href="{g('why-testers-drop')}">テスターが消える理由</a>にまとめました。</p>

<h2>14日を短く感じる方法</h2>
<p>テスターが毎日開いたかを人が確認するにはスクリーンショットのやり取りが要り、
14日続くと全員が疲れます。<b>ACT Party</b>では相手のアプリを開くとその日の
チェックインが自動で記録されます。開発者は誰が何日開いたかをボードで見て、
テスターは何も報告しません。</p>''',
            faq_h='よくある質問',
            faq=[
                ('14日はいつから数えますか？', 'テスターごとにオプトインした日から数えます。12人が同じ日に入る必要はありませんが、12人が同時にオプトイン状態である期間が14日必要です。'),
                ('テスターがアプリを開かないと審査に落ちますか？', 'いいえ。Googleはオプトイン期間を見ます。実測44件で平均8.5日しか開かず、通過しました。ただし設問で参加度を聞かれるので、まったく開かないのは避けたいところです。'),
                ('14日経ったのにボタンが開きません', '12人が同時にオプトイン状態で14日連続だったか確認してください。誰か一人が抜けて11人になった日は数えられません。'),
                ('内部テストでもいいですか？', 'いいえ。非公開テスト（Closed testing）トラックである必要があります。内部テストは条件に含まれません。'),
            ],
            cta=f'<b>ACT Party</b> は開発者同士でアプリを交換してテストし、毎日開いたかを代わりに記録します。無料です。<a href="/">ボードを見る</a> · <a href="{STORE}">アプリを入手</a>',
        ),
        'zh-Hans': dict(
            title='Google Play 封闭测试的 14 天 — 实际会发生什么 | ACT Party',
            desc='12 名测试者必须保持加入状态 14 天才能发布。Google 到底在数什么、测试者真正打开应用的天数、人会在第几天流失、第 14 天怎么申请。来自 44 次已完成的测试。',
            h1='封闭测试的 14 天，实际是这样过的',
            sub='44 次已完成测试的逐日记录',
            body=f'''
<p>Google Play Console 对新开发者账号的要求是<b>12 名测试者、14 天</b>。
规则只有一行，这 14 天里该做什么、到底在数什么，哪里都没写。
在一个开发者互测的看板上，我们记录了 44 次已完成测试的每日数据。</p>

<h2>Google 数的是「加入时长」，不是打开次数</h2>
<p>问题不在于测试者是否每天打开应用，而在于他是否<b>保持加入状态满 14 天</b>。
几天不打开不影响审核；退出测试则那个人的计时停止。依据见
<a href="{g('what-google-checks')}">Google 实际检查什么</a>。</p>

<h2>测试者在 14 天里只打开 8.5 天</h2>
<p>这是 44 次的平均值。14 天全部打开的测试者，44 人里只有 2 个。流失不在最后，
而在<b>第 2～3 天</b>。人们出于好奇打开两三次，然后就忘了。完整数字见
<a href="{g('daily-opens-data')}">没有人会连开 14 天</a>。</p>

<h2>按天来看</h2>
<ol class="steps">
  <li><b>第 1 天</b> — 加入与安装。一半的问题出在这里：链接打不开、群组进不去、轨道上没有版本。
  先看<a href="{g('google-group')}">Google 群组指南</a>。</li>
  <li><b>第 2～3 天</b> — 流失最多的区间。没有理由打开应用的测试者会在这里消失。</li>
  <li><b>第 4～13 天</b> — 平静期。只要加入状态保持，要求就在被满足。</li>
  <li><b>第 14 天</b> — 正式版申请按钮打开。先别按，先读<a href="{g('production-form')}">那 9 个问题</a>。其中两个决定结果。</li>
</ol>

<h2>中途有人退出怎么办</h2>
<p>不用从头再来。其他人的天数照常累计，补进来的人只需满自己的 14 天。
但少于 12 人的那些天不计入，所以留 13～14 人更稳妥。他们为什么会走，见
<a href="{g('why-testers-drop')}">测试者为什么会消失</a>。</p>

<h2>让 14 天变短的办法</h2>
<p>人工确认测试者每天有没有打开，意味着两周里来回发截图，谁都会累。
用 <b>ACT Party</b>，打开对方的应用就自动记下当天打卡。开发者在看板上看到谁打开了几天，
测试者什么都不用汇报。</p>''',
            faq_h='常见问题',
            faq=[
                ('14 天从什么时候开始算？', '按每个测试者各自加入的那天算。12 个人不必同一天加入，但必须有连续 14 天同时有 12 人处于加入状态。'),
                ('测试者不打开应用会审核不过吗？', '不会。Google 看的是加入时长。实测 44 次平均只打开 8.5 天，都通过了。不过申请表会问参与度，完全不打开也不好看。'),
                ('已经 14 天了按钮还是锁着', '检查是否连续 14 天都有 12 人同时处于加入状态。哪天有人退出只剩 11 人，那天就不算。'),
                ('内部测试算吗？', '不算。必须是封闭测试（Closed testing）轨道。内部测试不在要求之内。'),
            ],
            cta=f'<b>ACT Party</b> 让开发者互相测试应用，并替你记录每天的打开情况。免费。<a href="/">查看看板</a> · <a href="{STORE}">获取应用</a>',
        ),
        'zh-Hant': dict(
            title='Google Play 封閉測試的 14 天 — 實際會發生什麼 | ACT Party',
            desc='12 名測試者必須保持加入狀態 14 天才能發布。Google 到底在數什麼、測試者真正打開應用程式的天數、人會在第幾天流失、第 14 天怎麼申請。來自 44 次已完成的測試。',
            h1='封閉測試的 14 天，實際是這樣過的',
            sub='44 次已完成測試的逐日記錄',
            body=f'''
<p>Google Play Console 對新開發者帳號的要求是<b>12 名測試者、14 天</b>。
規則只有一行，這 14 天裡該做什麼、到底在數什麼，哪裡都沒寫。
在一個開發者互測的看板上，我們記錄了 44 次已完成測試的每日資料。</p>

<h2>Google 數的是「加入時長」，不是打開次數</h2>
<p>問題不在於測試者是否每天打開應用程式，而在於他是否<b>保持加入狀態滿 14 天</b>。
幾天不打開不影響審核；退出測試則那個人的計時停止。依據見
<a href="{g('what-google-checks')}">Google 實際檢查什麼</a>。</p>

<h2>測試者在 14 天裡只打開 8.5 天</h2>
<p>這是 44 次的平均值。14 天全部打開的測試者，44 人裡只有 2 個。流失不在最後，
而在<b>第 2～3 天</b>。人們出於好奇打開兩三次，然後就忘了。完整數字見
<a href="{g('daily-opens-data')}">沒有人會連開 14 天</a>。</p>

<h2>按天來看</h2>
<ol class="steps">
  <li><b>第 1 天</b> — 加入與安裝。一半的問題出在這裡：連結打不開、群組進不去、測試群組上沒有版本。
  先看<a href="{g('google-group')}">Google 群組指南</a>。</li>
  <li><b>第 2～3 天</b> — 流失最多的區間。沒有理由打開應用程式的測試者會在這裡消失。</li>
  <li><b>第 4～13 天</b> — 平靜期。只要加入狀態保持，要求就在被滿足。</li>
  <li><b>第 14 天</b> — 正式版申請按鈕打開。先別按，先讀<a href="{g('production-form')}">那 9 個問題</a>。其中兩個決定結果。</li>
</ol>

<h2>中途有人退出怎麼辦</h2>
<p>不用從頭再來。其他人的天數照常累計，補進來的人只需滿自己的 14 天。
但少於 12 人的那些天不計入，所以留 13～14 人更穩妥。他們為什麼會走，見
<a href="{g('why-testers-drop')}">測試者為什麼會消失</a>。</p>

<h2>讓 14 天變短的辦法</h2>
<p>人工確認測試者每天有沒有打開，意味著兩週裡來回傳截圖，誰都會累。
用 <b>ACT Party</b>，打開對方的應用程式就自動記下當天打卡。開發者在看板上看到誰打開了幾天，
測試者什麼都不用回報。</p>''',
            faq_h='常見問題',
            faq=[
                ('14 天從什麼時候開始算？', '按每個測試者各自加入的那天算。12 個人不必同一天加入，但必須有連續 14 天同時有 12 人處於加入狀態。'),
                ('測試者不打開應用程式會審核不過嗎？', '不會。Google 看的是加入時長。實測 44 次平均只打開 8.5 天，都通過了。不過申請表會問參與度，完全不打開也不好看。'),
                ('已經 14 天了按鈕還是鎖著', '檢查是否連續 14 天都有 12 人同時處於加入狀態。哪天有人退出只剩 11 人，那天就不算。'),
                ('內部測試算嗎？', '不算。必須是封閉測試（Closed testing）。內部測試不在要求之內。'),
            ],
            cta=f'<b>ACT Party</b> 讓開發者互相測試應用程式，並替你記錄每天的打開情況。免費。<a href="/">查看看板</a> · <a href="{STORE}">取得應用程式</a>',
        ),
    }[lang]
