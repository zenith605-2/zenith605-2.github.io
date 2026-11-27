"""네이버·빙(IndexNow)에 주소 제출. 2026-11-27: Aside 크레딧이 떨어져 네이버 웹 페이지 수집을 대신함.
사용: python3 indexnow_submit.py /ko/new-page.html /other.html
키 파일은 사이트 루트 6b74258fa5576c1799c15663211617fa.txt (지우지 말 것)."""
import json, sys, urllib.request, urllib.error
K = '6b74258fa5576c1799c15663211617fa'
urls = ['https://actparty.app' + p for p in sys.argv[1:]]
if not urls: sys.exit(__doc__)
body = json.dumps({"host": "actparty.app", "key": K, "keyLocation": f"https://actparty.app/{K}.txt", "urlList": urls}).encode()
for ep in ['https://searchadvisor.naver.com/indexnow', 'https://api.indexnow.org/indexnow']:
    r = urllib.request.Request(ep, data=body, headers={'Content-Type': 'application/json; charset=utf-8'})
    try:
        print(ep, urllib.request.urlopen(r, timeout=30).status)
    except urllib.error.HTTPError as e:
        print(ep, e.code, e.read()[:200])
