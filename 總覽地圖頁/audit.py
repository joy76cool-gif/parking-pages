import pathlib, sys
from playwright.sync_api import sync_playwright
f = pathlib.Path(sys.argv[1]); out = f.parent
JS_T = """()=>Array.from(document.querySelectorAll('a,button,summary,[tabindex],.pin')).filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0}).map(e=>{const r=e.getBoundingClientRect();return [e.tagName+'.'+(e.className.baseVal!==undefined?e.className.baseVal:e.className),Math.round(r.width),Math.round(r.height)]}).filter(x=>x[1]<44||x[2]<44)"""
JS_C = """sel=>Array.from(document.querySelectorAll(sel)).slice(0,3).map(e=>{const c=getComputedStyle(e);function bg(n){while(n){const b=getComputedStyle(n).backgroundColor;if(b&&!b.endsWith(', 0)')&&b!=='transparent')return b;n=n.parentElement}return 'rgb(255,255,255)'}function L(s){const m=s.match(/[0-9.]+/g).map(Number).slice(0,3).map(v=>{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4)});return .2126*m[0]+.7152*m[1]+.0722*m[2]}const a=L(c.color),b=L(bg(e));return e.textContent.trim().slice(0,10)+' '+((Math.max(a,b)+.05)/(Math.min(a,b)+.05)).toFixed(2)+' '+c.fontSize})"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for name,w,h,sch,touch in [('1920',1920,900,'light',False),('375',375,800,'light',True),('320',320,700,'light',True),('375d',375,800,'dark',True)]:
        ctx = b.new_context(viewport={'width':w,'height':h}, color_scheme=sch, has_touch=touch, is_mobile=touch)
        pg = ctx.new_page(); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(f.as_uri()); pg.wait_for_timeout(1200)
        small = pg.evaluate(JS_T)
        from collections import Counter
        c = Counter((x[0][:30], x[1], x[2]) for x in small)
        print(name, 'sw', pg.evaluate('document.documentElement.scrollWidth'), 'errs', errs[:1])
        print('  small targets:', c.most_common(8))
        for s in ['.date','.steps span','.hint','.dl small','.nm small','.mapnote','.foot','.out']:
            print('  ', s, pg.evaluate(JS_C, s))
        pg.screenshot(path=str(out/f'a_{name}.png'))
        ctx.close()
    b.close()
