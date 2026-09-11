# -*- coding: utf-8 -*-
"""랜딩 4 — "안드로이드 비공개 테스트, 실제로 돌려 보면 어떻게 되나"

검색: 안드로이드 비공개 테스트 / android closed testing / クローズドテスト /
      安卓封闭测试

앞의 세 페이지는 "어떻게 하나"를 설명한다. 그 검색어는 이미 경쟁이 심하고,
구글 문서를 옮겨 적은 글이 수백 개다. 이 페이지는 다르게 간다 — 우리만 가진
숫자를 낸다. 2026-08-16 ~ 09-10, 참여 1,862건에서 나온 실측이다.

수치를 고칠 때 주의: 완주율의 분모는 '시작한 지 14일이 실제로 지난 건'이다.
전체로 나누면 아직 5일째인 건이 중도포기로 세어져서 완주율이 1.7% 로 나온다.
그건 거짓말이다.

또 하나 — 매일 실행은 구글 요건이 아니다. 구글은 옵트인이 14일 이어졌는지를
본다. 인증 일수는 우리가 '진짜 테스트했는지' 보려고 재는 값이다. 이 구분을
뭉개면 경쟁 글들과 똑같아진다.
"""


def p_data(lang):
    # 모듈 최상단에서 import 하면 순환이 된다 (landing_build 가 이 파일을 부른다).
    # landing_find 와 같은 방식으로 함수 안에서 가져온다.
    from landing_build import guide, STORE
    g = lambda n: guide(lang, n)  # noqa: E731

    return {
        'ko': dict(
            title='안드로이드 비공개 테스트, 참여 1,862건 실측 데이터 | ACT Party',
            desc='안드로이드 비공개 테스트 14일을 참여 1,862건 돌려 본 결과. 완주율 27.6%, 이탈은 10~13일에 몰린다, "설치가 안 돼요" 105건 중 87건은 링크가 멀쩡했다.',
            h1='안드로이드 비공개 테스트, 실제로 돌려 보면 이렇게 됩니다',
            sub='참여 1,862건 · 인증 8,054건에서 나온 숫자 (2026년 8월 16일 ~ 9월 10일)',
            body=f'''
<p>안드로이드 비공개 테스트를 어떻게 하는지 설명하는 글은 많습니다. 그런데
<b>실제로 12명을 모아 14일을 돌리면 어떻게 되는지</b>를 숫자로 쓴 글은 없습니다.
저희는 개발자끼리 비공개 테스트를 교환하는 서비스를 운영하고 있어서 그 데이터가
쌓였습니다. 그대로 공개합니다.</p>

<p class="muted" style="font-size:13px">집계 범위 — 2026년 8월 16일 ~ 9월 10일 ·
개발자 144명 · 앱 115개 · 테스트 참여 1,862건 · 일일 인증 기록 8,054건</p>

<h2>1. 14일을 다 채우는 사람은 4명 중 1명입니다</h2>
<p>시작한 지 14일이 <b>실제로 지난</b> 참여 116건만 셌습니다. 아직 5일째인 건을
중도 포기로 세면 안 되니까요.</p>
<ul class="steps">
  <li>14일 완주 — <b>32건 (27.6%)</b></li>
  <li>중도 이탈 — 78건</li>
  <li>한 번도 안 연 사람 — 6건 (5.2%)</li>
  <li>평균 인증 일수 — <b>10.3일</b></li>
</ul>
<p>12명을 모았다고 12명이 끝까지 가지 않습니다. 넉넉하게 모아야 합니다.</p>

<h2>2. 그런데 사람들은 초반에 그만두지 않습니다</h2>
<p>이탈 78건이 며칠째에 멈췄는지 세어 봤습니다. 예상은 "1~3일에 우수수 빠진다"
였는데 정반대였습니다.</p>
<ul class="steps">
  <li>1~5일에 멈춘 사람 — 19건</li>
  <li>6~9일 — 9건</li>
  <li><b>10~13일 — 50건</b></li>
</ul>
<p>이탈의 <b>3분의 2가 마지막 나흘</b>에 몰려 있습니다. 이 사람들은 마음이 식은 게
아닙니다. 열흘 넘게 매일 열다가 하루를 빠뜨린 겁니다. 바빴거나, 폰을 바꿨거나,
알림을 껐거나.</p>
<p>그래서 <b>12일째·13일째의 리마인드 한 번</b>이 초반 안내 열 번보다 낫습니다.
자세한 이야기는 <a href="{g('why-testers-drop')}">테스터가 중간에 빠지는 이유</a>에
있습니다.</p>

<h2>3. "설치가 안 돼요"의 83%는 링크 문제가 아닙니다</h2>
<p>테스터가 "링크가 안 열려요"라고 신고한 게 <b>105건</b> 있었습니다. 그때마다
같은 앱에 다른 사람이 최근 7일 안에 들어간 기록이 있는지 자동으로 확인했습니다.</p>
<p><b>105건 중 87건은 다른 사람들이 멀쩡히 들어가고 있었습니다.</b> 링크는
정상이고 그 사람만 못 들어간 겁니다. 원인은 셋 중 하나였습니다.</p>

<h3>① 국가가 안 열려 있다 — 신고 61건</h3>
<p>가장 흔합니다. 비공개 테스트의 국가 설정이 좁으면 다른 나라 테스터는 스토어에서
앱 자체를 못 봅니다. <code>이 앱은 사용자의 국가에서 제공되지 않습니다</code>만
뜨고 끝입니다. 신고가 들어온 국가는 이렇습니다.</p>
<p class="muted">GB 13 · KR 12 · IN 6 · BR 6 · SE 6 · JP 5 · FR 4 · US 4</p>
<p>한국 개발자가 한국에만 열어 두고 해외 테스터를 모으면 그 사람들은 아무것도
못 합니다. <b>테스터를 모으기 전에 국가를 전체로 열어 두세요.</b> Play Console →
비공개 테스트 → 국가/지역. 확인법은
<a href="{g('country-availability')}">국가 때문에 설치가 안 될 때</a>에 있습니다.</p>

<h3>② 로그인 계정과 플레이스토어 계정이 다르다</h3>
<p>잘 안 보이는 함정입니다. 그룹 가입과 옵트인은 <b>폰의 플레이스토어에 로그인된
계정</b>으로 해야 동작합니다. 구글 계정을 여러 개 쓰는 사람은 여기서 갈립니다.</p>
<p>테스터에게 이메일을 받을 때 "쓰시는 이메일"이 아니라 <b>"폰 플레이스토어에
로그인된 계정"</b>이라고 물어야 합니다. 한 글자 차이인데 결과가 다릅니다.</p>

<h3>③ 그룹에 가입하지 않고 옵트인 링크부터 눌렀다</h3>
<p>구글 그룹으로 테스터를 관리하면 순서가 있습니다. <b>그룹 가입 → 옵트인 →
설치</b>. 옵트인부터 누르면 <code>이 프로그램에 참여할 수 없습니다</code>가 뜹니다.
그런데 이 화면에는 "그룹에 먼저 가입하세요"라는 말이 없습니다. 그래서 테스터는
링크가 깨진 줄 압니다. 순서와 화면은
<a href="{g('google-group')}">구글 그룹 연결하기</a>에 정리해 뒀습니다.</p>

<h2>4. 그리고 반영에 시간이 걸립니다</h2>
<p>옵트인을 눌러도 스토어에 바로 안 뜹니다. 최대 30분쯤 걸립니다. 이걸 모르면
"역시 안 되네" 하고 그냥 닫습니다. 테스터에게 미리 말해 두세요.</p>

<h2>모으기 전에 확인할 것</h2>
<ol class="steps">
  <li>비공개 테스트 <b>국가를 전체로</b> 열었는가</li>
  <li>테스터에게 <b>"폰 플레이스토어 계정"</b>이라고 명시해서 이메일을 받았는가</li>
  <li>그룹 방식이면 <b>그룹 가입 → 옵트인 → 설치</b> 순서를 안내했는가</li>
  <li>옵트인 후 <b>최대 30분</b> 걸린다고 미리 알렸는가</li>
  <li>12명이 아니라 <b>넉넉하게</b> 모았는가 (완주율 27.6%)</li>
  <li><b>12~13일째 리마인드</b>를 준비했는가</li>
</ol>
<p>앞의 네 개만 지켜도 "설치가 안 돼요" 문의가 대부분 사라집니다.</p>''',
            faq_h='자주 묻는 질문',
            faq=[
                ('안드로이드 비공개 테스트는 테스터가 매일 앱을 열어야 하나요?',
                 '구글이 보는 건 옵트인 상태가 14일 이어졌는지입니다. 매일 실행은 구글 요건이 아닙니다. 다만 한 번도 안 여는 테스터가 섞이면 프로덕션 신청 설문에서 설명하기 어려워집니다.'),
                ('12명 중 한 명이 중간에 나가면 처음부터 다시인가요?',
                 '아닙니다. 남은 사람의 기간은 그대로 쌓이고, 새로 들어온 테스터만 14일을 채우면 됩니다.'),
                ('테스터가 "앱을 찾을 수 없다"고 하는데 링크는 정상입니다.',
                 '실측 105건 중 87건이 그 경우였습니다. 국가 미개방, 로그인 계정과 플레이스토어 계정 불일치, 그룹 미가입 순으로 흔합니다. 국가부터 확인하세요.'),
                ('테스터는 몇 명을 모아야 안전한가요?',
                 '완주율이 27.6%였습니다. 12명이 필요하면 그보다 넉넉하게 모으고, 12~13일째에 리마인드를 보내는 편이 확실합니다.'),
            ],
            cta=f'이 숫자는 <b>ACT Party</b>에서 나왔습니다. 개발자끼리 비공개 테스트를 품앗이하는 서비스이고, 앱을 열었는지는 안드로이드 사용 정보로 자동 기록됩니다. <a href="/">보드 보기</a> · <a href="{STORE}">앱 받기</a>',
        ),

        'en': dict(
            title='Android closed testing: what 1,862 real test runs look like | ACT Party',
            desc='Data from 1,862 Android closed-testing runs. 27.6% finish all 14 days, most drop-offs land on days 10-13, and 83% of "the link is broken" reports were not about the link.',
            h1='Android closed testing, measured',
            sub='1,862 test runs · 8,054 daily check-ins (16 Aug – 10 Sep 2026)',
            body=f'''
<p>Plenty of posts explain how Android closed testing works. Almost none say
<b>what happens when you actually run 12 testers for 14 days</b>. We operate a
service where developers test each other's apps, so we have that data. Here it is.</p>

<p class="muted" style="font-size:13px">Period — 16 Aug to 10 Sep 2026 ·
144 developers · 115 apps · 1,862 test runs · 8,054 daily check-ins</p>

<h2>1. One in four testers finishes all 14 days</h2>
<p>Counting only the 116 runs that <b>actually passed the 14-day mark</b>. A run
still on day 5 is not a drop-out.</p>
<ul class="steps">
  <li>Finished 14 days — <b>32 (27.6%)</b></li>
  <li>Dropped out — 78</li>
  <li>Never opened it once — 6 (5.2%)</li>
  <li>Average days logged — <b>10.3</b></li>
</ul>
<p>Recruiting 12 does not mean 12 finish. Recruit with slack.</p>

<h2>2. But people do not quit early</h2>
<p>We checked which day each of the 78 drop-offs stopped on. We expected a rush
of quitters in the first three days. It was the opposite.</p>
<ul class="steps">
  <li>Stopped on days 1–5 — 19</li>
  <li>Days 6–9 — 9</li>
  <li><b>Days 10–13 — 50</b></li>
</ul>
<p><b>Two thirds of drop-offs happen in the last four days.</b> These people did
not lose interest. They opened the app daily for over a week and then missed one
day — busy, new phone, notifications off.</p>
<p>So <b>one reminder on day 12 or 13</b> beats ten onboarding messages. More in
<a href="{g('why-testers-drop')}">Why testers drop out</a>.</p>

<h2>3. 83% of "I can't install it" is not the link</h2>
<p>Testers filed <b>105 reports</b> saying an opt-in link would not open. Each
time we checked automatically whether anyone else had entered that same app in
the previous 7 days.</p>
<p><b>In 87 of the 105, other people were getting in fine.</b> The link worked;
that one person could not use it. Three causes covered nearly all of them.</p>

<h3>1. The country is not open — 61 reports</h3>
<p>The most common by far. If the closed test's country list is narrow, testers
elsewhere cannot even see the app in the store. They get
<code>This app is not available in your country</code> and nothing else. The
countries the reports came from:</p>
<p class="muted">GB 13 · KR 12 · IN 6 · BR 6 · SE 6 · JP 5 · FR 4 · US 4</p>
<p><b>Open the country list before you recruit</b> — Play Console → closed
testing → Countries / regions. See
<a href="{g('country-availability')}">When a country blocks the install</a>.</p>

<h3>2. Their login is not their Play Store account</h3>
<p>Joining the group and opting in only work from the <b>Google account signed
into the Play Store on the phone</b>. Anyone with several Google accounts splits
here.</p>
<p>When you ask a tester for an email, ask for <b>"the account signed into your
Play Store"</b>, not "your email". Same question, different answer.</p>

<h3>3. They hit the opt-in link before joining the group</h3>
<p>With a Google Group the order matters: <b>join the group → opt in →
install</b>. Opting in first shows <code>You are not able to join this
program</code>, and that screen never says "join the group first". The tester
concludes the link is broken. Screens and order are in
<a href="{g('google-group')}">Connecting a Google Group</a>.</p>

<h2>4. And it takes time to propagate</h2>
<p>Opting in does not put the app in the store immediately — it can take about
30 minutes. Testers who do not know this close the page and give up. Tell them
up front.</p>

<h2>Checklist before recruiting</h2>
<ol class="steps">
  <li>Closed test <b>open to all countries</b>?</li>
  <li>Asked for the <b>Play Store account</b>, in those words?</li>
  <li>If using a group, explained <b>join → opt in → install</b>?</li>
  <li>Warned them about the <b>~30 minute</b> delay?</li>
  <li>Recruited <b>more than 12</b>? (27.6% finish)</li>
  <li>Reminder ready for <b>day 12–13</b>?</li>
</ol>
<p>The first four alone remove most "it will not install" messages.</p>''',
            faq_h='Frequently asked',
            faq=[
                ('Do testers have to open the app every day?',
                 'Google looks at whether the opt-in lasted 14 days. Daily opens are not a Google requirement. That said, testers who never open it at all are hard to explain on the production questionnaire.'),
                ('If one of the 12 leaves, do I start over?',
                 'No. The remaining testers keep their elapsed time; only a replacement needs their own 14 days.'),
                ('A tester says the app cannot be found, but the link works for me.',
                 'That was 87 of the 105 reports we measured. In order of frequency: country not open, login account differs from the Play Store account, group not joined. Check the country first.'),
                ('How many testers should I recruit to be safe?',
                 '27.6% finished all 14 days in our data. If you need 12, recruit with slack and send a reminder on day 12 or 13.'),
            ],
            cta=f'These numbers come from <b>ACT Party</b>, where developers trade closed tests with each other and daily opens are recorded automatically from Android usage stats. <a href="/">See the board</a> · <a href="{STORE}">Get the app</a>',
        ),

        'ja': dict(
            title='Androidクローズドテスト、1,862件の実測データ | ACT Party',
            desc='Androidクローズドテスト14日間を1,862件回した実測。完走率27.6%、離脱は10〜13日目に集中、「インストールできない」105件のうち87件はリンクの問題ではなかった。',
            h1='Androidクローズドテスト、実際に回すとこうなります',
            sub='テスト参加1,862件・日次記録8,054件（2026年8月16日〜9月10日）',
            body=f'''
<p>クローズドテストのやり方を説明する記事は多くあります。しかし
<b>実際に12人を集めて14日間回すとどうなるのか</b>を数字で書いた記事はありません。
私たちは開発者同士がクローズドテストを交換するサービスを運営しており、そのデータが
貯まりました。そのまま公開します。</p>

<p class="muted" style="font-size:13px">集計期間 — 2026年8月16日〜9月10日 ·
開発者144名 · アプリ115本 · テスト参加1,862件 · 日次記録8,054件</p>

<h2>1. 14日間を完走するのは4人に1人</h2>
<p>開始から14日が<b>実際に経過した</b>116件のみを数えました。まだ5日目の件を
離脱として数えるわけにはいきません。</p>
<ul class="steps">
  <li>14日完走 — <b>32件（27.6%）</b></li>
  <li>途中離脱 — 78件</li>
  <li>一度も開かなかった人 — 6件（5.2%）</li>
  <li>平均認証日数 — <b>10.3日</b></li>
</ul>
<p>12人集めても12人が最後まで行くわけではありません。余裕をもって集めてください。</p>

<h2>2. しかし人は序盤では辞めません</h2>
<p>離脱78件が何日目で止まったかを数えました。予想は「1〜3日目に一気に抜ける」
でしたが、正反対でした。</p>
<ul class="steps">
  <li>1〜5日目で停止 — 19件</li>
  <li>6〜9日目 — 9件</li>
  <li><b>10〜13日目 — 50件</b></li>
</ul>
<p>離脱の<b>3分の2が最後の4日間</b>に集中しています。この人たちは飽きたのでは
ありません。10日以上毎日開いていて、1日だけ抜けたのです。忙しかったか、機種変更か、
通知を切ったか。</p>
<p>つまり<b>12日目・13日目のリマインド1回</b>が、序盤の案内10回より効きます。
詳しくは<a href="{g('why-testers-drop')}">テスターが途中で抜ける理由</a>に。</p>

<h2>3.「インストールできない」の83%はリンクの問題ではない</h2>
<p>テスターから「リンクが開かない」という報告が<b>105件</b>ありました。その都度、
同じアプリに直近7日以内に他の人が入れているかを自動で確認しました。</p>
<p><b>105件のうち87件は、他の人は問題なく入れていました。</b>リンクは正常で、
その人だけが入れなかったのです。原因は次の3つでした。</p>

<h3>① 国が開いていない — 報告61件</h3>
<p>最も多い原因です。クローズドテストの国設定が狭いと、他国のテスターはストアで
アプリ自体を見られません。<code>このアプリはお住まいの国では提供されていません</code>
だけが表示されます。報告のあった国は次のとおりです。</p>
<p class="muted">GB 13 · KR 12 · IN 6 · BR 6 · SE 6 · JP 5 · FR 4 · US 4</p>
<p><b>テスターを集める前に国を全体に開いてください。</b>Play Console → クローズド
テスト → 国/地域。詳しくは<a href="{g('country-availability')}">国が原因でインストールできないとき</a>に。</p>

<h3>② ログインアカウントとPlayストアのアカウントが違う</h3>
<p>見えにくい落とし穴です。グループ参加とオプトインは<b>スマホのPlayストアに
ログインしているアカウント</b>で行う必要があります。Googleアカウントを複数使う人は
ここで分かれます。</p>
<p>テスターにメールを聞くときは「お使いのメール」ではなく
<b>「スマホのPlayストアにログイン中のアカウント」</b>と聞いてください。</p>

<h3>③ グループに参加せずオプトインリンクを先に押した</h3>
<p>Googleグループでテスターを管理する場合は順番があります。<b>グループ参加 →
オプトイン → インストール</b>。オプトインから押すと
<code>このプログラムには参加できません</code>と表示されますが、その画面には
「先にグループに参加してください」とは書かれていません。だからテスターはリンクが
壊れていると思います。<a href="{g('google-group')}">Googleグループの連携</a>にまとめました。</p>

<h2>4. 反映には時間がかかります</h2>
<p>オプトインしてもストアにすぐは出ません。最大30分ほどかかります。これを知らないと
「やっぱりダメだ」と閉じてしまいます。事前に伝えてください。</p>

<h2>集める前に確認すること</h2>
<ol class="steps">
  <li>クローズドテストの<b>国を全体に</b>開いたか</li>
  <li>テスターに<b>「Playストアのアカウント」</b>と明示して聞いたか</li>
  <li>グループ方式なら<b>参加 → オプトイン → インストール</b>の順を案内したか</li>
  <li>オプトイン後<b>最大30分</b>かかると伝えたか</li>
  <li>12人ではなく<b>余裕をもって</b>集めたか（完走率27.6%）</li>
  <li><b>12〜13日目のリマインド</b>を用意したか</li>
</ol>''',
            faq_h='よくある質問',
            faq=[
                ('テスターは毎日アプリを開く必要がありますか？',
                 'Googleが見るのはオプトイン状態が14日続いたかです。毎日の起動はGoogleの要件ではありません。ただし一度も開かないテスターが混ざると、製品版申請のアンケートで説明しづらくなります。'),
                ('12人のうち1人が抜けたら最初からやり直しですか？',
                 'いいえ。残った人の期間はそのまま積み上がり、新しく入ったテスターだけが14日を満たせば大丈夫です。'),
                ('テスターが「アプリが見つからない」と言いますが、リンクは正常です。',
                 '実測105件のうち87件がその状況でした。国が開いていない、ログインとPlayストアのアカウント不一致、グループ未参加の順に多いです。まず国を確認してください。'),
                ('テスターは何人集めれば安全ですか？',
                 '完走率は27.6%でした。12人必要なら余裕をもって集め、12〜13日目にリマインドを送るのが確実です。'),
            ],
            cta=f'この数字は<b>ACT Party</b>から出ています。開発者同士でクローズドテストを交換するサービスで、アプリを開いたかはAndroidの使用状況から自動で記録されます。<a href="/">ボードを見る</a> · <a href="{STORE}">アプリを入手</a>',
        ),

        'zh-Hans': dict(
            title='安卓封闭测试：1,862 次真实运行的数据 | ACT Party',
            desc='来自 1,862 次安卓封闭测试的实测数据。27.6% 完成全部 14 天，流失集中在第 10-13 天，"装不上"的 105 次反馈中有 87 次并非链接问题。',
            h1='安卓封闭测试，用数据说话',
            sub='1,862 次测试 · 8,054 条每日记录（2026 年 8 月 16 日 – 9 月 10 日）',
            body=f'''
<p>讲解封闭测试怎么做的文章很多，但几乎没有人写
<b>真正凑齐 12 位测试者、跑满 14 天之后会发生什么</b>。我们运营着一个开发者互相
测试彼此应用的服务，数据就在这里，原样公开。</p>

<p class="muted" style="font-size:13px">统计范围 — 2026 年 8 月 16 日至 9 月 10 日 ·
开发者 144 人 · 应用 115 个 · 测试参与 1,862 次 · 每日记录 8,054 条</p>

<h2>1. 每四个人里只有一个跑满 14 天</h2>
<p>只统计<b>确实已经过了 14 天</b>的 116 次。还在第 5 天的不能算作放弃。</p>
<ul class="steps">
  <li>完成 14 天 — <b>32 次（27.6%）</b></li>
  <li>中途流失 — 78 次</li>
  <li>一次都没打开 — 6 次（5.2%）</li>
  <li>平均记录天数 — <b>10.3 天</b></li>
</ul>
<p>招到 12 人不等于 12 人跑到最后。要留出余量。</p>

<h2>2. 但人们并不会在前期放弃</h2>
<p>我们统计了 78 次流失分别停在第几天。原以为会集中在前三天，结果正相反。</p>
<ul class="steps">
  <li>第 1–5 天停止 — 19 次</li>
  <li>第 6–9 天 — 9 次</li>
  <li><b>第 10–13 天 — 50 次</b></li>
</ul>
<p><b>三分之二的流失发生在最后四天。</b>这些人不是失去兴趣，而是连续打开十几天后
漏掉了一天 —— 忙、换手机、关了通知。</p>
<p>所以<b>第 12、13 天的一次提醒</b>，胜过前期十次说明。详见
<a href="{g('why-testers-drop')}">测试者中途退出的原因</a>。</p>

<h2>3. "装不上"里有 83% 不是链接的问题</h2>
<p>测试者提交了 <b>105 次</b>"链接打不开"的反馈。每一次我们都会自动检查：最近 7 天
内是否有别人成功进入了同一个应用。</p>
<p><b>105 次里有 87 次，别人都进得去。</b>链接是好的，只有那个人进不去。原因几乎
都是下面三种。</p>

<h3>① 没有开放该国家 — 61 次</h3>
<p>最常见。如果封闭测试的国家范围很窄，其他国家的测试者在商店里根本看不到应用，
只会看到<code>此应用在您所在的国家/地区不可用</code>。反馈来自这些国家：</p>
<p class="muted">GB 13 · KR 12 · IN 6 · BR 6 · SE 6 · JP 5 · FR 4 · US 4</p>
<p><b>招募之前先把国家开放。</b>Play Console → 封闭测试 → 国家/地区。详见
<a href="{g('country-availability')}">国家限制导致无法安装时</a>。</p>

<h3>② 登录账号不是 Play 商店账号</h3>
<p>加入群组和加入测试，都必须用<b>手机 Play 商店当前登录的那个 Google 账号</b>。
有多个账号的人就卡在这里。</p>
<p>向测试者要邮箱时，问的应该是<b>"你手机 Play 商店登录的账号"</b>，而不是
"你的邮箱"。</p>

<h3>③ 没加入群组就先点了测试链接</h3>
<p>用 Google 群组管理测试者时有顺序：<b>加入群组 → 加入测试 → 安装</b>。先点测试
链接会显示<code>您无法加入此计划</code>，而那个页面并不会提示"请先加入群组"，
测试者便以为链接坏了。见<a href="{g('google-group')}">连接 Google 群组</a>。</p>

<h2>4. 生效需要时间</h2>
<p>加入测试之后商店不会立刻出现该应用，大约需要 30 分钟。不知道这一点的人会直接
关掉页面。请提前告诉他们。</p>

<h2>招募前的检查清单</h2>
<ol class="steps">
  <li>封闭测试是否<b>开放所有国家</b></li>
  <li>是否明确按<b>"Play 商店账号"</b>索要邮箱</li>
  <li>用群组的话，是否说明<b>加入群组 → 加入测试 → 安装</b>的顺序</li>
  <li>是否提前告知<b>约 30 分钟</b>的延迟</li>
  <li>是否招募了<b>多于 12 人</b>（完成率 27.6%）</li>
  <li>是否准备了<b>第 12–13 天的提醒</b></li>
</ol>''',
            faq_h='常见问题',
            faq=[
                ('测试者必须每天打开应用吗？',
                 'Google 看的是加入测试的状态是否持续了 14 天。每天打开并不是 Google 的要求。不过如果有测试者一次都没打开，在生产环境申请问卷里会比较难解释。'),
                ('12 人里有一个退出，要从头再来吗？',
                 '不用。其余测试者已积累的时间照常保留，只有新加入的人需要自己跑满 14 天。'),
                ('测试者说找不到应用，但链接在我这里是好的。',
                 '我们统计的 105 次里有 87 次就是这种情况。按常见程度排序：国家未开放、登录账号与 Play 商店账号不一致、没有加入群组。先查国家。'),
                ('招多少测试者才保险？',
                 '我们的数据里完成率是 27.6%。如果需要 12 人，请留出余量，并在第 12 或 13 天发一次提醒。'),
            ],
            cta=f'这些数据来自 <b>ACT Party</b> —— 开发者之间互相进行封闭测试的服务，是否打开过应用由 Android 使用情况自动记录。<a href="/">查看看板</a> · <a href="{STORE}">获取应用</a>',
        ),

        'zh-Hant': dict(
            title='Android 封閉測試：1,862 次真實執行的數據 | ACT Party',
            desc='來自 1,862 次 Android 封閉測試的實測數據。27.6% 完成全部 14 天，流失集中在第 10-13 天，「裝不上」的 105 次回報中有 87 次並非連結問題。',
            h1='Android 封閉測試，用數據說話',
            sub='1,862 次測試 · 8,054 筆每日紀錄（2026 年 8 月 16 日 – 9 月 10 日）',
            body=f'''
<p>說明封閉測試怎麼做的文章很多，但幾乎沒有人寫
<b>真正湊齊 12 位測試者、跑滿 14 天之後會發生什麼</b>。我們營運一個開發者互相
測試彼此應用的服務，數據就在這裡，原樣公開。</p>

<p class="muted" style="font-size:13px">統計範圍 — 2026 年 8 月 16 日至 9 月 10 日 ·
開發者 144 人 · 應用 115 個 · 測試參與 1,862 次 · 每日紀錄 8,054 筆</p>

<h2>1. 每四個人只有一個跑滿 14 天</h2>
<p>只統計<b>確實已經過了 14 天</b>的 116 次。還在第 5 天的不能算放棄。</p>
<ul class="steps">
  <li>完成 14 天 — <b>32 次（27.6%）</b></li>
  <li>中途流失 — 78 次</li>
  <li>一次都沒打開 — 6 次（5.2%）</li>
  <li>平均紀錄天數 — <b>10.3 天</b></li>
</ul>
<p>招到 12 人不等於 12 人跑到最後。要留出餘量。</p>

<h2>2. 但人們不會在前期放棄</h2>
<p>我們統計了 78 次流失分別停在第幾天。原以為會集中在前三天，結果正相反。</p>
<ul class="steps">
  <li>第 1–5 天停止 — 19 次</li>
  <li>第 6–9 天 — 9 次</li>
  <li><b>第 10–13 天 — 50 次</b></li>
</ul>
<p><b>三分之二的流失發生在最後四天。</b>這些人不是失去興趣，而是連續打開十幾天後
漏掉了一天 —— 忙、換手機、關了通知。</p>
<p>所以<b>第 12、13 天的一次提醒</b>，勝過前期十次說明。詳見
<a href="{g('why-testers-drop')}">測試者中途退出的原因</a>。</p>

<h2>3.「裝不上」有 83% 不是連結的問題</h2>
<p>測試者提交了 <b>105 次</b>「連結打不開」的回報。每一次我們都會自動檢查：最近
7 天內是否有別人成功進入同一個應用。</p>
<p><b>105 次裡有 87 次，別人都進得去。</b>連結是好的，只有那個人進不去。原因幾乎
都是下面三種。</p>

<h3>① 沒有開放該國家 — 61 次</h3>
<p>最常見。如果封閉測試的國家範圍很窄，其他國家的測試者在商店裡根本看不到應用，
只會看到<code>此應用在您所在的國家/地區無法使用</code>。回報來自這些國家：</p>
<p class="muted">GB 13 · KR 12 · IN 6 · BR 6 · SE 6 · JP 5 · FR 4 · US 4</p>
<p><b>招募之前先把國家開放。</b>Play Console → 封閉測試 → 國家/地區。詳見
<a href="{g('country-availability')}">國家限制導致無法安裝時</a>。</p>

<h3>② 登入帳號不是 Play 商店帳號</h3>
<p>加入群組和加入測試，都必須用<b>手機 Play 商店目前登入的那個 Google 帳號</b>。
有多個帳號的人就卡在這裡。</p>
<p>向測試者要信箱時，問的應該是<b>「你手機 Play 商店登入的帳號」</b>，而不是
「你的信箱」。</p>

<h3>③ 沒加入群組就先點了測試連結</h3>
<p>用 Google 群組管理測試者時有順序：<b>加入群組 → 加入測試 → 安裝</b>。先點測試
連結會顯示<code>您無法加入此計畫</code>，而那個頁面並不會提示「請先加入群組」，
測試者便以為連結壞了。見<a href="{g('google-group')}">連接 Google 群組</a>。</p>

<h2>4. 生效需要時間</h2>
<p>加入測試之後商店不會立刻出現該應用，大約需要 30 分鐘。不知道這一點的人會直接
關掉頁面。請提前告訴他們。</p>

<h2>招募前的檢查清單</h2>
<ol class="steps">
  <li>封閉測試是否<b>開放所有國家</b></li>
  <li>是否明確按<b>「Play 商店帳號」</b>索取信箱</li>
  <li>用群組的話，是否說明<b>加入群組 → 加入測試 → 安裝</b>的順序</li>
  <li>是否提前告知<b>約 30 分鐘</b>的延遲</li>
  <li>是否招募了<b>多於 12 人</b>（完成率 27.6%）</li>
  <li>是否準備了<b>第 12–13 天的提醒</b></li>
</ol>''',
            faq_h='常見問題',
            faq=[
                ('測試者必須每天打開應用嗎？',
                 'Google 看的是加入測試的狀態是否持續了 14 天。每天打開並不是 Google 的要求。不過如果有測試者一次都沒打開，在正式版申請問卷裡會比較難解釋。'),
                ('12 人裡有一個退出，要從頭再來嗎？',
                 '不用。其餘測試者已累積的時間照常保留，只有新加入的人需要自己跑滿 14 天。'),
                ('測試者說找不到應用，但連結在我這裡是好的。',
                 '我們統計的 105 次裡有 87 次就是這種情況。按常見程度排序：國家未開放、登入帳號與 Play 商店帳號不一致、沒有加入群組。先查國家。'),
                ('要招多少測試者才保險？',
                 '我們的數據裡完成率是 27.6%。如果需要 12 人，請留出餘量，並在第 12 或 13 天發一次提醒。'),
            ],
            cta=f'這些數據來自 <b>ACT Party</b> —— 開發者之間互相進行封閉測試的服務，是否打開過應用由 Android 使用情況自動記錄。<a href="/">查看看板</a> · <a href="{STORE}">取得應用</a>',
        ),
    }[lang]
