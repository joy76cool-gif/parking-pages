import re,html,sys
def md(t):
    out=[];tb=[];inl=False
    def il(s):
        s=html.escape(s); s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s); s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
        s=re.sub(r'(https?://[^\s<）)]+)',r'<a href="\1" target="_blank" rel="noopener">\1</a>',s); return s
    def flush():
        nonlocal tb
        if tb:
            rows=[r for r in tb if not re.match(r'^\|[\s\-:|]+\|$',r)]
            h='<div class="wrap"><table>'
            for i,r in enumerate(rows):
                cells=[c.strip() for c in r.strip().strip('|').split('|')]
                tag='th' if i==0 else 'td'
                h+='<tr>'+''.join(f'<{tag}>{il(c)}</{tag}>' for c in cells)+'</tr>'
            out.append(h+'</table></div>'); tb=[]
    for line in t.splitlines():
        if line.startswith('|'): tb.append(line); continue
        flush()
        m=re.match(r'^(#{1,4})\s+(.*)',line)
        if m: n=len(m.group(1))+1; out.append(f'<h{min(n,4)}>{il(m.group(2))}</h{min(n,4)}>'); continue
        if re.match(r'^\s*[-*]\s+',line): out.append('<div class="li">• '+il(re.sub(r'^\s*[-*]\s+','',line))+'</div>'); continue
        if line.startswith('>'): out.append('<div class="note">'+il(line.lstrip('> '))+'</div>'); continue
        if line.strip(): out.append('<p>'+il(line)+'</p>')
    flush(); return '\n'.join(out)
import openpyxl
def xl_html(f):
    wb=openpyxl.load_workbook(f); out=''
    for ws in wb.worksheets:
        out+=f'<details><summary>報價表：{html.escape(ws.title)}</summary><div class="wrap"><table>'
        for r in ws.iter_rows(values_only=True):
            if not any(c not in (None,'') for c in r): continue
            def fmt(c):
                if isinstance(c,(int,float)): return f'{c:,.0f}'
                return html.escape(str(c)) if c is not None else ''
            out+='<tr>'+''.join(f'<td>{fmt(c)}</td>' for c in r)+'</tr>'
        out+='</table></div></details>'
    return out
eq=open('板橋_設備詢價單草稿.md',encoding='utf-8').read()
zo=open('板橋_15筆地號使用分區.md',encoding='utf-8').read()
top=open('板橋三件_摘要.html',encoding='utf-8').read()
css=''':root{--bad:#e50012;--bg:#fbfaf7;--fg:#231815;--muted:#6b6862;--line:#e3dfd6;--card:#fff;--acc:#231815;--warn:#9c938c;--in:#f4f1ea}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#171816;--fg:#ecebe6;--muted:#a3a19a;--line:#33342f;--card:#20211e;--acc:#f2efe9;--bad:#ff6b6b;--warn:#6f6862;--in:#2a2b27}}
:root[data-theme="dark"]{--bg:#171816;--fg:#ecebe6;--muted:#a3a19a;--line:#33342f;--card:#20211e;--acc:#f2efe9;--bad:#ff6b6b;--warn:#6f6862;--in:#2a2b27}
*{box-sizing:border-box}body{background:var(--bg);color:var(--fg);font:15.5px/1.65 "Noto Sans TC",system-ui,sans-serif;margin:0;padding:20px 16px}main{max-width:1560px;margin:0 auto}
h1{font-size:22px;margin:0 0 6px}h2{font-size:18px;margin:22px 0 8px}h3{font-size:16px;margin:16px 0 6px}h4{font-size:15px;margin:12px 0 4px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 16px;margin:10px 0}.big{font-size:26px;font-weight:700;color:var(--acc)}
.sub{color:var(--muted);font-size:13.5px}.note{background:var(--in);border-left:4px solid var(--warn);padding:6px 10px;margin:6px 0;font-size:14px}
.li{margin:2px 0 2px 6px}.wrap{overflow:auto;border:1px solid var(--line);border-radius:8px;margin:8px 0;background:var(--card)}
table{border-collapse:collapse;width:100%;font-size:13.5px}th,td{padding:5px 7px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}th{color:var(--muted);white-space:nowrap}
details{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:8px 14px;margin:10px 0}summary{cursor:pointer;font-weight:600}a{color:var(--acc);word-break:break-all}code{font-size:12.5px}'''
xl=xl_html('板橋_設備清單報價表.xlsx')
doc=f'<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>板橋信義國小</title><style>{css}</style></head><body><main>{top}{xl}<details><summary>設備詢價單草稿全文（舊版：第 4 節數字沒含車格前 18 支鏡頭）（含舊價出處、給廠商的清單在第 7 節）</summary>{md(eq)}</details><details><summary>15 筆地號使用分區全文</summary>{md(zo)}</details></main></body></html>'
open('板橋三件.html','w',encoding='utf-8').write(doc)
import runpy, os as _os
_ff = runpy.run_path(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'fold_folder.py'))
_t = open('板橋三件.html', encoding='utf-8').read(); open('板橋三件.html', 'w', encoding='utf-8').write(_ff['fix'](_t)[0])
