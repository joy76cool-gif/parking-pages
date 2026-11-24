import json, sys, re, html, datetime as dt
src, stats_p, map_p, out = sys.argv[1:5]
s = open(src, encoding='utf8').read()
st = json.load(open(stats_p, encoding='utf8'))
cent = json.load(open(map_p, encoding='utf8'))['cent']
e = html.escape
TODAY = dt.date.today()
TD = '%d/%d（%s）' % (TODAY.month, TODAY.day, '一二三四五六日'[TODAY.weekday()])
WK = '一二三四五六日'
def wd(d):
    return sum(1 for i in range((d - TODAY).days + 1) if (TODAY + dt.timedelta(i)).weekday() < 5)
def md(d):
    return '%d/%d' % (d.month, d.day)
def T(n, how='行政區中心（案名或文件寫的區）'):
    c = cent[n]; return {'lon': c[0], 'lat': c[1], 'n': n, 'how': how}
def P(lon, lat, how):
    return {'lon': lon, 'lat': lat, 'n': '', 'how': how}

# 舊頁每案的公告和資料夾那兩列，照原樣搬
old = {}
for m in re.finditer(r'<details data-i="\d+">(.*?)</details>', s, re.S):
    blk = m.group(1)
    nm = re.search(r'<span class="nm">(.*?)<small>', blk).group(1)
    nm = re.sub(r'<[^>]+>', '', nm).strip()
    pub = re.search(r'<dt>公告</dt><dd>(.*?)</dd>', blk)
    fold = re.search(r'<dt>資料夾</dt><dd>(.*?)</dd>', blk)
    old[nm] = ((pub.group(1) if pub else ''), (fold.group(1) if fold else ''))

GO = [  # 數字都照各案評估頁試算區（11/24 讀）
 dict(k='蘆洲長安', d=dt.date(2026,11,26), t='17:00', rec=('可以考慮投','go'), pay='6.2 個月', yrs='合約 4 年', n='汽車 382 格', rev='174.1 萬', typ='委託經營', fee='4 年至少 4,081 萬（每月 85 萬）', roi='約 194%', dep='400 萬＋408.1 萬', miss='24 小時派人用參考值；42 項設備找不到舊價、18 項數量未確認，開辦費只算到下限 163.9 萬', url='https://claude.ai/artifact/EqVS422WXyYkjSwLVAre6P', pts=[P(121.461634, 25.080988, '門牌位置（新北市門牌位置資料）')]),
 dict(k='板橋信義國小', d=dt.date(2026,11,26), t='17:00', rec=('可以考慮投','go'), pay='16.7 個月', yrs='合約 4 年', n='汽車 259 格', rev='90.9 萬', typ='委託經營', fee='4 年至少 1,734 萬（每月 36.1 萬）', roi='約 72%', dep='249 萬＋173 萬', miss='47 項設備沒算（找不到舊價或數量未確認），回本會變長；地價稅、電費還是 0', url='https://claude.ai/artifact/Xs1EDFa42ygp3L1vENA5GS', pts=[P(121.452813, 24.991737, '門牌定位（案源 S2-16，假設）')]),
 dict(k='三芝、淡水 4 場', d=dt.date(2026,11,26), t='17:00', rec=('可以考慮投','go'), pay='1.4 個月', yrs='合約 6 年', n='汽車 875 格', rev='295.1 萬', typ='委託經營（4 場一案）', fee='6 年至少 2,248 萬（每月 31.2 萬）', roi='約 857%', dep='400 萬＋224.8 萬', miss='開辦費只算到下限 210 萬；停車比例 60% 是假設，三芝兩場在郊區，數字偏樂觀', url='https://claude.ai/artifact/1wqHvZtdX2yXAYGrwWek6v', pts=[T('新北市三芝區'), T('新北市淡水區')]),
 dict(k='臺南林森 ROT', d=dt.date(2026,11,26), t='17:00', rec=('要再看','chase'), pay='139.6 個月（約 11.6 年）', yrs='合約 20 年', n='汽車 545 格、機車 857 格', rev='137.9 萬', typ='ROT（整修後經營）', fee='每年至少 50 萬', roi='約 8.6%', dep='100 萬＋1,000 萬', miss='整修投資用契約下限 1 億；房屋稅還是 0', url='https://claude.ai/artifact/5LMiU3WqzH9zEzQXQFPudP', pts=[P(120.217248, 22.982316, '林森路一段與崇德路口（案源 S2-16，新聞寫的位置，假設）')]),
 dict(k='高雄鳳山停 9 BOT', d=dt.date(2026,12,18), t='17:00', rec=('不建議','no'), pay='182 年', yrs='營運約 46 年', n='至少 566 格（要自己蓋）', rev='153.6 萬', typ='BOT（新建後經營）', fee='每年至少 300 萬，另開發權利金 100 萬', roi='約 0.5%', dep='500 萬＋2,000 萬', miss='工程費是線索（附近案例推算）；停車場算不算在總樓地板面積裡，契約沒寫，未確認', url='https://claude.ai/artifact/ASowSTTXQcb7Xipnki1g6a', pts=[T('高雄市鳳山區')]),
]
OLDKEY = {'蘆洲長安':'蘆洲長安','板橋信義國小':'板橋信義國小','三芝、淡水 4 場':'三芝、淡水 4 場','臺南林森 ROT':'臺南林森 ROT','高雄鳳山停 9 BOT':'高雄鳳山停 9 BOT'}
LOCMISS = {
 '東港鎮路外停車場委託經營管理': [T('屏東縣東港鎮')],
 '116年度屏東縣遙控無人機飛行場及附屬停車場維護及管理': [T('屏東縣屏東市', '行政區中心（機關所在地，場地位置公告沒寫，假設）')],
 '潮州鎮第一公有零售市場停車場收費管理及維護工作': [T('屏東縣潮州鎮')],
 '臺北市北投區溫泉段三小段175等地號暨財政部國產署161等地號部分土地': [T('臺北市北投區')],
 '瑠公管理處 115 年度第 8 批 (2處土地) 農田水利非事業用不動產公開標租案': [T('臺北市大安區', '行政區中心（土地位置公告頁沒寫，用機關所在地，假設）')],
 '新北市鶯歌區國姓段616地號部分土地標租案': [T('新北市鶯歌區')],
 '本校羽球場、停車場場地出租公開標租案3年': [T('臺中市北區', '行政區中心（學校所在地，假設）')],
 '高雄巿鹽埕區鹽北段201等30筆地號部分土地，面積：4,613.88㎡': [T('高雄市鹽埕區')],
 '116年度委託民間保全業者辦理拖吊場警衛勤務業務': [T('臺中市西屯區', '行政區中心（機關所在地，拖吊場位置沒寫，假設）')],
 '116年度臺中市公有停車場監視、求救及車位傳輸設備維護工作開口契約': [T('臺中市西屯區', '行政區中心（機關所在地，多場合約，假設）')],
 '「基隆市過港路二、東勢街26巷及工建路平面停車場委託專業服務經營管理勞務採購」案決標公告': [T('基隆市仁愛區', '行政區中心（3 場位置沒對門牌，假設）')],
}
pts = []; go_html = []; i = 0
for c in GO:
    pub, fold = old.get(OLDKEY[c['k']], ('', ''))
    left = wd(c['d'])
    go_html.append(
      '<details data-i="%d"><summary><span class="dl">%s<small>剩 %d 個工作天</small></span>'
      '<span class="nm"><span class="rec %s">%s</span> %s<small>回本 %s／%s（假設）</small></span></summary>\n'
      '<div class="more"><dl><dt>建議</dt><dd>%s（照目前試算，都是假設）</dd><dt>截止</dt><dd>%s（%s）%s</dd><dt>回本</dt><dd>%s／%s（假設）</dd>'
      '<dt>格數</dt><dd>%s</dd><dt>每月營業額</dt><dd>%s（假設）</dd><dt>類型</dt><dd>%s</dd><dt>權利金</dt><dd>%s</dd><dt>投報率</dt><dd>%s／年（假設）</dd><dt>先押</dt><dd>%s</dd>'
      '<dt>還缺</dt><dd>%s</dd><dt>評估頁</dt><dd><a href="%s" target="_blank" rel="noopener">看怎麼算 ↗</a></dd>%s%s</dl></div></details>'
      % (i, md(c['d']), left, c['rec'][1], c['rec'][0], e(c['k']), e(c['pay']), e(c['yrs']),
         c['rec'][0], md(c['d']), WK[c['d'].weekday()], c['t'], e(c['pay']), e(c['yrs']),
         e(c['n']), e(c['rev']), e(c['typ']), e(c['fee']), e(c['roi']), e(c['dep']), e(c['miss']), c['url'],
         ('<dt>公告</dt><dd>%s</dd>' % pub) if pub else '', ('<dt>資料夾</dt><dd>%s</dd>' % fold) if fold else ''))
    pts.append(c['pts']); i += 1
miss = sorted(st['缺資料清單'], key=lambda x: x['截止'] if x['截止'][:2]=='20' else '9')
ch_html = []
for x in miss:
    d = x['截止'][:10]
    if d[:2] == '20':
        dd = dt.date.fromisoformat(d); dl = '%s<small>剩 %d 個工作天</small>' % (md(dd), wd(dd))
    else:
        dl = '沒寫<small>公告沒寫截止</small>'
    ch_html.append(
      '<details data-i="%d"><summary><span class="dl">%s</span><span class="nm"><span class="dot" style="background:var(--chase)"></span>%s<small>%s</small></span></summary>\n'
      '<div class="more"><dl><dt>機關</dt><dd>%s</dd><dt>類別</dt><dd>%s</dd><dt>缺什麼</dt><dd>%s</dd><dt>為什麼缺</dt><dd>%s</dd><dt>下一步</dt><dd>%s</dd><dt>公告</dt><dd><a href="%s" target="_blank" rel="noopener">公告 ↗</a></dd></dl></div></details>'
      % (i, dl, e(x['案名']), e(x['缺什麼']), e(x['機關']), e(x['類別']), e(x['缺什麼']), e(x['為什麼缺']), e(x['誰處理']), e(x['公告網址'])))
    pts.append(LOCMISS[x['案名']]); i += 1
F = {f['層'][0]: f['件數'] for f in st['漏斗']}

C = st['各類別件數']
NOT13 = [  # 2026-11-24 對案源清單逐列核對；每天要重看（新案、已截止）
 ('大寮三場', '妳 11/20 選不投'),
 ('新竹香山停1', '11/26 截止，雷達抓到時離截止已不到 4 個工作天，照規則不做'),
 ('桃園農業局租公務車位', '是機關要租車位，不是給我們經營'),
 ('屏東新街段土地', '合約不到 3 年'),
 ('116 年度公務汽車停車位租賃案', '政府付錢的採購案，走另一條流程'),
]
WHY = ('<div class="why"><b>每一步少掉的是什麼</b><ul>'
 '<li>%d → %d：另外 %d 件是土地標租、標售（空地，不是現成的停車場標案）</li>' % (F['1'], F['2'], F['1'] - F['2']) +
 '<li>%d → %d：另外 %d 件不是我們經營的：工程 %d、維運 %d（政府付錢請人顧停車場）、設備銷售 %d、充電樁或保管場 %d</li>' % (F['2'], F['3'], F['2'] - F['3'], C['工程'], C['維運'], C['設備銷售'], C['充電樁保管場']) +
 '<li>%d → %d：另外 %d 件缺車位數或合約年數，列在下面「資料不夠」</li>' % (F['3'], F['4'], F['3'] - F['4']) +
 '<li>%d 件 → 5 案在評估：同一案有兩列的合併（停9、林森、大寮），剩 10 案；其中 5 案在評估，另外 5 案：%s</li>' % (F['4'], '；'.join('%s（%s）' % x for x in NOT13)) +
 '</ul></div>\n')
col = ('<div class="colL">\n<p class="date">' + TD + '・ 雷達 %s 跑完 ・ 只算還在招標的</p>\n'
 '<p class="lead">在評估的有 <em>5 案</em>，最近的 4 案都是 11/26（四）截止；另有 %d 件資料不夠。</p>\n'
 '<div class="steps"><div><b>%d</b><span>掃到</span></div><div><b>%d</b><span>停車場</span></div><div><b>%d</b><span>經營</span></div><div><b>%d</b><span>資料夠</span></div><div><b>5 案</b><span>評估中</span></div></div>\n'

 + WHY +
 '<h2 class="go"><span class="n">5</span>案在評估<span class="hint" style="margin:0">建議是照試算用規則分的</span></h2>\n'
 '<p class="hint">照截止日排。點一下看格數、營業額、權利金、投報率和評估頁。建議規則：回本不到合約一半＝可以考慮投；一半到整個合約＝要再看；超過合約＝不建議。</p>\n'
 '<div class="list">\n%s\n</div>\n'
 '<p class="out">沒投：高雄大寮三場（11/20 妳選不投）、宜蘭第二行政中心（11/19 妳選不投）、七堵停3 和臺北羅斯福路（11/19 截止前不到 4 個工作天先不處理）、彰化南郭路（11/17 已截止）。</p>\n'
 '<h2 class="chase"><span class="n">%d</span>件資料不夠</h2>\n<p class="hint">照截止日排。點一下看缺什麼、為什麼缺、下一步誰做。</p>\n'
 '<div class="list">\n%s\n</div>\n'
 '<p class="foot">數字出處：雷達每日統計 %s；評估中 5 案的數字照各案評估頁的試算（11/24 讀）。剩幾個工作天從 ' + TD + ' 算，含今天和截止日。資料不夠這張有 %d 件，比「經營 − 資料夠」的 %d 件多，因為也包含維運、保管場這類還看不出誰付錢的案子。</p>\n'
 ) % (st['製表時間'][-5:], len(miss), F['1'], F['2'], F['3'], F['4'], '\n'.join(go_html), len(miss), '\n'.join(ch_html), st['製表時間'], len(miss), F['3'] - F['4'])
a = s.index('<div class="colL">'); b = s.index('<aside class="pan"')
# colL 後面原本有一個關閉 colL 的 </div>
tail = s[a:b]; close = tail.rstrip()
assert close.endswith('</div>')
s = s[:a] + col + '</div>' + s[b:]
# 地圖點
k = s.index('PTS=') + 4
old_pts, end = json.JSONDecoder().raw_decode(s[k:])
s = s[:k] + json.dumps(pts, ensure_ascii=False) + s[k + end:]
# 樣式：建議標籤、手機觸控
css = ('.rec{display:inline-block;font-size:.78rem;font-weight:700;border:1.5px solid currentColor;border-radius:4px;padding:0 6px;margin-right:4px;line-height:1.5;white-space:nowrap}'
       '.rec.go{color:var(--go)}.rec.chase{color:var(--chase)}.rec.no{color:#b3261e}'
       '@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .rec.no{color:#ff8a80}}:root[data-theme="dark"] .rec.no{color:#ff8a80}'
       '@media (pointer:coarse){.more a{display:inline-flex;align-items:center;min-height:44px}.tw .pin{stroke-width:32;stroke:transparent;paint-order:stroke}}'
       ':root{--muted:#646d69}@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--muted:#a1aba6}}:root[data-theme="dark"]{--muted:#a1aba6}')
s = s.replace('</style>', css + '</style>', 1)
open(out, 'w', encoding='utf8').write(s)
print('ok', i, len(pts), len(old_pts))
