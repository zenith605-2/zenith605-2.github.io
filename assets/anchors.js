// 가이드의 각 구간에 고유 주소와 복사 버튼을 단다.
//
// 막히는 화면 다섯 가지를 한 페이지에 모아 뒀더니, 남을 도와줄 때 "그 글
// 어딘가에 있다"고밖에 못 말했다. 구간마다 주소가 있으면 "당신은 2번"이라고
// 정확히 보낼 수 있다 (2026-09-14).
//
// 페이지를 쪼개지 않은 이유: 검색 순위가 흩어지고, 어차피 다섯 화면은
// 한 흐름에서 차례로 만나는 것들이다.

const LABEL = {
  ko: { copy: '링크 복사', done: '복사했어요' },
  en: { copy: 'Copy link', done: 'Copied' },
  ja: { copy: 'リンクをコピー', done: 'コピーしました' },
  zhHans: { copy: '复制链接', done: '已复制' },
  zhHant: { copy: '複製連結', done: '已複製' },
};

/// 본문을 그린 뒤에 부른다. h2 마다 #s1, #s2 … 를 매기고 복사 버튼을 붙인다.
///
/// 번호로 매기는 건 언어판마다 제목이 달라도 같은 구간을 가리키게 하려는
/// 것이다 — 한국어판 #s2 와 영어판 #s2 는 같은 화면이다.
export function sectionAnchors(lang) {
  const t = LABEL[lang] || LABEL.en;
  const doc = document.getElementById('doc');
  if (!doc) return;

  [...doc.querySelectorAll('h2')].forEach((h, i) => {
    const id = h.id || `s${i + 1}`;
    h.id = id;

    const btn = document.createElement('button');
    btn.className = 'anchor-copy';
    btn.type = 'button';
    btn.textContent = t.copy;
    btn.onclick = async () => {
      const url = location.origin + location.pathname + '#' + id;
      try {
        await navigator.clipboard.writeText(url);
      } catch {
        // 클립보드를 막아 둔 브라우저 — 주소창만이라도 바꿔 주면 복사할 수 있다
        location.hash = id;
        return;
      }
      btn.textContent = t.done;
      setTimeout(() => (btn.textContent = t.copy), 1600);
    };
    h.appendChild(btn);
  });

  // 주소에 #s2 를 달고 들어온 사람을 그 자리로 보낸다. 본문을 그린 뒤라
  // 브라우저가 놓친 상태다.
  if (location.hash) {
    const target = doc.querySelector(location.hash);
    if (target) target.scrollIntoView({ block: 'start' });
  }
}
