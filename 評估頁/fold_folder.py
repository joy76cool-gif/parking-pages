"""把案件頁「資料夾」那一行改成：摘要只放一顆「複製 NAS 位置」按鈕，完整路徑收進點開的區塊。
用法：python fold_folder.py 檔1.html 檔2.html ...（直接改檔）"""
import re, sys, html

PAT = re.compile(r'<details><summary><span class="k">資料夾</span><span class="a"[^>]*>(.*?)</span></summary><div class="src">(.*?)</div></details>', re.S)
BTN = re.compile(r'<button type="button" class="cp"[^>]*>.*?</button>　?[^<]*', re.S)
CSS = ('<style>.cp{font:inherit;font-size:13px;border:1px solid var(--line);border-radius:6px;background:var(--card);'
       'color:var(--fg);padding:3px 10px;cursor:pointer}.cp.big{font-weight:600}</style>')
JS = ('<script>document.addEventListener("click",e=>{const b=e.target.closest(".cp");if(!b)return;e.preventDefault();e.stopPropagation();'
      'const t=b.dataset.cp;const old=b.dataset.label||b.textContent;b.dataset.label=old;'
      'const done=()=>{b.textContent="已複製 ✓";setTimeout(()=>b.textContent=old,1800)};'
      'if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(done,()=>{fb(t);done()})}else{fb(t);done()}});'
      'function fb(t){const a=document.createElement("textarea");a.value=t;document.body.appendChild(a);a.select();try{document.execCommand("copy")}catch(_){}a.remove()}</script>')

def fix(doc):
    def rep(m):
        path_html = m.group(1).strip()
        path = html.unescape(path_html)
        rest = BTN.sub('', m.group(2)).strip()
        rest = re.sub(r'(<br>\s*)+$', '', rest)
        attr = html.escape(path, quote=True)
        return ('<details><summary><span class="k">資料夾</span><span class="a">'
                f'<button type="button" class="cp big" data-cp="{attr}">按這裡複製 NAS 位置</button></span></summary>'
                f'<div class="src">完整位置（點路徑也能複製）：<span class="cp" data-cp="{attr}" title="按一下複製" style="border:0;background:none;padding:0;margin:0;font:inherit;color:inherit;overflow-wrap:anywhere;text-decoration:underline dotted">{path_html}</span><br>'
                '複製後貼到檔案總管上面的網址列，按 Enter 就會打開。'
                + (f'<br>{rest}' if rest else '') + '</div></details>')
    doc, n = PAT.subn(rep, doc)
    if n and 'id="cpjs"' not in doc:
        doc = re.sub(r'<script>document\.addEventListener\("click",e=>\{const b=e\.target\.closest\("\.cp"\).*?</script>', '', doc, flags=re.S)
        doc = doc.replace('</body>', CSS + JS.replace('<script>', '<script id="cpjs">', 1) + '</body>', 1)
    return doc, n

if __name__ == '__main__':
    for f in sys.argv[1:]:
        d = open(f, encoding='utf-8').read()
        d2, n = fix(d)
        open(f, 'w', encoding='utf-8').write(d2)
        print(f, '改了', n, '處')

def add_unslop(doc):
    import os
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'unslop_block.html')
    if 'id="unslop"' in doc or not os.path.exists(p): return doc
    u = open(p, encoding='utf-8').read()
    i = doc.rfind('</main>')
    return doc[:i] + u + '\n' + doc[i:] if i >= 0 else doc
_old_fix = fix
def fix(doc):
    d, n = _old_fix(doc)
    return add_unslop(d), n

def add_nascp(doc):
    import os
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nascp_block.html')
    if 'id="nascp"' in doc or not os.path.exists(p): return doc
    i = doc.rfind('</body>')
    return doc[:i] + open(p, encoding='utf-8').read() + '\n' + doc[i:] if i >= 0 else doc
_old_fix2 = fix
def fix(doc):
    d, n = _old_fix2(doc)
    return add_nascp(d), n
