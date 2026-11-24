import sys
s = open(sys.argv[1], encoding='utf8').read()
def rep(a, b):
    global s
    assert s.count(a) == 1, a
    s = s.replace(a, b)
s = s.replace("querySelectorAll('small,.dot')", "querySelectorAll('small,.dot,.rec')")
# 1 一打開看全台，不先選案子
rep("if(wide())pick(0);else{drawMarks();note.textContent='點案子，地圖會跟著打開並放大到那附近。'}",
    "drawMarks();note.textContent='點地圖上的點或清單裡的案子，地圖會放大到那附近，標出 1 公里內停車場的名字。';if(wide())pan.innerHTML='<p class=\"sub\">點左邊地圖上的點，或中間清單的案子，這裡會出現細節和附近停車場。</p>';")
# 2 選到案子時，附近 1 公里內最近幾座停車場直接標名字
rep("if(zoomed){",
    "var NEAR={};if(cur!=null){var nr=[];PTS[cur].forEach(function(p){LOTS.forEach(function(L){var dk=km(p.lat,p.lon,L[0],L[1]);if(dk<=1)nr.push([dk,L])})});nr.sort(function(a,b){return a[0]-b[0]});var lim=wide()?8:4,cnt=0;nr.forEach(function(r){var k=r[1][2]+r[1][0];if(!(k in NEAR)&&cnt<lim){NEAR[k]=1;cnt++}})}\n  if(zoomed){")
rep("c.appendChild(t);lotsG.appendChild(c)});",
    "c.appendChild(t);lotsG.appendChild(c);if((L[2]+L[0]) in NEAR){var tx=el('text',{x:q[0]+5*sc,y:q[1]+4*sc,'class':'llbl','font-size':13*sc,'stroke-width':3.5*sc,'font-weight':'700'});tx.textContent=L[2]+(L[4]?'・'+L[4]+' 格':'');lotsG.appendChild(tx)}});")
# 3 每案加 Google 地圖連結
rep("var where='<p class=\"src\">地圖紅點位置：'+esc(hw.join('；'))+'</p>';",
    "var g=PTS[i][0];var where='<p class=\"src\"><a class=\"gmap\" href=\"https://www.google.com/maps/search/?api=1&query='+g.lat+','+g.lon+'\" target=\"_blank\" rel=\"noopener\">在 Google 地圖打開這附近（看街道） ↗</a></p><p class=\"src\">地圖紅點位置：'+esc(hw.join('；'))+'</p>';")
rep("藍色小方塊，滑鼠移上去看名稱", "藍色小方塊；最近幾座直接標名字，其餘滑鼠移上去看名稱")
open(sys.argv[2], 'w', encoding='utf8').write(s)
print('ok')
# 4 字的層次（11/24 Joy）＋案名全名提示
s = open(sys.argv[2], encoding='utf8').read()
css = open('font_fix.css', encoding='utf8').read()
a = s.index('</style>'); s = s[:a] + css + s[a:]
k = "drawMarks();note.textContent='點地圖上的點"
assert s.count(k) == 1
s = s.replace(k, "ds.forEach(function(d){var n=d.querySelector('.nm');n.title=n.textContent.replace(/\s+/g,' ').trim()});" + k, 1)
open(sys.argv[2], 'w', encoding='utf8').write(s)
print('ok2')
