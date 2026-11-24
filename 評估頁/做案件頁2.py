"""板橋第 20 版樣子的案件頁：python 做案件頁2.py 資料.json 設定.json 輸出.html
資料.json＝sonnet 整理、opus 核過的頁面資料；設定.json＝試算面板的設定（cfg）。"""
import json, sys, re, html
E = html.escape
d = json.load(open(sys.argv[1], encoding='utf-8'))
cfg = json.load(open(sys.argv[2], encoding='utf-8'))
base = open('板橋三件.html', encoding='utf-8').read()
head_css = base[base.index('<style>') + 7:base.index('</style>')]
summ = open('板橋三件_摘要.html', encoding='utf-8').read()
s1 = summ[summ.index('<style>') + 7:summ.index('</style>')]
s2a = summ.index(':root{--acc-text'); s2 = summ[s2a:summ.index('</style>', s2a)]
gloss = summ[summ.index('<h2>名詞（點開複習）</h2>'):summ.index('<h2>內部資料</h2>')]
panel = open('試算面板.html', encoding='utf-8').read().replace("data-cfg='CFG'", "data-cfg='" + html.escape(json.dumps(cfg, ensure_ascii=False), quote=True) + "'")

# 用跟試算面板一樣的算式，算預設值放在重點
D = cfg['def']; g = lambda k: D[k]
P = g('occ')/100; T = g('tHours'); N = cfg['n']; mr = g('rBiz') if g('area') == 'biz' else g('rRes'); nM = N * mr / 100; nT = N - nM
revM = nM * g('rentRate') / 100 * g('monthFee'); cr = D.get('collect', 100) / 100; revT = nT * P * g('hourFee') * 30 * T * cr; rev = revM + revT
ev = g('evCount'); evM = ev * mr / 100; evT = ev - evM; kwh = evM * g('evMonthKwh') + evT * g('kw') * T * 30 * g('evShare') / 100 * P
evRev = kwh * g('kwhPrice'); evCost = kwh * g('kwhCost'); ext = (D.get('motoN', 0) * P * D.get('motoFee', 0) * 30 + D.get('busN', 0) * P * D.get('busFee', 0) * T * 30) * cr if cfg.get('extra') else 0; fee = (rev + evRev + ext) * g('cardFee') / 100
ops = g('staff') + g('svc') + g('houseTax') + g('landTax') + g('insure') + g('util') + fee + evCost
sh = cfg.get('share') or {'mode': 'none'}; yrN = (rev + evRev + ext) * 12 / (1.05 if sh.get('taxIncl') else 1); share = 0
if sh['mode'] == 'fixed': share = max(0, yrN - g('rent') * 12 * 2 * 1.15) * g('shareRate') / 100 / 12
elif sh['mode'] == 'pct': share = yrN / 12 * g('shareRate') / 100
# 'pred'：預估年收入預設＝這個預設停車比例的一年營業額，所以預設下分成是 0
net = rev + evRev + ext - ops - g('rent') - share; preCost = D.get('preMonths', 0) * ((g('staff') + g('svc')) * D.get('preStaffPct', 100) / 100 + g('houseTax') + g('landTax') + g('insure') + g('util') + (g('rent') if D.get('preRent', 0) else 0)); pay = (g('open') + preCost) / net if net > 0 and g('open') > 0 else None
wan = lambda n: ('−' if n < 0 else '') + (f'{abs(n)/1e4:,.1f}'.rstrip('0').rstrip('.') + ' 萬' if abs(n) >= 1e4 else f'{abs(n):,.0f}')
paytxt = (f'{pay:.1f} 個月' if pay < 1200 else f'{pay/12:,.0f} 年') if pay else ('還沒算' if g('open') <= 0 else '回不了本')

short = lambda s: re.split(r'[；（(]', s or '', 1)[0]
o = [f'<style>{s1}</style><h1>{E(d["標題"])}</h1><h2 style="margin-top:8px">重點</h2><div class="kpis">']
o.append(f'<div class="kpi"><div class="l">停車格</div><div class="v">{N} 格</div><div class="s">{E(cfg.get("nNote",""))}</div></div>')
o.append(f'<div class="kpi"><div class="l">預計每月營業額（假設）</div><div class="v">{wan(rev + ext)}</div><div class="s">有停車的比例 {round(P*100)}%{"，含機車大型車 " + wan(ext) if ext else ""}</div></div>')
o.append(f'<div class="kpi"><div class="l">扣掉每月成本後（假設）</div><div class="v">{wan(net)}</div><div class="s">{E(cfg.get("netNote","有幾項成本先填 0"))}</div></div>')
o.append(f'<div class="kpi"><div class="l">回本時間（假設）</div><div class="v">{paytxt}</div><div class="s">{E(cfg.get("payNote",""))}</div></div></div>')
o.append(f'<div class="note">這幾個數字是下面「營業額和成本」的預設值，可以在那裡改數字。{E(d["狀態"])}</div>')
tx = d.get('提醒', [])
if len(tx) > 3: o.append(f'<details class="card" style="margin:8px 0"><summary>⚠ 要注意的事 {len(tx)} 條（點開）</summary>' + ''.join(f'<div class="note">⚠ {E(x)}</div>' for x in tx) + '</details>')
else:
    for x in tx: o.append(f'<div class="note">⚠ {E(x)}</div>')
o.append('<h2>投標</h2><div class="kpis">')
for c in d['卡']: o.append(f'<div class="kpi"><div class="l">{E(c["l"])}</div><div class="v">{E(c["v"])}</div><div class="s">{E(short(c["s"]))}</div></div>')
o.append('</div><div class="two"><div><h2>基本資料</h2><div class="rows">')
for r in d['基本資料']: o.append(f'<details><summary><span class="k">{E(r["k"])}</span><span class="a">{E(r["a"]).replace("&lt;br&gt;","<br>")}</span></summary><div class="src">{r["src"]}</div></details>')
o.append('</div><h2>要花的錢（明細）</h2><div class="rows cost">')
for r in d['要花的錢']: o.append(f'<details><summary><span class="k">{E(r["k"])}</span><span class="a"><b>{E(r["v"])}</b></span></summary><div class="src">{E(r["s"])}<br>{r["明細"]}</div></details>')
o.append(f'</div><div class="note">還沒算：{E(re.sub(r"^還沒算：", "", d["還沒算"]))}</div></div><div><h2>營業額和成本</h2>{panel}</div></div>')
o.append(gloss)
o.append('<h2>內部資料</h2><details class="card"><summary>投標 4 格的完整說明</summary><div class="src">' + '<br>'.join(f'<b>{E(c["l"])}</b>：{E(c["s"])}' for c in d['卡']) + '</div></details>')
doc = f'<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(d["標題"][:14])}</title><style>{head_css}</style></head><body><main>{"".join(o)}<style>.cp{{font:inherit;font-size:12.5px;border:1px solid var(--line);border-radius:6px;background:var(--card);color:var(--fg);padding:2px 8px;cursor:pointer;margin-left:6px}}.rows summary .a{{overflow-wrap:anywhere}}.kpi .v{{white-space:normal!important;overflow-wrap:anywhere}}{s2}.rows.cost summary .k{{white-space:normal;width:8.5em;min-width:8.5em!important}}</style><script>document.addEventListener("click",e=>{{const b=e.target.closest(".cp");if(!b)return;e.preventDefault();const t=b.dataset.cp;const done=()=>{{b.textContent="已複製";setTimeout(()=>b.textContent="複製路徑",1500)}};(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(done).catch(()=>{{const x=document.createElement("textarea");x.value=t;document.body.appendChild(x);x.select();try{{document.execCommand("copy");done()}}catch(_){{}}x.remove()}})}});</script></main></body></html>'
open(sys.argv[3], 'w', encoding='utf-8').write(doc)
print(d['標題'], '營業額', round(rev), '淨', round(net), '回本', paytxt)
import runpy, os as _os
_ff = runpy.run_path(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'fold_folder.py'))
_t = open(sys.argv[3], encoding='utf-8').read(); open(sys.argv[3], 'w', encoding='utf-8').write(_ff['fix'](_t)[0])
