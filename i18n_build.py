"""가이드를 언어별 URL 로 굽는다.

가이드 본문은 각 파일의 <script> 안 DOC 객체에 다섯 언어로 들어 있고,
브라우저가 그중 하나를 골라 그린다. 사람에게는 충분하지만 구글은 자바스크립트
이후를 안 보고, 본다 해도 URL 하나에 언어 하나만 매긴다. 그래서 한국어·일본어
검색에는 우리 글이 없다.

    python web/i18n_build.py      (그다음 python web/build.py 로 사이트맵)

결과:
  web/{ko,ja,zh-Hans,zh-Hant}/guides/*.html  본문이 HTML 에 박힌 언어판
  영어 원본 <head> 에 hreflang 링크 추가 (한 번만, 이미 있으면 건너뜀)
  web/i18n_pages.json                          build.py 가 사이트맵에 넣을 경로들
"""
import html
import io
import json
import os
import re
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://actparty.app'
LANGS = ['ko', 'ja', 'zh-Hans', 'zh-Hant']          # 영어는 원본 URL 이 맡는다
ALL = ['en'] + LANGS
GUIDES_DIR = os.path.join(BASE, 'guides')
EXTRACT = os.path.join(BASE, 'tools', 'extract_docs.mjs')

# 언어 전환 줄에 쓰는 이름. 검색이 읽는 내부 링크이기도 하다.
LANG_NAME = {'en': 'English', 'ko': '한국어', 'ja': '日本語',
             'zh-Hans': '简体中文', 'zh-Hant': '繁體中文'}


def extract_docs(files):
    """Node 로 DOC 객체를 평가한다. 템플릿 리터럴 안의 ${SHOT()} 까지 그대로."""
    out = subprocess.run(['node', EXTRACT, *files], capture_output=True,
                         text=True, encoding='utf-8', check=True)
    return json.loads(out.stdout)


def alt_links(rel_path):
    """hreflang 묶음. rel_path 는 '/guides/x.html' 처럼 영어 URL 기준."""
    lines = [f'<link rel="alternate" hreflang="en" href="{SITE}{rel_path}">']
    for l in LANGS:
        lines.append(
            f'<link rel="alternate" hreflang="{l}" href="{SITE}/{l}{rel_path}">')
    lines.append(f'<link rel="alternate" hreflang="x-default" href="{SITE}{rel_path}">')
    return '\n'.join(lines)


def lang_bar(rel_path, current):
    """본문 위 한 줄 — 같은 글의 다른 언어판. 사람에게도, 크롤러에게도."""
    items = []
    for l in ALL:
        href = rel_path if l == 'en' else f'/{l}{rel_path}'
        if l == current:
            items.append(f'<b>{LANG_NAME[l]}</b>')
        else:
            items.append(f'<a href="{href}" hreflang="{l}">{LANG_NAME[l]}</a>')
    return ('<p class="muted" style="font-size:12.5px;margin:0 0 18px">'
            + ' · '.join(items) + '</p>')


def title_and_desc(doc_html, fallback_title, fallback_desc):
    """h1 과 그 아래 muted 한 줄을 제목·설명으로 쓴다. 번역을 따로 안 둬도
    글마다 이미 다섯 언어로 적혀 있는 문장이라 어긋나지 않는다."""
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', doc_html, re.S)
    sub = re.search(r'</h1>\s*<p class="muted"[^>]*>(.*?)</p>', doc_html, re.S)
    strip = lambda s: html.unescape(re.sub(r'<[^>]+>', '', s)).strip()
    title = strip(h1.group(1)) if h1 else fallback_title
    desc = strip(sub.group(1)) if sub else fallback_desc
    return title, desc


def localize_links(doc_html, lang):
    """본문 안의 /guides/... 링크는 같은 언어판으로 보낸다. 랜딩 페이지도."""
    doc_html = re.sub(r'href="/guides/', f'href="/{lang}/guides/', doc_html)
    for slug in ('google-play-12-testers', 'closed-testing-14-days', 'find-android-app-testers'):
        doc_html = doc_html.replace(f'href="/{slug}.html"', f'href="/{lang}/{slug}.html"')
    return doc_html


def build_lang_page(src, doc_html, lang, rel_path, en_title, en_desc):
    s = src
    title, desc = title_and_desc(doc_html, en_title, en_desc)
    s = re.sub(r'<html lang="[^"]*">', f'<html lang="{lang}">', s, count=1)
    s = re.sub(r'<title>.*?</title>', f'<title>{html.escape(title)} | ACT Party</title>',
               s, count=1, flags=re.S)
    s = re.sub(r'<meta name="description" content="[^"]*">',
               f'<meta name="description" content="{html.escape(desc, quote=True)}">',
               s, count=1)
    s = re.sub(r'<link rel="canonical" href="[^"]*">',
               f'<link rel="canonical" href="{SITE}/{lang}{rel_path}">\n' + alt_links(rel_path),
               s, count=1)
    # 본문을 HTML 에 박는다
    body = lang_bar(rel_path, lang) + localize_links(doc_html, lang)
    s = re.sub(r'(<article[^>]*id="doc"[^>]*>)(</article>)',
               lambda m: m.group(1) + body + m.group(2), s, count=1, flags=re.S)
    # 스크립트에서 DOC 정의와 본문 주입 줄을 뺀다 — 나머지(내비 번역·로그인)는 그대로
    s = re.sub(r'\nconst DOC = \{.*?\n\};\n', '\n', s, count=1, flags=re.S)
    s = re.sub(r"\ndocument\.getElementById\('doc'\)\.innerHTML = .*?;\n", '\n', s, count=1)
    return s


def add_hreflang_to_english(path, rel_path):
    s = io.open(path, encoding='utf-8').read()
    if 'hreflang="x-default"' in s:
        return False
    s = re.sub(r'(<link rel="canonical" href="[^"]*">)',
               lambda m: m.group(1) + '\n' + alt_links(rel_path), s, count=1)
    io.open(path, 'w', encoding='utf-8', newline='').write(s)
    return True


def main():
    files = sorted(f for f in os.listdir(GUIDES_DIR) if f.endswith('.html'))
    docs = extract_docs([os.path.join(GUIDES_DIR, f) for f in files])
    pages = []
    for f in files:
        d = docs.get(f) or {}
        if 'error' in d or 'en' not in d:
            print(f'건너뜀 {f}: {d.get("error", "DOC 없음")}')
            continue
        src_path = os.path.join(GUIDES_DIR, f)
        src = io.open(src_path, encoding='utf-8').read()
        rel = '/guides/' + ('' if f == 'index.html' else f)
        en_title = re.search(r'<title>(.*?)</title>', src, re.S).group(1)
        en_desc = (re.search(r'<meta name="description" content="([^"]*)">', src) or [None, ''])[1]
        for lang in LANGS:
            if lang not in d:
                continue
            out_dir = os.path.join(BASE, lang, 'guides')
            os.makedirs(out_dir, exist_ok=True)
            page = build_lang_page(src, d[lang], lang, rel, en_title, en_desc)
            io.open(os.path.join(out_dir, f), 'w', encoding='utf-8', newline='').write(page)
            pages.append(f'/{lang}{rel}')
        if add_hreflang_to_english(src_path, rel):
            print(f'hreflang 추가: {f}')
    io.open(os.path.join(BASE, 'i18n_pages.json'), 'w', encoding='utf-8').write(
        json.dumps(pages, ensure_ascii=False, indent=1))
    print(f'언어판 {len(pages)}개 생성')


if __name__ == '__main__':
    sys.exit(main())
