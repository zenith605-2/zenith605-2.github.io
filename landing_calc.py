"""무료 14일 계산기 — "closed testing calculator" 검색을 받는 페이지 (2026-10-07).

검색 상위의 계산기는 유료 테스터 판매로 이어진다(testerbee). 가입도 판매도 없는
계산기를 둔다. 기준은 구글 문서 14151465 의 문장 하나 — "최소 12명의 테스터가
지난 14일 이상 계속 옵트인한 비공개 테스트". 테스터마다 옵트인한 날(나간 날)을
넣으면, 12명이 동시에 14일을 채우는 첫날을 계산한다. 계산은 전부 브라우저에서.
"""
import json

DOC = 'https://support.google.com/googleplay/android-developer/answer/14151465'

# 화면 문구 — 계산기 스크립트가 쓴다
UI = {
    'en': dict(joined='Opted in', left='Left (if they did)', add='+ Add tester', reset='Reset',
               today='Today', calc='Calculate',
               ok='You can apply for production on <b>{d}</b> (12 testers opted in for 14 days on that day).',
               already='<b>Already met</b> since {d}. The production access button should be open — if not, give the console a day to update.',
               short='Not yet reachable: only <b>{n}</b> testers can be counted. Add {m} more and keep everyone opted in.',
               nowline='Today: {c} of 12 testers have 14+ continuous days. {k} are still counting.',
               empty='Enter at least one opt-in date.', tester='Tester'),
    'ko': dict(joined='옵트인한 날', left='나간 날 (나갔다면)', add='+ 테스터 추가', reset='초기화',
               today='오늘', calc='계산하기',
               ok='<b>{d}</b>부터 프로덕션 신청을 할 수 있어요 (그날 12명이 14일을 채움).',
               already='<b>{d}부터 이미 채웠어요.</b> 프로덕션 신청 버튼이 열려 있어야 합니다 — 안 열렸으면 콘솔 반영을 하루 기다려 보세요.',
               short='아직 못 채워요: 셀 수 있는 테스터가 <b>{n}명</b>뿐입니다. {m}명을 더 받고 모두 옵트인을 유지하세요.',
               nowline='오늘 기준: 12명 중 {c}명이 14일 이상 연속, {k}명은 아직 세는 중.',
               empty='옵트인한 날을 하나 이상 넣어 주세요.', tester='테스터'),
    'ja': dict(joined='オプトイン日', left='離脱日（あれば）', add='+ テスター追加', reset='リセット',
               today='今日', calc='計算する',
               ok='<b>{d}</b> から製品版の申請ができます（その日に12人が14日に到達）。',
               already='<b>{d} から条件を満たしています。</b>製品版アクセスのボタンが開いているはずです — まだなら Console の反映を1日待ってください。',
               short='まだ届きません：数えられるテスターが <b>{n}人</b> だけです。あと {m}人 集めて、全員オプトインを続けてください。',
               nowline='今日の時点：12人中 {c}人 が14日以上連続、{k}人 はカウント中。',
               empty='オプトイン日を1つ以上入力してください。', tester='テスター'),
    'zh-Hans': dict(joined='加入日期', left='退出日期（如有）', add='+ 添加测试人员', reset='重置',
                    today='今天', calc='计算',
                    ok='从 <b>{d}</b> 起可以申请正式版（当天 12 人满 14 天）。',
                    already='<b>从 {d} 起已满足。</b>正式版访问按钮应已开放 — 如果还没有，请等 Console 更新一天。',
                    short='暂时无法满足：只有 <b>{n}</b> 位测试人员可计入。再找 {m} 位，并让所有人保持加入。',
                    nowline='截至今天：12 人中 {c} 人已连续 14 天以上，{k} 人仍在计算中。',
                    empty='请至少输入一个加入日期。', tester='测试人员'),
    'zh-Hant': dict(joined='加入日期', left='退出日期（如有）', add='+ 新增測試人員', reset='重設',
                    today='今天', calc='計算',
                    ok='從 <b>{d}</b> 起可以申請正式版（當天 12 人滿 14 天）。',
                    already='<b>從 {d} 起已符合。</b>正式版存取按鈕應已開放 — 如果還沒有，請等 Console 更新一天。',
                    short='暫時無法符合：只有 <b>{n}</b> 位測試人員可計入。再找 {m} 位，並讓所有人保持加入。',
                    nowline='截至今天：12 人中 {c} 人已連續 14 天以上，{k} 人仍在計算中。',
                    empty='請至少輸入一個加入日期。', tester='測試人員'),
}


def tool(lang):
    """계산기 HTML + 스크립트. 날짜는 yyyy-mm-dd 를 UTC 자정으로 바꿔 일 단위로 센다."""
    return '''
<style>
  /* 한 줄에 한 명 — 번호 · 옵트인 · 나간 날. 폰 폭에서도 두 줄로 꺾이지 않게 */
  #calc .grid { display: grid; grid-template-columns: 28px 1fr 1fr; gap: 6px 8px; align-items: center }
  #calc .grid input { width: 100%%; min-width: 0; box-sizing: border-box }
  #calc .hd { font-size: 12px }
  #out { position: sticky; top: 0; background: inherit; padding: 2px 0 12px; line-height: 1.7; z-index: 1 }
</style>
<div id="calc" class="note" style="padding:16px 18px;margin:18px 0 8px">
  <div id="out"></div>
  <div class="grid" id="rows"></div>
  <p style="margin:12px 0 0">
    <button type="button" class="btn ghost sm" id="addRow"></button>
    <button type="button" class="btn ghost sm" id="resetRows"></button>
  </p>
</div>
<script>
(function(){
  var T = %s;
  var DAY = 864e5, N = 12, NEED = 14;
  var IS = 'background:var(--ink800);color:var(--ink100);border:1px solid var(--ink600);border-radius:8px;padding:5px 8px;color-scheme:dark;font:inherit';
  var rows = document.getElementById('rows'), out = document.getElementById('out');
  document.getElementById('addRow').textContent = T.add;
  document.getElementById('resetRows').textContent = T.reset;
  function d2n(s){ if(!s) return null; var p=s.split('-'); return Date.UTC(+p[0],+p[1]-1,+p[2])/DAY; }
  function n2d(n){ return new Date(n*DAY).toISOString().slice(0,10); }
  function today(){ var t=new Date(); return Date.UTC(t.getFullYear(),t.getMonth(),t.getDate())/DAY; }
  function cell(html, cls){ var s=document.createElement('span'); if(cls) s.className=cls; s.innerHTML=html; rows.appendChild(s); return s; }
  function row(i){
    cell(String(i+1), 'muted hd');
    cell('<input type="date" class="j" aria-label="'+T.tester+' '+(i+1)+' '+T.joined+'" style="'+IS+'">');
    cell('<input type="date" class="l" aria-label="'+T.tester+' '+(i+1)+' '+T.left+'" style="'+IS+'">');
  }
  function reset(){
    rows.innerHTML='';
    cell('#', 'muted hd'); cell(T.joined, 'muted hd'); cell(T.left, 'muted hd');
    for(var i=0;i<N;i++) row(i);
    calc();
  }
  rows.addEventListener('input', calc);
  // 테스터 한 명 = [옵트인한 날, 나간 날 또는 무한]. 날 X 에 그 사람이 세지려면
  // 옵트인 뒤 14일이 지났고(X - 옵트인 >= 14) 아직 안 나갔어야(X < 나간 날) 한다.
  function counted(ts, x){ var c=0; ts.forEach(function(t){ if(x-t[0]>=NEED && x<t[1]) c++; }); return c; }
  function calc(){
    var ts=[], js=rows.querySelectorAll('.j'), ls=rows.querySelectorAll('.l');
    js.forEach(function(e, i){
      var j=d2n(e.value), l=d2n(ls[i].value);
      if(j!==null) ts.push([j, l===null?Infinity:l]);
    });
    if(!ts.length){ out.innerHTML='<span class="muted">'+T.empty+'</span>'; return; }
    var now=today(), lo=Math.min.apply(null, ts.map(function(t){return t[0];}));
    var first=null;
    for(var x=lo; x<=Math.max(now, lo)+400; x++){ if(counted(ts,x)>=N){ first=x; break; } }
    var html='';
    if(first===null){
      var alive=ts.filter(function(t){return t[1]===Infinity;}).length;
      html=T.short.replace('{n}',alive).replace('{m}',Math.max(N-alive,1));
    } else if(first<=now){ html=T.already.replace('{d}',n2d(first)); }
    else { html=T.ok.replace('{d}',n2d(first)); }
    var c=counted(ts,now), k=ts.filter(function(t){return t[0]<=now && now<t[1] && now-t[0]<NEED;}).length;
    out.innerHTML=html+'<br><span class="muted" style="font-size:13px">'+T.nowline.replace('{c}',c).replace('{k}',k)+'</span>';
  }
  document.getElementById('addRow').onclick=function(){ row(rows.querySelectorAll('.j').length); };
  document.getElementById('resetRows').onclick=reset;
  reset();
})();
</script>''' % json.dumps(UI[lang], ensure_ascii=False)


def p_calc(lang):
    from landing_build import STORE, guide   # 모듈 로드 뒤에 부르므로 순환 아님
    g = lambda n: guide(lang, n)
    cta_board = f'<a href="/">{ {"en": "See the board", "ko": "보드 보기", "ja": "ボードを見る", "zh-Hans": "查看看板", "zh-Hant": "查看看板"}[lang] }</a>'
    cta_app = f'<a href="{STORE}">{ {"en": "Get the app", "ko": "앱 받기", "ja": "アプリを入手", "zh-Hans": "获取应用", "zh-Hant": "取得應用程式"}[lang] }</a>'
    return {
        'en': dict(
            title='Closed testing calculator: when do 12 testers reach 14 days? (free) | ACT Party',
            desc='Free Google Play closed testing calculator. Enter the day each tester opted in (and left, if they did) and see the first day you can apply for production. No sign-up.',
            h1='Closed testing 14-day calculator',
            sub='Enter when each tester opted in. See the first day 12 of them have 14 continuous days. Free, no sign-up, runs in your browser.',
            body=tool('en') + f'''
<h2>How it is calculated</h2>
<p>Google's rule for new personal developer accounts is a closed test with
<b>at least 12 testers who have been opted in for at least the last 14 days continuously</b>
(<a href="{DOC}">Google Play Console Help</a>). So the clock runs per tester, from their
opt-in, and someone who leaves stops counting. The calculator looks for the first day on
which 12 testers each have 14 unbroken days behind them.</p>
<ul class="steps">
  <li>The 12 do not have to join on the same day. The date is set by the 12th to reach 14 days.</li>
  <li>If someone leaves, they no longer count — add a replacement and keep the others opted in.</li>
  <li>Opening the app every day is not part of this rule. See <a href="{g('what-google-checks')}">what Google actually checks</a>.</li>
</ul>''',
            faq_h='Questions people ask',
            faq=[
                ('Is day 14 or day 15 the day I can apply?',
                 'Count 14 full days from the opt-in date: someone who opted in on the 1st has 14 days on the 15th. The console can lag by about a day.'),
                ('What if a tester opts out and joins again?',
                 'Their continuous stretch starts again from the new opt-in. Enter the new date as a separate tester.'),
                ('Does uninstalling the app count as leaving?',
                 "Google's rule is written in terms of being opted in. Ask testers to stay opted in until you launch."),
            ],
            cta=f'Need the 12 testers in the first place? On <b>ACT Party</b> developers swap closed tests for free, and each day a tester opens your app is recorded automatically. {cta_board} · {cta_app}',
        ),
        'ko': dict(
            title='비공개 테스트 14일 계산기 — 12명이 언제 14일을 채우나 (무료) | ACT Party',
            desc='구글 플레이 비공개 테스트 계산기. 테스터마다 옵트인한 날(나간 날)을 넣으면 프로덕션 신청이 가능한 첫날을 알려 줍니다. 가입 없이 무료.',
            h1='비공개 테스트 14일 계산기',
            sub='테스터마다 옵트인한 날을 넣으면, 12명이 동시에 14일을 채우는 첫날을 계산합니다. 무료, 가입 없음, 브라우저 안에서만 계산.',
            body=tool('ko') + f'''
<h2>이렇게 계산합니다</h2>
<p>새 개인 개발자 계정의 조건은 <b>최소 12명의 테스터가 지난 14일 이상 계속 옵트인한 비공개
테스트</b>입니다 (<a href="{DOC}">Play Console 고객센터</a>). 그래서 14일은 테스터마다
옵트인한 날부터 따로 세고, 나간 사람은 더 이상 세지 않습니다. 계산기는 12명이 각자 끊김 없이
14일을 채운 첫날을 찾습니다.</p>
<ul class="steps">
  <li>12명이 같은 날 들어올 필요는 없습니다. 날짜는 열두 번째로 14일을 채우는 사람이 정합니다.</li>
  <li>나간 사람은 빠집니다 — 한 명을 새로 받고, 나머지는 옵트인을 유지하세요.</li>
  <li>매일 앱을 여는지는 이 조건에 없습니다. <a href="{g('what-google-checks')}">구글이 실제로 보는 것</a>을 참고하세요.</li>
</ul>''',
            faq_h='자주 묻는 질문',
            faq=[
                ('14일째에 신청하나요, 15일째에 신청하나요?',
                 '옵트인한 날부터 만 14일입니다. 1일에 옵트인한 사람은 15일에 14일이 됩니다. 콘솔 반영은 하루쯤 늦을 수 있습니다.'),
                ('테스터가 옵트아웃했다가 다시 들어오면요?',
                 '다시 옵트인한 날부터 새로 이어집니다. 새 날짜를 다른 테스터 줄에 넣어 계산하세요.'),
                ('앱을 지우면 나간 걸로 치나요?',
                 '구글 조건은 옵트인 기준으로 적혀 있습니다. 출시할 때까지 옵트인은 유지해 달라고 부탁하세요.'),
            ],
            cta=f'12명부터 구해야 한다면 — <b>ACT Party</b>에서는 개발자끼리 비공개 테스트를 무료로 품앗이하고, 테스터가 앱을 연 날이 자동으로 기록됩니다. {cta_board} · {cta_app}',
        ),
        'ja': dict(
            title='クローズドテスト14日計算機 — 12人がいつ14日に届くか（無料） | ACT Party',
            desc='Google Play クローズドテストの無料計算機。テスターごとのオプトイン日（離脱日）を入れると、製品版を申請できる最初の日が分かります。登録不要。',
            h1='クローズドテスト 14日計算機',
            sub='テスターごとのオプトイン日を入れると、12人が同時に14日に届く最初の日を計算します。無料・登録不要・ブラウザ内で計算。',
            body=tool('ja') + f'''
<h2>計算のしかた</h2>
<p>新しい個人デベロッパーアカウントの条件は、<b>少なくとも12人のテスターが直近14日以上続けてオプトインしているクローズドテスト</b>です
（<a href="{DOC}">Play Console ヘルプ</a>）。14日はテスターごとにオプトインした日から数え、離脱した人は数えません。
計算機は、12人がそれぞれ途切れずに14日を満たす最初の日を探します。</p>
<ul class="steps">
  <li>12人が同じ日に参加する必要はありません。日付は12番目に14日に届く人で決まります。</li>
  <li>離脱した人は外れます — 代わりを1人入れて、ほかの人はオプトインを続けてもらいましょう。</li>
  <li>毎日アプリを開くことはこの条件に含まれません。<a href="{g('what-google-checks')}">Google が実際に見ているもの</a>も参照してください。</li>
</ul>''',
            faq_h='よくある質問',
            faq=[
                ('申請できるのは14日目ですか、15日目ですか？',
                 'オプトイン日から満14日です。1日にオプトインした人は15日に14日になります。Console の反映は1日ほど遅れることがあります。'),
                ('テスターがオプトアウトして戻ってきたら？',
                 '再オプトインした日から改めて数えます。新しい日付を別のテスター行に入れて計算してください。'),
                ('アプリを削除したら離脱扱いですか？',
                 'Google の条件はオプトインを基準に書かれています。リリースまではオプトインを続けてもらうよう頼みましょう。'),
            ],
            cta=f'まず12人を集めるなら — <b>ACT Party</b> では開発者同士でクローズドテストを無料で交換でき、テスターがアプリを開いた日が自動で記録されます。{cta_board} · {cta_app}',
        ),
        'zh-Hans': dict(
            title='封闭测试 14 天计算器 — 12 位测试人员何时满 14 天（免费） | ACT Party',
            desc='免费的 Google Play 封闭测试计算器。输入每位测试人员的加入日期（和退出日期），即可知道最早可以申请正式版的日子。无需注册。',
            h1='封闭测试 14 天计算器',
            sub='输入每位测试人员的加入日期，算出 12 人同时满 14 天的第一天。免费、无需注册、只在浏览器内计算。',
            body=tool('zh-Hans') + f'''
<h2>计算方法</h2>
<p>新个人开发者账号的条件是：<b>封闭测试中至少有 12 位测试人员在过去 14 天以上持续选择加入</b>
（<a href="{DOC}">Play 管理中心帮助</a>）。所以 14 天按每位测试人员各自的加入日期计算，退出的人不再计入。
计算器会找出 12 人各自连续满 14 天的第一天。</p>
<ul class="steps">
  <li>12 人不必同一天加入。日期由第 12 位满 14 天的人决定。</li>
  <li>退出的人不再计入 — 补一位新的，其他人保持加入。</li>
  <li>每天打开应用不在这条规则里。请参考 <a href="{g('what-google-checks')}">Google 实际检查什么</a>。</li>
</ul>''',
            faq_h='常见问题',
            faq=[
                ('第 14 天还是第 15 天可以申请？',
                 '从加入日起满 14 天。1 日加入的人在 15 日满 14 天。Console 可能会晚一天更新。'),
                ('测试人员退出后又重新加入呢？',
                 '从重新加入的日期重新计算。把新日期填在另一行。'),
                ('卸载应用算退出吗？',
                 'Google 的条件是按"选择加入"来写的。请测试人员在上线前保持加入。'),
            ],
            cta=f'还没凑齐 12 人？在 <b>ACT Party</b>，开发者之间免费互换封闭测试，测试人员打开应用的日子会自动记录。{cta_board} · {cta_app}',
        ),
        'zh-Hant': dict(
            title='封閉測試 14 天計算器 — 12 位測試人員何時滿 14 天（免費） | ACT Party',
            desc='免費的 Google Play 封閉測試計算器。輸入每位測試人員的加入日期（和退出日期），即可知道最早可以申請正式版的日子。無需註冊。',
            h1='封閉測試 14 天計算器',
            sub='輸入每位測試人員的加入日期，算出 12 人同時滿 14 天的第一天。免費、無需註冊、只在瀏覽器內計算。',
            body=tool('zh-Hant') + f'''
<h2>計算方法</h2>
<p>新個人開發者帳戶的條件是：<b>封閉測試中至少有 12 位測試人員在過去 14 天以上持續選擇加入</b>
（<a href="{DOC}">Play 管理中心說明</a>）。所以 14 天按每位測試人員各自的加入日期計算，退出的人不再計入。
計算器會找出 12 人各自連續滿 14 天的第一天。</p>
<ul class="steps">
  <li>12 人不必同一天加入。日期由第 12 位滿 14 天的人決定。</li>
  <li>退出的人不再計入 — 補一位新的，其他人保持加入。</li>
  <li>每天打開應用程式不在這條規則裡。請參考 <a href="{g('what-google-checks')}">Google 實際檢查什麼</a>。</li>
</ul>''',
            faq_h='常見問題',
            faq=[
                ('第 14 天還是第 15 天可以申請？',
                 '從加入日起滿 14 天。1 日加入的人在 15 日滿 14 天。Console 可能會晚一天更新。'),
                ('測試人員退出後又重新加入呢？',
                 '從重新加入的日期重新計算。把新日期填在另一行。'),
                ('解除安裝應用程式算退出嗎？',
                 'Google 的條件是按「選擇加入」來寫的。請測試人員在上架前保持加入。'),
            ],
            cta=f'還沒湊齊 12 人？在 <b>ACT Party</b>，開發者之間免費互換封閉測試，測試人員打開應用程式的日子會自動記錄。{cta_board} · {cta_app}',
        ),
    }[lang]
