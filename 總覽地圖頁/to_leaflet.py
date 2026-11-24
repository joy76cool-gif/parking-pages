import json, sys
src, js_p, out = sys.argv[1:4]
s = open(src, encoding='utf8').read()
a = s.index('/* 點一案：地圖放大'); b = s.index('})();', a) + 5
blk = s[a:b]
dec = json.JSONDecoder()
k = blk.index('PTS=') + 4; PTS, _ = dec.raw_decode(blk[k:])
k = blk.index('LOTS=') + 5; LOTS, _ = dec.raw_decode(blk[k:])
js = open(js_p, encoding='utf8').read().replace('__PTS__', json.dumps(PTS, ensure_ascii=False)).replace('__LOTS__', json.dumps(LOTS, ensure_ascii=False, separators=(',', ':')))
s = s[:a] + js + s[b:]
i = s.index('<svg class="tw" id="tw"'); j = s.index('</svg>', i) + 6
s = s[:i] + '<div id="lmap" class="lmap" role="region" aria-label="地圖：案子位置和附近停車場"></div>' + s[j:]
assert s.count('<div class="wrap">') == 1
s = s.replace('<div class="wrap">', '<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>\n<div class="wrap">', 1)
css = '''
/* Leaflet 1.9.4 需要的樣式（只留用到的部分，寫在頁面裡） */
.leaflet-pane,.leaflet-tile,.leaflet-marker-icon,.leaflet-marker-shadow,.leaflet-tile-container,.leaflet-pane>svg,.leaflet-pane>canvas,.leaflet-zoom-box,.leaflet-image-layer,.leaflet-layer{position:absolute;left:0;top:0}
.leaflet-container{overflow:hidden;-webkit-tap-highlight-color:transparent;background:#e9ece8;font-family:var(--sans);outline-offset:1px}
.leaflet-tile,.leaflet-marker-icon,.leaflet-marker-shadow{-webkit-user-select:none;user-select:none;-webkit-user-drag:none}
.leaflet-container img.leaflet-tile{max-width:none!important;max-height:none!important;padding:0}
.leaflet-tile{filter:inherit;visibility:hidden}.leaflet-tile-loaded{visibility:inherit}
.leaflet-container.leaflet-touch-zoom{touch-action:pan-x pan-y}.leaflet-container.leaflet-touch-drag{touch-action:none}
.leaflet-pane{z-index:400}.leaflet-tile-pane{z-index:200}.leaflet-overlay-pane{z-index:400}.leaflet-shadow-pane{z-index:500}.leaflet-marker-pane{z-index:600}.leaflet-tooltip-pane{z-index:650}.leaflet-popup-pane{z-index:700}
.leaflet-pane>svg path,.leaflet-tile-container{pointer-events:none}
.leaflet-pane>svg path.leaflet-interactive{pointer-events:visiblePainted;pointer-events:auto;cursor:pointer}
.leaflet-zoom-animated{transform-origin:0 0}
.leaflet-zoom-anim .leaflet-zoom-animated{transition:transform .25s cubic-bezier(0,0,.25,1)}
.leaflet-zoom-anim .leaflet-zoom-hide{visibility:hidden}
.leaflet-fade-anim .leaflet-tile{will-change:opacity}
.leaflet-control{position:relative;z-index:800;pointer-events:visiblePainted;pointer-events:auto;float:left;clear:both}
.leaflet-top,.leaflet-bottom{position:absolute;z-index:1000;pointer-events:none}.leaflet-top{top:0}.leaflet-right{right:0}.leaflet-bottom{bottom:0}.leaflet-left{left:0}
.leaflet-right .leaflet-control{float:right;margin-right:10px}.leaflet-top .leaflet-control{margin-top:10px}.leaflet-bottom .leaflet-control{margin-bottom:10px}.leaflet-left .leaflet-control{margin-left:10px}
.leaflet-bar{box-shadow:0 1px 5px rgba(0,0,0,.65);border-radius:6px}
.leaflet-bar a{background:#fff;color:#1d2321;border-bottom:1px solid #ccc;width:44px;height:44px;line-height:44px;display:block;text-align:center;text-decoration:none;font:bold 22px/44px sans-serif}
.leaflet-bar a:first-child{border-radius:6px 6px 0 0}.leaflet-bar a:last-child{border-radius:0 0 6px 6px;border-bottom:none}
.leaflet-bar a:focus-visible{outline:2px solid var(--link);outline-offset:1px}
.leaflet-bar a.leaflet-disabled{color:#9aa29e;background:#f4f4f4;cursor:default}
.leaflet-control-attribution{background:rgba(255,255,255,.85);margin:0!important;padding:0 6px;font-size:12px;color:#333}
.leaflet-control-attribution a{color:#1f4f8f}
.leaflet-attribution-flag{display:none!important}
.leaflet-tooltip{position:absolute;padding:1px 6px;background:#fff;color:#1d2321;border:1px solid #c7ccc9;border-radius:4px;white-space:nowrap;pointer-events:none;box-shadow:0 1px 3px rgba(0,0,0,.3);font-size:12.5px;line-height:1.5}
.leaflet-tooltip.lotlbl{color:#1f3f6b;font-weight:600}
.leaflet-tooltip.pinlbl{font-weight:700}
.lmap{width:100%;height:60vh;min-height:320px;border-radius:8px;border:1px solid var(--line)}
@media (min-width:1000px){.mapbox .lmap{height:calc(100vh - 110px)}}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .leaflet-tile-pane{filter:brightness(.82) contrast(1.05)}}
:root[data-theme="dark"] .leaflet-tile-pane{filter:brightness(.82) contrast(1.05)}
'''
s = s.replace('</style>', css + '</style>', 1)
open(out, 'w', encoding='utf8').write(s)
print('ok', len(s.encode('utf8')), len(PTS), len(LOTS))
