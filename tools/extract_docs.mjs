// 가이드 HTML 안의 <script type="module"> 에서 DOC 객체를 평가해 언어별 본문 HTML 을 JSON 으로 낸다.
import fs from 'node:fs';
import vm from 'node:vm';
import path from 'node:path';
const [,, ...files] = process.argv;
const out = {};
for (const f of files) {
  const src = fs.readFileSync(f, 'utf8');
  const m = src.match(/<script type="module">([\s\S]*?)<\/script>/);
  if (!m) { out[path.basename(f)] = { error: 'no module script' }; continue; }
  let js = m[1]
    .replace(/^\s*import .*$/gm, '')                       // import 제거
    .replace(/document\.getElementById[\s\S]*$/m, '');     // DOM 조작 이후 잘라냄
  js += '\n;__out = DOC;';
  const ctx = { __out: null, LANG: 'en', t: (k) => k, applyDom() {}, langPicker: () => '', wireLangPicker() {}, mountAuth() {} };
  try { vm.runInNewContext(js, ctx, { filename: f }); out[path.basename(f)] = ctx.__out; }
  catch (e) { out[path.basename(f)] = { error: String(e) }; }
}
process.stdout.write(JSON.stringify(out));
