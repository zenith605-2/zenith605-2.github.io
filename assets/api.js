// Supabase 접속. publishable 키라 웹에 공개해도 되는 값이다 (RLS 가 실제 경계).
const SUPABASE_URL = 'https://eedqzvckdxfcuoyycivu.supabase.co';
const SUPABASE_KEY = 'sb_publishable_hF3_Mw-TybTPGxXPBx4M3Q_sPKe06UU';

export const sb = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY, {
  auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true },
});

export const STORE_URL =
  'https://play.google.com/store/apps/details?id=kr.testerparty.tester_party';

// ---- 인증 ----
// 안드로이드 앱과 같은 Supabase 프로젝트라 같은 계정으로 들어온다.
export async function signIn() {
  const { error } = await sb.auth.signInWithOAuth({
    provider: 'google',
    options: { redirectTo: location.origin + location.pathname },
  });
  if (error) throw error;
}

/** 로그인 직후 주소창에 남는 #access_token 을 지운다. */
export function cleanUrl() {
  if (location.hash.includes('access_token') || location.search.includes('code=')) {
    history.replaceState({}, '', location.pathname);
  }
}

export async function signOut() {
  await sb.auth.signOut();
  location.reload();
}

// 구글에서 돌아오면 토큰이 URL 해시(#access_token) 또는 쿼리(?code)에 실려 온다.
// detectSessionInUrl 이 그걸 세션으로 바꾸는데 비동기다.
//
// 주의: onAuthStateChange 는 저장된 세션이 없으면 곧바로 INITIAL_SESSION(null)
// 을 쏜다. 그 첫 신호에 결론을 내면 URL 의 토큰을 읽기 전에 '로그인 안 됨'으로
// 확정돼 버린다 — 로그인하고 돌아와도 로그인 화면이 다시 뜨던 이유가 이것이다.
// 그래서 URL 에 토큰이 있을 때는 SIGNED_IN 이 올 때까지 기다린다.
let _ready;
export function authReady() {
  return _ready ??= new Promise((resolve) => {
    const pending = location.hash.includes('access_token') ||
                    /[?&]code=/.test(location.search);
    let done = false;
    const finish = (u) => { if (!done) { done = true; resolve(u ?? null); } };

    sb.auth.onAuthStateChange((event, session) => {
      if (session?.user) return finish(session.user);
      // 토큰을 들고 돌아온 참이면 INITIAL_SESSION(null) 은 무시한다
      if (pending && event === 'INITIAL_SESSION') return;
      finish(null);
    });

    sb.auth.getSession().then(({ data }) => {
      if (data?.session) finish(data.session.user);
      else if (!pending) finish(null);
    }).catch(() => { if (!pending) finish(null); });

    // 교환이 끝내 실패해도 화면이 멈추면 안 된다
    if (pending) setTimeout(() => finish(null), 8000);
  });
}

export async function me() {
  const u = await authReady();
  if (u) return u;
  const { data } = await sb.auth.getUser();
  return data?.user ?? null;
}

// ---- 공개 데이터 (로그인 없이 읽힌다) ----
export async function publicApps() {
  const { data, error } = await sb.rpc('public_apps');
  if (error) throw error;
  return data ?? [];
}

export async function appTesters(appId) {
  const { data } = await sb.rpc('app_testers', { p_app_id: appId });
  return data ?? [];
}

export async function completedTrades(ownerId) {
  const { data } = await sb.rpc('completed_trades', { p_owner: ownerId });
  return data ?? [];
}

// ---- 로그인해야 되는 것들 ----
export async function myApps() {
  // apps 의 SELECT 정책은 true(전체 공개)다 — 앱보드가 그걸로 읽는다.
  // 그래서 여기서 owner_id 를 직접 걸지 않으면 남의 앱까지 딸려온다.
  const uid = (await me())?.id;
  if (!uid) return [];
  const { data, error } = await sb
    .from('apps')
    .select('id,name,description,package_name,opt_in_url,google_group_url,' +
            'icon_url,is_public,recruiting,console_url,needed_testers,created_at,' +
            'optin_broken_at,optin_reports,long_description,screenshot_url')
    .eq('owner_id', uid)
    .order('created_at');
  if (error) throw error;
  return data ?? [];
}

export async function myAppProgress() {
  const { data } = await sb.rpc('my_app_progress');
  return data ?? [];
}

export async function saveApp(app) {
  const uid = (await me())?.id;
  if (!uid) throw new Error('signin');
  const row = {
    owner_id: uid,
    name: app.name,
    description: app.description || null,
    package_name: app.package_name || null,
    opt_in_url: app.opt_in_url || null,
    google_group_url: app.google_group_url || null,
    icon_url: app.icon_url || null,
    long_description: app.long_description || null,
    screenshot_url: app.screenshot_url || null,
    is_public: app.is_public !== false,
  };
  if (app.id) {
    const { error } = await sb.from('apps').update(row)
      .eq('id', app.id).eq('owner_id', uid);
    if (error) throw error;
    return app.id;
  }
  const { data, error } = await sb.from('apps').insert(row).select('id');
  if (error) throw error;
  return data?.[0]?.id;
}

export async function setAppPublic(appId, on) {
  const { error } = await sb.from('apps').update({ is_public: on }).eq('id', appId);
  if (error) throw error;
}

export async function myExchanges() {
  const { data, error } = await sb
    .from('exchanges')
    .select('*, exchange_checkins(day_date,minutes,opens)')
    .order('created_at');
  if (error) throw error;
  return data ?? [];
}

// 앱과 같은 경로 — trade_requests 에 직접 넣는다 (Gateway.requestTrade 와 동일)
export async function offerTrade(appId, myAppId, message) {
  const uid = (await me())?.id;
  if (!uid) throw new Error('signin');
  const row = { app_id: appId, requester_id: uid };
  if (myAppId) row.requester_app_id = myAppId;
  if (message) row.message = message;
  const { error } = await sb.from('trade_requests').insert(row);
  if (error) throw error;
}

export async function cancelTrade(appId) {
  const uid = (await me())?.id;
  const { error } = await sb.from('trade_requests').delete()
    .eq('app_id', appId).eq('requester_id', uid);
  if (error) throw error;
}

export async function incomingRequests() {
  const { data } = await sb.rpc('incoming_trade_requests');
  return data ?? [];
}

export async function acceptRequest(requestId) {
  const { error } = await sb.rpc('accept_trade_request', { p_request_id: requestId });
  if (error) throw error;
}

// 스토어 페이지에서 앱 정보 긁어오기 — 브라우저 직접 요청은 CORS 로 막히므로
// 엣지 함수를 거친다.
export async function fetchStoreMeta(pkgOrUrl) {
  const { data, error } = await sb.functions.invoke('store-meta', {
    body: { q: pkgOrUrl },
  });
  if (error) throw error;
  return data;
}

// ---- 표시용 ----
export function pkgFromUrl(v) {
  const s = String(v || '').trim();
  // 스토어 링크: .../store/apps/details?id=kr.foo.bar&hl=ko
  const m = s.match(/[?&]id=([A-Za-z0-9_.]+)/);
  if (m) return m[1];
  // 옵트인 링크: .../apps/testing/kr.foo.bar
  // 비공개 테스트 중인 앱은 스토어 페이지가 안 보이는 경우가 많아,
  // 개발자가 실제로 들고 있는 링크는 대개 이쪽이다.
  const o = s.match(/\/apps\/testing\/([A-Za-z0-9_.]+)/);
  if (o) return o[1];
  return /^[A-Za-z0-9_]+(\.[A-Za-z0-9_]+)+$/.test(s) ? s : '';
}

export function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g,
    (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

export function iconHtml(url, name, cls = 'app-icon') {
  if (url) return `<img class="${cls}" src="${esc(url)}" alt="" loading="lazy">`;
  const ch = (name || '?').trim().charAt(0).toUpperCase();
  return `<div class="${cls} ph">${esc(ch)}</div>`;
}

export function ago(iso) {
  if (!iso) return '';
  const d = Math.floor((Date.now() - new Date(iso).getTime()) / 60000);
  if (d < 60) return `${d}m ago`;
  if (d < 1440) return `${Math.floor(d / 60)}h ago`;
  return `${Math.floor(d / 1440)}d ago`;
}

/** 헤더 우측 인증 영역. 구글 로그인이라 가입·로그인이 같은 버튼이다 —
 *  처음 누르면 계정이 만들어지고, 그다음부터는 로그인이 된다. */
export async function mountAuth(slotId, t) {
  const el = document.getElementById(slotId);
  if (!el) return;
  const user = await me().catch(() => null);
  if (user) {
    // 구글 계정 이름(박준형)이 아니라 ACT 에서 쓰는 개발자명(zenith.studio)이어야
    // 한다. 보드·앱카드·채팅에 전부 개발자명으로 나오는데 헤더만 달랐다.
    let label = user.user_metadata?.name || user.email || '';
    try {
      const { data } = await sb.from('profiles')
        .select('developer_name, nickname').eq('id', user.id).maybeSingle();
      label = data?.developer_name || data?.nickname || label;
    } catch (_) {}
    el.innerHTML =
      // "내 앱"은 로그인한 사람만 갈 곳이다. 공개 메뉴가 아니라
      // 계정 쪽에 붙어야 어디로 가는 링크인지 읽힌다.
      `<a href="/console.html" class="mine">${t('nav_myapps')}</a>` +

      `<a href="/console.html" class="who-me" style="font-size:13px">` +
      `<span class="emo">🧑</span>${esc(label)}</a>` +
      `<a href="#" id="soBtn" style="font-size:13px;margin-left:12px">${t('sign_out')}</a>`;
    document.getElementById('soBtn').onclick = (e) => { e.preventDefault(); signOut(); };
    mountBell(t);
  } else {
    el.innerHTML =
      `<a href="#" id="siBtn" style="font-size:13px">${t('sign_in')}</a>` +
      `<a href="#" id="suBtn" class="btn sm" style="margin-left:10px;color:var(--ink900)">${t('sign_up')}</a>`;
    const go = (e) => { e.preventDefault(); signIn().catch((x) => alert(x.message || x)); };
    document.getElementById('siBtn').onclick = go;
    document.getElementById('suBtn').onclick = go;
  }
}

/** 인증 달력. 앱의 TradeDayStrip 과 같은 규칙 —
 *  위 줄은 내가 연 날(분), 아래 줄은 상대가 내 앱을 연 날. */
export function dayStrip(ex, peerDays) {
  const days = ex.days ?? 14;
  const start = new Date((ex.started_on || '') + 'T00:00:00');
  if (isNaN(start)) return '';
  const today = new Date(); today.setHours(0, 0, 0, 0);
  const key = (d) => d.toISOString().slice(0, 10);
  const mine = {};
  for (const c of ex.exchange_checkins || []) mine[c.day_date] = c.minutes ?? 0;

  const labels = [], mineRow = [], peerRow = [];
  for (let i = 0; i < days; i++) {
    const d = new Date(start); d.setDate(start.getDate() + i);
    const k = key(d);
    const isToday = k === key(today);
    const future = d > today;
    labels.push(`<div class="lbl${isToday ? ' today' : ''}">${d.getDate()}</div>`);

    const m = mine[k];
    mineRow.push(`<div class="cell${m !== undefined ? ' done' : future ? ' future' : ''}">${
      m ? m : m !== undefined ? '✓' : ''}</div>`);

    if (peerDays) {
      const pm = peerDays[k];
      peerRow.push(`<div class="cell${pm !== undefined ? ' peer' : future ? ' future' : ''}">${
        pm ? pm : pm !== undefined ? '✓' : ''}</div>`);
    }
  }
  const cols = `grid-template-columns:repeat(${days},1fr)`;
  return `<div class="strip" style="${cols}">${labels.join('')}</div>
    <div class="strip" style="${cols}">${mineRow.join('')}</div>
    ${peerDays ? `<div class="strip" style="${cols}">${peerRow.join('')}</div>` : ''}`;
}

/** 상대가 내 앱을 연 날 — 앱의 peer_check_days 와 같은 RPC */
export async function peerCheckDays(packages) {
  if (!packages.length) return {};
  try {
    const { data } = await sb.rpc('peer_check_days', { p_packages: packages });
    const out = {};
    for (const r of data ?? []) {
      (out[r.package_name] ??= {})[r.day_date] = r.minutes ?? 0;
    }
    return out;
  } catch (_) { return {}; }
}

// ---- 채팅 ----
export async function myTradeChats() {
  const { data } = await sb.rpc('my_trade_chats');
  return data ?? [];
}

export async function tradeMessages(requestId) {
  const { data, error } = await sb
    .from('trade_messages').select('*')
    .eq('request_id', requestId).order('created_at');
  if (error) throw error;
  return data ?? [];
}

export async function sendTradeMessage(requestId, body) {
  const uid = (await me())?.id;
  const { data, error } = await sb.from('trade_messages')
    .insert({ request_id: requestId, sender_id: uid, body }).select();
  if (error) throw error;
  return data?.[0];
}

export async function markTradeRead(requestId) {
  try { await sb.rpc('mark_trade_read', { p_request_id: requestId }); } catch (_) {}
}

export async function ensureThread(exchangeId) {
  const { data } = await sb.rpc('ensure_trade_thread', { p_exchange_id: exchangeId });
  return data ?? null;
}

/** 새 메시지를 실시간으로 받는다. 반환값을 호출하면 구독이 끊긴다. */
export function watchTrade(requestId, onRow) {
  const ch = sb.channel(`tm-${requestId}`)
    .on('postgres_changes',
        { event: 'INSERT', schema: 'public', table: 'trade_messages',
          filter: `request_id=eq.${requestId}` },
        (p) => onRow(p.new))
    .subscribe();
  return () => sb.removeChannel(ch);
}

// ---- 피드백 ----
export async function myFeedbacks() {
  const { data } = await sb.rpc('my_feedbacks');
  return data ?? [];
}

export async function mySentFeedbacks() {
  const { data } = await sb.rpc('my_sent_feedbacks');
  return data ?? [];
}

export async function sendFeedback(appId, body) {
  const uid = (await me())?.id;
  const { error } = await sb.from('feedbacks')
    .insert({ app_id: appId, author_id: uid, body });
  if (error) throw error;
}

export async function replyFeedback(feedbackId, body) {
  const uid = (await me())?.id;
  const { error } = await sb.from('feedback_replies')
    .insert({ feedback_id: feedbackId, author_id: uid, body });
  if (error) throw error;
}

// ---- 테스터 이메일 (그룹 대신 이메일 목록으로 받는 앱) ----
export async function testerEmails(appId) {
  const { data, error } = await sb
    .from('tester_emails')
    .select('tester_id, email, registered, created_at')
    .eq('app_id', appId).order('created_at');
  if (error) throw error;
  return data ?? [];
}

export async function markEmailRegistered(appId, testerId, on) {
  const { error } = await sb.from('tester_emails')
    .update({ registered: on }).eq('app_id', appId).eq('tester_id', testerId);
  if (error) throw error;
}

// ---- 그룹 공개 여부 ----
export async function checkGroup(urlOrName) {
  const { data, error } = await sb.functions.invoke('group-check', {
    body: { q: urlOrName },
  });
  if (error) throw error;
  return data;
}

// ---- 옵트인 관문 ----
/// 테스터가 "들어가졌다 / 안 된다" 를 한 번 누른다.
export async function reportOptin(appId, ok) {
  const { error } = await sb.rpc('report_optin', { p_app_id: appId, p_ok: ok });
  if (error) throw error;
}

/// 주인이 고쳤다고 표시하면 보드 배지를 내린다.
export async function clearOptinFlag(appId) {
  const { error } = await sb.rpc('clear_optin_flag', { p_app_id: appId });
  if (error) throw error;
}

/// 패키지명으로 앱을 찾는다 — exchanges 는 app_id 가 아니라 패키지명을 들고 있다.
export async function appIdByPackage(pkg) {
  if (!pkg) return null;
  const { data } = await sb.from('apps').select('id').eq('package_name', pkg).limit(1);
  return data?.[0]?.id ?? null;
}

// ---- 헤더 알림함 ----
// 콘솔 탭 배지는 콘솔에 있을 때만 보인다. 보드를 보고 있든 가이드를 읽고
// 있든, 새 신청·메시지·피드백은 한 곳에서 보여야 한다. notifications 는
// 실시간 퍼블리케이션에 올려 뒀으므로 새로고침 없이 들어온다.
/// 알림 종류마다 갈 곳이 다르다. 전부 콘솔로 보내면 눌러 놓고
/// 다시 찾아 들어가야 한다. 콘솔이 아닌 곳으로 가는 것도 있다 —
/// 새 앱이 보드에 올라왔다는 알림은 내 앱이 아니라 보드로 가야 한다.
function hrefOf(r) {
  const kind = r?.kind;
  const pkg = r?.data?.package_name || r?.data?.package;
  switch (kind) {
    case 'app_board': {
      // 푸시 payload 에는 app_id 만 실린다 — 상세를 id 로도 열 수 있게 해 뒀다
      const id = r?.data?.app_id;
      if (pkg) return `/app.html?p=${encodeURIComponent(pkg)}`;
      return id ? `/app.html?id=${encodeURIComponent(id)}` : '/';
    }
    case 'trade_chat': {
      // 목록까지만 보내면 어느 방에서 온 알림인지 다시 찾아야 한다
      const rid = r?.data?.request_id;
      return rid ? `/console.html#chat=${rid}` : '/console.html#chats';
    }
    case 'support': return '/console.html#contact';
    case 'chat': return '/console.html#chats';
    case 'trade_feedback': case 'feedback_reply': return '/console.html#feedback';
    case 'trade_request': return '/console.html#offers';
    case 'trade_request_result': case 'peer_checkin': case 'trade_nudge':
    case 'country_block': return '/console.html#testing';
    case 'optin_broken': case 'tester_email': case 'tester_email_ok':
    case 'my_apps': return '/console.html#apps';
    default: return '/console.html';
  }
}

async function mountBell(t) {
  // 헤더 메뉴에 끼워 넣으니 공개 메뉴들과 섞여 무엇이 내 것인지 흐려졌다.
  // 화면 오른쪽 위에 따로 띄운다 — 서랍도 그쪽에서 열린다.
  let btn = document.getElementById('notiFab');
  if (!btn) {
    btn = document.createElement('button');
    btn.id = 'notiFab';
    btn.className = 'noti-fab';
    btn.type = 'button';
    btn.title = t('noti_h');
    btn.setAttribute('aria-label', t('noti_h'));
    btn.innerHTML =
      `<span class="arrow">◀</span><span class="lbl">${t('noti_h')}</span>` +
      `<i id="bellN"></i>`;
    document.body.appendChild(btn);
  }
  const dot = document.getElementById('bellN');

  // 헤더에서 아래로 펼치는 목록은 본문을 통째로 가린다. 알림이 열 개만 넘어도
  // 화면 절반이 덮인다. 왼쪽에 붙이고 접었다 폈다 하게 한다.
  let drawer = document.getElementById('notiDrawer');
  if (!drawer) {
    drawer = document.createElement('aside');
    drawer.id = 'notiDrawer';
    drawer.className = 'noti';
    drawer.innerHTML =
      `<div class="head"><b>${t('noti_h')}</b>
        <button class="x" id="notiClose" aria-label="close">✕</button></div>
       <div class="list" id="notiList"></div>`;
    document.body.appendChild(drawer);
    const back = document.createElement('div');
    back.id = 'notiBack';
    back.className = 'noti-back';
    document.body.appendChild(back);
    back.onclick = () => setOpen(false);
    document.getElementById('notiClose').onclick = () => setOpen(false);
  }
  const list = document.getElementById('notiList');
  const back = document.getElementById('notiBack');
  let rows = [];

  const setOpen = (on) => {
    document.body.classList.toggle('noti-open', on);
    try { localStorage.setItem('act_noti', on ? '1' : '0'); } catch (_) {}
    if (on) markRead();
  };

  let lastUnread = 0;
  const paint = () => {
    const un = rows.filter((r) => !r.read_at).length;
    dot.textContent = un > 0 ? String(un) : '';
    dot.style.display = un > 0 ? '' : 'none';
    // 안 읽은 게 있으면 메뉴 글자에 불이 들어온다.
    // 숫자만 있으면 작아서, 스크롤 중에는 눈에 안 들어온다.
    btn.classList.toggle('has', un > 0);
    if (un > lastUnread) {
      btn.classList.remove('ping');
      void btn.offsetWidth;      // 애니메이션을 다시 트는 표준 수법
      btn.classList.add('ping');
    }
    lastUnread = un;
    list.innerHTML = rows.length
      ? rows.map((r) => `
        <div class="ni${r.read_at ? '' : ' new'}" data-nid="${r.id}">
          <p class="t">${esc(r.title || '')}</p>
          ${r.body ? `<p class="b">${esc(r.body)}</p>` : ''}
          <p class="a">${ago(r.created_at)}</p>
        </div>`).join('')
      : `<p class="muted" style="padding:16px">${t('no_noti')}</p>`;
    list.querySelectorAll('[data-nid]').forEach((el) => {
      const r = rows.find((x) => String(x.id) === el.dataset.nid);
      el.onclick = () => {
        const url = hrefOf(r);
        const [path, hash] = url.split('#');
        setOpen(false);
        // 이미 그 페이지에 있으면 해시만 바뀌고 아무 일도 안 일어난다.
        // 보고 있던 탭에 그대로 남는다 — 직접 알려 줘야 한다.
        if (location.pathname === path || (path === '/' && location.pathname === '/')) {
          location.hash = hash ? '#' + hash : '';
          dispatchEvent(new PopStateEvent('popstate'));
        } else {
          location.href = url;
        }
      };
    });
  };

  const markRead = async () => {
    const ids = rows.filter((r) => !r.read_at).map((r) => r.id);
    if (!ids.length) return;
    const now = new Date().toISOString();
    rows = rows.map((r) => ({ ...r, read_at: r.read_at ?? now }));
    paint();
    try { await sb.from('notifications').update({ read_at: now }).in('id', ids); }
    catch (_) {}
  };

  const { data } = await sb.from('notifications')
    .select('id,title,body,kind,data,read_at,created_at')
    .order('created_at', { ascending: false }).limit(15);
  rows = data ?? [];
  paint();

  sb.channel('noti')
    .on('postgres_changes',
        { event: 'INSERT', schema: 'public', table: 'notifications' },
        (p) => {
          rows.unshift(p.new);
          rows = rows.slice(0, 15);
          paint();
          // 열어 둔 채로 새 알림이 오면 그것도 읽은 것으로 친다
          if (document.body.classList.contains('noti-open')) markRead();
        })
    .subscribe();

  btn.onclick = (e) => {
    e.stopPropagation();
    setOpen(!document.body.classList.contains('noti-open'));
  };
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') setOpen(false);
  });

  // 지난번에 열어 뒀으면 그대로 열어 준다
  let was = '0';
  try { was = localStorage.getItem('act_noti') ?? '0'; } catch (_) {}
  if (was === '1' && innerWidth > 900) document.body.classList.add('noti-open');
}

/// 기간이 끝난 내 품앗이를 완주로 정리한다. 체크인이 끊긴 건은
/// 체크인 경로로 안 닫히므로, 콘솔을 열 때 한 번 훑는다.
export async function closeElapsed() {
  try { await sb.rpc('close_elapsed_exchanges', { p_owner: null }); } catch (_) {}
}

// ---- 관리자 문의 (앱의 support_messages 와 같은 방) ----
export async function supportMessages() {
  const uid = (await me())?.id;
  if (!uid) return [];
  const { data, error } = await sb.from('support_messages')
    .select('*').eq('user_id', uid).order('created_at');
  if (error) throw error;
  return data ?? [];
}

export async function sendSupportMessage(body) {
  const uid = (await me())?.id;
  if (!uid) throw new Error('signin');
  const { data, error } = await sb.from('support_messages')
    .insert({ user_id: uid, sender_id: uid, body }).select();
  if (error) throw error;
  return data?.[0];
}

export async function supportMarkRead() {
  const uid = (await me())?.id;
  if (!uid) return;
  try { await sb.rpc('support_mark_read', { p_user: uid }); } catch (_) {}
}

export function watchSupport(userId, onRow) {
  const ch = sb.channel(`sup-${userId}`)
    .on('postgres_changes',
        { event: 'INSERT', schema: 'public', table: 'support_messages',
          filter: `user_id=eq.${userId}` },
        (p) => onRow(p.new))
    .subscribe();
  return () => sb.removeChannel(ch);
}

/// 품앗이 준비 단계 표시 — 그룹 가입·옵트인은 웹에서도 할 수 있다.
/// 설치 확인만 안드로이드 앱이 한다(사용 기록을 읽어야 알 수 있다).
export async function setSetupStep(exchangeId, field, on) {
  const allowed = ['setup_group_done', 'setup_optin_done'];
  if (!allowed.includes(field)) throw new Error('bad field');
  const { error } = await sb.from('exchanges')
    .update({ [field]: on }).eq('id', exchangeId);
  if (error) throw error;
}

/// 밖에서 따로 구한 품앗이를 직접 넣는다. 레딧이나 텔레그램에서 잡아 온 건
/// 여기 없으니, 손으로 넣어야 인증 달력이 돈다.
export async function addExchange(x) {
  const uid = (await me())?.id;
  if (!uid) throw new Error('signin');
  const row = {
    owner_id: uid,
    peer_app_name: x.peer_app_name,
    days: x.days ?? 14,
  };
  for (const k of ['peer_package', 'peer_group_url', 'peer_optin_url',
                   'peer_handle', 'peer_icon_url', 'my_app_id', 'source']) {
    if (x[k]) row[k] = x[k];
  }
  const { data, error } = await sb.from('exchanges').insert(row).select('id');
  if (error) throw error;
  return data?.[0]?.id;
}

/// 앱 스크린샷 한 장. 경로를 <uid>/ 로 시작해야 정책이 통과한다.
export async function uploadShot(file) {
  const uid = (await me())?.id;
  if (!uid) throw new Error('signin');
  if (!/^image\//.test(file.type)) throw new Error('image only');
  if (file.size > 5 * 1024 * 1024) throw new Error('too big');
  const ext = (file.name.split('.').pop() || 'jpg').toLowerCase().slice(0, 5);
  const path = `${uid}/${crypto.randomUUID()}.${ext}`;
  const { error } = await sb.storage.from('app-shots')
    .upload(path, file, { contentType: file.type, upsert: false });
  if (error) throw error;
  return sb.storage.from('app-shots').getPublicUrl(path).data.publicUrl;
}

// ---- 개발자명 ----
export async function myProfile() {
  const uid = (await me())?.id;
  if (!uid) return null;
  const { data } = await sb.from('profiles')
    .select('id, developer_name, nickname, country, karma, completed_count')
    .eq('id', uid).maybeSingle();
  return data ?? null;
}

export async function saveDeveloperName(name) {
  const uid = (await me())?.id;
  if (!uid) throw new Error('signin');
  const v = String(name || '').trim().slice(0, 40);
  if (!v) throw new Error('empty');
  const { error } = await sb.from('profiles')
    .update({ developer_name: v }).eq('id', uid);
  if (error) throw error;
  return v;
}

// ---- 게시판 ----
export async function posts() {
  const { data } = await sb.rpc('community_list');
  return data ?? [];
}

export async function post(id) {
  const { data } = await sb.rpc('community_post', { p_id: id });
  return data ?? null;
}

export async function addPost(category, title, content) {
  const uid = (await me())?.id;
  if (!uid) throw new Error('signin');
  const { error } = await sb.from('community_posts')
    .insert({ author_id: uid, category, title, content, lang: LANG_OF() });
  if (error) throw error;
}

export async function addComment(postId, body) {
  const uid = (await me())?.id;
  if (!uid) throw new Error('signin');
  const { error } = await sb.from('community_comments')
    .insert({ post_id: postId, author_id: uid, body });
  if (error) throw error;
}

export async function deletePost(id) {
  const { error } = await sb.from('community_posts').delete().eq('id', id);
  if (error) throw error;
}

/// 글에 언어를 같이 저장한다 — 나중에 언어별로 걸러 보여 줄 수 있게.
function LANG_OF() {
  try { return (document.documentElement.lang || 'en').slice(0, 7); }
  catch (_) { return 'en'; }
}

/// 품앗이 상대 앱에 남기는 비공개 피드백. exchange_id 를 같이 넣어야
/// 상대 화면에서 어느 품앗이에서 온 말인지 이어진다.
export async function sendTradeFeedback(exchangeId, appId, body) {
  const uid = (await me())?.id;
  if (!uid) throw new Error('signin');
  const { error } = await sb.from('feedbacks').insert({
    author_id: uid, app_id: appId, exchange_id: exchangeId, body,
  });
  if (error) throw error;
}

// ---- 찌르기 ----
/// 서버가 조건을 검사하고 결과를 문자열로 돌려준다:
/// ok / self(내가 오늘 안 엶) / already(상대가 이미 엶) / sent_today / nopeer
export async function nudgePeer(exchangeId) {
  const { data, error } = await sb.rpc('nudge_peer', { p_exchange_id: exchangeId });
  if (error) throw error;
  return data;
}

// ---- 차단 · 신고 ----
export async function blockUser(userId) {
  const uid = (await me())?.id;
  if (!uid) throw new Error('signin');
  const { error } = await sb.from('blocks')
    .insert({ blocker_id: uid, blocked_id: userId });
  if (error && error.code !== '23505') throw error;
}

export async function unblockUser(userId) {
  const uid = (await me())?.id;
  if (!uid) return;
  await sb.from('blocks').delete().eq('blocker_id', uid).eq('blocked_id', userId);
}

export async function myBlocks() {
  const uid = (await me())?.id;
  if (!uid) return [];
  const { data } = await sb.from('blocks').select('blocked_id').eq('blocker_id', uid);
  return (data ?? []).map((r) => r.blocked_id);
}

export async function reportSomething(targetType, targetId, targetUserId, reason, detail) {
  const uid = (await me())?.id;
  if (!uid) throw new Error('signin');
  const { error } = await sb.from('reports').insert({
    reporter_id: uid, target_type: targetType, target_id: String(targetId ?? ''),
    target_user_id: targetUserId || null, reason, detail: detail || null,
  });
  if (error) throw error;
}

// ---- 사진 올리기 ----
/// bucket 마다 규칙이 다르다. app-shots 만 <uid>/ 로 시작해야 한다.
export async function uploadImage(bucket, file) {
  const uid = (await me())?.id;
  if (!uid) throw new Error('signin');
  if (!/^image\//.test(file.type)) throw new Error('image only');
  if (file.size > 5 * 1024 * 1024) throw new Error('too big');
  const ext = (file.name.split('.').pop() || 'jpg').toLowerCase().slice(0, 5);
  const path = `${uid}/${crypto.randomUUID()}.${ext}`;
  const { error } = await sb.storage.from(bucket)
    .upload(path, file, { contentType: file.type, upsert: false });
  if (error) throw error;
  return sb.storage.from(bucket).getPublicUrl(path).data.publicUrl;
}

export async function sendTradeImage(requestId, url) {
  const uid = (await me())?.id;
  const { data, error } = await sb.from('trade_messages')
    .insert({ request_id: requestId, sender_id: uid, body: '', image_url: url }).select();
  if (error) throw error;
  return data?.[0];
}

export async function sendSupportImage(url) {
  const uid = (await me())?.id;
  const { data, error } = await sb.from('support_messages')
    .insert({ user_id: uid, sender_id: uid, body: '', image_url: url }).select();
  if (error) throw error;
  return data?.[0];
}

// ---- 파티 ----
export async function openParties() {
  const { data } = await sb.rpc('open_parties');
  return data ?? [];
}

export async function joinParty(partyId, appId, password) {
  const { error } = await sb.rpc('join_party', {
    p_party_id: partyId, p_app_id: appId, p_password: password || null });
  if (error) throw error;
}

export async function leaveParty(partyId) {
  const { error } = await sb.rpc('leave_party', { p_party_id: partyId });
  if (error) throw error;
}

export async function createParty(name, lang, capacity, minKarma, appId, password) {
  const { data, error } = await sb.rpc('create_party', {
    p_name: name, p_lang: lang, p_capacity: capacity,
    p_min_karma: minKarma, p_app_id: appId, p_password: password || null });
  if (error) throw error;
  return data;
}

export async function partyMembers(partyId) {
  const { data } = await sb.rpc('party_install_status', { p_party_id: partyId });
  return data ?? [];
}

// ---- 지우기 · 고치기 ----
export async function deleteApp(id) {
  const { error } = await sb.from('apps').delete().eq('id', id);
  if (error) throw error;
}

export async function deleteExchange(id) {
  const { error } = await sb.from('exchanges').delete().eq('id', id);
  if (error) throw error;
}

export async function updateExchange(id, patch) {
  const { error } = await sb.from('exchanges').update(patch).eq('id', id);
  if (error) throw error;
}

/// 품앗이 상대가 누구인지. 패키지명만 대조하면 놓친다 —
/// 상대가 임시 패키지명으로 올려 뒀거나 손으로 넣은 품앗이도 있다.
/// 서버가 counterpart_id → 패키지명 → 앱 이름 순으로 찾아 준다.
export async function peerIdentity(exchangeIds) {
  const list = [...new Set((exchangeIds || []).filter(Boolean))];
  if (!list.length) return {};
  const { data } = await sb.rpc('peer_identity', { p_exchange_ids: list });
  return Object.fromEntries((data ?? []).map((r) => [r.exchange_id, r]));
}
