
/* 2026-11-24 改：底圖用國土測繪中心電子地圖（Leaflet）；一打開看全台灣、不先選案子；選到一案時 1 公里內停車場標出名字 */
(function(){
var PTS=__PTS__, LOTS=__LOTS__;
function km(a,b,c,d){var R=6371,x=(d-b)*Math.PI/180*Math.cos((a+c)/2*Math.PI/180),y=(c-a)*Math.PI/180;return R*Math.sqrt(x*x+y*y)}
var pan=document.getElementById('pan'),note=document.getElementById('mapnote'),box=document.getElementById('mapbox'),mapcol=document.getElementById('mapcol'),ttl=document.getElementById('mapttl');
var ds=[].slice.call(document.querySelectorAll('details[data-i]'));
var firstList=document.querySelectorAll('.list')[0];
var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
function kind(d){return firstList.contains(d)?'go':'chase'}
function title(d){var nm=d.querySelector('.nm').cloneNode(true);var x=nm.querySelectorAll('small,.dot,.rec');for(var i=0;i<x.length;i++)x[i].remove();return nm.textContent.trim()}
function esc(t){return String(t).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function cv(n){return getComputedStyle(document.documentElement).getPropertyValue(n).trim()}
function wide(){return matchMedia('(min-width:1000px)').matches}
var LEG='<span class="lg" style="background:var(--pin)"></span>在評估<span class="lg" style="background:var(--pin2)"></span>資料不夠<span class="lg" style="background:var(--sel)"></span>選到的案子<span class="lg" style="background:var(--lot)"></span>附近停車場　虛線圈＝1 公里';
var cur=null;
if(!window.L){note.textContent='地圖工具載不進來（網路擋住），清單和右邊細節照常可以看。';return}
var map=L.map('lmap',{zoomSnap:0.5,minZoom:6,maxZoom:19,zoomAnimation:!reduce,fadeAnimation:!reduce});
var tiles=L.tileLayer('https://wmts.nlsc.gov.tw/wmts/EMAP/default/GoogleMapsCompatible/{z}/{y}/{x}',{maxZoom:19,maxNativeZoom:19,attribution:'底圖：<a href="https://maps.nlsc.gov.tw/" target="_blank" rel="noopener">國土測繪中心</a>'}).addTo(map);
var bad=0;tiles.on('tileerror',function(){bad++;if(bad===6)note.textContent='底圖讀不到（可能是網路擋住國土測繪中心），案子的點和附近停車場照常標出。'});
var TW=L.latLngBounds([21.88,119.98],[25.32,122.02]);
function home(anim){map.fitBounds(TW,{padding:[8,8],animate:!!anim&&!reduce})}
var pinL=L.layerGroup().addTo(map),lotL=L.layerGroup().addTo(map);
function near(i){
  var rows=[];PTS[i].forEach(function(p){LOTS.forEach(function(Lt){var dk=km(p.lat,p.lon,Lt[0],Lt[1]);if(dk<=1)rows.push([dk,Lt,p])})});
  rows.sort(function(a,b){return a[0]-b[0]});
  var seen={},u=[];rows.forEach(function(r){var k=r[1][2]+r[1][0];if(!seen[k]){seen[k]=1;u.push(r)}});return u}
function drawPins(){
  pinL.clearLayers();
  ds.forEach(function(d,i){PTS[i].forEach(function(p){
    var sel=i===cur;
    var m=L.circleMarker([p.lat,p.lon],{radius:sel?10:8,color:'#ffffff',weight:2,fillColor:sel?cv('--sel'):(kind(d)==='go'?cv('--pin'):cv('--pin2')),fillOpacity:1,bubblingMouseEvents:false});
    m.bindTooltip(esc(title(d)),{direction:'top',offset:[0,-8],className:'pinlbl',permanent:sel});
    m.on('click',function(){openRow(i)});m.addTo(pinL)})});
}
function drawLots(){
  lotL.clearLayers();if(cur==null)return;
  PTS[cur].forEach(function(p){L.circle([p.lat,p.lon],{radius:1000,color:cv('--sel'),weight:1.5,dashArray:'5 4',fill:false,interactive:false}).addTo(lotL)});
  near(cur).forEach(function(r,n){var Lt=r[1];
    var m=L.circleMarker([Lt[0],Lt[1]],{radius:6,color:'#ffffff',weight:1.5,fillColor:cv('--lot'),fillOpacity:1});
    var nm=esc(Lt[2])+(Lt[4]?'・'+esc(Lt[4])+' 格':'');
    m.bindTooltip(nm,{direction:'right',offset:[6,0],className:'lotlbl',permanent:n<(wide()?8:4)});
    m.addTo(lotL)});
}
function nearList(i){
  var u=near(i);
  var html='<div class="near"><h4>附近 1 公里內的停車場：'+u.length+' 座</h4>';
  if(!u.length)html+='<p class="src">資料裡這個位置 1 公里內沒有登記的停車場（沒登記的民營小場不會出現）。</p>';
  else{html+='<ol>'+u.slice(0,15).map(function(r){var Lt=r[1];return '<li><span class="d">'+(r[0]<1?Math.round(r[0]*1000)+' 公尺':r[0].toFixed(1)+' 公里')+'</span><span><b>'+esc(Lt[2])+'</b>'+(Lt[4]?'・'+esc(Lt[4])+' 格':'')+(Lt[3]?'<small>'+esc(Lt[3])+'</small>':'')+'</span></li>'}).join('')+'</ol>';
    if(u.length>15)html+='<p class="src">地圖上最近幾座直接標名字（電腦 8 座、手機 4 座），其餘是藍點，滑鼠移上去或點一下看名稱。</p>'}
  html+='<p class="src">距離是從案子的點算的直線距離；有些點是行政區中心，只是大概位置，距離只能當參考。資料：交通部 TDX 各縣市路外停車場、臺北市停車管理工程處、新北市開放資料（2026-11-19 下載）。</p></div>';
  return html}
function bindCp(root){root.querySelectorAll('.cp').forEach(function(b){b.addEventListener('click',function(e){e.preventDefault();var c=b.previousElementSibling,t=c.textContent;function ok(){b.textContent='已複製';setTimeout(function(){b.textContent='複製'},1600)}function sl(){var r=document.createRange();r.selectNodeContents(c);var s=getSelection();s.removeAllRanges();s.addRange(r);b.textContent='按 Ctrl+C'}try{navigator.clipboard.writeText(t).then(ok,sl)}catch(x){sl()}})})}
function fitCase(i){var b=L.latLngBounds([]);PTS[i].forEach(function(p){b.extend(L.latLng(p.lat,p.lon).toBounds(2300))});map.fitBounds(b,{padding:[10,10],animate:!reduce,maxZoom:16})}
function pick(i){
  cur=i;var d=ds[i];ds.forEach(function(x){x.classList.remove('sel')});d.classList.add('sel');
  var sm=d.querySelector('.nm small'),dl=d.querySelector('.dl'),dls=dl.querySelector('small');
  var hw=[];PTS[i].forEach(function(p){var h=(p.n?p.n+'：':'')+p.how;if(hw.indexOf(h)<0)hw.push(h)});
  var head='<h3>'+esc(title(d))+'</h3><p class="sub">'+esc('截止 '+dl.firstChild.textContent+(dls?'（'+dls.textContent+'）':'')+(sm?'・'+sm.textContent:''))+'</p>';
  ttl.textContent=title(d);note.innerHTML=LEG;
  var where='<p class="src">地圖上案子的位置：'+esc(hw.join('；'))+'</p>';
  if(wide()){pan.innerHTML=head+d.querySelector('.more').innerHTML+nearList(i).replace('</div>',where+'</div>');bindCp(pan)}
  else{var mo=d.querySelector('.more'),nb=mo.querySelector('.near');if(nb)nb.remove();mo.insertAdjacentHTML('beforeend',nearList(i).replace('</div>',where+'</div>'));d.open=true;mo.insertBefore(box,mo.firstChild);map.invalidateSize()}
  drawPins();drawLots();fitCase(i);
}
function openRow(i){if(!wide()){ds[i].open=true}pick(i);if(!wide())ds[i].scrollIntoView({block:'start',behavior:reduce?'auto':'smooth'})}
function reset(){cur=null;ds.forEach(function(x){x.classList.remove('sel')});ttl.textContent='全台灣';note.innerHTML='點地圖上的點或清單裡的案子，地圖會放大到那附近，標出 1 公里內的停車場。'+'<br>'+LEG.replace(/<span class="lg" style="background:var\(--sel\)"><\/span>選到的案子/,'');pan.innerHTML='<p class="sub">點左邊地圖上的點，或中間清單的案子，這裡會出現細節和附近停車場。</p>';if(!wide()&&box.parentNode!==mapcol){mapcol.appendChild(box);map.invalidateSize()}drawPins();drawLots();home(true)}
document.getElementById('zall').addEventListener('click',reset);
ds.forEach(function(d,i){d.querySelector('summary').addEventListener('click',function(e){if(wide()){e.preventDefault();pick(i)}else{setTimeout(function(){if(d.open)pick(i)},0)}})});
addEventListener('resize',function(){if(wide()&&box.parentNode!==mapcol){mapcol.appendChild(box)}map.invalidateSize()});
reset();home(false);
})();
